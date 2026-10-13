import os
import sys
import shutil
from pathlib import Path

import yaml
from dotenv import load_dotenv


def _is_frozen() -> bool:
    """True when running from a PyInstaller bundle (installed app)."""
    return getattr(sys, "frozen", False)


def _user_data_dir() -> Path:
    """Writable per-user data dir for the installed app (%APPDATA%\\RealTime Translator)."""
    base = os.getenv("APPDATA") or str(Path.home())
    d = Path(base) / "RealTime Translator"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _bundle_dir() -> Path:
    """Directory where PyInstaller extracted bundled data (or project root in dev)."""
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent.parent))


class Config:
    def __init__(self, config_path: str = None):
        # In a frozen/installed build, config and .env live in a writable user
        # directory; in development they live next to the source tree.
        if _is_frozen():
            self._base = _user_data_dir()
        else:
            self._base = Path(__file__).resolve().parent.parent.parent

        self._config_path = Path(config_path) if config_path else (self._base / "config.yaml")
        self._env_path = self._base / ".env"
        self._data = {}
        self._seed_defaults()
        self._load_env()
        self._load_yaml()

    def _seed_defaults(self):
        """On first run of the installed app, copy the bundled default config."""
        if _is_frozen() and not self._config_path.exists():
            src = _bundle_dir() / "config.yaml"
            try:
                if src.exists():
                    shutil.copyfile(src, self._config_path)
            except OSError:
                pass

    def _load_env(self):
        if self._env_path.exists():
            load_dotenv(self._env_path, override=True)

    def _load_yaml(self):
        if self._config_path.exists():
            with open(self._config_path, "r", encoding="utf-8") as f:
                self._data = yaml.safe_load(f) or {}

    def get(self, key: str, default=None):
        keys = key.split(".")
        value = self._data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def set(self, key: str, value):
        keys = key.split(".")
        data = self._data
        for k in keys[:-1]:
            if k not in data or not isinstance(data[k], dict):
                data[k] = {}
            data = data[k]
        data[keys[-1]] = value

    def save(self):
        with open(self._config_path, "w", encoding="utf-8") as f:
            yaml.dump(self._data, f, default_flow_style=False, allow_unicode=True)

    def save_api_keys(self, deepgram: str, deepl: str, azure_key: str, azure_region: str, google_key: str = ""):
        lines = []
        lines.append(f"DEEPGRAM_API_KEY={deepgram}")
        lines.append(f"DEEPL_API_KEY={deepl}")
        lines.append(f"AZURE_SPEECH_KEY={azure_key}")
        lines.append(f"AZURE_SPEECH_REGION={azure_region}")
        lines.append(f"GOOGLE_TRANSLATE_API_KEY={google_key}")
        with open(self._env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        # Reload into environment
        os.environ["DEEPGRAM_API_KEY"] = deepgram
        os.environ["DEEPL_API_KEY"] = deepl
        os.environ["AZURE_SPEECH_KEY"] = azure_key
        os.environ["AZURE_SPEECH_REGION"] = azure_region
        os.environ["GOOGLE_TRANSLATE_API_KEY"] = google_key

    @property
    def has_required_keys(self) -> bool:
        provider = self.get("translation.provider", "deepl")
        if provider == "google":
            return bool(self.deepgram_api_key and self.google_api_key)
        return bool(self.deepgram_api_key and self.deepl_api_key)

    @property
    def deepgram_api_key(self) -> str:
        return os.getenv("DEEPGRAM_API_KEY", "")

    @property
    def deepl_api_key(self) -> str:
        return os.getenv("DEEPL_API_KEY", "")

    @property
    def google_api_key(self) -> str:
        return os.getenv("GOOGLE_TRANSLATE_API_KEY", "")

    @property
    def azure_speech_key(self) -> str:
        return os.getenv("AZURE_SPEECH_KEY", "")

    @property
    def azure_speech_region(self) -> str:
        return os.getenv("AZURE_SPEECH_REGION", "westeurope")
