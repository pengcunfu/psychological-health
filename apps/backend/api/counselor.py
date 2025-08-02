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
from utils.validate import validate_args

counselor_bp = Blueprint('counselor', __name__, url_prefix='/counselor')


@counselor_bp.route('', methods=['GET'])
def get_counselors():
    """获取咨询师列表"""
    form = validate_args(CounselorQueryForm)

    query = Counselor.query

    if form.name.data:
        query = query.filter(Counselor.name.like(f'%{form.name.data}%'))
    if form.title.data:
        query = query.filter(Counselor.title.like(f'%{form.title.data}%'))
    if form.status.data is not None:
        query = query.filter(Counselor.status == form.status.data)

    # 分页查询
    pagination = query.order_by(Counselor.create_time.desc()).paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )

    return JsonResult.success({
        'list': [counselor.to_dict() for counselor in pagination.items],
        'total': pagination.total,
        'page': form.page.data,
        'per_page': form.per_page.data,
        'pages': pagination.pages
    })


@counselor_bp.route('/<counselor_id>', methods=['GET'])
def get_counselor(counselor_id):
    """获取单个咨询师详情"""
    counselor = Counselor.query.filter_by(id=counselor_id).first()
    if not counselor:
        return JsonResult.error('咨询师不存在', 404)

    return JsonResult.success(counselor.to_dict())


@counselor_bp.route('', methods=['POST'])
def create_counselor():
    """创建咨询师"""
    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    # 使用表单验证
    form = validate_args(CounselorCreateForm)

    # 创建咨询师
    counselor = Counselor(
        id=str(uuid.uuid4()),
        name=form.name.data,
        avatar=form.avatar.data or '',
        title=form.title.data or '',
        price=form.price.data or 0.0,
        rating=form.rating.data or 0.0,
        consultation_count=form.consultation_count.data or 0,
        introduction=form.introduction.data or '',
        tags=form.tags.data or '',
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

    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    # 使用表单验证
    form = CounselorUpdateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 更新咨询师信息
    if form.name.data is not None:
        counselor.name = form.name.data
    if form.avatar.data is not None:
        counselor.avatar = form.avatar.data
    if form.title.data is not None:
        counselor.title = form.title.data
    if form.price.data is not None:
        counselor.price = form.price.data
    if form.rating.data is not None:
        counselor.rating = form.rating.data
    if form.consultation_count.data is not None:
        counselor.consultation_count = form.consultation_count.data
    if form.introduction.data is not None:
        counselor.introduction = form.introduction.data
    if form.tags.data is not None:
        counselor.tags = form.tags.data
    if form.status.data is not None:
        counselor.status = form.status.data

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
