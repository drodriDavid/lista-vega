// Necesario para poder instalar la lista como app y recibir enlaces compartidos.
// No guarda nada en caché: todo se pide siempre a la red.
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", () => {});
