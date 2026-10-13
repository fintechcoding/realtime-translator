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

        # No provider can actually speak this language. Returning a provider that
        # can't (e.g. an English voice for Russian) would produce garbled audio,
        # so return None and let the caller surface a clear warning.
        log.warning(f"No TTS provider supports '{language}' - skipping speech output")
        return None
