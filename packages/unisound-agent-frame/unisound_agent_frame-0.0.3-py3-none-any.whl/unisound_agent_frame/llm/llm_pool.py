import asyncio
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Set

from unisound_agent_frame.exception.business_exception import BusinessException
from unisound_agent_frame.llm.llm_connection import LLMConnection
from unisound_agent_frame.llm.llm_connection_factory import LLMConnectionFactory
from unisound_agent_frame.util.config_reader import ConfigReader


@dataclass(frozen=True)
class PoolConnectionKey:
    """连接池中的连接唯一标识"""
    connection_id: str = field(default_factory=lambda: str(id(object())))
    created_time: datetime = field(default_factory=datetime.now)


@dataclass
class PoolConnection:
    """连接池中的连接包装器"""
    connection: LLMConnection
    key: PoolConnectionKey = field(default_factory=PoolConnectionKey)
    is_dynamic: bool = False  # 是否是动态创建的连接
    in_use: bool = False  # 是否正在使用

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        if not isinstance(other, PoolConnection):
            return False
        return self.key == other.key

class LLMPool:
    """LLM连接池"""
    distributed_concurrency = None
    _initialized = False
    _instance = None

    def __new__(cls, *args, ** kwargs):
        if cls._instance is None:
            cls._instance = super(LLMPool,cls).__new__(cls)
        return cls._instance

    def __init__(self, distributed_concurrency=None):
        # 确保只初始化一次
        if not self._initialized:
            self.config = ConfigReader.get_frame_config()
            self.pool_config = self.config.get('llm_pool', {})
            self.max_size = self.pool_config.get('max_size', 10)
            self.min_size = self.pool_config.get('min_size', 2)
            self.connection_timeout = self.pool_config.get('connection_timeout', 30)
            if self.connection_timeout == -1:
                self.connection_timeout = None
            self.model_type = self.config.get('llm_model', 'UniGpt')

            self.pool: deque[PoolConnection] = deque()
            self.wait_queue: asyncio.Queue = asyncio.Queue()

            self.all_connections: Set[PoolConnection] = set()
            self.active_connections: Set[PoolConnection] = set()

            if distributed_concurrency is not None:
                self.distributed_concurrency = distributed_concurrency

            self.initialized = False
            self.cleanup_task = None

    @classmethod
    def get_instance(cls, distributed_concurrency=None):
        """获取单例实例的推荐方法"""
        if cls._instance is None:
            cls._instance = cls(distributed_concurrency)
        elif distributed_concurrency is not None and not hasattr(cls._instance, 'distributed_concurrency'):
            # 如果实例存在但需要设置distributed_concurrency
            cls._instance.distributed_concurrency = distributed_concurrency
        return cls._instance

    async def init_pool(self):
        """初始化连接池"""
        if self._initialized:
            return
        try:
            # 初始化分布式并发控制
            await self.distributed_concurrency.init()
            
            # 创建初始连接
            for _ in range(self.min_size):
                connection = LLMConnectionFactory.create_connection(self.model_type)
                await connection.init(self.config.get("models",{}).get(self.model_type))
                pool_conn = PoolConnection(
                    connection=connection,
                    is_dynamic=False
                )
                self.pool.append(pool_conn)
                self.all_connections.add(pool_conn)
                
            self._initialized = True
            
            # 启动清理任务
            self.cleanup_task = asyncio.create_task(self._cleanup_idle_connections())
        except Exception as e:
            print(f"连接池初始化失败: {str(e)}")
            raise

    async def get_connection(self) -> LLMConnection:
        """获取连接"""
        if not self._initialized:
            await self.init_pool()
            
        # # 获取分布式并发控制
        # acquired = await self.distributed_concurrency.acquire(
        #     'llm_connection',
        #     self.max_size,
        #     self.connection_timeout
        # )
        #
        # if not acquired:
        #     # 如果无法获取并发控制，加入等待队列
        #     future = asyncio.Future()
        #     await self.wait_queue.put(future)
        #     try:
        #         pool_conn = await asyncio.wait_for(future, timeout=self.connection_timeout)
        #         pool_conn.in_use = True
        #         self.active_connections.add(pool_conn)
        #         return pool_conn.connection
        #     except asyncio.TimeoutError:
        #         self.wait_queue.task_done()
        #         raise TimeoutError("获取连接超时")

        # 尝试从连接池获取连接
        while self.pool:
            pool_conn = self.pool.popleft()
            pool_conn.in_use = True
            self.active_connections.add(pool_conn)
            if pool_conn.connection.is_available():
                return pool_conn.connection
            else:
                pool_conn.in_use = False
                self.active_connections.discard(pool_conn)
                # 如果连接不可用，从所有集合中移除并关闭
                await self._remove_connection(pool_conn)

        # 如果没有可用连接且未达到最大连接数，创建新连接
        if len(self.all_connections) < self.max_size:
            connection = LLMConnectionFactory.create_connection(self.model_type)
            await connection.init(self.config.get("models",{}).get(self.model_type))
            pool_conn = PoolConnection(
                connection=connection,
                is_dynamic=True,
                in_use=True
            )
            self.all_connections.add(pool_conn)
            self.active_connections.add(pool_conn)
            return connection
            
        # 如果达到最大连接数，等待连接释放
        future = asyncio.Future()
        await self.wait_queue.put(future)
        try:
            pool_conn = await asyncio.wait_for(future, timeout=self.connection_timeout)
            pool_conn.in_use = True
            self.active_connections.add(pool_conn)
            return pool_conn.connection
        except asyncio.TimeoutError:
            future.set_exception(TimeoutError("连接获取超时"))  # 标记 future 为完成状态
            raise TimeoutError("获取连接超时")

    async def release_connection(self, connection: LLMConnection):
        """释放连接回连接池"""
        # 找到对应的PoolConnection对象
        pool_conn = next((pc for pc in self.all_connections
                         if pc.connection == connection), None)
        if not pool_conn:
            return
            
        pool_conn.in_use = False
        self.active_connections.discard(pool_conn)
        
        # if self.wait_queue.qsize() > 0:
        #     # 如果有等待的请求，直接将连接给等待的请求
        #     future = await self.wait_queue.get()
        #     future.set_result(pool_conn)
        if self.wait_queue.qsize() > 0:
            while not self.wait_queue.empty():
                future = await self.wait_queue.get()
                if not future.done():
                    # 仅当Future未完成时设置结果
                    future.set_result(pool_conn)
                    return
                self.wait_queue.task_done()  # 维护队列计数器
            # 所有等待的Future都已失效，放回连接池
            self.pool.append(pool_conn)
        else:
            # 否则放回连接池
            self.pool.append(pool_conn)
            # await self.distributed_concurrency.release('llm_connection')

    async def _remove_connection(self, pool_conn: PoolConnection):
        """移除并关闭连接"""
        if pool_conn.in_use:
            return  # 如果连接正在使用，不进行移除
        if pool_conn in self.pool:
            #延迟删除
            await asyncio.sleep(0.1)
            if not pool_conn.in_use and not pool_conn in self.active_connections:
                self.pool.remove(pool_conn)
                self.all_connections.discard(pool_conn)
                self.active_connections.discard(pool_conn)
                await pool_conn.connection.close()

    async def _cleanup_idle_connections(self):
        """定期清理空闲连接"""
        while True:
            try:
                await asyncio.sleep(60)  # 每分钟检查一次
                
                # 计算可以释放的连接数
                total_connections = len(self.all_connections)
                active_count = len(self.active_connections)
                idle_count = total_connections - active_count
                
                # 如果空闲连接数超过最小连接数，释放多余的连接
                if idle_count > self.min_size:
                    connections_to_remove = []
                    count_to_remove = idle_count - self.min_size
                    
                    # 优先选择动态创建的空闲连接进行释放
                    for pool_conn in sorted(
                        [pc for pc in self.pool if not pc.in_use],
                        key=lambda pc: (pc.is_dynamic, pc.key.created_time),
                        reverse=True
                    ):
                        if count_to_remove <= 0:
                            break
                        if not pool_conn.in_use:  # 再次检查确保连接仍然空闲
                            connections_to_remove.append(pool_conn)
                            count_to_remove -= 1
                    
                    for pool_conn in connections_to_remove:
                        if not pool_conn.in_use:
                            await self._remove_connection(pool_conn)
            except Exception as e:
                print(f"清理空闲连接时发生错误: {str(e)}")

    async def close(self):
        """关闭连接池"""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass

        # 2. 处理等待队列中的请求（避免永久阻塞）
        while not self.wait_queue.empty():
            waiter = self.wait_queue.get_nowait()
            waiter.set_exception(BusinessException(-2,"Connection pool is closed"))  # 自定义异常

        # 3. 强制关闭所有连接（无论是否活动）
        for conn in self.all_connections.copy():
            await self._remove_connection(conn)  # 确保该方法关闭连接并移除引用

        # 4. 清空数据结构
        self.pool.clear()
        self.all_connections.clear()
        self.active_connections.clear()

        self._initialized = False

    async def call_llm_auto_release_connection(self, messages: list,connection: LLMConnection, **kwargs) -> str:
        """
        使用连接池调用模型
        Args:
            messages: 对话消息列表
            **kwargs: 其他参数
        Returns:
            响应结果
        """
        # connection = await self.get_connection()
        try:
            result = await connection.chat(messages, **kwargs)
            await self.release_connection(connection)
            return result
        except Exception as e:
            await connection.close()
            # await self.distributed_concurrency.release('llm_connection')
            await connection.release(self.distributed_concurrency)
            raise e

    async def get_pool_status(self) -> Dict[str, int]:
        """获取连接池状态"""
        return {
            "total_connections": len(self.all_connections),
            "active_connections": len(self.active_connections),
            "available_connections": len(self.pool),
            "waiting_requests": self.wait_queue.qsize(),
            "dynamic_connections": sum(1 for pc in self.all_connections if pc.is_dynamic)
        }