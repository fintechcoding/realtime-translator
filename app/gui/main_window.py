import asyncio
import time
import webbrowser
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal, QObject, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QLabel,
    QTextEdit,
    QGroupBox,
    QSplitter,
    QStackedWidget,
    QLineEdit,
    QTextBrowser,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QScrollArea,
    QFrame,
    QMessageBox,
)

from app.core.audio_engine import AudioEngine
from app.core.audio_router import AudioRouter
from app.core.event_bus import EventBus
from app.core.pipeline import TranslationPipeline
from app.stt.deepgram_stt import DeepgramSTT
from app.translation.deepl_translator import DeepLTranslator
from app.translation.google_translator import GoogleTranslator
from app.tts.azure_tts import AzureTTS
from app.tts.deepgram_tts import DeepgramTTS
from app.tts.provider_manager import TTSProviderManager
from app.utils.config import Config
from app.utils.constants import SUPPORTED_LANGUAGES, APP_NAME, APP_VERSION
from app.utils.i18n import t, set_language, get_language, available_languages
from app.utils import key_validator
from app.gui.widgets.stats_tracker import StatsTracker
from app.gui.styles import theme, icons


class SignalBridge(QObject):
    transcript_signal = pyqtSignal(str, bool, str)
    translation_signal = pyqtSignal(str, str)
    latency_signal = pyqtSignal(float)
    status_signal = pyqtSignal(str)
    translation_complete_signal = pyqtSignal(str, str, float)


