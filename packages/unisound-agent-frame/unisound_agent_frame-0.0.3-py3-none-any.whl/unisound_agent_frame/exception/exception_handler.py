from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from unisound_agent_frame.exception.business_exception import BusinessException

class ExceptionHandler:
    def __init__(self, framework):
        self.framework = framework

    async def init_exception_handlers(self, app):
        """初始化全局异常处理器"""
        @app.exception_handler(Exception)
        async def global_exception_handler(request: Request, exc: Exception):
            await self.framework.logger.error(f"全局异常处理: {str(exc)}")
            # 默认错误信息
            code = 500
            message = "Internal server error"
            
            # 检查异常类型并设置对应的 code 和 message
            if isinstance(exc, HTTPException):
                code = exc.status_code
                message = exc.detail
            elif isinstance(exc, RequestValidationError):
                code = 422
                message = "请求参数错误"
            elif isinstance(exc, BusinessException):
                code = exc.code
                message = exc.message
            else:
                message = "服务器内部错误"
                
            # 返回统一结构的 JSON 响应，HTTP 状态码设为 200
            return JSONResponse(
                status_code=200,
                content={
                    "code": code,
                    "message": message,
                    "data": None
                }
            )