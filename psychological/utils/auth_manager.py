from functools import wraps
from flask import request
from typing import List, Optional
from psychological.utils.json_result import JsonResult
from psychological.utils.cache.redis_client import session_manager
from psychological.utils.logger_client import get_logger

logger = get_logger(__name__)


class AuthManager:
    """权限中间件"""

    @staticmethod
    def login_required(f):
        """登录验证装饰器"""

        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 从请求头获取token
            token = request.headers.get('Authorization')
            if not token:
                return JsonResult.error("未提供认证令牌", code=401)

            # 移除Bearer前缀
            if token.startswith('Bearer '):
                token = token[7:]

            # 从Redis验证token并获取用户信息
            user_info = session_manager.get_session(token)
            if not user_info:
                return JsonResult.error("认证令牌无效或已过期", code=401)

            # 延长会话有效期（每次访问都刷新）
            session_manager.extend_session(token)

            return f(*args, **kwargs)

        return decorated_function

    @staticmethod
    def permission_required(permission: str):
        """权限验证装饰器"""

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # 先检查登录状态
                token = request.headers.get('Authorization')
                if not token:
                    return JsonResult.error("未提供认证令牌", code=401)

                if token.startswith('Bearer '):
                    token = token[7:]

                # 从Redis获取用户信息
                user_info = session_manager.get_session(token)
                if not user_info:
                    return JsonResult.error("认证令牌无效或已过期", code=401)

                # 从Redis用户信息中获取用户ID
                user_id = user_info.get('user_id')
                if not user_id:
                    # 如果没有user_id，尝试从user_data中获取
                    user_data = user_info.get('user_data', {})
                    user_id = user_data.get('id')

                if not user_id:
                    return JsonResult.error("用户信息不完整", code=401)

                # 检查权限
                if not AuthManager._check_user_permission(user_id, permission):
                    return JsonResult.error("权限不足", code=403)

                # 延长会话有效期
                session_manager.extend_session(token)

                return f(*args, **kwargs)

            return decorated_function

        return decorator

    @staticmethod
    def role_required(roles: List[str]):
        """角色验证装饰器"""

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # 先检查登录状态
                token = request.headers.get('Authorization')
                if not token:
                    return JsonResult.error("未提供认证令牌", code=401)

                if token.startswith('Bearer '):
                    token = token[7:]

                # 从Redis获取用户信息
                user_info = session_manager.get_session(token)
                if not user_info:
                    return JsonResult.error("认证令牌无效或已过期", code=401)

                # 从Redis用户信息中获取用户ID
                user_id = user_info.get('user_id')
                if not user_id:
                    # 如果没有user_id，尝试从user_data中获取
                    user_data = user_info.get('user', {})
                    user_id = user_data.get('id')

                if not user_id:
                    return JsonResult.error("用户信息不完整", code=401)

                # 检查角色
                if not AuthManager._check_user_roles_from_redis(user_info, roles):
                    return JsonResult.error("角色权限不足", code=403)

                # 延长会话有效期
                session_manager.extend_session(token)

                return f(*args, **kwargs)

            return decorated_function

        return decorator

    @staticmethod
    def _check_user_permission(user_id: str, permission: str) -> bool:
        """检查用户是否有指定权限"""
        try:
            from models.user import User
            from models.role import Role
            from models.menu import Menu
            from models.user_role import UserRole

            user = User.query.filter_by(id=user_id).first()
            if not user:
                return False

            user_roles = UserRole.query.filter_by(user_id=user_id).all()
            user_role_ids = [ur.role_id for ur in user_roles]

            roles = Role.query.filter(Role.id.in_(user_role_ids)).all()
            for role in roles:
                if role.is_enabled():
                    menus = Menu.query.filter(Menu.id.in_(role.menu_ids)).all()
                    for menu in menus:
                        if menu.permission == permission and menu.status == 1:
                            return True

            return False
        except Exception as e:
            logger.error(f"检查用户权限失败: {e}")
            return False

    @staticmethod
    def _check_user_roles(user_id: str, required_roles: List[str]) -> bool:
        """检查用户是否有指定角色（从数据库查询）"""
        try:
            from models.user import User
            from models.role import Role
            from models.user_role import UserRole

            user = User.query.filter_by(id=user_id).first()
            if not user:
                return False

            user_roles = UserRole.query.filter_by(user_id=user_id).all()
            user_role_ids = [ur.role_id for ur in user_roles]

            roles = Role.query.filter(Role.id.in_(user_role_ids)).all()
            for role in roles:
                if role.is_enabled() and role.code in required_roles:
                    return True

            return False
        except Exception as e:
            logger.error(f"检查用户角色失败: {e}")
            return False

    @staticmethod
    def _check_user_roles_from_redis(user_info: dict, required_roles: List[str]) -> bool:
        """从Redis用户信息中检查用户是否有指定角色"""
        try:
            # 从user_data中获取角色信息
            user_data = user_info.get('user', {})
            roles = user_info.get('roles', [])

            # 提取角色代码
            user_role_codes = []
            for role in roles:
                if isinstance(role, dict):
                    code = role.get('code')
                    if code:
                        user_role_codes.append(code)
                elif isinstance(role, str):
                    user_role_codes.append(role)

            # 检查是否有匹配的角色
            for required_role in required_roles:
                if required_role in user_role_codes:
                    return True

            return False
        except Exception as e:
            logger.error(f"从Redis检查用户角色失败: {e}")
            return False

    @staticmethod
    def create_session(user_id: str, token: str, user_data: dict, roles_data: list[dict]):
        """创建用户会话"""
        session_data = {
            'user_id': user_id,
            'token': token,
            'user': user_data,
            'roles': roles_data,
            'login_ip': request.remote_addr
        }

        success = session_manager.create_session(token, session_data)
        if success:
            logger.info(f"用户 {user_id} 登录成功，会话已创建")
        else:
            logger.error(f"用户 {user_id} 会话创建失败")

        return success

    @staticmethod
    def destroy_session(token: str):
        """销毁用户会话"""
        success = session_manager.destroy_session(token)
        if success:
            logger.info(f"会话已销毁: {token[:8]}...")
        else:
            logger.error(f"会话销毁失败: {token[:8]}...")

        return success

    @staticmethod
    def get_current_user() -> Optional[dict]:
        """获取当前登录用户（直接从Redis获取）"""
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
        except Exception as e:
            logger.error(f"获取当前用户信息失败: {e}")
            return None

    @staticmethod
    def update_user_session(token: str, user_data: dict, roles_data: list[dict]) -> bool:
        """更新用户会话中的用户数据"""
        try:
            # 获取当前会话信息
            current_session = session_manager.get_session(token)
            if not current_session:
                logger.warning(f"尝试更新不存在的会话: {token[:8]}...")
                return False

            # 更新用户数据
            updated_session = {
                'user_id': current_session.get('user_id'),
                'token': token,
                'user': user_data,
                'roles': roles_data,
                'login_ip': current_session.get('login_ip', '')
            }

            success = session_manager.update_session(token, updated_session)
            if success:
                logger.info(f"用户会话数据已更新: {token[:8]}...")
            else:
                logger.warning(f"用户会话数据更新失败: {token[:8]}...")

            return success
        except Exception as e:
            logger.error(f"更新用户会话失败: {e}")
            return False

    @staticmethod
    def get_session_stats() -> dict:
        """获取会话统计信息"""
        try:
            total_sessions = session_manager.get_session_count()
            return {
                'total_sessions': total_sessions,
                'redis_available': session_manager.redis_client.is_available()
            }
        except Exception as e:
            logger.error(f"获取会话统计失败: {e}")
            return {
                'total_sessions': 0,
                'redis_available': False
            }


