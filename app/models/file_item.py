from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileItem:
    path: Path
    width: int | None = None
    height: int | None = None
    format: str = ""

    @property
    def filename(self) -> str:
        return self.path.name

    @property
    def size_kb(self) -> float:
        try:
            return self.path.stat().st_size / 1024
        except OSError:
            return 0.0
