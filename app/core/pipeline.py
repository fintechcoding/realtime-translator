import asyncio
import time
from typing import Optional

from app.core.audio_engine import AudioEngine
from app.core.event_bus import EventBus
from app.stt.base import BaseSTT
from app.translation.base import BaseTranslator
from app.tts.base import BaseTTS
from app.tts.provider_manager import TTSProviderManager
from app.utils.logger import log


class TranslationPipeline:
    def __init__(
        self,
        audio_engine: AudioEngine,
        stt: BaseSTT,
        translator: BaseTranslator,
        tts_manager: TTSProviderManager,
        event_bus: EventBus,
    ):
        self._audio = audio_engine
        self._stt = stt
        self._translator = translator
        self._tts_manager = tts_manager
        self._bus = event_bus

        self._source_lang: str = "TR"
        self._target_lang: str = "RU"
        self._running = False
        self._audio_queue: asyncio.Queue[bytes] = asyncio.Queue(maxsize=200)
        self._send_task: Optional[asyncio.Task] = None
        self._output_device_id: Optional[int] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    @property
    def is_running(self) -> bool:
        return self._running

    def set_languages(self, source: str, target: str):
        self._source_lang = source
        self._target_lang = target

    def set_output_device(self, device_id: Optional[int]):
        self._output_device_id = device_id

    async def start_outgoing(
        self,
        input_device_id: Optional[int] = None,
        output_device_id: Optional[int] = None,
    ):
        if self._running:
            return

        self._running = True
        self._output_device_id = output_device_id
        self._loop = asyncio.get_running_loop()
        log.info(f"Pipeline starting: {self._source_lang} -> {self._target_lang}")

        from app.utils.constants import SUPPORTED_LANGUAGES
        stt_lang = SUPPORTED_LANGUAGES.get(self._source_lang, {}).get("deepgram", "tr")

        self._stt.on_transcript = self._on_transcript
        await self._stt.start_stream(stt_lang)

        self._send_task = asyncio.create_task(self._audio_send_loop())

        self._audio.start_capture(input_device_id, self._on_audio_captured)

        await self._bus.emit("pipeline_started", self._source_lang, self._target_lang)
        log.info("Outgoing pipeline running")

    async def stop(self):
        if not self._running:
            return

        self._running = False
        self._audio.stop_capture()
        self._audio.stop_loopback()

        if self._send_task:
            self._send_task.cancel()
            try:
                await self._send_task
            except asyncio.CancelledError:
                pass

        await self._stt.stop_stream()
        await self._bus.emit("pipeline_stopped")
        log.info("Pipeline stopped")

    def _on_audio_captured(self, audio_bytes: bytes):
        # Called from the PortAudio callback thread — marshal onto the loop,
        # because asyncio.Queue is not thread-safe.
        loop = self._loop
        if loop is None:
            return
        loop.call_soon_threadsafe(self._enqueue_audio, audio_bytes)

    def _enqueue_audio(self, audio_bytes: bytes):
        try:
            self._audio_queue.put_nowait(audio_bytes)
        except asyncio.QueueFull:
            # Drop the oldest chunk to keep latency bounded under backpressure.
            try:
                self._audio_queue.get_nowait()
                self._audio_queue.put_nowait(audio_bytes)
            except (asyncio.QueueEmpty, asyncio.QueueFull):
                pass

    async def _audio_send_loop(self):
        while self._running:
            try:
                audio_chunk = await asyncio.wait_for(self._audio_queue.get(), timeout=0.5)
                await self._stt.send_audio(audio_chunk)
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                log.error(f"Audio send error: {e}")

    def _on_transcript(self, text: str, is_final: bool):
        # Deepgram dispatches this on its listen thread; schedule the coroutine
        # on the event loop thread (asyncio.ensure_future needs a running loop).
        loop = self._loop
        if loop is None:
            return
        loop.call_soon_threadsafe(
            lambda: asyncio.ensure_future(self._process_transcript(text, is_final))
        )

    async def _process_transcript(self, text: str, is_final: bool):
        start_time = time.time()
        await self._bus.emit("transcript", text, is_final, self._source_lang)

        if not is_final:
            return

        from app.utils.constants import SUPPORTED_LANGUAGES
        lang_key = self._translator.lang_key
        source_code = SUPPORTED_LANGUAGES.get(self._source_lang, {}).get(lang_key, "TR")
        target_code = SUPPORTED_LANGUAGES.get(self._target_lang, {}).get(lang_key, "RU")

        # DeepL accepts regional codes (EN-US, PT-PT, ZH-HANS) only as the target;
        # the source must be the base language code.
        if lang_key == "deepl":
            source_code = source_code.split("-")[0]

        translated = await self._translator.translate(text, source_code, target_code)
        await self._bus.emit("translation", translated, self._target_lang)

        tts_provider = self._tts_manager.get_provider(self._target_lang)
        if tts_provider is None:
            log.error("No TTS provider available")
            return

        audio_chunks = []
        async for chunk in tts_provider.synthesize_stream(translated, self._target_lang.lower()):
            audio_chunks.append(chunk)

        if audio_chunks:
            full_audio = b"".join(audio_chunks)
            tts_sample_rate = tts_provider.get_sample_rate()
            self._audio.play_audio(full_audio, self._output_device_id, tts_sample_rate)
            await self._bus.emit("tts_played", len(full_audio))

        latency_ms = (time.time() - start_time) * 1000
        await self._bus.emit("latency", latency_ms)
        await self._bus.emit("translation_complete", text, translated, latency_ms)
        log.info(f"Pipeline latency: {latency_ms:.0f}ms | '{text}' -> '{translated}'")
