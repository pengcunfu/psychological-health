"""
咨询师管理API
提供咨询师的增删改查功能

接口列表：
- GET /counselor - 获取咨询师列表
- GET /counselor/<counselor_id> - 获取单个咨询师详情
- POST /counselor - 创建咨询师
- PUT /counselor/<counselor_id> - 更新咨询师
- DELETE /counselor/<counselor_id> - 删除咨询师
- GET /counselor/<counselor_id>/reviews - 获取咨询师的评价列表
- GET /counselor/<counselor_id>/appointments - 获取咨询师的预约列表
- POST /counselor/<counselor_id>/avatar - 上传咨询师头像
- PUT /counselor/<counselor_id>/status - 更新咨询师状态
"""
from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
import uuid

from models.counselor import Counselor
from models.base import db
from utils.json_result import JsonResult
from form.counselor import CounselorCreateForm, CounselorUpdateForm, CounselorQueryForm
from utils.validate import validate_args, validate_data
from utils.image import process_counselor_images
from utils.model_helper import update_model_from_form

counselor_bp = Blueprint('counselor', __name__, url_prefix='/counselor')


@counselor_bp.route('', methods=['GET'])
def get_counselors():
    """获取咨询师列表"""
    form = validate_args(CounselorQueryForm)

    query = Counselor.query

    # 搜索条件
    if form.name.data:
        query = query.filter(Counselor.name.like(f'%{form.name.data}%'))
    if form.title.data:
        query = query.filter(Counselor.title.like(f'%{form.title.data}%'))
    if form.keyword.data:
        # 关键词搜索：在姓名、职称、介绍中搜索
        keyword = f'%{form.keyword.data}%'
        query = query.filter(
            (Counselor.name.like(keyword)) |
            (Counselor.title.like(keyword)) |
            (Counselor.introduction.like(keyword))
        )
    if form.status.data is not None:
        query = query.filter(Counselor.status == form.status.data)

    # 排序逻辑
    sort_by = form.sort_by.data or 'create_time'
    sort_order = form.sort_order.data or 'desc'

    # 验证排序字段
    valid_sort_fields = {
        'create_time': Counselor.create_time,
        'rating': Counselor.rating,
        'price': Counselor.price,
        'consultation_count': Counselor.consultation_count,
        'name': Counselor.name
    }

    if sort_by not in valid_sort_fields:
        sort_by = 'create_time'

    sort_column = valid_sort_fields[sort_by]

    # 应用排序
    if sort_order.lower() == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # 分页查询
    pagination = query.paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )

    # 处理咨询师数据中的图片URL
    counselors_data = [counselor.to_dict() for counselor in pagination.items]
    processed_counselors = process_counselor_images(counselors_data)

    return JsonResult.success({
        'list': processed_counselors,
        'total': pagination.total,
        'page': form.page.data,
        'per_page': form.per_page.data,
        'pages': pagination.pages,
        'sort_by': sort_by,
        'sort_order': sort_order
    })


@counselor_bp.route('/<counselor_id>', methods=['GET'])
def get_counselor(counselor_id):
    """获取单个咨询师详情"""
    counselor = Counselor.query.filter_by(id=counselor_id).first()
    if not counselor:
        return JsonResult.error('咨询师不存在', 404)

    # 处理咨询师数据中的图片URL
    counselor_data = process_counselor_images(counselor.to_dict())
    return JsonResult.success(counselor_data)


@counselor_bp.route('', methods=['POST'])
def create_counselor():
    """创建咨询师"""
    # 使用统一的验证方式
    form = validate_data(CounselorCreateForm)

    # 创建咨询师
    counselor = Counselor(
        id=str(uuid.uuid4()),
        name=form.name.data,
        avatar=form.avatar.data or '',
        title=form.title.data or '',
        phone=form.phone.data or '',
        email=form.email.data or '',
        price=form.price.data or 0.0,
        rating=form.rating.data or 0.0,
        consultation_count=form.consultation_count.data or 0,
        introduction=form.introduction.data or '',
        tags=form.tags.data or '',
        specialty=form.specialty.data or '',
        bio=form.bio.data or '',
    )

    db.session.add(counselor)
    db.session.commit()

    return JsonResult.success(counselor.to_dict(), '咨询师创建成功', 201)


@counselor_bp.route('/<counselor_id>', methods=['PUT'])
def update_counselor(counselor_id):
    """更新咨询师信息"""
    counselor = Counselor.query.filter_by(id=counselor_id).first()
    if not counselor:
        return JsonResult.error('咨询师不存在', 404)

    # 使用统一的验证和更新函数
    form = validate_data(CounselorUpdateForm)
    update_model_from_form(counselor, form)
    db.session.commit()

    return JsonResult.success(counselor.to_dict(), '咨询师信息更新成功')


@counselor_bp.route('/<counselor_id>', methods=['DELETE'])
def delete_counselor(counselor_id):
    """删除咨询师"""
    counselor = Counselor.query.filter_by(id=counselor_id).first()
    if not counselor:
        return JsonResult.error('咨询师不存在', 404)

    db.session.delete(counselor)
    db.session.commit()

    return JsonResult.success(None, '咨询师删除成功')
