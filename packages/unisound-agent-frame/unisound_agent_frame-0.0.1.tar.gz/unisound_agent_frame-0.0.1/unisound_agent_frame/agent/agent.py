from abc import ABC, abstractmethod
from typing import Dict, Any, Callable

from unisound_agent_frame.domain.request_model import AnalyzeRequest
from unisound_agent_frame.util.logger import MyLogger

SaveResultFunc = Callable[[str, int, str], None]

class Agent(ABC):
    def __init__(self):
        self.logger = MyLogger()
        # self.llm_pool = LLMConnectionPool()
        self.config: Dict[str, Any] = {}
        self.agent_type: str = ""
        self.agent_config=None

    @abstractmethod
    async def init(self, agent_config: str):
        """
        初始化Agent
        :param agent_config: Agent配置文件路径
        :return: Agent实例
        """
        pass

    @abstractmethod
    async def run(self, request: AnalyzeRequest, save_result_func: SaveResultFunc):
        """
        运行Agent
        :param request: 分析请求
        :param save_result_func: 结果保存回调函数，参数为(agent_type, request_id, result)
        :return: 分析结果
        """
        pass

    # @abstractmethod
    # async def run(self, request: AnalyzeRequest, save_result_func: SaveResultFunc) -> Dict[str, Any]:
    #     """
    #     运行Agent
    #     :param request: 分析请求
    #     :param save_result_func: 结果保存回调函数，参数为(agent_type, request_id, result)
    #     :return: 分析结果
    #     """
    #     pass

    async def close(self):
        """关闭Agent，释放资源"""
        pass
    #
    # async def _call_llm(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    #     """
    #     调用大模型
    #     :param endpoint: API端点
    #     :param payload: 请求参数
    #     :return: 响应结果
    #     """
    #     try:
    #         return await self.llm_pool.call_llm(endpoint, payload)
    #     except Exception as e:
    #         await self.logger.error(
    #             self.__class__.__name__,
    #             f"LLM调用失败: {str(e)}",
    #             {"endpoint": endpoint, "error": str(e)}
    #         )
    #         raise
    #
    # def create_error_response(
    #     self,
    #     request: AnalyzeRequest,
    #     error_code: str,
    #     error_message: str,
    #     error_detail: str = None
    # ) -> AnalyzeResponse:
    #     """
    #     创建错误响应
    #     :param request: 原始请求
    #     :param error_code: 错误代码
    #     :param error_message: 错误消息
    #     :param error_detail: 错误详情
    #     :return: 错误响应
    #     """
    #     return AnalyzeResponse(
    #         request_id=request.request_id,
    #         status=ResponseStatus.ERROR,
    #         message=error_message,
    #         error_code=error_code,
    #         error_detail=error_detail,
    #         model_type=request.model_type,
    #         result={},
    #         processing_time=0.0
    #     )