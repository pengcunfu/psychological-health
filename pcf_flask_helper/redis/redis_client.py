"""
Redis客户端工具
提供Redis连接和会话管理功能
"""
import json
import time
from typing import Optional, Dict, Any, Union

# 按需导入redis
try:
    import redis
except ImportError as e:
    raise ImportError(
        "Redis客户端需要安装redis依赖。请运行以下命令安装：\n"
        "pip install redis>=4.0.0"
    ) from e


class RedisClient:
    """Redis客户端类"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, 
                 password: Optional[str] = None, decode_responses: bool = True,
                 socket_connect_timeout: int = 5, socket_timeout: int = 5,
                 retry_on_timeout: bool = True):
        """
        初始化Redis连接
        
        Args:
            host: Redis服务器地址
            port: Redis服务器端口
            db: Redis数据库编号
            password: Redis密码
            decode_responses: 是否解码响应
            socket_connect_timeout: 连接超时时间
            socket_timeout: 套接字超时时间
            retry_on_timeout: 超时时是否重试
        """
        # 参数验证
        if not host:
            raise ValueError("Redis主机地址不能为空")
        if not isinstance(port, int) or port <= 0:
            raise ValueError("Redis端口必须是正整数")
        if not isinstance(db, int) or db < 0:
            raise ValueError("Redis数据库编号必须是非负整数")
        
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self.socket_connect_timeout = socket_connect_timeout
        self.socket_timeout = socket_timeout
        self.retry_on_timeout = retry_on_timeout
        
        # 创建Redis连接
        self._redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=decode_responses,
            socket_connect_timeout=socket_connect_timeout,
            socket_timeout=socket_timeout,
            retry_on_timeout=retry_on_timeout
        )
        
        # 测试连接
        try:
            self._redis_client.ping()
        except Exception as e:
            raise Exception(f"Redis连接失败: {str(e)}") from e

    @property
    def client(self):
        """获取Redis客户端"""
        return self._redis_client

    def is_available(self) -> bool:
        """检查Redis是否可用"""
        try:
            self._redis_client.ping()
            return True
        except Exception:
            return False
    
    def get(self, key: str) -> Optional[str]:
        """获取键值"""
        try:
            return self._redis_client.get(key)
        except Exception as e:
            raise Exception(f"获取键值失败: {str(e)}") from e
    
    def set(self, key: str, value: Union[str, int, float], ex: Optional[int] = None) -> bool:
        """设置键值"""
        try:
            return self._redis_client.set(key, value, ex=ex)
        except Exception as e:
            raise Exception(f"设置键值失败: {str(e)}") from e
    
    def delete(self, *keys: str) -> int:
        """删除键"""
        try:
            return self._redis_client.delete(*keys)
        except Exception as e:
            raise Exception(f"删除键失败: {str(e)}") from e
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        try:
            return self._redis_client.exists(key) > 0
        except Exception as e:
            raise Exception(f"检查键存在失败: {str(e)}") from e
    
    def expire(self, key: str, time: int) -> bool:
        """设置键过期时间"""
        try:
            return self._redis_client.expire(key, time)
        except Exception as e:
            raise Exception(f"设置过期时间失败: {str(e)}") from e
    
    def keys(self, pattern: str = "*") -> list:
        """获取匹配模式的键列表"""
        try:
            return self._redis_client.keys(pattern)
        except Exception as e:
            raise Exception(f"获取键列表失败: {str(e)}") from e


class SessionManager:
    """基于Redis的会话管理器"""
    
    def __init__(self, redis_client: RedisClient, session_prefix: str = "session:", 
                 session_expires: int = 7200):
        """
        初始化会话管理器
        
        Args:
            redis_client: Redis客户端实例
            session_prefix: 会话键前缀
            session_expires: 会话过期时间（秒）
        """
        if not isinstance(redis_client, RedisClient):
            raise ValueError("redis_client必须是RedisClient实例")
        if not session_prefix:
            raise ValueError("会话键前缀不能为空")
        if not isinstance(session_expires, int) or session_expires <= 0:
            raise ValueError("会话过期时间必须是正整数")
        
        self.redis_client = redis_client
        self.session_prefix = session_prefix
        self.session_expires = session_expires

    def _get_session_key(self, token: str) -> str:
        """获取会话键名"""
        return f"{self.session_prefix}{token}"

    def create_session(self, token: str, user_data: Dict[str, Any]) -> bool:
        """创建会话"""
        if not token:
            raise ValueError("会话令牌不能为空")
        if not isinstance(user_data, dict):
            raise ValueError("用户数据必须是字典类型")
        
        try:
            session_key = self._get_session_key(token)
            session_data = json.dumps(user_data, ensure_ascii=False)
            return self.redis_client.set(session_key, session_data, ex=self.session_expires)
        except Exception as e:
            raise Exception(f"创建会话失败: {str(e)}") from e

    def get_session(self, token: str) -> Optional[Dict[str, Any]]:
        """获取会话"""
        if not token:
            raise ValueError("会话令牌不能为空")
        
        try:
            session_key = self._get_session_key(token)
            session_data = self.redis_client.get(session_key)
            
            if session_data:
                return json.loads(session_data)
            return None
        except Exception as e:
            raise Exception(f"获取会话失败: {str(e)}") from e

    def update_session(self, token: str, user_data: Dict[str, Any]) -> bool:
        """更新会话"""
        if not token:
            raise ValueError("会话令牌不能为空")
        if not isinstance(user_data, dict):
            raise ValueError("用户数据必须是字典类型")
        
        try:
            session_key = self._get_session_key(token)
            
            # 检查会话是否存在
            if not self.redis_client.exists(session_key):
                return False
            
            session_data = json.dumps(user_data, ensure_ascii=False)
            return self.redis_client.set(session_key, session_data, ex=self.session_expires)
        except Exception as e:
            raise Exception(f"更新会话失败: {str(e)}") from e

    def destroy_session(self, token: str) -> bool:
        """销毁会话"""
        if not token:
            raise ValueError("会话令牌不能为空")
        
        try:
            session_key = self._get_session_key(token)
            return self.redis_client.delete(session_key) > 0
        except Exception as e:
            raise Exception(f"销毁会话失败: {str(e)}") from e

    def extend_session(self, token: str) -> bool:
        """延长会话有效期"""
        if not token:
            raise ValueError("会话令牌不能为空")
        
        try:
            session_key = self._get_session_key(token)
            return self.redis_client.expire(session_key, self.session_expires)
        except Exception as e:
            raise Exception(f"延长会话有效期失败: {str(e)}") from e

    def get_session_count(self) -> int:
        """获取会话总数"""
        try:
            pattern = f"{self.session_prefix}*"
            keys = self.redis_client.keys(pattern)
            return len(keys)
        except Exception as e:
            raise Exception(f"获取会话总数失败: {str(e)}") from e
