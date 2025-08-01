
import io
import base64
import PIL
from PIL import Image


def encode_image(image):
    assert isinstance(image, Image.Image), 'encode_image with invalid input type'
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def decode_image(image_data: str) -> PIL.Image.Image:
    assert isinstance(image_data, str), 'decode_image with invalid input type'
    try:
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception as e:
        raise ValueError('decode_image with invalid input value')

