from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProcessResult:
    success: bool
    output_path: Path | None = None
    message: str = ""
    extra: str | None = None
