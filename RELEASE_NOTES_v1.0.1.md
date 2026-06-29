# HyoT Image Tools v1.0.1

Stable release with the shipping 7-tool app, performance improvements, and fixed PyInstaller bundling.

## Tools (7)

- **Reduce Size** — Compress by quality or target file size
- **Resize** — Scale by percentage, exact dimensions, or longest side
- **Convert Format** — JPG, PNG, WebP, BMP, TIFF
- **Rotate / Flip** — Angle, flip, EXIF auto-orient
- **Crop** — Aspect presets and interactive crop
- **Merge Images** — Horizontal, vertical, or grid layout
- **Bulk Rename** — Prefix, numbering, and zero-padding

## What's new in v1.0.1

- Focused 7-tool UI with dark/light themes and Korean/English UI
- Background preview workers and batch conversion (no main-thread blocking)
- Fixed PyInstaller bundling for `app.ui.tools` submodules
- Transparent app icon for executable and Inno Setup installer

## Downloads

| Asset | File |
|-------|------|
| Installer (x64) | `HyoT-Image-Tools-1.0.1-x64-setup.exe` |
| Portable (x64) | `HyoT-Image-Tools-1.0.1-x64-portable.zip` |

## Install from source

```bash
git clone https://github.com/furss123/hyot-image-tools.git
cd HyoT-Image-Tools
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
