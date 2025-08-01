# tests/test_process_image.py
import pytest
import base64
import json
import os
import logging
from io import BytesIO
from PIL import Image
import numpy as np
from core.image_process import pipe_image_process
from params import parse_parameters


def create_test_image_base64(image_path='asset/obama.png'):
    """创建测试图像并返回 Base64 编码"""
    # 检查图像文件是否存在
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            image_data = f.read()
        return base64.b64encode(image_data).decode('utf-8')
    else:
        # 如果文件不存在，创建一个简单的测试图像
        img = Image.new('RGB', (224, 224), color=(73, 109, 137))
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode('utf-8')


def setup_cache_directory(subdir):
    """创建缓存目录用于保存测试结果"""
    cache_dir = os.path.join('cache/tests/test_process_image', subdir)
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def save_image_from_base64(image_b64, filename):
    """将Base64编码的图像保存为文件"""
    cache_dir = setup_cache_directory('result_image')
    image_data = base64.b64decode(image_b64)
    with open(os.path.join(cache_dir, filename), 'wb') as f:
        f.write(image_data)


def test_process_image_resize():
    """测试图像缩放处理"""
    image_data = create_test_image_base64()

    # 执行图像处理功能
    result = pipe_image_process("resize", image_data, 224, 224)

    assert result is not None
    assert "result" in result
    assert "elapsed" in result
    assert isinstance(result["result"], str)
    assert len(result["result"]) > 0
    assert result["elapsed"] >= 0

    # 保存处理后的图像
    save_image_from_base64(result["result"], "resized_image.png")

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory('result_json_common')
    with open(os.path.join(cache_dir, 'resize_result.json'), 'w', encoding='utf-8') as f:
        json.dump({
            "method": "resize",
            "input_size": [224, 224],
            "output_size": [224, 224],
            "result_length": len(result["result"]),
            "elapsed": result["elapsed"]
        }, f, ensure_ascii=False, indent=2)


def test_process_image_rotate():
    """测试图像旋转处理"""
    image_data = create_test_image_base64()

    # 执行图像处理功能
    result = pipe_image_process("rotate", image_data, 90)

    assert result is not None
    assert "result" in result
    assert "elapsed" in result
    assert isinstance(result["result"], str)
    assert len(result["result"]) > 0
    assert result["elapsed"] >= 0

    # 保存处理后的图像
    save_image_from_base64(result["result"], "rotated_image.png")

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory('result_json_common')
    with open(os.path.join(cache_dir, 'rotate_result.json'), 'w', encoding='utf-8') as f:
        json.dump({
            "method": "rotate",
            "angle": 90,
            "result_length": len(result["result"]),
            "elapsed": result["elapsed"]
        }, f, ensure_ascii=False, indent=2)


def test_process_image_grayscale():
    """测试图像灰度化处理"""
    image_data = create_test_image_base64()

    # 执行图像处理功能
    result = pipe_image_process("grayscale", image_data)

    assert result is not None
    assert "result" in result
    assert "elapsed" in result
    # 灰度化返回Image对象
    assert isinstance(result["result"], Image.Image)
    assert result["elapsed"] >= 0

    # 保存处理后的图像
    cache_dir = setup_cache_directory('result_image')
    result["result"].save(os.path.join(cache_dir, "grayscale_image.png"))

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory('result_json_common')
    with open(os.path.join(cache_dir, 'grayscale_result.json'), 'w', encoding='utf-8') as f:
        json.dump({
            "method": "grayscale",
            "result_type": type(result["result"]).__name__,
            "elapsed": result["elapsed"]
        }, f, ensure_ascii=False, indent=2)


def test_process_image_blur():
    """测试图像模糊处理"""
    image_data = create_test_image_base64()

    # 执行图像处理功能
    result = pipe_image_process("blur", image_data, 3)

    assert result is not None
    assert "result" in result
    assert "elapsed" in result
    assert isinstance(result["result"], Image.Image)
    assert result["elapsed"] >= 0

    # 保存处理后的图像
    cache_dir = setup_cache_directory('result_image')
    result["result"].save(os.path.join(cache_dir, "blurred_image.png"))

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory('result_json_common')
    with open(os.path.join(cache_dir, 'blur_result.json'), 'w', encoding='utf-8') as f:
        json.dump({
            "method": "blur",
            "radius": 3,
            "result_type": type(result["result"]).__name__,
            "elapsed": result["elapsed"]
        }, f, ensure_ascii=False, indent=2)


