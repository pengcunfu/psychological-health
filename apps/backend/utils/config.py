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


def get_config():
    """
    获取配置字典，用于Redis客户端等需要字典格式配置的模块
    """
    config_path = os.environ.get('CONFIG_PATH') or DEFAULT_CONFIG_PATH
    if not os.path.exists(config_path):
        # 返回默认配置
        return {
            'DEBUG': True,
            'SECRET_KEY': 'dev-secret-key',
            'DATABASE_URI': 'sqlite:///dev.db',
            'CORS_ORIGINS': '*',
            'REDIS': {
                'HOST': 'localhost',
                'PORT': 6379,
                'DB': 0,
                'PASSWORD': None,
                'DECODE_RESPONSES': True
            },
            'SESSION': {
                'TYPE': 'redis',
                'PERMANENT': False,
                'USE_SIGNER': True,
                'KEY_PREFIX': 'session:',
                'REDIS_KEY_PREFIX': 'session:',
                'COOKIE_HTTPONLY': True,
                'COOKIE_SECURE': False,
                'EXPIRES': 7200
            }
        }
    
    with open(config_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    
    # 处理环境变量替换
    data = _process_env_vars(data)
    
    # 确保包含默认的Redis和Session配置
    if 'REDIS' not in data:
        data['REDIS'] = {
            'HOST': 'localhost',
            'PORT': 6379,
            'DB': 0,
            'PASSWORD': None,
            'DECODE_RESPONSES': True
        }
    
    if 'SESSION' not in data:
        data['SESSION'] = {
            'TYPE': 'redis',
            'PERMANENT': False,
            'USE_SIGNER': True,
            'KEY_PREFIX': 'session:',
            'REDIS_KEY_PREFIX': 'session:',
            'COOKIE_HTTPONLY': True,
            'COOKIE_SECURE': False,
            'EXPIRES': 7200
        }
    
    return data


def _process_env_vars(data):
    """
    递归处理配置中的环境变量替换
    支持 ${VAR_NAME:-default_value} 格式
    """
    if isinstance(data, dict):
        return {k: _process_env_vars(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_process_env_vars(item) for item in data]
    elif isinstance(data, str) and data.startswith('${') and data.endswith('}'):
        # 解析环境变量格式 ${VAR_NAME:-default_value}
        env_expr = data[2:-1]  # 移除 ${ 和 }
        if ':-' in env_expr:
            var_name, default_value = env_expr.split(':-', 1)
            value = os.environ.get(var_name.strip(), default_value.strip())
        else:
            var_name = env_expr.strip()
            value = os.environ.get(var_name, data)
        
        # 尝试转换数据类型
        if value == 'null' or value == 'None':
            return None
        elif value == 'true' or value == 'True':
            return True
        elif value == 'false' or value == 'False':
            return False
        elif value.isdigit():
            return int(value)
        else:
            return value
    else:
        return data
