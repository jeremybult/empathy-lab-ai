# Legacy Migration: EmpathyLab2024 -> empathy-lab-ai

## Overview

This document explains how EmpathyLab2024 content was preserved while moving to the modern full-stack architecture in `empathy-lab-ai`.

## What existed in EmpathyLab2024

- Flask-driven prototype pages and route loop
- prompt files for Bee / Blindguy / Pajama Sam
- local voice tooling and helper scripts
- setup/docs notes and small utility scripts

## What replaced it in empathy-lab-ai

- Old Flask prototype -> **Next.js frontend + FastAPI backend**
- monorepo structure with deploy-ready frontend/backend separation
- API-first persona registry and chat pipeline

## What was preserved exactly

Archived under `legacy/empathylab2024/`:

- prompts (`Bee.txt`, `Blindguy.txt`, `Pajama Sam.txt`)
- prototype files (`pyTest.py`, `htmlTest.html`, `htmlTest2.html`)
- docs/utils (`howTo.txt`, `downloads.txt`, `downloads.py`)
- voice legacy metadata files (`requirements.txt`, `websockets_auth.py`)

## What was preserved as an optional modern integration

- Old Azure Speech-to-Text -> preserved as optional legacy provider metadata in backend config and exposed via `/api/voice/providers`
- Old ElevenLabs TTS -> preserved as optional legacy provider metadata in backend config and exposed via `/api/voice/providers`

## What remains intentionally modernized

- Production runtime remains `frontend/` Next.js + `backend/` FastAPI
- Browser-native voice remains the default free path
- Persona retrieval and routing are consolidated through backend endpoints
- Legacy personas are integrated into current backend persona registry and served from `/api/personas`
