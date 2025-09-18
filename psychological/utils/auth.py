"""
认证相关工具函数
提供密码哈希、令牌生成等认证功能
"""
import hashlib
import uuid


def hash_password(password: str) -> str:
    """
    密码哈希

    Args:
        password: 明文密码

    Returns:
        str: 哈希后的密码
    """
    return hashlib.md5(password.encode()).hexdigest()


def generate_token() -> str:
    """
    生成访问令牌

    Returns:
        str: 32位随机令牌
    """
    return str(uuid.uuid4()).replace('-', '')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    验证密码

    Args:
        password: 明文密码
        hashed_password: 哈希后的密码

    Returns:
        bool: 密码是否匹配
    """
    return hash_password(password) == hashed_password
