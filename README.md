# Empathy Lab AI: Free Full-Stack Starter

This monorepo is built for a free-tool deployment pattern:

- `frontend/`: Next.js app for the public site and live chatbot UI
- `backend/`: FastAPI API for personas, chat, health checks, and reset
- browser speech recognition + browser speech synthesis to avoid per-reply cloud TTS costs
- ready for a hosted chatbot on a subdomain such as `app.yourdomain.com`

## What changed in this backend revision

- Added deployment-shaped FastAPI structure
- Added environment-driven settings
- Added `/`, `/health`, `/api/config`, `/api/personas`, `/api/chat`, `/api/reset`
- Added server-side client ID fallback with cookie support
- Added safer request and response models
- Added deployment files for Render and generic Procfile platforms
- Kept demo fallback mode when `OPENAI_API_KEY` is missing

## Recommended platform pattern

Because free hosting plans change often and I cannot verify live plan limits in this environment, treat these as strong architecture picks rather than guaranteed current free tiers:

- Frontend: Vercel or Netlify
- Backend: Render or Railway
- DNS: Cloudflare or your domain registrar
- Code hosting: GitHub
- Optional database later: Supabase or Neon

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

## Environment variables

### Backend `.env`

```env
APP_NAME=Empathy Lab AI Backend
ENVIRONMENT=development
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
ALLOWED_ORIGINS=http://localhost:3000
SESSION_COOKIE_NAME=empathy_lab_client_id
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=lax
MAX_HISTORY_MESSAGES=12
```

### Frontend `.env.local`

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Empathy Lab AI
```

## Subdomain deployment pattern

Suggested setup:

- `https://app.yourdomain.com` -> Next.js frontend
- `https://api.yourdomain.com` -> FastAPI backend

Then set:

- frontend `NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com`
- backend `ALLOWED_ORIGINS=https://app.yourdomain.com`

## Suggested build order

1. Put the project on GitHub
2. Deploy the frontend to Vercel
3. Deploy the backend to Render or Railway
4. Connect custom subdomains
5. Add `OPENAI_API_KEY`
6. Test the live chat flow
7. Add persistence later only after the UI is stable

## Voice strategy

This starter avoids per-reply cloud TTS billing by using built-in browser speech synthesis.

That means:

- no ElevenLabs call per message by default
- no premium cloned voice out of the box
- much lower cost during development and demos

If you later want premium voice, add it as an optional mode, not the default runtime path.

## UX behavior note

When users switch personas in the frontend chat widget, the visible transcript is reset and a new context banner is shown. This prevents accidental context mixing across personas.

## CI deployment verification

GitHub Actions CI now validates deployment readiness with two jobs:

- Frontend: install dependencies and run `npm run build` in `frontend/`
- Backend: install dependencies and run `python scripts/smoke_test.py` in `backend/`

Workflow file: `.github/workflows/ci.yml`.
