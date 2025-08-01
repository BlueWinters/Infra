
import pytest
import base64
import os
import json
from io import BytesIO
from PIL import Image
from params import parse_parameters, RequestParams, ProcessParams, decode_data_item


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


def setup_cache_directory():
    """创建缓存目录用于保存测试结果"""
    cache_dir = 'cache/tests/test_params'
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def test_params_valid_image_process_request():
    """测试有效的图像处理请求解析"""
    # 创建测试图像数据
    image_data = create_test_image_base64()

    # 构造有效的请求数据
    request_data = {
        "process_type": "image_process",
        "process_params": {
            "method": "resize",
            "args": [image_data],
            "kwargs": {
                "width": 224,
                "height": 224
            }
        }
    }

    # 解析参数
    result = parse_parameters(request_data)

    # 验证结果
    assert result is not None
    assert isinstance(result, dict)
    assert result["process_type"] == "image_process"
    assert result["process_params"]["method"] == "resize"
    assert len(result["process_params"]["args"]) == 1
    assert result["process_params"]["kwargs"]["width"] == 224
    assert result["process_params"]["kwargs"]["height"] == 224

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory()
    with open(os.path.join(cache_dir, 'valid_request_result.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def test_params_valid_grayscale_request():
    """测试有效的灰度化处理请求解析"""
    image_data = create_test_image_base64()

    request_data = {
        "process_type": "image_process",
        "process_params": {
            "method": "grayscale",
            "args": [image_data],
            "kwargs": {}
        }
    }

    result = parse_parameters(request_data)

    assert result is not None
    assert result["process_type"] == "image_process"
    assert result["process_params"]["method"] == "grayscale"
    assert len(result["process_params"]["args"]) == 1

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory()
    with open(os.path.join(cache_dir, 'grayscale_request_result.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def test_params_valid_blur_request():
    """测试有效的模糊处理请求解析"""
    image_data = create_test_image_base64()

    request_data = {
        "process_type": "image_process",
        "process_params": {
            "method": "blur",
            "args": [image_data, 5],  # 图像和模糊半径
            "kwargs": {}
        }
    }

    result = parse_parameters(request_data)

    assert result is not None
    assert result["process_type"] == "image_process"
    assert result["process_params"]["method"] == "blur"
    assert len(result["process_params"]["args"]) == 2
    assert result["process_params"]["args"][1] == 5

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory()
    with open(os.path.join(cache_dir, 'blur_request_result.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def test_params_invalid_process_type():
    """测试无效的处理类型"""
    image_data = create_test_image_base64()

    request_data = {
        "process_type": "invalid_process_type",
        "process_params": {
            "method": "resize",
            "args": [image_data],
            "kwargs": {
                "width": 224,
                "height": 224
            }
        }
    }

    result = parse_parameters(request_data)

    # 无效的处理类型应该返回 None
    assert result is None

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory()
    with open(os.path.join(cache_dir, 'invalid_process_type_result.json'), 'w', encoding='utf-8') as f:
        json.dump({"result": result}, f, ensure_ascii=False, indent=2)


def test_params_missing_required_fields():
    """测试缺少必需字段的请求"""
    request_data = {
        "process_type": "image_process"
        # 缺少 process_params
    }

    result = parse_parameters(request_data)

    # 缺少必需字段应该返回 None
    assert result is None

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory()
    with open(os.path.join(cache_dir, 'missing_fields_result.json'), 'w', encoding='utf-8') as f:
        json.dump({"result": result}, f, ensure_ascii=False, indent=2)


def test_params_invalid_base64_image():
    """测试无效的Base64图像数据"""
    request_data = {
        "process_type": "image_process",
        "process_params": {
            "method": "resize",
            "args": ["invalid_base64_string"],
            "kwargs": {
                "width": 224,
                "height": 224
            }
        }
    }

    result = parse_parameters(request_data)

    # 解析应该成功（参数验证在后续处理阶段进行）
    assert result is not None
    assert result["process_params"]["args"][0] == "invalid_base64_string"

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory()
    with open(os.path.join(cache_dir, 'invalid_base64_result.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def test_request_params_model_validation():
    """测试 RequestParams 模型的验证功能"""
    image_data = create_test_image_base64()

    # 测试有效的模型创建
    process_params = ProcessParams(
        method="resize",
        args=[image_data],
        kwargs={"width": 224, "height": 224}
    )

    request_params = RequestParams(
        process_type="image_process",
        process_params=process_params
    )

    assert request_params.process_type == "image_process"
    assert request_params.process_params.method == "resize"

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory()
    with open(os.path.join(cache_dir, 'model_validation_result.json'), 'w', encoding='utf-8') as f:
        json.dump({
            "process_type": request_params.process_type,
            "method": request_params.process_params.method
        }, f, ensure_ascii=False, indent=2)


def test_params_complex_request_with_multiple_args():
    """测试包含多个参数的复杂请求解析"""
    image_data = create_test_image_base64()

    request_data = {
        "process_type": "image_process",
        "process_params": {
            "method": "rotate",
            "args": [image_data, 45],  # 图像和角度
            "kwargs": {
                "expand": True
            }
        }
    }

    result = parse_parameters(request_data)

    assert result is not None
    assert result["process_type"] == "image_process"
    assert result["process_params"]["method"] == "rotate"
    assert len(result["process_params"]["args"]) == 2
    assert result["process_params"]["args"][1] == 45
    assert result["process_params"]["kwargs"]["expand"] is True

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory()
    with open(os.path.join(cache_dir, 'complex_request_result.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def test_params_request_with_primitive_types():
    """测试包含基本类型的参数解析"""
    request_data = {
        "process_type": "text_process",
        "process_params": {
            "method": "process_text",
            "args": ["Hello, World!", 123],
            "kwargs": {
                "flag": True,
                "threshold": 0.95,
                "name": "test"
            }
        }
    }

    result = parse_parameters(request_data)

    assert result is not None
    assert result["process_type"] == "text_process"
    assert result["process_params"]["method"] == "process_text"
    assert len(result["process_params"]["args"]) == 2
    assert result["process_params"]["args"][0] == "Hello, World!"
    assert result["process_params"]["args"][1] == 123
    assert result["process_params"]["kwargs"]["flag"] is True
    assert result["process_params"]["kwargs"]["threshold"] == 0.95
    assert result["process_params"]["kwargs"]["name"] == "test"

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory()
    with open(os.path.join(cache_dir, 'primitive_types_result.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def test_decode_data_item_functionality():
    """测试 decode_data_item 函数的功能"""
    # 测试字符串类型
    string_item = {"type": "string", "data": "test_string"}
    decoded = decode_data_item(string_item)
    assert decoded == "test_string"

    # 测试整数类型
    int_item = {"type": "int", "data": 42}
    decoded = decode_data_item(int_item)
    assert decoded == 42

    # 测试浮点数类型
    float_item = {"type": "float", "data": 3.14}
    decoded = decode_data_item(float_item)
    assert decoded == 3.14

    # 测试布尔类型
    bool_item = {"type": "bool", "data": True}
    decoded = decode_data_item(bool_item)
    assert decoded is True

    # 测试列表类型
    list_item = {
        "type": "list",
        "data": [
            {"type": "int", "data": 1},
            {"type": "int", "data": 2},
            {"type": "int", "data": 3}
        ]
    }
    decoded = decode_data_item(list_item)
    assert decoded == [1, 2, 3]

    # 测试字典类型
    dict_item = {
        "type": "dict",
        "data": {
            "key1": {"type": "string", "data": "value1"},
            "key2": {"type": "int", "data": 42}
        }
    }
    decoded = decode_data_item(dict_item)
    assert decoded == {"key1": "value1", "key2": 42}

    # 保存结果到缓存目录以供检查
    cache_dir = setup_cache_directory()
    test_results = {
        "string": "test_string",
        "int": 42,
        "float": 3.14,
        "bool": True,
        "list": [1, 2, 3],
        "dict": {"key1": "value1", "key2": 42}
    }
    with open(os.path.join(cache_dir, 'decode_data_item_result.json'), 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 运行测试并生成报告
    pytest.main([__file__, "-v", "--tb=short"])