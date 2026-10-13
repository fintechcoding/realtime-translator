"""Corporate theme system for the application — light and dark palettes.

A single QSS template is filled from a palette dict, so light/dark stay in sync
and the app can switch at runtime. Component classes (card, pageHeader,
statusPill, statValue, …) are shared with main_window.py — keep names in sync.
"""

from string import Template

# ── Palettes ─────────────────────────────────────────────────────────
PALETTES = {
    "dark": {
        "bg": "#0a0d14",
        "surface": "#121620",
        "surface_alt": "#1a1f2c",
        "surface_hover": "#222838",
        "border": "#242b3a",
        "border_light": "#323a4d",
        "sidebar": "#0c0f17",
        "sidebar_border": "#1c2230",
        "sidebar_hover": "#161b27",
        "accent": "#4f7cff",
        "accent_bright": "#6f96ff",
        "accent_hover": "#6f96ff",
        "accent_pressed": "#3f67e0",
        "accent_dim": "rgba(79, 124, 255, 0.14)",
        "teal": "#2dd4bf",
        "ok": "#22c55e",
        "warn": "#f59e0b",
        "err": "#ef4444",
        "ok_dim": "rgba(34, 197, 94, 0.14)",
        "warn_dim": "rgba(245, 158, 11, 0.14)",
        "teal_dim": "rgba(45, 212, 191, 0.14)",
        "gray_dim": "rgba(90, 100, 121, 0.16)",
        "gray_fg": "#8a93a6",
        "text": "#e7eaf2",
        "text_sec": "#97a1b6",
        "text_muted": "#5a6479",
        "input_bg": "#1a1f2c",
        "input_border": "#2a3140",
        "input_hover_border": "#3a4457",
        "transcript_bg": "#0d111a",
        "transcript_border": "#222a38",
        "nav_active_text": "#ffffff",
        "nav_active_icon": "#ffffff",
        "nav_active_bg": "rgba(79, 124, 255, 0.14)",
        "on_accent": "#ffffff",
        "scrollbar": "#2a3140",
        "scrollbar_hover": "#3a4457",
        "table_alt": "#161b27",
        "tooltip_bg": "#1a1f2c",
        "selection": "rgba(79, 124, 255, 0.4)",
        "logo_sub": "#5a6479",
        "divider": "#1c2230",
        "disabled_bg": "#151a25",
    },
    "light": {
        "bg": "#eef1f6",
        "surface": "#ffffff",
        "surface_alt": "#f4f6fa",
        "surface_hover": "#e9edf4",
        "border": "#e2e7ef",
        "border_light": "#cfd6e2",
        "sidebar": "#ffffff",
        "sidebar_border": "#e6eaf1",
        "sidebar_hover": "#f1f4f9",
        "accent": "#3b6fe0",
        "accent_bright": "#2f5fd0",
        "accent_hover": "#305fd0",
        "accent_pressed": "#274fb5",
        "accent_dim": "rgba(59, 111, 224, 0.12)",
        "teal": "#0d9488",
        "ok": "#16a34a",
        "warn": "#d97706",
        "err": "#dc2626",
        "ok_dim": "rgba(22, 163, 74, 0.12)",
        "warn_dim": "rgba(217, 119, 6, 0.12)",
        "teal_dim": "rgba(13, 148, 136, 0.12)",
        "gray_dim": "rgba(100, 116, 139, 0.14)",
        "gray_fg": "#64748b",
        "text": "#16203a",
        "text_sec": "#52607a",
        "text_muted": "#8a94a6",
        "input_bg": "#f6f8fc",
        "input_border": "#d7deea",
        "input_hover_border": "#b9c4d6",
        "transcript_bg": "#f8fafc",
        "transcript_border": "#e2e7ef",
        "nav_active_text": "#1d4ed8",
        "nav_active_icon": "#1d4ed8",
        "nav_active_bg": "rgba(59, 111, 224, 0.12)",
        "on_accent": "#ffffff",
        "scrollbar": "#cfd6e2",
        "scrollbar_hover": "#b3bcce",
        "table_alt": "#f6f8fc",
        "tooltip_bg": "#1f2a44",
        "selection": "rgba(59, 111, 224, 0.28)",
        "logo_sub": "#94a0b4",
        "divider": "#e6eaf1",
        "disabled_bg": "#eef1f6",
    },
}

# Backwards-compatible default palette.
COLORS = PALETTES["dark"]


