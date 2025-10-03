"""
菜单管理API
提供系统菜单的增删改查功能
"""
from flask import Blueprint
from psychological.models.base import db
from psychological.models.menu import Menu
from psychological.models.role import Role
from psychological.models.user import User
from psychological.models.user_role import UserRole
from pcf_flask_helper.common import json_success, json_error
from psychological.utils.validate import assert_id_exists
from psychological.utils.query import create_query_builder
from psychological.utils.model_helper import update_model_fields
from psychological.form.menu import MenuQueryForm, MenuCreateForm, MenuUpdateForm
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required
from datetime import datetime
import uuid

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")


@menu_bp.route('', methods=['GET'])
@validate_form(MenuQueryForm)
@role_required(['admin', 'manager'])
@permission_required("menu:get_menus")
def get_menus(form):
    """获取菜单列表"""
    keyword = form.keyword.data
    page = form.page.data or 1
    size = form.size.data or 10

    # 如果有搜索关键词，返回平铺列表用于搜索
    if keyword:
        # 使用QueryBuilder构建查询并分页
        result = create_query_builder(Menu) \
            .filter(Menu.name.contains(keyword)) \
            .order_by(Menu.sort_order.asc(), Menu.create_time.desc()) \
            .paginate(page, size, 100)

        return json_success({
            'list': [menu.to_dict() for menu in result['items']],
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'pages': result['pages'],
            'is_tree': False
        })

    # 没有搜索关键词时，返回树形结构
    all_menus = create_query_builder(Menu) \
        .order_by(Menu.sort_order.asc(), Menu.create_time.asc()) \
        .all()

    def build_menu_tree(parent_id=""):
        """构建菜单树"""
        children = []
        for menu in all_menus:
            if menu.parent_id == parent_id:
                menu_dict = menu.to_dict()
                # 递归获取子菜单
                menu_dict['children'] = build_menu_tree(menu.id)
                children.append(menu_dict)

        # 按排序字段排序
        children.sort(key=lambda x: x['sort_order'])
        return children

    # 构建树形结构
    tree_data = build_menu_tree()

    # 计算总数（扁平化计算）
    total_count = len(all_menus)

    # 对树形数据进行分页（只对顶级菜单分页，子菜单全部返回）
    start = (page - 1) * size
    end = start + size
    paginated_tree = tree_data[start:end]

    return json_success({
        'list': paginated_tree,
        'total': len(tree_data),  # 顶级菜单数量作为分页基数
        'total_items': total_count,  # 总菜单数量
        'page': page,
        'per_page': size,
        'is_tree': True
    })


@menu_bp.route('', methods=['POST'])
@validate_form(MenuCreateForm)
@role_required(['admin', 'manager'])
@permission_required("menu:create_menu")
def create_menu(form):
    """创建菜单"""
    # 检查菜单名称是否重复
    existing_menu = create_query_builder(Menu) \
        .filter(Menu.name == form.name.data) \
        .first()
    if existing_menu:
        return json_error("菜单名称已存在", 400)

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
    return json_success(menu.to_dict(), "菜单创建成功", 201)


@menu_bp.route('/<menu_id>', methods=['PUT'])
@validate_form(MenuUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("menu:update_menu")
def update_menu(menu_id, form):
    """更新菜单"""
    assert_id_exists(menu_id, "菜单ID不能为空")

    # 查找菜单
    menu = Menu.query.filter_by(id=menu_id).first()
    if not menu:
        return json_error("菜单不存在", 404)

    # 检查菜单名称是否重复（排除自己）
    if form.name.data and form.name.data != menu.name:
        existing_menu = create_query_builder(Menu) \
            .filter(Menu.name == form.name.data) \
            .first()
        if existing_menu:
            return json_error("菜单名称已存在", 400)

    # 使用统一的更新函数
    update_model_fields(menu, form)
    menu.update_time = datetime.now()
    db.session.commit()

    return json_success(menu.to_dict(), "菜单更新成功")


@menu_bp.route('/<menu_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("menu:delete_menu")
def delete_menu(menu_id):
    """删除菜单"""
    assert_id_exists(menu_id, "菜单ID不能为空")

    # 查找菜单
    menu = Menu.query.filter_by(id=menu_id).first()
    if not menu:
        return json_error("菜单不存在", 404)

    # 检查是否有子菜单
    child_menu = create_query_builder(Menu) \
        .filter(Menu.parent_id == menu_id) \
        .first()
    if child_menu:
        return json_error("该菜单存在子菜单，无法删除", 400)

    # 检查是否有角色使用该菜单
    role_using_menu = create_query_builder(Role) \
        .filter(Role.menu_ids.contains(menu_id)) \
        .first()
    if role_using_menu:
        return json_error("该菜单正在被角色使用，无法删除", 400)

    db.session.delete(menu)
    db.session.commit()
    return json_success(None, "菜单删除成功")


@menu_bp.route('/user/<user_id>/permissions', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("menu:get_user_permissions")
def get_user_permissions(user_id):
    """获取用户权限（菜单列表）"""
    assert_id_exists(user_id, "用户ID不能为空")

    # 查找用户
    user = create_query_builder(User) \
        .filter(User.id == user_id) \
        .first()
    if not user:
        return json_error("用户不存在", 404)

    # 获取用户角色
    user_roles = create_query_builder(UserRole) \
        .filter(UserRole.user_id == user_id) \
        .all()
    user_role_ids = [ur.role_id for ur in user_roles]

    # 收集所有菜单权限
    menu_ids = set()
    if user_role_ids:
        roles = create_query_builder(Role) \
            .filter(Role.id.in_(user_role_ids)) \
            .all()
        for role in roles:
            if role.is_enabled():
                menu_ids.update(role.menu_ids)

    # 获取菜单详情并构建树形结构
    if menu_ids:
        user_menus = create_query_builder(Menu) \
            .filter(Menu.id.in_(list(menu_ids))) \
            .order_by(Menu.sort_order.asc()) \
            .all()
    else:
        user_menus = []

    def build_permission_tree(parent_id=""):
        children = []
        for menu in user_menus:
            if menu.parent_id == parent_id and menu.status == 1 and menu.is_visible == 1:
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

        children.sort(key=lambda x: next(
            (m.sort_order for m in user_menus if m.id == x['id']), 0))
        return children

    result = build_permission_tree()
    return json_success(result, "获取用户权限成功")


@menu_bp.route('/tree', methods=['GET'])
@role_required(['admin', 'manager'])
@permission_required("menu:get_menu_tree")
def get_menu_tree():
    """获取完整的菜单树结构（用于角色权限配置等）"""
    # 获取所有启用的菜单
    all_menus = create_query_builder(Menu) \
        .filter(Menu.status == 1) \
        .order_by(Menu.sort_order.asc(), Menu.create_time.desc()) \
        .all()

    def build_tree(parent_id=""):
        """构建菜单树"""
        children = []
        for menu in all_menus:
            if menu.parent_id == parent_id:
                menu_node = {
                    'id': menu.id,
                    'key': menu.id,
                    'title': menu.name,
                    'name': menu.name,
                    'level': menu.level,
                    'menu_type': menu.menu_type,
                    'sort_order': menu.sort_order,
                    'children': build_tree(menu.id)
                }
                children.append(menu_node)

        # 按排序字段排序
        children.sort(key=lambda x: x['sort_order'])
        return children

    tree_data = build_tree()
    return json_success(tree_data, "获取菜单树成功")
