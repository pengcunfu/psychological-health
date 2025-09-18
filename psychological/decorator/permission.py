"""
权限装饰器模块
提供基于角色和权限的访问控制装饰器

使用示例:
    @role_required('admin')                    # 校验用户角色
    @permission_required('user:read')          # 校验用户权限
"""

from functools import wraps
from typing import List, Union, Callable
from psychological.utils.auth_helper import get_roles, assert_current_user_id, get_role_objects
from psychological.utils.exceptions import UnauthorizedError, PermissionDeniedError
from psychological.utils.json_result import JsonResult


def role_required(required_roles: Union[str, List[str]]) -> Callable:
    """
    角色装饰器 - 专门校验用户角色
    
    Args:
        required_roles: 所需角色，可以是单个角色字符串或角色列表
                       如果是列表，用户只需具有其中任意一个角色即可
    
    Returns:
        装饰器函数
    
    Examples:
        @role_required('admin')
        def admin_only_function():
            pass
        
        @role_required(['admin', 'manager'])
        def admin_or_manager_function():
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # 检查用户是否登录
                user_id = assert_current_user_id()
                if not user_id:
                    return JsonResult.error('用户未登录', 401)
                
                # 获取用户角色
                user_roles = get_roles()
                if not user_roles:
                    return JsonResult.error('用户未分配角色，权限不足', 403)
                
                # 标准化required_roles为列表
                if isinstance(required_roles, str):
                    roles_to_check = [required_roles]
                else:
                    roles_to_check = required_roles
                
                # 将角色转换为小写进行比较
                user_roles_lower = [role.lower() for role in user_roles]
                required_roles_lower = [role.lower() for role in roles_to_check]
                
                # 检查用户是否具有任意一个所需角色
                has_required_role = any(role in user_roles_lower for role in required_roles_lower)
                
                if not has_required_role:
                    roles_str = ', '.join(roles_to_check)
                    return JsonResult.error(f'权限不足，需要以下角色之一: {roles_str}', 403)
                
                # 角色检查通过，执行原函数
                return func(*args, **kwargs)
                
            except UnauthorizedError as e:
                return JsonResult.error(str(e), 401)
            except PermissionDeniedError as e:
                return JsonResult.error(str(e), 403)
            except Exception as e:
                return JsonResult.error(f'角色验证失败: {str(e)}', 500)
        
        return wrapper
    return decorator


def permission_required(required_permissions: Union[str, List[str]]) -> Callable:
    """
    权限装饰器 - 校验用户是否有调用该方法的能力
    不校验角色，只校验用户是否有执行该操作的权限
    
    Args:
        required_permissions: 所需权限，可以是单个权限字符串或权限列表
                             如果是列表，用户只需具有其中任意一个权限即可
                             权限格式: 'module:action' 或 'menu_id'
    
    Returns:
        装饰器函数
    
    Examples:
        @permission_required('user:read')
        def get_users():
            pass
        
        @permission_required(['user:read', 'user:write'])
        def manage_users():
            pass
        
        @permission_required('system:admin')
        def admin_function():
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # 检查用户是否登录
                user_id = assert_current_user_id()
                if not user_id:
                    return JsonResult.error('用户未登录', 401)
                
                # 获取用户角色
                user_roles = get_roles()
                if not user_roles:
                    return JsonResult.error('用户未分配角色，无法获取权限', 403)
                
                # 检查是否为admin角色，如果是则跳过权限检查
                user_roles_lower = [role.lower() for role in user_roles]
                if 'admin' in user_roles_lower:
                    # admin角色拥有所有权限，直接通过
                    return func(*args, **kwargs)
                
                # 获取用户角色对象（包含权限信息）
                role_objects = get_role_objects()
                if not role_objects:
                    return JsonResult.error('用户未分配角色，无法获取权限', 403)
                
                # 标准化required_permissions为列表
                if isinstance(required_permissions, str):
                    permissions_to_check = [required_permissions]
                else:
                    permissions_to_check = required_permissions
                
                # 收集用户所有的权限（从角色的菜单权限中获取）
                user_permissions = set()
                for role in role_objects:
                    if role.get('status') == 1:  # 只考虑启用的角色
                        menu_ids = role.get('menu_ids', [])
                        if isinstance(menu_ids, list):
                            user_permissions.update(menu_ids)
                
                # 检查用户是否具有任意一个所需权限
                has_required_permission = any(
                    permission in user_permissions 
                    for permission in permissions_to_check
                )
                
                if not has_required_permission:
                    permissions_str = ', '.join(permissions_to_check)
                    return JsonResult.error(f'权限不足，需要以下权限之一: {permissions_str}', 403)
                
                # 权限检查通过，执行原函数
                return func(*args, **kwargs)
                
            except UnauthorizedError as e:
                return JsonResult.error(str(e), 401)
            except PermissionDeniedError as e:
                return JsonResult.error(str(e), 403)
            except Exception as e:
                return JsonResult.error(f'权限验证失败: {str(e)}', 500)
        
        return wrapper
    return decorator
