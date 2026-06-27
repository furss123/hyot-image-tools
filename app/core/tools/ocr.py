from pathlib import Path

import pytesseract
from pytesseract import TesseractNotFoundError

from app.models.file_item import FileItem
from app.models.result import ProcessResult
from app.models.tool_options import OcrOptions
from app.utils.file import resolve_output
from app.utils.image import open_image


def process(
    file: FileItem,
    options: OcrOptions,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
) -> ProcessResult:
    try:
        img = open_image(file.path)
        lang_str = "+".join(options.languages or ["kor", "eng"])
        text = pytesseract.image_to_string(img, lang=lang_str)

        if not options.merge_output:
            out_path = resolve_output(
                file.path,
                Path(output_dir),
                overwrite,
                suffix,
                ext=".txt",
            )
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(text, encoding="utf-8")
            return ProcessResult(success=True, output_path=out_path)

        return ProcessResult(success=True, output_path=None, extra=text)
    except TesseractNotFoundError as exc:
        return ProcessResult(success=False, message=str(exc))
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))
