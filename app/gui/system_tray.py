from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction

from app.utils.constants import APP_NAME
from app.utils.i18n import t


class SystemTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setToolTip(APP_NAME)
        self._is_running = False
        self._setup_menu()

    def _setup_menu(self):
        menu = QMenu()

        self._show_action = QAction(t("tray.show"))
        self._show_action.triggered.connect(self._on_show)
        menu.addAction(self._show_action)

        self._toggle_action = QAction(t("tray.start"))
        menu.addAction(self._toggle_action)

        menu.addSeparator()

        self._quit_action = QAction(t("tray.quit"))
        self._quit_action.triggered.connect(self._on_quit)
        menu.addAction(self._quit_action)

        self.setContextMenu(menu)

    def set_toggle_callback(self, callback):
        self._toggle_action.triggered.connect(callback)

    def update_status(self, running: bool):
        self._is_running = running
        self._toggle_action.setText(t("tray.stop") if running else t("tray.start"))

    def retranslate_ui(self):
        self._show_action.setText(t("tray.show"))
        self._quit_action.setText(t("tray.quit"))
        self._toggle_action.setText(t("tray.stop") if self._is_running else t("tray.start"))

    def _on_show(self):
        parent = self.parent()
        if parent:
            parent.show()
            parent.activateWindow()

    def _on_quit(self):
        from PyQt6.QtWidgets import QApplication
        QApplication.quit()
