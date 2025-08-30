
import io
import base64
import PIL
from PIL import Image


def encode_image(image):
    assert isinstance(image, Image.Image), 'encode_image with invalid input type'
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_bytes = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return dict(type='image_bytes', data=image_bytes)


def encode_data_item(item: any):
    if isinstance(item, str):
        return dict(type='string', data=item)
    elif isinstance(item, int):
        return dict(type='int', data=item)
    elif isinstance(item, float):
        return dict(type='float', data=item)
    elif isinstance(item, bool):
        return dict(type='bool', data=item)
    elif isinstance(item, bytes):
        return dict(type='bytes', data=item)
    elif isinstance(item, Image.Image):
        return encode_image(item)
    raise TypeError(f'encode_data with invalid input type: {type(item)}')


def encode_dict(result: dict):
    assert isinstance(result, dict), 'encode_data with invalid input type'
    for key, value in result.items():
        result[key] = encode_data_item(value)
    return result


def encode_list(result):
    assert isinstance(result, (list, tuple)), 'encode_data with invalid input type'
    return [encode_data_item(item) for item in result]


def encode_data(result: any):
    if isinstance(result, dict):
        return encode_dict(result)
    elif isinstance(result, list):
        return encode_list(result)
    elif isinstance(result, tuple):
        return tuple(encode_list(result))
    else:
        return encode_data_item(result)
