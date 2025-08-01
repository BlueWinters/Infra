
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
    assert isinstance(image, PIL.Image.Image), 'process_resize with invalid input image'
    assert isinstance(height, int) and height > 0, 'process_resize with invalid resize height'
    assert isinstance(width, int) and width > 0, 'process_resize with invalid resize width'
    resized = image.resize((width, height), Image.Resampling.BILINEAR)
    return resized


def process_rotate(image, angle):
    if isinstance(image, str):
        image = decode_image(image)
    assert isinstance(image, PIL.Image.Image), 'process_rotate with invalid input image'
    assert isinstance(angle, (float, int)), 'process_rotate with invalid rotation angle'
    rotated = image.rotate(angle, expand=True)
    return rotated


def process_grayscale(image):
    if isinstance(image, str):
        image = decode_image(image)
    assert isinstance(image, PIL.Image.Image), 'process_grayscale with invalid input image'
    return ImageOps.grayscale(image)


def process_blur(image, radius):
    if isinstance(image, str):
        image = decode_image(image)
    assert isinstance(image, PIL.Image.Image), 'process_blur invalid input image'
    assert isinstance(radius, int) and radius > 0, 'process_blur with invalid blur radius'
    return image.filter(ImageFilter.GaussianBlur(radius))


def process_flip(image):
    if isinstance(image, str):
        image = decode_image(image)
    assert isinstance(image, PIL.Image.Image), 'process_flip with invalid input image'
    return ImageOps.flip(image)


def process_mirror(image):
    if isinstance(image, str):
        image = decode_image(image)
    assert isinstance(image, PIL.Image.Image), 'process_mirror with invalid input image'
    return ImageOps.mirror(image)

