from flask import request
from typing import List, Optional, Dict, Any
from psychological.utils.cache.redis_client import session_manager
from psychological.utils.exceptions import UnauthorizedError


def _get_current_user_from_redis() -> Optional[Dict[Any, Any]]:
    """从Redis获取当前用户信息

    Returns:
        Optional[Dict]: 用户信息字典，如果未登录则返回None
    """
    try:
        # 从请求头获取token
        token = request.headers.get('Authorization')
        if not token:
            return None

        # 移除Bearer前缀
        if token.startswith('Bearer '):
            token = token[7:]

        # 从Redis获取会话信息
        user_info = session_manager.get_session(token)
        if user_info:
            # 延长会话有效期
            session_manager.extend_session(token)
            return user_info

        return None
    except Exception:
        return None


def assert_current_user_id() -> str:
    """获取当前登录用户的user_id

    Returns:
        str: 用户ID

    Raises:
        UnauthorizedError: 如果用户未登录
    """
    try:
        session_info = _get_current_user_from_redis()
        if session_info:
            # 从session中获取user_id字段
            user_id = session_info.get('user_id')
            if user_id:
                return user_id

            # 如果没有user_id，尝试从user_data中获取
            user_data = session_info.get('user', {})
            user_id = user_data.get('id')
            if user_id:
                return user_id

        # 如果没有获取到用户ID，抛出未登录异常
        raise UnauthorizedError("用户未登录")
    except UnauthorizedError:
        # 重新抛出UnauthorizedError
        raise
    except Exception:
        # 其他异常也视为未登录
        raise UnauthorizedError("用户未登录")


def get_roles() -> List[str]:
    """获取当前用户的角色列表

    Returns:
        List[str]: 角色代码列表，如果未登录或无角色则返回空列表
    """
    try:
        session_info = _get_current_user_from_redis()
        if session_info:
            # 从user_data中获取roles
            roles = session_info.get('roles', {})

            role_codes = []
            for role in roles:
                code = role.get('code')
                if code:
                    role_codes.append(code)
            return role_codes

        return []
    except Exception:
        return []


def get_current_user() -> Optional[Dict[Any, Any]]:
    """获取当前用户完整信息

    Returns:
        Optional[Dict]: 用户信息字典，如果未登录则返回None
    """
    session_info = _get_current_user_from_redis()
    if session_info:
        return session_info.get('user', {})
    return None


def get_session_info() -> Optional[Dict[Any, Any]]:
    """获取完整的会话信息（包含user_data、token等）

    Returns:
        Optional[Dict]: 会话信息字典，如果未登录则返回None
    """
    return _get_current_user_from_redis()


def get_role_objects() -> List[Dict[str, Any]]:
    """获取当前用户的角色对象列表（包含id、name、code）

    Returns:
        List[Dict]: 角色对象列表，如果未登录或无角色则返回空列表
    """
    try:
        session_info = _get_current_user_from_redis()
        if session_info:
            roles = session_info.get('roles', [])
            return [role for role in roles if isinstance(role, dict)]
    except Exception as e:
        pass
    return []


def get_role_names() -> List[str]:
    """获取当前用户的角色名称列表

    Returns:
        List[str]: 角色名称列表，如果未登录或无角色则返回空列表
    """
    try:
        role_objects = get_role_objects()
        return [role.get('name', '') for role in role_objects if role.get('name')]
    except Exception:
        return []


def is_admin() -> bool:
    """检查当前用户是否为管理员

    Returns:
        bool: 是否为管理员
    """
    roles = get_roles()
    return 'admin' in [role.lower() for role in roles]


def is_manager() -> bool:
    """检查当前用户是否为管理者

    Returns:
        bool: 是否为管理者
    """
    roles = get_roles()
    return 'manager' in [role.lower() for role in roles]


def is_manager_user() -> bool:
    """检查当前用户是否具有管理权限（管理员或管理者）

    Returns:
        bool: 是否为管理员或管理者
    """
    roles = get_roles()
    user_roles_lower = [role.lower() for role in roles]
    return 'admin' in user_roles_lower or 'manager' in user_roles_lower


def has_role(role: str) -> bool:
    """检查当前用户是否具有指定角色

    Args:
        role (str): 角色名称

    Returns:
        bool: 是否具有该角色
    """
    roles = get_roles()
    return role.lower() in [r.lower() for r in roles]


def has_any_role(required_roles: List[str]) -> bool:
    """检查当前用户是否具有任意一个指定角色

    Args:
        required_roles (List[str]): 所需角色列表

    Returns:
        bool: 是否具有任意一个角色
    """
    user_roles = [role.lower() for role in get_roles()]
    required_roles_lower = [role.lower() for role in required_roles]
    return any(role in user_roles for role in required_roles_lower)
