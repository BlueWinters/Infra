
import PIL
from PIL import Image, ImageOps, ImageFilter
from .pil_io import *


def process_check(*args, **kwargs):
    import pprint
    format_args = pprint.pformat(args, width=50, indent=4, compact=False)
    print(format_args)
    format_kwargs = pprint.pformat(kwargs, width=50, indent=4, compact=False)
    print(format_kwargs)


def process_resize(image, height, width):
    if isinstance(image, str):
        image = decode_image(image)
    assert isinstance(image, PIL.Image.Image)
    assert isinstance(height, int) and height > 0
    assert isinstance(width, int) and width > 0
    resized = image.resize((width, height), Image.Resampling.BILINEAR)
    return encode_image(resized)


def process_rotate(image, angle):
    if isinstance(image, str):
        image = decode_image(image)
    assert isinstance(image, PIL.Image.Image)
    assert isinstance(angle, (float, int))
    rotated = image.rotate(angle, expand=True)
    return encode_image(rotated)


def process_grayscale(img):
    """处理 grayscale 操作"""
    return ImageOps.grayscale(img), None


def process_blur(img, params):
    """处理 blur 操作"""
    radius = params.get("radius", 3)
    if not isinstance(radius, (int, float)) or radius <= 0:
        return None, "Invalid blur radius"
    return img.filter(ImageFilter.GaussianBlur(radius)), None


def process_flip(img):
    """处理 flip 操作"""
    return ImageOps.flip(img), None


def process_mirror(img):
    """处理 mirror 操作"""
    return ImageOps.mirror(img), None

