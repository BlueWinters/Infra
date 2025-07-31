
import logging
import base64
import numpy as np
from pydantic import BaseModel, Field, ValidationError
from typing import Union, Dict, List, Any, Optional

# 基础类型
Primitive = Union[str, int, float, bool, None]

# 允许嵌套的字典和列表（JSON 兼容结构）
JsonType = Union[Primitive, List[Any], Dict[str, Any]]


class DataItemNdarray(BaseModel):
    type: str = 'ndarray'
    shape: List[int]
    dtype: str
    data: str  # base64 编码的字符串

    @property
    def array(self) -> np.ndarray:
        return np.frombuffer(base64.b64decode(self.data), dtype=self.dtype).reshape(self.shape)

    @classmethod
    def from_array(cls, arr: np.ndarray):
        import base64
        return cls(
            shape=list(arr.shape),
            dtype=str(arr.dtype),
            data=base64.b64encode(arr.tobytes()).decode('utf-8')
        )


class ProcessParams(BaseModel):
    method: str
    args: List[JsonType] = Field(default_factory=list)  # 支持原始类型
    kwargs: Dict[str, JsonType] = Field(default_factory=dict)  # 支持原始类型


class RequestParams(BaseModel):
    process_type: str
    process_params: ProcessParams

    @classmethod
    def validate_process_type(cls, v):
        allowed = ['image_process', 'text_process', 'video_process']
        if v not in allowed:
            raise ValueError(f"must be one of {allowed}")
        return v


# 在接口中使用
def decode_data_item(item: Any) -> Any:
    """
    递归地将 DataItem 对象还原为原始值
    """
    if isinstance(item, dict):
        # 检查是否是包装类型
        item_type = item.get("type")

        if item_type == "string":
            return item["data"]
        elif item_type == "int":
            return item["data"]
        elif item_type == "float":
            return item["data"]
        elif item_type == "bool":
            return item["data"]
        elif item_type == "byte":
            data_b64 = item["data"]
            return base64.b64decode(data_b64)
        elif item_type == "ndarray":
            data_b64 = item["data"]
            dtype = np.dtype(item["dtype"])
            data_bytes = base64.b64decode(data_b64)
            arr = np.frombuffer(data_bytes, dtype=dtype)
            return arr.reshape(item["shape"])
        elif item_type == "list":
            return [decode_data_item(x) for x in item["data"]]
        elif item_type == "tuple":
            return tuple(decode_data_item(x) for x in item["data"])
        elif item_type == "dict":
            return {k: decode_data_item(v) for k, v in item["data"].items()}
        else:
            # 不认识的 type，尝试原样返回 data 或整体
            return item.get("data", item)
    elif isinstance(item, list):
        return [decode_data_item(x) for x in item]
    elif isinstance(item, (str, int, float, bool, type(None))):
        return item
    else:
        return item


def parse_parameters(request_json: Dict, verbose=True) -> Union[Dict[str, Any], None]:
    """
    验证并解析请求参数，将 args/kwargs 还原为可直接调用的值
    """
    try:
        # 1. 使用 Pydantic 验证结构
        validated_data = RequestParams(**request_json)

        # 2. 提取 process_params
        params = validated_data.process_params

        # 3. 解包 args 和 kwargs
        raw_args = []
        for arg in params.args or []:
            raw_args.append(decode_data_item(arg))

        raw_kwargs = {}
        for key, value in (params.kwargs or {}).items():
            raw_kwargs[key] = decode_data_item(value)

        # if verbose is True:
        #     import pprint
        #     pprint.pprint(raw_args)
        #     pprint.pprint(raw_kwargs)

        # 4. 返回可用于函数调用的字典
        return {
            "process_type": validated_data.process_type,
            "process_params": {
                "method": params.method,
                "args": raw_args,
                "kwargs": raw_kwargs
            }
        }

    except ValidationError as e:
        logging.error("validation Error:", e)
        return None


