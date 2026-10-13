"""Lightweight i18n module — key-value translations for TR / EN / RU."""

from __future__ import annotations

_current_language: str = "tr"

LANGUAGES = {
    "tr": "Turkce",
    "en": "English",
    "ru": "Русский",
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ── Sidebar ───────────────────────────────────────────────────
    "sidebar.translation": {
        "tr": "Ceviri",
        "en": "Translation",
        "ru": "Перевод",
    },
    "sidebar.statistics": {
        "tr": "Istatistikler",
        "en": "Statistics",
        "ru": "Статистика",
    },
    "sidebar.settings": {
        "tr": "Ayarlar",
        "en": "Settings",
        "ru": "Настройки",
    },
    "sidebar.ready": {
        "tr": "Hazir",
        "en": "Ready",
        "ru": "Готов",
    },
    "sidebar.active": {
        "tr": "Aktif",
        "en": "Active",
        "ru": "Активен",
    },
    "sidebar.stopped": {
        "tr": "Durduruldu",
        "en": "Stopped",
        "ru": "Остановлен",
    },
    "sidebar.section_main": {
        "tr": "MENU",
        "en": "MENU",
        "ru": "МЕНЮ",
    },

    # ── Page headers (subtitles) ──────────────────────────────────
    "page.translation_subtitle": {
        "tr": "Canli ses cevirisini baslatin ve transkripti izleyin",
        "en": "Start live voice translation and watch the transcript",
        "ru": "Запустите живой перевод речи и следите за транскриптом",
    },
    "page.stats_subtitle": {
        "tr": "Bu oturumdaki ceviri performansi ve kullanim",
        "en": "Translation performance and usage for this session",
        "ru": "Производительность перевода и использование за эту сессию",
    },
    "page.settings_subtitle": {
        "tr": "Servis saglayicilari, API anahtarlari ve tercihler",
        "en": "Service providers, API keys and preferences",
        "ru": "Поставщики услуг, API-ключи и настройки",
    },

    # ── Translation page ──────────────────────────────────────────
    "page.lang_selection": {
        "tr": "Dil Secimi",
        "en": "Language Selection",
        "ru": "Выбор языка",
    },
    "page.audio_devices": {
        "tr": "Ses Cihazlari",
        "en": "Audio Devices",
        "ru": "Аудиоустройства",
    },
    "label.source": {
        "tr": "Kaynak",
        "en": "Source",
        "ru": "Источник",
    },
    "label.target": {
        "tr": "Hedef",
        "en": "Target",
        "ru": "Цель",
    },
    "label.microphone": {
        "tr": "Mikrofon",
        "en": "Microphone",
        "ru": "Микрофон",
    },
    "label.output": {
        "tr": "Ceviri Cikisi",
        "en": "Translation Output",
        "ru": "Выход перевода",
    },
    "tooltip.swap_langs": {
        "tr": "Dilleri degistir",
        "en": "Swap languages",
        "ru": "Поменять языки",
    },

    # Buttons
    "btn.start": {
        "tr": "CEVIRIYI BASLAT",
        "en": "START TRANSLATION",
        "ru": "НАЧАТЬ ПЕРЕВОД",
    },
    "btn.stop": {
        "tr": "CEVIRIYI DURDUR",
        "en": "STOP TRANSLATION",
        "ru": "ОСТАНОВИТЬ ПЕРЕВОД",
    },

    # Status
    "status.ready": {
        "tr": "Hazir",
        "en": "Ready",
        "ru": "Готов",
    },
    "status.listening": {
        "tr": "Dinleniyor: {text}...",
        "en": "Listening: {text}...",
        "ru": "Слушаю: {text}...",
    },
    "status.active": {
        "tr": "Aktif: {src} \u2192 {tgt}",
        "en": "Active: {src} \u2192 {tgt}",
        "ru": "Активен: {src} \u2192 {tgt}",
    },
    "status.stopped": {
        "tr": "Durduruldu",
        "en": "Stopped",
        "ru": "Остановлен",
    },
    "status.latency": {
        "tr": "Gecikme: --",
        "en": "Latency: --",
        "ru": "Задержка: --",
    },
    "status.latency_value": {
        "tr": "Gecikme: {ms:.0f}ms",
        "en": "Latency: {ms:.0f}ms",
        "ru": "Задержка: {ms:.0f}мс",
    },

    # Transcript panels
    "transcript.source_title": {
        "tr": "Konusman (STT)",
        "en": "Speech (STT)",
        "ru": "Речь (STT)",
    },
    "transcript.target_title": {
        "tr": "Ceviri Cikisi",
        "en": "Translation Output",
        "ru": "Выход перевода",
    },
    "transcript.source_placeholder": {
        "tr": "Konusmaya basladiginizda metin burada gorunecek...",
        "en": "Text will appear here when you start speaking...",
        "ru": "Текст появится здесь, когда вы начнете говорить...",
    },
    "transcript.target_placeholder": {
        "tr": "Cevrilen metin burada gorunecek...",
        "en": "Translated text will appear here...",
        "ru": "Переведенный текст появится здесь...",
    },

    # ── Stats page ────────────────────────────────────────────────
    "stats.title": {
        "tr": "Oturum Istatistikleri",
        "en": "Session Statistics",
        "ru": "Статистика сессии",
    },
    "stats.session_duration": {
        "tr": "Oturum Suresi",
        "en": "Session Duration",
        "ru": "Длительность сессии",
    },
    "stats.translation_count": {
        "tr": "Ceviri Sayisi",
        "en": "Translations",
        "ru": "Переводы",
    },
    "stats.characters": {
        "tr": "Karakter",
        "en": "Characters",
        "ru": "Символы",
    },
    "stats.avg_latency": {
        "tr": "Ort. Gecikme",
        "en": "Avg. Latency",
        "ru": "Ср. задержка",
    },
    "stats.deepl_usage": {
        "tr": "DeepL API Kullanimi",
        "en": "DeepL API Usage",
        "ru": "Использование DeepL API",
    },
    "stats.deepl_loading": {
        "tr": "Ceviri baslatildiginda yuklenir...",
        "en": "Loads when translation starts...",
        "ru": "Загружается при начале перевода...",
    },
    "stats.deepl_remaining": {
        "tr": "Kalan: --",
        "en": "Remaining: --",
        "ru": "Остаток: --",
    },
    "stats.deepl_used": {
        "tr": "Kullanilan: {used:,} / {limit:,} karakter",
        "en": "Used: {used:,} / {limit:,} characters",
        "ru": "Использовано: {used:,} / {limit:,} символов",
    },
    "stats.deepl_remaining_value": {
        "tr": "Kalan: {remaining:,} karakter",
        "en": "Remaining: {remaining:,} characters",
        "ru": "Остаток: {remaining:,} символов",
    },
    "stats.recent_translations": {
        "tr": "Son Ceviriler",
        "en": "Recent Translations",
        "ru": "Последние переводы",
    },
    "stats.col_time": {
        "tr": "Zaman",
        "en": "Time",
        "ru": "Время",
    },
    "stats.col_source": {
        "tr": "Kaynak Metin",
        "en": "Source Text",
        "ru": "Исходный текст",
    },
    "stats.col_translation": {
        "tr": "Ceviri",
        "en": "Translation",
        "ru": "Перевод",
    },
    "stats.col_latency": {
        "tr": "Gecikme",
        "en": "Latency",
        "ru": "Задержка",
    },

    # ── Settings page ─────────────────────────────────────────────
    "settings.title": {
        "tr": "Ayarlar",
        "en": "Settings",
        "ru": "Настройки",
    },
    "settings.api_keys": {
        "tr": "API Anahtarlari",
        "en": "API Keys",
        "ru": "API-ключи",
    },
    "settings.api_info": {
        "tr": "API key'lerinizi asagiya girin. Bilgiler yerel .env dosyasina kaydedilir.",
        "en": "Enter your API keys below. They are stored locally in a .env file.",
        "ru": "Введите ваши API-ключи ниже. Они хранятся локально в файле .env.",
    },
    "settings.save": {
        "tr": "Kaydet",
        "en": "Save",
        "ru": "Сохранить",
    },
    "settings.deepgram_title": {
        "tr": "Deepgram",
        "en": "Deepgram",
        "ru": "Deepgram",
    },
    "settings.deepgram_desc": {
        "tr": "Zorunlu \u2014 Ses tanima (STT) ve metin-ses (TTS)",
        "en": "Required \u2014 Speech-to-text (STT) and text-to-speech (TTS)",
        "ru": "Обязательно \u2014 Распознавание речи (STT) и синтез речи (TTS)",
    },
    "settings.deepl_title": {
        "tr": "DeepL",
        "en": "DeepL",
        "ru": "DeepL",
    },
    "settings.deepl_desc": {
        "tr": "Zorunlu \u2014 Metin cevirisi (ayda 500K karakter ucretsiz)",
        "en": "Required \u2014 Text translation (500K chars/month free)",
        "ru": "Обязательно \u2014 Перевод текста (500 тыс. символов/мес. бесплатно)",
    },
    "settings.azure_title": {
        "tr": "Azure Speech",
        "en": "Azure Speech",
        "ru": "Azure Speech",
    },
    "settings.azure_desc": {
        "tr": "Opsiyonel \u2014 Turkce ve Rusca metin-ses (TTS) icin gerekli",
        "en": "Optional \u2014 Required for Turkish and Russian text-to-speech (TTS)",
        "ru": "Необязательно \u2014 Требуется для турецкого и русского TTS",
    },
    "settings.azure_note": {
        "tr": "Not: Azure olmadan da uygulama calisir. Turkce/Rusca TTS icin onerilen.",
        "en": "Note: The app works without Azure. Recommended for Turkish/Russian TTS.",
        "ru": "Примечание: Приложение работает без Azure. Рекомендуется для турецкого/русского TTS.",
    },
    "settings.link_deepgram": {
        "tr": "Ucretsiz Deepgram key al",
        "en": "Get free Deepgram key",
        "ru": "Получить бесплатный ключ Deepgram",
    },
    "settings.link_deepl": {
        "tr": "Ucretsiz DeepL key al",
        "en": "Get free DeepL key",
        "ru": "Получить бесплатный ключ DeepL",
    },
    "settings.link_azure": {
        "tr": "Azure ucretsiz hesap olustur",
        "en": "Create free Azure account",
        "ru": "Создать бесплатный аккаунт Azure",
    },
    "settings.btn_show": {
        "tr": "Goster",
        "en": "Show",
        "ru": "Показать",
    },
    "settings.btn_hide": {
        "tr": "Gizle",
        "en": "Hide",
        "ru": "Скрыть",
    },
    "settings.region": {
        "tr": "Region",
        "en": "Region",
        "ru": "Регион",
    },
    "settings.guide_title": {
        "tr": "Ses Kurulum Rehberi",
        "en": "Audio Setup Guide",
        "ru": "Руководство по настройке звука",
    },
    "settings.guide_html": {
        "tr": """
        <style>
            body { color: #e7eaf2; font-size: 13px; line-height: 1.6; }
            h2 { color: #6f96ff; margin-bottom: 8px; }
            h3 { color: #4f7cff; margin-top: 18px; margin-bottom: 6px; }
            a { color: #6f96ff; }
            pre {
                background: #0a0d14; color: #e7eaf2;
                padding: 14px; border-radius: 8px;
                border: 1px solid #242b3a;
                font-family: "Cascadia Code", "Consolas", monospace;
                font-size: 12px;
            }
            ol, ul { padding-left: 20px; }
            li { margin-bottom: 6px; }
            b { color: #e7eaf2; }
        </style>
        <h2>Ses Ayarlari Rehberi</h2>

        <h3>Hizli Kurulum</h3>
        <ol>
            <li><b>Mikrofon:</b> Gercek mikrofonunu sec</li>
            <li><b>Ceviri Cikisi:</b> VB-Cable Input'u sec</li>
            <li><b>Zoom / Telegram:</b> Mikrofon olarak "CABLE Output (VB-Audio)" sec</li>
        </ol>

        <h3>Ses Akisi Semasi</h3>
        <pre>
  Sen konusursun
       |
  [Mikrofon] --> Uygulama dinler
       |
  [Deepgram STT] --> Metin olusturur
       |
  [DeepL] --> Hedef dile cevirir
       |
  [TTS] --> Ses sentezi
       |
  [VB-Cable] --> Zoom / Telegram'a iletir
       |
  Karsi taraf duyar
        </pre>

        <h3>VB-Cable Nedir?</h3>
        <p>Bilgisayarinda sanal bir ses kablosu olusturur. Cevrilen sesi
        Zoom veya Telegram'a "mikrofon" olarak iletir.</p>
        <p><a href="https://vb-audio.com/Cable/">vb-audio.com/Cable</a> adresinden
        ucretsiz indirebilirsiniz. Kurulumdan sonra bilgisayari yeniden baslatin.</p>
        """,
        "en": """
        <style>
            body { color: #e7eaf2; font-size: 13px; line-height: 1.6; }
            h2 { color: #6f96ff; margin-bottom: 8px; }
            h3 { color: #4f7cff; margin-top: 18px; margin-bottom: 6px; }
            a { color: #6f96ff; }
            pre {
                background: #0a0d14; color: #e7eaf2;
                padding: 14px; border-radius: 8px;
                border: 1px solid #242b3a;
                font-family: "Cascadia Code", "Consolas", monospace;
                font-size: 12px;
            }
            ol, ul { padding-left: 20px; }
            li { margin-bottom: 6px; }
            b { color: #e7eaf2; }
        </style>
        <h2>Audio Setup Guide</h2>

        <h3>Quick Setup</h3>
        <ol>
            <li><b>Microphone:</b> Select your real microphone</li>
            <li><b>Translation Output:</b> Select VB-Cable Input</li>
            <li><b>Zoom / Telegram:</b> Select "CABLE Output (VB-Audio)" as microphone</li>
        </ol>

        <h3>Audio Flow Diagram</h3>
        <pre>
  You speak
       |
  [Microphone] --> App listens
       |
  [Deepgram STT] --> Generates text
       |
  [DeepL] --> Translates to target language
       |
  [TTS] --> Speech synthesis
       |
  [VB-Cable] --> Sends to Zoom / Telegram
       |
  Other person hears
        </pre>

        <h3>What is VB-Cable?</h3>
        <p>Creates a virtual audio cable on your computer. It sends the translated
        audio to Zoom or Telegram as a "microphone".</p>
        <p>Download for free from <a href="https://vb-audio.com/Cable/">vb-audio.com/Cable</a>.
        Restart your computer after installation.</p>
        """,
        "ru": """
        <style>
            body { color: #e7eaf2; font-size: 13px; line-height: 1.6; }
            h2 { color: #6f96ff; margin-bottom: 8px; }
            h3 { color: #4f7cff; margin-top: 18px; margin-bottom: 6px; }
            a { color: #6f96ff; }
            pre {
                background: #0a0d14; color: #e7eaf2;
                padding: 14px; border-radius: 8px;
                border: 1px solid #242b3a;
                font-family: "Cascadia Code", "Consolas", monospace;
                font-size: 12px;
            }
            ol, ul { padding-left: 20px; }
            li { margin-bottom: 6px; }
            b { color: #e7eaf2; }
        </style>
        <h2>Руководство по настройке звука</h2>

        <h3>Быстрая настройка</h3>
        <ol>
            <li><b>Микрофон:</b> Выберите ваш настоящий микрофон</li>
            <li><b>Выход перевода:</b> Выберите VB-Cable Input</li>
            <li><b>Zoom / Telegram:</b> Выберите "CABLE Output (VB-Audio)" как микрофон</li>
        </ol>

        <h3>Схема аудиопотока</h3>
        <pre>
  Вы говорите
       |
  [Микрофон] --> Приложение слушает
       |
  [Deepgram STT] --> Создает текст
       |
  [DeepL] --> Переводит на целевой язык
       |
  [TTS] --> Синтез речи
       |
  [VB-Cable] --> Передает в Zoom / Telegram
       |
  Собеседник слышит
        </pre>

        <h3>Что такое VB-Cable?</h3>
        <p>Создает виртуальный аудиокабель на вашем компьютере. Передает переведенный
        звук в Zoom или Telegram как "микрофон".</p>
        <p>Скачайте бесплатно с <a href="https://vb-audio.com/Cable/">vb-audio.com/Cable</a>.
        После установки перезагрузите компьютер.</p>
        """,
    },
    "settings.about_title": {
        "tr": "Hakkinda",
        "en": "About",
        "ru": "О программе",
    },
    "settings.about_desc": {
        "tr": "Gercek zamanli ses ceviri uygulamasi.\nDeepgram STT + DeepL Ceviri + Azure/Deepgram TTS",
        "en": "Real-time voice translation application.\nDeepgram STT + DeepL Translation + Azure/Deepgram TTS",
        "ru": "Приложение для перевода речи в реальном времени.\nDeepgram STT + DeepL Перевод + Azure/Deepgram TTS",
    },
    "settings.ui_language": {
        "tr": "Arayuz Dili",
        "en": "Interface Language",
        "ru": "Язык интерфейса",
    },
    "settings.missing_field": {
        "tr": "Eksik Alan",
        "en": "Missing Field",
        "ru": "Отсутствует поле",
    },
    "settings.dg_required": {
        "tr": "Deepgram API Key zorunludur!",
        "en": "Deepgram API Key is required!",
        "ru": "Ключ Deepgram API обязателен!",
    },
    "settings.dl_required": {
        "tr": "DeepL API Key zorunludur!",
        "en": "DeepL API Key is required!",
        "ru": "Ключ DeepL API обязателен!",
    },
    "settings.saved_ok": {
        "tr": "API key'ler basariyla kaydedildi",
        "en": "API keys saved successfully",
        "ru": "API-ключи успешно сохранены",
    },

    # ── Translation provider ──────────────────────────────────────
    "settings.translation_provider": {
        "tr": "Ceviri Servisi",
        "en": "Translation Service",
        "ru": "Сервис перевода",
    },
    "settings.provider_deepl": {
        "tr": "DeepL",
        "en": "DeepL",
        "ru": "DeepL",
    },
    "settings.provider_google": {
        "tr": "Google Cloud Translation",
        "en": "Google Cloud Translation",
        "ru": "Google Cloud Translation",
    },
    "settings.google_title": {
        "tr": "Google Cloud Translation",
        "en": "Google Cloud Translation",
        "ru": "Google Cloud Translation",
    },
    "settings.google_desc": {
        "tr": "Opsiyonel \u2014 Google Cloud Translation API key",
        "en": "Optional \u2014 Google Cloud Translation API key",
        "ru": "Необязательно \u2014 Ключ Google Cloud Translation API",
    },
    "settings.link_google": {
        "tr": "Google Cloud Console'a git",
        "en": "Go to Google Cloud Console",
        "ru": "Перейти в Google Cloud Console",
    },
    "settings.google_required": {
        "tr": "Google API key veya DeepL API key gerekli!",
        "en": "Google API key or DeepL API key is required!",
        "ru": "Требуется ключ Google API или DeepL API!",
    },
    "settings.provider_note": {
        "tr": "Secilen servise gore API key zorunludur.",
        "en": "API key is required for the selected service.",
        "ru": "Ключ API обязателен для выбранного сервиса.",
    },

    # ── VB-Cable / devices ────────────────────────────────────────
    "vbcable.detected": {
        "tr": "VB-Cable algilandi ve secildi",
        "en": "VB-Cable detected and selected",
        "ru": "VB-Cable обнаружен и выбран",
    },
    "vbcable.not_found": {
        "tr": "VB-Cable bulunamadi \u2014 Ayarlar > Ses Kurulum Rehberi'ne bakin",
        "en": "VB-Cable not found \u2014 See Settings > Audio Setup Guide",
        "ru": "VB-Cable не найден \u2014 См. Настройки > Руководство по настройке звука",
    },
    "vbcable.for_app": {
        "tr": "Zoom/Telegram icin",
        "en": "For Zoom/Telegram",
        "ru": "Для Zoom/Telegram",
    },
    "device.virtual_prefix": {
        "tr": "[SANAL] ",
        "en": "[VIRTUAL] ",
        "ru": "[ВИРТУАЛЬНЫЙ] ",
    },

    # ── Errors / misc ─────────────────────────────────────────────
    "error.pipeline_failed": {
        "tr": "Pipeline baslatilamadi:\n{error}",
        "en": "Pipeline failed to start:\n{error}",
        "ru": "Не удалось запустить конвейер:\n{error}",
    },
    "error.device_error": {
        "tr": "Cihaz hatasi: {error}",
        "en": "Device error: {error}",
        "ru": "Ошибка устройства: {error}",
    },
    "status.enter_keys": {
        "tr": "Lutfen once API key'lerinizi girin",
        "en": "Please enter your API keys first",
        "ru": "Сначала введите ваши API-ключи",
    },

    # ── System tray ───────────────────────────────────────────────
    "tray.show": {
        "tr": "Pencereyi Goster",
        "en": "Show Window",
        "ru": "Показать окно",
    },
    "tray.start": {
        "tr": "Ceviriyi Baslat",
        "en": "Start Translation",
        "ru": "Начать перевод",
    },
    "tray.stop": {
        "tr": "Ceviriyi Durdur",
        "en": "Stop Translation",
        "ru": "Остановить перевод",
    },
    "tray.quit": {
        "tr": "Cikis",
        "en": "Quit",
        "ru": "Выход",
    },
}


def set_language(code: str) -> None:
    """Set the active UI language (e.g. 'tr', 'en', 'ru')."""
    global _current_language
    if code in LANGUAGES:
        _current_language = code


def get_language() -> str:
    """Return the current UI language code."""
    return _current_language


def available_languages() -> dict[str, str]:
    """Return ``{code: display_name}`` for every supported language."""
    return dict(LANGUAGES)


def t(key: str, **kwargs) -> str:
    """Look up *key* in the active language and optionally format it.

    Falls back to Turkish, then returns the key itself if nothing is found.
    """
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key

    text = entry.get(_current_language) or entry.get("tr", key)

    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass

    return text
