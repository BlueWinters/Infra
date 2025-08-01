
from .image_process import pipe_image_process
from .text_process import pipe_text_process
from .video_process import pipe_video_process


ProcessMapping = {
    "image_process": pipe_image_process,
    "text_process": pipe_text_process,
    "video_process": pipe_video_process,
}


def do_process(parameters):
    process_type = parameters.get("process_type")
    process_params = parameters.get('process_params')
    return ProcessMapping[process_type](
        process_params['method'],
        *process_params['args'],
        **process_params['kwargs'])
