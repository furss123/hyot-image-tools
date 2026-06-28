from __future__ import annotations

import io
from pathlib import Path

from PIL import Image
from PyQt6.QtCore import QThread, pyqtSignal

from app.models.tool_options import ResizeOptions, RotateOptions
from app.utils.exif import bake_rotation

PREVIEW_DEBOUNCE_MS = 200


def close_image(img: Image.Image | None) -> None:
    if img is None:
        return
    try:
        img.close()
    except Exception:
        pass


class BeforePreviewWorker(QThread):
    loaded = pyqtSignal(bytes, bytes)
    failed = pyqtSignal(str)

    def __init__(self, path: Path, max_size: tuple[int, int]) -> None:
        super().__init__()
        self._path = path
        self._max_size = max_size

    def run(self) -> None:
        try:
            with Image.open(self._path) as opened:
                if opened.mode in ("RGBA", "LA", "P"):
                    full = opened.convert("RGBA")
                else:
                    full = opened.convert("RGB")
                full_buf = io.BytesIO()
                full_fmt = "PNG" if full.mode == "RGBA" else "JPEG"
                full.save(full_buf, format=full_fmt)
                thumb = full.copy()
                thumb.thumbnail(self._max_size, Image.Resampling.LANCZOS)
                thumb_buf = io.BytesIO()
                thumb.save(thumb_buf, format=full_fmt)
                close_image(full)
                close_image(thumb)
            self.loaded.emit(thumb_buf.getvalue(), full_buf.getvalue())
        except Exception as exc:
            self.failed.emit(str(exc))


class RotatePreviewWorker(QThread):
    done = pyqtSignal(bytes)
    failed = pyqtSignal(str)

    def __init__(self, path: Path, options: RotateOptions) -> None:
        super().__init__()
        self._path = path
        self._options = options

    def run(self) -> None:
        img: Image.Image | None = None
        try:
            img = Image.open(self._path)
            opts = self._options
            if opts.auto_exif:
                img = bake_rotation(img)
            if opts.flip_h:
                img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if opts.flip_v:
                img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            if opts.angle != 0:
                if opts.fill_color is None:
                    img = img.convert("RGBA")
                    img = img.rotate(-opts.angle, expand=True)
                else:
                    fill = _parse_fill_color(opts.fill_color)
                    if img.mode == "RGBA":
                        fill = (*fill, 255)
                    img = img.rotate(-opts.angle, expand=True, fillcolor=fill)
            fmt = "PNG" if img.mode == "RGBA" else "JPEG"
            buf = io.BytesIO()
            img.save(buf, format=fmt)
            self.done.emit(buf.getvalue())
        except Exception as exc:
            self.failed.emit(str(exc))
        finally:
            close_image(img)


class ResizePreviewWorker(QThread):
    done = pyqtSignal(bytes, bytes, bytes, str)
    failed = pyqtSignal(str)

    def __init__(
        self,
        path: Path,
        options: ResizeOptions,
        source_bytes: bytes | None,
    ) -> None:
        super().__init__()
        self._path = path
        self._options = options
        self._source_bytes = source_bytes

    def run(self) -> None:
        img: Image.Image | None = None
        source: Image.Image | None = None
        result_img: Image.Image | None = None
        try:
            if self._source_bytes:
                source = Image.open(io.BytesIO(self._source_bytes))
                img = source.copy()
            else:
                img = Image.open(self._path)
            opts = self._options
            orig_w, orig_h = img.size

            if opts.mode == "percent":
                nw = max(1, int(orig_w * opts.percent / 100))
                nh = max(1, int(orig_h * opts.percent / 100))
            elif opts.mode == "exact":
                if opts.keep_aspect:
                    ratio = min(opts.width / orig_w, opts.height / orig_h)
                    nw = max(1, int(orig_w * ratio))
                    nh = max(1, int(orig_h * ratio))
                else:
                    nw, nh = max(1, opts.width), max(1, opts.height)
            elif opts.mode == "longest_side":
                ratio = opts.longest_side / max(orig_w, orig_h)
                nw = max(1, int(orig_w * ratio))
                nh = max(1, int(orig_h * ratio))
            else:
                nw, nh = orig_w, orig_h

            if not opts.allow_upscale:
                nw = min(nw, orig_w)
                nh = min(nh, orig_h)

            resample_map = {
                "lanczos": Image.Resampling.LANCZOS,
                "bicubic": Image.Resampling.BICUBIC,
                "nearest": Image.Resampling.NEAREST,
            }
            resample = resample_map.get(opts.resample, Image.Resampling.LANCZOS)
            result_img = img.resize((nw, nh), resample)

            before_buf = io.BytesIO()
            img.save(before_buf, format="PNG")
            after_buf = io.BytesIO()
            result_img.save(after_buf, format="PNG")
            status = (
                f"{orig_w}|{orig_h}|{nw}|{nh}|{int(nw / orig_w * 100) if orig_w else 100}"
            )
            self.done.emit(
                before_buf.getvalue(),
                after_buf.getvalue(),
                after_buf.getvalue(),
                status,
            )
        except Exception as exc:
            self.failed.emit(str(exc))
        finally:
            close_image(source)
            close_image(img)
            close_image(result_img)


class FilePixmapWorker(QThread):
    loaded = pyqtSignal(bytes)
    failed = pyqtSignal(str)

    def __init__(self, path: Path) -> None:
        super().__init__()
        self._path = path

    def run(self) -> None:
        try:
            with Image.open(self._path) as opened:
                if opened.mode in ("RGBA", "LA", "P"):
                    converted = opened.convert("RGBA")
                else:
                    converted = opened.convert("RGB")
                buf = io.BytesIO()
                fmt = "PNG" if converted.mode == "RGBA" else "JPEG"
                converted.save(buf, format=fmt)
                if converted is not opened:
                    close_image(converted)
            self.loaded.emit(buf.getvalue())
        except Exception as exc:
            self.failed.emit(str(exc))


def _parse_fill_color(fill_color: str | tuple[int, int, int]) -> tuple[int, ...]:
    if isinstance(fill_color, tuple):
        return fill_color
    color = fill_color.lstrip("#")
    return (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))
