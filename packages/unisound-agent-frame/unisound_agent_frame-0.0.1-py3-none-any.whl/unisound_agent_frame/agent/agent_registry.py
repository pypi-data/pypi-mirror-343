import importlib
import json
import os
from datetime import datetime
from typing import Dict, Type, Optional

import aioredis

from unisound_agent_frame.concurrency.agent_concurrency import AgentConcurrencyCounter
from unisound_agent_frame.domain.models import ServiceLog
from unisound_agent_frame.domain.request_model import AnalyzeRequest
from unisound_agent_frame.util.config_reader import ConfigReader
from unisound_agent_frame.util.data_logger import DataLogger
from unisound_agent_frame.util.logger import MyLogger
from unisound_agent_frame.agent.agent import Agent


class AgentRegistry:
    _instance = None
    _agents: Dict[str, Agent] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.config = ConfigReader.get_frame_config()
            self.settings_config = ConfigReader.get_settings_config()
            self.data_logger = DataLogger()
            self.logger = MyLogger()
            self.redis: Optional[aioredis.Redis] = None
            self.redis_config = self.config.get('redis', {})
            self.initialized = False
            config = ConfigReader.get_frame_config()
            self.service_id = config.get('service_id', 'default')
            self.agent_concurrency = AgentConcurrencyCounter()

    async def init_redis(self):
        """初始化Redis连接"""

        if self.initialized:
            return
        if not self.redis:
            self.redis = await aioredis.from_url(
                f"redis://{self.redis_config.get('host', 'localhost')}:{self.redis_config.get('port', 6379)}",
                password=self.redis_config.get('password'),
                db=self.redis_config.get('db', 0)
            )
        self.initialized = True

    def _get_model_key(self, agent_id: str, request_id: str) -> str:
        return f"{self.service_id}:{agent_id}:{request_id}"

    async def get_result(self, agent_id: str, request_id: str) -> str:
        await self.init_redis()  # 假设这也是异步方法
        key = self._get_model_key(agent_id, request_id)
        result = await self.redis.get(key)  # 添加await
        return result if result else ""  # 处理可能的None值

    async def save_result(
            self,
            request: AnalyzeRequest,
            result: str,
            status: int,
            message: str,
            cost_time: int
    ):
        """保存处理结果
        Args:
            request: 请求对象
            result: 处理结果
            status: 状态码
            message: 状态消息
            cost_time: 处理耗时(毫秒)
        """
        try:
            await self.init_redis()
            key = self._get_model_key(request.agent_id, request.request_id)
            await self.redis.set(key, str(result), ex=3600)  # 1小时过期

            # 构造日志对象
            log_data = ServiceLog(
                agent_id=request.agent_id,
                request_id=request.request_id,
                request_time=datetime.now(),
                request_data=json.dumps(request.dict(), ensure_ascii=False),
                response_data=result,
                status=status,
                error_message=message if status != 200 else '',
                cost_time=cost_time
            )

            # 保存日志
            await self.data_logger.save_log(log_data)
            await self.logger.info(f"agent_registry#save_result info")
        except Exception as e:
            await self.logger.error(f"agent_registry#save_result 处理异常:{str(e)}")
        finally:
            # 释放并发许可
            await self.agent_concurrency.sub_one(request.agent_id)

    # async def save_result(self, agent_type: str, request_id: str, result: Dict[str, Any]):
    #     """
    #     保存结果到Redis
    #     :param agent_type: Agent类型
    #     :param request_id: 请求ID
    #     :param result: 结果数据
    #     """
    #     await self.init_redis()
    #     key = f"{agent_type}:{request_id}"
    #     await self.redis.set(key, str(result), ex=3600)  # 1小时过期

    async def init_agents(self):
        """初始化所有配置的Agent"""
        # base_agent_setting = self.settings_config.get('agent_base_setting',{})
        # #默认查找config目录
        # config_path = base_agent_setting.get('config_path', 'config')
        # agent_mapping = base_agent_setting.get('config_key', 'agent_mapping')
        algorithm_mapping = self.config.get('agent_mapping', {})
        config_dir = os.path.join(os.getcwd(), 'config')

        for agent_type, class_path in algorithm_mapping.items():
            try:
                # 动态导入Agent实现类
                module_path, class_name = class_path.rsplit('.', 1)
                module = importlib.import_module(module_path)
                agent_class: Type[Agent] = getattr(module, class_name)

                # 获取Agent配置文件路径
                agent_config = os.path.join(config_dir, f'{agent_type}.yml')

                # 实例化Agent并初始化
                agent = agent_class()
                agent.agent_type = agent_type
                await agent.init(agent_config)
                self._agents[agent_type] = agent

                await self.logger.info(
                    f'Successfully initialized agent: {agent_type}',
                    component='AgentRegistry',
                    class_path=class_path
                )
            except Exception as e:
                await self.logger.error(
                    f"AgentRegistry Failed to initialize agent: {agent_type} class_path': class_path, error: {str(e)}")
                raise

    def get_agent(self, agent_type: str) -> Optional[Agent]:
        """
        获取指定类型的Agent实例
        :param agent_type: Agent类型
        :return: Agent实例
        """
        return self._agents.get(agent_type)

    async def close(self):
        """关闭所有Agent"""
        for agent_type, agent in self._agents.items():
            try:
                await agent.close()
                await self.logger.info(f"AgentRegistry Successfully closed agent: {agent_type}")
            except Exception as e:
                await self.logger.error(f"AgentRegistry Error closing agent: {agent_type} error: {str(e)}")

        if self.redis:
            await self.redis.close()
