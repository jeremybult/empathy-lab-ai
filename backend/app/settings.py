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

def _split_csv(raw: str) -> List[str]:
    return [item.strip() for item in raw.split(',') if item.strip()]

def _bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {'1', 'true', 'yes', 'on'}

def _is_production(environment: str) -> bool:
    return environment.strip().lower() in {'prod', 'production'}

def get_settings() -> Settings:
    environment = os.getenv('ENVIRONMENT', 'development').strip() or 'development'
    production_defaults = _is_production(environment)

    samesite = (os.getenv('SESSION_COOKIE_SAMESITE', 'lax').strip() or 'lax').lower()
    if samesite not in {'lax', 'strict', 'none'}:
        samesite = 'lax'

    return Settings(
        app_name=os.getenv('APP_NAME', 'Empathy Lab AI Backend').strip() or 'Empathy Lab AI Backend',
        environment=environment,
        openai_api_key=os.getenv('OPENAI_API_KEY', '').strip(),
        openai_model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini').strip() or 'gpt-4o-mini',
        allowed_origins=_split_csv(os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000')),
        session_cookie_name=os.getenv('SESSION_COOKIE_NAME', 'empathy_lab_client_id').strip() or 'empathy_lab_client_id',
        max_history_messages=max(4, int(os.getenv('MAX_HISTORY_MESSAGES', '12'))),
        session_cookie_secure=_bool_env('SESSION_COOKIE_SECURE', production_defaults),
        session_cookie_httponly=_bool_env('SESSION_COOKIE_HTTPONLY', True),
        session_cookie_samesite=samesite,
    )
