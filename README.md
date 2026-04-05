# Empathy Lab AI: Canonical Full-Stack Starter

This repository is the canonical extracted source tree for the Empathy Lab AI MVP.

## Structure

- `frontend/` – Next.js app (liquid-glass landing page + integrated chatbot UI)
- `backend/` – FastAPI service (personas, chat, reset, health/config, session cookies)
- `vercel_subdomain_notes.md` – subdomain deployment notes for `app.` and `api.`

## Current behavior highlights

- Persona-aware chatbot flow with demo fallback when `OPENAI_API_KEY` is missing.
- Browser speech recognition and browser speech synthesis (no per-reply cloud TTS required by default).
- Session cookie behavior is environment-aware:
  - production defaults to `Secure` + `HttpOnly`
  - local development stays workable without HTTPS
- Persona switching in the UI clears/resets the visible transcript to avoid mixed-context confusion.

## Local development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Frontend: `http://localhost:3000`  
Backend: `http://localhost:8000`

## Backend environment variables

See `backend/.env.example` for the full list. Key values:

- `ENVIRONMENT` (`development` or `production`)
- `OPENAI_API_KEY`
- `ALLOWED_ORIGINS`
- `SESSION_COOKIE_SECURE`
- `SESSION_COOKIE_HTTPONLY`
- `SESSION_COOKIE_SAMESITE`

## Deployment pattern

Recommended:

- `https://app.yourdomain.com` -> frontend
- `https://api.yourdomain.com` -> backend

Then set:

- frontend `NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com`
- backend `ALLOWED_ORIGINS=https://app.yourdomain.com`

## Voice strategy

Default runtime avoids per-output cloud voice billing by using browser-native speech synthesis.
Premium voice providers can be added later as an optional mode.
