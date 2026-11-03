/* Rende il sito utilizzabile anche senza rete: la pagina si aggiorna appena c'è connessione, il resto resta in cache. */
const CACHE = 'casa-v3';
const CORE = ['./', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'apple-touch-icon.png'];
const LIBS = [
  'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',
  'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js',
  'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(async c => {
    await c.addAll(CORE);
    await Promise.all(LIBS.map(u => c.add(u).catch(() => {})));
    await self.skipWaiting();
  }));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

async function fromNetwork(req, key) {
  const res = await fetch(req);
  if (res.ok || res.type === 'opaque') (await caches.open(CACHE)).put(key || req, res.clone());
  return res;
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  if (req.mode === 'navigate') {
    e.respondWith(fromNetwork(req).catch(() => caches.match(req, {ignoreSearch: true}).then(hit => hit || caches.match('./'))));
    return;
  }
  // I file del sito (dati dei materiali, Excel) prima dalla rete, così non restano vecchi; le librerie dalla cache.
  if (new URL(req.url).origin === location.origin) {
    e.respondWith(fromNetwork(req).catch(() => caches.match(req)));
    return;
  }
  e.respondWith(caches.match(req).then(hit => {
    const net = fromNetwork(req);
    if (hit) { net.catch(() => {}); return hit; }
    return net;
  }));
});
