from abc import ABC, abstractmethod
from typing import Callable, Optional


class BaseSTT(ABC):
    def __init__(self):
        self.on_transcript: Optional[Callable[[str, bool], None]] = None

    @abstractmethod
    async def start_stream(self, language: str) -> None:
        pass

    @abstractmethod
    async def send_audio(self, audio_chunk: bytes) -> None:
        pass

    @abstractmethod
    async def stop_stream(self) -> None:
        pass

    @abstractmethod
    def is_streaming(self) -> bool:
        pass
