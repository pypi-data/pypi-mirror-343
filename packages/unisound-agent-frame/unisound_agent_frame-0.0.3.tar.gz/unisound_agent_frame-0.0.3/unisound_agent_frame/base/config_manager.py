import asyncio
from unisound_agent_frame.util.config_reader import ConfigReader
from unisound_agent_frame.util.data_logger import DataLogger
from unisound_agent_frame.util.logger import MyLogger
from unisound_agent_frame.util.mysql_util import MySQLUtil

class ConfigManager:
    def __init__(self):
        self.config = None
        self.settings_config = None
        self.logger = None
        self.mysql = None
        self.data_logger = None

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

    async def close(self):
        """关闭配置管理器，释放资源"""
        try:
            if self.mysql:
                await self.mysql.close()
            if self.logger:
                await self.logger.close()
        except Exception as e:
            print(f"配置管理器关闭失败: {str(e)}")
            raise