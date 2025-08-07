from flask import Blueprint, request, g
from sqlalchemy import or_, and_
from models.consultant import Consultant, GenderEnum, RelationshipEnum
from models.user import User
from form.consultant import ConsultantCreateForm, ConsultantUpdateForm, ConsultantListForm
import uuid

from models.base import db
from utils.json_result import JsonResult
from utils.validate import validate_args, validate_data
from middleware.auth import role_required, Roles


consultant_bp = Blueprint('consultant', __name__, url_prefix='/consultant')


@consultant_bp.route('', methods=['GET'])
# @role_required([Roles.ADMIN, Roles.MANAGER])
def get_consultants():
    """获取咨询人列表（管理后台）"""
    form = validate_args(ConsultantListForm)

    # 构建查询 - 管理后台显示所有咨询人，使用LEFT JOIN支持user_id为None的情况
    query = Consultant.query.outerjoin(User, Consultant.user_id == User.id)

    # 关键词搜索
    if form.keyword.data:
        keyword = f"%{form.keyword.data}%"
        query = query.filter(
            or_(
                Consultant.real_name.like(keyword),
                Consultant.phone.like(keyword),
                Consultant.emergency_name.like(keyword),
                Consultant.emergency_phone.like(keyword),
                User.username.like(keyword)
            )
        )

    # 性别筛选
    if form.gender.data:
        query = query.filter(Consultant.gender == GenderEnum(form.gender.data))

    # 状态筛选
    if form.status.data is not None:
        query = query.filter(Consultant.status == form.status.data)

    # 排序：默认咨询人优先，然后按创建时间倒序
    query = query.order_by(Consultant.is_default.desc(), Consultant.create_time.desc())

    # 分页
    page = form.page.data or 1
    per_page = form.per_page.data or 10
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    consultants_data = []
    for consultant in pagination.items:
        consultant_dict = consultant.to_dict()
        # 添加用户信息
        if consultant.user:
            consultant_dict['user_info'] = {
                'username': consultant.user.username,
                'phone': consultant.user.phone,
                'email': consultant.user.email
            }
        else:
            consultant_dict['user_info'] = None
        consultants_data.append(consultant_dict)

    return JsonResult.success({
        'list': consultants_data,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@consultant_bp.route('/<consultant_id>', methods=['GET'])
# @role_required([Roles.ADMIN, Roles.MANAGER])
def get_consultant_detail(consultant_id):
    """获取咨询人详情（管理后台）"""
    consultant = Consultant.query.filter_by(id=consultant_id).first()

    if not consultant:
        return JsonResult.error('咨询人不存在')

    consultant_dict = consultant.to_dict()
    # 添加用户信息
    if consultant.user:
        consultant_dict['user_info'] = {
            'username': consultant.user.username,
            'phone': consultant.user.phone,
            'email': consultant.user.email
        }

    return JsonResult.success(consultant_dict)


@consultant_bp.route('', methods=['POST'])
# @role_required([Roles.ADMIN, Roles.MANAGER])
def create_consultant():
    """创建咨询人（管理后台）"""
    form = validate_data(ConsultantCreateForm)

    # 生成唯一ID
    consultant_id = str(uuid.uuid4())

    # 检查手机号是否已存在（全局检查）
    existing = Consultant.query.filter_by(phone=form.phone.data).first()
    if existing:
        return JsonResult.error('该手机号已存在咨询人信息')

    # 检查用户是否存在
    user = User.query.filter_by(id=form.user_id.data).first()
    if not user:
        return JsonResult.error('指定的用户不存在')

    # 创建咨询人
    consultant = Consultant(
        id=consultant_id,
        user_id=form.user_id.data if form.user_id.data and str(form.user_id.data).strip() else None,
        real_name=form.real_name.data,
        birth_year=form.birth_year.data or 0,
        birth_month=form.birth_month.data or 0,
        gender=GenderEnum(form.gender.data),
        phone=form.phone.data,
        emergency_name=form.emergency_name.data,
        emergency_relationship=RelationshipEnum(form.emergency_relationship.data),
        emergency_phone=form.emergency_phone.data,
        notes=form.notes.data if form.notes.data and str(form.notes.data).strip() else None,
        is_default=form.is_default.data or 0
    )

    db.session.add(consultant)
    db.session.commit()
    return JsonResult.success(consultant.to_dict(), '咨询人创建成功')



@consultant_bp.route('/<consultant_id>', methods=['PUT'])
# @role_required([Roles.ADMIN, Roles.MANAGER])
def update_consultant(consultant_id):
    """更新咨询人信息（管理后台）"""
    form = validate_data(ConsultantUpdateForm)

    # 查找咨询人
    consultant = Consultant.query.filter_by(id=consultant_id).first()

    if not consultant:
        return JsonResult.error('咨询人不存在')

    # 检查手机号是否已存在（排除当前咨询人）
    existing = Consultant.query.filter(
        and_(
            Consultant.phone == form.phone.data,
            Consultant.id != consultant_id
        )
    ).first()
    if existing:
        return JsonResult.error('该手机号已存在其他咨询人信息')

    # 处理 is_default 字段
    is_default = 0
    if form.is_default.data is not None:
        if isinstance(form.is_default.data, bool):
            is_default = 1 if form.is_default.data else 0
        elif isinstance(form.is_default.data, (int, str)):
            try:
                is_default = 1 if int(form.is_default.data) == 1 else 0
            except (ValueError, TypeError):
                is_default = 0

    # 处理年份和月份字段
    birth_year = None
    if form.birth_year.data is not None and form.birth_year.data != '':
        try:
            birth_year = int(form.birth_year.data)
        except (ValueError, TypeError):
            birth_year = None
    
    birth_month = None
    if form.birth_month.data is not None and form.birth_month.data != '':
        try:
            birth_month = int(form.birth_month.data)
        except (ValueError, TypeError):
            birth_month = None

    # 如果设置为默认咨询人，需要取消该用户的其他默认咨询人
    if is_default == 1 and consultant.user_id:
        Consultant.query.filter(
            and_(
                Consultant.user_id == consultant.user_id,
                Consultant.is_default == 1,
                Consultant.id != consultant_id
            )
        ).update({'is_default': 0})

    # 更新咨询人信息
    consultant.real_name = form.real_name.data
    consultant.birth_year = birth_year
    consultant.birth_month = birth_month
    consultant.gender = GenderEnum(form.gender.data)
    consultant.phone = form.phone.data
    consultant.emergency_name = form.emergency_name.data
    consultant.emergency_relationship = RelationshipEnum(form.emergency_relationship.data)
    consultant.emergency_phone = form.emergency_phone.data
    consultant.notes = form.notes.data if form.notes.data and str(form.notes.data).strip() else None
    consultant.is_default = is_default

    if form.status.data is not None:
        consultant.status = form.status.data

    try:
        db.session.commit()
        return JsonResult.success(consultant.to_dict(), '咨询人更新成功')
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'更新失败: {str(e)}')


@consultant_bp.route('/<consultant_id>', methods=['DELETE'])
# @role_required([Roles.ADMIN, Roles.MANAGER])
def delete_consultant(consultant_id):
    """删除咨询人（管理后台）"""
    consultant = Consultant.query.filter_by(id=consultant_id).first()

    if not consultant:
        return JsonResult.error('咨询人不存在')

    # 检查是否有关联的预约记录
    # if consultant.appointments:
    #     return JsonResult.error('该咨询人存在预约记录，无法删除')

    try:
        db.session.delete(consultant)
        db.session.commit()
        return JsonResult.success(message='咨询人删除成功')
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'删除失败: {str(e)}')


