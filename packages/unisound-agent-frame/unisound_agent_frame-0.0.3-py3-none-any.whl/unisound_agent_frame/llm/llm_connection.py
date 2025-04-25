from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Any, Dict

from unisound_agent_frame.concurrency.distributed_concurrency import DistributedConcurrency


class LLMConnection(ABC):
    """大模型连接抽象基类"""

    # 链接信息
    last_used = datetime.now()
    is_busy = False
    total_requests = 0

    @abstractmethod
    async def init(self, config: Dict[str, Any]):
        """初始化连接
        Args:
            config: 配置信息
        """
        pass

    @abstractmethod
    async def chat(self, messages: list, task_id: Optional[str] = None, **kwargs) -> str:
        """发送对话请求
        Args:
            messages: 对话消息列表
            **kwargs: 其他参数
        Returns:
            响应结果
        """
        pass

    @abstractmethod
    async def close(self):
        """关闭连接"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查连接是否可用"""
        pass

    @abstractmethod
    def acquire(self, distributed_concurrency: DistributedConcurrency):
        """获取连接使用权"""
        pass

    @abstractmethod
    def release(self, distributed_concurrency: DistributedConcurrency):
        """释放连接"""
        pass

# class LLMConnectionImpl:
#     def __init__(self):
#         self.session: Optional[aiohttp.ClientSession] = None
#         self.config = ConfigReader.get_frame_config()
#         self.llm_config = self.config.get('llm', {})
#         self.base_url = self.llm_config.get('base_url')
#         self.headers = {
#             'Authorization': f"Bearer {self.llm_config.get('api_key')}",
#             'Content-Type': 'application/json'
#         }
#
#     async def __init(self):
#         """初始化连接"""
#         if not self.session:
#             self.session = aiohttp.ClientSession(
#                 base_url=self.base_url,
#                 headers=self.headers
#             )
#
#     async def acquire(self) -> bool:
#         """获取连接"""
#         await self.__init()
#         return True
#
#     async def release(self) -> bool:
#         """释放连接"""
#         if self.session:
#             await self.session.close()
#             self.session = None
#         return True
#
#     async def call_model(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         调用大模型接口
#         :param endpoint: API端点
#         :param payload: 请求参数
#         :return: 响应结果
#         """
#         if not self.session:
#             await self.__init()
#
#         try:
#             async with self.session.post(endpoint, json=payload) as response:
#                 if response.status != 200:
#                     raise Exception(f"API调用失败: {response.status}")
#                 return await response.json()
#         except Exception as e:
#             await self.release()
#             raise e
#
#     async def __aenter__(self):
#         """异步上下文管理器入口"""
#         await self.acquire()
#         return self
#
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         """异步上下文管理器出口"""
#         await self.release()
