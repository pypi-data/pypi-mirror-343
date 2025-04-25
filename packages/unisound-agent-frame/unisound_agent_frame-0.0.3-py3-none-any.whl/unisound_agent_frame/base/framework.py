import asyncio
import uvicorn
from fastapi import FastAPI

from unisound_agent_frame.base.config_manager import ConfigManager
from unisound_agent_frame.base.component_manager import ComponentManager
from unisound_agent_frame.base.router_manager import RouterManager
from unisound_agent_frame.exception.exception_handler import ExceptionHandler

class Framework:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Framework, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            # 构造函数初始化
            self.config_manager = ConfigManager()
            self.component_manager = ComponentManager(self)
            self.router_manager = RouterManager(self)
            self.exception_handler = ExceptionHandler(self)
            self.initialized = False

            # 从ConfigManager中获取配置
            self.config = None
            self.settings_config = None
            self.logger = None
            self.mysql = None
            self.data_logger = None

            # 从ComponentManager中获取组件
            self.llm_pool = None
            self.agent_registry = None
            self.agent_concurrency = None
            self.distributed_concurrency = None
            self.app = None

    async def init(self):
        """框架初始化"""
        # 1. 初始化配置
        if not await self.config_manager.init_config():
            raise Exception("配置初始化失败")

        # 更新配置相关属性
        self.config = self.config_manager.config
        self.settings_config = self.config_manager.settings_config
        self.logger = self.config_manager.logger
        self.mysql = self.config_manager.mysql
        self.data_logger = self.config_manager.data_logger

        # 2. 初始化组件
        if not await self.component_manager.init_components():
            raise Exception("组件初始化失败")

        # 更新组件相关属性
        self.llm_pool = self.component_manager.llm_pool
        self.agent_registry = self.component_manager.agent_registry
        self.agent_concurrency = self.component_manager.agent_concurrency
        self.distributed_concurrency = self.component_manager.distributed_concurrency
        self.app = self.component_manager.app

        # 3. 初始化路由
        self.router_manager.init_routes(self.app)

        # 4. 初始化异常处理
        await self.exception_handler.init_exception_handlers(self.app)

        self.initialized = True
        await self.logger.info('Framework 框架初始化完成')

    async def close(self):
        """关闭框架，释放资源"""
        try:
            await self.component_manager.close()
            await self.config_manager.close()
            await self.logger.info('Framework 框架关闭完成')
        except Exception as e:
            print(f"框架关闭失败: {str(e)}")
            raise

    def get_app(self) -> FastAPI:
        """获取FastAPI应用实例"""
        if not self.initialized:
            raise RuntimeError("框架未初始化")
        return self.app

    async def start(self, workers=None):
        """启动框架服务"""
        try:
            # 初始化框架
            await self.init()

            # 获取服务配置
            server_config = self.config.get('server', {})
            final_workers = server_config.get('workers') or workers or 1

            # 配置uvicorn服务器
            config = uvicorn.Config(
                app=self.get_app(),
                host=server_config.get('host', '0.0.0.0'),
                port=server_config.get('port', 8000),
                reload=server_config.get('reload', False),
                workers=final_workers,
                loop='asyncio'
            )

            # 创建服务器实例
            server = uvicorn.Server(config)

            # 启动服务
            await self.logger.info('Framework 开始启动服务器')
            await server.serve()

        except Exception as e:
            await self.logger.error(f'Framework 服务启动失败: {str(e)}')
            raise

    @classmethod
    async def create_and_start(cls):
        """创建框架实例并启动服务"""
        framework = cls()
        return await framework.start()

    async def shutdown(self, signal_name: str = None):
        """优雅关闭服务"""
        if signal_name:
            await self.logger.info(f'Framework 收到信号 {signal_name}，开始关闭服务...')

        # 取消所有正在运行的任务
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]

        # 关闭框架
        await self.close()
        await self.logger.info('Framework 服务关闭完成')

        # 延迟等待
        await asyncio.sleep(0.1)
