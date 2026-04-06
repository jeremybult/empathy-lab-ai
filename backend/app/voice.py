from .settings import Settings


class VoiceProviderService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_provider_status(self) -> dict:
        browser = {
            'id': 'browser_native',
            'name': 'Browser Native Voice',
            'type': 'default',
            'supports_stt': True,
            'supports_tts': True,
            'available': True,
            'configured': True,
            'notes': 'Uses browser SpeechRecognition and speechSynthesis on the client side.',
        }

        azure = {
            'id': 'azure_speech',
            'name': 'Azure Speech',
            'type': 'optional_legacy',
            'supports_stt': True,
            'supports_tts': False,
            'available': self.settings.enable_legacy_voice_providers,
            'configured': bool(self.settings.azure_speech_key and self.settings.azure_speech_region),
            'notes': 'Legacy-compatible Azure Speech-to-Text path preserved from EmpathyLab2024.',
        }

        elevenlabs = {
            'id': 'elevenlabs',
            'name': 'ElevenLabs',
            'type': 'optional_legacy',
            'supports_stt': False,
            'supports_tts': True,
            'available': self.settings.enable_legacy_voice_providers,
            'configured': bool(self.settings.elevenlabs_api_key),
            'default_voice': self.settings.elevenlabs_voice_name,
            'notes': 'Legacy-compatible ElevenLabs Text-to-Speech path preserved from EmpathyLab2024.',
        }

        return {
            'default_provider': 'browser_native',
            'providers': [browser, azure, elevenlabs],
        }
