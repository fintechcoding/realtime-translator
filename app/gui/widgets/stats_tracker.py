"""Session statistics tracker for translation metrics."""

import time
from dataclasses import dataclass, field
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal, QTimer


@dataclass
class TranslationRecord:
    timestamp: float
    source_text: str
    translated_text: str
    latency_ms: float


class StatsTracker(QObject):
    """Tracks session statistics: translations, characters, latency, etc."""

    stats_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._session_start: Optional[float] = None
        self._translation_count: int = 0
        self._total_characters: int = 0
        self._latencies: list[float] = []
        self._recent_translations: list[TranslationRecord] = []
        self._max_recent = 50
        self._deepl_usage: Optional[int] = None
        self._deepl_limit: Optional[int] = None

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.stats_updated.emit)

    def start_session(self):
        self._session_start = time.time()
        self._timer.start(1000)

    def stop_session(self):
        self._timer.stop()

    def reset(self):
        self._session_start = None
        self._translation_count = 0
        self._total_characters = 0
        self._latencies.clear()
        self._recent_translations.clear()
        self._timer.stop()

    def record_translation(self, source: str, translated: str, latency_ms: float):
        self._translation_count += 1
        self._total_characters += len(source) + len(translated)
        self._latencies.append(latency_ms)

        record = TranslationRecord(
            timestamp=time.time(),
            source_text=source,
            translated_text=translated,
            latency_ms=latency_ms,
        )
        self._recent_translations.append(record)
        if len(self._recent_translations) > self._max_recent:
            self._recent_translations.pop(0)

        self.stats_updated.emit()

    def set_deepl_usage(self, used: int, limit: int):
        self._deepl_usage = used
        self._deepl_limit = limit
        self.stats_updated.emit()

    @property
    def session_duration(self) -> float:
        if self._session_start is None:
            return 0.0
        return time.time() - self._session_start

    @property
    def session_duration_str(self) -> str:
        seconds = int(self.session_duration)
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    @property
    def translation_count(self) -> int:
        return self._translation_count

    @property
    def total_characters(self) -> int:
        return self._total_characters

    @property
    def total_characters_str(self) -> str:
        c = self._total_characters
        if c >= 1_000_000:
            return f"{c / 1_000_000:.1f}M"
        if c >= 1_000:
            return f"{c / 1_000:.1f}K"
        return str(c)

    @property
    def average_latency(self) -> float:
        if not self._latencies:
            return 0.0
        return sum(self._latencies) / len(self._latencies)

    @property
    def average_latency_str(self) -> str:
        avg = self.average_latency
        if avg == 0:
            return "--"
        return f"{avg:.0f}ms"

    @property
    def deepl_usage(self) -> Optional[int]:
        return self._deepl_usage

    @property
    def deepl_limit(self) -> Optional[int]:
        return self._deepl_limit

    @property
    def deepl_usage_percent(self) -> float:
        if self._deepl_usage is None or self._deepl_limit is None or self._deepl_limit == 0:
            return 0.0
        return (self._deepl_usage / self._deepl_limit) * 100

    @property
    def recent_translations(self) -> list[TranslationRecord]:
        return list(reversed(self._recent_translations))
