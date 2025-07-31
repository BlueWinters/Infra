import logging
import time
from .pil_io import *
from .pil_function import *


# 支持的操作映射
Processors = {
    "check": process_check,
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
        # 记录开始时间
        start_time = time.perf_counter()

        # 应用图像处理
        processor = Processors[method]
        result = processor(*args, **kwargs)

        # 记录结束时间
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        # 返回成功响应
        return {
            "result": result,
            "elapsed": round(elapsed_time, 4),
        }
    except AssertionError as e:
        logging.error('process assert error: '.format(str(e)))
        raise e
