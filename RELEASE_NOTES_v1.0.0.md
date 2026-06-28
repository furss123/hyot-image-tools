# HyoT Image Tools v1.0.0

Initial stable release of HyoT Image Tools — a Windows batch image processor.

## Tools (7)

- **Reduce Size** — Compress images by quality or target file size (JPEG, WebP, PNG)
- **Resize** — Scale by percentage, exact width/height, or longest side
- **Convert Format** — Convert between JPG, PNG, WebP, BMP, and TIFF
- **Rotate / Flip** — Rotate at any angle, flip horizontally/vertically, auto EXIF orientation
- **Crop** — Interactive crop with aspect-ratio presets
- **Merge Images** — Combine images horizontally, vertically, or in a grid
- **Bulk Rename** — Batch rename with prefix, start number, and zero-padding

## Highlights

- Drag-and-drop and folder import
- Live before/after preview (resize, rotate, merge)
- Dark and light themes · Korean / English UI
- Background batch processing with progress and cancel
- Custom output folder, suffix, and overwrite options

## Downloads

| Asset | File |
|-------|------|
| Installer (x64) | `HyoT-Image-Tools-1.0.0-x64-setup.exe` |
| Portable (x64) | `HyoT-Image-Tools-1.0.0-x64-portable.zip` |

## Requirements

- Windows 10 22H2+ (x64)
- Python 3.10+ (source install): PyQt6, Pillow

## Install from source

```bash
git clone https://github.com/furss123/hyot-image-tools.git
cd HyoT-Image-Tools
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Full changelog:** https://github.com/furss123/hyot-image-tools/compare/v1.0.0