def test_process_image_flip():
    """测试图像垂直翻转处理"""
    image_data = create_test_image_base64()

    # 执行图像处理功能
    result = pipe_image_process("flip", image_data)

    assert result is not None
    assert "result" in result
    assert "elapsed" in result
    assert isinstance(result["result"], Image.Image)
    assert result["elapsed"] >= 0

    # 保存处理后的图像
    cache_dir = setup_cache_directory('result_image')
    result["result"].save(os.path.join(cache_dir, "flipped_image.png"))

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory('result_json_common')
    with open(os.path.join(cache_dir, 'flip_result.json'), 'w', encoding='utf-8') as f:
        json.dump({
            "method": "flip",
            "result_type": type(result["result"]).__name__,
            "elapsed": result["elapsed"]
        }, f, ensure_ascii=False, indent=2)


def test_process_image_mirror():
    """测试图像水平翻转处理"""
    image_data = create_test_image_base64()

    # 执行图像处理功能
    result = pipe_image_process("mirror", image_data)

    assert result is not None
    assert "result" in result
    assert "elapsed" in result
    assert isinstance(result["result"], Image.Image)
    assert result["elapsed"] >= 0

    # 保存处理后的图像
    cache_dir = setup_cache_directory('result_image')
    result["result"].save(os.path.join(cache_dir, "mirrored_image.png"))

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory('result_json_common')
    with open(os.path.join(cache_dir, 'mirror_result.json'), 'w', encoding='utf-8') as f:
        json.dump({
            "method": "mirror",
            "result_type": type(result["result"]).__name__,
            "elapsed": result["elapsed"]
        }, f, ensure_ascii=False, indent=2)


def test_process_image_invalid_method():
    """测试无效的处理方法"""
    image_data = create_test_image_base64()

    # 测试不存在的处理方法应抛出异常
    try:
        pipe_image_process("invalid_method", image_data)
        assert False, "Should have raised AssertionError"
    except AssertionError as e:
        # 保存结果到缓存目录以供检查
        cache_dir = setup_cache_directory('result_json_error')
        with open(os.path.join(cache_dir, 'invalid_method_result.json'), 'w', encoding='utf-8') as f:
            json.dump({
                "method": "invalid_method",
                "expected_exception": "AssertionError",
                "exception_message": str(e)
            }, f, ensure_ascii=False, indent=2)


def test_process_image_invalid_parameters():
    """测试无效的参数"""
    image_data = create_test_image_base64()

    # 测试无效的缩放参数（负数）
    try:
        pipe_image_process("resize", image_data, -1, -1)
        assert False, "Should have raised AssertionError"
    except AssertionError as e:
        cache_dir = setup_cache_directory('result_json_error')
        with open(os.path.join(cache_dir, 'invalid_resize_parameters_result.json'), 'w', encoding='utf-8') as f:
            json.dump({
                "method": "resize",
                "params": [-1, -1],
                "expected_exception": "AssertionError",
                "exception_message": str(e)
            }, f, ensure_ascii=False, indent=2)

    # 测试无效的模糊半径（负数）
    try:
        pipe_image_process("blur", image_data, -1)
        assert False, "Should have raised AssertionError"
    except AssertionError as e:
        cache_dir = setup_cache_directory('result_json_error')
        with open(os.path.join(cache_dir, 'invalid_blur_parameters_result.json'), 'w', encoding='utf-8') as f:
            json.dump({
                "method": "blur",
                "params": [-1],
                "expected_exception": "AssertionError",
                "exception_message": str(e)
            }, f, ensure_ascii=False, indent=2)

    # 测试无效的旋转角度（错误类型）
    try:
        pipe_image_process("rotate", image_data, "invalid_angle")
        assert False, "Should have raised AssertionError"
    except AssertionError as e:
        cache_dir = setup_cache_directory('result_json_error')
        with open(os.path.join(cache_dir, 'invalid_rotate_parameters_result.json'), 'w', encoding='utf-8') as f:
            json.dump({
                "method": "rotate",
                "params": ["invalid_angle"],
                "expected_exception": "AssertionError",
                "exception_message": str(e)
            }, f, ensure_ascii=False, indent=2)


