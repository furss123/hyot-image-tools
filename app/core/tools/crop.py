from pathlib import Path

from app.models.file_item import FileItem
from app.models.result import ProcessResult
from app.models.tool_options import CropOptions
from app.utils.file import resolve_output
from app.utils.image import detect_format, format_extension, open_image, save_image


def _parse_ratio(ratio: str) -> tuple[int, int]:
    parts = ratio.strip().split(":")
    if len(parts) != 2:
        return 1, 1
    try:
        left = max(1, int(parts[0].strip()))
        right = max(1, int(parts[1].strip()))
        return left, right
    except ValueError:
        return 1, 1


def _clamp_box(x: int, y: int, w: int, h: int, img_w: int, img_h: int) -> tuple[int, int, int, int]:
    x = max(0, min(x, max(img_w - 1, 0)))
    y = max(0, min(y, max(img_h - 1, 0)))
    w = max(1, min(w, img_w - x))
    h = max(1, min(h, img_h - y))
    return x, y, w, h


def _center_square_box(img_w: int, img_h: int) -> tuple[int, int, int, int]:
    side = min(img_w, img_h)
    x = (img_w - side) // 2
    y = (img_h - side) // 2
    return x, y, side, side


def _ratio_box(img_w: int, img_h: int, ratio: str) -> tuple[int, int, int, int]:
    ratio_w, ratio_h = _parse_ratio(ratio)
    target_ratio = ratio_w / ratio_h
    img_ratio = img_w / img_h

    if img_ratio > target_ratio:
        crop_h = img_h
        crop_w = int(img_h * target_ratio)
    else:
        crop_w = img_w
        crop_h = int(img_w / target_ratio)

    crop_w = max(1, min(crop_w, img_w))
    crop_h = max(1, min(crop_h, img_h))
    x = (img_w - crop_w) // 2
    y = (img_h - crop_h) // 2
    return x, y, crop_w, crop_h


def _crop_box(img_w: int, img_h: int, options: CropOptions) -> tuple[int, int, int, int]:
    if options.mode == "manual":
        box = (options.x, options.y, options.width, options.height)
    elif options.mode == "ratio":
        box = _ratio_box(img_w, img_h, options.ratio)
    elif options.mode == "center":
        box = _center_square_box(img_w, img_h)
    else:
        box = (0, 0, img_w, img_h)

    return _clamp_box(*box, img_w, img_h)


def process(
    file: FileItem,
    options: CropOptions,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
) -> ProcessResult:
    try:
        img = open_image(file.path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))

    img_w, img_h = img.size
    x, y, w, h = _crop_box(img_w, img_h, options)

    fmt = detect_format(file.path, img)
    out_path = resolve_output(
        file.path,
        Path(output_dir),
        overwrite,
        suffix,
        ext=format_extension(fmt),
    )

    try:
        cropped = img.crop((x, y, x + w, y + h))
        save_image(cropped, out_path, format=fmt)
        return ProcessResult(success=True, output_path=out_path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))
