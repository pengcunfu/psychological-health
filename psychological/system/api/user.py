"""
用户管理API
提供用户的增删改查功能
"""
from flask import Blueprint, request
import uuid

from pcf_flask_helper.model.base import db
from ..models import User, Role, UserRole
from ..form import UserCreateForm, UserUpdateForm, SystemUserQueryForm as UserQueryForm
from pcf_flask_helper.common import json_success, json_error
from psychological.utils.auth_helper import assert_current_user_id, is_manager_user
from psychological.utils.model_helper import update_model_fields
from psychological.utils.auth import hash_password
from pcf_flask_helper.model.query import create_query_builder, assert_exists, assert_not_exists
from psychological.utils.decorator import validate_form
from psychological.utils.decorator.permission import role_required, permission_required
from pcf_flask_helper.form.validate import assert_id_exists

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('', methods=['GET'])
@validate_form(UserQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("user:get_users")
def get_users(form: UserQueryForm):
    """获取用户列表（支持动态角色权限）"""
    # 获取当前用户信息
    current_user_id = assert_current_user_id()
    is_manager = is_manager_user()

    # 构建查询
    builder = create_query_builder(User) \
        .unless(is_manager, User.id == current_user_id)

    # 管理员可以使用搜索条件
    if is_manager:
        builder.when(form.username.data, User.username.like(f'%{form.username.data}%')) \
            .when(form.phone.data, User.phone.like(f'%{form.phone.data}%')) \
            .when(form.email.data, User.email.like(f'%{form.email.data}%')) \
            .when(form.real_name.data, User.real_name.like(f'%{form.real_name.data}%')) \
            .when(form.nick_name.data, User.nick_name.like(f'%{form.nick_name.data}%')) \
            .when(form.gender.data is not None, User.gender == form.gender.data) \
            .when(form.status.data is not None, User.status == form.status.data)

    # 分页查询
    result = builder.order_by(User.create_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    # 添加角色信息
    users_data = []
    for user in result['items']:
        user_roles = create_query_builder(Role) \
            .join(UserRole) \
            .filter(UserRole.user_id == user.id) \
            .all()

        user_dict = user.to_dict()
        # 根据权限决定是否显示敏感信息
        if is_manager or user.id == current_user_id:
            user_dict['roles'] = [role.to_dict() for role in user_roles]
        else:
            # 不显示其他用户的角色信息
            user_dict['roles'] = []
        users_data.append(user_dict)

    return json_success({
        'list': users_data,
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'has_manage_permission': is_manager
    })


@user_bp.route('/<user_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("user:get_user")
def get_user(user_id):
    """获取用户详情（支持动态角色权限）"""
    if not user_id or not user_id.strip():
        return json_error('用户ID不能为空', 400)

    # 获取当前用户信息
    current_user_id = assert_current_user_id()
    has_manage_permission = is_manager_user()

    user = assert_exists(User, User.id == user_id, "用户不存在")

    # 权限检查：管理员和管理者可以查看所有用户，普通用户只能查看自己
    if not has_manage_permission and user_id != current_user_id:
        return json_error('无权限查看该用户信息', 403)

    # 获取用户角色
    user_roles = create_query_builder(Role) \
        .join(UserRole) \
        .filter(UserRole.user_id == user_id) \
        .all()

    result = user.to_dict()
    result['roles'] = [role.to_dict() for role in user_roles]

    return json_success(result)


@user_bp.route('', methods=['POST'])
def create_user():
    """创建用户（支持动态角色权限）"""
    # 权限检查：只有管理员和管理者可以创建用户
    has_manage_permission = is_manager_user()
    if not has_manage_permission:
        raise ValueError('无权限创建用户')

    form = validate_form(UserCreateForm)

    # 检查用户名是否已存在
    assert_not_exists(User, User.username == form.username.data, "用户名已存在")

    # 检查手机号是否已存在（如果提供了手机号）
    if form.phone.data:
        assert_not_exists(User, User.phone == form.phone.data, "手机号已存在")

    # 检查邮箱是否已存在（如果提供了邮箱）
    if form.email.data:
        assert_not_exists(User, User.email == form.email.data, "邮箱已存在")

    # 创建用户
    user = User(
        id=str(uuid.uuid4()),
        username=form.username.data,
        avatar=form.avatar.data or '',
        phone=form.phone.data or '',
        email=form.email.data or '',
        real_name=form.real_name.data or '',
        nick_name=form.nick_name.data or '',
        password_hash=hash_password(form.password.data),
        gender=form.gender.data if form.gender.data is not None else 0,
        birth_date=form.birth_date.data,
        brief_introduction=form.brief_introduction.data or '',
        status=form.status.data if form.status.data is not None else 1
    )
    db.session.add(user)
    db.session.commit()
    return json_success(user.to_dict(), '用户创建成功', 201)


@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户（支持动态角色权限）"""
    if not user_id or not user_id.strip():
        return json_error('用户ID不能为空', 400)

    # 获取当前用户信息
    current_user_id = assert_current_user_id()
    has_manage_permission = is_manager_user()

    user = assert_exists(User, User.id == user_id, "用户不存在")

    # 权限检查：管理员和管理者可以修改所有用户，普通用户只能修改自己
    if not has_manage_permission and user_id != current_user_id:
        raise ValueError("无权限修改该用户信息")

    form = validate_form(UserUpdateForm)

    # 检查用户名是否已存在（排除当前用户）
    if form.username.data and form.username.data != user.username:
        assert_not_exists(User, [User.username == form.username.data, User.id != user_id], "用户名已存在")

    # 检查手机号是否已存在（排除当前用户）
    if form.phone.data and form.phone.data != user.phone:
        assert_not_exists(User, [User.phone == form.phone.data, User.id != user_id], "手机号已存在")

    # 检查邮箱是否已存在（排除当前用户）
    if form.email.data and form.email.data != user.email:
        assert_not_exists(User, [User.email == form.email.data, User.id != user_id], "邮箱已存在")

    # 处理密码特殊情况
    if form.password.data:
        user.password_hash = hash_password(form.password.data)

    # 更新用户信息
    update_model_fields(user, form, exclude_fields=['password'])

    db.session.commit()
    return json_success(user.to_dict(), '用户更新成功')


@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户（支持动态角色权限）"""
    assert_id_exists(user_id, "用户ID不能为空")

    # 获取当前用户信息
    current_user_id = assert_current_user_id()
    has_manage_permission = is_manager_user()

    # 权限检查：只有管理员和管理者可以删除用户，且不能删除自己
    if not has_manage_permission:
        raise ValueError('无权限删除用户')

    if user_id == current_user_id:
        raise ValueError('不能删除自己的账户')

    user = assert_exists(User, User.id == user_id, "用户不存在")

    db.session.delete(user)
    db.session.commit()
    return json_success(None, '用户删除成功')


@user_bp.route('/<user_id>/roles', methods=['PUT'])
def assign_user_roles(user_id):
    """分配用户角色（支持动态角色权限）"""
    assert_id_exists(user_id, "用户ID不能为空")

    # 权限检查：只有管理员和管理者可以分配角色
    has_manage_permission = is_manager_user()
    if not has_manage_permission:
        raise ValueError('无权限分配用户角色')

    user = assert_exists(User, User.id == user_id, "用户不存在")

    data = request.get_json()
    if not data:
        raise ValueError('请求数据不能为空')

    role_ids = data.get('role_ids', [])
    if not isinstance(role_ids, list):
        raise ValueError('角色ID列表格式错误')

    # 验证角色是否存在
    for role_id in role_ids:
        assert_exists(Role, Role.id == role_id, f"角色 {role_id} 不存在")

    # 删除用户现有角色
    UserRole.query.filter_by(user_id=user_id).delete()

    # 添加新角色
    for role_id in role_ids:
        user_role = UserRole(
            id=str(uuid.uuid4()),
            user_id=user_id,
            role_id=role_id
        )
        db.session.add(user_role)

    db.session.commit()
    return json_success(None, '角色分配成功')
