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


def _parse_bg_color(bg_color: tuple[int, int, int] | str) -> tuple[int, int, int]:
    if isinstance(bg_color, tuple):
        return bg_color
    hex_color = bg_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


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

    if options.bg_color == "transparent":
        if target_fmt == "JPEG":
            target_fmt = "PNG"
        img = img.convert("RGBA")
    elif img.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", img.size, _parse_bg_color(options.bg_color))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1])
        img = bg

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
