from typing import Any

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


def success_response(message: str, data: Any) -> JSONResponse:
    """将响应信息分装成JSONResponse

    Args:
        message(str): 返回信息
        data(Any): 返回数据
    """
    content = {
        "code": 200,
        "message": message,
        "data": data
    }

    return JSONResponse(content=jsonable_encoder(content))