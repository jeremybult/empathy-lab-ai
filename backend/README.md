# Backend: FastAPI API

This backend is Phase 1-ready for Render deployment and provides:

- `GET /`
- `GET /health`
- `GET /api/config`
- `GET /api/personas`
- `POST /api/chat`
- `POST /api/reset`
- `GET /docs`

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Render Phase 1 settings

- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Recommended env vars:

```env
ENVIRONMENT=production
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4o-mini
ALLOWED_ORIGINS=https://app.yourdomain.com
SESSION_COOKIE_NAME=empathy_lab_client_id
MAX_HISTORY_MESSAGES=12
```

## Smoke verification

A lightweight smoke script is included and used in CI:

```bash
python scripts/smoke_test.py
```

It verifies `/`, `/health`, `/api/personas`, `/api/chat`, and `/api/reset`.
