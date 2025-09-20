"""
管理员命令模块
提供系统初始化命令
"""
import click
import uuid
from flask import current_app
from flask.cli import with_appcontext
from datetime import datetime

from ..models.base import db
from ..models.user import User
from ..models.user_password import UserPassword
from ..models.user_role import UserRole
from ..models.role import Role
from ..utils.auth import hash_password
from ..utils.logger_client import get_logger

logger = get_logger(__name__)


@click.group()
def admin():
    """管理员命令组"""
    pass


def create_role(role_data):
    """创建角色的辅助函数"""
    role = Role(
        id=str(uuid.uuid4()),
        name=role_data['name'],
        code=role_data['code'],
        description=role_data['description'],
        sort_order=role_data['sort_order'],
        data_scope=role_data['data_scope'],
        status=1,
        is_default=role_data.get('is_default', False),
        remark=role_data.get('remark', '系统初始化创建')
    )
    db.session.add(role)
    return role


def create_user_with_role(user_data, role):
    """创建用户并分配角色的辅助函数"""
    user_id = str(uuid.uuid4())
    
    # 创建用户
    user = User(
        id=user_id,
        username=user_data['username'],
        email=user_data['email'],
        real_name=user_data['real_name'],
        nick_name=user_data['nick_name'],
        status=1,
        gender=0
    )
    
    # 创建密码记录
    password_hash = hash_password(user_data['password'])
    user_password = UserPassword(
        id=str(uuid.uuid4()),
        user_id=user_id,
        password_hash=password_hash
    )
    
    # 创建用户角色关联
    user_role = UserRole(
        id=str(uuid.uuid4()),
        user_id=user_id,
        role_id=role.id
    )
    
    db.session.add(user)
    db.session.add(user_password)
    db.session.add(user_role)
    
    return user


def create_roles_and_users():
    """创建角色和用户的统一函数"""
    # 检查是否已有角色和用户数据，如果有则跳过
    existing_roles = db.session.query(Role).count()
    existing_users = db.session.query(User).count()
    
    if existing_roles > 0:
        click.echo(f'   ⚠️  系统中已存在 {existing_roles} 个角色，跳过角色创建')
        roles = db.session.query(Role).all()
        roles_dict = {role.code: role for role in roles}
    else:
        # 定义角色数据
        roles_data = [
            {
                'name': '系统管理员',
                'code': 'admin',
                'description': '系统管理员，拥有所有权限',
                'sort_order': 1,
                'data_scope': 1,  # 全部数据权限
                'is_default': False,
                'remark': '系统管理员角色，拥有最高权限'
            },
            {
                'name': '经理',
                'code': 'manager',
                'description': '经理角色，拥有部门管理权限',
                'sort_order': 2,
                'data_scope': 3,  # 本部门数据权限
                'is_default': False,
                'remark': '经理角色，可管理本部门数据'
            },
            {
                'name': '普通用户',
                'code': 'user',
                'description': '普通用户，基础权限',
                'sort_order': 3,
                'data_scope': 5,  # 仅本人数据权限
                'is_default': True,
                'remark': '普通用户角色，默认角色'
            }
        ]
        
        # 创建角色
        roles_dict = {}
        for role_data in roles_data:
            role = create_role(role_data)
            roles_dict[role_data['code']] = role
            click.echo(f'   ✅ 创建角色: {role_data["name"]} ({role_data["code"]})')
        
        db.session.flush()  # 刷新获取角色ID
    
    if existing_users > 0:
        click.echo(f'   ⚠️  系统中已存在 {existing_users} 个用户，跳过用户创建')
        users = db.session.query(User).all()
        # 构建返回格式以保持一致性
        created_users = []
        for user in users:
            user_roles = db.session.query(UserRole).filter_by(user_id=user.id).all()
            if user_roles:
                role = db.session.query(Role).filter_by(id=user_roles[0].role_id).first()
                if role:
                    user_data = {
                        'username': user.username,
                        'password': '***',  # 不显示真实密码
                        'email': user.email,
                        'real_name': user.real_name,
                        'nick_name': user.nick_name,
                        'role_code': role.code
                    }
                    created_users.append((user, user_data, role))
    else:
        # 定义默认账户数据
        users_data = [
            {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@example.com',
                'real_name': '系统管理员',
                'nick_name': '管理员',
                'role_code': 'admin'
            },
            {
                'username': 'manager',
                'password': 'manager123',
                'email': 'manager@example.com',
                'real_name': '部门经理',
                'nick_name': '经理',
                'role_code': 'manager'
            },
            {
                'username': 'user',
                'password': 'user123',
                'email': 'user@example.com',
                'real_name': '普通用户',
                'nick_name': '用户',
                'role_code': 'user'
            }
        ]
        
        # 创建用户
        created_users = []
        for user_data in users_data:
            role = roles_dict[user_data['role_code']]
            user = create_user_with_role(user_data, role)
            created_users.append((user, user_data, role))
            click.echo(f'   ✅ 创建用户: {user_data["username"]} ({role.name})')
    
    return list(roles_dict.values()) if existing_roles == 0 else roles, created_users


