import aioredis

from unisound_agent_frame.util.config_reader import ConfigReader


class DistributedConcurrency:
    def __init__(self):
        self.redis = None
        self.model_concurrency_map = {}
        self.initialized = False
        self.service_id = None

    async def init(self):
        """初始化Redis连接和并发配置"""
        if self.initialized:
            return

        try:
            # 读取配置
            config = ConfigReader.get_frame_config()
            redis_config = config.get('redis', {})
            self.initialized = True
            # 获取服务ID
            self.service_id = config.get('service_id', 'default')

            # 连接Redis
            self.redis = await aioredis.from_url(
                f"redis://{redis_config.get('host', 'localhost')}:{redis_config.get('port', 6379)}",
                password=redis_config.get('password'),
                db=redis_config.get('db', 0),
                encoding='utf-8',
                decode_responses=True
            )

            # 从配置中读取模型并发设置并保存到Redis
            models_config = config.get('models', {})
            for model_type, model_config in models_config.items():
                max_concurrent = model_config.get('max_concurrent', 10)
                await self.set_max_concurrent(model_type, max_concurrent)
        except Exception as e:
            print(f"分布式并发控制初始化失败: {str(e)}")
            self.initialized = False
            raise

    def _get_model_key(self, llm_type: str) -> str:
        """获取模型在Redis中的key
        Args:
            llm_type: 模型类型
        Returns:
            带服务ID前缀的Redis key
        """
        return f"{self.service_id}:model_concurrent:{llm_type}"

    async def set_max_concurrent(self, llm_type: str, max_concurrent: int):
        """设置模型最大并发数
        Args:
            llm_type: 模型类型
            max_concurrent: 最大并发数
        """
        if not self.initialized:
            await self.init()

        # 更新内存中的并发映射
        self.model_concurrency_map[llm_type] = max_concurrent

        # 保存到Redis
        key = self._get_model_key(llm_type)
        await self.redis.set(f"{key}:max", str(max_concurrent))

    async def get_current_count(self, llm_type: str) -> int:
        """获取当前并发数"""
        if not self.initialized:
            await self.init()

        key = self._get_model_key(llm_type)
        value = await self.redis.get(key)
        return int(value) if value else 0

    async def acquire(self, llm_type: str) -> bool:
        # """获取并发许可"""
        # if not self.initialized:
        #     await self.init()
        #
        # key = self._get_model_key(llm_type)
        # max_key = f"{key}:max"
        #
        # # 使用Redis的原子操作检查并增加计数
        # async with self.redis.pipeline(transaction=True) as pipe:
        #     try:
        #         # 监视当前值
        #         await pipe.watch(key)
        #
        #         # 获取当前值和最大值
        #         current = await self.redis.get(key)
        #         max_concurrent = await self.redis.get(max_key)
        #
        #         current = int(current) if current else 0
        #         max_concurrent = int(max_concurrent) if max_concurrent else self.model_concurrency_map.get(llm_type, 0)
        #
        #         # 检查是否超过最大并发
        #         if current >= max_concurrent:
        #             return False
        #
        #         # 增加计数
        #         await pipe.multi()
        #         await pipe.incr(key)
        #         await pipe.execute()
        #         return True
        #
        #     except aioredis.WatchError:
        #         # 如果值被其他客户端修改，返回False
        #         return False
        """获取并发许可（Lua脚本实现）"""
        if not self.initialized:
            await self.init()

        key = self._get_model_key(llm_type)
        max_key = f"{key}:max"
        default_max = self.model_concurrency_map.get(llm_type, 0)

        # Lua脚本实现原子操作
        lua_script = """
           local current = tonumber(redis.call('GET', KEYS[1]) or 0)
           local max_value = tonumber(redis.call('GET', KEYS[2]) or ARGV[1])
           if current < max_value then
               return redis.call('INCR', KEYS[1])
           else
               return 0
           end
           """

        try:
            # 执行脚本并处理结果
            result = await self.redis.eval(
                lua_script,
                keys=[key, max_key],
                args=[str(default_max)]
            )
            return bool(result)
        except aioredis.RedisError as e:
            # 可添加日志记录
            return False

    async def release(self, llm_type: str):
        """释放并发许可"""
        if not self.initialized:
            await self.init()

        key = self._get_model_key(llm_type)
        await self.redis.decr(key)

    async def close(self):
        """关闭Redis连接"""
        if self.redis:
            await self.redis.close()
            self.initialized = False
            self.redis=None