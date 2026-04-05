import logging
from typing import List

import requests

from .personas import PERSONAS
from .settings import Settings
from .storage import MemoryConversationStore

logger = logging.getLogger(__name__)

class ProviderAPIError(RuntimeError):
    pass

class ChatService:
    def __init__(self, settings: Settings, store: MemoryConversationStore) -> None:
        self.settings = settings
        self.store = store

    def _conversation_key(self, client_id: str, persona_id: str) -> str:
        return f'{client_id}:{persona_id}'

    def reset(self, client_id: str, persona_id: str) -> None:
        self.store.reset(self._conversation_key(client_id, persona_id))

    def get_personas(self) -> List[dict]:
        return [
            {key: value for key, value in persona.items() if key != 'system_prompt'}
            for persona in PERSONAS.values()
        ]

    def chat(self, client_id: str, persona_id: str, message: str) -> dict:
        persona = PERSONAS.get(persona_id)
        if not persona:
            raise ValueError('Unknown persona_id')

        key = self._conversation_key(client_id, persona_id)
        history = self.store.get_history(key)
        history.append({'role': 'user', 'content': message})

        if not self.settings.openai_api_key:
            reply = self._demo_reply(persona=persona, user_message=message)
            history.append({'role': 'assistant', 'content': reply})
            self.store.replace(key, history)
            return {
                'reply': reply,
                'mode': 'demo',
                'client_id': client_id,
                'persona_id': persona_id,
            }

        system_message = {
            'role': 'system',
            'content': (
                persona['system_prompt']
                + ' You are part of an educational empathy platform. Keep answers concise but helpful.'
                + ' Do not provide medical diagnosis, emergency advice, or crisis instructions.'
                + ' If a user may be in danger, urge them to contact a licensed professional or emergency services.'
            ),
        }
        messages = [system_message] + history[-10:]
        payload = {'model': self.settings.openai_model, 'messages': messages, 'temperature': 0.7}
        headers = {
            'Authorization': f'Bearer {self.settings.openai_api_key}',
            'Content-Type': 'application/json',
        }
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                json=payload,
                headers=headers,
                timeout=60,
            )
        except requests.RequestException:
            logger.exception('Provider request failed before response')
            raise ProviderAPIError('Upstream AI provider request failed')
        if response.status_code >= 400:
            logger.error(
                'Provider request failed status=%s body=%s',
                response.status_code,
                response.text[:1000],
            )
            raise ProviderAPIError('Upstream AI provider error')

        data = response.json()
        reply = data['choices'][0]['message']['content'].strip()
        history.append({'role': 'assistant', 'content': reply})
        self.store.replace(key, history)
        return {
            'reply': reply,
            'mode': 'live',
            'client_id': client_id,
            'persona_id': persona_id,
        }

    def _demo_reply(self, persona: dict, user_message: str) -> str:
        name = persona['name']
        lower = user_message.lower()

        if 'hello' in lower or 'hi' in lower:
            return (
                f'Hi, I am {name}. This is demo mode, but the backend flow is working. '
                'Ask me about symptoms, lived experience, study habits, or how this project supports empathy development.'
            )
        if 'adhd' in lower:
            return (
                f'{name} here. In demo mode, I can still reflect the structure of the real experience. '
                'ADHD often affects attention regulation, task initiation, working memory, organization, and follow-through, '
                'but it shows up differently from person to person.'
            )
        if 'ocd' in lower:
            return (
                f'{name} here. OCD is not just about liking order. It involves intrusive thoughts, anxiety, '
                'and repetitive behaviors or mental rituals that people may feel driven to perform.'
            )
        if 'empathy' in lower:
            return (
                f'{name} here. One goal of this project is to make psychology learning more human and memorable. '
                'Interactive dialogue can help users connect symptoms and concepts to lived experience instead of treating them like abstract definitions.'
            )
        return (
            f'{name} received your question: {user_message!r}. The backend is running in demo mode because no OPENAI_API_KEY is configured yet. '
            'Once you add a key, this same interface will return live model responses while keeping the free browser-based voice path.'
        )
