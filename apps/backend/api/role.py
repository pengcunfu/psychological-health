"""
角色管理API
提供系统角色的增删改查功能

接口列表：
- GET /role - 获取角色列表
- POST /role - 创建角色
- PUT /role/<role_id> - 更新角色信息
- DELETE /role/<role_id> - 删除角色
"""
from flask import Blueprint, request
import uuid

from models.role import Role
from models.user_role import UserRole
from models.base import db
from form.role import RoleQueryForm, RoleCreateForm, RoleUpdateForm
from utils.json_result import JsonResult
from utils.validate import validate_data, validate_args
from utils.model_helper import update_model_from_form

role_bp = Blueprint("role", __name__, url_prefix="/role")


@role_bp.route('', methods=['GET'])
def get_roles():
    """获取角色列表"""
    form = validate_args(RoleQueryForm)

    page = form.page.data
    per_page = form.per_page.data
    keyword = form.keyword.data

    # 构建查询
    query = Role.query

    # 关键词搜索
    if keyword:
        query = query.filter(
            (Role.name.like(f'%{keyword}%')) |
            (Role.code.like(f'%{keyword}%'))
        )

    # 分页查询
    pagination = query.order_by(Role.sort_order.asc(), Role.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    result = []
    for role in pagination.items:
        role_dict = role.to_dict()
        if hasattr(role, 'get_data_scope_name'):
            role_dict['data_scope_name'] = role.get_data_scope_name()
        result.append(role_dict)

    return JsonResult.success({
        'roles': result,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@role_bp.route('', methods=['POST'])
def create_role():
    """创建角色"""
    form = validate_data(RoleCreateForm)

    role = Role(
        id=str(uuid.uuid4()),
        name=form.name.data,
        code=form.code.data,
        description=form.description.data or '',
        sort_order=form.sort_order.data or 0,
        data_scope=form.data_scope.data or 1,
        status=form.status.data or 1,
        is_default=form.is_default.data or False,
        remark=form.remark.data or ''
    )
    
    # 处理菜单权限
    if form.menu_ids.data:
        if isinstance(form.menu_ids.data, str):
            # 如果是字符串，分割为列表
            menu_id_list = [mid.strip() for mid in form.menu_ids.data.split(',') if mid.strip()]
        else:
            # 如果已经是列表，直接使用
            menu_id_list = form.menu_ids.data
        role.menu_ids = menu_id_list

    db.session.add(role)
    db.session.commit()

    return JsonResult.success(role.to_dict(), '角色创建成功')


@role_bp.route('/<role_id>', methods=['PUT'])
def update_role(role_id):
    """更新角色"""
    if not role_id or not role_id.strip():
        return JsonResult.error('角色ID不能为空', 400)

    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return JsonResult.error('角色不存在', 404)

    # 使用统一的验证和更新函数
    form = validate_data(RoleUpdateForm)
    update_model_from_form(role, form, exclude_fields=['menu_ids'])

    # 特殊处理菜单权限
    if form.menu_ids.data is not None:
        if isinstance(form.menu_ids.data, str):
            # 如果是字符串，分割为列表
            menu_id_list = [mid.strip() for mid in form.menu_ids.data.split(',') if mid.strip()]
        else:
            # 如果已经是列表，直接使用
            menu_id_list = form.menu_ids.data
        role.menu_ids = menu_id_list

    db.session.commit()
    return JsonResult.success(role.to_dict(), '角色更新成功')


@role_bp.route('/<role_id>', methods=['DELETE'])
def delete_role(role_id):
    """删除角色"""
    if not role_id or not role_id.strip():
        return JsonResult.error('角色ID不能为空', 400)

    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return JsonResult.error('角色不存在', 404)

    # 检查是否有用户使用该角色
    user_role_count = UserRole.query.filter_by(role_id=role_id).count()
    if user_role_count > 0:
        return JsonResult.error('该角色正在被使用，无法删除', 400)

    db.session.delete(role)
    db.session.commit()
    return JsonResult.success(None, '角色删除成功')
