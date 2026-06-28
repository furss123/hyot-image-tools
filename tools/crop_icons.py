from pathlib import Path

from PIL import Image

ICON_DIR = Path(__file__).resolve().parent.parent / "assets" / "icons"


def main() -> None:
    for path in sorted(ICON_DIR.glob("*.png")):
        img = Image.open(path).convert("RGBA")
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
        size = max(img.size)
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        offset = ((size - img.width) // 2, (size - img.height) // 2)
        canvas.paste(img, offset, img)
        canvas.save(path)
        print(f"Cropped: {path.name}")


if __name__ == "__main__":
    main()
