import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any

import aiofiles
from loguru import logger

from unisound_agent_frame.domain.models import ServiceLog
from unisound_agent_frame.util.config_reader import ConfigReader
from unisound_agent_frame.util.mysql_util import MySQLUtil


class DataStorage(ABC):
    @abstractmethod
    async def save(self, log_data: ServiceLog):
        """保存日志"""
        pass

    @abstractmethod
    async def close(self):
        """关闭存储连接"""
        pass


class MySQLStorage(DataStorage):
    def __init__(self, config: Dict[str, Any]):
        self.mysql = MySQLUtil(config)

    async def save(self, log_data: ServiceLog):
        sql = """
        INSERT INTO service_logs (
            agent_id, request_id, request_time, request_data, 
            response_data, status, error_message, cost_time
        ) VALUES (
            %(agent_id)s, %(request_id)s, %(request_time)s, %(request_data)s,
            %(response_data)s, %(status)s, %(error_message)s, %(cost_time)s
        )
        """
        params = {
            'agent_id': log_data.agent_id,
            'request_id': log_data.request_id,
            'request_time': log_data.request_time,
            'request_data': log_data.request_data,
            'response_data': log_data.response_data,
            'status': log_data.status,
            'error_message': log_data.error_message,
            'cost_time': log_data.cost_time
        }
        await self.mysql.execute(sql, params)

    async def close(self):
        pass


class FileStorage(DataStorage):
    def __init__(self, config: Dict[str, Any]):
        self.log_path = config.get('log_path', 'logs')
        os.makedirs(self.log_path, exist_ok=True)
        self.file_path = os.path.join(
            self.log_path,
            "llm_data_log.txt"
        )

    async def save(self, log_data: ServiceLog):
        log_dict = {
            'agent_id': log_data.agent_id,
            'request_id': log_data.request_id,
            'request_time': log_data.request_time.isoformat(),
            'request_data': log_data.request_data,
            'response_data': log_data.response_data,
            'status': log_data.status,
            'error_message': log_data.error_message,
            'cost_time': log_data.cost_time,
            'created_time': datetime.now().isoformat()
        }
        async with aiofiles.open(self.file_path, mode='a', encoding='utf-8') as f:
            await f.write(json.dumps(log_dict, ensure_ascii=False) + '\n')

    async def close(self):
        pass


class DataLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.config = ConfigReader.get_frame_config().get('data_logger', {})
            self.storage_type = self.config.get('storage_type', 'file')  # 默认使用file
            self.log_path = self.config.get('log_path', '.')  # 默认使用项目根目录
            self.mysql = None
            self.initialized = False

    async def init_storage(self):
        """初始化存储"""
        if not self.initialized:
            if self.storage_type == 'file':
                os.makedirs(self.log_path, exist_ok=True)
            else:
                mysql_config = ConfigReader.get_frame_config().get('mysql', {})
                self.mysql = MySQLUtil(mysql_config)
                await self.mysql.init_pool()
            self.initialized = True

    async def save_log(self, log_data: ServiceLog):
        """保存日志
        Args:
            log_data: ServiceLog对象，包含以下字段：
            - agent_id: 智能体标识
            - request_id: 请求唯一ID
            - request_time: 请求时间
            - request_data: 请求数据
            - response_data: 响应数据
            - status: 状态码
            - error_message: 错误信息
            - cost_time: 总耗时
        """
        if not self.initialized:
            raise RuntimeError("Logger未初始化")

        if self.storage_type == 'file':
            storage = FileStorage(self.config)
        else:
            storage = MySQLStorage(self.config)

        try:
            await storage.save(log_data)
        except Exception as e:
            logger.error(f"looger.py#save_log保存日志异常：{str(e)}")
        finally:
            await storage.close()

    async def close(self):
        """关闭日志器"""
        if self.mysql:
            await self.mysql.close()