_TEMPLATE = Template("""
/* ===== Global ===== */
* {
    font-family: "Segoe UI", "Inter", "SF Pro Display", sans-serif;
    outline: none;
}

QMainWindow, QWidget#central {
    background-color: ${bg};
    color: ${text};
}

/* ===== Sidebar ===== */
QWidget#sidebar {
    background-color: ${sidebar};
    border-right: 1px solid ${sidebar_border};
}

QFrame#navSep { background-color: ${divider}; }
QFrame#hLine { background-color: ${border}; max-height: 1px; min-height: 1px; border: none; }

QLabel#sidebarLogo {
    color: ${text};
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.3px;
}

QLabel#sidebarSubtitle {
    color: ${logo_sub};
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
}

QLabel#navSection {
    color: ${text_muted};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

QPushButton.nav-btn {
    background-color: transparent;
    color: ${text_sec};
    border: none;
    border-radius: 9px;
    text-align: left;
    padding: 10px 14px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton.nav-btn:hover {
    background-color: ${sidebar_hover};
    color: ${text};
}

QPushButton.nav-btn[active="true"] {
    background-color: ${nav_active_bg};
    color: ${nav_active_text};
    font-weight: 700;
}

/* ===== Content ===== */
QWidget#contentArea, QWidget#pageRoot {
    background-color: ${bg};
}

QScrollArea {
    background-color: ${bg};
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: ${bg};
}

/* ===== Page header ===== */
QLabel#pageTitle {
    color: ${text};
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 0.2px;
}

QLabel#pageSubtitle {
    color: ${text_sec};
    font-size: 12.5px;
    font-weight: 500;
}

QFrame#headerDivider {
    background-color: ${divider};
    max-height: 1px;
    min-height: 1px;
    border: none;
}

/* ===== Cards ===== */
QFrame.card {
    background-color: ${surface};
    border: 1px solid ${border};
    border-radius: 14px;
}

QLabel.cardTitle {
    color: ${text};
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.4px;
    background: transparent;
    border: none;
}

QLabel.cardHint { color: ${text_muted}; font-size: 11px; background: transparent; border: none; }

QLabel.fieldLabel {
    color: ${text_sec};
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4px;
    background: transparent;
    border: none;
}

QLabel.statValue { color: ${text}; font-size: 28px; font-weight: 800; background: transparent; border: none; }
QLabel.statName  { color: ${text_sec}; font-size: 11.5px; font-weight: 600; background: transparent; border: none; }

QLabel.settingTitle { color: ${text}; font-size: 14px; font-weight: 700; background: transparent; }
QLabel.settingDesc  { color: ${text_muted}; font-size: 11px; background: transparent; }
QLabel.settingInfo  { color: ${text_sec}; font-size: 12px; background: transparent; }
QLabel.note         { color: ${text_muted}; font-size: 11px; font-style: italic; background: transparent; }
QLabel.secondary    { color: ${text_sec}; font-size: 12px; background: transparent; }
QLabel.verLabel     { color: ${text_muted}; font-size: 11px; background: transparent; }

/* Legacy GroupBox (settings groups) */
QGroupBox {
    background-color: ${surface};
    border: 1px solid ${border};
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
    background-color: ${surface};
    color: ${text};
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

/* ===== Labels ===== */
QLabel { color: ${text}; font-size: 13px; background: transparent; }

/* ===== Combo Boxes ===== */
QComboBox {
    background-color: ${input_bg};
    color: ${text};
    border: 1px solid ${input_border};
    border-radius: 10px;
    padding: 9px 14px;
    min-height: 22px;
    font-size: 13px;
}

QComboBox:hover { border-color: ${input_hover_border}; background-color: ${surface_hover}; }
QComboBox:focus { border-color: ${accent}; }
QComboBox:disabled { color: ${text_muted}; background-color: ${disabled_bg}; }

QComboBox::drop-down { border: none; width: 30px; }

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid ${text_sec};
    margin-right: 11px;
}

QComboBox QAbstractItemView {
    background-color: ${surface};
    color: ${text};
    border: 1px solid ${input_border};
    border-radius: 10px;
    selection-background-color: ${accent};
    selection-color: ${on_accent};
    outline: none;
    padding: 5px;
}

QComboBox QAbstractItemView::item { padding: 7px 12px; min-height: 28px; border-radius: 7px; }

/* ===== Primary Action Button ===== */
QPushButton#startBtn {
    background-color: ${accent};
    color: ${on_accent};
    border: none;
    border-radius: 13px;
    font-size: 14px;
    font-weight: 800;
    padding: 14px;
    letter-spacing: 0.4px;
}

QPushButton#startBtn:hover { background-color: ${accent_hover}; }
QPushButton#startBtn:pressed { background-color: ${accent_pressed}; }
QPushButton#startBtn[running="true"] { background-color: ${err}; }
QPushButton#startBtn[running="true"]:hover { background-color: ${err}; }

/* ===== Generic Buttons ===== */
QPushButton {
    background-color: ${input_bg};
    color: ${text};
    border: 1px solid ${input_border};
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton:hover { background-color: ${surface_hover}; border-color: ${input_hover_border}; }
QPushButton:pressed { background-color: ${surface_alt}; }

QPushButton.accent-btn {
    background-color: ${accent};
    color: ${on_accent};
    border: none;
    border-radius: 10px;
    font-weight: 700;
    font-size: 13px;
}

QPushButton.accent-btn:hover { background-color: ${accent_hover}; }
QPushButton.accent-btn:pressed { background-color: ${accent_pressed}; }

QPushButton.link-btn {
    background: transparent;
    border: none;
    color: ${accent};
    text-align: left;
    padding: 2px 0;
    font-size: 12px;
    font-weight: 600;
}

QPushButton.link-btn:hover { color: ${accent_bright}; }

QPushButton#swapBtn {
    background-color: ${input_bg};
    border: 1px solid ${input_border};
    border-radius: 19px;
}

QPushButton#swapBtn:hover { background-color: ${accent}; border-color: ${accent}; }

QPushButton.toggle-btn {
    background-color: ${surface_hover};
    border: 1px solid ${input_border};
    border-radius: 10px;
    color: ${text_sec};
    font-size: 11px;
    font-weight: 600;
    padding: 8px 12px;
}

QPushButton.toggle-btn:hover { background-color: ${surface_alt}; color: ${text}; }

/* ===== Text Edits (Transcript) ===== */
QTextEdit {
    background-color: ${transcript_bg};
    color: ${text};
    border: 1px solid ${transcript_border};
    border-radius: 11px;
    padding: 13px;
    font-family: "Cascadia Code", "Consolas", "Courier New", monospace;
    font-size: 12.5px;
    selection-background-color: ${selection};
}

QTextEdit:focus { border-color: ${accent}; }

/* ===== Line Edits ===== */
QLineEdit {
    background-color: ${input_bg};
    color: ${text};
    border: 1px solid ${input_border};
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    selection-background-color: ${selection};
}

QLineEdit:hover { border-color: ${input_hover_border}; }
QLineEdit:focus { border-color: ${accent}; }

/* ===== Progress Bar ===== */
QProgressBar {
    background-color: ${input_bg};
    border: none;
    border-radius: 7px;
    text-align: center;
    color: ${text};
    font-size: 11px;
    font-weight: 700;
    min-height: 14px;
    max-height: 14px;
}

QProgressBar::chunk { background-color: ${accent}; border-radius: 7px; }

/* ===== Scroll Bars ===== */
QScrollBar:vertical { background-color: transparent; width: 8px; margin: 4px 0; }
QScrollBar::handle:vertical { background-color: ${scrollbar}; border-radius: 4px; min-height: 40px; }
QScrollBar::handle:vertical:hover { background-color: ${scrollbar_hover}; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; border: none; height: 0; }

QScrollBar:horizontal { background-color: transparent; height: 8px; margin: 0 4px; }
QScrollBar::handle:horizontal { background-color: ${scrollbar}; border-radius: 4px; min-width: 40px; }
QScrollBar::handle:horizontal:hover { background-color: ${scrollbar_hover}; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; border: none; width: 0; }

/* ===== Text Browser ===== */
QTextBrowser {
    background-color: ${transcript_bg};
    color: ${text};
    border: 1px solid ${transcript_border};
    border-radius: 11px;
    padding: 14px;
    font-size: 13px;
}

/* ===== Splitter ===== */
QSplitter::handle { background-color: transparent; width: 10px; }

/* ===== Table Widget ===== */
QTableWidget {
    background-color: ${surface};
    alternate-background-color: ${table_alt};
    color: ${text};
    border: 1px solid ${border};
    border-radius: 12px;
    gridline-color: transparent;
    font-size: 12px;
    selection-background-color: ${accent_dim};
    selection-color: ${text};
    outline: none;
}

QTableWidget::item { padding: 9px 12px; border: none; }

QHeaderView::section {
    background-color: ${surface};
    color: ${text_sec};
    border: none;
    border-bottom: 1px solid ${border};
    padding: 10px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

QTableCornerButton::section { background-color: ${surface}; border: none; }

/* ===== Tooltips ===== */
QToolTip {
    background-color: ${tooltip_bg};
    color: #ffffff;
    border: 1px solid ${input_border};
    border-radius: 7px;
    padding: 6px 10px;
    font-size: 12px;
}

/* ===== Message Box ===== */
QMessageBox { background-color: ${surface}; }
QMessageBox QLabel { color: ${text}; font-size: 13px; }
QMessageBox QPushButton { min-width: 84px; padding: 8px 20px; }
""")


def palette(mode: str = "dark") -> dict:
    """Return the color palette dict for *mode* ('dark' or 'light')."""
    return PALETTES.get(mode, PALETTES["dark"])


def get_stylesheet(mode: str = "dark") -> str:
    """Return the full QSS stylesheet for *mode*."""
    return _TEMPLATE.substitute(palette(mode))
