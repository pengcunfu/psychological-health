from flask import Blueprint
import uuid
from models.announcement import Announcement
from models.base import db
from utils.json_result import JsonResult
from form.announcement import AnnouncementCreateForm, AnnouncementUpdateForm, AnnouncementQueryForm
from utils.validate import validate_args, validate_data, check_id
from utils.model_helper import update_model_from_form

announcements_bp = Blueprint('announcements', __name__, url_prefix='/announcements')


@announcements_bp.route('', methods=['GET'])
def get_announcements():
    """获取公告列表"""
    # 使用表单验证查询参数
    form = validate_args(AnnouncementQueryForm)

    # 构建查询
    query = Announcement.query

    if form.counselor_id.data:
        query = query.filter(Announcement.counselor_id == form.counselor_id.data)
    if form.user_id.data:
        query = query.filter(Announcement.user_id == form.user_id.data)
    if form.service_id.data:
        query = query.filter(Announcement.service_id == form.service_id.data)
    if form.status.data:
        query = query.filter(Announcement.status == form.status.data)
    if form.date.data:
        query = query.filter(Announcement.date == form.date.data)

    # 分页查询
    pagination = query.order_by(Announcement.create_time.desc()).paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )

    announcements = [announcement.to_dict() for announcement in pagination.items]

    return JsonResult.success({
        'announcements': announcements,
        'total': pagination.total,
        'page': form.page.data,
        'per_page': form.per_page.data,
        'pages': pagination.pages
    })


@announcements_bp.route('/<announcement_id>', methods=['GET'])
def get_announcement(announcement_id):
    """获取单个公告详情"""
    check_id(announcement_id, "公告ID不能为空")
    announcement = Announcement.query.filter_by(id=announcement_id).first()
    if not announcement:
        return JsonResult.error('公告不存在', 404)

    return JsonResult.success(announcement.to_dict())


@announcements_bp.route('', methods=['POST'])
def create_announcement():
    """创建公告"""
    form: AnnouncementCreateForm = validate_data(AnnouncementCreateForm)

    # 创建公告
    announcement = Announcement(
        id=str(uuid.uuid4()),
        counselor_id=form.counselor_id.data,
        service_id=form.service_id.data,
        user_id=form.user_id.data,
        date=form.date.data,
        note=form.note.data or '',
        time_slot=form.time_slot.data,
        status=form.status.data or 1
    )

    db.session.add(announcement)
    db.session.commit()

    return JsonResult.success(announcement.to_dict(), '公告创建成功', 201)


@announcements_bp.route('/<announcement_id>', methods=['PUT'])
def update_announcement(announcement_id):
    """更新公告"""
    check_id(announcement_id, "公告ID不能为空")
    announcement = Announcement.query.filter_by(id=announcement_id).first()
    if not announcement:
        return JsonResult.error('公告不存在', 404)
    form = validate_data(AnnouncementUpdateForm)
    update_model_from_form(announcement, form)
    db.session.commit()
    return JsonResult.success(announcement.to_dict(), '公告更新成功')


@announcements_bp.route('/<announcement_id>', methods=['DELETE'])
def delete_announcement(announcement_id):
    """删除公告"""
    check_id(announcement_id, "公告ID不能为空")
    announcement = Announcement.query.filter_by(id=announcement_id).first()
    if not announcement:
        return JsonResult.error('公告不存在', 404)
    db.session.delete(announcement)
    db.session.commit()
    return JsonResult.success(None, '公告删除成功')
