"""
公告管理API
提供系统公告的增删改查功能

接口列表：
- GET /announcement - 获取公告列表
- GET /announcement/<announcement_id> - 获取单个公告详情
- POST /announcement - 创建公告
- PUT /announcement/<announcement_id> - 更新公告
- DELETE /announcement/<announcement_id> - 删除公告
"""
from flask import Blueprint
import uuid
from datetime import datetime
from models.announcement import Announcement
from models.base import db
from utils.json_result import JsonResult
from form.announcement import AnnouncementCreateForm, AnnouncementUpdateForm, AnnouncementQueryForm
from utils.validate import validate_args, validate_data, check_id
from utils.model_helper import update_model_from_form

announcements_bp = Blueprint('announcement', __name__, url_prefix='/announcement')


@announcements_bp.route('', methods=['GET'])
def get_announcements():
    """获取公告列表"""
    # 使用表单验证查询参数
    form = validate_args(AnnouncementQueryForm)

    # 构建查询
    query = Announcement.query

    if form.title.data:
        query = query.filter(Announcement.title.contains(form.title.data))
    if form.type.data:
        query = query.filter(Announcement.type == form.type.data)
    if form.status.data:
        query = query.filter(Announcement.status == form.status.data)
    if form.priority.data:
        query = query.filter(Announcement.priority == form.priority.data)

    # 分页查询
    pagination = query.order_by(Announcement.create_time.desc()).paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )

    announcements = [announcement.to_dict() for announcement in pagination.items]

    return JsonResult.success({
        'list': announcements,
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

    # 解析时间字段
    start_time = None
    end_time = None
    
    if form.start_time.data:
        try:
            start_time = datetime.strptime(form.start_time.data, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return JsonResult.error('生效时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式', 400)
    
    if form.end_time.data:
        try:
            end_time = datetime.strptime(form.end_time.data, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return JsonResult.error('失效时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式', 400)

    # 创建公告
    announcement = Announcement(
        id=str(uuid.uuid4()),
        title=form.title.data,
        type=form.type.data,
        priority=form.priority.data,
        status=form.status.data,
        summary=form.summary.data or '',
        content=form.content.data,
        start_time=start_time,
        end_time=end_time,
        is_pinned=form.is_pinned.data or False
        # user_id 暂时不传入
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
    
    # 处理时间字段
    if form.start_time.data:
        try:
            announcement.start_time = datetime.strptime(form.start_time.data, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return JsonResult.error('生效时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式', 400)
    
    if form.end_time.data:
        try:
            announcement.end_time = datetime.strptime(form.end_time.data, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return JsonResult.error('失效时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式', 400)
    
    # 更新其他字段
    if form.title.data is not None:
        announcement.title = form.title.data
    if form.type.data is not None:
        announcement.type = form.type.data
    if form.priority.data is not None:
        announcement.priority = form.priority.data
    if form.status.data is not None:
        announcement.status = form.status.data
    if form.summary.data is not None:
        announcement.summary = form.summary.data
    if form.content.data is not None:
        announcement.content = form.content.data
    if form.is_pinned.data is not None:
        announcement.is_pinned = form.is_pinned.data
    
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
