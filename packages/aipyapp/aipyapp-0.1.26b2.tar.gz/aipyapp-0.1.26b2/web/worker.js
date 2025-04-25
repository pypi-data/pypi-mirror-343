// Cloudflare Worker for receiving files and storing in R2
// Enhanced with version checking endpoint and client data storage

// Cache for PyPI version information
const CACHE_TTL = 3600; // Cache time-to-live in seconds (1 hour)
let versionCache = {
  lastFetched: 0,
  latestVersion: null
};

// 生成随机ID
function generateRandomId() {
  return crypto.randomUUID();
}

export default {
  async fetch(request, env) {
    // 定义随机路径
    const secretPath = env.SECRET_PATH || "upload_s3cr3t_p4th";
    const versionCheckPath = env.VERSION_CHECK_PATH || "check_version";
    const viewPath = env.VIEW_PATH || "view";
    
    // 获取请求的 URL 路径
    const url = new URL(request.url);
    const requestPath = url.pathname.replace(/^\/+/, '');
    
    // 处理文件查看请求
    if (request.method === "GET" && requestPath.startsWith(viewPath)) {
      return await handleFileView(request, env);
    }
    
    // 其他请求必须是 POST
    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405 });
    }
    
    // Get user's IP address
    const clientIP = request.headers.get("cf-connecting-ip") || "unknown-ip";
    
    try {
      // 根据路径分发请求
      if (requestPath === versionCheckPath) {
        return await handleVersionCheck(request, env, clientIP);
      } else if (requestPath === secretPath) {
        // 处理文件上传
        return await handleFileUpload(request, env, clientIP);
      } else {
        // 请求路径不匹配任何已知端点
        return new Response("Not found", { status: 404 });
      }
    } catch (error) {
      console.error("Error processing request:", error);
      return new Response(JSON.stringify({
        success: false,
        error: "Internal server error"
      }), {
        status: 500,
        headers: { "Content-Type": "application/json" }
      });
    }
  }
};

/**
 * Handle file upload request
 */
async function handleFileUpload(request, env, clientIP) {
  try {
    // 检查 API-KEY
    const apiKey = request.headers.get("API-KEY");
    if (!apiKey || apiKey !== env.API_KEY) {
      return new Response("Unauthorized", { status: 401 });
    }

    // Get the uploaded file from the request
    const formData = await request.formData();
    const file = formData.get("file");
    if (!file || !(file instanceof File)) {
      return new Response("No file uploaded", { status: 400 });
    }
    
    // 生成随机ID作为文件名
    const fileId = generateRandomId();
    
    // 获取文件扩展名
    const originalFileName = file.name;
    const fileExtension = originalFileName.includes('.')
      ? originalFileName.substring(originalFileName.lastIndexOf('.'))
      : '';
    
    // 创建文件路径: {fileId}{extension}
    const filePath = `${fileId}${fileExtension}`;
    
    // Upload the file to R2
    await env.AIPY_BUCKET.put(filePath, file.stream(), {
      contentType: file.type,
      customMetadata: {
        originalName: file.name,
        uploadedBy: clientIP,
        uploadDate: new Date().toISOString(),
        fileId: fileId
      }
    });
    
    // 生成查看文件的URL，直接使用完整的文件路径
    const requestUrl = new URL(request.url);
    const viewUrl = `${requestUrl.origin}/${env.VIEW_PATH || 'view'}/${filePath}`;
    
    return new Response(JSON.stringify({
      success: true,
      viewUrl: viewUrl
    }), {
      headers: {
        "Content-Type": "application/json"
      }
    });
  } catch (error) {
    console.error("Error uploading file:", error);
    return new Response(JSON.stringify({
      success: false,
      error: "File upload failed"
    }), {
      status: 500,
      headers: {
        "Content-Type": "application/json"
      }
    });
  }
}

/**
 * Handle file view request
 */
async function handleFileView(request, env) {
  try {
    const url = new URL(request.url);
    const filePath = url.pathname.split('/').slice(2).join('/'); // 移除 /view/ 前缀
    
    if (!filePath) {
      return new Response("File path not specified", { status: 400 });
    }
    
    // 从 R2 获取文件
    const object = await env.AIPY_BUCKET.get(filePath);
    
    if (!object) {
      return new Response("File not found", { status: 404 });
    }
    
    // 优先使用 R2 中存储的 content-type
    let contentType = object.httpMetadata?.contentType;
    
    // 如果没有存储的 content-type，则根据扩展名设置
    if (!contentType) {
      if (filePath.endsWith('.html')) {
        contentType = 'text/html';
      } else if (filePath.endsWith('.json')) {
        contentType = 'application/json';
      } else if (filePath.endsWith('.txt')) {
        contentType = 'text/plain';
      } else if (filePath.endsWith('.py')) {
        contentType = 'text/x-python';
      } else {
        contentType = 'application/octet-stream';
      }
    }
    
    // 返回文件内容，设置 inline 显示
    return new Response(object.body, {
      headers: {
        'Content-Type': contentType,
        'Content-Disposition': 'inline',
        'Access-Control-Allow-Origin': '*'
      }
    });
  } catch (error) {
    console.error("Error viewing file:", error);
    return new Response(JSON.stringify({
      success: false,
      error: "File view failed"
    }), {
      status: 500,
      headers: {
        "Content-Type": "application/json"
      }
    });
  }
}

