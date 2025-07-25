from flask import Blueprint, request

from models import db
from models.user import User
from models.role import Role
from models.user_role import UserRole
from form.user import UserCreateForm, UserUpdateForm, UserQueryForm
from utils.json_result import JsonResult
import uuid
from utils.validate import validate_data, validate_args, check_id
from utils.model_helper import create_model_from_form

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('', methods=['GET'])
def get_users():
    """获取用户列表"""
    form = validate_args(UserQueryForm)

    query = User.query
    if form.username.data:
        query = query.filter(User.username.like(f'%{form.username.data}%'))

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
        user_dict['roles'] = [role.to_dict() for role in user_roles]
        result.append(user_dict)

    return JsonResult.success({
        'list': result,
        'total': paginate.total,
        'page': form.page.data,
        'per_page': form.per_page.data
    })


@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户详情"""
    if not user_id or not user_id.strip():
        return JsonResult.error('用户ID不能为空', 400)

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return JsonResult.error('用户不存在', 404)

    # 获取用户角色
    user_roles = db.session.query(Role).join(UserRole).filter(
        UserRole.user_id == user_id
    ).all()

    result = user.to_dict()
    result['roles'] = [role.to_dict() for role in user_roles]

    return JsonResult.success(result)


@user_bp.route('', methods=['POST'])
def create_user():
    """创建用户"""
    form = validate_data(UserCreateForm)
    existing_user = User.query.filter_by(username=form.username.data).first()
    if existing_user:
        return JsonResult.error('用户名已存在', 409)
    user = User(
        id=str(uuid.uuid4()),
        username=form.username.data,
        avatar=form.avatar.data or '',
        phone=form.phone.data or '',
        email=form.email.data or ''
    )
    db.session.add(user)
    db.session.commit()
    return JsonResult.success(user.to_dict(), '用户创建成功', 201)


@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户"""
    if not user_id or not user_id.strip():
        return JsonResult.error('用户ID不能为空', 400)

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return JsonResult.error('用户不存在', 404)

    form = validate_data(UserUpdateForm)
    create_model_from_form(user, form)
    db.session.commit()
    return JsonResult.success(user.to_dict(), '用户更新成功')


@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户"""
    if not user_id or not user_id.strip():
        return JsonResult.error('用户ID不能为空', 400)

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return JsonResult.error('用户不存在', 404)

    db.session.delete(user)
    db.session.commit()
    return JsonResult.success(None, '用户删除成功')


@user_bp.route('/<user_id>/roles', methods=['PUT'])
def assign_user_roles(user_id):
    """分配用户角色"""
    check_id(user_id, "用户ID不能为空")
    
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
