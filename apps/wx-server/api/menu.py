from flask import Blueprint, request
from models.base import db
from models.menu import Menu
from models.role import Role
from models.user import User
from models.user_role import UserRole
from sqlalchemy.exc import SQLAlchemyError
from utils.json_result import JsonResult
from form.menu import MenuQueryForm, MenuCreateForm, MenuUpdateForm
from datetime import datetime
import uuid

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")


@menu_bp.route('', methods=['GET'])
def get_menus():
    """获取菜单列表"""
    # 参数验证
    form = MenuQueryForm()
    if not form.validate_on_submit():
        return JsonResult.error("参数验证失败", form.errors)

    keyword = form.keyword.data
    page = form.page.data or 1
    size = form.size.data or 10

    # 构建查询
    query = Menu.query
    if keyword:
        query = query.filter(Menu.name.contains(keyword))

    # 添加排序
    query = query.order_by(Menu.sort_order.asc(), Menu.create_time.desc())

    # 分页查询
    pagination = query.paginate(
        page=page,
        per_page=size,
        error_out=False
    )

    return JsonResult.success({
        'items': [menu.to_dict() for menu in pagination.items],
        'total': pagination.total,
        'page': page,
        'size': size
    }, "获取菜单列表成功")


@menu_bp.route('', methods=['POST'])
def create_menu():
    """创建菜单"""
    # 检查请求数据
    if not request.get_json():
        return JsonResult.error("请求数据不能为空")

    # 参数验证
    form = MenuCreateForm()
    if not form.validate_on_submit():
        return JsonResult.error("参数验证失败", form.errors)

    # 检查菜单名称是否重复
    if Menu.query.filter_by(name=form.name.data).first():
        return JsonResult.error("菜单名称已存在")

    # 创建菜单
    menu = Menu(
        id=str(uuid.uuid4()),
        name=form.name.data,
        path=form.path.data,
        icon=form.icon.data,
        parent_id=form.parent_id.data,
        level=form.level.data or 1,
        sort_order=form.sort_order.data or 0,
        menu_type=form.menu_type.data or 0,
        permission=form.permission.data,
        component=form.component.data,
        is_external=form.is_external.data or 0,
        is_visible=form.is_visible.data or 1,
        is_cache=form.is_cache.data or 0,
        status=form.status.data or 1,
        remark=form.remark.data,
        create_time=datetime.now(),
        update_time=datetime.now()
    )

    db.session.add(menu)
    db.session.commit()
    return JsonResult.success(menu.to_dict(), "菜单创建成功")


@menu_bp.route('/<menu_id>', methods=['PUT'])
def update_menu(menu_id):
    """更新菜单"""
    # 检查请求数据
    if not request.get_json():
        return JsonResult.error("请求数据不能为空")

    # 查找菜单
    menu = Menu.query.filter_by(id=menu_id).first()
    if not menu:
        return JsonResult.error("菜单不存在")

    # 参数验证
    form = MenuUpdateForm()
    if not form.validate_on_submit():
        return JsonResult.error("参数验证失败", form.errors)

    # 检查菜单名称是否重复（排除自己）
    if form.name.data and form.name.data != menu.name:
        if Menu.query.filter_by(name=form.name.data).first():
            return JsonResult.error("菜单名称已存在")

    # 更新菜单信息
    update_fields = [
        'name', 'path', 'icon', 'parent_id', 'level', 'sort_order',
        'menu_type', 'permission', 'component', 'is_external',
        'is_visible', 'is_cache', 'status', 'remark'
    ]

    for field in update_fields:
        if hasattr(form, field) and getattr(form, field).data is not None:
            setattr(menu, field, getattr(form, field).data)

    menu.update_time = datetime.now()
    db.session.commit()

    return JsonResult.success(menu.to_dict(), "菜单更新成功")


@menu_bp.route('/<menu_id>', methods=['DELETE'])
def delete_menu(menu_id):
    """删除菜单"""
    # 查找菜单
    menu = Menu.query.filter_by(id=menu_id).first()
    if not menu:
        return JsonResult.error("菜单不存在")

    # 检查是否有子菜单
    if Menu.query.filter_by(parent_id=menu_id).first():
        return JsonResult.error("该菜单存在子菜单，无法删除")

    # 检查是否有角色使用该菜单
    if Role.query.filter(Role.menu_ids.contains(menu_id)).first():
        return JsonResult.error("该菜单正在被角色使用，无法删除")

    db.session.delete(menu)
    db.session.commit()
    return JsonResult.success(None, "菜单删除成功")


@menu_bp.route('/user/<user_id>/permissions', methods=['GET'])
def get_user_permissions(user_id):
    """获取用户权限（菜单列表）"""
    # 查找用户
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return JsonResult.error("用户不存在")

    # 获取用户角色
    user_roles = UserRole.query.filter_by(user_id=user_id).all()
    user_role_ids = [ur.role_id for ur in user_roles]

    # 收集所有菜单权限
    menu_ids = set()
    roles = Role.query.filter(Role.id.in_(user_role_ids)).all()
    for role in roles:
        if role.is_enabled():
            menu_ids.update(role.menu_ids)

    # 获取菜单详情并构建树形结构
    user_menus = Menu.query.filter(Menu.id.in_(list(menu_ids))).order_by(Menu.sort_order.asc()).all()

    def build_permission_tree(parent_id=""):
        children = []
        for menu in user_menus:
            if menu.parent_id == parent_id and menu.status == 1 and menu.is_visible:
                menu_dict = {
                    'id': menu.id,
                    'name': menu.name,
                    'path': menu.path,
                    'icon': menu.icon,
                    'level': menu.level,
                    'menu_type': menu.menu_type,
                    'permission': menu.permission,
                    'component': menu.component,
                    'is_external': menu.is_external,
                    'is_cache': menu.is_cache,
                    'children': build_permission_tree(menu.id)
                }
                children.append(menu_dict)

        children.sort(key=lambda x: next((m.sort_order for m in user_menus if m.id == x['id']), 0))
        return children

    result = build_permission_tree()
    return JsonResult.success(result, "获取用户权限成功")
