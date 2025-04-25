import asyncio
from fastapi import FastAPI
from unisound_agent_frame.concurrency.agent_concurrency import AgentConcurrencyCounter
from unisound_agent_frame.concurrency.distributed_concurrency import DistributedConcurrency
from unisound_agent_frame.llm.llm_pool import LLMPool
from unisound_agent_frame.agent.agent_registry import AgentRegistry

class ComponentManager:
    def __init__(self, framework):
        self.framework = framework
        self.agent_concurrency = None
        self.distributed_concurrency = None
        self.llm_pool = None
        self.agent_registry = None
        self.app = None

    async def init_components(self):
        """组件初始化阶段"""
        try:
            # 初始化agent并发计数器
            self.agent_concurrency = AgentConcurrencyCounter()
            await self.agent_concurrency.init()
            await self.framework.logger.info('Framework Agent并发计数器初始化完成')

            # 初始化分布式并发控制组件
            self.distributed_concurrency = DistributedConcurrency()
            await self.distributed_concurrency.init()
            await self.framework.logger.info('Framework 分布式并发控制组件初始化完成')

            # 初始化连接池组件
            self.llm_pool = LLMPool(self.distributed_concurrency)
            await self.llm_pool.init_pool()
            await self.framework.logger.info('Framework 大模型连接池组件初始化完成')

            # 初始化Agent注册组件
            self.agent_registry = AgentRegistry()
            await self.agent_registry.init_agents()
            await self.agent_registry.init_redis()
            await self.framework.logger.info('Framework Agent注册组件初始化完成')

            # 初始化FastAPI应用
            self.app = FastAPI(
                title=self.framework.settings_config.get('service_name', 'AI Service Framework'),
                description=self.framework.settings_config.get('service_description', 'AI Service Framework API'),
                version=self.framework.settings_config.get('service_version', '1.0.0')
            )

            return True
        except Exception as e:
            await self.framework.logger.error('Framework', f'组件初始化失败: {str(e)}')
            return False

    async def close(self):
        """关闭组件管理器，释放资源"""
        try:
            if self.llm_pool:
                await self.llm_pool.close()
            if self.agent_registry:
                await self.agent_registry.close()
            if self.distributed_concurrency:
                await self.distributed_concurrency.close()
            if self.agent_concurrency:
                await self.agent_concurrency.close()
            await self.framework.logger.info('组件管理器关闭完成')
        except Exception as e:
            await self.framework.logger.error(f"组件管理器关闭失败: {str(e)}")
            raise