from functools import wraps
from flask import request, g
from typing import List, Optional
from utils.json_result import JsonResult
from utils.redis_client import session_manager
from utils.logger_client import get_logger

logger = get_logger(__name__)


# 移除内存会话存储，改用Redis
# user_sessions = {}


class AuthMiddleware:
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

            # 将用户信息存储到g对象中
            g.current_user = user_info
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

                # 检查权限
                if not AuthMiddleware._check_user_permission(user_info['user_id'], permission):
                    return JsonResult.error("权限不足", code=403)

                # 延长会话有效期
                session_manager.extend_session(token)

                g.current_user = user_info
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

                # 检查角色
                if not AuthMiddleware._check_user_roles(user_info['user_id'], roles):
                    return JsonResult.error("角色权限不足", code=403)

                # 延长会话有效期
                session_manager.extend_session(token)

                g.current_user = user_info
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
        """检查用户是否有指定角色"""
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
    def create_session(user_id: str, token: str, user_data: dict):
        """创建用户会话"""
        session_data = {
            'user_id': user_id,
            'token': token,
            'user_data': user_data,
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
        """获取当前登录用户"""
        return getattr(g, 'current_user', None)

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
login_required = AuthMiddleware.login_required
permission_required = AuthMiddleware.permission_required
role_required = AuthMiddleware.role_required


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
