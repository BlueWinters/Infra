
import time
import celery
import logging
import traceback
from config import *
from params import *
from algebra import pipe_add_x_y, pipe_sub_x_y
from image_process import Processors


app_celery = celery.Celery(
    'core',
    broker=f'redis://{REDIS_HOST}:6379/0',
    backend=f'redis://@{REDIS_HOST}:6379/1',
    # others
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    result_expires=3600,
)

app_celery.autodiscover_tasks()


def check_celery_broker():
    try:
        with app_celery.connection() as conn:
            conn.ensure_connection(max_retries=3)
            print("Broker连接成功")
            return True
    except Exception as e:
        print(f"Broker connect failed: {e}")
        return False


def check_celery_backend():
    try:
        result = app_celery.AsyncResult("non-existent-id")
        print("Backend连接成功")
        return True
    except Exception as e:
        print(f"Backend connect failed: {e}")
        return False


@app_celery.task
def algebra_add_x_y(parameters: dict):
    try:
        format_params = decode_data(parameters)
        time_beg = time.perf_counter()
        result = pipe_add_x_y(*format_params['args'], **format_params['kwargs'])
        time_end = time.perf_counter()
        return {
            'output': encode_data(result),
            'elapsed': round(time_end-time_beg, 4),
            'finish_time': time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception as e:
        logging.error(f"task-{parameters.get('task_id')} failed: {e}")
        error_info = {
            "status": "failed",
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        return error_info


@app_celery.task
def algebra_sub_x_y(parameters: dict):
    try:
        format_params = decode_data(parameters)
        time_beg = time.perf_counter()
        result = pipe_sub_x_y(*format_params['args'], **format_params['kwargs'])
        time_end = time.perf_counter()
        return {
            'output': encode_data(result),
            'elapsed': round(time_end-time_beg, 4),
            'finish_time': time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception as e:
        logging.error(f"task-{parameters.get('task_id')} failed: {e}")
        raise


@app_celery.task
def process_image_resize(parameters: dict):
    try:
        format_params = decode_data(parameters)
        time_beg = time.perf_counter()
        result = Processors['resize'](
            *format_params['args'],
            **format_params['kwargs'],
        )
        time_end = time.perf_counter()

        return {
            'output': encode_data(result),
            'elapsed': round(time_end-time_beg, 4),
            'finish_time': time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception as e:
        logging.error(f"task-{parameters.get('task_id')} failed: {e}")
        raise
