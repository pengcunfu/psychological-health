"""
评价管理API
提供用户评价的增删改查功能
"""
from flask import Blueprint
import uuid

from models.review import Review
from models.base import db
from utils.json_result import JsonResult
from utils.validate import assert_id_exists
from utils.query import create_query_builder
from utils.model_helper import update_model_fields
from form.review import ReviewCreateForm, ReviewUpdateForm, ReviewQueryForm
from decorator.form import validate_form
from decorator.permission import role_required, permission_required

review_bp = Blueprint('review', __name__, url_prefix='/review')


@review_bp.route('', methods=['GET'])
@validate_form(ReviewQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("review:get_reviews")
def get_reviews(form):
    """获取评价列表"""
    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(Review) \
        .when(form.get_counselor_id(), Review.counselor_id == form.get_counselor_id()) \
        .when(form.get_order_id(), Review.order_id == form.get_order_id()) \
        .order_by(Review.create_time.desc()) \
        .paginate(form.get_page(), form.get_per_page(), 100)

    return JsonResult.success({
        'reviews': [review.to_dict() for review in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@review_bp.route('/<review_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("review:get_review")
def get_review(review_id):
    """获取单个评价详情"""
    assert_id_exists(review_id, "评价ID不能为空")

    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return JsonResult.error('评价不存在', 404)

    return JsonResult.success(review.to_dict())


@review_bp.route('', methods=['POST'])
@validate_form(ReviewCreateForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("review:create_review")
def create_review(form):
    """创建评价"""
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
@validate_form(ReviewUpdateForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("review:update_review")
def update_review(review_id, form):
    """更新评价"""
    assert_id_exists(review_id, "评价ID不能为空")

    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return JsonResult.error('评价不存在', 404)

    # 使用model_helper的update_model_from_form简化更新逻辑
    update_model_fields(review, form)

    db.session.commit()

    return JsonResult.success(review.to_dict(), '评价更新成功')


@review_bp.route('/<review_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("review:delete_review")
def delete_review(review_id):
    """删除评价"""
    assert_id_exists(review_id, "评价ID不能为空")

    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return JsonResult.error('评价不存在', 404)

    db.session.delete(review)
    db.session.commit()

    return JsonResult.success(None, '评价删除成功')