class MainWindow(QMainWindow):
    def __init__(self, config: Config):
        super().__init__()
        self._config = config
        self._pipeline: Optional[TranslationPipeline] = None
        self._event_bus = EventBus()
        self._signals = SignalBridge()
        self._running = False
        self._audio_router = AudioRouter()
        self._stats = StatsTracker(self)
        self._nav_buttons: list[QPushButton] = []

        # Theme state
        self._mode = self._config.get("gui.theme", "light")
        if self._mode not in ("light", "dark"):
            self._mode = "light"
        self._pal = theme.palette(self._mode)
        self._themed_icons: list[tuple] = []   # (kind, widget, name, color_key, size)
        self._themed_chips: list[tuple] = []    # (label, dim_key)
        self._pill_state = "idle"
        self._badge_state = "idle"
        self._vb_state: Optional[bool] = None

        # Apply saved UI language before building UI
        saved_lang = self._config.get("gui.language", "tr")
        set_language(saved_lang)

        self._setup_ui()
        self._apply_theme(self._mode)
        self._connect_signals()
        self._populate_devices()
        self._check_first_run()

    # Palette shortcut
    def _c(self, key: str) -> str:
        return self._pal[key]

    # ================================================================
    #  UI SETUP
    # ================================================================

    def _setup_ui(self):
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1060, 720)

        icon_path = Path(__file__).resolve().parent / "assets" / "app.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_sidebar())

        self._pages = QStackedWidget()
        self._pages.setObjectName("contentArea")
        self._pages.addWidget(self._build_translation_page())
        self._pages.addWidget(self._build_stats_page())
        self._pages.addWidget(self._build_settings_page())
        root.addWidget(self._pages, 1)

    # ── Theming ──────────────────────────────────────────────────

    def _reg_icon_label(self, label: QLabel, name: str, color_key: str, size: int) -> QLabel:
        self._themed_icons.append(("label", label, name, color_key, size))
        label.setPixmap(icons.pixmap(name, self._pal[color_key], size))
        return label

    def _reg_icon_button(self, btn: QPushButton, name: str, color_key: str, size: int) -> QPushButton:
        self._themed_icons.append(("button", btn, name, color_key, size))
        btn.setIcon(icons.icon(name, self._pal[color_key], size))
        btn.setIconSize(QSize(size, size))
        return btn

    def _apply_theme(self, mode: str):
        self._mode = mode
        self._pal = theme.palette(mode)
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(theme.get_stylesheet(mode))

        # Recolor registered icons
        for kind, widget, name, color_key, size in self._themed_icons:
            if kind == "label":
                widget.setPixmap(icons.pixmap(name, self._pal[color_key], size))
            else:
                widget.setIcon(icons.icon(name, self._pal[color_key], size))

        # Stat-card icon chips
        for label, dim_key in self._themed_chips:
            label.setStyleSheet(f"background-color: {self._pal[dim_key]}; border-radius: 10px;")

        # Nav icons (active/inactive colors)
        self._set_active_nav(self._pages.currentIndex() if hasattr(self, "_pages") else 0)

        # Start button icon reflects running state
        if hasattr(self, "_start_btn"):
            self._start_btn.setIcon(icons.icon("stop" if self._running else "play", self._pal["on_accent"], 18))

        # Dynamic state styles
        self._style_pill(self._tr_pill, self._pill_state)
        self._update_sidebar_badge(self._badge_state)
        self._apply_status_default_colors()
        self._apply_vb_status_color()

    def _apply_status_default_colors(self):
        if not self._running:
            self._status_label.setStyleSheet(f"color: {self._c('text_sec')}; font-size: 12px;")
            self._latency_label.setStyleSheet(f"color: {self._c('text_muted')}; font-size: 12px;")

    def _apply_vb_status_color(self):
        if self._vb_state is True:
            self._vb_status.setStyleSheet(f"color: {self._c('ok')}; font-size: 11px;")
        elif self._vb_state is False:
            self._vb_status.setStyleSheet(f"color: {self._c('warn')}; font-size: 11px;")

    # ── Shared building blocks ───────────────────────────────────

    def _build_header(self, title: str, subtitle: str, pill: bool = False):
        wrap = QWidget()
        v = QVBoxLayout(wrap)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(16)

        row = QHBoxLayout()
        row.setSpacing(12)
        col = QVBoxLayout()
        col.setSpacing(4)
        tl = QLabel(title)
        tl.setObjectName("pageTitle")
        sb = QLabel(subtitle)
        sb.setObjectName("pageSubtitle")
        col.addWidget(tl)
        col.addWidget(sb)
        row.addLayout(col)
        row.addStretch()

        pill_lbl = None
        if pill:
            pill_lbl = QLabel()
            pill_lbl.setProperty("class", "statusPill")
            row.addWidget(pill_lbl, 0, Qt.AlignmentFlag.AlignVCenter)
        v.addLayout(row)

        div = QFrame()
        div.setObjectName("headerDivider")
        div.setFixedHeight(1)
        v.addWidget(div)
        return wrap, tl, sb, pill_lbl

    def _card(self):
        card = QFrame()
        card.setProperty("class", "card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(18, 16, 18, 18)
        lay.setSpacing(12)
        return card, lay

    def _card_title_row(self, icon_name: str, text: str, color_key: str = "accent"):
        row = QHBoxLayout()
        row.setSpacing(9)
        ic = QLabel()
        ic.setFixedSize(16, 16)
        self._reg_icon_label(ic, icon_name, color_key, 16)
        lbl = QLabel(text)
        lbl.setProperty("class", "cardTitle")
        row.addWidget(ic)
        row.addWidget(lbl)
        row.addStretch()
        return row, lbl

    def _style_pill(self, lbl: QLabel, state: str):
        self._pill_state = state
        palette = {
            "idle": (self._c("accent_dim"), self._c("accent"), t("sidebar.ready")),
            "active": (self._c("ok_dim"), self._c("ok"), t("sidebar.active")),
            "stopped": (self._c("gray_dim"), self._c("gray_fg"), t("sidebar.stopped")),
        }
        bg, fg, text = palette.get(state, palette["idle"])
        lbl.setText(f"●  {text}")
        lbl.setStyleSheet(
            f"background-color: {bg}; color: {fg}; font-size: 12px; font-weight: 700;"
            f" border-radius: 13px; padding: 6px 15px;"
        )

    # ── Sidebar ──────────────────────────────────────────────────

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(232)

        lay = QVBoxLayout(sidebar)
        lay.setContentsMargins(0, 0, 0, 18)
        lay.setSpacing(0)

        logo_area = QWidget()
        logo_lay = QHBoxLayout(logo_area)
        logo_lay.setContentsMargins(20, 24, 20, 22)
        logo_lay.setSpacing(11)

        mark = QLabel()
        mark.setFixedSize(26, 26)
        self._reg_icon_label(mark, "globe", "accent", 26)
        logo_lay.addWidget(mark, 0, Qt.AlignmentFlag.AlignVCenter)

        name_col = QVBoxLayout()
        name_col.setSpacing(1)
        logo = QLabel("RealTime")
        logo.setObjectName("sidebarLogo")
        sub = QLabel("TRANSLATOR")
        sub.setObjectName("sidebarSubtitle")
        name_col.addWidget(logo)
        name_col.addWidget(sub)
        logo_lay.addLayout(name_col)
        logo_lay.addStretch()
        lay.addWidget(logo_area)

        sep = QFrame()
        sep.setObjectName("navSep")
        sep.setFixedHeight(1)
        sep.setContentsMargins(20, 0, 20, 0)
        lay.addWidget(sep)
        lay.addSpacing(16)

        self._nav_section = QLabel("  " + t("sidebar.section_main"))
        self._nav_section.setObjectName("navSection")
        self._nav_section.setContentsMargins(20, 0, 0, 0)
        lay.addWidget(self._nav_section)
        lay.addSpacing(6)

        self._nav_keys = [
            "sidebar.translation",
            "sidebar.statistics",
            "sidebar.settings",
        ]
        self._nav_icons = ["languages", "chart", "settings"]
        nav_wrap = QWidget()
        nav_lay = QVBoxLayout(nav_wrap)
        nav_lay.setContentsMargins(12, 0, 12, 0)
        nav_lay.setSpacing(4)
        for idx, (key, icn) in enumerate(zip(self._nav_keys, self._nav_icons)):
            btn = QPushButton("  " + t(key))
            btn.setProperty("class", "nav-btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(42)
            btn.setIcon(icons.icon(icn, self._pal["text_sec"], 18))
            btn.setIconSize(QSize(18, 18))
            btn.clicked.connect(lambda _, i=idx: self._navigate_to(i))
            nav_lay.addWidget(btn)
            self._nav_buttons.append(btn)
        lay.addWidget(nav_wrap)

        lay.addStretch()

        badge_wrap = QWidget()
        badge_lay = QVBoxLayout(badge_wrap)
        badge_lay.setContentsMargins(18, 0, 18, 0)

        self._sidebar_status = QLabel(t("sidebar.ready"))
        self._sidebar_status.setObjectName("statusBadge")
        self._sidebar_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._update_sidebar_badge("idle")
        badge_lay.addWidget(self._sidebar_status)

        lay.addWidget(badge_wrap)

        self._set_active_nav(0)
        return sidebar

    def _navigate_to(self, index: int):
        self._pages.setCurrentIndex(index)
        self._set_active_nav(index)

    def _set_active_nav(self, active: int):
        for i, btn in enumerate(self._nav_buttons):
            is_active = i == active
            btn.setProperty("active", "true" if is_active else "false")
            color = self._pal["nav_active_icon"] if is_active else self._pal["text_sec"]
            btn.setIcon(icons.icon(self._nav_icons[i], color, 18))
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _update_sidebar_badge(self, state: str):
        self._badge_state = state
        styles = {
            "idle": (self._c("accent_dim"), self._c("accent")),
            "active": (self._c("ok_dim"), self._c("ok")),
            "stopped": (self._c("gray_dim"), self._c("gray_fg")),
        }
        bg, fg = styles.get(state, styles["idle"])
        self._sidebar_status.setStyleSheet(
            f"background-color: {bg}; color: {fg};"
            " border-radius: 9px; padding: 9px 12px; font-size: 11px; font-weight: 600;"
        )

    # ── Page 1: Translation ──────────────────────────────────────

    def _build_translation_page(self) -> QWidget:
        page = QWidget()
        page.setObjectName("pageRoot")
        lay = QVBoxLayout(page)
        lay.setContentsMargins(30, 26, 30, 18)
        lay.setSpacing(18)

        header, self._tr_title, self._tr_sub, self._tr_pill = self._build_header(
            t("sidebar.translation"), t("page.translation_subtitle"), pill=True
        )
        self._style_pill(self._tr_pill, "idle")
        lay.addWidget(header)

        config_row = QHBoxLayout()
        config_row.setSpacing(16)

        # Language card
        lang_card, lang_lay = self._card()
        lang_title_row, self._lang_card_title = self._card_title_row("languages", t("page.lang_selection"), "accent")
        lang_lay.addLayout(lang_title_row)

        self._source_lang = QComboBox()
        self._target_lang = QComboBox()
        for code, info in SUPPORTED_LANGUAGES.items():
            self._source_lang.addItem(f"{info['name']} ({code})", code)
            self._target_lang.addItem(f"{info['name']} ({code})", code)
        self._restore_language_pair()

        self._swap_btn = QPushButton()
        self._swap_btn.setObjectName("swapBtn")
        self._swap_btn.setFixedSize(38, 38)
        self._reg_icon_button(self._swap_btn, "swap", "accent", 17)
        self._swap_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._swap_btn.setToolTip(t("tooltip.swap_langs"))
        self._swap_btn.clicked.connect(self._swap_languages)

        self._src_label = QLabel(t("label.source"))
        self._src_label.setProperty("class", "fieldLabel")
        self._tgt_label = QLabel(t("label.target"))
        self._tgt_label.setProperty("class", "fieldLabel")

        src_col = QVBoxLayout()
        src_col.setSpacing(5)
        src_col.addWidget(self._src_label)
        src_col.addWidget(self._source_lang)

        tgt_col = QVBoxLayout()
        tgt_col.setSpacing(5)
        tgt_col.addWidget(self._tgt_label)
        tgt_col.addWidget(self._target_lang)

        pair = QHBoxLayout()
        pair.setSpacing(10)
        pair.addLayout(src_col, 1)
        pair.addWidget(self._swap_btn, 0, Qt.AlignmentFlag.AlignBottom)
        pair.addLayout(tgt_col, 1)
        lang_lay.addLayout(pair)
        lang_lay.addStretch()
        config_row.addWidget(lang_card, 1)

        # Device card
        dev_card, dev_lay = self._card()
        dev_title_row, self._dev_card_title = self._card_title_row("mic", t("page.audio_devices"), "teal")
        dev_lay.addLayout(dev_title_row)

        self._mic_lbl = QLabel(t("label.microphone"))
        self._mic_lbl.setProperty("class", "fieldLabel")
        self._input_device = QComboBox()
        dev_lay.addWidget(self._mic_lbl)
        dev_lay.addWidget(self._input_device)

        self._out_lbl = QLabel(t("label.output"))
        self._out_lbl.setProperty("class", "fieldLabel")
        self._output_device = QComboBox()
        dev_lay.addWidget(self._out_lbl)
        dev_lay.addWidget(self._output_device)

        self._vb_status = QLabel()
        self._vb_status.setProperty("class", "cardHint")
        self._vb_status.setWordWrap(True)
        dev_lay.addWidget(self._vb_status)
        dev_lay.addStretch()
        config_row.addWidget(dev_card, 1)

        lay.addLayout(config_row)

        # Start / Stop
        self._start_btn = QPushButton(t("btn.start"))
        self._start_btn.setObjectName("startBtn")
        self._start_btn.setFixedHeight(52)
        self._start_btn.setIcon(icons.icon("play", self._pal["on_accent"], 18))
        self._start_btn.setIconSize(QSize(18, 18))
        self._start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._start_btn.clicked.connect(self._toggle_pipeline)
        lay.addWidget(self._start_btn)

        # Transcript
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        src_card, src_glay = self._card()
        src_glay.setContentsMargins(16, 14, 16, 16)
        src_title_row, self._src_card_title = self._card_title_row("waveform", t("transcript.source_title"), "accent")
        src_glay.addLayout(src_title_row)
        self._source_text = QTextEdit()
        self._source_text.setReadOnly(True)
        self._source_text.setPlaceholderText(t("transcript.source_placeholder"))
        src_glay.addWidget(self._source_text, 1)

        tgt_card, tgt_glay = self._card()
        tgt_glay.setContentsMargins(16, 14, 16, 16)
        tgt_title_row, self._tgt_card_title = self._card_title_row("languages", t("transcript.target_title"), "teal")
        tgt_glay.addLayout(tgt_title_row)
        self._target_text = QTextEdit()
        self._target_text.setReadOnly(True)
        self._target_text.setPlaceholderText(t("transcript.target_placeholder"))
        tgt_glay.addWidget(self._target_text, 1)

        splitter.addWidget(src_card)
        splitter.addWidget(tgt_card)
        splitter.setSizes([500, 500])
        lay.addWidget(splitter, 1)

        # Footer
        status_lay = QHBoxLayout()
        status_lay.setContentsMargins(4, 0, 4, 0)
        status_lay.setSpacing(10)
        self._status_label = QLabel(t("status.ready"))
        self._status_label.setProperty("class", "secondary")
        self._latency_label = QLabel(t("status.latency"))
        self._latency_label.setProperty("class", "verLabel")
        ver = QLabel(f"v{APP_VERSION}")
        ver.setProperty("class", "verLabel")

        status_lay.addWidget(self._status_label)
        status_lay.addStretch()
        status_lay.addWidget(self._latency_label)
        status_lay.addSpacing(12)
        status_lay.addWidget(ver)
        lay.addLayout(status_lay)

        return page

    def _restore_language_pair(self):
        """Restore saved source/target from config, else sensible defaults."""
        src = self._config.get("translation.source_language", "TR")
        tgt = self._config.get("translation.target_language", "RU")
        codes = list(SUPPORTED_LANGUAGES.keys())
        si = codes.index(src) if src in codes else 0
        ti = codes.index(tgt) if tgt in codes else (1 if len(codes) > 1 else 0)
        self._source_lang.setCurrentIndex(si)
        self._target_lang.setCurrentIndex(ti)

    # ── Page 2: Statistics ───────────────────────────────────────

    def _build_stats_page(self) -> QWidget:
        page = QWidget()
        page.setObjectName("pageRoot")
        lay = QVBoxLayout(page)
        lay.setContentsMargins(30, 26, 30, 18)
        lay.setSpacing(18)

        header, self._stats_title, self._stats_sub, _ = self._build_header(
            t("stats.title"), t("page.stats_subtitle")
        )
        lay.addWidget(header)

        cards = QHBoxLayout()
        cards.setSpacing(16)

        self._stat_session = self._make_stat_card("clock", t("stats.session_duration"), "00:00:00", "accent")
        self._stat_translations = self._make_stat_card("repeat", t("stats.translation_count"), "0", "ok")
        self._stat_characters = self._make_stat_card("type", t("stats.characters"), "0", "warn")
        self._stat_latency = self._make_stat_card("zap", t("stats.avg_latency"), "--", "teal")

        for card in [self._stat_session, self._stat_translations, self._stat_characters, self._stat_latency]:
            cards.addWidget(card["widget"])
        lay.addLayout(cards)

        self._deepl_group = QGroupBox(t("stats.deepl_usage"))
        dl_lay = QVBoxLayout(self._deepl_group)
        dl_lay.setContentsMargins(18, 14, 18, 16)
        dl_lay.setSpacing(10)

        self._deepl_usage_label = QLabel(t("stats.deepl_loading"))
        self._deepl_usage_label.setProperty("class", "secondary")
        dl_lay.addWidget(self._deepl_usage_label)

        self._deepl_progress = QProgressBar()
        self._deepl_progress.setRange(0, 100)
        self._deepl_progress.setValue(0)
        self._deepl_progress.setTextVisible(False)
        dl_lay.addWidget(self._deepl_progress)

        self._deepl_remaining = QLabel(t("stats.deepl_remaining"))
        self._deepl_remaining.setProperty("class", "verLabel")
        dl_lay.addWidget(self._deepl_remaining)

        lay.addWidget(self._deepl_group)

        self._tbl_group = QGroupBox(t("stats.recent_translations"))
        tbl_lay = QVBoxLayout(self._tbl_group)
        tbl_lay.setContentsMargins(14, 12, 14, 14)

        self._translations_table = QTableWidget()
        self._translations_table.setColumnCount(4)
        self._translations_table.setHorizontalHeaderLabels([
            t("stats.col_time"), t("stats.col_source"),
            t("stats.col_translation"), t("stats.col_latency"),
        ])
        hdr = self._translations_table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self._translations_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._translations_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._translations_table.verticalHeader().setVisible(False)
        self._translations_table.setAlternatingRowColors(True)
        self._translations_table.setShowGrid(False)
        tbl_lay.addWidget(self._translations_table)

        lay.addWidget(self._tbl_group, 1)

        self._stats.stats_updated.connect(self._refresh_stats_ui)
        return page

    def _make_stat_card(self, icon_name: str, label: str, value: str, color_key: str) -> dict:
        card = QFrame()
        card.setProperty("class", "card")
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(18, 16, 18, 16)
        card_lay.setSpacing(12)

        top = QHBoxLayout()
        top.setSpacing(10)
        ic = QLabel()
        ic.setFixedSize(36, 36)
        ic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dim_key = f"{color_key}_dim"
        ic.setStyleSheet(f"background-color: {self._pal[dim_key]}; border-radius: 10px;")
        self._reg_icon_label(ic, icon_name, color_key, 18)
        self._themed_chips.append((ic, dim_key))

        name = QLabel(label)
        name.setProperty("class", "statName")
        top.addWidget(ic, 0, Qt.AlignmentFlag.AlignVCenter)
        top.addWidget(name, 1, Qt.AlignmentFlag.AlignVCenter)

        val = QLabel(value)
        val.setProperty("class", "statValue")

        card_lay.addLayout(top)
        card_lay.addWidget(val)

        return {"widget": card, "value": val, "label": name}

    def _refresh_stats_ui(self):
        self._stat_session["value"].setText(self._stats.session_duration_str)
        self._stat_translations["value"].setText(str(self._stats.translation_count))
        self._stat_characters["value"].setText(self._stats.total_characters_str)
        self._stat_latency["value"].setText(self._stats.average_latency_str)

        if self._stats.deepl_usage is not None and self._stats.deepl_limit is not None:
            used = self._stats.deepl_usage
            limit = self._stats.deepl_limit
            remaining = limit - used
            pct = self._stats.deepl_usage_percent
            self._deepl_usage_label.setText(t("stats.deepl_used", used=used, limit=limit))
            self._deepl_progress.setValue(int(pct))
            self._deepl_remaining.setText(t("stats.deepl_remaining_value", remaining=remaining))

            if pct > 80:
                bar_color = self._c("err")
            elif pct > 60:
                bar_color = self._c("warn")
            else:
                bar_color = self._c("accent")
            self._deepl_progress.setStyleSheet(
                f"QProgressBar::chunk {{ background-color: {bar_color}; border-radius: 7px; }}"
            )

        records = self._stats.recent_translations
        self._translations_table.setRowCount(len(records))
        for row, rec in enumerate(records):
            ts = time.strftime("%H:%M:%S", time.localtime(rec.timestamp))
            self._translations_table.setItem(row, 0, QTableWidgetItem(ts))
            self._translations_table.setItem(row, 1, QTableWidgetItem(rec.source_text[:100]))
            self._translations_table.setItem(row, 2, QTableWidgetItem(rec.translated_text[:100]))
            self._translations_table.setItem(row, 3, QTableWidgetItem(f"{rec.latency_ms:.0f}ms"))

    # ── Page 3: Settings ─────────────────────────────────────────

    def _build_settings_page(self) -> QWidget:
        page = QWidget()
        page.setObjectName("pageRoot")
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        lay = QVBoxLayout(content)
        lay.setContentsMargins(30, 26, 30, 28)
        lay.setSpacing(18)

        header, self._settings_title, self._settings_sub, _ = self._build_header(
            t("settings.title"), t("page.settings_subtitle")
        )
        lay.addWidget(header)

        # ── Appearance (UI language + theme) ──
        self._appearance_group = QGroupBox(t("settings.appearance"))
        appearance_lay = QHBoxLayout(self._appearance_group)
        appearance_lay.setContentsMargins(18, 14, 18, 16)
        appearance_lay.setSpacing(18)

        lang_col = QVBoxLayout()
        lang_col.setSpacing(5)
        self._ui_lang_lbl = QLabel(t("settings.ui_language"))
        self._ui_lang_lbl.setProperty("class", "fieldLabel")
        self._ui_lang_combo = QComboBox()
        for code, display in available_languages().items():
            self._ui_lang_combo.addItem(display, code)
        cur = get_language()
        for i in range(self._ui_lang_combo.count()):
            if self._ui_lang_combo.itemData(i) == cur:
                self._ui_lang_combo.setCurrentIndex(i)
                break
        self._ui_lang_combo.currentIndexChanged.connect(self._on_ui_language_changed)
        lang_col.addWidget(self._ui_lang_lbl)
        lang_col.addWidget(self._ui_lang_combo)

        theme_col = QVBoxLayout()
        theme_col.setSpacing(5)
        self._theme_lbl = QLabel(t("settings.theme"))
        self._theme_lbl.setProperty("class", "fieldLabel")
        self._theme_combo = QComboBox()
        self._theme_combo.addItem(t("settings.theme_light"), "light")
        self._theme_combo.addItem(t("settings.theme_dark"), "dark")
        for i in range(self._theme_combo.count()):
            if self._theme_combo.itemData(i) == self._mode:
                self._theme_combo.setCurrentIndex(i)
                break
        self._theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        theme_col.addWidget(self._theme_lbl)
        theme_col.addWidget(self._theme_combo)

        appearance_lay.addLayout(lang_col, 1)
        appearance_lay.addLayout(theme_col, 1)
        lay.addWidget(self._appearance_group)

        # ── Translation Provider ──
        self._provider_group = QGroupBox(t("settings.translation_provider"))
        provider_lay = QVBoxLayout(self._provider_group)
        provider_lay.setContentsMargins(18, 14, 18, 16)
        provider_lay.setSpacing(8)

        self._provider_combo = QComboBox()
        self._provider_combo.addItem(t("settings.provider_deepl"), "deepl")
        self._provider_combo.addItem(t("settings.provider_google"), "google")
        saved_provider = self._config.get("translation.provider", "deepl")
        for i in range(self._provider_combo.count()):
            if self._provider_combo.itemData(i) == saved_provider:
                self._provider_combo.setCurrentIndex(i)
                break
        self._provider_combo.currentIndexChanged.connect(self._on_provider_changed)
        provider_lay.addWidget(self._provider_combo)

        self._provider_note = QLabel(t("settings.provider_note"))
        self._provider_note.setProperty("class", "note")
        self._provider_note.setWordWrap(True)
        provider_lay.addWidget(self._provider_note)

        lay.addWidget(self._provider_group)

        # ── API Keys ──
        self._api_group = QGroupBox(t("settings.api_keys"))
        api_lay = QVBoxLayout(self._api_group)
        api_lay.setContentsMargins(18, 14, 18, 18)
        api_lay.setSpacing(14)

        self._api_info = QLabel(t("settings.api_info"))
        self._api_info.setProperty("class", "settingInfo")
        self._api_info.setWordWrap(True)
        api_lay.addWidget(self._api_info)

        # Deepgram
        self._dg_title = QLabel(t("settings.deepgram_title"))
        self._dg_title.setProperty("class", "settingTitle")
        api_lay.addWidget(self._dg_title)
        self._dg_desc = QLabel(t("settings.deepgram_desc"))
        self._dg_desc.setProperty("class", "settingDesc")
        api_lay.addWidget(self._dg_desc)
        self._deepgram_key, self._dg_toggle = self._key_row("dg_xxxxxxxxxxxxxxxxxxxxxxxx", self._config.deepgram_api_key, api_lay)
        self._dg_link = self._link_button(t("settings.link_deepgram"), "https://console.deepgram.com/signup", api_lay)

        api_lay.addWidget(self._h_line())

        # DeepL
        self._dl_title = QLabel(t("settings.deepl_title"))
        self._dl_title.setProperty("class", "settingTitle")
        api_lay.addWidget(self._dl_title)
        self._dl_desc = QLabel(t("settings.deepl_desc"))
        self._dl_desc.setProperty("class", "settingDesc")
        api_lay.addWidget(self._dl_desc)
        self._deepl_key, self._dl_toggle = self._key_row("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:fx", self._config.deepl_api_key, api_lay)
        self._dl_link = self._link_button(t("settings.link_deepl"), "https://www.deepl.com/pro-api", api_lay)

        api_lay.addWidget(self._h_line())

        # Google
        self._gg_title = QLabel(t("settings.google_title"))
        self._gg_title.setProperty("class", "settingTitle")
        api_lay.addWidget(self._gg_title)
        self._gg_desc = QLabel(t("settings.google_desc"))
        self._gg_desc.setProperty("class", "settingDesc")
        api_lay.addWidget(self._gg_desc)
        self._google_key, self._gg_toggle = self._key_row("AIzaXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX", self._config.google_api_key, api_lay)
        self._gg_link = self._link_button(t("settings.link_google"), "https://console.cloud.google.com/apis/credentials", api_lay)

        api_lay.addWidget(self._h_line())

        # Azure
        self._az_title = QLabel(t("settings.azure_title"))
        self._az_title.setProperty("class", "settingTitle")
        api_lay.addWidget(self._az_title)
        self._az_desc = QLabel(t("settings.azure_desc"))
        self._az_desc.setProperty("class", "settingDesc")
        api_lay.addWidget(self._az_desc)
        self._azure_key, self._az_toggle = self._key_row("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", self._config.azure_speech_key, api_lay)
        self._az_link = self._link_button(t("settings.link_azure"), "https://azure.microsoft.com/en-us/products/ai-services/speech-service", api_lay)

        region_row = QHBoxLayout()
        region_row.setSpacing(10)
        self._region_lbl = QLabel(t("settings.region"))
        self._region_lbl.setFixedWidth(52)
        self._region_lbl.setProperty("class", "fieldLabel")
        self._azure_region = QLineEdit(self._config.azure_speech_region)
        self._azure_region.setPlaceholderText("westeurope")
        self._azure_region.setMaximumWidth(280)
        region_row.addWidget(self._region_lbl)
        region_row.addWidget(self._azure_region)
        region_row.addStretch()
        api_lay.addLayout(region_row)

        self._az_note = QLabel(t("settings.azure_note"))
        self._az_note.setProperty("class", "note")
        self._az_note.setWordWrap(True)
        api_lay.addWidget(self._az_note)

        api_lay.addWidget(self._h_line())

        # Test + Save row
        self._test_result = QLabel("")
        self._test_result.setProperty("class", "secondary")
        self._test_result.setWordWrap(True)
        self._test_result.setTextFormat(Qt.TextFormat.RichText)
        api_lay.addWidget(self._test_result)

        action_row = QHBoxLayout()
        self._test_btn = QPushButton(t("settings.test_keys"))
        self._test_btn.setFixedHeight(40)
        self._test_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._reg_icon_button(self._test_btn, "check", "accent", 16)
        self._test_btn.clicked.connect(self._test_keys)
        action_row.addWidget(self._test_btn)
        action_row.addStretch()

        self._save_btn = QPushButton(t("settings.save"))
        self._save_btn.setProperty("class", "accent-btn")
        self._save_btn.setFixedSize(130, 40)
        self._reg_icon_button(self._save_btn, "check", "on_accent", 16)
        self._save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._save_btn.clicked.connect(self._save_settings)
        action_row.addWidget(self._save_btn)
        api_lay.addLayout(action_row)

        lay.addWidget(self._api_group)

        # ── Audio Setup Guide ──
        self._guide_group = QGroupBox(t("settings.guide_title"))
        guide_lay = QVBoxLayout(self._guide_group)
        guide_lay.setContentsMargins(14, 12, 14, 14)

        self._guide_browser = QTextBrowser()
        self._guide_browser.setOpenExternalLinks(True)
        self._guide_browser.setMinimumHeight(300)
        self._guide_browser.setHtml(t("settings.guide_html"))
        guide_lay.addWidget(self._guide_browser)
        lay.addWidget(self._guide_group)

        # ── About ──
        self._about_group = QGroupBox(t("settings.about_title"))
        about_lay = QVBoxLayout(self._about_group)
        about_lay.setContentsMargins(18, 12, 18, 16)
        self._about_txt = QLabel(f"{APP_NAME} v{APP_VERSION}\n\n{t('settings.about_desc')}")
        self._about_txt.setProperty("class", "secondary")
        self._about_txt.setWordWrap(True)
        about_lay.addWidget(self._about_txt)
        lay.addWidget(self._about_group)

        lay.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)
        return page

    # ── Settings helpers ─────────────────────────────────────────

    def _key_row(self, placeholder: str, value: str, parent_lay) -> tuple:
        row = QHBoxLayout()
        row.setSpacing(8)
        field = QLineEdit(value)
        field.setEchoMode(QLineEdit.EchoMode.Password)
        field.setPlaceholderText(placeholder)
        row.addWidget(field, 1)
        toggle = QPushButton(t("settings.btn_show"))
        toggle.setProperty("class", "toggle-btn")
        toggle.setFixedSize(64, 38)
        toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        toggle.clicked.connect(lambda: self._toggle_visibility(field, toggle))
        row.addWidget(toggle)
        parent_lay.addLayout(row)
        return field, toggle

    def _link_button(self, text: str, url: str, parent_lay) -> QPushButton:
        btn = QPushButton(text)
        btn.setProperty("class", "link-btn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda: webbrowser.open(url))
        parent_lay.addWidget(btn)
        return btn

    def _h_line(self) -> QFrame:
        line = QFrame()
        line.setObjectName("hLine")
        line.setFixedHeight(1)
        return line

    def _toggle_visibility(self, field: QLineEdit, btn: QPushButton):
        if field.echoMode() == QLineEdit.EchoMode.Password:
            field.setEchoMode(QLineEdit.EchoMode.Normal)
            btn.setText(t("settings.btn_hide"))
        else:
            field.setEchoMode(QLineEdit.EchoMode.Password)
            btn.setText(t("settings.btn_show"))

    def _on_provider_changed(self, index: int):
        provider = self._provider_combo.itemData(index)
        if provider:
            self._config.set("translation.provider", provider)
            self._config.save()

    def _on_theme_changed(self, index: int):
        mode = self._theme_combo.itemData(index)
        if mode and mode != self._mode:
            self._apply_theme(mode)
            self._config.set("gui.theme", mode)
            self._config.save()

    # ── API key testing ──────────────────────────────────────────

    def _test_keys(self):
        asyncio.ensure_future(self._run_key_tests())

    async def _run_key_tests(self):
        loop = asyncio.get_event_loop()
        self._test_result.setText(t("settings.testing"))
        self._test_btn.setEnabled(False)
        try:
            dg = self._deepgram_key.text().strip()
            dl = self._deepl_key.text().strip()
            gg = self._google_key.text().strip()
            az = self._azure_key.text().strip()
            region = self._azure_region.text().strip() or "westeurope"

            results = {
                "Deepgram": await loop.run_in_executor(None, key_validator.validate_deepgram, dg),
                "DeepL": await loop.run_in_executor(None, key_validator.validate_deepl, dl),
                "Google": await loop.run_in_executor(None, key_validator.validate_google, gg),
                "Azure": await loop.run_in_executor(None, key_validator.validate_azure, az, region),
            }
            self._test_result.setText(self._format_test_results(results))
        finally:
            self._test_btn.setEnabled(True)

    def _format_test_results(self, results: dict) -> str:
        color = {
            "valid": self._c("ok"),
            "invalid": self._c("err"),
            "empty": self._c("text_muted"),
            "error": self._c("warn"),
        }
        mark = {"valid": "✓", "invalid": "✕", "empty": "–", "error": "!"}
        msg_key = {
            "valid": "settings.key_valid",
            "invalid": "settings.key_invalid",
            "empty": "settings.key_empty",
            "error": "settings.key_error",
        }
        lines = []
        for svc, st in results.items():
            txt = t(msg_key.get(st, "settings.key_error"), service=svc)
            lines.append(f'<span style="color:{color.get(st, color["error"])}">{mark.get(st, "?")} {txt}</span>')
        return "<br>".join(lines)

    # ================================================================
    #  i18n — RETRANSLATE UI
    # ================================================================

    def _on_ui_language_changed(self, index: int):
        code = self._ui_lang_combo.itemData(index)
        if code and code != get_language():
            set_language(code)
            self._config.set("gui.language", code)
            self._config.save()
            self._retranslate_ui()

    def _retranslate_ui(self):
        """Refresh every translatable text in the window."""
        self._nav_section.setText("  " + t("sidebar.section_main"))
        for i, key in enumerate(self._nav_keys):
            self._nav_buttons[i].setText("  " + t(key))

        self._sidebar_status.setText(t("sidebar.active") if self._running else t("sidebar.ready"))

        # Translation page
        self._tr_title.setText(t("sidebar.translation"))
        self._tr_sub.setText(t("page.translation_subtitle"))
        self._style_pill(self._tr_pill, "active" if self._running else self._pill_state)
        self._lang_card_title.setText(t("page.lang_selection"))
        self._src_label.setText(t("label.source"))
        self._tgt_label.setText(t("label.target"))
        self._swap_btn.setToolTip(t("tooltip.swap_langs"))
        self._dev_card_title.setText(t("page.audio_devices"))
        self._mic_lbl.setText(t("label.microphone"))
        self._out_lbl.setText(t("label.output"))

        if not self._running:
            self._start_btn.setText(t("btn.start"))
            self._status_label.setText(t("status.ready"))
            self._latency_label.setText(t("status.latency"))
        else:
            self._start_btn.setText(t("btn.stop"))

        self._src_card_title.setText(t("transcript.source_title"))
        self._tgt_card_title.setText(t("transcript.target_title"))
        self._source_text.setPlaceholderText(t("transcript.source_placeholder"))
        self._target_text.setPlaceholderText(t("transcript.target_placeholder"))

        # Stats page
        self._stats_title.setText(t("stats.title"))
        self._stats_sub.setText(t("page.stats_subtitle"))
        self._stat_session["label"].setText(t("stats.session_duration"))
        self._stat_translations["label"].setText(t("stats.translation_count"))
        self._stat_characters["label"].setText(t("stats.characters"))
        self._stat_latency["label"].setText(t("stats.avg_latency"))
        self._deepl_group.setTitle(t("stats.deepl_usage"))
        self._deepl_remaining.setText(t("stats.deepl_remaining"))
        self._tbl_group.setTitle(t("stats.recent_translations"))
        self._translations_table.setHorizontalHeaderLabels([
            t("stats.col_time"), t("stats.col_source"),
            t("stats.col_translation"), t("stats.col_latency"),
        ])

        # Settings page
        self._settings_title.setText(t("settings.title"))
        self._settings_sub.setText(t("page.settings_subtitle"))
        self._appearance_group.setTitle(t("settings.appearance"))
        self._ui_lang_lbl.setText(t("settings.ui_language"))
        self._theme_lbl.setText(t("settings.theme"))
        self._theme_combo.setItemText(0, t("settings.theme_light"))
        self._theme_combo.setItemText(1, t("settings.theme_dark"))
        self._api_group.setTitle(t("settings.api_keys"))
        self._api_info.setText(t("settings.api_info"))
        self._dg_title.setText(t("settings.deepgram_title"))
        self._dg_desc.setText(t("settings.deepgram_desc"))
        self._dl_title.setText(t("settings.deepl_title"))
        self._dl_desc.setText(t("settings.deepl_desc"))
        self._gg_title.setText(t("settings.google_title"))
        self._gg_desc.setText(t("settings.google_desc"))
        self._gg_link.setText(t("settings.link_google"))
        self._az_title.setText(t("settings.azure_title"))
        self._az_desc.setText(t("settings.azure_desc"))
        self._az_note.setText(t("settings.azure_note"))
        self._dg_link.setText(t("settings.link_deepgram"))
        self._dl_link.setText(t("settings.link_deepl"))
        self._az_link.setText(t("settings.link_azure"))
        self._region_lbl.setText(t("settings.region"))
        self._test_btn.setText(t("settings.test_keys"))
        self._save_btn.setText(t("settings.save"))
        self._provider_group.setTitle(t("settings.translation_provider"))
        self._provider_note.setText(t("settings.provider_note"))
        self._provider_combo.setItemText(0, t("settings.provider_deepl"))
        self._provider_combo.setItemText(1, t("settings.provider_google"))
        self._guide_group.setTitle(t("settings.guide_title"))
        self._guide_browser.setHtml(t("settings.guide_html"))
        self._about_group.setTitle(t("settings.about_title"))
        self._about_txt.setText(f"{APP_NAME} v{APP_VERSION}\n\n{t('settings.about_desc')}")

        self._dg_toggle.setText(t("settings.btn_show"))
        self._dl_toggle.setText(t("settings.btn_show"))
        self._gg_toggle.setText(t("settings.btn_show"))
        self._az_toggle.setText(t("settings.btn_show"))

        self._populate_devices()

        tray = getattr(self, "_system_tray", None)
        if tray and hasattr(tray, "retranslate_ui"):
            tray.retranslate_ui()

    # ================================================================
    #  SIGNALS
    # ================================================================

    def _connect_signals(self):
        self._signals.transcript_signal.connect(self._update_transcript)
        self._signals.translation_signal.connect(self._update_translation)
        self._signals.latency_signal.connect(self._update_latency)
        self._signals.status_signal.connect(self._update_status)
        self._signals.translation_complete_signal.connect(self._on_translation_complete)

    # ================================================================
    #  DEVICE POPULATION
    # ================================================================

    def _populate_devices(self):
        try:
            engine = AudioEngine()
            input_devs = engine.list_input_devices()
            output_devs = engine.list_output_devices()

            self._input_device.clear()
            real_mic_idx = 0
            for i, dev in enumerate(input_devs):
                name = dev["name"]
                is_cable = any(kw in name.lower() for kw in ["cable", "virtual", "vb-audio"])
                label = f"{t('device.virtual_prefix') if is_cable else ''}{name}"
                self._input_device.addItem(label, dev["id"])
                if not is_cable and "microphone" in name.lower() and real_mic_idx == 0:
                    real_mic_idx = i
            if self._input_device.count() > 0:
                self._input_device.setCurrentIndex(real_mic_idx)

            self._output_device.clear()
            cable_idx = -1
            for i, dev in enumerate(output_devs):
                name = dev["name"]
                is_cable = any(kw in name.lower() for kw in ["cable input", "vb-audio"])
                if is_cable:
                    label = f"{name} ({t('vbcable.for_app')})"
                    cable_idx = i
                else:
                    label = name
                self._output_device.addItem(label, dev["id"])

            if cable_idx >= 0:
                self._output_device.setCurrentIndex(cable_idx)
                self._vb_status.setText(t("vbcable.detected"))
                self._vb_state = True
            else:
                self._vb_status.setText(t("vbcable.not_found"))
                self._vb_state = False
            self._apply_vb_status_color()

        except Exception as e:
            self._status_label.setText(t("error.device_error", error=e))

    # ================================================================
    #  FIRST RUN
    # ================================================================

    def _check_first_run(self):
        if not self._config.has_required_keys:
            self._navigate_to(2)

    # ================================================================
    #  SETTINGS SAVE
    # ================================================================

    def _save_settings(self):
        dg = self._deepgram_key.text().strip()
        dl = self._deepl_key.text().strip()
        gg = self._google_key.text().strip()
        az = self._azure_key.text().strip()
        region = self._azure_region.text().strip() or "westeurope"
        provider = self._provider_combo.currentData() or "deepl"

        if not dg:
            QMessageBox.warning(self, t("settings.missing_field"), t("settings.dg_required"))
            return
        if provider == "deepl" and not dl:
            QMessageBox.warning(self, t("settings.missing_field"), t("settings.dl_required"))
            return
        if provider == "google" and not gg:
            QMessageBox.warning(self, t("settings.missing_field"), t("settings.google_required"))
            return

        self._config.save_api_keys(dg, dl, az, region, gg)
        self._navigate_to(0)
        self._status_label.setText(t("settings.saved_ok"))
        self._status_label.setStyleSheet(f"color: {self._c('ok')}; font-size: 12px; font-weight: 600;")
        self._populate_devices()

    # ================================================================
    #  LANGUAGE
    # ================================================================

    def _swap_languages(self):
        s, tg = self._source_lang.currentIndex(), self._target_lang.currentIndex()
        self._source_lang.setCurrentIndex(tg)
        self._target_lang.setCurrentIndex(s)

    # ================================================================
    #  PIPELINE
    # ================================================================

    def _toggle_pipeline(self):
        if self._running:
            asyncio.ensure_future(self._stop_pipeline())
        else:
            asyncio.ensure_future(self._start_pipeline())

    async def _start_pipeline(self):
        provider = self._config.get("translation.provider", "deepl")

        if not self._config.deepgram_api_key:
            self._navigate_to(2)
            self._status_label.setText(t("status.enter_keys"))
            self._status_label.setStyleSheet(f"color: {self._c('warn')}; font-size: 12px;")
            return
        if provider == "google" and not self._config.google_api_key:
            self._navigate_to(2)
            self._status_label.setText(t("status.enter_keys"))
            self._status_label.setStyleSheet(f"color: {self._c('warn')}; font-size: 12px;")
            return
        if provider == "deepl" and not self._config.deepl_api_key:
            self._navigate_to(2)
            self._status_label.setText(t("status.enter_keys"))
            self._status_label.setStyleSheet(f"color: {self._c('warn')}; font-size: 12px;")
            return

        source = self._source_lang.currentData()
        target = self._target_lang.currentData()
        input_dev = self._input_device.currentData()
        output_dev = self._output_device.currentData()

        # Persist chosen language pair
        self._config.set("translation.source_language", source)
        self._config.set("translation.target_language", target)
        self._config.save()

        audio_engine = AudioEngine(
            sample_rate=self._config.get("audio.sample_rate", 16000),
            channels=self._config.get("audio.channels", 1),
            buffer_ms=self._config.get("audio.buffer_ms", 100),
        )

        stt = DeepgramSTT(
            api_key=self._config.deepgram_api_key,
            model=self._config.get("stt.deepgram.model", "nova-2"),
            sample_rate=self._config.get("audio.sample_rate", 16000),
            interim_results=self._config.get("stt.deepgram.interim_results", True),
            endpointing=self._config.get("stt.deepgram.endpointing", 300),
            punctuate=self._config.get("stt.deepgram.punctuate", True),
        )

        if provider == "google":
            translator = GoogleTranslator(
                api_key=self._config.google_api_key,
                cache_size=self._config.get("translation.cache_size", 1000),
            )
        else:
            translator = DeepLTranslator(
                api_key=self._config.deepl_api_key,
                formality=self._config.get("translation.formality", "default"),
                cache_size=self._config.get("translation.cache_size", 1000),
            )

        tts_manager = TTSProviderManager()
        deepgram_tts = DeepgramTTS(
            api_key=self._config.deepgram_api_key,
            model=self._config.get("tts.deepgram.model", "aura-asteria-en"),
        )
        tts_manager.add_provider(deepgram_tts)

        if self._config.azure_speech_key:
            azure_tts = AzureTTS(
                speech_key=self._config.azure_speech_key,
                region=self._config.azure_speech_region,
            )
            tts_manager.add_provider(azure_tts)

        self._event_bus = EventBus()
        self._event_bus.on("transcript", self._on_transcript_event)
        self._event_bus.on("translation", self._on_translation_event)
        self._event_bus.on("latency", self._on_latency_event)
        self._event_bus.on("translation_complete", self._on_translation_complete_event)

        self._pipeline = TranslationPipeline(
            audio_engine=audio_engine,
            stt=stt,
            translator=translator,
            tts_manager=tts_manager,
            event_bus=self._event_bus,
        )
        self._pipeline.set_languages(source, target)

        try:
            await self._pipeline.start_outgoing(input_dev, output_dev)
            self._running = True

            self._start_btn.setText(t("btn.stop"))
            self._start_btn.setIcon(icons.icon("stop", self._pal["on_accent"], 18))
            self._start_btn.setProperty("running", "true")
            self._start_btn.style().unpolish(self._start_btn)
            self._start_btn.style().polish(self._start_btn)

            src_name = SUPPORTED_LANGUAGES.get(source, {}).get("name", source)
            tgt_name = SUPPORTED_LANGUAGES.get(target, {}).get("name", target)
            self._status_label.setText(t("status.active", src=src_name, tgt=tgt_name))
            self._status_label.setStyleSheet(f"color: {self._c('ok')}; font-size: 12px; font-weight: 600;")

            self._sidebar_status.setText(t("sidebar.active"))
            self._update_sidebar_badge("active")
            self._style_pill(self._tr_pill, "active")

            self._source_lang.setEnabled(False)
            self._target_lang.setEnabled(False)
            self._input_device.setEnabled(False)
            self._output_device.setEnabled(False)

            self._stats.start_session()
            if provider == "deepl":
                asyncio.ensure_future(self._fetch_deepl_usage())

        except Exception as e:
            QMessageBox.critical(self, "Error", t("error.pipeline_failed", error=e))

    async def _stop_pipeline(self):
        if self._pipeline:
            await self._pipeline.stop()
            self._pipeline = None

        self._running = False

        self._start_btn.setText(t("btn.start"))
        self._start_btn.setIcon(icons.icon("play", self._pal["on_accent"], 18))
        self._start_btn.setProperty("running", "false")
        self._start_btn.style().unpolish(self._start_btn)
        self._start_btn.style().polish(self._start_btn)

        self._status_label.setText(t("status.stopped"))
        self._status_label.setStyleSheet(f"color: {self._c('text_sec')}; font-size: 12px;")
        self._latency_label.setText(t("status.latency"))
        self._latency_label.setStyleSheet(f"color: {self._c('text_muted')}; font-size: 12px;")

        self._sidebar_status.setText(t("sidebar.stopped"))
        self._update_sidebar_badge("stopped")
        self._style_pill(self._tr_pill, "stopped")

        self._source_lang.setEnabled(True)
        self._target_lang.setEnabled(True)
        self._input_device.setEnabled(True)
        self._output_device.setEnabled(True)

        self._stats.stop_session()

    # ================================================================
    #  DEEPL USAGE
    # ================================================================

    async def _fetch_deepl_usage(self):
        try:
            import deepl
            translator = deepl.Translator(self._config.deepl_api_key)
            usage = translator.get_usage()
            if usage.character and usage.character.limit:
                self._stats.set_deepl_usage(usage.character.count, usage.character.limit)
        except Exception:
            pass

    # ================================================================
    #  EVENT HANDLERS (async -> signal bridge)
    # ================================================================

    async def _on_transcript_event(self, text: str, is_final: bool, lang: str):
        self._signals.transcript_signal.emit(text, is_final, lang)

    async def _on_translation_event(self, text: str, lang: str):
        self._signals.translation_signal.emit(text, lang)

    async def _on_latency_event(self, ms: float):
        self._signals.latency_signal.emit(ms)

    async def _on_translation_complete_event(self, source: str, translated: str, latency_ms: float):
        self._signals.translation_complete_signal.emit(source, translated, latency_ms)

    # ================================================================
    #  UI UPDATES (main thread via signals)
    # ================================================================

    def _update_transcript(self, text: str, is_final: bool, lang: str):
        if is_final:
            self._source_text.append(text)
        else:
            self._status_label.setText(t("status.listening", text=text[:60]))
            self._status_label.setStyleSheet(f"color: {self._c('text_sec')}; font-size: 12px;")

    def _update_translation(self, text: str, lang: str):
        self._target_text.append(text)

    def _update_latency(self, ms: float):
        if ms < 800:
            color = self._c("ok")
        elif ms < 1500:
            color = self._c("warn")
        else:
            color = self._c("err")
        self._latency_label.setText(t("status.latency_value", ms=ms))
        self._latency_label.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: 600;")

    def _update_status(self, text: str):
        self._status_label.setText(text)

    def _on_translation_complete(self, source: str, translated: str, latency_ms: float):
        self._stats.record_translation(source, translated, latency_ms)

    # ================================================================
    #  CLOSE
    # ================================================================

    def closeEvent(self, event):
        if self._running:
            asyncio.ensure_future(self._stop_pipeline())
        event.accept()
