from typing import Optional

import aioredis
from fastapi import Request

from unisound_agent_frame.util.config_reader import ConfigReader


class AgentConcurrencyCounter:

    _instance = None

    def __new__(cls, *args, ** kwargs):
        if cls._instance is None:
            cls._instance = super(AgentConcurrencyCounter,cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.redis = None
            self.max_concurrent = {}
            self.initialized = False
            self.service_id = None

    async def init(self):
        """初始化Redis连接和最大并发数配置"""
        if not self.initialized:
            config = ConfigReader.get_frame_config()
            redis_config = config.get('redis', {})
            self.service_id = config.get('service_id', 'default')
            # 构建Redis URL
            redis_url = f"redis://{redis_config.get('host', 'localhost')}:{redis_config.get('port', 6379)}"

            # 使用新版本的aioredis API
            self.redis = await aioredis.from_url(
                redis_url,
                password=redis_config.get('password'),
                db=redis_config.get('db', 0),
                encoding='utf-8',
                decode_responses=True
            )

            # # 从配置中读取每个agent的最大并发数
            agent_max_concurrent = config.get('agent_max_concurrent', 1000)
            self.max_concurrent[self.service_id] = agent_max_concurrent
            # for agent_id, agent_config in agent_configs.items():
            #     self.max_concurrent[agent_id] = agent_config.get('max_concurrent', 10)

            self.initialized = True

    def _get_model_key(self, agent_id: str, request: Optional[Request] = None) -> str:
        """获取模型在Redis中的key
        Args:
            agent_id: agentId
        Returns:
            带服务ID前缀的Redis key
        """
        return f"agent_concurrent:{self.service_id}"

    async def add_one(self, agent_id: str) -> bool:
        """增加agent并发数，如果超过最大并发数则返回False"""
        if not self.initialized:
            await self.init()

        key = self._get_model_key(agent_id)
        try:
            await self.redis.incr(key)
            return True
        except Exception as e:
            print(e)
            return False

    async def sub_one(self, agent_id: str):
        """减少agent并发数（步长1），确保≥0（使用Lua脚本保证原子性）"""
        if not self.initialized:
            await self.init()

        key = self._get_model_key(agent_id)
        # Lua脚本原子执行：current = max(current - 1, 0)
        script = """
            local key = KEYS[1]
            local current = tonumber(redis.call('get', key) or 0)
            local new_value = current > 0 and (current - 1) or 0
            redis.call('set', key, new_value)
            return new_value
        """
        # 执行脚本（返回新值，无需额外查询）
        new_val = await self.redis.eval(script, 1, key)
        return new_val

    async def get_concurrent(self, agent_id: str=None) -> int:
        """获取当前agent的并发数"""
        if not self.initialized:
            await self.init()

        key = self._get_model_key(agent_id)
        value = await self.redis.get(key)
        return int(value) if value else 0

    async def reset_currency(self, agent_id: str=None):
        """获取当前agent的并发数"""
        if not self.initialized:
            await self.init()

        key = self._get_model_key(agent_id)
        value = await self.redis.set(key, 0)


    async def close(self):
        """关闭Redis连接"""
        # if self.redis is not None:
        #     await self.redis.close()
        #     self.initialized = False
