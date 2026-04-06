# empathy-lab-ai (Canonical Full-Stack Repository)

This is the canonical production repository for Empathy Lab AI.

## Architecture

- `frontend/` — Next.js web app (UI, chat shell, browser voice UX)
- `backend/` — FastAPI API (personas, chat, session, config, voice provider metadata)

The current production architecture remains **Next.js + FastAPI**.

## Legacy preservation (EmpathyLab2024)

This repo now preserves legacy EmpathyLab2024 content as part of the same codebase:

- legacy prompts migrated into backend persona registry
- legacy prototype/docs/scripts archived under `legacy/empathylab2024/`
- optional legacy-compatible provider metadata for:
  - Azure Speech-to-Text (STT)
  - ElevenLabs Text-to-Speech (TTS)

### Archived legacy tree

- `legacy/empathylab2024/prompts/`
- `legacy/empathylab2024/prototype/`
- `legacy/empathylab2024/docs/`
- `legacy/empathylab2024/voice/`

## Voice strategy

Default path (recommended for cost control):

- Browser-native SpeechRecognition + speechSynthesis

Optional legacy-compatible integrations:

- Azure STT (metadata/config exposure)
- ElevenLabs TTS (metadata/config exposure)

Browser-native voice remains the default behavior.

## Personas

All personas (modern + legacy) are available through the same endpoint:

- `GET /api/personas`

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

Expected local URLs:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

## Backend environment variables

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
AZURE_SPEECH_KEY=
AZURE_SPEECH_REGION=
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_NAME=Brit
ENABLE_LEGACY_VOICE_PROVIDERS=true
```

## API routes

- `GET /`
- `GET /health`
- `GET /api/config`
- `GET /api/personas`
- `GET /api/voice/providers`
- `POST /api/chat`
- `POST /api/reset`
- `GET /docs`

## Deployment model (Phase 1)

- Vercel for `frontend/`
- Render for `backend/`
- Suggested domains:
  - `app.yourdomain.com` -> frontend
  - `api.yourdomain.com` -> backend

See `vercel_subdomain_notes.md` for quick deploy settings.

## Migration completeness

This repository is now intended to be a **superset** of EmpathyLab2024:

- modernized production stack retained
- legacy prompts preserved and active in persona registry
- legacy prototype/docs archived in-repo
- optional legacy-compatible voice provider metadata exposed

See `docs/legacy_migration.md` for the explicit old->new mapping.
