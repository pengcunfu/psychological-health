"""
评价管理API
提供用户评价的增删改查功能

接口列表：
- GET /review - 获取评价列表
- GET /review/<review_id> - 获取单个评价详情
- POST /review - 创建评价
- PUT /review/<review_id> - 更新评价
- DELETE /review/<review_id> - 删除评价
- GET /review/user/<user_id> - 获取用户的评价列表
- GET /review/counselor/<counselor_id> - 获取咨询师的评价列表
- GET /review/course/<course_id> - 获取课程的评价列表
"""
from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError
import uuid

from models.review import Review
from models.base import db
from utils.json_result import JsonResult
from utils.swagger_models import create_review_models
from form.review import ReviewCreateForm, ReviewUpdateForm, ReviewQueryForm

review_bp = Blueprint('review', __name__, url_prefix='/review')


@review_bp.route('', methods=['GET'])
def get_reviews():
    """获取评价列表"""
    # 使用表单验证查询参数
    form = ReviewQueryForm(data=request.args)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 构建查询
    query = Review.query

    if form.get_counselor_id():
        query = query.filter(Review.counselor_id == form.get_counselor_id())
    if form.get_order_id():
        query = query.filter(Review.order_id == form.get_order_id())

    # 分页查询
    pagination = query.order_by(Review.create_time.desc()).paginate(
        page=form.get_page(), per_page=form.get_per_page(), error_out=False
    )

    reviews = [review.to_dict() for review in pagination.items]

    return JsonResult.success({
        'reviews': reviews,
        'total': pagination.total,
        'page': form.get_page(),
        'per_page': form.get_per_page(),
        'pages': pagination.pages
    })


@review_bp.route('/<review_id>', methods=['GET'])
def get_review(review_id):
    """获取单个评价详情"""
    if not review_id or not review_id.strip():
        return JsonResult.error('评价ID不能为空', 400)

    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return JsonResult.error('评价不存在', 404)

    return JsonResult.success(review.to_dict())


@review_bp.route('', methods=['POST'])
def create_review():
    """创建评价"""
    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    # 使用表单验证数据
    form = ReviewCreateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 创建评价
    review = Review(
        id=str(uuid.uuid4()),
        counselor_id=form.counselor_id.data,
        order_id=form.order_id.data,
        content=form.content.data or '',
        rating=form.rating.data or 5
    )

    db.session.add(review)
    db.session.commit()

    return JsonResult.success(review.to_dict(), '评价创建成功')


@review_bp.route('/<review_id>', methods=['PUT'])
def update_review(review_id):
    """更新评价"""
    if not review_id or not review_id.strip():
        return JsonResult.error('评价ID不能为空', 400)

    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return JsonResult.error('评价不存在', 404)

    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    # 使用表单验证数据
    form = ReviewUpdateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 更新字段
    if form.content.data is not None:
        review.content = form.content.data
    if form.rating.data is not None:
        review.rating = form.rating.data

    db.session.commit()

    return JsonResult.success(review.to_dict(), '评价更新成功')


@review_bp.route('/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """删除评价"""
    if not review_id or not review_id.strip():
        return JsonResult.error('评价ID不能为空', 400)

    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return JsonResult.error('评价不存在', 404)

    db.session.delete(review)
    db.session.commit()

    return JsonResult.success(None, '评价删除成功')
