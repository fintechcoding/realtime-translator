"""Lightweight, dependency-free API key validators.

Each function makes one short authenticated request and returns a status string:
    "valid"   — the key authenticated successfully
    "invalid" — the service rejected the key (401/403/400 auth error)
    "error"   — could not determine (network/timeout/other); not the key's fault

These are blocking (urllib); call them from a thread/executor, not the UI thread.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

_TIMEOUT = 8


def _status_from_http(code: int) -> str:
    if code in (200, 201, 204):
        return "valid"
    if code in (401, 403, 400):
        return "invalid"
    return "error"


def validate_deepgram(api_key: str) -> str:
    if not api_key:
        return "empty"
    req = urllib.request.Request(
        "https://api.deepgram.com/v1/projects",
        headers={"Authorization": f"Token {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            return _status_from_http(resp.status)
    except urllib.error.HTTPError as e:
        return _status_from_http(e.code)
    except Exception:
        return "error"


def validate_deepl(api_key: str) -> str:
    if not api_key:
        return "empty"
    # Free keys end with ":fx" and use the free host.
    host = "api-free.deepl.com" if api_key.strip().endswith(":fx") else "api.deepl.com"
    req = urllib.request.Request(
        f"https://{host}/v2/usage",
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            return _status_from_http(resp.status)
    except urllib.error.HTTPError as e:
        return _status_from_http(e.code)
    except Exception:
        return "error"


def validate_google(api_key: str) -> str:
    if not api_key:
        return "empty"
    params = urllib.parse.urlencode({"key": api_key, "target": "en"})
    url = f"https://translation.googleapis.com/language/translate/v2/languages?{params}"
    try:
        with urllib.request.urlopen(url, timeout=_TIMEOUT) as resp:
            return _status_from_http(resp.status)
    except urllib.error.HTTPError as e:
        return _status_from_http(e.code)
    except Exception:
        return "error"


def validate_azure(api_key: str, region: str) -> str:
    if not api_key:
        return "empty"
    region = (region or "westeurope").strip()
    url = f"https://{region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    req = urllib.request.Request(
        url, data=b"", method="POST",
        headers={"Ocp-Apim-Subscription-Key": api_key, "Content-Length": "0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            return _status_from_http(resp.status)
    except urllib.error.HTTPError as e:
        return _status_from_http(e.code)
    except Exception:
        return "error"