# 便捷的装饰器别名
login_required = AuthManager.login_required
permission_required = AuthManager.permission_required
role_required = AuthManager.role_required


# 权限常量
class Permissions:
    """权限常量类"""

    # 系统管理权限
    SYSTEM_VIEW = "system:view"
    SYSTEM_MANAGE = "system:manage"

    # 用户管理权限
    USER_VIEW = "system:user:view"
    USER_CREATE = "system:user:create"
    USER_UPDATE = "system:user:update"
    USER_DELETE = "system:user:delete"
    USER_ASSIGN_ROLE = "system:user:assign_role"

    # 角色管理权限
    ROLE_VIEW = "system:role:view"
    ROLE_CREATE = "system:role:create"
    ROLE_UPDATE = "system:role:update"
    ROLE_DELETE = "system:role:delete"
    ROLE_ASSIGN_MENU = "system:role:assign_menu"

    # 菜单管理权限
    MENU_VIEW = "system:menu:view"
    MENU_CREATE = "system:menu:create"
    MENU_UPDATE = "system:menu:update"
    MENU_DELETE = "system:menu:delete"

    # 业务权限
    WORKSPACE_VIEW = "business:workspace:view"
    WORKSPACE_MANAGE = "business:workspace:manage"

    GROUP_VIEW = "business:group:view"
    GROUP_MANAGE = "business:group:manage"

    COUNSELOR_VIEW = "business:counselor:view"
    COUNSELOR_MANAGE = "business:counselor:manage"


# 角色常量
class Roles:
    """角色常量类"""

    ADMIN = "admin"  # 系统管理员
    MANAGER = "manager"  # 业务管理员
    COUNSELOR = "counselor"  # 咨询师
    USER = "user"  # 普通用户
