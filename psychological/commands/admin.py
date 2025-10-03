"""
管理员命令模块
提供系统初始化命令
"""
import click
import uuid
from typing import List, Tuple, Dict, Any

from pcf_flask_helper.model.base import db
from psychological.system.models import User, Role, UserRole
from psychological.utils.auth import hash_password


def create_roles() -> None:
    """创建系统角色"""
    # 检查是否已有角色数据，如果有则跳过
    existing_count = db.session.query(Role).count()
    if existing_count > 0:
        click.echo(f'   警告: 系统中已存在 {existing_count} 个角色，跳过角色创建')
        return

    # 角色数据定义
    roles_data = [
        {
            'id': str(uuid.uuid4()),
            'name': '系统管理员',
            'code': 'admin',
            'description': '系统管理员，拥有所有权限',
            'sort_order': 1,
            'data_scope': 1,  # 全部数据权限
            'status': 1,
            'is_default': False,
            'remark': '系统管理员角色，拥有最高权限'
        },
        {
            'id': str(uuid.uuid4()),
            'name': '经理',
            'code': 'manager',
            'description': '经理角色，拥有部门管理权限',
            'sort_order': 2,
            'data_scope': 3,  # 本部门数据权限
            'status': 1,
            'is_default': False,
            'remark': '经理角色，可管理本部门数据'
        },
        {
            'id': str(uuid.uuid4()),
            'name': '普通用户',
            'code': 'user',
            'description': '普通用户，基础权限',
            'sort_order': 3,
            'data_scope': 5,  # 仅本人数据权限
            'status': 1,
            'is_default': True,
            'remark': '普通用户角色，默认角色'
        }
    ]

    # 创建角色实例
    created_roles = []
    for role_data in roles_data:
        role = Role(**role_data)
        db.session.add(role)
        created_roles.append(role)
        click.echo(f'   创建角色: {role_data["name"]} ({role_data["code"]})')

    db.session.flush()  # 刷新获取角色ID
    
    click.echo(f'\n角色创建完成！')
    click.echo(f'角色: {len(created_roles)} 个')


def create_users() -> None:
    """创建系统用户"""
    # 检查是否已有用户数据，如果有则跳过
    existing_count = db.session.query(User).count()
    if existing_count > 0:
        click.echo(f'   警告: 系统中已存在 {existing_count} 个用户，跳过用户创建')
        return

    # 获取角色引用
    roles = {role.code: role for role in db.session.query(Role).all()}
    
    if not roles.get('admin') or not roles.get('manager') or not roles.get('user'):
        click.echo('   错误: 未找到必要的角色，请先创建角色')
        return

    # 用户数据定义
    users_data = [
        {
            'id': str(uuid.uuid4()),
            'username': 'admin',
            'email': 'admin@example.com',
            'real_name': '系统管理员',
            'nick_name': '管理员',
            'password': 'admin123',
            'status': 1,
            'gender': 0,
            'role_code': 'admin'
        },
        {
            'id': str(uuid.uuid4()),
            'username': 'manager',
            'email': 'manager@example.com',
            'real_name': '部门经理',
            'nick_name': '经理',
            'password': 'manager123',
            'status': 1,
            'gender': 0,
            'role_code': 'manager'
        },
        {
            'id': str(uuid.uuid4()),
            'username': 'user',
            'email': 'user@example.com',
            'real_name': '普通用户',
            'nick_name': '用户',
            'password': 'user123',
            'status': 1,
            'gender': 0,
            'role_code': 'user'
        }
    ]

    # 创建用户实例
    created_users = []
    for user_data in users_data:
        # 创建用户
        user = User(
            id=user_data['id'],
            username=user_data['username'],
            email=user_data['email'],
            real_name=user_data['real_name'],
            nick_name=user_data['nick_name'],
            password_hash=hash_password(user_data['password']),
            status=user_data['status'],
            gender=user_data['gender']
        )
        
        # 创建用户角色关联
        user_role = UserRole(
            id=str(uuid.uuid4()),
            user_id=user_data['id'],
            role_id=roles[user_data['role_code']].id
        )
        
        db.session.add(user)
        db.session.add(user_role)
        created_users.append((user, user_data, roles[user_data['role_code']]))
        click.echo(f'   创建用户: {user_data["username"]} ({user_data["real_name"]})')

    click.echo(f'\n用户创建完成！')
    click.echo(f'用户: {len(created_users)} 个')
    
    # 显示用户信息
    if created_users:
        click.echo('\n默认账户信息:')
        for user, user_data, role in created_users:
            click.echo(f'   • {role.name}: {user_data["username"]} / {user_data["password"]}')
