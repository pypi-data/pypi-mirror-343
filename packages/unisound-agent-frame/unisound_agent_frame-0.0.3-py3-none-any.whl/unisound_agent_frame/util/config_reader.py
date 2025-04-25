import os
import yaml
from typing import Any, Dict, Optional

class ConfigReader:
    _instance = None
    _config_cache: Dict[str, Any] = {}
    _env: Optional[str] = None  # 缓存当前环境

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
        return cls._instance

    @classmethod
    def _get_env(cls) -> str:
        """获取当前环境，优先级：环境变量 > 配置文件 > 默认dev"""
        if cls._env is not None:
            return cls._env

        # 1. 检查环境变量
        env = os.environ.get("SERVICE_ENV", "").lower()
        if env:
            cls._env = env
            return env

        # 2. 检查配置文件
        settings_path = os.path.join(os.getcwd(), 'config', 'settings.yml')
        try:
            config = cls.read_yaml(settings_path)
            env = config.get("service_env", "dev").lower()
            cls._env = env
            return env
        except FileNotFoundError:
            pass

        # 3. 默认值
        cls._env = "dev"
        return cls._env

    @staticmethod
    def read_yaml(file_path: str) -> Dict[str, Any]:
        """读取并缓存YAML配置文件"""
        if file_path in ConfigReader._config_cache:
            return ConfigReader._config_cache[file_path]

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"配置文件不存在: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                config = yaml.safe_load(f)
                ConfigReader._config_cache[file_path] = config
                return config
            except yaml.YAMLError as e:
                raise ValueError(f"YAML解析错误: {file_path} - {str(e)}")

    @classmethod
    def get_frame_config(cls, config_path: Optional[str] = None) -> Dict[str, Any]:
        """根据环境读取frame配置"""
        if config_path is None:
            env = cls._get_env()
            config_path = os.path.join(os.getcwd(),'config', f'frame_{env}.yml')
        return cls.read_yaml(config_path)

    @classmethod
    def get_agent_config(cls, agent_type: str, config_path: Optional[str] = None) -> Dict[str, Any]:
        """根据环境读取agent配置"""
        if config_path is None:
            config_path = os.path.join(os.getcwd(), 'config', f'{agent_type}.yml')
        return cls.read_yaml(config_path)

    @classmethod
    def get_settings_config(cls, config_path: Optional[str] = None) -> Dict[str, Any]:
        """根据环境读取setting配置"""
        if config_path is None:
            config_path = os.path.join(os.getcwd(), 'config', f'settings.yml')
        return cls.read_yaml(config_path)
    @classmethod
    def clear_cache(cls):
        """清除配置缓存及环境缓存"""
        cls._config_cache.clear()
        cls._env = None