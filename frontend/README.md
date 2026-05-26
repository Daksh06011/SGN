Frontend (Vercel) deployment

- The `frontend/` folder contains the static site assets (HTML/CSS/JS). Deploy this folder to Vercel as a static site.
- Configure an environment variable in Vercel for the backend base URL, e.g. `BACKEND_URL=https://your-railway-backend.up.railway.app`.
- Update your frontend JS to call the API via the full URL (use `BACKEND_URL` at build time), or use a rewrite rule in `vercel.json` to proxy `/api/*` to the Railway backend.

Example Vercel `vercel.json` rewrite (optional):
```
{
  "rewrites": [
    { "source": "/api/:match*", "destination": "https://YOUR_BACKEND_URL/api/:match*" }
  ]
}
```

Local preview:
Open `frontend/index.html` in a browser, or run a simple static server:
```
python -m http.server 5000 --directory frontend
```
