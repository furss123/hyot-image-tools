from PIL import Image

_ORIENTATION_TRANSPOSE = {
    2: Image.Transpose.FLIP_LEFT_RIGHT,
    3: Image.Transpose.ROTATE_180,
    4: Image.Transpose.FLIP_TOP_BOTTOM,
    5: Image.Transpose.TRANSPOSE,
    6: Image.Transpose.ROTATE_270,
    7: Image.Transpose.TRANSVERSE,
    8: Image.Transpose.ROTATE_90,
}


def bake_rotation(img: Image.Image) -> Image.Image:
    try:
        exif = img.getexif()
        orientation = exif.get(274)
        if orientation in _ORIENTATION_TRANSPOSE:
            img = img.transpose(_ORIENTATION_TRANSPOSE[orientation])
    except Exception:
        pass
    return img
