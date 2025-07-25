from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
import uuid

from models.category import Category
from models.base import db
from utils.json_result import JsonResult
from form.category import CategoryCreateForm, CategoryUpdateForm, CategoryQueryForm, CategoryStatusUpdateForm

category_bp = Blueprint('category', __name__, url_prefix='/categories')


@category_bp.route('', methods=['GET'])
def get_categories():
    """获取分类列表"""
    # 使用表单验证查询参数
    form = CategoryQueryForm(data=request.args)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 构建查询
    query = Category.query

    if form.name.data:
        query = query.filter(Category.name.like(f'%{form.name.data}%'))
    if form.status.data is not None:
        query = query.filter(Category.status == form.status.data)

    # 分页查询
    pagination = query.order_by(Category.sort_order.asc()).paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )

    return JsonResult.success({
        'categories': [category.to_dict() for category in pagination.items],
        'total': pagination.total,
        'page': form.page.data,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    })


@category_bp.route('/<category_id>', methods=['GET'])
def get_category(category_id):
    """获取单个分类详情"""
    category = Category.query.filter_by(id=category_id).first()
    if not category:
        return JsonResult.error('分类不存在', 404)

    return JsonResult.success(category.to_dict())


@category_bp.route('', methods=['POST'])
def create_category():
    """创建分类"""
    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    # 使用表单验证
    form = CategoryCreateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 创建分类
    category = Category(
        id=str(uuid.uuid4()),
        name=form.name.data,
        icon=form.icon.data or '',
        path=form.path.data or '',
        description=form.description.data or '',
        sort_order=form.sort_order.data or 0,
        status=form.status.data or 1
    )

    db.session.add(category)
    db.session.commit()

    return JsonResult.success(category.to_dict(), '分类创建成功', 201)


@category_bp.route('/<category_id>', methods=['PUT'])
def update_category(category_id):
    """更新分类"""
    category = Category.query.filter_by(id=category_id).first()
    if not category:
        return JsonResult.error('分类不存在', 404)

    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    # 使用表单验证
    form = CategoryUpdateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 更新字段
    if form.name.data:
        category.name = form.name.data
    if form.icon.data is not None:
        category.icon = form.icon.data
    if form.path.data is not None:
        category.path = form.path.data
    if form.description.data is not None:
        category.description = form.description.data
    if form.sort_order.data is not None:
        category.sort_order = form.sort_order.data
    if form.status.data is not None:
        category.status = form.status.data

    db.session.commit()

    return JsonResult.success(category.to_dict(), '分类更新成功')


@category_bp.route('/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    """删除分类"""
    category = Category.query.filter_by(id=category_id).first()
    if not category:
        return JsonResult.error('分类不存在', 404)

    # 这里可以添加检查是否有关联数据的逻辑
    # 例如：检查是否有课程或产品使用了该分类
    # 如果有关联数据，可以返回错误或者同时删除关联数据

    db.session.delete(category)
    db.session.commit()

    return JsonResult.success(None, '分类删除成功')


@category_bp.route('/<category_id>/status', methods=['PATCH'])
def update_category_status(category_id):
    """更新分类状态（启用/禁用）"""
    category = Category.query.filter_by(id=category_id).first()
    if not category:
        return JsonResult.error('分类不存在', 404)

    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    # 使用表单验证
    form = CategoryStatusUpdateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    category.status = form.status.data
    db.session.commit()

    return JsonResult.success(category.to_dict(), f'分类已{"启用" if form.status.data == 1 else "禁用"}')
