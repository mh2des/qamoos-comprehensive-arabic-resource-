// Minimal service worker for PWA functionality// Service Worker DISABLED - causing caching issues

self.addEventListener('install', () => {// This file is now empty to prevent caching problems during development

    self.skipWaiting();

});self.addEventListener('install', (event) => {

  self.skipWaiting();

self.addEventListener('activate', event => {});

    event.waitUntil(self.clients.claim());

});self.addEventListener('activate', (event) => {

  event.waitUntil(

self.addEventListener('fetch', () => {    caches.keys().then((cacheNames) => {

    // No-op - let all requests pass through      return Promise.all(

});        cacheNames.map((cacheName) => {

          return caches.delete(cacheName);
        })
      );
    }).then(() => self.clients.claim())
  );
});

// No caching - just let all requests pass through
self.addEventListener('fetch', (event) => {
  return;
});

// Install event - cache essential files
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[ServiceWorker] Pre-caching essential files');
        return cache.addAll(PRECACHE_URLS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
            console.log('[ServiceWorker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // API requests - Network first, cache fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      caches.open(RUNTIME_CACHE).then((cache) => {
        return fetch(request)
          .then((response) => {
            // Cache successful API responses
            if (response.ok) {
              cache.put(request, response.clone());
            }
            return response;
          })
          .catch(() => {
            // Fallback to cache if network fails
            return cache.match(request).then((cached) => {
              return cached || new Response(
                JSON.stringify({ error: 'Offline - cached data not available' }),
                { headers: { 'Content-Type': 'application/json' } }
              );
            });
          });
      })
    );
    return;
  }

  // HTML pages - Cache first, network fallback
  if (request.destination === 'document') {
    event.respondWith(
      caches.match(request).then((cached) => {
        return cached || fetch(request).then((response) => {
          return caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, response.clone());
            return response;
          });
        });
      })
    );
    return;
  }

  // Other assets (CSS, JS, images) - Cache first
  event.respondWith(
    caches.match(request).then((cached) => {
      return cached || fetch(request).then((response) => {
        // Don't cache if not successful
        if (!response || response.status !== 200 || response.type === 'error') {
          return response;
        }

        return caches.open(RUNTIME_CACHE).then((cache) => {
          cache.put(request, response.clone());
          return response;
        });
      });
    })
  );
});

// Background sync for offline searches (future enhancement)
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-searches') {
    event.waitUntil(syncSearches());
  }
});

async function syncSearches() {
  // Placeholder for syncing offline searches when back online
  console.log('[ServiceWorker] Syncing offline searches');
}

// Push notifications (future enhancement)
self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'New update available!',
    icon: '/icon-192.png',
    badge: '/icon-96.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    }
  };

  event.waitUntil(
    self.registration.showNotification('القاموس', options)
  );
});
