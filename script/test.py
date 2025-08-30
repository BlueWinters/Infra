
import logging
import PIL.Image
import requests
import json
import time
import os
import base64
import io
from worker.params import *
from worker.params.decoder import decode_data_item

logging.basicConfig(level=logging.INFO)
BASE_URL = "http://localhost:5000"


def create_test_image_base64(image_path='asset/obama.png'):
    """创建测试图像并返回 Base64 编码"""
    # 检查图像文件是否存在
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            image_data = f.read()
        return base64.b64encode(image_data).decode('utf-8')
    raise FileNotFoundError(f"Image file '{image_path}' not found.")


def test_add_x_y():
    """测试图像模糊处理"""
    parameters = {
        "user_id": '007',
        "task": "tasks.algebra_add_x_y",
        'parameters': {
            "args": encode_list([100, 100]),
            "kwargs": {},
        },
    }

    response = requests.post(f"{BASE_URL}/process", json=parameters)
    response_data = response.json()
    print(response_data)
    return response_data['task_id']


def test_process_image():
    """测试图像模糊处理"""
    parameters = {
        "user_id": '007',
        "task": "tasks.process_image_resize",
        'parameters': {
            "args": encode_list([PIL.Image.open(R'X:\project\infra\asset\obama.png'), 100, 100]),
            "kwargs": {},
        },
    }

    response = requests.post(f"{BASE_URL}/process", json=parameters)
    response_data = response.json()
    print(response_data)
    return response_data['task_id']


def show_result(result):
    assert isinstance(result, dict), type(result)
    logging.info('elapsed ==> {}'.format(result['elapsed']))
    logging.info('finish_time ==> {}'.format(result['finish_time']))
    output = result['output']
    decoded = decode_data_item(output)
    if isinstance(decoded, PIL.Image.Image):
        logging.info("图像处理成功 ==> 展示图像")
        decoded.show()
    else:
        logging.info("数据处理成功 ==> {}".format(decoded))


def query_task_status(task_id):
    """查询任务状态"""
    url = f"{BASE_URL}/status/{task_id}"

    response = requests.get(url)
    data = response.json()
    logging.info(f"任务状态: {url} ==> {data['state']}")
    if data['state'] == 'SUCCESS':
        logging.info("任务成功")
        show_result(data['result'])
    elif data['state'] == 'FAILURE':
        logging.error("任务失败:")
        logging.error(data['state'])
        logging.error(data['error'])
        logging.error(data['traceback'])
    else:
        logging.info("任务处理中，等待...")
        time.sleep(1)  # 每秒查询一次


if __name__ == "__main__":
    task_id1 = test_add_x_y()
    time.sleep(2)
    query_task_status(task_id1)

    task_id2 = test_process_image()
    time.sleep(2)
    query_task_status(task_id2)
