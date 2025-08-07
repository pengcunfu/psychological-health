"""
用户管理API
提供用户的增删改查功能

接口列表：
- GET /user - 获取用户列表
- GET /user/<user_id> - 获取单个用户详情
- POST /user - 创建用户
- PUT /user/<user_id> - 更新用户信息
- DELETE /user/<user_id> - 删除用户
- PUT /user/<user_id>/roles - 分配用户角色
"""
from flask import Blueprint, request
from sqlalchemy import or_
import uuid

from models import db
from models.user import User
from models.role import Role
from models.user_role import UserRole
from form.user import UserCreateForm, UserUpdateForm, UserQueryForm
from utils.json_result import JsonResult
from utils.auth_helper import get_user_id, is_manager_user
from utils.validate import validate_form, check_id
from utils.model_helper import update_model_from_form
from utils.auth import hash_password

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('', methods=['GET'])
def get_users():
    """获取用户列表（支持动态角色权限）"""
    # 获取当前用户信息
    current_user_id = get_user_id()
    has_manage_permission = is_manager_user()
    
    form = validate_form(UserQueryForm)

    # 权限控制：普通用户只能查看自己的信息
    if has_manage_permission:
        # 管理员和管理者可以查看所有用户
        query = User.query
        
        # 构建搜索条件
        search_conditions = []
        if form.username.data:
            search_conditions.append(User.username.like(f'%{form.username.data}%'))
        if form.phone.data:
            search_conditions.append(User.phone.like(f'%{form.phone.data}%'))
        if form.email.data:
            search_conditions.append(User.email.like(f'%{form.email.data}%'))
        if form.real_name.data:
            search_conditions.append(User.real_name.like(f'%{form.real_name.data}%'))
        if form.nick_name.data:
            search_conditions.append(User.nick_name.like(f'%{form.nick_name.data}%'))
        if form.gender.data is not None:
            search_conditions.append(User.gender == form.gender.data)
        if form.status.data is not None:
            search_conditions.append(User.status == form.status.data)
            
        if search_conditions:
            query = query.filter(or_(*search_conditions))
    else:
        # 普通用户只能查看自己的信息
        query = User.query.filter_by(id=current_user_id)

    paginate = query.order_by(User.create_time.desc()).paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )

    # 添加角色信息
    result = []
    for user in paginate.items:
        user_roles = db.session.query(Role).join(UserRole).filter(
            UserRole.user_id == user.id
        ).all()

        user_dict = user.to_dict()
        # 根据权限决定是否显示敏感信息
        if has_manage_permission or user.id == current_user_id:
            user_dict['roles'] = [role.to_dict() for role in user_roles]
        else:
            # 不显示其他用户的角色信息
            user_dict['roles'] = []
        result.append(user_dict)

    return JsonResult.success({
        'list': result,
        'total': paginate.total,
        'page': form.page.data,
        'per_page': form.per_page.data,
        'has_manage_permission': has_manage_permission
    })


