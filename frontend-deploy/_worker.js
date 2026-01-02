/**
 * Cloudflare Worker for qamoos.org
 * Proxies /api/* requests to Google Cloud Run backend
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // IMPORTANT: Serve JSON files directly without any processing
    if (url.pathname.endsWith('.json')) {
      return env.ASSETS.fetch(request);
    }
    
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': 'https://qamoos.org',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
        }
      });
    }
    
    // Proxy /api/* requests to Google Cloud Run
    if (url.pathname.startsWith('/api/')) {
      const backendUrl = env.BACKEND_URL || 'https://qamoos-api-804325795495.us-east1.run.app';
      const targetUrl = backendUrl + url.pathname + url.search;
      
      console.log(`Proxying: ${url.pathname} -> ${targetUrl}`);
      
      // Forward request to backend
      const backendRequest = new Request(targetUrl, {
        method: request.method,
        headers: request.headers,
        body: request.body,
      });
      
      const response = await fetch(backendRequest);
      
      // Clone response and add CORS headers
      const newResponse = new Response(response.body, response);
      newResponse.headers.set('Access-Control-Allow-Origin', 'https://qamoos.org');
      newResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
      newResponse.headers.set('Access-Control-Allow-Headers', 'Content-Type');
      newResponse.headers.set('Cache-Control', 'public, max-age=300'); // Cache for 5 minutes
      
      return newResponse;
    }
    
    // For non-API requests, serve from Cloudflare Pages
    return env.ASSETS.fetch(request);
  }
};
