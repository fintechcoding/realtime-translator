"""Corporate dark theme stylesheet for the application.

A refined deep-navy surface system with an indigo/blue primary accent and a
teal secondary. Component classes (card, pageHeader, statusPill, …) are shared
with main_window.py — keep object names in sync when editing either file.
"""

COLORS = {
    "bg": "#0a0d14",
    "surface": "#121620",
    "surface_alt": "#1a1f2c",
    "surface_hover": "#222838",
    "border": "#242b3a",
    "border_light": "#323a4d",
    "sidebar": "#0c0f17",
    "sidebar_hover": "#161b27",
    "accent": "#4f7cff",
    "accent_bright": "#6f96ff",
    "accent_dim": "rgba(79, 124, 255, 0.14)",
    "accent2": "#2dd4bf",
    "success": "#22c55e",
    "success_dim": "rgba(34, 197, 94, 0.14)",
    "warning": "#f59e0b",
    "warning_dim": "rgba(245, 158, 11, 0.14)",
    "error": "#ef4444",
    "error_dim": "rgba(239, 68, 68, 0.14)",
    "text": "#e7eaf2",
    "text_secondary": "#97a1b6",
    "text_muted": "#5a6479",
}

DARK_STYLESHEET = """
/* ===== Global ===== */
* {
    font-family: "Segoe UI", "Inter", "SF Pro Display", sans-serif;
    outline: none;
}

QMainWindow, QWidget#central {
    background-color: #0a0d14;
    color: #e7eaf2;
}

/* ===== Sidebar ===== */
QWidget#sidebar {
    background-color: #0c0f17;
    border-right: 1px solid #1c2230;
}

QLabel#sidebarLogo {
    color: #f3f5fa;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.3px;
}

QLabel#sidebarSubtitle {
    color: #5a6479;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
}

QLabel#navSection {
    color: #525c70;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

QPushButton.nav-btn {
    background-color: transparent;
    color: #97a1b6;
    border: none;
    border-radius: 9px;
    text-align: left;
    padding: 10px 14px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton.nav-btn:hover {
    background-color: #161b27;
    color: #e7eaf2;
}

QPushButton.nav-btn[active="true"] {
    background-color: rgba(79, 124, 255, 0.14);
    color: #ffffff;
    font-weight: 700;
}

QLabel#statusBadge {
    font-size: 11px;
    font-weight: 600;
    border-radius: 9px;
    padding: 8px 12px;
}

/* ===== Content ===== */
QWidget#contentArea, QWidget#pageRoot {
    background-color: #0a0d14;
}

QScrollArea {
    background-color: #0a0d14;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: #0a0d14;
}

/* ===== Page header ===== */
QLabel#pageTitle {
    color: #f3f5fa;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 0.2px;
}

QLabel#pageSubtitle {
    color: #7e889d;
    font-size: 12.5px;
    font-weight: 500;
}

QLabel.statusPill {
    font-size: 12px;
    font-weight: 700;
    border-radius: 13px;
    padding: 6px 15px;
}

QFrame#headerDivider {
    background-color: #1c2230;
    max-height: 1px;
    min-height: 1px;
    border: none;
}

/* ===== Cards ===== */
QFrame.card {
    background-color: #121620;
    border: 1px solid #242b3a;
    border-radius: 14px;
}

QLabel.cardTitle {
    color: #c3cad9;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.4px;
    background: transparent;
    border: none;
}

QLabel.cardHint {
    color: #5a6479;
    font-size: 11px;
    background: transparent;
    border: none;
}

QLabel.fieldLabel {
    color: #7e889d;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4px;
    background: transparent;
    border: none;
}

/* Legacy GroupBox (settings guide/about) kept consistent */
QGroupBox {
    background-color: #121620;
    border: 1px solid #242b3a;
    border-radius: 14px;
    margin-top: 18px;
    padding: 18px 18px 16px 18px;
    font-size: 12px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    top: 1px;
    padding: 2px 8px;
    background-color: #121620;
    color: #c3cad9;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

/* ===== Labels ===== */
QLabel {
    color: #e7eaf2;
    font-size: 13px;
    background: transparent;
}

QLabel.secondary {
    color: #97a1b6;
}

/* ===== Combo Boxes ===== */
QComboBox {
    background-color: #1a1f2c;
    color: #e7eaf2;
    border: 1px solid #2a3140;
    border-radius: 10px;
    padding: 9px 14px;
    min-height: 22px;
    font-size: 13px;
}

QComboBox:hover {
    border-color: #3a4457;
    background-color: #202636;
}

QComboBox:focus {
    border-color: #4f7cff;
}

QComboBox:disabled {
    color: #5a6479;
    background-color: #151a25;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #7e889d;
    margin-right: 11px;
}

QComboBox QAbstractItemView {
    background-color: #1a1f2c;
    color: #e7eaf2;
    border: 1px solid #2a3140;
    border-radius: 10px;
    selection-background-color: #4f7cff;
    selection-color: white;
    outline: none;
    padding: 5px;
}

QComboBox QAbstractItemView::item {
    padding: 7px 12px;
    min-height: 28px;
    border-radius: 7px;
}

/* ===== Primary Action Button ===== */
QPushButton#startBtn {
    background-color: #4f7cff;
    color: white;
    border: none;
    border-radius: 13px;
    font-size: 14px;
    font-weight: 800;
    padding: 14px;
    letter-spacing: 0.4px;
}

QPushButton#startBtn:hover {
    background-color: #6f96ff;
}

QPushButton#startBtn:pressed {
    background-color: #3f67e0;
}

QPushButton#startBtn[running="true"] {
    background-color: #ef4444;
}

QPushButton#startBtn[running="true"]:hover {
    background-color: #f45b5b;
}

/* ===== Generic Buttons ===== */
QPushButton {
    background-color: #1a1f2c;
    color: #e7eaf2;
    border: 1px solid #2a3140;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #222838;
    border-color: #3a4457;
}

QPushButton:pressed {
    background-color: #161b27;
}

QPushButton.accent-btn {
    background-color: #4f7cff;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    font-size: 13px;
}

QPushButton.accent-btn:hover {
    background-color: #6f96ff;
}

QPushButton.accent-btn:pressed {
    background-color: #3f67e0;
}

QPushButton.link-btn {
    background: transparent;
    border: none;
    color: #6f96ff;
    text-align: left;
    padding: 2px 0;
    font-size: 12px;
    font-weight: 600;
}

QPushButton.link-btn:hover {
    color: #93b2ff;
}

QPushButton#swapBtn {
    background-color: #1a1f2c;
    border: 1px solid #2a3140;
    border-radius: 19px;
    color: #6f96ff;
}

QPushButton#swapBtn:hover {
    background-color: #4f7cff;
    border-color: #4f7cff;
    color: white;
}

QPushButton.toggle-btn {
    background-color: #222838;
    border: 1px solid #2a3140;
    border-radius: 10px;
    color: #97a1b6;
    font-size: 11px;
    font-weight: 600;
    padding: 8px 12px;
}

QPushButton.toggle-btn:hover {
    background-color: #2b3243;
    color: #e7eaf2;
}

/* ===== Text Edits (Transcript) ===== */
QTextEdit {
    background-color: #0d111a;
    color: #e7eaf2;
    border: 1px solid #222a38;
    border-radius: 11px;
    padding: 13px;
    font-family: "Cascadia Code", "Consolas", "Courier New", monospace;
    font-size: 12.5px;
    line-height: 1.6;
    selection-background-color: rgba(79, 124, 255, 0.4);
}

QTextEdit:focus {
    border-color: #2e3850;
}

/* ===== Line Edits ===== */
QLineEdit {
    background-color: #1a1f2c;
    color: #e7eaf2;
    border: 1px solid #2a3140;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    selection-background-color: rgba(79, 124, 255, 0.4);
}

QLineEdit:hover {
    border-color: #3a4457;
}

QLineEdit:focus {
    border-color: #4f7cff;
}

/* ===== Progress Bar ===== */
QProgressBar {
    background-color: #1a1f2c;
    border: none;
    border-radius: 7px;
    text-align: center;
    color: #e7eaf2;
    font-size: 11px;
    font-weight: 700;
    min-height: 14px;
    max-height: 14px;
}

QProgressBar::chunk {
    background-color: #4f7cff;
    border-radius: 7px;
}

/* ===== Scroll Bars ===== */
QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
    margin: 4px 0;
}

QScrollBar::handle:vertical {
    background-color: #2a3140;
    border-radius: 4px;
    min-height: 40px;
}

QScrollBar::handle:vertical:hover {
    background-color: #3a4457;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none; border: none; height: 0;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
    margin: 0 4px;
}

QScrollBar::handle:horizontal {
    background-color: #2a3140;
    border-radius: 4px;
    min-width: 40px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #3a4457;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none; border: none; width: 0;
}

/* ===== Text Browser ===== */
QTextBrowser {
    background-color: #0d111a;
    color: #e7eaf2;
    border: 1px solid #222a38;
    border-radius: 11px;
    padding: 14px;
    font-size: 13px;
}

/* ===== Splitter ===== */
QSplitter::handle {
    background-color: transparent;
    width: 10px;
}

/* ===== Table Widget ===== */
QTableWidget {
    background-color: #121620;
    alternate-background-color: #161b27;
    color: #e7eaf2;
    border: 1px solid #242b3a;
    border-radius: 12px;
    gridline-color: transparent;
    font-size: 12px;
    selection-background-color: rgba(79, 124, 255, 0.18);
    selection-color: #ffffff;
    outline: none;
}

QTableWidget::item {
    padding: 9px 12px;
    border: none;
}

QHeaderView::section {
    background-color: #121620;
    color: #7e889d;
    border: none;
    border-bottom: 1px solid #242b3a;
    padding: 10px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

QTableCornerButton::section {
    background-color: #121620;
    border: none;
}

/* ===== Tooltips ===== */
QToolTip {
    background-color: #1a1f2c;
    color: #e7eaf2;
    border: 1px solid #2a3140;
    border-radius: 7px;
    padding: 6px 10px;
    font-size: 12px;
}

/* ===== Message Box ===== */
QMessageBox {
    background-color: #121620;
}

QMessageBox QLabel {
    color: #e7eaf2;
    font-size: 13px;
}

QMessageBox QPushButton {
    min-width: 84px;
    padding: 8px 20px;
}
"""


def get_stylesheet() -> str:
    return DARK_STYLESHEET