@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户详情（支持动态角色权限）"""
    if not user_id or not user_id.strip():
        return JsonResult.error('用户ID不能为空', 400)

    # 获取当前用户信息
    current_user_id = get_user_id()
    has_manage_permission = is_manager_user()

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return JsonResult.error('用户不存在', 404)

    # 权限检查：管理员和管理者可以查看所有用户，普通用户只能查看自己
    if not has_manage_permission and user_id != current_user_id:
        return JsonResult.error('无权限查看该用户信息', 403)

    # 获取用户角色
    user_roles = db.session.query(Role).join(UserRole).filter(
        UserRole.user_id == user_id
    ).all()

    result = user.to_dict()
    result['roles'] = [role.to_dict() for role in user_roles]

    return JsonResult.success(result)


@user_bp.route('', methods=['POST'])
def create_user():
    """创建用户（支持动态角色权限）"""
    # 权限检查：只有管理员和管理者可以创建用户
    has_manage_permission = is_manager_user()
    if not has_manage_permission:
        return JsonResult.error('无权限创建用户', 403)
    
    form = validate_form(UserCreateForm)
    
    # 检查用户名是否已存在
    existing_user = User.query.filter_by(username=form.username.data).first()
    if existing_user:
        return JsonResult.error('用户名已存在', 409)
    
    # 检查手机号是否已存在（如果提供了手机号）
    if form.phone.data:
        existing_phone = User.query.filter_by(phone=form.phone.data).first()
        if existing_phone:
            return JsonResult.error('手机号已存在', 409)
    
    # 检查邮箱是否已存在（如果提供了邮箱）
    if form.email.data:
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            return JsonResult.error('邮箱已存在', 409)
    
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
    return JsonResult.success(user.to_dict(), '用户创建成功', 201)


@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户（支持动态角色权限）"""
    if not user_id or not user_id.strip():
        return JsonResult.error('用户ID不能为空', 400)

    # 获取当前用户信息
    current_user_id = get_user_id()
    has_manage_permission = is_manager_user()

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return JsonResult.error('用户不存在', 404)

    # 权限检查：管理员和管理者可以修改所有用户，普通用户只能修改自己
    if not has_manage_permission and user_id != current_user_id:
        return JsonResult.error('无权限修改该用户信息', 403)

    form = validate_form(UserUpdateForm)
    
    # 检查用户名是否已存在（排除当前用户）
    if form.username.data and form.username.data != user.username:
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            return JsonResult.error('用户名已存在', 409)
    
    # 检查手机号是否已存在（排除当前用户）
    if form.phone.data and form.phone.data != user.phone:
        existing_phone = User.query.filter_by(phone=form.phone.data).first()
        if existing_phone:
            return JsonResult.error('手机号已存在', 409)
    
    # 检查邮箱是否已存在（排除当前用户）
    if form.email.data and form.email.data != user.email:
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            return JsonResult.error('邮箱已存在', 409)
    
    # 更新用户信息
    if form.username.data:
        user.username = form.username.data
    if form.avatar.data is not None:
        user.avatar = form.avatar.data
    if form.phone.data is not None:
        user.phone = form.phone.data
    if form.email.data is not None:
        user.email = form.email.data
    if form.real_name.data is not None:
        user.real_name = form.real_name.data
    if form.nick_name.data is not None:
        user.nick_name = form.nick_name.data
    if form.password.data:
        user.password_hash = hash_password(form.password.data)
    if form.gender.data is not None:
        user.gender = form.gender.data
    if form.birth_date.data is not None:
        user.birth_date = form.birth_date.data
    if form.brief_introduction.data is not None:
        user.brief_introduction = form.brief_introduction.data
    if form.status.data is not None:
        user.status = form.status.data
    
    db.session.commit()
    return JsonResult.success(user.to_dict(), '用户更新成功')


@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户（支持动态角色权限）"""
    if not user_id or not user_id.strip():
        return JsonResult.error('用户ID不能为空', 400)

    # 获取当前用户信息
    current_user_id = get_user_id()
    has_manage_permission = is_manager_user()

    # 权限检查：只有管理员和管理者可以删除用户，且不能删除自己
    if not has_manage_permission:
        return JsonResult.error('无权限删除用户', 403)
    
    if user_id == current_user_id:
        return JsonResult.error('不能删除自己的账户', 400)

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return JsonResult.error('用户不存在', 404)

    db.session.delete(user)
    db.session.commit()
    return JsonResult.success(None, '用户删除成功')


@user_bp.route('/<user_id>/roles', methods=['PUT'])
def assign_user_roles(user_id):
    """分配用户角色（支持动态角色权限）"""
    check_id(user_id, "用户ID不能为空")

    # 权限检查：只有管理员和管理者可以分配角色
    has_manage_permission = is_manager_user()
    if not has_manage_permission:
        return JsonResult.error('无权限分配用户角色', 403)

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return JsonResult.error('用户不存在', 404)

    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    role_ids = data.get('role_ids', [])
    if not isinstance(role_ids, list):
        return JsonResult.error('角色ID列表格式错误', 400)

    # 验证角色是否存在
    for role_id in role_ids:
        role = Role.query.filter_by(id=role_id).first()
        if not role:
            return JsonResult.error(f'角色 {role_id} 不存在', 400)

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
    return JsonResult.success(None, '角色分配成功')
