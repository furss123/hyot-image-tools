import json

from app.constants import I18N_DIR

_strings: dict = {}


def load(lang: str) -> None:
    global _strings
    path = I18N_DIR / f"{lang}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        _strings = data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        _strings = {}


def tr(key: str) -> str:
    return _strings.get(key, key)
