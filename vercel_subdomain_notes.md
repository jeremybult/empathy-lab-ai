# Phase 1 Deployment Notes (Vercel + Render)

This repo is intended to deploy with:

- Frontend (`frontend/`) on **Vercel**
- Backend (`backend/`) on **Render**
- `app.yourdomain.com` -> frontend
- `api.yourdomain.com` -> backend

## Vercel (frontend)

- Framework Preset: `Next.js`
- Root Directory: `frontend`
- Env vars:
  - `NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com`
  - `NEXT_PUBLIC_APP_NAME=Empathy Lab AI`

## Render (backend)

- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Env vars:
  - `ENVIRONMENT=production`
  - `OPENAI_API_KEY=...`
  - `OPENAI_MODEL=gpt-4o-mini`
  - `ALLOWED_ORIGINS=https://app.yourdomain.com`
  - `SESSION_COOKIE_NAME=empathy_lab_client_id`
  - `MAX_HISTORY_MESSAGES=12`

## DNS mapping

- `app` CNAME -> Vercel deployment target
- `api` CNAME -> Render backend target

## Validation URLs

Backend:

- `https://api.yourdomain.com/`
- `https://api.yourdomain.com/health`
- `https://api.yourdomain.com/docs`

Frontend:

- `https://app.yourdomain.com`
