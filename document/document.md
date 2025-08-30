

## 请求格式
```json
{
    "user_id": 123,
    "task_id": 456,
    "parameters": {
        "process_type": "image_process",
        "process_params": {
            "method": "method_name",
            "args": [
                {
                    "type": "image",
                    "data": "image_bytes"
                },
                {
                    "type": "string",
                    "data": "string_data"
                },
                {
                    "type": "int",
                    "data": 123
                }
            ],
            "kwargs": {
                "key_name1": {
                    "type": "image",
                    "data": "image_bytes"
                },
                "key_name2": {
                    "type": "string",
                    "data": "string_data"
                },
                "key_name3": {
                    "type": "float",
                    "data": 0.123456
                },
                "key_name4": {
                    "type": "int",
                    "data": 123456
                }
            }
        },
        "process_target": [
            "process_target_name1",
            "process_target_name2"
        ]
    }
}
```

- Resize
```json
{
    "user_id": 123,
    "task_id": 456,
    "parameters": {
        "process_type": "image_process",
        "process_params": {
            "method": "resize",
            "args": [],
            "kwargs": {
                "image": "image_bytes_to_base64",
                "height": 10,
                "width": 10
            }
        }
    }
}
```