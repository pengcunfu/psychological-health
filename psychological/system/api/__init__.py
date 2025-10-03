from .auth import login_bp
from .banner import banner_bp
from .category import category_bp
from .group import group_bp
from .menu import menu_bp
from .role import role_bp
from .upload import file_upload_bp
from .user import user_bp
from .workspace import workspace_bp
from flask import current_app


def register_system_blueprints():
    """注册所有系统相关的API蓝图"""
    current_app.register_blueprint(login_bp)
    current_app.register_blueprint(banner_bp)
    current_app.register_blueprint(category_bp)
    current_app.register_blueprint(group_bp)
    current_app.register_blueprint(menu_bp)
    current_app.register_blueprint(role_bp)
    current_app.register_blueprint(file_upload_bp)
    current_app.register_blueprint(user_bp)
    current_app.register_blueprint(workspace_bp)


__all__ = [
    # Blueprints
    'login_bp',
    'banner_bp',
    'category_bp',
    'group_bp',
    'menu_bp',
    'role_bp',
    'file_upload_bp',
    'user_bp',
    'workspace_bp',

    # Registration function
    'register_system_blueprints'
]
