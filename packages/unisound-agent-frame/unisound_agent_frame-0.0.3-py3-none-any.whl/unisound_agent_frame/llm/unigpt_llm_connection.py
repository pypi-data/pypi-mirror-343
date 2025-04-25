import asyncio

import aiohttp
import time
import json
from typing import Dict, Any, Optional, List

from unisound_agent_frame.concurrency.distributed_concurrency import DistributedConcurrency
from unisound_agent_frame.llm.llm_connection import LLMConnection
from unisound_agent_frame.util.config_reader import ConfigReader
from unisound_agent_frame.util.logger import MyLogger
from datetime import datetime

logger = MyLogger()


class UniGptLLMConnection(LLMConnection):


    def __init__(self):

        self.initialized = False
        self.session: Optional[aiohttp.ClientSession] = None
        self.model_name: Optional[str] = None
        self.api_url: Optional[str] = None
        self.api_key: Optional[str] = None
        self.api_secret: Optional[str] = None
        self.api_vendor: Optional[str] = None
        self.api_host: str = ""
        self.default_temperature: float = 0.0  # 新增默认参数
        self.default_max_tokens: int = 10240  # 新增默认参数
        self.initialized: bool = False

        # if not hasattr(self, 'initialized'):
        #     self.initialized = False
        #     self.session: Optional[aiohttp.ClientSession] = None
        #     self.model_name: Optional[str] = None
        #     self.api_url: Optional[str] = None
        #     self.api_key: Optional[str] = None
        #     self.api_secret: Optional[str] = None
        #     self.api_vendor: Optional[str] = None
        #     self.api_host: str = ""
        #     self.default_temperature: float = 0.0  # 新增默认参数
        #     self.default_max_tokens: int = 10240    # 新增默认参数
        #     self.initialized: bool = False

    async def init(self, config: Dict[str, Any]):
        """初始化连接"""
        # 从配置中提取参数（新增参数获取）
        self.model_name = config['model_name']
        self.api_url = config['api_url']
        self.api_key = config['api_key']
        self.api_secret = config.get('api_secret')
        self.api_vendor = config.get('api_vendor')
        self.api_host = config.get('api_host', "")
        self.default_temperature = config.get('temperature', 0.0)          # 从配置读取
        self.default_max_tokens = config.get('max_new_tokens', 10240)      # 从配置读取

        # 验证必要参数
        required_fields = ['model_name', 'api_url', 'api_key', 'api_vendor']
        if not all(config.get(field) for field in required_fields):
            raise ValueError("Missing required llm configuration fields")
        # 初始化时设置连接池参数
        connector = aiohttp.TCPConnector(
                limit=2,  # 最大连接数
                limit_per_host=2000,  # 单个目标主机的最大连接数
                ssl=False
            )
        self.session = aiohttp.ClientSession(connector=connector)
        self.initialized = True


    def get_llm_model_type(self):
        config = ConfigReader.get_frame_config()
        # 获取大模型配置字典
        models = config.get('models', {})  # 确保即使没有models配置也不报错
        # 获取配置中的 llm_model 值，若不存在或无效则默认使用 models 中的第一个模型
        llm_model_type = config.get('llm_model', next(iter(models.keys())))  # 默认取 models 的第一个 key
        if llm_model_type not in models:
            llm_model_type = next(iter(models.keys()))  # 强制回退到第一个模型
        return llm_model_type


    async def chat(self, messages: list,task_id: Optional[str] = None,** kwargs) -> str:
        """执行LLM推理请求"""
        if not self.initialized:
            raise RuntimeError("Connection not initialized")

        # 生成请求头
        headers, request_id = await self._generate_headers(task_id)

        # 构造请求体
        data = {
            "messages": messages,
            "model": self.model_name,
            "temperature": self.default_temperature,
            "max_tokens": self.default_max_tokens
        }
        data.update(kwargs)

        # 带重试机制的请求
        fail_count = 0
        while True:
            try:
                async with self.session.post(
                        self.api_url,
                        headers=headers,
                        json=data
                ) as response:
                    # 处理HTTP错误状态码
                    if response.status == 504:
                        raise TimeoutError("Inference API Timeout!")
                    response.raise_for_status()

                    # 解析响应
                    return await self._process_response(await response.json(), request_id)

            except aiohttp.ClientResponseError as e:
                await self._handle_retry(e, fail_count)
                fail_count += 1
            except Exception as e:
                await self._handle_retry(e, fail_count)
                fail_count += 1

    async def _generate_headers(self, task_id: Optional[str]) -> tuple:
        """生成请求头"""
        headers = {"Content-Type": "application/json"}

        headers.update({
            "timestamp": str(int(time.time() * 1000)),
            "appkey": self.api_key,
            "vendor": self.api_vendor,
            "requestId": task_id
        })
        # if self.api_host:
        #     headers["host"] = self.api_host
        await logger.info(f"Task_generate_headers {task_id} - LLM RequestID: {task_id}")

        return headers, task_id

    async def _process_response(self, response: Dict, request_id: Optional[str]) -> str:
        """处理API响应"""
        await logger.info(f"request_id:{request_id},llm process response:{response}")
        try:
            # 解包result字段
            if 'result' not in response:
                raise ValueError(f"_process_response request_id:{request_id} response error: {response}")
            response = response['result']
            return response['choices'][0]['message']['content']

        except KeyError as e:
            await logger.error(f"Response missing key: {e}")
            raise ValueError("Invalid response format")
        except json.JSONDecodeError as e:
            await logger.error(f"JSON decode failed: {e}")
            raise ValueError("Invalid JSON response")

    async def _handle_retry(self, error: Exception, fail_count: int):
        """处理重试逻辑"""
        if fail_count > 9:
            await logger.error("LLM API failed after 9 retries")
            raise TimeoutError("LLM API not responding after 9 retries")

        await logger.warning(f"LLM Request failed ({error}), retry {fail_count + 1}/10...")
        await asyncio.sleep(10)

    async def close(self):
        """关闭连接"""
        if self.session:
            await self.session.close()
            self.initialized = False

    def is_available(self) -> bool:
        return self.initialized and not self.session.closed

    def get_model_type(self) -> str:
        return "UniGpt"


    async def acquire(self, distributed_concurrency: DistributedConcurrency):
        """获取连接使用权"""
        llm_model_type = self.get_llm_model_type()

        # 持续尝试获取分布式并发控制
        while True:
            # 获取分布式并发控制
            acquired = await distributed_concurrency.acquire(llm_model_type)

            if acquired:
                self.is_busy = True
                self.last_used = datetime.now()
                self.total_requests += 1
                return True  # 成功获取

            # 获取失败则等待5秒后重试
            await asyncio.sleep(5)

    async def release(self, distributed_concurrency: DistributedConcurrency):
        """释放连接"""
        self.is_busy = False
        await distributed_concurrency.release(self.get_llm_model_type())