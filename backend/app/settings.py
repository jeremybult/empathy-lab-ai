import os
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Settings:
    app_name: str
    environment: str
    openai_api_key: str
    openai_model: str
    allowed_origins: List[str]
    session_cookie_name: str
    max_history_messages: int
    session_cookie_secure: bool
    session_cookie_httponly: bool
    session_cookie_samesite: str
    azure_speech_key: str
    azure_speech_region: str
    elevenlabs_api_key: str
    elevenlabs_voice_name: str
    enable_legacy_voice_providers: bool



def _split_csv(raw: str) -> List[str]:
    return [item.strip() for item in raw.split(',') if item.strip()]



def _is_production(environment: str) -> bool:
    return environment.strip().lower() in {'production', 'prod'}



def _parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {'1', 'true', 'yes', 'on'}:
        return True
    if normalized in {'0', 'false', 'no', 'off'}:
        return False
    return default



def get_settings() -> Settings:
    environment = os.getenv('ENVIRONMENT', 'development').strip() or 'development'
    production = _is_production(environment)

    session_cookie_secure = _parse_bool(os.getenv('SESSION_COOKIE_SECURE'), default=production)
    session_cookie_httponly = _parse_bool(os.getenv('SESSION_COOKIE_HTTPONLY'), default=True)
    session_cookie_samesite = os.getenv('SESSION_COOKIE_SAMESITE', 'lax').strip().lower() or 'lax'

    return Settings(
        app_name=os.getenv('APP_NAME', 'Empathy Lab AI Backend').strip() or 'Empathy Lab AI Backend',
        environment=environment,
        openai_api_key=os.getenv('OPENAI_API_KEY', '').strip(),
        openai_model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini').strip() or 'gpt-4o-mini',
        allowed_origins=_split_csv(os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000')),
        session_cookie_name=os.getenv('SESSION_COOKIE_NAME', 'empathy_lab_client_id').strip() or 'empathy_lab_client_id',
        max_history_messages=max(4, int(os.getenv('MAX_HISTORY_MESSAGES', '12'))),
        session_cookie_secure=session_cookie_secure,
        session_cookie_httponly=session_cookie_httponly,
        session_cookie_samesite=session_cookie_samesite,
        azure_speech_key=os.getenv('AZURE_SPEECH_KEY', '').strip(),
        azure_speech_region=os.getenv('AZURE_SPEECH_REGION', '').strip(),
        elevenlabs_api_key=os.getenv('ELEVENLABS_API_KEY', '').strip(),
        elevenlabs_voice_name=os.getenv('ELEVENLABS_VOICE_NAME', 'Brit').strip() or 'Brit',
        enable_legacy_voice_providers=_parse_bool(os.getenv('ENABLE_LEGACY_VOICE_PROVIDERS'), default=True),
    )