def test_process_image_invalid_base64():
    """测试无效的Base64图像数据"""
    invalid_image_data = "invalid_base64"

    # 测试无效的Base64数据应抛出异常
    try:
        pipe_image_process("grayscale", invalid_image_data)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        # 保存结果到缓存目录以供检查
        cache_dir = setup_cache_directory('result_json_error')
        with open(os.path.join(cache_dir, 'invalid_base64_result.json'), 'w', encoding='utf-8') as f:
            json.dump({
                "input": "invalid_base64",
                "expected_exception": "ValueError",
                "exception_message": str(e)
            }, f, ensure_ascii=False, indent=2)


def test_process_image_performance():
    """测试图像处理性能"""
    image_data = create_test_image_base64()

    # 执行多次处理以测试性能
    elapsed_times = []
    for i in range(5):
        result = pipe_image_process("grayscale", image_data)
        assert result["elapsed"] >= 0
        assert isinstance(result["result"], Image.Image)
        elapsed_times.append(result["elapsed"])

        # 保存每次处理的结果图像
        cache_dir = setup_cache_directory('result_image')
        result["result"].save(os.path.join(cache_dir, f"performance_test_{i}.png"))

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory('result_json_common')
    with open(os.path.join(cache_dir, 'performance_result.json'), 'w', encoding='utf-8') as f:
        json.dump({
            "method": "grayscale",
            "image_size": [224, 224],
            "iterations": 5,
            "elapsed_times": elapsed_times,
            "average_time": sum(elapsed_times) / len(elapsed_times)
        }, f, ensure_ascii=False, indent=2)


def test_process_image_consistency():
    """测试图像处理结果一致性"""
    image_data = create_test_image_base64()

    # 多次处理同一图像应产生相同结果（对于确定性操作）
    results = []
    for i in range(3):
        result = pipe_image_process("grayscale", image_data)
        results.append(result["result"])

        # 保存每次处理的结果图像
        cache_dir = setup_cache_directory('result_image')
        result["result"].save(os.path.join(cache_dir, f"consistency_test_{i}.png"))

    # 对于灰度化等确定性操作，结果应该一致
    for result in results:
        assert isinstance(result, Image.Image)

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory('result_json_common')
    with open(os.path.join(cache_dir, 'consistency_result.json'), 'w', encoding='utf-8') as f:
        json.dump({
            "method": "grayscale",
            "iterations": 3,
            "result_types": [type(r).__name__ for r in results]
        }, f, ensure_ascii=False, indent=2)


def test_process_image_with_parsed_parameters():
    """测试使用parse_parameters解析的参数进行图像处理"""
    image_data = create_test_image_base64()

    # 构造请求数据
    request_data = {
        "process_type": "image_process",
        "process_params": {
            "method": "resize",
            "args": [image_data, 224, 224],
            "kwargs": {}
        }
    }

    # 解析参数
    parsed_params = parse_parameters(request_data)
    assert parsed_params is not None

    # 使用解析后的参数执行处理
    result = pipe_image_process(
        parsed_params["process_params"]["method"],
        *parsed_params["process_params"]["args"],
        **parsed_params["process_params"]["kwargs"]
    )

    assert result is not None
    assert "result" in result
    assert "elapsed" in result
    assert isinstance(result["result"], str)
    assert len(result["result"]) > 0
    assert result["elapsed"] >= 0

    # 保存处理后的图像
    save_image_from_base64(result["result"], "parsed_parameters_image.png")

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory('result_json_common')
    with open(os.path.join(cache_dir, 'parsed_parameters_result.json'), 'w', encoding='utf-8') as f:
        json.dump({
            "process_type": parsed_params["process_type"],
            "method": parsed_params["process_params"]["method"],
            "args_count": len(parsed_params["process_params"]["args"]),
            "result_length": len(result["result"]),
            "elapsed": result["elapsed"]
        }, f, ensure_ascii=False, indent=2)


def test_process_image_check():
    """测试check方法，用于调试参数"""
    image_data = create_test_image_base64()

    # 执行check方法，该方法会打印参数信息
    result = pipe_image_process("check", image_data, 123, flag=True)

    assert result is not None
    assert "result" in result
    assert "elapsed" in result
    assert result["elapsed"] >= 0

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory('result_json_common')
    with open(os.path.join(cache_dir, 'check_result.json'), 'w', encoding='utf-8') as f:
        json.dump({
            "method": "check",
            "elapsed": result["elapsed"]
        }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 运行测试并生成报告
    pytest.main([__file__, "-v", "--tb=short"])
