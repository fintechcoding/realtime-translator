import sys

from app.utils.config import Config
from app.utils.logger import log


def main():
    log.info("RealTime Translator starting...")
    config = Config()

    # Warn only about the keys the active translation provider actually needs.
    provider = config.get("translation.provider", "deepl")
    missing = []
    if not config.deepgram_api_key:
        missing.append("DEEPGRAM_API_KEY")
    if provider == "google" and not config.google_api_key:
        missing.append("GOOGLE_TRANSLATE_API_KEY")
    elif provider != "google" and not config.deepl_api_key:
        missing.append("DEEPL_API_KEY")
    if missing:
        log.warning(f"Missing API keys: {', '.join(missing)}. Set them in the app Settings or .env file.")

    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QIcon
    from qasync import QEventLoop
    import asyncio
    from pathlib import Path

    # Windows taskbar: distinct AppUserModelID so our icon shows (not Python's)
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "RealTimeTranslator.App"
            )
        except Exception:
            pass

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    icon_path = base / "app" / "gui" / "assets" / "app.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    # Apply premium dark theme
    from app.gui.styles.theme import get_stylesheet
    app.setStyleSheet(get_stylesheet())

    from app.gui.main_window import MainWindow

    window = MainWindow(config)
    window.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
