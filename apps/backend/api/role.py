from flask import Blueprint, request
import uuid

from models.role import Role
from models.user_role import UserRole
from models.base import db
from form.role import RoleQueryForm, RoleCreateForm, RoleUpdateForm
from utils.json_result import JsonResult

role_bp = Blueprint("role", __name__, url_prefix="/role")


@role_bp.route('', methods=['GET'])
def get_roles():
    """获取角色列表"""
    form = RoleQueryForm(data=request.args)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    page = form.page
    per_page = form.per_page
    keyword = form.keyword

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
    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    form = RoleCreateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    role = Role(
        id=str(uuid.uuid4()),
        name=form.name.data,
        code=form.code.data,
        description=form.description.data or '',
        sort_order=form.sort_order.data or 0,
        data_scope=form.data_scope.data or 1,
        menu_ids=form.menu_ids.data or '',
        status=form.status.data or 1,
        is_default=form.is_default.data or False,
        remark=form.remark.data or ''
    )

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

    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    form = RoleUpdateForm(role_id=role_id, data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 更新角色信息
    if form.name.data is not None:
        role.name = form.name.data
    if form.code.data is not None:
        role.code = form.code.data
    if form.description.data is not None:
        role.description = form.description.data
    if form.sort_order.data is not None:
        role.sort_order = form.sort_order.data
    if form.data_scope.data is not None:
        role.data_scope = form.data_scope.data
    if form.menu_ids.data is not None:
        role.menu_ids = form.menu_ids.data
    if form.status.data is not None:
        role.status = form.status.data
    if form.is_default.data is not None:
        role.is_default = form.is_default.data
    if form.remark.data is not None:
        role.remark = form.remark.data

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
