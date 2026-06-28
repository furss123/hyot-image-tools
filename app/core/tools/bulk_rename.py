import shutil
from pathlib import Path

from app.models.file_item import FileItem
from app.models.result import ProcessResult
from app.models.tool_options import BulkRenameOptions


def process(
    file: FileItem,
    options: BulkRenameOptions,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
) -> ProcessResult:
    del overwrite, suffix
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        number = options.start_number + options.file_index
        new_name = (
            f"{options.prefix}{number:0{options.padding}d}{file.path.suffix.lower()}"
        )
        out_path = output_dir / new_name
        if out_path.exists():
            return ProcessResult(
                success=False,
                message=f"File already exists: {new_name}",
            )
        shutil.copy2(file.path, out_path)
        return ProcessResult(success=True, output_path=out_path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))
