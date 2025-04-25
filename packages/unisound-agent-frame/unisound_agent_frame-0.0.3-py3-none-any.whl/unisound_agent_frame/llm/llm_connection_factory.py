from typing import Dict, Type
from unisound_agent_frame.llm.llm_connection import LLMConnection
from unisound_agent_frame.llm.gpt4_llm_connection import GPT4LLMConnection
from unisound_agent_frame.llm.unigpt_llm_connection import UniGptLLMConnection

class LLMConnectionFactory:
    """LLM连接工厂类"""
    
    _connection_types: Dict[str, Type[LLMConnection]] = {
        "GPT4": GPT4LLMConnection,
        "UniGpt": UniGptLLMConnection
    }
    
    @classmethod
    def register_connection_type(cls, model_type: str, connection_class: Type[LLMConnection]):
        """注册新的连接类型
        Args:
            model_type: 模型类型
            connection_class: 连接类
        """
        cls._connection_types[model_type] = connection_class
    
    @classmethod
    def create_connection(cls, model_type: str) -> LLMConnection:
        """创建LLM连接
        Args:
            model_type: 模型类型
        Returns:
            LLMConnection实例
        Raises:
            ValueError: 如果模型类型未注册
        """
        connection_class = cls._connection_types.get(model_type)
        if not connection_class:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        return connection_class() 