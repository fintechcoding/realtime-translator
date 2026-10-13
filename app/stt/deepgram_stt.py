import asyncio
import threading
from typing import Callable, Optional

from deepgram import DeepgramClient
from deepgram.core.events import EventType

from app.stt.base import BaseSTT
from app.utils.logger import log


class DeepgramSTT(BaseSTT):
    def __init__(self, api_key: str, model: str = "nova-2"):
        super().__init__()
        self._api_key = api_key
        self._model = model
        self._client: Optional[DeepgramClient] = None
        self._connection = None
        self._ctx_manager = None
        self._streaming = False
        self._listen_thread: Optional[threading.Thread] = None
        self._language: str = ""
        self._reconnect_attempts = 0
        self._max_reconnect = 5

    async def start_stream(self, language: str) -> None:
        if self._streaming:
            await self.stop_stream()

        self._language = language
        loop = asyncio.get_running_loop()

        try:
            await loop.run_in_executor(None, self._connect_sync, language)
            self._streaming = True
            self._reconnect_attempts = 0
            log.info(f"Deepgram STT stream started (lang={language}, model={self._model})")
        except Exception as e:
            log.error(f"Failed to start Deepgram STT stream: {e}")
            raise

    def _connect_sync(self, language: str):
        self._client = DeepgramClient(api_key=self._api_key)

        self._ctx_manager = self._client.listen.v1.connect(
            model=self._model,
            language=language,
            encoding="linear16",
            sample_rate="16000",
            channels="1",
            interim_results="true",
            utterance_end_ms="1000",
            punctuate="true",
            endpointing="300",
        )
        self._connection = self._ctx_manager.__enter__()

        self._connection.on(EventType.MESSAGE, self._on_message)
        self._connection.on(EventType.ERROR, self._on_error)
        self._connection.on(EventType.CLOSE, self._on_close)

        self._listen_thread = threading.Thread(
            target=self._listen_loop, daemon=True
        )
        self._listen_thread.start()

    def _listen_loop(self):
        try:
            self._connection.start_listening()
        except Exception as e:
            if self._streaming:
                log.error(f"Deepgram listen loop error: {e}")

    def _on_message(self, message):
        try:
            if not hasattr(message, "channel"):
                return
            alternatives = message.channel.alternatives
            if not alternatives:
                return
            transcript = alternatives[0].transcript
            if transcript and transcript.strip():
                is_final = getattr(message, "is_final", False)
                if self.on_transcript:
                    self.on_transcript(transcript, is_final)
        except (IndexError, AttributeError) as e:
            log.warning(f"Error parsing transcript: {e}")

    def _on_error(self, error):
        log.error(f"Deepgram STT error: {error}")

    def _on_close(self, close_event):
        log.info("Deepgram STT connection closed")

    async def send_audio(self, audio_chunk: bytes) -> None:
        if self._connection and self._streaming:
            loop = asyncio.get_running_loop()
            try:
                await loop.run_in_executor(None, self._connection.send_media, audio_chunk)
            except Exception as e:
                log.error(f"Error sending audio to Deepgram: {e}")

    async def stop_stream(self) -> None:
        self._streaming = False
        if self._ctx_manager:
            try:
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(None, self._ctx_manager.__exit__, None, None, None)
            except Exception:
                pass
            self._ctx_manager = None
            self._connection = None

        if self._listen_thread and self._listen_thread.is_alive():
            self._listen_thread.join(timeout=3)
            self._listen_thread = None

        log.info("Deepgram STT stream stopped")

    def is_streaming(self) -> bool:
        return self._streaming
