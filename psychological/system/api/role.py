"""
角色管理API
提供系统角色的增删改查功能
"""
from flask import Blueprint
import uuid

from ..models import Role, UserRole
from pcf_flask_helper.model.base import db
from ..form import SystemRoleQueryForm as RoleQueryForm, SystemRoleCreateForm as RoleCreateForm, SystemRoleUpdateForm as RoleUpdateForm
from pcf_flask_helper.common import json_success, json_error
from psychological.utils.model_helper import update_model_fields
from pcf_flask_helper.model.query import create_query_builder
from pcf_flask_helper.form.validate import assert_id_exists
from psychological.utils.decorator import validate_form
from psychological.utils.decorator.permission import role_required, permission_required

role_bp = Blueprint("role", __name__, url_prefix="/role")


@role_bp.route('', methods=['GET'])
@validate_form(RoleQueryForm)
@role_required(['admin'])
@permission_required("role:get_roles")
def get_roles(form):
    """获取角色列表（仅管理员）"""

    # 构建查询并分页
    result = create_query_builder(Role) \
        .when(form.keyword.data,
              (Role.name.like(f'%{form.keyword.data}%')) |
              (Role.code.like(f'%{form.keyword.data}%'))) \
        .order_by(Role.sort_order.asc(), Role.create_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return json_success({
        'roles': [role.to_dict() for role in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@role_bp.route('', methods=['POST'])
@validate_form(RoleCreateForm)
@role_required(['admin'])
@permission_required("role:create_role")
def create_role(form):
    """创建角色（仅管理员）"""

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

    return json_success(role.to_dict(), '角色创建成功')


@role_bp.route('/<role_id>', methods=['PUT'])
@validate_form(RoleUpdateForm)
@role_required(['admin'])
@permission_required("role:update_role")
def update_role(role_id, form):
    """更新角色（仅管理员）"""
    assert_id_exists(role_id, "角色ID不能为空")

    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return json_error('角色不存在', 404)

    # 使用统一的更新函数
    update_model_fields(role, form, exclude_fields=['menu_ids'])

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
    return json_success(role.to_dict(), '角色更新成功')


@role_bp.route('/<role_id>', methods=['DELETE'])
@role_required(['admin'])
@permission_required("role:delete_role")
def delete_role(role_id):
    """删除角色（仅管理员）"""
    assert_id_exists(role_id, "角色ID不能为空")

    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return json_error('角色不存在', 404)

    # 检查是否有用户使用该角色
    user_role_count = UserRole.query.filter_by(role_id=role_id).count()
    if user_role_count > 0:
        return json_error('该角色正在被使用，无法删除', 400)

    db.session.delete(role)
    db.session.commit()
    return json_success(None, '角色删除成功')