@consultant_bp.route('/<consultant_id>/set-default', methods=['PUT'])
# @role_required([Roles.ADMIN, Roles.MANAGER])
def set_default_consultant(consultant_id):
    """设置默认咨询人（管理后台）"""
    consultant = Consultant.query.filter_by(id=consultant_id).first()

    if not consultant:
        return JsonResult.error('咨询人不存在')

    if not consultant.user_id:
        return JsonResult.error('该咨询人未关联用户，无法设置为默认')

    try:
        # 取消该用户的其他默认咨询人
        Consultant.query.filter(
            and_(
                Consultant.user_id == consultant.user_id,
                Consultant.is_default == 1,
                Consultant.id != consultant_id
            )
        ).update({'is_default': 0})

        # 设置当前为默认
        consultant.is_default = 1
        db.session.commit()

        return JsonResult.success(consultant.to_dict(), '默认咨询人设置成功')
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'设置失败: {str(e)}')


@consultant_bp.route('/stats', methods=['GET'])
# @role_required([Roles.ADMIN, Roles.MANAGER])
def get_consultant_stats():
    """获取咨询人统计信息（管理后台）"""
    try:
        total_count = Consultant.query.count()
        active_count = Consultant.query.filter_by(status=1).count()
        male_count = Consultant.query.filter_by(gender=GenderEnum.MALE).count()
        female_count = Consultant.query.filter_by(gender=GenderEnum.FEMALE).count()
        default_count = Consultant.query.filter_by(is_default=1).count()

        return JsonResult.success({
            'total_count': total_count,
            'active_count': active_count,
            'inactive_count': total_count - active_count,
            'male_count': male_count,
            'female_count': female_count,
            'default_count': default_count
        })
    except Exception as e:
        return JsonResult.error(f'获取统计信息失败: {str(e)}')


@consultant_bp.route('/enums', methods=['GET'])
def get_consultant_enums():
    """获取咨询人相关枚举值"""
    return JsonResult.success({
        'genders': [
            {'value': 'male', 'label': '男'},
            {'value': 'female', 'label': '女'}
        ],
        'relationships': [
            {'value': 'self', 'label': '本人'},
            {'value': 'spouse', 'label': '配偶'},
            {'value': 'child', 'label': '子女'},
            {'value': 'parent', 'label': '父母'},
            {'value': 'sibling', 'label': '兄弟姐妹'},
            {'value': 'friend', 'label': '朋友'},
            {'value': 'other', 'label': '其他'}
        ]
    })
