"""
公告管理API
提供系统公告的增删改查功能，包含权限控制
"""
from flask import Blueprint
import uuid
from datetime import datetime
from psychological.models.announcement import Announcement
from psychological.models.base import db
from pcf_flask_helper.common import json_success, json_error
from psychological.form.announcement import AnnouncementCreateForm, AnnouncementUpdateForm, AnnouncementQueryForm
from psychological.utils.validate import assert_id_exists
from psychological.utils.query import assert_exists
from psychological.utils.auth_helper import is_manager_user, assert_current_user_id
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required
from psychological.utils.model_helper import update_model_fields
from psychological.utils.query import create_query_builder


announcements_bp = Blueprint(
    'announcement', __name__, url_prefix='/announcement')


@announcements_bp.route('', methods=['GET'])
@validate_form(AnnouncementQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("announcement:get_announcements")
def get_announcements(form):
    """获取公告列表"""

    # 一行搞定所有条件和分页！
    result = create_query_builder(Announcement) \
        .unless(is_manager_user(), Announcement.status == 'published') \
        .when(form.title.data, Announcement.title.contains(form.title.data)) \
        .when(form.type.data, Announcement.type == form.type.data) \
        .when(form.status.data, Announcement.status == form.status.data) \
        .when(form.priority.data, Announcement.priority == form.priority.data) \
        .order_by(Announcement.create_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return json_success({
        'list': [announcement.to_dict() for announcement in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@announcements_bp.route('/<announcement_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("announcement:get_announcement")
def get_announcement(announcement_id):
    """获取单个公告详情"""
    assert_id_exists(announcement_id, "公告ID不能为空")

    # 普通用户只能查看已发布的公告
    if not is_manager_user():
        announcement = assert_exists(
            Announcement,
            [Announcement.id == announcement_id,
             Announcement.status == 'published'],
            "公告不存在"
        )
    else:
        announcement = assert_exists(
            Announcement, Announcement.id == announcement_id, "公告不存在")

    return json_success(announcement.to_dict())


@announcements_bp.route('', methods=['POST'])
@validate_form(AnnouncementCreateForm)
@role_required(['admin', 'manager'])
@permission_required("announcement:create_announcement")
def create_announcement(form):
    """创建公告（仅管理员）"""
    current_user_id = assert_current_user_id()

    # 解析时间字段（表单已验证格式）
    start_time = None
    end_time = None

    if form.start_time.data:
        start_time = datetime.strptime(
            form.start_time.data, '%Y-%m-%d %H:%M:%S')

    if form.end_time.data:
        end_time = datetime.strptime(
            form.end_time.data, '%Y-%m-%d %H:%M:%S')

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
        is_pinned=form.is_pinned.data or False,
        user_id=current_user_id  # 添加创建者ID
    )

    db.session.add(announcement)
    db.session.commit()

    return json_success(announcement.to_dict(), '公告创建成功', 201)


@announcements_bp.route('/<announcement_id>', methods=['PUT'])
@validate_form(AnnouncementUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("announcement:update_announcement")
def update_announcement(announcement_id, form):
    """更新公告（仅管理员）"""
    assert_id_exists(announcement_id, "公告ID不能为空")
    announcement = assert_exists(
        Announcement, Announcement.id == announcement_id, "公告不存在")

    # 处理时间字段转换（表单已验证格式）
    if form.start_time.data:
        announcement.start_time = datetime.strptime(
            form.start_time.data, '%Y-%m-%d %H:%M:%S')

    if form.end_time.data:
        announcement.end_time = datetime.strptime(
            form.end_time.data, '%Y-%m-%d %H:%M:%S')

    # 使用model_helper的update_model_from_form简化更新逻辑
    update_model_fields(announcement, form)

    db.session.commit()
    return json_success(announcement.to_dict(), '公告更新成功')


@announcements_bp.route('/<announcement_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("announcement:delete_announcement")
def delete_announcement(announcement_id):
    """删除公告（仅管理员）"""
    assert_id_exists(announcement_id, "公告ID不能为空")
    announcement = assert_exists(
        Announcement, Announcement.id == announcement_id, "公告不存在")
    db.session.delete(announcement)
    db.session.commit()
    return json_success(None, '公告删除成功')


@announcements_bp.route('/active', methods=['GET'])
@validate_form(AnnouncementQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("announcement:get_active_announcements")
def get_active_announcements(form):
    """获取有效公告列表（普通用户接口）"""
    current_time = datetime.now()

    result = create_query_builder(Announcement) \
        .filter(Announcement.status == 'published') \
        .filter(
        (Announcement.start_time.is_(None)) | (
                Announcement.start_time <= current_time),
        (Announcement.end_time.is_(None)) | (
                Announcement.end_time >= current_time)
    ) \
        .when(form.title.data, Announcement.title.contains(form.title.data)) \
        .when(form.type.data, Announcement.type == form.type.data) \
        .when(form.priority.data, Announcement.priority == form.priority.data) \
        .order_by(
        Announcement.is_pinned.desc(),
        Announcement.priority.desc(),
        Announcement.create_time.desc()
    ) \
        .paginate(form.page.data, form.per_page.data, 100)

    return json_success({
        'list': [announcement.to_dict() for announcement in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })
