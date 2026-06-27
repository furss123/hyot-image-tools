import io
from pathlib import Path
from typing import BinaryIO

from PIL import Image

_EXT_TO_FORMAT = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "bmp": "BMP",
    "tif": "TIFF",
    "tiff": "TIFF",
    "gif": "GIF",
}

_FORMAT_TO_EXT = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "WEBP": ".webp",
    "BMP": ".bmp",
    "TIFF": ".tiff",
    "GIF": ".gif",
}


def open_image(path: Path) -> Image.Image:
    img = Image.open(path)
    img.load()
    return img


def detect_format(path: Path, img: Image.Image) -> str:
    if img.format:
        return img.format.upper()
    ext = path.suffix.lower().lstrip(".")
    return _EXT_TO_FORMAT.get(ext, "JPEG")


def format_extension(fmt: str) -> str:
    return _FORMAT_TO_EXT.get(fmt.upper(), ".jpg")


def _prepare_for_save(img: Image.Image, fmt: str) -> Image.Image:
    if fmt.upper() in ("JPEG", "JPG") and img.mode in ("RGBA", "P", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
        return background
    return img


def _save_kwargs(fmt: str, quality: int) -> dict:
    upper = fmt.upper()
    if upper in ("JPEG", "JPG"):
        return {"quality": quality, "optimize": True}
    if upper == "WEBP":
        return {"quality": quality, "method": 6}
    if upper == "PNG":
        return {"optimize": True}
    return {}


def save_image(
    img: Image.Image,
    dest: Path | BinaryIO,
    *,
    format: str,
    quality: int = 85,
) -> None:
    prepared = _prepare_for_save(img, format)
    kwargs = _save_kwargs(format, quality)
    if isinstance(dest, Path):
        dest.parent.mkdir(parents=True, exist_ok=True)
    prepared.save(dest, format=format, **kwargs)


def save_image_to_bytes(img: Image.Image, *, format: str, quality: int) -> bytes:
    buffer = io.BytesIO()
    save_image(img, buffer, format=format, quality=quality)
    return buffer.getvalue()
