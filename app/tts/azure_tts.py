import asyncio
import io
from typing import AsyncIterator

import azure.cognitiveservices.speech as speechsdk

from app.tts.base import BaseTTS
from app.utils.constants import SUPPORTED_LANGUAGES
from app.utils.logger import log


class AzureTTS(BaseTTS):
    def __init__(self, speech_key: str, region: str = "westeurope"):
        self._speech_key = speech_key
        self._region = region
        self._sample_rate = 24000

    def _get_voice(self, language: str) -> str:
        lang_upper = language.upper()
        if lang_upper in SUPPORTED_LANGUAGES:
            return SUPPORTED_LANGUAGES[lang_upper]["azure_voice"]
        return "en-US-JennyNeural"

    async def synthesize(self, text: str, language: str) -> bytes:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._synthesize_sync, text, language)

    def _synthesize_sync(self, text: str, language: str) -> bytes:
        speech_config = speechsdk.SpeechConfig(
            subscription=self._speech_key, region=self._region
        )
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Raw24Khz16BitMonoPcm
        )
        speech_config.speech_synthesis_voice_name = self._get_voice(language)

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=None
        )

        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            log.error(f"Azure TTS canceled: {cancellation.reason}")
            if cancellation.error_details:
                log.error(f"Azure TTS error: {cancellation.error_details}")
            return b""
        return b""

    async def synthesize_stream(self, text: str, language: str) -> AsyncIterator[bytes]:
        audio_data = await self.synthesize(text, language)
        if audio_data:
            chunk_size = 4096
            stream = io.BytesIO(audio_data)
            while True:
                chunk = stream.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    def supports_language(self, language: str) -> bool:
        return language.upper() in SUPPORTED_LANGUAGES

    def get_sample_rate(self) -> int:
        return self._sample_rate
