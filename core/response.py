from pydantic import BaseModel
from typing import Any
from fastapi.responses import JSONResponse



class ResponseModel(BaseModel):
    """ 标准的响应体 Pydantic 模型，用于 Swagger 文档展示 """
    code: int
    msg: str
    data: Any = None


def success(data: Any = None, msg: str = "success") -> ResponseModel:
    """ 成功返回的快捷函数 """
    return ResponseModel(code=0, data=data, msg=msg)

def fail(code: int, msg: str, data: Any = None) -> JSONResponse:
    """
    失败返回的快捷函数
    采用 JSONResponse, 设置 HTTP 状态码为 200
    真正的错误码藏在内容字典的 'code' 里
    """
    content = {"code": code, "msg": msg, "data": data}
    return JSONResponse(status_code=200, content=content)


