import os
import sys
from typing import Dict, Any

from loguru import logger


class MyLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MyLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.config = None
            self.initialized = False

    async def init(self, config: Dict[str, Any]):
        """初始化日志配置
        Args:
            config: 包含日志配置的字典，格式如：
            {
                'filePath': 'path/to/log/file.txt'
            }
        """
        if not self.initialized:
            self.config = config

            # 移除默认的sink
            logger.remove()

            # 添加控制台输出
            logger.add(
                sys.stdout,
                format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
            )

            # 添加文件输出
            if 'file_path' in config:
                file_path = config['file_path']
                # 确保日志目录存在
                os.makedirs(file_path, exist_ok=True)

                # 构造按天轮转的日志文件路径
                log_file = os.path.join(file_path, "out-{time:YYYY-MM-DD}.log")

                logger.add(
                    log_file,
                    rotation="00:00",  # 每天午夜轮转
                    retention="10 days",  # 保留10天的日志
                    compression="zip",  # 压缩轮转的日志
                    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
                    encoding="utf-8"
                )

            self.initialized = True

    async def debug(self, message: str, **kwargs):
        """记录debug级别日志"""
        logger.opt(depth=1).debug(message, **kwargs)

    async def info(self, message: str, **kwargs):
        """记录info级别日志"""
        logger.opt(depth=1).info(message, **kwargs)

    async def warning(self, message: str, **kwargs):
        """记录warning级别日志"""
        logger.opt(depth=1).warning(message, **kwargs)

    async def error(self, message: str, **kwargs):
        """记录error级别日志"""
        logger.opt(depth=1).error(message, **kwargs)

    async def critical(self, message: str, **kwargs):
        """记录critical级别日志"""
        logger.opt(depth=1).critical(message, **kwargs)

    async def close(self):
        """关闭日志器"""
        pass  # loguru不需要显式关闭
