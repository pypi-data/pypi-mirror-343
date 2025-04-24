import uuid

from unisound_agent_frame.agent.agent import Agent, SaveResultFunc
from unisound_agent_frame.domain.request_model import AnalyzeRequest
from unisound_agent_frame.llm.llm_pool import LLMPool
from unisound_agent_frame.util.logger import MyLogger

logger = MyLogger()


class DemoAgent(Agent):
    """文本分析"""

    async def init(self, agent_config: str):
        self.agent_config = agent_config

    async def run(self, request: AnalyzeRequest, save_result_func: SaveResultFunc):
        connection = None
        llm_pool = LLMPool.get_instance()
        try:
            await self.logger.info(f"DemoAgent run,request:{request},agent_config:{self.agent_config}")
            # 模拟处理请求，获取结果
            result = "文本分析结果"
            status = 0  # 0 表示成功
            message = "分析成功完成"
            messages = [
                {"role": "user", "content": "人应当怎样度过自己的一生？"}
            ]
            task_id = uuid.uuid4().hex
            connection = await llm_pool.get_connection()
            result = await connection.chat(messages=messages, task_id=task_id)
            await logger.info(f"llm result:{result}")

            await llm_pool.release_connection(connection)

            await logger.info(f"llm release:{result}")
            # 调用回调函数保存结果
            await save_result_func(result, status, message)

        except Exception as e:
            # 处理异常情况
            error_status = 1  # 非0 表示失败
            error_message = f"分析失败: {str(e)}"
            if connection is not None:
                await llm_pool.release_connection(connection)
            await save_result_func("", error_status, error_message)
