SUPPORTED_LANGUAGES = {
    "TR": {"name": "Türkçe", "deepgram": "tr", "deepl": "TR", "google": "tr", "azure_voice": "tr-TR-AhmetNeural"},
    "RU": {"name": "Русский", "deepgram": "ru", "deepl": "RU", "google": "ru", "azure_voice": "ru-RU-DmitryNeural"},
    "EN": {"name": "English", "deepgram": "en", "deepl": "EN-US", "google": "en", "azure_voice": "en-US-JennyNeural"},
    "DE": {"name": "Deutsch", "deepgram": "de", "deepl": "DE", "google": "de", "azure_voice": "de-DE-ConradNeural"},
    "FR": {"name": "Français", "deepgram": "fr", "deepl": "FR", "google": "fr", "azure_voice": "fr-FR-HenriNeural"},
    "ES": {"name": "Español", "deepgram": "es", "deepl": "ES", "google": "es", "azure_voice": "es-ES-AlvaroNeural"},
    "IT": {"name": "Italiano", "deepgram": "it", "deepl": "IT", "google": "it", "azure_voice": "it-IT-DiegoNeural"},
    "PT": {"name": "Português", "deepgram": "pt", "deepl": "PT-PT", "google": "pt", "azure_voice": "pt-PT-DuarteNeural"},
    "NL": {"name": "Nederlands", "deepgram": "nl", "deepl": "NL", "google": "nl", "azure_voice": "nl-NL-MaartenNeural"},
    "PL": {"name": "Polski", "deepgram": "pl", "deepl": "PL", "google": "pl", "azure_voice": "pl-PL-MarekNeural"},
    "JA": {"name": "日本語", "deepgram": "ja", "deepl": "JA", "google": "ja", "azure_voice": "ja-JP-KeitaNeural"},
    "ZH": {"name": "中文", "deepgram": "zh", "deepl": "ZH-HANS", "google": "zh", "azure_voice": "zh-CN-YunxiNeural"},
    "KO": {"name": "한국어", "deepgram": "ko", "deepl": "KO", "google": "ko", "azure_voice": "ko-KR-InJoonNeural"},
    "AR": {"name": "العربية", "deepgram": "ar", "deepl": "AR", "google": "ar", "azure_voice": "ar-SA-HamedNeural"},
    "UK": {"name": "Українська", "deepgram": "uk", "deepl": "UK", "google": "uk", "azure_voice": "uk-UA-OstapNeural"},
}

DEEPGRAM_AURA_SUPPORTED_LANGUAGES = {"EN", "ES", "DE", "FR", "IT", "JA", "NL", "PT"}

AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_DTYPE = "int16"
AUDIO_BUFFER_MS = 100

APP_NAME = "RealTime Translator"
APP_VERSION = "0.1.0"
