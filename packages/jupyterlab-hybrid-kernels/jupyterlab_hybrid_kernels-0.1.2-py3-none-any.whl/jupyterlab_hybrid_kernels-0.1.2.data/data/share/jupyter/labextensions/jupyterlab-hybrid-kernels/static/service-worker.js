"use strict";
// eslint-disable-next-line @typescript-eslint/triple-slash-reference
/// <reference path="../../../node_modules/@types/serviceworker/index.d.ts" />
/**
 * The name of the cache
 */
const CACHE = 'precache';
/**
 * Communication channel for drive access
 */
const broadcast = new BroadcastChannel('/api/drive.v1');
/**
 * Whether to enable the cache
 */
let enableCache = false;
/**
 * Install event listeners
 */
self.addEventListener('install', onInstall);
self.addEventListener('activate', onActivate);
self.addEventListener('fetch', onFetch);
// Event handlers
/**
 * Handle installation with the cache
 */
function onInstall(event) {
    void self.skipWaiting();
    event.waitUntil(cacheAll());
}
/**
 * Handle activation.
 */
function onActivate(event) {
    // check if we should enable the cache
    const searchParams = new URL(location.href).searchParams;
    enableCache = searchParams.get('enableCache') === 'true';
    event.waitUntil(self.clients.claim());
}
/**
 * Handle fetching a single resource.
 */
async function onFetch(event) {
    const { request } = event;
    const url = new URL(event.request.url);
    if (url.pathname === '/api/service-worker-heartbeat') {
        event.respondWith(new Response('ok'));
        return;
    }
    let responsePromise = null;
    if (shouldBroadcast(url)) {
        responsePromise = broadcastOne(request);
    }
    else if (!shouldDrop(request, url)) {
        responsePromise = maybeFromCache(event);
    }
    if (responsePromise) {
        event.respondWith(responsePromise);
    }
}
// utilities
/** Get a cached response, and update cache. */
async function maybeFromCache(event) {
    const { request } = event;
    if (!enableCache) {
        return await fetch(request);
    }
    let response = await fromCache(request);
    if (response) {
        event.waitUntil(refetch(request));
    }
    else {
        response = await fetch(request);
        event.waitUntil(updateCache(request, response.clone()));
    }
    return response;
}
/**
 * Restore a response from the cache based on the request.
 */
async function fromCache(request) {
    const cache = await openCache();
    const response = await cache.match(request);
    if (!response || response.status === 404) {
        return null;
    }
    return response;
}
/**
 * This is where we call the server to get the newest version of the
 * file to use the next time we show view
 */
async function refetch(request) {
    const fromServer = await fetch(request);
    await updateCache(request, fromServer);
    return fromServer;
}
/**
 * Whether a given URL should be broadcast
 */
function shouldBroadcast(url) {
    return url.origin === location.origin && url.pathname.includes('/api/drive');
}
/**
 * Whether the fallback behavior should be used
 */
function shouldDrop(request, url) {
    return (request.method !== 'GET' ||
        url.origin.match(/^http/) === null ||
        url.pathname.includes('/api/'));
}
/**
 * Forward request to main using the broadcast channel
 */
async function broadcastOne(request) {
    const message = await request.json();
    const promise = new Promise((resolve) => {
        const messageHandler = (event) => {
            const data = event.data;
            if (data.browsingContextId !== message.browsingContextId) {
                // bail if the message is not for us
                return;
            }
            const response = data.response;
            resolve(new Response(JSON.stringify(response)));
            broadcast.removeEventListener('message', messageHandler);
        };
        broadcast.addEventListener('message', messageHandler);
    });
    broadcast.postMessage(message);
    return await promise;
}
async function openCache() {
    return await caches.open(CACHE);
}
/**
 * Cache a request/response pair.
 */
async function updateCache(request, response) {
    const cache = await openCache();
    return cache.put(request, response);
}
/**
 * Add all to the cache
 *
 * this is where we should (try to) add all relevant files
 */
async function cacheAll() {
    const cache = await openCache();
    return await cache.addAll([]);
}
//# sourceMappingURL=service-worker.js.map