from abc import ABC, abstractmethod


class BaseTranslator(ABC):
    @property
    def lang_key(self) -> str:
        return "deepl"

    @abstractmethod
    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        pass

    @abstractmethod
    def supports_pair(self, source_lang: str, target_lang: str) -> bool:
        pass
