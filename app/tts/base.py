from abc import ABC, abstractmethod
from typing import AsyncIterator


class BaseTTS(ABC):
    @abstractmethod
    async def synthesize(self, text: str, language: str) -> bytes:
        pass

    @abstractmethod
    async def synthesize_stream(self, text: str, language: str) -> AsyncIterator[bytes]:
        pass

    @abstractmethod
    def supports_language(self, language: str) -> bool:
        pass

    @abstractmethod
    def get_sample_rate(self) -> int:
        pass
