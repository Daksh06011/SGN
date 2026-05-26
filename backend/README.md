Backend (Railway) deployment

- Deploy the contents of this `backend/` directory to Railway.
- Ensure environment variables are set on Railway: `DATABASE_URL` (Postgres) or set `USE_SQLITE=true` for SQLite, `SECRET_KEY`, and any MQTT credentials.
- Railway will use the `Procfile` to start the app with Gunicorn + Eventlet.

Quick local run:
```
python -m venv .venv
source .venv/Scripts/activate (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python app.py
```

Notes:
- This folder contains an API-only wrapper of the original project. The frontend is a separate static site suitable for Vercel.
- If you need the full `app.py` logic copied from the project root, copy `app.py` from project root into this folder (it is large). The wrapper currently blocks non-API routes to avoid template serving on Railway.
