from pathlib import Path

from PIL import Image

from app.models.file_item import FileItem
from app.models.result import ProcessResult
from app.models.tool_options import ConvertOptions
from app.utils.file import resolve_output
from app.utils.image import open_image, save_image

_FORMAT_EXT = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "WEBP": ".webp",
    "BMP": ".bmp",
    "TIFF": ".tiff",
    "GIF": ".gif",
    "ICO": ".ico",
}


def _has_alpha(img: Image.Image) -> bool:
    if img.mode in ("RGBA", "LA"):
        return True
    if img.mode == "P" and "transparency" in img.info:
        return True
    return False


def _flatten_onto_color(img: Image.Image, bg_color: tuple[int, int, int]) -> Image.Image:
    if img.mode == "P":
        img = img.convert("RGBA")
    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, bg_color)
        background.paste(img, mask=img.split()[-1])
        return background
    if img.mode != "RGB":
        return img.convert("RGB")
    return img


def process(
    file: FileItem,
    options: ConvertOptions,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
) -> ProcessResult:
    try:
        img = open_image(file.path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))

    target_fmt = options.format.upper()
    if target_fmt == "JPG":
        target_fmt = "JPEG"

    if target_fmt == "JPEG" and _has_alpha(img):
        img = _flatten_onto_color(img, options.bg_color)

    ext = _FORMAT_EXT.get(target_fmt, ".jpg")
    out_path = resolve_output(
        file.path,
        Path(output_dir),
        overwrite,
        suffix,
        ext=ext,
    )

    try:
        save_image(img, out_path, format=target_fmt, quality=options.quality)
        return ProcessResult(success=True, output_path=out_path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))
