"""
验证码缓存工具
提供验证码的Redis存储、获取、删除等功能
"""
from flask import session
from pcf_flask_helper.redis.redis_client import RedisClient
from psychological.utils.session import get_redis_client
from loguru import logger


class VerifyCodeCache:
    """验证码缓存管理类"""

    def __init__(self, redis_client: RedisClient = None, verify_code_prefix: str = "verify_code:", 
                 expire_time: int = 300):
        """
        初始化验证码缓存
        
        Args:
            redis_client: Redis客户端实例，如果为None则使用默认配置
            verify_code_prefix: 验证码键前缀
            expire_time: 过期时间（秒）
        """
        self.redis_client = redis_client or get_redis_client()
        self.verify_code_prefix = verify_code_prefix
        self.expire_time = expire_time

    def _get_verify_code_key(self, identifier: str) -> str:
        """生成验证码Redis键名"""
        return f"{self.verify_code_prefix}{identifier}"

    def store_verify_code(self, identifier: str, code: str) -> bool:
        """
        存储验证码到Redis
        
        Args:
            identifier: 标识符（UUID）
            code: 验证码
            
        Returns:
            bool: 存储是否成功
            
        Raises:
            ValueError: 参数错误
            Exception: 存储失败
        """
        if not identifier:
            raise ValueError("标识符不能为空")
        if not code:
            raise ValueError("验证码不能为空")
        
        try:
            key = self._get_verify_code_key(identifier)
            return self.redis_client.set(key, code, ex=self.expire_time)
        except Exception as e:
            raise Exception(f"存储验证码失败: {str(e)}") from e

    def get_verify_code(self, identifier: str) -> str:
        """
        从Redis获取验证码
        
        Args:
            identifier: 标识符（UUID）
            
        Returns:
            str: 验证码，如果不存在返回None
            
        Raises:
            ValueError: 参数错误
            Exception: 获取失败
        """
        if not identifier:
            raise ValueError("标识符不能为空")
        
        try:
            key = self._get_verify_code_key(identifier)
            return self.redis_client.get(key)
        except Exception as e:
            raise Exception(f"获取验证码失败: {str(e)}") from e

    def delete_verify_code(self, identifier: str) -> bool:
        """
        删除验证码
        
        Args:
            identifier: 标识符（UUID）
            
        Returns:
            bool: 删除是否成功
            
        Raises:
            ValueError: 参数错误
            Exception: 删除失败
        """
        if not identifier:
            raise ValueError("标识符不能为空")
        
        try:
            key = self._get_verify_code_key(identifier)
            return self.redis_client.delete(key) > 0
        except Exception as e:
            raise Exception(f"删除验证码失败: {str(e)}") from e

    def verify_code(self, identifier: str, input_code: str) -> bool:
        """
        验证验证码
        
        Args:
            identifier: 标识符（UUID）
            input_code: 用户输入的验证码
            
        Returns:
            bool: 验证是否成功
            
        Raises:
            ValueError: 参数错误
            Exception: 验证失败
        """
        if not identifier:
            raise ValueError("标识符不能为空")
        if not input_code:
            raise ValueError("验证码不能为空")

        try:
            stored_code = self.get_verify_code(identifier)
            if not stored_code:
                return False

            # 验证码不区分大小写
            is_valid = stored_code.lower() == input_code.lower()

            # 验证成功后删除验证码，防止重复使用
            if is_valid:
                self.delete_verify_code(identifier)

            return is_valid
        except Exception as e:
            raise Exception(f"验证验证码失败: {str(e)}") from e
