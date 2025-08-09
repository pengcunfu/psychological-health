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
    domain: str = ''

    @classmethod
    def from_yaml(cls, config_path: str = None):
        path = config_path or os.environ.get('CONFIG_PATH') or DEFAULT_CONFIG_PATH
        if not os.path.exists(path):
            return cls()
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        obj = cls()
        for k, v in data.items():
            # 将配置键转换为小写进行匹配
            lower_k = k.lower()
            # 检查类中是否有对应的小写属性
            for attr_name in dir(obj):
                if attr_name.lower() == lower_k and not attr_name.startswith('_') and not callable(getattr(obj, attr_name)):
                    setattr(obj, attr_name, v)
                    break
        return obj


def get_config():
    """
    获取配置字典，用于Redis客户端等需要字典格式配置的模块
    """
    config_path = os.environ.get('CONFIG_PATH') or DEFAULT_CONFIG_PATH
    if not os.path.exists(config_path):
        # 返回默认配置
        return {
            'debug': True,
            'secret_key': 'dev-secret-key',
            'database_uri': 'sqlite:///dev.db',
            'cors_origins': '*',
            'domain': '',
            'code': {
                'smtp_server': 'smtp.qq.com',
                'smtp_port': 587,
                'use_tls': True,
                'sender_email': '',
                'sender_password': '',
                'sender_name': '心理健康平台'
            },
            'redis': {
                'host': 'localhost',
                'port': 6379,
                'db': 0,
                'password': None,
                'decode_responses': True
            },
            'session': {
                'type': 'redis',
                'permanent': False,
                'use_signer': True,
                'key_prefix': 'session:',
                'redis_key_prefix': 'session:',
                'cookie_httponly': True,
                'cookie_secure': False,
                'expires': 7200
            }
        }
    
    with open(config_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    
    # 处理环境变量替换
    data = _process_env_vars(data)
    
    # 将所有键转换为小写
    data = _normalize_keys_to_lowercase(data)
    
    # 确保包含默认的Redis和Session配置
    if 'redis' not in data:
        data['redis'] = {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'password': None,
            'decode_responses': True
        }
    
    if 'session' not in data:
        data['session'] = {
            'type': 'redis',
            'permanent': False,
            'use_signer': True,
            'key_prefix': 'session:',
            'redis_key_prefix': 'session:',
            'cookie_httponly': True,
            'cookie_secure': False,
            'expires': 7200
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


def _normalize_keys_to_lowercase(data):
    """
    递归将配置字典的所有键转换为小写
    """
    if isinstance(data, dict):
        return {k.lower(): _normalize_keys_to_lowercase(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_normalize_keys_to_lowercase(item) for item in data]
    else:
        return data
