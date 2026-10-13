# RealTime Translator

Gercek zamanli ses ceviri uygulamasi. Deepgram STT + DeepL/Google Translation + Azure/Deepgram TTS.

## Teknoloji Stack
- **Dil:** Python 3.11+
- **GUI:** PyQt6 + qasync (async event loop)
- **STT:** Deepgram Nova-2 (WebSocket streaming)
- **Ceviri:** DeepL API veya Google Cloud Translation v2 (provider secimli)
- **TTS:** Deepgram Aura (primary) + Azure Speech (fallback, TR/RU icin)
- **Config:** YAML (`config.yaml`) + `.env` (API key'ler)
- **Dependency yonetimi:** pip (requirements.txt)

## Proje Yapisi
```
main.py                          # Giris noktasi
config.yaml                      # Uygulama ayarlari (provider, dil, ses, gui)
.env                             # API key'ler (gitignore'da)
RealTimeTranslator.spec          # PyInstaller build spec (onedir, windowed)
installer.iss                    # Inno Setup kurulum sihirbazi script'i
build.ps1                        # Tek komutla build (PyInstaller + Inno Setup)
BUILD.md                         # Build & installer rehberi
tools/
  make_icon.py                   # app.ico/app.png uretici (globe mark)
app/
  core/
    pipeline.py                  # Ana ceviri pipeline'i (STT -> Translation -> TTS)
    audio_engine.py              # Ses yakalama ve oynatma
    audio_router.py              # Cihaz yonlendirme
    event_bus.py                 # Async event sistemi
  stt/
    base.py                      # BaseSTT abstract class
    deepgram_stt.py              # Deepgram STT implementasyonu
  translation/
    base.py                      # BaseTranslator abstract class (lang_key property)
    deepl_translator.py          # DeepL API translator
    google_translator.py         # Google Cloud Translation v2 translator
    cache.py                     # LRU translation cache
  tts/
    base.py                      # BaseTTS abstract class
    deepgram_tts.py              # Deepgram Aura TTS
    azure_tts.py                 # Azure Speech TTS
    provider_manager.py          # TTS provider secimi (dil bazli)
  gui/
    main_window.py               # Ana pencere (3 sayfa: Ceviri, Istatistik, Ayarlar)
    system_tray.py               # System tray entegrasyonu
    styles/
      theme.py                   # QSS kurumsal koyu tema (lacivert/mavi palet)
      icons.py                   # Inline SVG ikon seti -> QIcon/QPixmap (ek bagimlilik yok)
    assets/
      app.ico / app.png          # Uygulama ikonu (tools/make_icon.py ile uretilir)
    widgets/
      stats_tracker.py           # Oturum istatistikleri
  utils/
    config.py                    # Config sinifi (YAML + .env)
    constants.py                 # Desteklenen diller, ses sabitleri
    i18n.py                      # Coklu dil desteği (TR/EN/RU)
    logger.py                    # Loglama
```

## Mimari Kararlar

### Translation Provider Sistemi
- `BaseTranslator.lang_key` property: her translator kendi dil kodu mapping key'ini bilir ("deepl" veya "google")
- `SUPPORTED_LANGUAGES` dict'inde her dil icin hem `"deepl"` hem `"google"` kodlari var
- Pipeline, `self._translator.lang_key` kullanarak dogru dil kodunu secer
- `config.yaml` > `translation.provider` ile aktif provider belirlenir ("deepl" | "google")
- GUI'de Ayarlar sayfasinda provider dropdown + ilgili API key alanlari var

### Dil Kodlari Farkliliklari
- DeepL: buyuk harf, bazen bolgesel (EN-US, PT-PT, ZH-HANS)
- Google: kucuk harf ISO 639-1 (en, pt, zh)
- Deepgram: kucuk harf ISO 639-1

### Config Yapisi
- `config.yaml`: uygulama ayarlari (provider, formality, cache_size, ses, gui)
- `.env`: API key'ler (DEEPGRAM_API_KEY, DEEPL_API_KEY, GOOGLE_TRANSLATE_API_KEY, AZURE_SPEECH_KEY, AZURE_SPEECH_REGION)
- `Config.has_required_keys`: provider'a gore gerekli key kontrolu

### i18n
- 3 dil: TR (varsayilan), EN, RU
- `t("key", **kwargs)` fonksiyonu ile ceviri
- GUI dil degistiginde `_retranslate_ui()` tum widget'lari gunceller

### UI / Tasarim
- Kurumsal koyu tema: `styles/theme.py` (lacivert yuzeyler + `#4f7cff` mavi aksan + `#2dd4bf` teal ikincil)
- Her sayfa bir header bar ile baslar: baslik + alt-baslik; Ceviri sayfasinda ayrica durum pill'i (Hazir/Aktif/Durduruldu)
- Kart tabanli layout (`QFrame` class="card"), ikonlu kart basliklari, ikonlu sidebar nav
- Ikonlar `styles/icons.py` icinde inline SVG olarak tanimli; `icons.icon(ad, renk, boyut)` ile QIcon uretilir (QtSvg kullanir, ek asset dosyasi yok)
- Tema renk degisiklikleri iki yerde tutulur: `theme.py` QSS + `main_window.py` ustundeki palet sabitleri (TEXT/ACCENT/OK/... ) — ikisi senkron tutulmali
- `_retranslate_ui()` kart baslik label'larini (`_lang_card_title` vb.) gunceller; eski GroupBox `setTitle` yerine label `setText`

### Paketleme (frozen / installed)
- `Config` PyInstaller frozen modunu algilar (`sys.frozen`): `config.yaml` + `.env` kullanici-yazilabilir `%APPDATA%\RealTime Translator\` altina yazilir (Program Files salt-okunur)
- Ilk calistirmada paketteki (`sys._MEIPASS`) varsayilan `config.yaml` APPDATA'ya kopyalanir (`_seed_defaults`)
- Gelistirmede davranis degismez: config/.env proje kokunde
- Ikon yollari hem dev hem frozen'da calisir (`sys._MEIPASS` fallback)

## Build / Installer
Detaylar: `BUILD.md`
```powershell
powershell -ExecutionPolicy Bypass -File build.ps1
```
- PyInstaller -> `dist\RealTimeTranslator\` (onedir, windowed)
- Inno Setup kuruluysa -> `installer_output\RealTimeTranslator-Setup-<ver>.exe`
- Surum: `constants.py APP_VERSION` + `installer.iss MyAppVersion` birlikte guncellenir

## Calistirma
```bash
python main.py
```

## Onemli Notlar
- Yeni dependency eklenmeden Google Translate implementasyonu yapildi (urllib kullanildi)
- Google Translator, DeepL ile ayni pattern'i takip eder (cache, run_in_executor, hata yonetimi)
- Provider degisikligi config.yaml'a kaydedilir, pipeline restart'inda yeni provider kullanilir
