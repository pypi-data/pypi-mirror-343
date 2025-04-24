from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ServiceLog(Base):
    __tablename__ = 'service_logs'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    agent_id = Column(String(100), comment='智能体标识')
    request_id = Column(String(36), comment='请求唯一ID')
    request_time = Column(DateTime, comment='请求时间')
    request_data = Column(Text, comment='请求数据')
    response_data = Column(Text, comment='响应数据')
    status = Column(Integer, comment='状态码')
    error_message = Column(Text, comment='错误信息')
    cost_time = Column(Integer, comment='总耗时')
    created_time = Column(DateTime, nullable=False, default=datetime.now, comment='记录时间')

    def __init__(self, agent_id: str, request_id: str, request_time: datetime,
                 request_data: str, response_data: str, status: int,
                 error_message: str, cost_time: int):
        self.agent_id = agent_id
        self.request_id = request_id
        self.request_time = request_time
        self.request_data = request_data
        self.response_data = response_data
        self.status = status
        self.error_message = error_message
        self.cost_time = cost_time 