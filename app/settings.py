import json
from dataclasses import asdict, dataclass

from app.constants import SETTINGS_FILE


@dataclass
class Settings:
    theme: str = "dark"
    language: str = "ko"
    last_output_dir: str = ""
    overwrite: bool = False
    suffix: str = "_processed"
    last_tool: str = "compress"


def load_settings() -> Settings:
    if not SETTINGS_FILE.is_file():
        return Settings()

    try:
        data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return Settings()

    if not isinstance(data, dict):
        return Settings()

    known = {f.name for f in Settings.__dataclass_fields__.values()}
    return Settings(**{k: v for k, v in data.items() if k in known})


def save_settings(s: Settings) -> None:
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(
        json.dumps(asdict(s), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
