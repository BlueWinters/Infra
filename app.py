# app.py
import logging
import os
from flask import Flask, request, jsonify, render_template
from core import do_process
from params import parse_parameters

# application
app = Flask(__name__, static_folder='static', template_folder='templates')
# config logging level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# make directories
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)


StatusMapping = {
    "success": {
        "status_code": 0,
        "message": "success",
    },
    "invalid_json": {
        "status_code": 4000,
        "message": "Invalid JSON Format"
    },
    "missing_user_id": {
        "status_code": 4001,
        "message": "Missing User Identity"
    },
    "missing_task_id": {
        "status_code": 4002,
        "message": "Missing Task Identity"
    },
    "missing_parameter": {
        "status_code": 4003,
        "message": "Missing Parameter"
    },
    #
    "unknown_error": {
        "status_code": 5000,
        "message": "Unknown Error"
    }
}


@app.route('/')
def index():
    """主页路由，返回图像处理页面"""
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        if not data:
            return jsonify(StatusMapping['invalid_json']), 400
        # extract parameters
        user_id = data.get("user_id")
        if not user_id:
            return jsonify(StatusMapping['missing_user_id']), 400
        task_id = data.get("task_id")
        if not task_id:
            return jsonify(StatusMapping['missing_task_id']), 400
        parameters = data.get("parameters")
        if not parameters:
            return jsonify(StatusMapping['missing_parameter']), 400
        # operation process
        format_params = parse_parameters(parameters)
        process_result = do_process(format_params)
        return jsonify(process_result), 200
    except Exception as e:
        logger.error("request failed: {}".format(str(e)))
        info = StatusMapping['unknown_error']
        info["message"] = str(e)
        return jsonify(info), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(StatusMapping['success'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

