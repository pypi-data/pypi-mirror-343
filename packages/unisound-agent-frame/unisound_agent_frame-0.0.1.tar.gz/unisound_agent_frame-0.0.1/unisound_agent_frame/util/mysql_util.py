from typing import Dict, Any, List, Optional

import aiomysql


class MySQLUtil:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MySQLUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self, config: Dict[str, Any]):
        if not hasattr(self, 'initialized'):
            self.config = config
            self.pool = None

    async def init_pool(self):
        """初始化连接池"""
        if self.pool is None:
            self.pool = await aiomysql.create_pool(
                host=self.config.get('host', 'localhost'),
                port=self.config.get('port', 3306),
                user=self.config.get('user', 'root'),
                password=self.config.get('password', ''),
                db=self.config.get('database', 'test'),
                charset=self.config.get('charset', 'utf8'),
                autocommit=True
            )
        self.initialized = True

    async def init_tables(self):
        """初始化数据表"""
        create_service_logs_table = """
        CREATE TABLE IF NOT EXISTS service_logs (
            id bigint(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
            agent_id VARCHAR(100) COMMENT '智能体标识',
            request_id VARCHAR(36) COMMENT '请求唯一ID',
            request_time DATETIME COMMENT '请求时间',
            request_data TEXT COMMENT '请求数据',
            response_data TEXT COMMENT '响应数据',
            status INT COMMENT '状态码',
            error_message TEXT COMMENT '错误信息',
            cost_time INT COMMENT '总耗时',
            created_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
            PRIMARY KEY (`id`,`created_time`) USING BTREE,
            INDEX idx_request_id (`request_id`) USING BTREE,
            INDEX idx_created_time (`created_time`) USING BTREE
        )ENGINE = InnoDB AUTO_INCREMENT = 0 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact
        """
        await self.execute(create_service_logs_table)

    async def execute(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[tuple]:
        """执行SQL语句"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, params)
                return await cur.fetchall()

    async def save_service_log(self, log_data: Dict[str, Any]):
        """保存服务日志"""
        sql = """
        INSERT INTO service_logs (
            agent_id, request_id, request_time, request_data, 
            response_data, status, error_message, cost_time
        ) VALUES (
            %(agent_id)s, %(request_id)s, %(request_time)s, %(request_data)s,
            %(response_data)s, %(status)s, %(error_message)s, %(cost_time)s
        )
        """
        await self.execute(sql, log_data)

    async def get_service_log(self, request_id: str) -> Optional[Dict[str, Any]]:
        """根据request_id获取服务日志"""
        sql = """
        SELECT agent_id, request_id, request_time, request_data, 
               response_data, status, error_message, cost_time, created_time
        FROM service_logs 
        WHERE request_id = %s
        """
        results = await self.execute(sql, {'request_id': request_id})
        if results:
            row = results[0]
            return {
                'agent_id': row[0],
                'request_id': row[1],
                'request_time': row[2].isoformat(),
                'request_data': row[3],
                'response_data': row[4],
                'status': row[5],
                'error_message': row[6],
                'cost_time': row[7],
                'created_time': row[8].isoformat()
            }
        return None

    async def close(self):
        """关闭连接池"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
