# Deployment Notes: Vercel Frontend + Python Backend on Subdomains

## Recommended setup

- Frontend: Vercel
- Backend: Render or Railway
- DNS: Cloudflare or your registrar

## Example domains

- `app.empathylabai.org` -> frontend
- `api.empathylabai.org` -> backend

## Frontend on Vercel

- Framework preset: Next.js
- Root directory: `frontend`
- Environment variable:
  - `NEXT_PUBLIC_API_BASE_URL=https://api.empathylabai.org`

## Backend on Render or Railway

- Root directory: `backend`
- Start command:
  - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment variables:
  - `ENVIRONMENT=production`
  - `OPENAI_API_KEY=...`
  - `OPENAI_MODEL=gpt-4o-mini`
  - `ALLOWED_ORIGINS=https://app.empathylabai.org`
  - `SESSION_COOKIE_NAME=empathy_lab_client_id`
  - `MAX_HISTORY_MESSAGES=12`

## DNS

Point:

- `app` CNAME -> your Vercel deployment target
- `api` CNAME -> your backend deployment target

## Security note

This starter uses browser speech synthesis to keep costs low. It uses in-memory chat state for simplicity. Move to a real database once the core UX is locked.
