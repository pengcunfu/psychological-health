"""
验证码缓存工具
提供验证码的Redis存储、获取、删除等功能
"""
from flask import session
from utils.redis_client import RedisClient
from utils.logger_client import get_logger

logger = get_logger(__name__)


class VerifyCodeCache:
    """验证码缓存管理类"""
    
    def __init__(self):
        self.redis_client = RedisClient()
        self.verify_code_prefix = "verify_code:"
        self.expire_time = 300  # 5分钟过期时间
    
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
        """
        try:
            if self.redis_client.is_available():
                key = self._get_verify_code_key(identifier)
                # 设置5分钟过期时间
                result = self.redis_client.client.setex(key, self.expire_time, code)
                logger.info(f"验证码已存储到Redis: key={key}, code={code}, result={result}")
                return bool(result)
            else:
                # Redis不可用时，降级到session存储
                session_key = f'verify_code_{identifier}'
                session[session_key] = code
                logger.warning(f"Redis不可用，验证码已存储到session: {session_key}={code}")
                return True
        except Exception as e:
            logger.error(f"存储验证码失败: {e}")
            # 如果Redis操作失败，降级到session存储
            try:
                session_key = f'verify_code_{identifier}'
                session[session_key] = code
                logger.warning(f"Redis存储失败，降级到session: {session_key}={code}")
                return True
            except Exception as session_error:
                logger.error(f"Session存储也失败: {session_error}")
                return False
    
    def get_verify_code(self, identifier: str) -> str:
        """
        从Redis获取验证码
        
        Args:
            identifier: 标识符（UUID）
            
        Returns:
            str: 验证码，如果不存在返回None
        """
        try:
            if self.redis_client.is_available():
                key = self._get_verify_code_key(identifier)
                code = self.redis_client.client.get(key)
                logger.info(f"从Redis获取验证码: key={key}, code={code}")
                return code if code else None
            else:
                # Redis不可用时，从session获取
                session_key = f'verify_code_{identifier}'
                code = session.get(session_key)
                logger.warning(f"Redis不可用，从session获取验证码: {session_key}={code}")
                return code
        except Exception as e:
            logger.error(f"获取验证码失败: {e}")
            # 如果Redis操作失败，从session获取
            try:
                session_key = f'verify_code_{identifier}'
                code = session.get(session_key)
                logger.warning(f"Redis获取失败，从session获取: {session_key}={code}")
                return code
            except Exception as session_error:
                logger.error(f"Session获取也失败: {session_error}")
                return None
    
    def delete_verify_code(self, identifier: str) -> bool:
        """
        删除验证码
        
        Args:
            identifier: 标识符（UUID）
            
        Returns:
            bool: 删除是否成功
        """
        try:
            if self.redis_client.is_available():
                key = self._get_verify_code_key(identifier)
                result = self.redis_client.client.delete(key)
                logger.info(f"从Redis删除验证码: key={key}, result={result}")
                return result > 0
            else:
                # Redis不可用时，清除session中的验证码
                session_key = f'verify_code_{identifier}'
                session.pop(session_key, None)
                logger.warning(f"Redis不可用，从session删除验证码: {session_key}")
                return True
        except Exception as e:
            logger.error(f"删除验证码失败: {e}")
            # 如果Redis操作失败，清除session中的验证码
            try:
                session_key = f'verify_code_{identifier}'
                session.pop(session_key, None)
                logger.warning(f"Redis删除失败，从session删除: {session_key}")
                return True
            except Exception as session_error:
                logger.error(f"Session删除也失败: {session_error}")
                return False
    
    def verify_code(self, identifier: str, input_code: str) -> bool:
        """
        验证验证码
        
        Args:
            identifier: 标识符（UUID）
            input_code: 用户输入的验证码
            
        Returns:
            bool: 验证是否成功
        """
        if not input_code:
            logger.warning("验证码为空")
            return False
            
        stored_code = self.get_verify_code(identifier)
        if not stored_code:
            logger.warning(f"未找到验证码: identifier={identifier}")
            return False
            
        # 验证码不区分大小写
        is_valid = stored_code.lower() == input_code.lower()
        logger.info(f"验证码验证: identifier={identifier}, input={input_code}, stored={stored_code}, valid={is_valid}")
        
        # 验证成功后删除验证码，防止重复使用
        if is_valid:
            self.delete_verify_code(identifier)
            
        return is_valid


# 全局验证码缓存实例
verify_code_cache = VerifyCodeCache()