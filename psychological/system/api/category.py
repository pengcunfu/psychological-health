"""
分类管理API
提供系统分类的增删改查功能
"""
from flask import Blueprint
import uuid

from ..models import Category
from pcf_flask_helper.model.base import db
from pcf_flask_helper.common import json_success
from pcf_flask_helper.form.validate import assert_id_exists
from pcf_flask_helper.model.query import create_query_builder, assert_exists
from psychological.utils.model_helper import update_model_fields
from ..form import CategoryCreateForm, CategoryUpdateForm, CategoryQueryForm, CategoryStatusUpdateForm
from psychological.utils.decorator import validate_form
from psychological.utils.decorator.permission import role_required, permission_required

category_bp = Blueprint('category', __name__, url_prefix='/category')


@category_bp.route('', methods=['GET'])
@validate_form(CategoryQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("category:get_categories")
def get_categories(form):
    """获取分类列表"""
    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(Category) \
        .when(form.name.data, Category.name.like(f'%{form.name.data}%')) \
        .when(form.type.data, Category.type == form.type.data) \
        .when(form.status.data is not None, Category.status == form.status.data) \
        .order_by(Category.sort_order.asc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return json_success({
        'list': [category.to_dict() for category in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@category_bp.route('/<category_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("category:get_category")
def get_category(category_id):
    """获取单个分类详情"""
    assert_id_exists(category_id, "分类ID不能为空")

    category = assert_exists(Category, Category.id == category_id, "分类不存在")

    return json_success(category.to_dict())


@category_bp.route('', methods=['POST'])
@validate_form(CategoryCreateForm)
@role_required(['admin', 'manager'])
@permission_required("category:create_category")
def create_category(form):
    """创建分类"""
    # 创建分类
    category = Category(
        id=str(uuid.uuid4()),
        name=form.name.data,
        type=form.type.data or 'course',
        icon=form.icon.data or '',
        path=form.path.data or '',
        description=form.description.data or '',
        sort_order=form.sort_order.data or 0,
        status=form.status.data or 1
    )

    db.session.add(category)
    db.session.commit()

    return json_success(category.to_dict(), '分类创建成功', 201)


@category_bp.route('/<category_id>', methods=['PUT'])
@validate_form(CategoryUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("category:update_category")
def update_category(category_id, form):
    """更新分类"""
    assert_id_exists(category_id, "分类ID不能为空")

    category = assert_exists(Category, Category.id == category_id, "分类不存在")

    # 使用统一的更新函数
    update_model_fields(category, form)

    db.session.commit()

    return json_success(category.to_dict(), '分类更新成功')


@category_bp.route('/<category_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("category:delete_category")
def delete_category(category_id):
    """删除分类"""
    assert_id_exists(category_id, "分类ID不能为空")

    category = assert_exists(Category, Category.id == category_id, "分类不存在")

    # 这里可以添加检查是否有关联数据的逻辑
    # 例如：检查是否有课程或产品使用了该分类
    # 如果有关联数据，可以返回错误或者同时删除关联数据

    db.session.delete(category)
    db.session.commit()

    return json_success(None, '分类删除成功')


@category_bp.route('/<category_id>/status', methods=['PATCH'])
@validate_form(CategoryStatusUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("category:update_category_status")
def update_category_status(category_id, form):
    """更新分类状态（启用/禁用）"""
    assert_id_exists(category_id, "分类ID不能为空")

    category = assert_exists(Category, Category.id == category_id, "分类不存在")

    category.status = form.status.data
    db.session.commit()

    return json_success(category.to_dict(), f'分类已{"启用" if form.status.data == 1 else "禁用"}')
