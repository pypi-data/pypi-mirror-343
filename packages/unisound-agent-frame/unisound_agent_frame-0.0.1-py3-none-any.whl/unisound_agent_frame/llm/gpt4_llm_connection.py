import aiohttp
from typing import Dict, Any, Optional, List
from unisound_agent_frame.llm.llm_connection import LLMConnection

class GPT4LLMConnection(LLMConnection):
    """GPT4模型连接实现"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.api_key: Optional[str] = None
        self.base_url: Optional[str] = None
        self.model: str = "gpt-4"
        self.initialized: bool = False
        
    async def init(self, config: Dict[str, Any]):
        """初始化连接"""
        if self.initialized:
            return
            
        self.api_key = config.get('api_key')
        self.base_url = config.get('base_url', 'https://api.openai.com/v1')
        self.model = config.get('model', 'gpt-4')
        
        if not self.api_key:
            raise ValueError("GPT4 API key is required")
            
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        self.initialized = True
        
    async def chat(self, messages: List[Dict],task_id: Optional[str] = None,** kwargs) -> str:
        """发送对话请求"""
        if not self.initialized:
            raise RuntimeError("Connection not initialized")
            
        data = {
            "model": self.model,
            "messages": messages,
            **kwargs
        }
        
        async with self.session.post(f"{self.base_url}/chat/completions", json=data) as response:
            response.raise_for_status()
            return await response.json()
            
    async def close(self):
        """关闭连接"""
        if self.session:
            await self.session.close()
            self.initialized = False
            
    def is_available(self) -> bool:
        """检查连接是否可用"""
        return self.initialized and self.session is not None
        
    def get_model_type(self) -> str:
        """获取模型类型"""
        return "GPT4" 