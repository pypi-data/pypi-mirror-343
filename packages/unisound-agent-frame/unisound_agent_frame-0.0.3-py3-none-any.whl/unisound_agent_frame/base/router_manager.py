from datetime import datetime
import json
import time
import asyncio
from fastapi import FastAPI, Request
from unisound_agent_frame.domain.models import ServiceLog
from unisound_agent_frame.domain.request_model import AnalyzeRequest, HealthCheckRequest, MetricsRequest, GetResultRequest
from unisound_agent_frame.domain.response_model import AnalyzeResponse, HealthCheckResponse, MetricsResponse, ResponseStatus
from unisound_agent_frame.exception.business_exception import BusinessException

class RouterManager:
    def __init__(self, framework):
        self.framework = framework
        self.app = None

    def init_routes(self, app: FastAPI):
        """初始化所有路由"""
        self.app = app
        self._setup_core_routes()
        self._setup_service_routes()
        self._setup_management_routes()

    def _setup_core_routes(self):
        """设置核心业务路由"""
        @self.app.post("/analyze", response_model=AnalyzeResponse)
        async def analyze(request: AnalyzeRequest, fastapi_request: Request):
            await self.framework.logger.info(f'请求分析接口请求参数：{request}')
            agent = self.framework.agent_registry.get_agent(request.agent_id)
            if not agent:
                return AnalyzeResponse.fail(message="agent_id is error", data="", code=-1)

            asyncio.create_task(self._handle_analyze(request, agent))
            return AnalyzeResponse.success()

        @self.app.post("/get_result", response_model=AnalyzeResponse)
        async def get_result(request: GetResultRequest):
            try:
                result = await self.framework.agent_registry.get_result(request.agent_id, request.request_id)
                if result:
                    return AnalyzeResponse.success(data=result)
                else:
                    return AnalyzeResponse.success(data="")
            except Exception as e:
                await self.framework.logger.error(f'获取分析结果失败，requestId:{request.request_id},异常信息: {str(e)}')
                return AnalyzeResponse.fail()

    def _setup_service_routes(self):
        """设置服务检测路由"""
        @self.app.post("/health", response_model=HealthCheckResponse)
        async def health_check(request: HealthCheckRequest=None):
            system_info = {
                'service_name': self.framework.settings_config.get('service_name'),
                'version': self.framework.settings_config.get('service_version'),
                'status': "ok"
            }
            return HealthCheckResponse(
                code=ResponseStatus.SUCCESS.code,
                message=ResponseStatus.SUCCESS.message,
                data=system_info
            )

        @self.app.post("/metrics", response_model=MetricsResponse)
        async def get_metrics(request: MetricsRequest=None):
            metrics = []
            service_id = self.framework.config.get('service_id', 'default')
            
            # 收集模型并发数据
            for model_type in self.framework.config.get('models', {}).keys():
                current_count = await self.framework.distributed_concurrency.get_current_count(model_type)
                max_count = self.framework.distributed_concurrency.model_concurrency_map.get(model_type, 0)
                metrics.append({
                    'name': f'{service_id}_{model_type}_model_concurrent_count',
                    'value': current_count,
                    'timestamp': time.time(),
                    'max_concurrent': max_count
                })

            # 收集agent并发数据
            agent_max_concurrent = self.framework.config.get('agent_max_concurrent', 1000)
            current_count = await self.framework.agent_concurrency.get_concurrent()
            metrics.append({
                'name': f'{service_id}_agent_concurrent_count',
                'value': current_count,
                'timestamp': time.time(),
                'max_concurrent': agent_max_concurrent
            })

            # 收集连接池状态
            pool_status = await self.framework.llm_pool.get_pool_status()
            metrics.append({
                'name': f'{service_id}_pool',
                'pool': pool_status
            })

            return MetricsResponse(
                code=ResponseStatus.SUCCESS.code,
                message=ResponseStatus.SUCCESS.message,
                data=metrics
            )

    def _setup_management_routes(self):
        """设置管理类路由"""
        @self.app.post("/set_model_max_concurrent")
        async def set_model_max_concurrent(model_type: str, max_concurrent: int):
            try:
                await self.framework.distributed_concurrency.set_max_concurrent(model_type, max_concurrent)
                return {"status": 0, "message": f"模型 {model_type} 最大并发数更新为 {max_concurrent}", "data": ""}
            except Exception as e:
                self.framework.logger.error(f"设置模型最大并发数失败,异常信息：{str(e)}")
                raise BusinessException(code=-1, message="设置模型最大并发数失败")

        @self.app.post("/reset_agent_concurrency")
        async def reset_agent_concurrency(current_concurrent: int):
            try:
                service_id = self.framework.config.get('service_id', 'default')
                await self.framework.agent_concurrency.reset_currency()
                return {"status": 0, "message": f"service_id:{service_id} 重置agent当前并发数", "data": ""}
            except Exception as e:
                self.framework.logger.error(f"重置agent当前并发数,异常信息：{str(e)}")
                raise BusinessException(code=-1, message="重置agent当前并发数失败")

    async def _handle_analyze(self, request: AnalyzeRequest, agent):
        """处理分析请求"""
        start_time = time.time()
        try:
            await self.framework.agent_concurrency.add_one(request.agent_id)
            await agent.run(
                request,
                lambda result, status, message: self.framework.agent_registry.save_result(
                    request=request,
                    result=result,
                    status=status,
                    message=message,
                    cost_time=int((time.time() - start_time) * 1000)
                )
            )
            await self.framework.logger.info('_handle_analyze 分析任务完成')
        except Exception as e:
            await self.framework.logger.error(f'分析失败，requestId:{request.request_id},异常信息: {str(e)}')
            error_time = time.time()
            processing_time = error_time - start_time

            error_log = ServiceLog(
                agent_id=request.agent_id,
                request_id=request.request_id,
                request_time=datetime.now(),
                request_data=json.dumps(request.dict(), ensure_ascii=False),
                response_data=json.dumps({}),
                status=500,
                error_message=str(e),
                cost_time=int(processing_time * 1000)
            )

            await self.framework.data_logger.save_log(error_log)