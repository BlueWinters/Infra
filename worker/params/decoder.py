
import logging
import base64
import numpy as np
import io
from PIL import Image
from pydantic import BaseModel, Field
from typing import Union, Dict, List, Any, Optional


# 基础类型
Primitive = Union[str, int, float, bool, None]

# 允许嵌套的字典和列表（JSON兼容结构）
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
    args: List[JsonType] = Field(default_factory=list)  # 支持原始类型
    kwargs: Dict[str, JsonType] = Field(default_factory=dict)  # 支持原始类型


# 在接口中使用
def decode_data_item(item: Any) -> Any:
    """
    递归地将 DataItem对象还原为原始值
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
        elif item_type == "bytes":
            data_b64 = item["data"]
            return base64.b64decode(data_b64)
        elif item_type == "ndarray":
            data_b64 = item["data"]
            dtype = np.dtype(item["dtype"])
            data_bytes = base64.b64decode(data_b64)
            arr = np.frombuffer(data_bytes, dtype=dtype)
            return arr.reshape(item["shape"])
        elif item_type == "image_bytes":
            image_bytes = base64.b64decode(item["data"])
            image = Image.open(io.BytesIO(image_bytes))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        elif item_type == "list":
            return [decode_data_item(x) for x in item["data"]]
        elif item_type == "tuple":
            return tuple(decode_data_item(x) for x in item["data"])
        elif item_type == "dict":
            return {k: decode_data_item(v) for k, v in item["data"].items()}
        else:
            # 不认识的 type，尝试原样返回data或整体
            return item.get("data", item)
    elif isinstance(item, list):
        return [decode_data_item(x) for x in item]
    elif isinstance(item, (str, int, float, bool, type(None))):
        return item
    else:
        return item


def decode_data(parameters: dict) -> Union[Dict[str, Any], None]:
    """
    验证并解析请求参数，将args/kwargs还原为可直接调用的值
    """
    try:
        # 使用Pydantic验证结构
        params = ProcessParams(
            args=parameters.get('args', []),
            kwargs=parameters.get('kwargs', {}))

        # 解包args和kwargs
        raw_args = []
        for arg in params.args or []:
            raw_args.append(decode_data_item(arg))

        raw_kwargs = {}
        for key, value in (params.kwargs or {}).items():
            raw_kwargs[key] = decode_data_item(value)

        # 返回可用于函数调用的字典
        return {
            "args": raw_args,
            "kwargs": raw_kwargs
        }

    except Exception as e:
        logging.error("parse parameters error: {}".format(str(e)))
        raise


