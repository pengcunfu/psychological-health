"""
咨询师管理API
提供咨询师的增删改查功能
"""
from flask import Blueprint
import uuid

from models.counselor import Counselor
from models.base import db
from utils.json_result import JsonResult
from utils.validate import assert_id_exists
from utils.query import create_query_builder
from utils.image import process_counselor_images
from utils.model_helper import update_model_fields
from form.counselor import CounselorCreateForm, CounselorUpdateForm, CounselorQueryForm
from decorator.form import validate_form
from decorator.permission import role_required, permission_required

counselor_bp = Blueprint('counselor', __name__, url_prefix='/counselor')


@counselor_bp.route('', methods=['GET'])
@validate_form(CounselorQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("counselor:get_counselors")
def get_counselors(form):
    """获取咨询师列表"""
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

    # 确定排序方向
    order_column = sort_column.asc() if sort_order.lower() == 'asc' else sort_column.desc()

    # 使用QueryBuilder构建查询并分页
    builder = create_query_builder(Counselor) \
        .when(form.name.data, Counselor.name.like(f'%{form.name.data}%')) \
        .when(form.title.data, Counselor.title.like(f'%{form.title.data}%')) \
        .when(form.status.data is not None, Counselor.status == form.status.data) \
        .order_by(order_column)
    
    # 处理关键词搜索
    if form.keyword.data:
        keyword = f'%{form.keyword.data}%'
        builder.filter(
            (Counselor.name.like(keyword)) |
            (Counselor.title.like(keyword)) |
            (Counselor.introduction.like(keyword))
        )
    
    result = builder.paginate(form.page.data, form.per_page.data, 100)

    # 处理咨询师数据中的图片URL
    counselors_data = [counselor.to_dict() for counselor in result['items']]
    processed_counselors = process_counselor_images(counselors_data)

    return JsonResult.success({
        'list': processed_counselors,
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages'],
        'sort_by': sort_by,
        'sort_order': sort_order
    })


@counselor_bp.route('/<counselor_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("counselor:get_counselor")
def get_counselor(counselor_id):
    """获取单个咨询师详情"""
    assert_id_exists(counselor_id, "咨询师ID不能为空")
    
    counselor = Counselor.query.filter_by(id=counselor_id).first()
    if not counselor:
        return JsonResult.error('咨询师不存在', 404)

    # 处理咨询师数据中的图片URL
    counselor_data = process_counselor_images(counselor.to_dict())
    return JsonResult.success(counselor_data)


@counselor_bp.route('', methods=['POST'])
@validate_form(CounselorCreateForm)
@role_required(['admin', 'manager'])
@permission_required("counselor:create_counselor")
def create_counselor(form):
    """创建咨询师"""
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
@validate_form(CounselorUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("counselor:update_counselor")
def update_counselor(counselor_id, form):
    """更新咨询师信息"""
    assert_id_exists(counselor_id, "咨询师ID不能为空")
    
    counselor = Counselor.query.filter_by(id=counselor_id).first()
    if not counselor:
        return JsonResult.error('咨询师不存在', 404)

    # 使用统一的更新函数
    update_model_fields(counselor, form)
    db.session.commit()

    return JsonResult.success(counselor.to_dict(), '咨询师信息更新成功')


@counselor_bp.route('/<counselor_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("counselor:delete_counselor")
def delete_counselor(counselor_id):
    """删除咨询师"""
    assert_id_exists(counselor_id, "咨询师ID不能为空")
    
    counselor = Counselor.query.filter_by(id=counselor_id).first()
    if not counselor:
        return JsonResult.error('咨询师不存在', 404)

    db.session.delete(counselor)
    db.session.commit()

    return JsonResult.success(None, '咨询师删除成功')
