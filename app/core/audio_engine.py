import threading
from typing import Callable, Optional

import numpy as np
import sounddevice as sd

from app.utils.logger import log


class AudioEngine:
    def __init__(self, sample_rate: int = 16000, channels: int = 1, buffer_ms: int = 100):
        self.sample_rate = sample_rate
        self.channels = channels
        self.block_size = int(sample_rate * buffer_ms / 1000)
        self._capture_stream: Optional[sd.InputStream] = None
        self._loopback_stream: Optional[sd.InputStream] = None
        self._playback_stream: Optional[sd.OutputStream] = None
        self._playback_lock = threading.Lock()

    def list_input_devices(self) -> list[dict]:
        devices = sd.query_devices()
        result = []
        for i, d in enumerate(devices):
            if d["max_input_channels"] > 0:
                result.append({"id": i, "name": d["name"], "channels": d["max_input_channels"]})
        return result

    def list_output_devices(self) -> list[dict]:
        devices = sd.query_devices()
        result = []
        for i, d in enumerate(devices):
            if d["max_output_channels"] > 0:
                result.append({"id": i, "name": d["name"], "channels": d["max_output_channels"]})
        return result

    def start_capture(self, device_id: Optional[int], callback: Callable[[bytes], None]):
        if self._capture_stream is not None:
            self.stop_capture()

        def _audio_callback(indata, frames, time_info, status):
            if status:
                log.warning(f"Capture status: {status}")
            audio_bytes = indata.tobytes()
            callback(audio_bytes)

        self._capture_stream = sd.InputStream(
            device=device_id,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            blocksize=self.block_size,
            callback=_audio_callback,
        )
        self._capture_stream.start()
        log.info(f"Capture started (device={device_id}, rate={self.sample_rate}, block={self.block_size})")

    def stop_capture(self):
        if self._capture_stream is not None:
            self._capture_stream.stop()
            self._capture_stream.close()
            self._capture_stream = None
            log.info("Capture stopped")

    def start_loopback(self, device_id: Optional[int], callback: Callable[[bytes], None]):
        if self._loopback_stream is not None:
            self.stop_loopback()

        try:
            import sounddevice as sd_wasapi

            def _loopback_callback(indata, frames, time_info, status):
                if status:
                    log.warning(f"Loopback status: {status}")
                audio_bytes = indata.tobytes()
                callback(audio_bytes)

            self._loopback_stream = sd_wasapi.InputStream(
                device=device_id,
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="int16",
                blocksize=self.block_size,
                callback=_loopback_callback,
                extra_settings=sd_wasapi.WasapiSettings(loopback=True) if device_id else None,
            )
            self._loopback_stream.start()
            log.info(f"Loopback started (device={device_id})")
        except Exception as e:
            log.error(f"Loopback failed: {e}. WASAPI loopback may not be supported on this device.")

    def stop_loopback(self):
        if self._loopback_stream is not None:
            self._loopback_stream.stop()
            self._loopback_stream.close()
            self._loopback_stream = None
            log.info("Loopback stopped")

    def play_audio(self, audio_data: bytes, device_id: Optional[int] = None, sample_rate: int = None):
        rate = sample_rate or self.sample_rate
        with self._playback_lock:
            try:
                audio_np = np.frombuffer(audio_data, dtype=np.int16)
                sd.play(audio_np, samplerate=rate, device=device_id, blocking=False)
            except Exception as e:
                log.error(f"Playback error: {e}")

    def start_output_stream(self, device_id: Optional[int] = None, sample_rate: int = None) -> sd.OutputStream:
        rate = sample_rate or self.sample_rate
        stream = sd.OutputStream(
            device=device_id,
            samplerate=rate,
            channels=self.channels,
            dtype="int16",
        )
        stream.start()
        return stream

    def stop_all(self):
        self.stop_capture()
        self.stop_loopback()
        sd.stop()
        log.info("All audio stopped")
