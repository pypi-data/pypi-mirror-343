from pydantic import BaseModel, Field
from datetime import datetime

class BaseRequest(BaseModel):
    request_id: str = Field(..., description="请求ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="请求时间戳")
    service_name: str = Field(..., description="服务名称")
    version: str = Field("1.0", description="API版本")

class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="文本")
    config: str = Field(..., description="配置")
    agent_id: str = Field(..., description="agent_id")
    request_id: str = Field(..., description="请求ID")

class GetResultRequest(BaseModel):
    request_id: str = Field(..., description="请求ID")
    agent_id: str = Field(..., description="agent_id")

class HealthCheckRequest(BaseModel):
    request_id: str

class MetricsRequest(BaseModel):
    request_id: str 