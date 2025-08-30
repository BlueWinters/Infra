import logging
from .pil_function import *


# 支持的操作映射
Processors = {
    "resize": process_resize,
    "rotate": process_rotate,
    "grayscale": process_grayscale,
    "blur": process_blur,
    "flip": process_flip,
    "mirror": process_mirror
}


def pipe_image_process(method, *args, **kwargs):
    """图像处理主流程"""
    try:
        assert method in Processors, 'pipe_image_process with invalid method'
        processor = Processors[method]
        result = processor(*args, **kwargs)
        return result
    except AssertionError as e:
        logging.error('process assert error: '.format(str(e)))
        raise e
