from pathlib import Path
import os
import sys

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices


def open_folder_in_explorer(path: Path) -> bool:
    folder = path if path.is_dir() else path.parent
    if not folder.exists():
        return False
    if sys.platform == "win32":
        os.startfile(folder)  # noqa: S606
        return True
    return QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))


def resolve_output(
    input_path: Path,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
    ext: str | None = None,
) -> Path:
    extension = ext or input_path.suffix
    if extension and not extension.startswith("."):
        extension = f".{extension}"
    stem = input_path.stem if overwrite else f"{input_path.stem}{suffix}"
    return output_dir / f"{stem}{extension}"
