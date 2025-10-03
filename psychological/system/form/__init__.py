from .auth import (
    LoginForm, PhoneLoginForm, UserLoginForm, RegisterForm, UpdateProfileForm,
    ChangePasswordForm, UserQueryForm, RoleCreateForm, RoleUpdateForm, 
    RoleQueryForm, MenuCreateForm, MenuUpdateForm, MenuQueryForm
)
from .banner import BannerQueryForm, BannerCreateForm, BannerUpdateForm
from .category import CategoryCreateForm, CategoryUpdateForm, CategoryQueryForm, CategoryStatusUpdateForm
from .group import GroupQueryForm, GroupCreateForm, GroupUpdateForm
from .menu import MenuQueryForm as SystemMenuQueryForm, MenuCreateForm as SystemMenuCreateForm, MenuUpdateForm as SystemMenuUpdateForm
from .role import RoleQueryForm as SystemRoleQueryForm, RoleCreateForm as SystemRoleCreateForm, RoleUpdateForm as SystemRoleUpdateForm
from .user import UserCreateForm, UserUpdateForm, UserQueryForm as SystemUserQueryForm
from .workspace import WorkspaceQueryForm, WorkspaceCreateForm, WorkspaceUpdateForm

__all__ = [
    # Auth forms
    'LoginForm',
    'PhoneLoginForm',
    'UserLoginForm',
    'RegisterForm',
    'UpdateProfileForm',
    'ChangePasswordForm',
    'UserQueryForm',
    'RoleCreateForm',
    'RoleUpdateForm',
    'RoleQueryForm',
    'MenuCreateForm',
    'MenuUpdateForm',
    'MenuQueryForm',
    
    # Banner forms
    'BannerQueryForm',
    'BannerCreateForm',
    'BannerUpdateForm',
    
    # Category forms
    'CategoryCreateForm',
    'CategoryUpdateForm',
    'CategoryQueryForm',
    'CategoryStatusUpdateForm',
    
    # Group forms
    'GroupQueryForm',
    'GroupCreateForm',
    'GroupUpdateForm',
    
    # Menu forms (system specific)
    'SystemMenuQueryForm',
    'SystemMenuCreateForm',
    'SystemMenuUpdateForm',
    
    # Role forms (system specific)
    'SystemRoleQueryForm',
    'SystemRoleCreateForm',
    'SystemRoleUpdateForm',
    
    # User forms
    'UserCreateForm',
    'UserUpdateForm',
    'SystemUserQueryForm',
    
    # Workspace forms
    'WorkspaceQueryForm',
    'WorkspaceCreateForm',
    'WorkspaceUpdateForm'
]
