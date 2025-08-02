import os
import yaml

DEFAULT_CONFIG_PATH = 'config.yaml'


class Config:
    """
    配置项定义，包含默认值，可通过 from_yaml 加载覆盖。
    """
    DEBUG: bool = True
    SECRET_KEY: str = 'dev-secret-key'
    DATABASE_URI: str = 'sqlite:///dev.db'
    CORS_ORIGINS: str = '*'

    @classmethod
    def from_yaml(cls, config_path: str = None):
        path = config_path or os.environ.get('CONFIG_PATH') or DEFAULT_CONFIG_PATH
        if not os.path.exists(path):
            return cls()
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        obj = cls()
        for k, v in data.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj
