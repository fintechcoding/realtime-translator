import asyncio
from typing import Optional

import deepl

from app.translation.base import BaseTranslator
from app.translation.cache import TranslationCache
from app.utils.logger import log


class DeepLTranslator(BaseTranslator):
    @property
    def lang_key(self) -> str:
        return "deepl"

    def __init__(self, api_key: str, formality: str = "default", cache_size: int = 1000):
        self._translator = deepl.Translator(api_key)
        self._formality = formality
        self._cache = TranslationCache(max_size=cache_size)
        self._loop = None

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
        except deepl.DeepLException as e:
            log.error(f"DeepL translation error: {e}")
            return text

    def _translate_sync(self, text: str, source_lang: str, target_lang: str) -> str:
        result = self._translator.translate_text(
            text,
            source_lang=source_lang,
            target_lang=target_lang,
            formality=self._formality if self._formality != "default" else None,
        )
        return result.text

    def supports_pair(self, source_lang: str, target_lang: str) -> bool:
        return True
