import asyncio
import json
import time
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from unisound_agent_frame.agent.agent_registry import AgentRegistry
from unisound_agent_frame.concurrency.agent_concurrency import AgentConcurrencyCounter
from unisound_agent_frame.concurrency.distributed_concurrency import DistributedConcurrency
from unisound_agent_frame.domain.models import ServiceLog
from unisound_agent_frame.domain.request_model import AnalyzeRequest, HealthCheckRequest, MetricsRequest,GetResultRequest
from unisound_agent_frame.domain.response_model import AnalyzeResponse, HealthCheckResponse, MetricsResponse, ResponseStatus
from unisound_agent_frame.exception.business_exception import BusinessException
from unisound_agent_frame.llm.llm_pool import LLMPool
from unisound_agent_frame.util.config_reader import ConfigReader
from unisound_agent_frame.util.data_logger import DataLogger
from unisound_agent_frame.util.logger import MyLogger
from unisound_agent_frame.util.mysql_util import MySQLUtil


class Framework:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Framework, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            # 构造函数初始化
            self.config = None
            self.settings_config = None
            self.logger = None
            self.mysql = None
            self.data_logger = None
            self.llm_pool = None
            self.agent_registry = None
            self.agent_concurrency = None
            self.app = None
            self.initialized = False

    async def init_config(self):
        """配置初始化阶段"""
        try:
            # 1. 构造函数阶段 - 读取配置文件
            self.config = ConfigReader.get_frame_config()
            self.settings_config = ConfigReader.get_settings_config()

            # 2. 配置初始化 - 加载默认配置
            storage_type = self.config.get('data_logger', {}).get('storage_type', 'file')

            if storage_type == 'mysql':
                try:
                    # MySQL配置初始化
                    self.mysql = MySQLUtil(self.config.get('mysql', {}))
                    await self.mysql.init_pool()

                    # 检查表是否存在
                    check_table_sql = """
                              SELECT COUNT(*)
                              FROM information_schema.tables 
                              WHERE table_schema = DATABASE()
                              AND table_name = 'service_logs'
                              """
                    result = await self.mysql.execute(check_table_sql)
                    if result and result[0][0] == 0:
                        # 表不存在时才创建
                        await self.mysql.init_tables()

                except Exception as e:
                    print(f"MySQL初始化失败: {str(e)}")
                    return False

            # 日志配置初始化
            self.data_logger = DataLogger()
            await self.data_logger.init_storage()

            # MyLogger配置初始化
            self.logger = MyLogger()
            agent_log_config = self.config.get('agent_log', {})
            await self.logger.init(agent_log_config)
            await self.logger.info("MyLogger初始化完成")

            return True
        except Exception as e:
            print(f"配置初始化失败: {str(e)}")
            return False

    async def init_components(self):
        """组件初始化阶段"""
        try:
            # 初始化agent并发计数器
            self.agent_concurrency = AgentConcurrencyCounter()
            await self.agent_concurrency.init()
            await self.logger.info('Framework Agent并发计数器初始化完成')

            # 初始化分布式并发控制组件
            self.distributed_concurrency = DistributedConcurrency()
            await self.distributed_concurrency.init()
            await self.logger.info('Framework 分布式并发控制组件初始化完成')

            # 初始化连接池组件
            self.llm_pool = LLMPool(self.distributed_concurrency)
            await self.llm_pool.init_pool()
            await self.logger.info('Framework 大模型连接池组件初始化完成')

            # 初始化Agent注册组件
            self.agent_registry = AgentRegistry()
            await self.agent_registry.init_agents()
            await self.agent_registry.init_redis()
            await self.logger.info('Framework Agent注册组件初始化完成')

            # 初始化FastAPI应用
            self.app = FastAPI(
                title=self.settings_config.get('service_name', 'AI Service Framework'),
                description=self.settings_config.get('service_description', 'AI Service Framework API'),
                version=self.settings_config.get('service_version', '1.0.0')
            )
            self._setup_routes()
            await self.logger.info('Framework 路由注册完成')

            self.initialized = True
            return True
        except Exception as e:
            await self.logger.error(f'Framework 组件初始化失败: {str(e)}')
            return False

    def _setup_routes(self):
        """设置路由"""

        # 1. 核心接口
        @self.app.post("/analyze", response_model=AnalyzeResponse)
        async def analyze(request: AnalyzeRequest, fastapi_request: Request):
            await self.logger.info(f'请求分析接口请求参数：{request}')
            # 创建异步任务
            # 获取对应的Agent
            agent = self.agent_registry.get_agent(request.agent_id)
            if not agent:
                return AnalyzeResponse.fail(message="agent_id is error", data="", code=-1)

            asyncio.create_task(self._handle_analyze(request, agent))

            # 直接返回响应
            return AnalyzeResponse.success()

        @self.app.post("/get_result", response_model=AnalyzeResponse)
        async def get_result(request: GetResultRequest):
            try:
                # 从Redis获取结果
                result = await self.agent_registry.get_result(request.agent_id, request.request_id)
                if result:
                    return AnalyzeResponse.success(data=result)
                else:
                    return AnalyzeResponse.success(data="")
            except Exception as e:
                await self.logger.error(f'获取分析结果失败，requestId:{request.request_id},异常信息: {str(e)}')
                return AnalyzeResponse.fail()

        # 2. 服务检测
        @self.app.post("/health", response_model=HealthCheckResponse)
        async def health_check(request: HealthCheckRequest=None):
            return await self._handle_health_check(request)

        # 3. 弹性扩缩容
        @self.app.post("/metrics", response_model=MetricsResponse)
        async def get_metrics(request: MetricsRequest=None):
            return await self._handle_metrics(request)

        # 4. 修改最大并发
        @self.app.post("/set_model_max_concurrent")
        async def set_model_max_concurrent(model_type: str, max_concurrent: int):
            """设置模型最大并发数"""
            try:
                await self.distributed_concurrency.set_max_concurrent(model_type, max_concurrent)
                return {"status": 0, "message": f"模型 {model_type} 最大并发数更新为 {max_concurrent}", "data": ""}
            except Exception as e:
                self.logger.error(f"设置模型最大并发数失败,异常信息：{str(e)}")
                raise BusinessException(code=-1, message="设置模型最大并发数失败")

        # 回滚redis
        @self.app.post("/reset_agent_concurrency")
        async def reset_agent_concurrency(current_concurrent: int):
            """重置agent当前并发数"""
            try:
                service_id = self.config.get('service_id', 'default')
                await self.agent_concurrency.reset_currency()
                return {"status": 0, "message": f"service_id:{service_id} 重置agent当前并发数", "data": ""}
            except Exception as e:
                self.logger.error(f"重置agent当前并发数,异常信息：{str(e)}")
                raise BusinessException(code=-1, message="重置agent当前并发数失败")

        # 全局异常处理器
        @self.app.exception_handler(Exception)
        async def global_exception_handler(request: Request, exc: Exception):
            await self.logger.error(f"全局异常处理: {str(exc)}")
            # 默认错误信息
            code = 500
            message = "Internal server error"
            # 检查异常类型并设置对应的 code 和 message
            if isinstance(exc, HTTPException):
                code = exc.status_code
                message = exc.detail
            elif isinstance(exc, RequestValidationError):
                code = 422
                message = "请求参数错误"
            elif isinstance(exc, BusinessException):
                code = exc.code
                message = exc.message
            else:
                message = "服务器内部错误"
            # 返回统一结构的 JSON 响应，HTTP 状态码设为 200
            return JSONResponse(
                status_code=200,
                content={
                    "code": code,
                    "message": message,
                    "data": None
                }
            )

    async def _handle_analyze(self, request: AnalyzeRequest, agent):
        """处理分析请求"""
        start_time = time.time()
        try:
            # 获取并发许可
            await self.agent_concurrency.add_one(request.agent_id)
            # 执行分析,这种方式如果方法执行耗时太久会会阻塞事件循环
            await agent.run(
                request,
                lambda result, status, message: self.agent_registry.save_result(
                    request=request,
                    result=result,
                    status=status,
                    message=message,
                    cost_time=int((time.time() - start_time) * 1000)
                )
            )
            await self.logger.info('_handle_analyze 分析任务完成')
        except Exception as e:
            await self.logger.error(f'分析失败，requestId:{request.request_id},异常信息: {str(e)}')
            error_time = time.time()
            processing_time = error_time - start_time

            # 构造错误日志对象
            error_log = ServiceLog(
                agent_id=request.agent_id,
                request_id=request.request_id,
                request_time=datetime.now(),
                request_data=json.dumps(request.dict(), ensure_ascii=False),
                response_data=json.dumps({}),
                status=500,
                error_message=str(e),
                cost_time=int(processing_time * 1000)  # 转换为毫秒
            )

            # 保存错误日志
            await self.data_logger.save_log(error_log)

    async def _handle_health_check(self, request: HealthCheckRequest) -> HealthCheckResponse:
        """处理健康检查请求"""
        # components = {
        #     'llm_pool': await self._check_llm_pool(),
        #     'agent_registry': bool(self.agent_registry._agents)
        # }
        #
        # system_info = {
        #     'service_name': self.settings_config.get('service_name'),
        #     'version': self.settings_config.get('service_version'),
        #     'components_status': components
        # }
        system_info = {
            'service_name': self.settings_config.get('service_name'),
            'version': self.settings_config.get('service_version'),
            'status': "ok"
        }
        return HealthCheckResponse(
            code=ResponseStatus.SUCCESS.code,
            message=ResponseStatus.SUCCESS.message,
            data=system_info
        )

    async def _handle_metrics(self, request: MetricsRequest) -> MetricsResponse:
        """处理指标请求"""
        metrics = []
        service_id = self.config.get('service_id', 'default')
        # 收集各个模型的并发数据
        for model_type in self.config.get('models', {}).keys():
            current_count = await self.distributed_concurrency.get_current_count(model_type)
            max_count = self.distributed_concurrency.model_concurrency_map.get(model_type, 0)

            metrics.append({
                'name': f'{service_id}_{model_type}_model_concurrent_count',
                'value': current_count,
                'timestamp': time.time(),
                'max_concurrent': max_count
            })
        agent_max_concurrent = self.config.get('agent_max_concurrent', 1000)
        current_count = await self.agent_concurrency.get_concurrent()
        metrics.append({
            'name': f'{service_id}_agent_concurrent_count',
            'value': current_count,
            'timestamp': time.time(),
            'max_concurrent': agent_max_concurrent
        })

        pool_status = await self.llm_pool.get_pool_status()
        metrics.append({
            'name': f'{service_id}_pool',
            'pool': pool_status
        })

        return MetricsResponse(
            code=ResponseStatus.SUCCESS.code,
            message=ResponseStatus.SUCCESS.message,
            data=metrics
        )

    # async def _check_mysql(self) -> bool:
    #     """检查MySQL连接状态"""
    #     try:
    #         await self.mysql.execute("SELECT 1")
    #         return True
    #     except:
    #         return False
    #
    # async def _check_redis(self) -> bool:
    #     """检查Redis连接状态"""
    #     try:
    #         await self.distributed_concurrency.redis.ping()
    #         return True
    #     except:
    #         return False

    async def _check_llm_pool(self) -> bool:
        """检查连接池状态"""
        return bool(self.llm_pool and self.llm_pool.pool)

    async def init(self):
        """框架初始化"""
        if not await self.init_config():
            raise Exception("配置初始化失败")

        if not await self.init_components():
            raise Exception("组件初始化失败")

        await self.logger.info('Framework 框架初始化完成')

    async def close(self):
        """关闭框架，释放资源"""
        try:
            if self.llm_pool:
                await self.llm_pool.close()
            if self.agent_registry:
                await self.agent_registry.close()
            if self.distributed_concurrency:
                await self.distributed_concurrency.close()
            if self.mysql:
                await self.mysql.close()
            if self.logger:
                await self.logger.close()
            if self.agent_concurrency:
                await self.agent_concurrency.close()
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

            final_workers =  server_config.get('workers') or workers  or 1
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
