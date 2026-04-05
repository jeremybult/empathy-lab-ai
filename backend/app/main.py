import logging
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from .models import ChatRequest, ChatResponse, ResetRequest, ResetResponse
from .services import ChatService, ProviderAPIError
from .settings import get_settings
from .storage import MemoryConversationStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()
store = MemoryConversationStore(max_messages=settings.max_history_messages)
service = ChatService(settings=settings, store=store)

app = FastAPI(
    title=settings.app_name,
    version='0.2.1',
    docs_url='/docs',
    redoc_url='/redoc',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)



def resolve_client_id(request: Request, incoming_client_id: str | None) -> str:
    if incoming_client_id:
        return incoming_client_id
    cookie_value = request.cookies.get(settings.session_cookie_name)
    if cookie_value:
        return cookie_value
    return str(uuid4())



def set_session_cookie(response: Response, client_id: str) -> None:
    response.set_cookie(
        key=settings.session_cookie_name,
        value=client_id,
        httponly=settings.session_cookie_httponly,
        secure=settings.session_cookie_secure,
        samesite=settings.session_cookie_samesite,
        max_age=60 * 60 * 24 * 30,
    )


@app.get('/')
def root() -> dict:
    return {
        'name': settings.app_name,
        'status': 'ok',
        'docs': '/docs',
        'mode': 'live' if settings.openai_api_key else 'demo',
    }


@app.get('/health')
def health() -> dict:
    return {
        'status': 'ok',
        'environment': settings.environment,
        'mode': 'live' if settings.openai_api_key else 'demo',
        'allowed_origins': settings.allowed_origins,
    }


@app.get('/api/personas')
def personas() -> dict:
    return {'personas': service.get_personas()}


@app.get('/api/config')
def config() -> dict:
    return {
        'app_name': settings.app_name,
        'mode': 'live' if settings.openai_api_key else 'demo',
        'session_cookie_name': settings.session_cookie_name,
        'session_cookie_secure': settings.session_cookie_secure,
        'session_cookie_httponly': settings.session_cookie_httponly,
        'session_cookie_samesite': settings.session_cookie_samesite,
    }


@app.post('/api/chat', response_model=ChatResponse)
def chat(request: Request, payload: ChatRequest, response: Response) -> ChatResponse:
    client_id = resolve_client_id(request, payload.client_id)
    normalized_message = payload.message.strip()
    if not normalized_message:
        raise HTTPException(
            status_code=400,
            detail={
                'code': 'invalid_message',
                'message': 'Message must contain non-whitespace characters.',
            },
        )

    try:
        result = service.chat(
            client_id=client_id,
            persona_id=payload.persona_id,
            message=normalized_message,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail={'code': 'invalid_request', 'message': str(exc)}) from exc
    except ProviderAPIError:
        raise HTTPException(
            status_code=502,
            detail={
                'code': 'upstream_error',
                'message': 'The AI provider is temporarily unavailable. Please try again shortly.',
            },
        )
    except Exception:
        logger.exception('Unhandled server error while processing /api/chat')
        raise HTTPException(
            status_code=500,
            detail={
                'code': 'internal_error',
                'message': 'An unexpected server error occurred. Please try again.',
            },
        )

    set_session_cookie(response, client_id)
    return ChatResponse(**result)


@app.post('/api/reset', response_model=ResetResponse)
def reset(request: Request, payload: ResetRequest, response: Response) -> ResetResponse:
    client_id = resolve_client_id(request, payload.client_id)
    service.reset(client_id=client_id, persona_id=payload.persona_id)
    set_session_cookie(response, client_id)
    return ResetResponse(status='reset', client_id=client_id, persona_id=payload.persona_id)
