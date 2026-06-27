from pathlib import Path

from PIL import Image

from app.models.file_item import FileItem
from app.models.result import ProcessResult
from app.models.tool_options import ResizeOptions
from app.utils.file import resolve_output
from app.utils.image import detect_format, format_extension, open_image, save_image

_RESAMPLE_MAP = {
    "lanczos": Image.Resampling.LANCZOS,
    "bicubic": Image.Resampling.BICUBIC,
    "nearest": Image.Resampling.NEAREST,
}


def _compute_size(w: int, h: int, options: ResizeOptions) -> tuple[int, int]:
    if options.mode == "percent":
        return (
            max(1, int(w * options.percent / 100)),
            max(1, int(h * options.percent / 100)),
        )

    if options.mode == "exact":
        target_w = max(1, options.width)
        target_h = max(1, options.height)
        if options.keep_aspect:
            scale = min(target_w / w, target_h / h)
            return max(1, int(w * scale)), max(1, int(h * scale))
        return target_w, target_h

    if options.mode == "longest_side":
        longest = max(1, options.longest_side)
        max_dim = max(w, h)
        scale = longest / max_dim
        return max(1, int(w * scale)), max(1, int(h * scale))

    return w, h


def process(
    file: FileItem,
    options: ResizeOptions,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
) -> ProcessResult:
    try:
        img = open_image(file.path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))

    w, h = img.size
    new_w, new_h = _compute_size(w, h, options)

    if not options.allow_upscale and (new_w > w or new_h > h):
        return ProcessResult(success=False, message="upscale_not_allowed")

    fmt = detect_format(file.path, img)
    out_path = resolve_output(
        file.path,
        Path(output_dir),
        overwrite,
        suffix,
        ext=format_extension(fmt),
    )

    try:
        resample = _RESAMPLE_MAP.get(options.resample, Image.Resampling.LANCZOS)
        resized = img.resize((new_w, new_h), resample=resample)
        save_image(resized, out_path, format=fmt)
        return ProcessResult(success=True, output_path=out_path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))
