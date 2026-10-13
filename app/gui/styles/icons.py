"""Inline SVG icon set rendered to QIcon/QPixmap (no external assets, no extra deps).

Lucide-style 24x24 outline icons. Color is injected at render time so the same
glyph can be drawn in any accent. Results are cached per (name, color, size).
"""

from __future__ import annotations

from PyQt6.QtCore import QByteArray, QRectF, QSize, Qt
from PyQt6.QtGui import QIcon, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer

# Raw inner SVG (paths only) for a 24x24 viewBox, stroke-based.
_PATHS: dict[str, str] = {
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>'
             '<path d="M12 3a15 15 0 0 1 4 9 15 15 0 0 1-4 9 15 15 0 0 1-4-9 15 15 0 0 1 4-9z"/>',
    "languages": '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/>'
                 '<path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    "settings": '<path d="M20 7h-9"/><path d="M14 17H5"/>'
                '<circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 16 14"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/>'
              '<path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    "type": '<polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/>'
            '<line x1="12" y1="4" x2="12" y2="20"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>'
           '<path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="22"/>',
    "speaker": '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>'
               '<path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M19 5a10 10 0 0 1 0 14"/>',
    "swap": '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
    "play": '<polygon points="6 4 20 12 6 20 6 4"/>',
    "stop": '<rect x="6" y="6" width="12" height="12" rx="2"/>',
    "key": '<circle cx="7.5" cy="15.5" r="4.5"/><path d="m21 3-9 9"/><path d="m15 6 3 3 3-3-3-3"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>'
            '<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "info": '<circle cx="12" cy="12" r="9"/><line x1="12" y1="11" x2="12" y2="16"/>'
            '<line x1="12" y1="8" x2="12" y2="8"/>',
    "waveform": '<path d="M2 12h2"/><path d="M6 8v8"/><path d="M10 4v16"/><path d="M14 7v10"/>'
                '<path d="M18 9v6"/><path d="M22 11v2"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
}

_FILLED = {"zap", "play"}  # glyphs that look better filled than stroked

_cache: dict[tuple[str, str, int], QIcon] = {}


def _svg_bytes(name: str, color: str, stroke_width: float = 2.0) -> bytes:
    inner = _PATHS.get(name, "")
    if name in _FILLED:
        fill, stroke = color, "none"
    else:
        fill, stroke = "none", color
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round">{inner}</svg>'
    ).encode("utf-8")


def pixmap(name: str, color: str = "#e6e9f0", size: int = 20, stroke_width: float = 2.0) -> QPixmap:
    renderer = QSvgRenderer(QByteArray(_svg_bytes(name, color, stroke_width)))
    dpr = 2  # render crisp on hi-dpi
    pm = QPixmap(QSize(size * dpr, size * dpr))
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    renderer.render(painter, QRectF(0, 0, size * dpr, size * dpr))
    painter.end()
    pm.setDevicePixelRatio(dpr)
    return pm


def icon(name: str, color: str = "#e6e9f0", size: int = 20, stroke_width: float = 2.0) -> QIcon:
    key = (name, color, size)
    if key not in _cache:
        _cache[key] = QIcon(pixmap(name, color, size, stroke_width))
    return _cache[key]
