import math
import time
from pathlib import Path

from PIL import Image, ImageColor

from app.models.file_item import FileItem
from app.models.result import ProcessResult
from app.models.tool_options import MergeOptions
from app.utils.file import resolve_output
from app.utils.image import save_image


def _create_canvas(total_w: int, total_h: int, bg_color_val: str) -> Image.Image:
    if bg_color_val == "transparent":
        return Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    if bg_color_val and Path(bg_color_val).exists():
        bg_img = Image.open(bg_color_val).convert("RGBA")
        return bg_img.resize((total_w, total_h), Image.Resampling.LANCZOS)
    try:
        rgb = ImageColor.getrgb(bg_color_val)
        return Image.new("RGBA", (total_w, total_h), rgb + (255,))
    except Exception:
        return Image.new("RGBA", (total_w, total_h), (255, 255, 255, 255))


def merge_images(images: list[Image.Image], options: MergeOptions) -> Image.Image:
    if options.mode == "horizontal":
        total_w = sum(img.width for img in images) + options.gap * (len(images) - 1)
        total_h = max(img.height for img in images)
        canvas = _create_canvas(total_w, total_h, options.bg_color)
        x = 0
        for img in images:
            if options.align == "center":
                y = (total_h - img.height) // 2
            elif options.align == "bottom":
                y = total_h - img.height
            else:
                y = 0
            canvas.paste(img, (x, y), img)
            x += img.width + options.gap
        return canvas

    if options.mode == "vertical":
        total_w = max(img.width for img in images)
        total_h = sum(img.height for img in images) + options.gap * (len(images) - 1)
        canvas = _create_canvas(total_w, total_h, options.bg_color)
        y = 0
        for img in images:
            if options.align == "center":
                x = (total_w - img.width) // 2
            elif options.align == "right":
                x = total_w - img.width
            else:
                x = 0
            canvas.paste(img, (x, y), img)
            y += img.height + options.gap
        return canvas

    n = len(images)
    cols = options.grid_cols if options.grid_cols > 0 else math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    cell_w = max(img.width for img in images)
    cell_h = max(img.height for img in images)
    total_w = cols * cell_w + options.gap * (cols - 1)
    total_h = rows * cell_h + options.gap * (rows - 1)
    canvas = _create_canvas(total_w, total_h, options.bg_color)
    for i, img in enumerate(images):
        col = i % cols
        row = i // cols
        x = col * (cell_w + options.gap) + (cell_w - img.width) // 2
        y = row * (cell_h + options.gap) + (cell_h - img.height) // 2
        canvas.paste(img, (x, y), img)
    return canvas


def process(
    files: list[FileItem],
    options: MergeOptions,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
) -> ProcessResult:
    start = time.time()
    if not files:
        return ProcessResult(success=False, message="No files to merge")

    try:
        images = [Image.open(f.path).convert("RGBA") for f in files]
        canvas = merge_images(images, options)

        fmt = options.output_format.upper()
        if fmt == "JPG":
            canvas = canvas.convert("RGB")
            ext = ".jpg"
            save_fmt = "JPEG"
        else:
            ext = ".png"
            save_fmt = "PNG"

        out_path = resolve_output(
            files[0].path, Path(output_dir), overwrite, suffix, ext=ext
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        save_image(canvas, out_path, format=save_fmt, quality=90)

        duration = int((time.time() - start) * 1000)
        return ProcessResult(
            success=True,
            output_path=out_path,
            message="",
            extra=str(duration),
        )
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))
