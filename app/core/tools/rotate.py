from pathlib import Path

from PIL import Image

from app.models.file_item import FileItem
from app.models.result import ProcessResult
from app.models.tool_options import RotateOptions
from app.utils.exif import bake_rotation
from app.utils.file import resolve_output
from app.utils.image import detect_format, format_extension, open_image, save_image


def _parse_fill_color(fill_color: str | tuple[int, int, int]) -> tuple[int, ...]:
    if isinstance(fill_color, tuple):
        return fill_color
    color = fill_color.lstrip("#")
    return (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))


def process(
    file: FileItem,
    options: RotateOptions,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
) -> ProcessResult:
    try:
        img = open_image(file.path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))

    fmt = detect_format(file.path, img)

    try:
        if options.auto_exif:
            img = bake_rotation(img)

        if options.flip_h:
            img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if options.flip_v:
            img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        if options.angle != 0:
            if options.fill_color is None:
                img = img.convert("RGBA")
                img = img.rotate(-options.angle, expand=True, fillcolor=None)
                fmt = "PNG"
            else:
                fill = _parse_fill_color(options.fill_color)
                if img.mode == "RGBA":
                    fill = (*fill, 255)
                img = img.rotate(-options.angle, expand=True, fillcolor=fill)

        out_path = resolve_output(
            file.path,
            Path(output_dir),
            overwrite,
            suffix,
            ext=format_extension(fmt),
        )
        save_image(img, out_path, format=fmt)
        return ProcessResult(success=True, output_path=out_path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))
