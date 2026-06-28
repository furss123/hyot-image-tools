from dataclasses import dataclass, field


@dataclass
class CompressOptions:
    quality: int = 85
    target_kb: int = 0
    keep_format: bool = True


@dataclass
class ResizeOptions:
    mode: str = "percent"
    percent: int = 100
    width: int = 0
    height: int = 0
    keep_aspect: bool = True
    longest_side: int = 0
    allow_upscale: bool = False
    resample: str = "lanczos"


@dataclass
class ConvertOptions:
    format: str = "JPEG"
    quality: int = 85
    bg_color: tuple[int, int, int] | str = (255, 255, 255)


@dataclass
class CropOptions:
    mode: str = "manual"
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    ratio: str = "1:1"


@dataclass
class RotateOptions:
    angle: int = 0
    flip_h: bool = False
    flip_v: bool = False
    auto_exif: bool = True
    fill_color: tuple[int, int, int] | str | None = (255, 255, 255)


@dataclass
class OcrOptions:
    languages: list[str] = field(default_factory=lambda: ["kor", "eng"])
    merge_output: bool = False

@dataclass
class BulkRenameOptions:
    prefix: str = "image_"
    start_number: int = 1
    padding: int = 3
    file_index: int = 0


@dataclass
class MergeOptions:
    mode: str = "horizontal"
    gap: int = 4
    align: str = "top"
    grid_cols: int = 0
    output_format: str = "PNG"
    bg_color: str = "#FFFFFF"
