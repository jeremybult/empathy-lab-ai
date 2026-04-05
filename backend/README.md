# Backend: FastAPI API

This backend powers the persona chatbot, health checks, reset flow, and deployment-ready CORS configuration.

## Endpoints

- `GET /` basic service metadata
- `GET /health` health and mode check
- `GET /api/config` frontend-safe config
- `GET /api/personas` list personas
- `POST /api/chat` send a message
- `POST /api/reset` reset one persona conversation
- `GET /docs` Swagger docs

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Example request

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "local-demo-user",
    "persona_id": "andrea_miller",
    "message": "What is OCD actually like day to day?"
  }'
```

## Production notes

- Add your deployed frontend URL to `ALLOWED_ORIGINS`
- Set `OPENAI_API_KEY`
- Keep browser speech synthesis as the default voice path to avoid per-reply TTS costs
- In-memory storage is fine for demos. Add a real database later for persistent conversations.

## Smoke verification

A lightweight smoke script is included and used in CI:

```bash
python scripts/smoke_test.py
```

It verifies core endpoint behavior (`/`, `/health`, `/api/personas`, `/api/chat`, `/api/reset`) without introducing a full test suite.
