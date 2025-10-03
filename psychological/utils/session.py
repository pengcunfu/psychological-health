# -*- coding: utf-8 -*-
"""
会话管理工具
提供Redis初始化、连接和会话管理功能
"""
from typing import Optional
from pcf_flask_helper.redis.redis_client import RedisClient, SessionManager
from psychological.config import cfg


class SessionService:
    """会话服务类 - 管理Redis连接和会话"""

    _redis_client: Optional[RedisClient] = None
    _session_manager: Optional[SessionManager] = None

    @classmethod
    def get_redis_client(cls) -> RedisClient:
        """获取Redis客户端实例"""
        if cls._redis_client is None:
            cls._redis_client = RedisClient(
                host=cfg.get("redis.host", "localhost"),
                port=int(cfg.get("redis.port", "6379")),
                db=int(cfg.get("redis.db", "0")),
                password=cfg.get("redis.password") or None,
                decode_responses=cfg.get("redis.decode_responses", True),
                socket_connect_timeout=int(cfg.get("redis.socket_connect_timeout", "5")),
                socket_timeout=int(cfg.get("redis.socket_timeout", "5")),
                retry_on_timeout=cfg.get("redis.retry_on_timeout", "true").lower() == "true"
            )
        return cls._redis_client

    @classmethod
    def get_session_manager(cls) -> SessionManager:
        """获取会话管理器实例"""
        if cls._session_manager is None:
            redis_client = cls.get_redis_client()
            cls._session_manager = SessionManager(
                redis_client=redis_client,
                session_prefix=cfg.get("session.key_prefix", "session:"),
                session_expires=int(cfg.get("session.expires", "7200"))
            )
        return cls._session_manager

    @classmethod
    def is_redis_available(cls) -> bool:
        """检查Redis是否可用"""
        try:
            redis_client = cls.get_redis_client()
            return redis_client.is_available()
        except Exception:
            return False

    @classmethod
    def reset_connections(cls):
        """重置连接（用于测试或重新初始化）"""
        cls._redis_client = None
        cls._session_manager = None


# 便捷函数
def get_redis_client() -> RedisClient:
    """获取Redis客户端"""
    return SessionService.get_redis_client()


def get_session_manager() -> SessionManager:
    """获取会话管理器"""
    return SessionService.get_session_manager()


def is_redis_available() -> bool:
    """检查Redis是否可用"""
    return SessionService.is_redis_available()
