import aiohttp
from typing import AsyncIterator

from app.tts.base import BaseTTS
from app.utils.constants import DEEPGRAM_AURA_SUPPORTED_LANGUAGES
from app.utils.logger import log


DEEPGRAM_TTS_URL = "https://api.deepgram.com/v1/speak"


class DeepgramTTS(BaseTTS):
    def __init__(self, api_key: str, model: str = "aura-asteria-en"):
        self._api_key = api_key
        self._model = model
        self._sample_rate = 24000

    async def synthesize(self, text: str, language: str) -> bytes:
        chunks = []
        async for chunk in self.synthesize_stream(text, language):
            chunks.append(chunk)
        return b"".join(chunks)

    async def synthesize_stream(self, text: str, language: str) -> AsyncIterator[bytes]:
        headers = {
            "Authorization": f"Token {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {"text": text}
        params = {
            "model": self._model,
            "encoding": "linear16",
            "sample_rate": str(self._sample_rate),
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    DEEPGRAM_TTS_URL, headers=headers, json=payload, params=params
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        log.error(f"Deepgram TTS error {response.status}: {error_text}")
                        return

                    async for chunk in response.content.iter_chunked(4096):
                        yield chunk
        except Exception as e:
            log.error(f"Deepgram TTS stream error: {e}")

    def supports_language(self, language: str) -> bool:
        return language.upper() in DEEPGRAM_AURA_SUPPORTED_LANGUAGES

    def get_sample_rate(self) -> int:
        return self._sample_rate
