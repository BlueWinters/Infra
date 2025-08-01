# tests/test_benchmark.py
import pytest
import requests
import json
import time
import os
from PIL import Image
import base64
from io import BytesIO

# Flask应用的URL
BASE_URL = "http://localhost:5000"


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
    cache_dir = os.path.join('cache/benchmark/app', subdir)
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


class TestBenchmark:
    """基准测试类"""

    def setup_class(self):
        """在测试类开始前执行"""
        self.image_data = create_test_image_base64()
        self.user_id = 1001
        self.task_id = "task_001"

    def test_health_check(self):
        """测试健康检查接口"""
        start_time = time.perf_counter()
        response = requests.get(f"{BASE_URL}/health")
        end_time = time.perf_counter()

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status_code"] == 0
        assert response_data["message"] == "success"

        # 保存结果到通用JSON目录
        cache_dir = setup_cache_directory('result_common_json')
        elapsed_time = end_time - start_time
        result_data = {
            "endpoint": "/health",
            "status_code": response.status_code,
            "response_time": elapsed_time,
            "response": response_data,
            "user_id": self.user_id,
            "task_id": self.task_id
        }

        with open(os.path.join(cache_dir, 'health_check_result.json'), 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

    def test_index_endpoint(self):
        """测试根路径接口"""
        start_time = time.perf_counter()
        response = requests.get(f"{BASE_URL}/")
        end_time = time.perf_counter()

        assert response.status_code == 200
        # 根路径返回HTML页面，不需要检查JSON结构

        # 保存结果到通用JSON目录
        cache_dir = setup_cache_directory('result_common_json')
        elapsed_time = end_time - start_time
        result_data = {
            "endpoint": "/",
            "status_code": response.status_code,
            "response_time": elapsed_time,
            "content_type": response.headers.get('content-type'),
            "user_id": self.user_id,
            "task_id": self.task_id
        }

        with open(os.path.join(cache_dir, 'index_result.json'), 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

    def test_image_resize_process(self):
        """测试图像缩放处理"""
        payload = {
            "user_id": self.user_id,
            "task_id": self.task_id,
            "parameters": {
                "process_type": "image_process",
                "process_params": {
                    "method": "resize",
                    "args": [self.image_data, 224, 224],
                    "kwargs": {}
                }
            }
        }

        start_time = time.perf_counter()
        response = requests.post(f"{BASE_URL}/process", json=payload)
        end_time = time.perf_counter()

        assert response.status_code == 200
        response_data = response.json()
        assert "result" in response_data
        assert "elapsed" in response_data

        # 保存结果到通用JSON目录
        cache_dir = setup_cache_directory('result_common_json')
        elapsed_time = end_time - start_time
        result_data = {
            "endpoint": "/process",
            "method": "resize",
            "status_code": response.status_code,
            "total_response_time": elapsed_time,
            "process_time": response_data["elapsed"],
            "result_length": len(response_data["result"]) if isinstance(response_data["result"], str) else "N/A",
            "user_id": self.user_id,
            "task_id": self.task_id
        }

        with open(os.path.join(cache_dir, 'image_resize_result.json'), 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        # 保存处理后的图像到通用图像目录
        cache_dir = setup_cache_directory('result_common_image')
        if isinstance(response_data["result"], str):
            image_data = base64.b64decode(response_data["result"])
            with open(os.path.join(cache_dir, 'resized_image_output.png'), 'wb') as f:
                f.write(image_data)

    def test_image_grayscale_process(self):
        """测试图像灰度化处理"""
        payload = {
            "user_id": self.user_id,
            "task_id": self.task_id,
            "parameters": {
                "process_type": "image_process",
                "process_params": {
                    "method": "grayscale",
                    "args": [self.image_data],
                    "kwargs": {}
                }
            }
        }

        start_time = time.perf_counter()
        response = requests.post(f"{BASE_URL}/process", json=payload)
        end_time = time.perf_counter()

        assert response.status_code == 200
        response_data = response.json()
        assert "result" in response_data
        assert "elapsed" in response_data

        # 保存结果到通用JSON目录
        cache_dir = setup_cache_directory('result_common_json')
        elapsed_time = end_time - start_time
        result_data = {
            "endpoint": "/process",
            "method": "grayscale",
            "status_code": response.status_code,
            "total_response_time": elapsed_time,
            "process_time": response_data["elapsed"],
            "user_id": self.user_id,
            "task_id": self.task_id
        }

        with open(os.path.join(cache_dir, 'image_grayscale_result.json'), 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        # 保存处理后的图像到通用图像目录
        cache_dir = setup_cache_directory('result_common_image')
        if isinstance(response_data["result"], str):
            image_data = base64.b64decode(response_data["result"])
            with open(os.path.join(cache_dir, 'grayscale_image_output.png'), 'wb') as f:
                f.write(image_data)

    def test_image_blur_process(self):
        """测试图像模糊处理"""
        payload = {
            "user_id": self.user_id,
            "task_id": self.task_id,
            "parameters": {
                "process_type": "image_process",
                "process_params": {
                    "method": "blur",
                    "args": [self.image_data, 3],
                    "kwargs": {}
                }
            }
        }

        start_time = time.perf_counter()
        response = requests.post(f"{BASE_URL}/process", json=payload)
        end_time = time.perf_counter()

        assert response.status_code == 200
        response_data = response.json()
        assert "result" in response_data
        assert "elapsed" in response_data

        # 保存结果到通用JSON目录
        cache_dir = setup_cache_directory('result_common_json')
        elapsed_time = end_time - start_time
        result_data = {
            "endpoint": "/process",
            "method": "blur",
            "status_code": response.status_code,
            "total_response_time": elapsed_time,
            "process_time": response_data["elapsed"],
            "user_id": self.user_id,
            "task_id": self.task_id
        }

        with open(os.path.join(cache_dir, 'image_blur_result.json'), 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        # 保存处理后的图像到通用图像目录
        cache_dir = setup_cache_directory('result_common_image')
        if isinstance(response_data["result"], str):
            image_data = base64.b64decode(response_data["result"])
            with open(os.path.join(cache_dir, 'blur_image_output.png'), 'wb') as f:
                f.write(image_data)

    def test_invalid_method_process(self):
        """测试无效方法处理"""
        payload = {
            "user_id": self.user_id,
            "task_id": self.task_id,
            "parameters": {
                "process_type": "image_process",
                "process_params": {
                    "method": "invalid_method",
                    "args": [self.image_data],
                    "kwargs": {}
                }
            }
        }

        start_time = time.perf_counter()
        response = requests.post(f"{BASE_URL}/process", json=payload)
        end_time = time.perf_counter()

        # 应该返回500错误，因为后端会抛出AssertionError
        assert response.status_code == 500

        # 保存结果到错误JSON目录
        cache_dir = setup_cache_directory('result_error_json')
        elapsed_time = end_time - start_time
        result_data = {
            "endpoint": "/process",
            "method": "invalid_method",
            "status_code": response.status_code,
            "response_time": elapsed_time,
            "error": response.json(),
            "user_id": self.user_id,
            "task_id": self.task_id
        }

        with open(os.path.join(cache_dir, 'invalid_method_result.json'), 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

    def test_missing_user_id(self):
        """测试缺少user_id的情况"""
        payload = {
            "task_id": self.task_id,
            "parameters": {
                "process_type": "image_process",
                "process_params": {
                    "method": "resize",
                    "args": [self.image_data, 224, 224],
                    "kwargs": {}
                }
            }
        }

        start_time = time.perf_counter()
        response = requests.post(f"{BASE_URL}/process", json=payload)
        end_time = time.perf_counter()

        # 应该返回400错误，缺少user_id
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["status_code"] == 4001
        assert response_data["message"] == "Missing User Identity"

        # 保存结果到错误JSON目录
        cache_dir = setup_cache_directory('result_error_json')
        elapsed_time = end_time - start_time
        result_data = {
            "endpoint": "/process",
            "error_type": "missing_user_id",
            "status_code": response.status_code,
            "response_time": elapsed_time,
            "response": response_data,
            "user_id": "missing",
            "task_id": self.task_id
        }

        with open(os.path.join(cache_dir, 'missing_user_id_result.json'), 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

    def test_missing_task_id(self):
        """测试缺少task_id的情况"""
        payload = {
            "user_id": self.user_id,
            "parameters": {
                "process_type": "image_process",
                "process_params": {
                    "method": "resize",
                    "args": [self.image_data, 224, 224],
                    "kwargs": {}
                }
            }
        }

        start_time = time.perf_counter()
        response = requests.post(f"{BASE_URL}/process", json=payload)
        end_time = time.perf_counter()

        # 应该返回400错误，缺少task_id
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["status_code"] == 4002
        assert response_data["message"] == "Missing Task Identity"

        # 保存结果到错误JSON目录
        cache_dir = setup_cache_directory('result_error_json')
        elapsed_time = end_time - start_time
        result_data = {
            "endpoint": "/process",
            "error_type": "missing_task_id",
            "status_code": response.status_code,
            "response_time": elapsed_time,
            "response": response_data,
            "user_id": self.user_id,
            "task_id": "missing"
        }

        with open(os.path.join(cache_dir, 'missing_task_id_result.json'), 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

    def test_concurrent_requests(self):
        """测试并发请求处理"""
        payloads = [
            {
                "user_id": self.user_id,
                "task_id": f"{self.task_id}_resize",
                "parameters": {
                    "process_type": "image_process",
                    "process_params": {
                        "method": "resize",
                        "args": [self.image_data, 100, 100],
                        "kwargs": {}
                    }
                }
            },
            {
                "user_id": self.user_id,
                "task_id": f"{self.task_id}_grayscale",
                "parameters": {
                    "process_type": "image_process",
                    "process_params": {
                        "method": "grayscale",
                        "args": [self.image_data],
                        "kwargs": {}
                    }
                }
            },
            {
                "user_id": self.user_id,
                "task_id": f"{self.task_id}_blur",
                "parameters": {
                    "process_type": "image_process",
                    "process_params": {
                        "method": "blur",
                        "args": [self.image_data, 2],
                        "kwargs": {}
                    }
                }
            }
        ]

        start_time = time.perf_counter()

        # 发送并发请求
        responses = []
        for payload in payloads:
            response = requests.post(f"{BASE_URL}/process", json=payload)
            responses.append(response)

        end_time = time.perf_counter()

        # 验证所有响应
        for response in responses:
            assert response.status_code == 200
            response_data = response.json()
            assert "result" in response_data
            assert "elapsed" in response_data

        # 保存结果到通用JSON目录
        cache_dir = setup_cache_directory('result_common_json')
        total_elapsed_time = end_time - start_time
        result_data = {
            "endpoint": "/process",
            "concurrent_requests": len(payloads),
            "total_time": total_elapsed_time,
            "average_time_per_request": total_elapsed_time / len(payloads),
            "individual_results": [],
            "user_id": self.user_id,
            "task_id": self.task_id
        }

        for i, response in enumerate(responses):
            response_data = response.json()
            result_data["individual_results"].append({
                "request": i + 1,
                "process_time": response_data["elapsed"],
                "method": payloads[i]["parameters"]["process_params"]["method"],
                "task_id": payloads[i]["task_id"]
            })

        with open(os.path.join(cache_dir, 'concurrent_requests_result.json'), 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        # 保存处理后的图像到通用图像目录
        cache_dir = setup_cache_directory('result_common_image')
        for i, response in enumerate(responses):
            response_data = response.json()
            if isinstance(response_data["result"], str):
                image_data = base64.b64decode(response_data["result"])
                with open(os.path.join(cache_dir, f'concurrent_test_{i}_output.png'), 'wb') as f:
                    f.write(image_data)

    def test_large_image_performance(self):
        """测试大图像处理性能"""
        # 创建大图像
        large_image = create_test_image_base64()

        payload = {
            "user_id": self.user_id,
            "task_id": f"{self.task_id}_large",
            "parameters": {
                "process_type": "image_process",
                "process_params": {
                    "method": "resize",
                    "args": [large_image, 224, 224],
                    "kwargs": {}
                }
            }
        }

        start_time = time.perf_counter()
        response = requests.post(f"{BASE_URL}/process", json=payload)
        end_time = time.perf_counter()

        assert response.status_code == 200
        response_data = response.json()
        assert "result" in response_data
        assert "elapsed" in response_data

        # 保存结果到通用JSON目录
        cache_dir = setup_cache_directory('result_common_json')
        elapsed_time = end_time - start_time
        result_data = {
            "endpoint": "/process",
            "method": "resize",
            "input_size": "800x800",
            "output_size": "224x224",
            "status_code": response.status_code,
            "total_response_time": elapsed_time,
            "process_time": response_data["elapsed"],
            "user_id": self.user_id,
            "task_id": f"{self.task_id}_large"
        }

        with open(os.path.join(cache_dir, 'large_image_performance_result.json'), 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        # 保存处理后的图像到通用图像目录
        cache_dir = setup_cache_directory('result_common_image')
        if isinstance(response_data["result"], str):
            image_data = base64.b64decode(response_data["result"])
            with open(os.path.join(cache_dir, 'large_image_output.png'), 'wb') as f:
                f.write(image_data)


if __name__ == "__main__":
    import sys
    # 检查是否需要生成覆盖率报告
    if "--cov" in sys.argv:
        # 运行带覆盖率的测试
        pytest.main([
            __file__,
            "-v",
            "--tb=short",
            "--cov=core",
            "--cov-report=term-missing",
            "--cov-report=html:cache/benchmark/app/coverage_report"
        ])
    else:
        # 运行普通测试
        pytest.main([__file__, "-v", "--tb=short"])
