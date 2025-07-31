
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


def process_grayscale(image):
    if isinstance(image, str):
        image = decode_image(image)
    assert isinstance(image, PIL.Image.Image)
    return ImageOps.grayscale(image)


def process_blur(image, radius):
    if isinstance(image, str):
        image = decode_image(image)
    assert isinstance(image, PIL.Image.Image)
    assert isinstance(radius, int) and radius > 0
    return image.filter(ImageFilter.GaussianBlur(radius))


def process_flip(image):
    if isinstance(image, str):
        image = decode_image(image)
    assert isinstance(image, PIL.Image.Image)
    return ImageOps.flip(image)


def process_mirror(image):
    if isinstance(image, str):
        image = decode_image(image)
    assert isinstance(image, PIL.Image.Image)
    return ImageOps.mirror(image)

