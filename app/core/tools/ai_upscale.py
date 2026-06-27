import re
import subprocess
from collections.abc import Callable
from pathlib import Path
from threading import Thread

from app.constants import THIRD_PARTY_DIR
from app.models.file_item import FileItem
from app.models.result import ProcessResult
from app.models.tool_options import AiUpscaleOptions
from app.utils.file import resolve_output

_BINARY = THIRD_PARTY_DIR / "realesrgan" / "realesrgan-ncnn-vulkan.exe"
_MODELS = THIRD_PARTY_DIR / "realesrgan" / "models"
_PERCENT_RE = re.compile(r"(\d+\.\d+)%")


def _drain_stderr(stderr, progress_cb: Callable[[int], None] | None) -> None:
    try:
        for line in iter(stderr.readline, b""):
            text = line.decode("utf-8", errors="replace")
            if progress_cb is None:
                continue
            match = _PERCENT_RE.search(text)
            if match:
                progress_cb(int(float(match.group(1))))
    finally:
        stderr.close()


def process(
    file: FileItem,
    options: AiUpscaleOptions,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
    progress_cb: Callable[[int], None] | None = None,
) -> ProcessResult:
    if not _BINARY.is_file():
        return ProcessResult(success=False, message="Binary missing")

    out_path = resolve_output(
        file.path,
        Path(output_dir),
        overwrite,
        suffix,
        ext=".png",
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(_BINARY),
        "-i",
        str(file.path),
        "-o",
        str(out_path),
        "-m",
        str(_MODELS),
        "-n",
        options.model,
        "-s",
        str(options.scale),
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert proc.stderr is not None
        Thread(
            target=_drain_stderr,
            args=(proc.stderr, progress_cb),
            daemon=True,
        ).start()
        proc.wait()
        if proc.stdout:
            proc.stdout.close()

        if proc.returncode != 0:
            return ProcessResult(
                success=False,
                message=f"Real-ESRGAN exited with code {proc.returncode}",
            )
        if not out_path.is_file():
            return ProcessResult(success=False, message="Output file was not created")

        return ProcessResult(success=True, output_path=out_path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))
