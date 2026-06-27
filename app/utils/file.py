from pathlib import Path


def resolve_output(
    input_path: Path,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
    ext: str | None = None,
) -> Path:
    extension = ext or input_path.suffix
    if extension and not extension.startswith("."):
        extension = f".{extension}"
    stem = input_path.stem if overwrite else f"{input_path.stem}{suffix}"
    return output_dir / f"{stem}{extension}"
