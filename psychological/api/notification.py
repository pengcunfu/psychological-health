"""
通知管理API
提供站内通知的完整功能接口
"""
from datetime import datetime
from flask import Blueprint, request
from psychological.models.base import db
from psychological.utils.json_result import JsonResult
from psychological.utils.auth_helper import assert_current_user_id, is_manager_user
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required
from psychological.form.notification import (
    NotificationQueryForm, NotificationCreateForm, NotificationBulkCreateForm,
    NotificationUpdateForm, NotificationMarkReadForm, NotificationConfigForm,
    NotificationTemplateCreateForm, NotificationStatsForm
)
from psychological.notify.service import notification_service
from psychological.notify.manager import notification_manager
from psychological.notify.models import Notification, NotificationTemplate
from psychological.notify.types import NotificationType, NotificationPriority, NotificationStatus

notification_bp = Blueprint('notification', __name__, url_prefix='/notification')


@notification_bp.route('', methods=['GET'])
@validate_form(NotificationQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("notification:get_notifications")
def get_notifications(form):
    """获取用户通知列表"""
    try:
        user_id = assert_current_user_id()
        
        result = notification_service.get_user_notifications(
            user_id=user_id,
            status=NotificationStatus(form.status.data) if form.status.data else None,
            notification_type=NotificationType(form.type.data) if form.type.data else None,
            page=form.page.data,
            per_page=form.per_page.data,
            include_expired=form.include_expired.data
        )
        
        return JsonResult.success(result['data'], result['message'])
        
    except Exception as e:
        return JsonResult.error(f"获取通知列表失败: {str(e)}")


@notification_bp.route('/unread-count', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
def get_unread_count():
    """获取未读通知数量"""
    try:
        user_id = assert_current_user_id()
        
        result = notification_service.get_unread_count(user_id)
        
        if result['code'] == 200:
            return JsonResult.success(result['data'])
        else:
            return JsonResult.error(result['message'])
            
    except Exception as e:
        return JsonResult.error(f"获取未读数量失败: {str(e)}")


@notification_bp.route('/<notification_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("notification:get_notification")
def get_notification(notification_id):
    """获取单个通知详情"""
    try:
        user_id = assert_current_user_id()
        
        notification = db.session.query(Notification).filter_by(
            id=notification_id, recipient_id=user_id
        ).first()
        
        if not notification:
            return JsonResult.error("通知不存在")
        
        if not notification.is_readable():
            return JsonResult.error("通知已过期或已删除")
        
        return JsonResult.success(notification.to_dict())
        
    except Exception as e:
        return JsonResult.error(f"获取通知详情失败: {str(e)}")


@notification_bp.route('', methods=['POST'])
@validate_form(NotificationCreateForm)
@role_required(['admin', 'manager'])
@permission_required("notification:create_notification")
def create_notification(form):
    """创建通知（管理员功能）"""
    try:
        # 使用模板创建
        if form.template_code.data:
            result = notification_service.create_notification_from_template(
                template_code=form.template_code.data,
                recipient_id=form.recipient_id.data,
                variables=form.variables.data or {},
                sender_id=assert_current_user_id(),
                priority=NotificationPriority(form.priority.data) if form.priority.data else None,
                scheduled_time=form.scheduled_time.data,
                expire_time=form.expire_time.data
            )
        else:
            # 直接创建
            result = notification_service.create_notification(
                recipient_id=form.recipient_id.data,
                title=form.title.data,
                content=form.content.data,
                summary=form.summary.data,
                notification_type=NotificationType(form.type.data),
                priority=NotificationPriority(form.priority.data) if form.priority.data else NotificationPriority.NORMAL,
                sender_id=assert_current_user_id(),
                related_id=form.related_id.data,
                related_type=form.related_type.data,
                action_url=form.action_url.data,
                scheduled_time=form.scheduled_time.data,
                expire_time=form.expire_time.data
            )
        
        if result['code'] == 200:
            return JsonResult.success(result['data'], result['message'])
        else:
            return JsonResult.error(result['message'])
            
    except Exception as e:
        return JsonResult.error(f"创建通知失败: {str(e)}")


@notification_bp.route('/bulk', methods=['POST'])
@validate_form(NotificationBulkCreateForm)
@role_required(['admin', 'manager'])
@permission_required("notification:bulk_create_notification")
def bulk_create_notification(form):
    """批量创建通知"""
    try:
        result = notification_manager.broadcast_notification(
            user_ids=form.user_ids.data,
            title=form.title.data,
            content=form.content.data,
            template_code=form.template_code.data,
            variables=form.variables.data or {},
            notification_type=NotificationType(form.type.data),
            priority=NotificationPriority(form.priority.data) if form.priority.data else NotificationPriority.NORMAL,
            sender_id=assert_current_user_id(),
            scheduled_time=form.scheduled_time.data,
            expire_time=form.expire_time.data
        )
        
        if result['code'] == 200:
            return JsonResult.success(result['data'], result['message'])
        else:
            return JsonResult.error(result['message'])
            
    except Exception as e:
        return JsonResult.error(f"批量创建通知失败: {str(e)}")


@notification_bp.route('/mark-read', methods=['POST'])
@validate_form(NotificationMarkReadForm)
@role_required(['admin', 'manager', 'user'])
def mark_notifications_read(form):
    """标记通知为已读"""
    try:
        user_id = assert_current_user_id()
        
        if form.notification_ids.data:
            # 标记指定通知
            result = notification_service.mark_as_read(
                notification_ids=form.notification_ids.data,
                user_id=user_id
            )
        else:
            # 标记所有通知
            result = notification_service.mark_all_as_read(
                user_id=user_id,
                notification_type=NotificationType(form.type.data) if form.type.data else None
            )
        
        if result['code'] == 200:
            return JsonResult.success(result['data'], result['message'])
        else:
            return JsonResult.error(result['message'])
            
    except Exception as e:
        return JsonResult.error(f"标记已读失败: {str(e)}")


@notification_bp.route('/delete', methods=['POST'])
@validate_form(NotificationMarkReadForm)  # 复用同样的表单
@role_required(['admin', 'manager', 'user'])
def delete_notifications(form):
    """删除通知"""
    try:
        user_id = assert_current_user_id()
        
        if not form.notification_ids.data:
            return JsonResult.error("请指定要删除的通知ID")
        
        result = notification_service.delete_notifications(
            notification_ids=form.notification_ids.data,
            user_id=user_id
        )
        
        if result['code'] == 200:
            return JsonResult.success(result['data'], result['message'])
        else:
            return JsonResult.error(result['message'])
            
    except Exception as e:
        return JsonResult.error(f"删除通知失败: {str(e)}")


@notification_bp.route('/config', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
def get_notification_config():
    """获取用户通知配置"""
    try:
        user_id = assert_current_user_id()
        
        result = notification_manager.get_user_notification_config(user_id)
        
        if result['code'] == 200:
            return JsonResult.success(result['data'])
        else:
            return JsonResult.error(result['message'])
            
    except Exception as e:
        return JsonResult.error(f"获取通知配置失败: {str(e)}")


@notification_bp.route('/config', methods=['POST'])
@validate_form(NotificationConfigForm)
@role_required(['admin', 'manager', 'user'])
def update_notification_config(form):
    """更新用户通知配置"""
    try:
        user_id = assert_current_user_id()
        
        result = notification_manager.update_user_notification_config(
            user_id=user_id,
            notification_type=NotificationType(form.type.data),
            config_data={
                'in_app_enabled': form.in_app_enabled.data,
                'email_enabled': form.email_enabled.data,
                'sms_enabled': form.sms_enabled.data,
                'push_enabled': form.push_enabled.data,
                'quiet_start_time': form.quiet_start_time.data,
                'quiet_end_time': form.quiet_end_time.data,
                'max_daily_count': form.max_daily_count.data,
                'max_hourly_count': form.max_hourly_count.data,
                'min_priority': form.min_priority.data
            }
        )
        
        if result['code'] == 200:
            return JsonResult.success(result['data'], result['message'])
        else:
            return JsonResult.error(result['message'])
            
    except Exception as e:
        return JsonResult.error(f"更新通知配置失败: {str(e)}")


@notification_bp.route('/templates', methods=['GET'])
@role_required(['admin', 'manager'])
@permission_required("notification:get_templates")
def get_notification_templates():
    """获取通知模板列表"""
    try:
        templates = db.session.query(NotificationTemplate).filter_by(
            is_active=True
        ).order_by(NotificationTemplate.create_time.desc()).all()
        
        return JsonResult.success({
            'templates': [template.to_dict() for template in templates]
        })
        
    except Exception as e:
        return JsonResult.error(f"获取模板列表失败: {str(e)}")


@notification_bp.route('/templates', methods=['POST'])
@validate_form(NotificationTemplateCreateForm)
@role_required(['admin', 'manager'])
@permission_required("notification:create_template")
def create_notification_template(form):
    """创建通知模板"""
    try:
        result = notification_manager.create_notification_template(
            name=form.name.data,
            code=form.code.data,
            notification_type=NotificationType(form.type.data),
            title_template=form.title_template.data,
            content_template=form.content_template.data,
            summary_template=form.summary_template.data,
            description=form.description.data,
            priority=NotificationPriority(form.priority.data) if form.priority.data else NotificationPriority.NORMAL,
            icon=form.icon.data,
            color=form.color.data,
            variables=form.variables.data
        )
        
        if result['code'] == 200:
            return JsonResult.success(result['data'], result['message'])
        else:
            return JsonResult.error(result['message'])
            
    except Exception as e:
        return JsonResult.error(f"创建模板失败: {str(e)}")


@notification_bp.route('/stats', methods=['GET'])
@validate_form(NotificationStatsForm)
@role_required(['admin', 'manager'])
@permission_required("notification:get_stats")
def get_notification_stats(form):
    """获取通知统计信息"""
    try:
        user_id = form.user_id.data if is_manager_user() else assert_current_user_id()
        
        result = notification_manager.get_notification_statistics(
            user_id=user_id,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        
        if result['code'] == 200:
            return JsonResult.success(result['data'])
        else:
            return JsonResult.error(result['message'])
            
    except Exception as e:
        return JsonResult.error(f"获取统计信息失败: {str(e)}")


@notification_bp.route('/cleanup', methods=['POST'])
@role_required(['admin'])
@permission_required("notification:cleanup")
def cleanup_notifications():
    """清理过期通知（管理员功能）"""
    try:
        result = notification_service.cleanup_old_notifications()
        
        if result['code'] == 200:
            return JsonResult.success(result['data'], result['message'])
        else:
            return JsonResult.error(result['message'])
            
    except Exception as e:
        return JsonResult.error(f"清理通知失败: {str(e)}")


@notification_bp.route('/process-scheduled', methods=['POST'])
@role_required(['admin'])
@permission_required("notification:process_scheduled")
def process_scheduled_notifications():
    """处理定时通知（管理员功能）"""
    try:
        result = notification_manager.process_scheduled_notifications()
        
        if result['code'] == 200:
            return JsonResult.success(result['data'], result['message'])
        else:
            return JsonResult.error(result['message'])
            
    except Exception as e:
        return JsonResult.error(f"处理定时通知失败: {str(e)}")
