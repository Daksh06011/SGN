// Runtime backend URL placeholder
// Replace the value below with your deployed backend URL (no trailing slash),
// or let Vercel/Git host replace this file at deploy time.
window.__BACKEND_URL = window.__BACKEND_URL || 'https://<RAILWAY_BACKEND_URL>';

// Example: window.__BACKEND_URL = 'https://my-backend.up.railway.app'

console.info('[INIT] backend URL set to', window.__BACKEND_URL);
