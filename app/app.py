# app.py
import redis
import flask
import celery
import copy
from config import *

# flask app
app_flask = flask.Flask(__name__)
app = app_flask
logger = app_flask.logger
# celery app
app_celery = celery.Celery(
    'tasks',
    broker=f'redis://{REDIS_HOST}:6379/0',
    backend=f'redis://@{REDIS_HOST}:6379/1',
    # others
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    result_expires=3600,
    # broker_connection_retry_on_startup=True,
)


# check connect to redis
try:
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
    )
    r.ping()
    app_flask.logger.info("Redis connect success")
except Exception as e:
    app_flask.logger.error(f"Redis connect fail: {e}")
    raise


StatusMapping = {
    "success": {
        "status_code": 0,
        "message": "success",
    },
    "task_submitted": {
        "status_code": 202,
        "message": "Task submitted successfully",
        "task_id": ""
    },
    "task_result": {
        "status_code": 200,
        "message": "",
        "result": ""
    },
    "task_pending": {
        "status_code": 100,
        "message": "Task is waiting to be processed"
    },
    "task_failure": {
        "status_code": 5001,
        "message": "Task execution failed",
        "error": ""
    },
    "submitted_error": {
        "status_code": 5002,
        "message": "Task submitted successfully failed",
        "error": ""
    }
}


def logging_function(level, *args, **kwargs):
    if level == 'debug':
        logger.debug(*args, **kwargs)
    elif level == 'info':
        logger.info(*args, **kwargs)
    elif level == 'info':
        logger.warning(*args, **kwargs)
    elif level == 'error':
        logger.error(*args, **kwargs)
    elif level == 'critical':
        logger.critical(*args, **kwargs)
    raise NotImplemented("Not implemented logging level")


@app_flask.route('/')
def index():
    return '<h1>Flask + Redis + Celery</h1><p><a href="/process">点击触发图像处理</a></p>'


@app_flask.route('/process', methods=['POST'])
def process():
    try:
        data = flask.request.get_json()
        verbose = data.get('verbose', None)
        if isinstance(verbose, str):
            logging_function(verbose, data)

        parameters = data.get('parameters', None)
        assert isinstance(parameters, dict), "parameters must be a dict"
        task = app_celery.send_task(
            data['task'],
            kwargs={'parameters': parameters}
        )
        response = copy.deepcopy(StatusMapping['task_submitted'])
        response["task_id"] = task.id  # 返回任务ID，供客户端轮询结果
        return flask.jsonify(response), 202
    except Exception as e:
        logger.error("task submitted failed, {}".format(str(e)))
        info = copy.deepcopy(StatusMapping['submitted_error'])
        info["error"] = str(e)
        return flask.jsonify(info), 500


@app_flask.route('/status/<task_id>')
def check_task_status(task_id):
    try:
        task = app_celery.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                "state": task.state,
                "status": "Task is waiting to be processed"
            }
        elif task.state == 'SUCCESS':
            response = {
                "state": task.state,
                "result": task.result
            }
        elif task.state == 'FAILURE':
            response = {
                "state": task.state,
                "error": str(task.info),  # 错误信息
                "traceback": task.traceback  # 详细堆栈
            }
        else:
            response = {
                "state": task.state,
                "status": str(task.info)
            }
        return flask.jsonify(response)
    except Exception as e:
        return flask.jsonify({
            "task_id": task_id,
            "error": str(e),
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

