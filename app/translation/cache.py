from collections import OrderedDict
from typing import Optional


class TranslationCache:
    def __init__(self, max_size: int = 1000):
        self._max_size = max_size
        self._cache: OrderedDict[str, str] = OrderedDict()

    def _make_key(self, text: str, source_lang: str, target_lang: str) -> str:
        return f"{source_lang}:{target_lang}:{text.strip().lower()}"

    def get(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        key = self._make_key(text, source_lang, target_lang)
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def put(self, text: str, source_lang: str, target_lang: str, translation: str):
        key = self._make_key(text, source_lang, target_lang)
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = translation
        while len(self._cache) > self._max_size:
            self._cache.popitem(last=False)

    def clear(self):
        self._cache.clear()

    @property
    def size(self) -> int:
        return len(self._cache)
