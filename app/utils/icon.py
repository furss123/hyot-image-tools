from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QImage, QPixmap

from app.constants import ASSETS_DIR

APP_ASSETS_DIR = Path(__file__).parent.parent / "assets"


def load_pixmap(
    path: str | Path,
    width: int | None = None,
    height: int | None = None,
) -> QPixmap:
    image = QImage(str(path))
    if image.isNull():
        return QPixmap()
    image = image.convertToFormat(QImage.Format.Format_ARGB32)
    pixmap = QPixmap.fromImage(image)
    if width is not None and height is not None:
        pixmap = pixmap.scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
    return pixmap


def load_app_icon() -> QIcon | None:
    ico_path = APP_ASSETS_DIR / "icon.ico"
    if ico_path.is_file():
        return QIcon(str(ico_path))
    png_path = APP_ASSETS_DIR / "icon.png"
    if png_path.is_file():
        return QIcon(str(png_path))
    legacy_png = ASSETS_DIR / "icons" / "app.png"
    if legacy_png.is_file():
        return QIcon(str(legacy_png))
    legacy_ico = ASSETS_DIR / "icons" / "app.ico"
    if legacy_ico.is_file():
        return QIcon(str(legacy_ico))
    return None
