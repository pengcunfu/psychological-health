"""
Redis客户端工具
提供Redis连接和会话管理功能
"""
import redis
import json
import threading
import time
from typing import Optional, Dict, Any
from psychological.utils.config import get_config
from psychological.utils.logger_client import get_logger

logger = get_logger(__name__)


class RedisClient:
    """Redis客户端类"""

    _instance = None
    _redis_client = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化Redis连接"""
        if self._redis_client is None:
            self._init_redis()

    def _init_redis(self):
        """初始化Redis连接"""
        try:
            config = get_config()
            redis_config = config.get('REDIS', {})

            self._redis_client = redis.Redis(
                host=redis_config.get('HOST', 'localhost'),
                port=redis_config.get('PORT', 6379),
                db=redis_config.get('DB', 0),
                password=redis_config.get('PASSWORD'),
                decode_responses=redis_config.get('DECODE_RESPONSES', True),
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )

            # 测试连接
            self._redis_client.ping()
            logger.info("Redis连接成功")

        except Exception as e:
            logger.error(f"Redis连接失败: {e}")
            # 如果Redis连接失败，使用内存存储作为降级方案
            self._redis_client = None
            raise e

    @property
    def client(self):
        """获取Redis客户端"""
        if self._redis_client is None:
            self._init_redis()
        return self._redis_client

    def is_available(self) -> bool:
        """检查Redis是否可用"""
        try:
            if self._redis_client is None:
                return False
            self._redis_client.ping()
            return True
        except Exception:
            return False


class SessionManager:
    """基于Redis的会话管理器"""

    def __init__(self):
        self.redis_client = RedisClient()
        self.session_prefix = get_config().get(
            'SESSION', {}).get('KEY_PREFIX', 'session:')
        self.session_expires = get_config().get(
            'SESSION', {}).get('EXPIRES', 7200)  # 默认2小时

        # 如果Redis不可用，使用内存存储作为降级方案
        self._memory_sessions = {}
        self._cleanup_thread = None
        self._cleanup_running = False

        # 启动内存会话清理线程
        self._start_cleanup_thread()

    def _start_cleanup_thread(self):
        """启动内存会话清理线程"""
        if not self.redis_client.is_available() and not self._cleanup_running:
            self._cleanup_running = True
            self._cleanup_thread = threading.Thread(
                target=self._cleanup_worker, daemon=True)
            self._cleanup_thread.start()
            logger.info("内存会话清理线程已启动")

    def _cleanup_worker(self):
        """清理线程工作函数"""
        while self._cleanup_running:
            try:
                if not self.redis_client.is_available():
                    self.cleanup_expired_sessions()
                time.sleep(300)  # 每5分钟清理一次
            except Exception as e:
                logger.error(f"会话清理线程错误: {e}")
                time.sleep(60)  # 出错后等待1分钟再重试

    def _get_session_key(self, token: str) -> str:
        """获取会话键名"""
        return f"{self.session_prefix}{token}"

    def create_session(self, token: str, user_data: Dict[str, Any]) -> bool:
        """创建会话"""
        try:
            session_key = self._get_session_key(token)
            session_data = json.dumps(user_data, ensure_ascii=False)

            if self.redis_client.is_available():
                # 使用Redis存储
                result = self.redis_client.client.setex(
                    session_key,
                    self.session_expires,
                    session_data
                )
                logger.info(f"会话已创建到Redis: {token[:8]}...")
                return result
            else:
                # 降级到内存存储
                self._memory_sessions[token] = {
                    'data': user_data,
                    'expires_at': time.time() + self.session_expires
                }
                logger.warning(f"Redis不可用，会话已创建到内存: {token[:8]}...")
                # 确保清理线程正在运行
                if not self._cleanup_running:
                    self._start_cleanup_thread()
                return True

        except Exception as e:
            logger.error(f"创建会话失败: {e}")
            return False

    def get_session(self, token: str) -> Optional[Dict[str, Any]]:
        """获取会话"""
        try:
            if self.redis_client.is_available():
                # 从Redis获取
                session_key = self._get_session_key(token)
                session_data = self.redis_client.client.get(session_key)

                if session_data:
                    return json.loads(session_data)
                return None
            else:
                # 从内存获取
                session = self._memory_sessions.get(token)
                if session:
                    if time.time() < session['expires_at']:
                        return session['data']
                    else:
                        # 会话已过期，删除
                        del self._memory_sessions[token]
                return None

        except Exception as e:
            logger.error(f"获取会话失败: {e}")
            return None

    def update_session(self, token: str, user_data: Dict[str, Any]) -> bool:
        """更新会话"""
        try:
            if self.redis_client.is_available():
                # 更新Redis中的会话
                session_key = self._get_session_key(token)
                session_data = json.dumps(user_data, ensure_ascii=False)

                # 检查会话是否存在
                if self.redis_client.client.exists(session_key):
                    result = self.redis_client.client.setex(
                        session_key,
                        self.session_expires,
                        session_data
                    )
                    logger.info(f"会话已更新到Redis: {token[:8]}...")
                    return result
                return False
            else:
                # 更新内存中的会话
                if token in self._memory_sessions:
                    self._memory_sessions[token] = {
                        'data': user_data,
                        'expires_at': time.time() + self.session_expires
                    }
                    logger.warning(f"Redis不可用，会话已更新到内存: {token[:8]}...")
                    return True
                return False

        except Exception as e:
            logger.error(f"更新会话失败: {e}")
            return False

    def destroy_session(self, token: str) -> bool:
        """销毁会话"""
        try:
            if self.redis_client.is_available():
                # 从Redis删除
                session_key = self._get_session_key(token)
                result = self.redis_client.client.delete(session_key)
                logger.info(f"会话已从Redis删除: {token[:8]}...")
                return result > 0
            else:
                # 从内存删除
                if token in self._memory_sessions:
                    del self._memory_sessions[token]
                    logger.warning(f"Redis不可用，会话已从内存删除: {token[:8]}...")
                    return True
                return False

        except Exception as e:
            logger.error(f"销毁会话失败: {e}")
            return False

    def extend_session(self, token: str) -> bool:
        """延长会话有效期"""
        try:
            if self.redis_client.is_available():
                # 延长Redis中的会话
                session_key = self._get_session_key(token)
                result = self.redis_client.client.expire(
                    session_key, self.session_expires)
                if result:
                    logger.debug(f"会话有效期已延长: {token[:8]}...")
                return result
            else:
                # 延长内存中的会话
                if token in self._memory_sessions:
                    self._memory_sessions[token]['expires_at'] = time.time(
                    ) + self.session_expires
                    logger.debug(f"Redis不可用，内存会话有效期已延长: {token[:8]}...")
                    return True
                return False

        except Exception as e:
            logger.error(f"延长会话有效期失败: {e}")
            return False

    def get_session_count(self) -> int:
        """获取会话总数"""
        try:
            if self.redis_client.is_available():
                # 统计Redis中的会话数量
                pattern = f"{self.session_prefix}*"
                keys = self.redis_client.client.keys(pattern)
                return len(keys)
            else:
                # 统计内存中的会话数量（排除过期会话）
                current_time = time.time()
                active_sessions = 0
                for token, session in self._memory_sessions.items():
                    if current_time < session['expires_at']:
                        active_sessions += 1
                return active_sessions

        except Exception as e:
            logger.error(f"获取会话总数失败: {e}")
            return 0

    def cleanup_expired_sessions(self):
        """清理过期的内存会话（仅在降级模式下使用）"""
        if not self.redis_client.is_available():
            current_time = time.time()
            expired_tokens = []

            for token, session in self._memory_sessions.items():
                if current_time >= session['expires_at']:
                    expired_tokens.append(token)

            for token in expired_tokens:
                del self._memory_sessions[token]

            if expired_tokens:
                logger.info(f"已清理 {len(expired_tokens)} 个过期的内存会话")

    def shutdown(self):
        """关闭会话管理器"""
        self._cleanup_running = False
        if self._cleanup_thread and self._cleanup_thread.is_alive():
            self._cleanup_thread.join(timeout=5)
            logger.info("内存会话清理线程已停止")


# 全局会话管理器实例
session_manager = SessionManager()


# 初始化Redis连接
def init_redis():
    """初始化Redis连接"""
    try:
        if session_manager.redis_client.is_available():
            logger.info("Redis连接成功，会话将存储到Redis")
        else:
            logger.warning("Redis连接失败，会话将存储到内存（降级模式）")
    except Exception as e:
        logger.error(f"Redis初始化失败: {e}")
        logger.warning("将使用内存存储作为降级方案")
