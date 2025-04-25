from enum import Enum
from typing import Dict, Any, List

from pydantic import BaseModel


# class ResponseStatus(str, Enum):
#     SUCCESS = "success"
#     ERROR = "error"
#     TIMEOUT = "timeout"
#     NOT_FOUND = "not found"


class ResponseStatus(Enum):
    SUCCESS = (0, "操作成功")
    NOT_FOUND = (-1, "资源不存在")
    ERROR = (-1, "服务器错误")

    def __init__(self, code, message):
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message


# class BaseResponse(BaseModel):
#     request_id: str = Field(..., description="请求ID")
#     status: ResponseStatus.code = Field(..., description="响应状态")
#     message: str = Field("", description="响应消息")
#     timestamp: datetime = Field(default_factory=datetime.now, description="响应时间戳")
#     error_code: Optional[str] = Field(None, description="错误代码")
#     error_detail: Optional[str] = Field(None, description="错误详情")

class AnalyzeResponse(BaseModel):
    code: int
    message: str
    data: str

    @classmethod
    def success(
            cls,
            message: str = ResponseStatus.SUCCESS.message,
            data: str = "",
            code: int = 0
    ) -> "AnalyzeResponse":
        """
        创建成功的响应

        Args:
            message: 响应消息，默认为"Success"
            data: 响应数据，默认为空字符串
            code: 响应代码，默认为0

        Returns:
            AnalyzeResponse实例
        """
        return cls(code=code, message=message, data=data)

    @classmethod
    def fail(
            cls,
            message: str = ResponseStatus.ERROR.message,
            data: str = "",
            code: int = -1
    ) -> "AnalyzeResponse":
        """
        创建失败的响应

        Args:
            message: 响应消息，默认为"Error"
            data: 响应数据，默认为空字符串
            code: 响应代码，默认为-1

        Returns:
            AnalyzeResponse实例
        """
        return cls(code=code, message=message, data=data)


class HealthCheckResponse(BaseModel):
    code: int
    message: str
    data: Dict[str, Any]


class MetricsResponse(BaseModel):
    code: int
    message: str
    data: List[Dict[str, Any]]
