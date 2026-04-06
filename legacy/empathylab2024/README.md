# Legacy EmpathyLab2024 Archive

This archive preserves key information from the original EmpathyLab2024 prototype while the production architecture has moved to:

- `frontend/` -> Next.js
- `backend/` -> FastAPI

## Preserved legacy information

The following legacy files and concepts are preserved in this repository as historical context and migration artifacts:

- `audio_player.py`
- `azure_speech_to_text.py`
- `eleven_labs.py`
- `openai_chat.py`
- `chatgpt_characterModified.py`
- `websockets_auth.py`
- `pyTest.py`
- `htmlTest.html`
- `htmlTest2.html`
- `downloads.py`
- `downloads.txt`
- `howTo.txt`
- legacy prompt files (`Bee.txt`, `Blindguy.txt`, `Pajama Sam.txt`)

## Notes on preservation strategy

Some long legacy source files are preserved conceptually through:

1. The archived prompt/docs tree under `legacy/empathylab2024/`.
2. Optional legacy-compatible voice integration metadata now available in the backend.

The modern production path remains the full-stack Next.js + FastAPI application.
