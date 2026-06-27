from pathlib import Path

from app.models.file_item import FileItem
from app.models.result import ProcessResult
from app.models.tool_options import CompressOptions
from app.utils.file import resolve_output
from app.utils.image import (
    detect_format,
    format_extension,
    open_image,
    save_image,
    save_image_to_bytes,
)


def process(
    file: FileItem,
    options: CompressOptions,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
) -> ProcessResult:
    try:
        img = open_image(file.path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))

    fmt = detect_format(file.path, img) if options.keep_format else "JPEG"
    out_path = resolve_output(
        file.path,
        Path(output_dir),
        overwrite,
        suffix,
        ext=format_extension(fmt),
    )

    try:
        if options.target_kb > 0:
            target_bytes = options.target_kb * 1024
            quality = 95
            data = b""
            while quality >= 5:
                data = save_image_to_bytes(img, format=fmt, quality=quality)
                if len(data) <= target_bytes:
                    break
                quality -= 5
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(data)
        else:
            save_image(img, out_path, format=fmt, quality=options.quality)

        return ProcessResult(success=True, output_path=out_path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))
