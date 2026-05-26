Deployment guide — Backend (Railway) + Frontend (Vercel)

Overview
- Backend: deploy the `backend/` folder to Railway (Python Flask + Socket.IO).
- Frontend: deploy the `frontend/` static site to Vercel; use rewrites to proxy `/api` to the Railway backend.

Backend (Railway)
1. Create a new Railway project and connect to GitHub (or deploy from local via Railway CLI).
2. Set the project root (Railway will detect the repo). Ensure `backend/Procfile` exists (we set `web: gunicorn -k eventlet -w 1 backend.app:app`).
3. Environment variables to add in Railway project settings:
   - `DATABASE_URL` = your Postgres connection (Railway provides this when you add a Postgres plugin)
   - `SECRET_KEY` = a random secret for Flask sessions
   - `JWT_SECRET_KEY` = your JWT secret
   - `FLASK_DEBUG` = `false` (recommended for production)
   - `RAILWAY_ENVIRONMENT` = `production` (optional flag used by the app)
   - Any MQTT credentials (if using external MQTT): `MQTT_HOST`, `MQTT_PORT`, `MQTT_USERNAME`, `MQTT_PASSWORD` etc. (app reads from environment or datasource table)
4. Railway build: it will install dependencies from `backend/requirements.txt`. Ensure `gunicorn`, `eventlet` (or chosen worker) are present.
5. Start command: Railway uses `Procfile` — no extra start command needed.
6. After deployment, note the Railway service URL (e.g. `https://my-backend.up.railway.app`).

Notes:
- Socket.IO compatibility: using `gunicorn -k eventlet` is the recommended approach for Flask-SocketIO in production. If you switch to `gevent`, update `Procfile` and `requirements.txt`.
- If you prefer threaded workers, change Procfile to use `gunicorn -k gthread -w 1 backend.app:app` and ensure `requirements.txt` reflects that.

Frontend (Vercel)
Option A — Simple: proxy `/api` to backend (recommended)
1. In `frontend/vercel.json` we include a rewrite that proxies `/api/*` to your Railway backend URL. Edit `frontend/vercel.json` and replace `<RAILWAY_BACKEND_URL>` with your Railway URL (without trailing `/`).
2. Deploy the `frontend/` folder to Vercel (create a new Vercel project pointing at the Git repo or import the `frontend` directory).
3. Vercel will serve static files; requests to `/api/...` will be forwarded to your Railway backend.

Option B — Client-side runtime URL (if not using rewrites)
1. The frontend reads `window.__BACKEND_URL` (see `frontend/static/script.js`). To inject it at runtime, add a small script file `frontend/set_backend_url.js` containing:
   window.__BACKEND_URL = "https://your-backend-url";
2. Include `<script src="/set_backend_url.js"></script>` in your HTML `head` before other scripts.
3. Add `set_backend_url.js` to your Vercel deployment.

Environment variables and secrets
- For server secrets, always set them in Railway environment settings, not in frontend code.
- For frontend API base URL, prefer using Vercel rewrites (Option A) so you don't need to expose variables client-side.

Testing locally before deploy
- Backend (dev):
```bash
python backend/app.py
```
- Frontend (static):
```bash
cd frontend
python -m http.server 8000
# open http://127.0.0.1:8000
```

Troubleshooting
- If Socket.IO connections fail, confirm the backend URL and CORS settings. Add the backend origin to allowed CORS in `app.py` if needed.
- If you see eventlet errors, ensure `eventlet` is in `requirements.txt` and `Procfile` uses the `eventlet` worker.

If you want, I can:
- Update `frontend/vercel.json` with your actual Railway URL.
- Create a small `set_backend_url.js` and modify the HTML to include it for Option B.
- Adjust `backend/requirements.txt` + `Procfile` to use `gevent` or threaded workers.

Tell me which follow-up to implement (replace rewrites, add runtime script, or change production worker).