/**
 * Handle version check request and store client data
 */
async function handleVersionCheck(request, env, clientIP) {
  try {
    // Get client data from the request
    let clientData;
    const contentType = request.headers.get("Content-Type") || "";
    
    if (contentType.includes("application/json")) {
      clientData = await request.json();
    } else {
      return new Response("Invalid content type. Expected application/json", { 
        status: 400,
        headers: { "Content-Type": "application/json" }
      });
    }
    
    // Extract client information
    const { xid = "", version = "unknown", meta = {} } = clientData;
    
    // Store client data in D1 database
    try {
      const timestamp = new Date().toISOString();
      
      // Create clients table if it doesn't exist (with flexible meta field)
      await env.CLIENTS_DB.prepare(`
        CREATE TABLE IF NOT EXISTS clients (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          xid TEXT,
          ip TEXT,
          version TEXT,
          timestamp TEXT,
          meta TEXT
        )
      `).run();
      
      // Convert meta object to JSON string
      const metaJson = JSON.stringify(meta);
      
      // Insert client data
      await env.CLIENTS_DB.prepare(`
        INSERT INTO clients (xid, ip, version, meta, timestamp)
        VALUES (?, ?, ?, ?, ?)
      `).bind(xid, clientIP, version, metaJson, timestamp).run();
      
    } catch (dbError) {
      console.error("Database error:", dbError);
      // Continue execution even if database operation fails
    }
    
    // Check if we need to fetch new version data from PyPI
    const currentTime = Math.floor(Date.now() / 1000);
    if (!versionCache.latestVersion || (currentTime - versionCache.lastFetched) > CACHE_TTL) {
      try {
        const pypiResponse = await fetch("https://pypi.org/pypi/aipyapp/json");
        
        if (pypiResponse.ok) {
          const pypiData = await pypiResponse.json();
          versionCache = {
            lastFetched: currentTime,
            latestVersion: pypiData.info.version
          };
        } else {
          console.error("PyPI API error:", pypiResponse.status);
          // If we can't fetch new data but have cached data, continue using it
          if (!versionCache.latestVersion) {
            return new Response(JSON.stringify({
              success: false,
              error: "Could not retrieve version information"
            }), {
              status: 502,
              headers: { "Content-Type": "application/json" }
            });
          }
        }
      } catch (pypiError) {
        console.error("PyPI fetch error:", pypiError);
        // If we can't fetch new data but have cached data, continue using it
        if (!versionCache.latestVersion) {
          return new Response(JSON.stringify({
            success: false,
            error: "Could not retrieve version information"
          }), {
            status: 502,
            headers: { "Content-Type": "application/json" }
          });
        }
      }
    }
    
    // Compare versions and return result
    const hasUpdate = compareVersions(version, versionCache.latestVersion);
    
    // 可以根据需要在响应中添加更多信息
    return new Response(JSON.stringify({
      success: true,
      latest_version: versionCache.latestVersion,
      has_update: hasUpdate,
      cache_time_remaining: CACHE_TTL - (currentTime - versionCache.lastFetched)
    }), {
      headers: { "Content-Type": "application/json" }
    });
    
  } catch (error) {
    console.error("Version check error:", error);
    return new Response(JSON.stringify({
      success: false,
      error: "Internal server error"
    }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}

/**
 * 比较两个版本号，判断是否需要更新
 * @param {string} clientVersion - 客户端版本号
 * @param {string} latestVersion - 最新版本号
 * @returns {boolean} - 如果需要更新，返回 true；否则返回 false
 */
function compareVersions(clientVersion, latestVersion) {
  const parseVersion = (v) => {
    // 匹配主版本、次版本、修订版本和可选的 beta 版本号
    const match = v.match(/^(\d+)\.(\d+)\.(\d+)(?:b(\d+))?$/);
    if (!match) return [0, 0, 0, Infinity]; // 不匹配时认为是最低版本

    const [, major, minor, patch, beta] = match;
    return [
      parseInt(major, 10),
      parseInt(minor, 10),
      parseInt(patch, 10),
      beta ? parseInt(beta, 10) : Infinity
    ];
  };

  const c = parseVersion(clientVersion);
  const l = parseVersion(latestVersion);

  for (let i = 0; i < 4; i++) {
    if (c[i] < l[i]) return true;
    if (c[i] > l[i]) return false;
  }

  return false; // 版本完全相同
}
