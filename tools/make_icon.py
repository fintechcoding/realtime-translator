"""Generate the application icon (app.ico + app.png) from the in-app globe mark.

Run once (or whenever the brand mark changes):
    python tools/make_icon.py
Outputs to app/gui/assets/.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PyQt6.QtWidgets import QApplication  # noqa: E402
from PyQt6.QtCore import QRectF, Qt  # noqa: E402
from PyQt6.QtGui import QPainter, QPixmap, QColor, QLinearGradient, QBrush, QImage  # noqa: E402

from app.gui.styles import icons  # noqa: E402


def build_pixmap(size: int) -> QPixmap:
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Rounded card with a vertical accent gradient
    radius = size * 0.22
    grad = QLinearGradient(0, 0, 0, size)
    grad.setColorAt(0.0, QColor("#5a86ff"))
    grad.setColorAt(1.0, QColor("#3f67e0"))
    p.setBrush(QBrush(grad))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawRoundedRect(QRectF(0, 0, size, size), radius, radius)

    # White globe mark centered
    glyph = int(size * 0.62)
    gpm = icons.pixmap("globe", "#ffffff", glyph, stroke_width=1.7)
    gx = (size - glyph) / 2
    gy = (size - glyph) / 2
    p.drawPixmap(int(gx), int(gy), gpm)
    p.end()
    return pm


def main():
    app = QApplication(sys.argv)  # noqa: F841
    out_dir = ROOT / "app" / "gui" / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Master PNG
    master = build_pixmap(256)
    master.save(str(out_dir / "app.png"), "PNG")

    # Multi-size ICO
    sizes = [256, 128, 64, 48, 32, 16]
    images = [build_pixmap(s).toImage().convertToFormat(QImage.Format.Format_ARGB32) for s in sizes]
    # Qt's ICO writer stores the QImage it is given; write the largest and let
    # Windows downscale, plus a 32px variant many shells prefer.
    master.save(str(out_dir / "app.ico"), "ICO")
    print("Wrote:", out_dir / "app.ico", "and app.png")


if __name__ == "__main__":
    main()
