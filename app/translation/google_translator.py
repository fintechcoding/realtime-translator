import asyncio
import json
import urllib.request
import urllib.error
import urllib.parse

from app.translation.base import BaseTranslator
from app.translation.cache import TranslationCache
from app.utils.logger import log


class GoogleTranslator(BaseTranslator):
    API_URL = "https://translation.googleapis.com/language/translate/v2"

    @property
    def lang_key(self) -> str:
        return "google"

    def __init__(self, api_key: str, cache_size: int = 1000):
        self._api_key = api_key
        self._cache = TranslationCache(max_size=cache_size)

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not text.strip():
            return ""

        cached = self._cache.get(text, source_lang, target_lang)
        if cached is not None:
            return cached

        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None,
                self._translate_sync,
                text,
                source_lang,
                target_lang,
            )
            self._cache.put(text, source_lang, target_lang, result)
            return result
        except Exception as e:
            log.error(f"Google Translation error: {e}")
            return text

    def _translate_sync(self, text: str, source_lang: str, target_lang: str) -> str:
        payload = json.dumps({
            "q": text,
            "source": source_lang,
            "target": target_lang,
            "format": "text",
        }).encode("utf-8")

        url = f"{self.API_URL}?key={urllib.parse.quote(self._api_key)}"
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))

        translations = body.get("data", {}).get("translations", [])
        if translations:
            return translations[0].get("translatedText", text)
        return text

    def supports_pair(self, source_lang: str, target_lang: str) -> bool:
        return True
