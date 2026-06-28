from __future__ import annotations

import importlib
from dataclasses import dataclass, replace
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal

from app.models.result import ProcessResult

_PREVIEW_TOOLS = frozenset({"resize", "rotate", "merge"})


@dataclass
class ConversionTask:
    tool_id: str
    files: list
    options: object
    output_dir: Path
    overwrite: bool
    suffix: str
    export_img: object | None = None
    crop_img: object | None = None
    crop_source_path: Path | None = None


def _save_preview_export(
    img,
    source_path: Path,
    tool_id: str,
    options,
    output_dir: Path,
    overwrite: bool,
    suffix: str,
) -> ProcessResult:
    from app.utils.file import resolve_output
    from app.utils.image import save_image

    try:
        if tool_id == "merge":
            fmt = options.output_format.upper()
            ext = ".jpg" if fmt == "JPG" else ".png"
            save_fmt = "JPEG" if fmt == "JPG" else "PNG"
        else:
            ext = source_path.suffix.lower() or ".png"
            if ext in (".jpg", ".jpeg"):
                save_fmt, ext = "JPEG", ".jpg"
            elif ext == ".webp":
                save_fmt = "WEBP"
            else:
                save_fmt, ext = "PNG", ".png"

        out_img = img
        if save_fmt == "JPEG" and out_img.mode == "RGBA":
            out_img = out_img.convert("RGB")

        out_path = resolve_output(
            source_path, Path(output_dir), overwrite, suffix, ext=ext
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        save_image(out_img, out_path, format=save_fmt, quality=90)
        return ProcessResult(success=True, output_path=out_path)
    except Exception as exc:
        return ProcessResult(success=False, message=str(exc))


class ConversionWorker(QThread):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(int, int, object)

    def __init__(self, task: ConversionTask) -> None:
        super().__init__()
        self._task = task
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    def run(self) -> None:
        task = self._task
        tool_id = task.tool_id

        if tool_id == "crop" and task.crop_img is not None:
            self._run_crop(task)
            return

        if tool_id == "merge":
            self._run_merge(task)
            return

        self._run_batch(task)

    def _emit_finished(self, success: int, fail: int, last_output: Path | None = None) -> None:
        self.finished.emit(success, fail, last_output)

    def _run_crop(self, task: ConversionTask) -> None:
        from app.utils.file import resolve_output
        from app.utils.image import save_image

        self.progress.emit(0, 1)
        if self._cancelled:
            self._emit_finished(0, 0)
            return
        try:
            source_path = task.crop_source_path or task.files[0].path
            out_path = resolve_output(
                source_path, task.output_dir, task.overwrite, task.suffix, ext=".png"
            )
            out_path.parent.mkdir(parents=True, exist_ok=True)
            save_image(task.crop_img, out_path, format="PNG")
            self.progress.emit(1, 1)
            self._emit_finished(1, 0, out_path)
        except Exception:
            self.progress.emit(1, 1)
            self._emit_finished(0, 1)

    def _run_merge(self, task: ConversionTask) -> None:
        self.progress.emit(0, 1)
        if self._cancelled:
            self._emit_finished(0, 0)
            return

        if task.export_img is not None:
            result = _save_preview_export(
                task.export_img,
                task.files[0].path,
                task.tool_id,
                task.options,
                task.output_dir,
                task.overwrite,
                task.suffix,
            )
            self.progress.emit(1, 1)
            self._emit_finished(
                1 if result.success else 0,
                0 if result.success else 1,
                result.output_path,
            )
            return

        from app.core.tools import merge as merge_module

        result = merge_module.process(
            task.files, task.options, task.output_dir, task.overwrite, task.suffix
        )
        self.progress.emit(1, 1)
        self._emit_finished(
            1 if result.success else 0,
            0 if result.success else 1,
            result.output_path,
        )

    def _run_batch(self, task: ConversionTask) -> None:
        tool_id = task.tool_id
        files = task.files
        total = len(files)

        try:
            module = importlib.import_module(f"app.core.tools.{tool_id}")
            process_fn = getattr(module, "process", None)
            if process_fn is None:
                self._emit_finished(0, 0)
                return
        except ImportError:
            self._emit_finished(0, 0)
            return

        success = 0
        fail = 0
        last_output: Path | None = None
        for i, file_item in enumerate(files, 1):
            if self._cancelled:
                self._emit_finished(success, fail, last_output)
                return

            run_options = task.options
            if tool_id == "bulk_rename":
                run_options = replace(task.options, file_index=i - 1)

            if i == 1 and task.export_img is not None and tool_id in _PREVIEW_TOOLS:
                result = _save_preview_export(
                    task.export_img,
                    file_item.path,
                    tool_id,
                    run_options,
                    task.output_dir,
                    task.overwrite,
                    task.suffix,
                )
            else:
                result = process_fn(
                    file_item,
                    run_options,
                    task.output_dir,
                    task.overwrite,
                    task.suffix,
                )

            if result.success:
                success += 1
                if result.output_path is not None:
                    last_output = result.output_path
            else:
                fail += 1
            self.progress.emit(i, total)

        self._emit_finished(success, fail, last_output)
