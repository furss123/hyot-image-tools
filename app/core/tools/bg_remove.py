import io
from pathlib import Path

from PIL import Image, ImageFilter
from rembg import new_session, remove

from app.models.file_item import FileItem
from app.models.result import ProcessResult
from app.models.tool_options import BgRemoveOptions
from app.utils.file import resolve_output
from app.utils.image import save_image


def process(
    file: FileItem,
    options: BgRemoveOptions,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
) -> ProcessResult:
    try:
        session = new_session(options.model)
        img_bytes = file.path.read_bytes()
        result_bytes = remove(img_bytes, session=session)
        img = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

        if options.feather > 0:
            alpha = img.split()[3]
            alpha = alpha.filter(ImageFilter.GaussianBlur(options.feather))
            img.putalpha(alpha)

        out_path = resolve_output(
            file.path,
            Path(output_dir),
            overwrite,
            suffix,
            ext=".png",
        )
        save_image(img, out_path, format="PNG")
        return ProcessResult(success=True, output_path=out_path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))
