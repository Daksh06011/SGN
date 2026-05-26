DEPLOY CHECKLIST — Backend (Railway) & Frontend (Vercel)

Summary
- Backend: `backend/` contains a standalone Flask + Socket.IO app; production worker configured for `gevent` in `backend/Procfile`.
- Frontend: `frontend/` contains static site; runtime backend URL helper at `frontend/set_backend_url.js` and a `frontend/vercel.json` rewrite placeholder.

Before you deploy (local checks)
- Ensure your repo has recent changes committed.
- Edit runtime placeholders:
  - Replace `<RAILWAY_BACKEND_URL>` in `frontend/vercel.json` or set `window.__BACKEND_URL` in `frontend/set_backend_url.js`.
- Test locally (dev):

Backend (dev):
```bash
python backend/app.py
# server should start on http://127.0.0.1:5000
```

Frontend (static serve):
```bash
cd frontend
python -m http.server 8000
# open http://127.0.0.1:8000
```

Quick API checks (local):
```bash
# demo devices (public)
curl http://127.0.0.1:5000/api/demo/devices

# protected endpoint (should return 401 without JWT)
curl -v "http://127.0.0.1:5000/api/data?device_id=5&hours=1"
```

Railway (backend) — deploy
1. Create a Railway project and connect to your repo OR use the Railway CLI to deploy the `backend/` folder.
2. Ensure `backend/Procfile` exists and points to `backend.app:app` with the chosen worker.
   - Current: `web: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 backend.app:app`
3. Environment variables (set in Railway project settings):
   - `DATABASE_URL` — Postgres connection (Railway plugin or external)
   - `SECRET_KEY` — Flask secret
   - `JWT_SECRET_KEY` — JWT signing secret
   - `FLASK_DEBUG=false`
   - MQTT credentials if required: `MQTT_HOST`, `MQTT_PORT`, `MQTT_USERNAME`, `MQTT_PASSWORD`
4. Push to Git (or trigger Railway deploy). Railway will install `backend/requirements.txt`.
5. After deploy, copy the Railway service URL (e.g. `https://my-backend.up.railway.app`).

Vercel (frontend) — deploy
Option A — Use Vercel rewrite (recommended):
1. Edit `frontend/vercel.json` and replace `<RAILWAY_BACKEND_URL>` with your Railway URL.
2. Create a new Vercel project and set the root to the `frontend/` folder (or use monorepo settings to deploy only that folder).
3. Deploy; Vercel will serve static files and rewrite `/api/*` to your Railway backend.

Option B — Runtime injection (alternative)
1. Edit `frontend/set_backend_url.js` and set `window.__BACKEND_URL = 'https://...';` to your backend URL.
2. Deploy `frontend/` to Vercel normally.

Verify after deploy
- Backend: curl the live endpoint:
```bash
curl https://<YOUR_RAILWAY_URL>/api/demo/devices
```
- Frontend: open deployed Vercel URL, confirm UI loads and real-time features connect (Socket.IO / WebSocket). Use browser console to inspect `window.__BACKEND_URL` and Socket.IO connection attempts.

Socket.IO notes
- If you changed worker (gevent vs eventlet), ensure `requirements.txt` and `Procfile` are consistent. Socket.IO server & client must both be able to use polling/websocket transport and CORS must allow the frontend origin.
- If Socket.IO fails, check server logs for handshake errors and CORS/transport fallbacks.

Rollback tips
- Revert `backend/Procfile` and `backend/requirements.txt` if worker incompatibility appears (switch back to `eventlet` by restoring those files).
- Use Railway's deployment history to rollback to a previous release.

Extras & security
- Keep secrets only in Railway/Vercel environment settings — never commit them.
- Consider enabling HTTPS-only and strict CORS origins.

If you want, I can:
- Create a small PR with these changes (commit + push).
- Replace `frontend/vercel.json` placeholder with the actual Railway URL you provide.
- Add a one-line health-check endpoint to `backend/app.py` (optional).
