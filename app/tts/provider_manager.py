from typing import Optional

from app.tts.base import BaseTTS
from app.utils.logger import log


class TTSProviderManager:
    def __init__(self):
        self._providers: list[BaseTTS] = []

    def add_provider(self, provider: BaseTTS):
        self._providers.append(provider)

    def get_provider(self, language: str) -> Optional[BaseTTS]:
        for provider in self._providers:
            if provider.supports_language(language):
                return provider

        if self._providers:
            log.warning(
                f"No TTS provider supports '{language}', using last fallback"
            )
            return self._providers[-1]

        log.error("No TTS providers configured")
        return None
