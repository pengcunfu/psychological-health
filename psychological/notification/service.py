"""
通知服务核心逻辑
"""
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Union
from sqlalchemy import and_, or_, desc
from sqlalchemy.orm import Session

from pcf_flask_helper.model.base import db
from loguru import logger
from pcf_flask_helper.common import success_result, error_result
from .models import Notification, NotificationTemplate, NotificationConfig
from .types import NotificationType, NotificationPriority, NotificationStatus, NotificationAction
from .config import NotificationConfig as Config, NOTIFICATION_TEMPLATES




class NotificationService:
    """通知服务类"""
    
    def __init__(self, session: Session = None):
        """初始化通知服务"""
        self.session = session or db.session
        self.config = Config()
    
    def create_notification(self, 
                          recipient_id: str,
                          title: str,
                          content: str = None,
                          summary: str = None,
                          notification_type: NotificationType = NotificationType.SYSTEM,
                          priority: NotificationPriority = NotificationPriority.NORMAL,
                          sender_id: str = None,
                          sender_name: str = None,
                          related_id: str = None,
                          related_type: str = None,
                          related_url: str = None,
                          action_type: NotificationAction = NotificationAction.NONE,
                          action_url: str = None,
                          action_data: dict = None,
                          icon: str = None,
                          color: str = None,
                          scheduled_time: datetime = None,
                          expire_time: datetime = None,
                          extra_data: dict = None,
                          is_broadcast: bool = False,
                          is_silent: bool = False) -> Dict:
        """
        创建通知
        
        Args:
            recipient_id: 接收者ID
            title: 通知标题
            content: 通知内容
            summary: 通知摘要
            notification_type: 通知类型
            priority: 优先级
            sender_id: 发送者ID
            sender_name: 发送者名称
            related_id: 关联对象ID
            related_type: 关联对象类型
            related_url: 关联URL
            action_type: 动作类型
            action_url: 动作URL
            action_data: 动作数据
            icon: 图标
            color: 颜色
            scheduled_time: 定时发送时间
            expire_time: 过期时间
            extra_data: 扩展数据
            is_broadcast: 是否广播
            is_silent: 是否静默
        
        Returns:
            Dict: 创建结果
        """
        try:
            # 验证必填参数
            if not recipient_id:
                return error_result("接收者ID不能为空")
            
            if not title:
                return error_result("通知标题不能为空")
            
            # 检查用户通知配置
            user_config = self._get_user_notification_config(recipient_id, notification_type)
            if not user_config.get('in_app_enabled', True):
                logger.info(f"用户 {recipient_id} 已关闭 {notification_type.value} 类型的站内通知")
                return success_result(None, "用户已关闭此类型通知")
            
            # 检查频率限制
            if not self._check_rate_limit(recipient_id, notification_type):
                logger.warning(f"用户 {recipient_id} 的通知频率超出限制")
                return error_result("通知发送频率超出限制")
            
            # 设置默认值
            if not sender_id:
                sender_id = Config.SYSTEM_SENDER['id']
                sender_name = Config.SYSTEM_SENDER['name']
            
            if not icon:
                icon = Config.DEFAULT_ICONS.get(notification_type.value, '📢')
            
            if not color:
                color = Config.DEFAULT_COLORS.get(priority.value, '#3B82F6')
            
            # 创建通知对象
            notification = Notification(
                id=str(uuid.uuid4()),
                title=title,
                content=content,
                summary=summary or title[:100],
                recipient_id=recipient_id,
                sender_id=sender_id,
                sender_name=sender_name,
                type=notification_type,
                priority=priority,
                related_id=related_id,
                related_type=related_type,
                related_url=related_url,
                action_type=action_type,
                action_url=action_url,
                action_data=action_data,
                icon=icon,
                color=color,
                scheduled_time=scheduled_time,
                expire_time=expire_time,
                extra_data=extra_data,
                is_broadcast=is_broadcast,
                is_silent=is_silent
            )
            
            # 保存到数据库
            self.session.add(notification)
            self.session.commit()
            
            logger.info(f"创建通知成功: {notification.id} -> {recipient_id}")
            return success_result(notification.to_dict(), "通知创建成功")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"创建通知失败: {str(e)}")
            return error_result(f"创建通知失败: {str(e)}")
    
    def create_notification_from_template(self,
                                        template_code: str,
                                        recipient_id: str,
                                        variables: dict = None,
                                        **kwargs) -> Dict:
        """
        使用模板创建通知
        
        Args:
            template_code: 模板代码
            recipient_id: 接收者ID
            variables: 模板变量
            **kwargs: 其他参数
            
        Returns:
            Dict: 创建结果
        """
        try:
            # 获取模板
            template = self.session.query(NotificationTemplate).filter_by(
                code=template_code, is_active=True
            ).first()
            
            if not template:
                # 尝试从预定义模板获取
                template_config = NOTIFICATION_TEMPLATES.get(template_code)
                if not template_config:
                    return error_result(f"通知模板不存在: {template_code}")
                
                # 使用预定义模板渲染
                render_data = template_config.copy()
                if variables:
                    from string import Template as StringTemplate
                    for key in ['title_template', 'content_template', 'summary_template', 'action_url_template']:
                        if key in render_data and render_data[key]:
                            render_data[key.replace('_template', '')] = StringTemplate(
                                render_data[key]
                            ).safe_substitute(variables)
                
                # 创建通知
                return self.create_notification(
                    recipient_id=recipient_id,
                    title=render_data.get('title', ''),
                    content=render_data.get('content', ''),
                    summary=render_data.get('summary', ''),
                    notification_type=NotificationType(render_data.get('type', 'system')),
                    action_type=NotificationAction(render_data.get('action_type', 'none')),
                    action_url=render_data.get('action_url', ''),
                    icon=render_data.get('icon', ''),
                    color=render_data.get('color', ''),
                    **kwargs
                )
            
            # 使用数据库模板渲染
            render_data = template.render_notification_data(variables or {})
            
            # 更新使用统计
            template.usage_count += 1
            template.last_used_time = datetime.utcnow()
            
            # 创建通知
            return self.create_notification(
                recipient_id=recipient_id,
                title=render_data.get('title', ''),
                content=render_data.get('content', ''),
                summary=render_data.get('summary', ''),
                notification_type=render_data.get('type', NotificationType.SYSTEM),
                priority=render_data.get('priority', NotificationPriority.NORMAL),
                action_type=render_data.get('action_type', NotificationAction.NONE),
                action_url=render_data.get('action_url', ''),
                icon=render_data.get('icon', ''),
                color=render_data.get('color', ''),
                **kwargs
            )
            
        except Exception as e:
            logger.error(f"使用模板创建通知失败: {str(e)}")
            return error_result(f"使用模板创建通知失败: {str(e)}")
    
    def get_user_notifications(self,
                             user_id: str,
                             status: NotificationStatus = None,
                             notification_type: NotificationType = None,
                             page: int = 1,
                             per_page: int = 20,
                             include_expired: bool = False) -> Dict:
        """
        获取用户通知列表
        
        Args:
            user_id: 用户ID
            status: 通知状态
            notification_type: 通知类型
            page: 页码
            per_page: 每页数量
            include_expired: 是否包含过期通知
            
        Returns:
            Dict: 通知列表
        """
        try:
            # 构建查询条件
            query = self.session.query(Notification).filter(
                Notification.recipient_id == user_id
            )
            
            # 状态过滤
            if status:
                query = query.filter(Notification.status == status)
            else:
                # 默认不包含已删除的通知
                query = query.filter(Notification.status != NotificationStatus.DELETED)
            
            # 类型过滤
            if notification_type:
                query = query.filter(Notification.type == notification_type)
            
            # 过期时间过滤
            if not include_expired:
                query = query.filter(
                    or_(
                        Notification.expire_time.is_(None),
                        Notification.expire_time > datetime.utcnow()
                    )
                )
            
            # 排序：置顶 > 优先级 > 创建时间
            query = query.order_by(
                desc(Notification.is_pinned),
                desc(Notification.priority),
                desc(Notification.create_time)
            )
            
            # 分页
            per_page = min(per_page, Config.MAX_PAGE_SIZE)
            total = query.count()
            
            notifications = query.offset((page - 1) * per_page).limit(per_page).all()
            
            return success_result({
                'notifications': [n.to_dict() for n in notifications],
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': (total + per_page - 1) // per_page,
                'unread_count': self._get_unread_count(user_id)
            })
            
        except Exception as e:
            logger.error(f"获取用户通知失败: {str(e)}")
            return error_result(f"获取用户通知失败: {str(e)}")
    
    def mark_as_read(self, notification_ids: Union[str, List[str]], user_id: str) -> Dict:
        """
        标记通知为已读
        
        Args:
            notification_ids: 通知ID或ID列表
            user_id: 用户ID
            
        Returns:
            Dict: 操作结果
        """
        try:
            if isinstance(notification_ids, str):
                notification_ids = [notification_ids]
            
            # 查询通知
            notifications = self.session.query(Notification).filter(
                and_(
                    Notification.id.in_(notification_ids),
                    Notification.recipient_id == user_id,
                    Notification.status == NotificationStatus.UNREAD
                )
            ).all()
            
            if not notifications:
                return error_result("没有找到可标记的未读通知")
            
            # 批量标记为已读
            updated_count = 0
            for notification in notifications:
                notification.mark_as_read()
                updated_count += 1
            
            self.session.commit()
            
            logger.info(f"用户 {user_id} 标记 {updated_count} 条通知为已读")
            return success_result({
                'updated_count': updated_count,
                'unread_count': self._get_unread_count(user_id)
            }, f"成功标记 {updated_count} 条通知为已读")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"标记通知已读失败: {str(e)}")
            return error_result(f"标记通知已读失败: {str(e)}")
    
    def mark_all_as_read(self, user_id: str, notification_type: NotificationType = None) -> Dict:
        """
        标记所有通知为已读
        
        Args:
            user_id: 用户ID
            notification_type: 通知类型（可选）
            
        Returns:
            Dict: 操作结果
        """
        try:
            # 构建查询条件
            query = self.session.query(Notification).filter(
                and_(
                    Notification.recipient_id == user_id,
                    Notification.status == NotificationStatus.UNREAD
                )
            )
            
            if notification_type:
                query = query.filter(Notification.type == notification_type)
            
            # 获取所有未读通知
            notifications = query.all()
            
            if not notifications:
                return success_result({'updated_count': 0}, "没有未读通知")
            
            # 批量标记为已读
            updated_count = 0
            for notification in notifications:
                notification.mark_as_read()
                updated_count += 1
            
            self.session.commit()
            
            logger.info(f"用户 {user_id} 标记所有通知为已读，共 {updated_count} 条")
            return success_result({
                'updated_count': updated_count,
                'unread_count': 0
            }, f"成功标记 {updated_count} 条通知为已读")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"标记所有通知已读失败: {str(e)}")
            return error_result(f"标记所有通知已读失败: {str(e)}")
    
    def delete_notifications(self, notification_ids: Union[str, List[str]], user_id: str) -> Dict:
        """
        删除通知
        
        Args:
            notification_ids: 通知ID或ID列表
            user_id: 用户ID
            
        Returns:
            Dict: 操作结果
        """
        try:
            if isinstance(notification_ids, str):
                notification_ids = [notification_ids]
            
            # 查询用户的通知
            notifications = self.session.query(Notification).filter(
                and_(
                    Notification.id.in_(notification_ids),
                    Notification.recipient_id == user_id,
                    Notification.status != NotificationStatus.DELETED
                )
            ).all()
            
            if not notifications:
                return error_result("没有找到可删除的通知")
            
            # 标记为删除状态
            deleted_count = 0
            for notification in notifications:
                notification.status = NotificationStatus.DELETED
                deleted_count += 1
            
            self.session.commit()
            
            logger.info(f"用户 {user_id} 删除 {deleted_count} 条通知")
            return success_result({
                'deleted_count': deleted_count
            }, f"成功删除 {deleted_count} 条通知")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"删除通知失败: {str(e)}")
            return error_result(f"删除通知失败: {str(e)}")
    
    def get_unread_count(self, user_id: str) -> Dict:
        """
        获取未读通知数量
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 未读数量统计
        """
        try:
            # 总未读数
            total_unread = self._get_unread_count(user_id)
            
            # 按类型统计未读数
            type_counts = {}
            for notification_type in NotificationType:
                count = self.session.query(Notification).filter(
                    and_(
                        Notification.recipient_id == user_id,
                        Notification.type == notification_type,
                        Notification.status == NotificationStatus.UNREAD,
                        or_(
                            Notification.expire_time.is_(None),
                            Notification.expire_time > datetime.utcnow()
                        )
                    )
                ).count()
                type_counts[notification_type.value] = count
            
            return success_result({
                'total_unread': total_unread,
                'type_counts': type_counts
            })
            
        except Exception as e:
            logger.error(f"获取未读通知数量失败: {str(e)}")
            return error_result(f"获取未读通知数量失败: {str(e)}")
    
    def _get_unread_count(self, user_id: str) -> int:
        """获取用户未读通知总数"""
        return self.session.query(Notification).filter(
            and_(
                Notification.recipient_id == user_id,
                Notification.status == NotificationStatus.UNREAD,
                or_(
                    Notification.expire_time.is_(None),
                    Notification.expire_time > datetime.utcnow()
                )
            )
        ).count()
    
    def _get_user_notification_config(self, user_id: str, notification_type: NotificationType) -> Dict:
        """获取用户通知配置"""
        config = self.session.query(NotificationConfig).filter_by(
            user_id=user_id, type=notification_type
        ).first()
        
        if config:
            return config.to_dict()
        
        # 返回默认配置
        return {
            'in_app_enabled': True,
            'email_enabled': True,
            'sms_enabled': False,
            'push_enabled': True
        }
    
    def _check_rate_limit(self, user_id: str, notification_type: NotificationType) -> bool:
        """检查通知频率限制"""
        # 获取用户配置
        config = self._get_user_notification_config(user_id, notification_type)
        
        # 检查每日限制
        max_daily = config.get('max_daily_count', Config.DEFAULT_MAX_DAILY_NOTIFICATIONS)
        if max_daily:
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            daily_count = self.session.query(Notification).filter(
                and_(
                    Notification.recipient_id == user_id,
                    Notification.type == notification_type,
                    Notification.create_time >= today_start
                )
            ).count()
            
            if daily_count >= max_daily:
                return False
        
        # 检查每小时限制
        max_hourly = config.get('max_hourly_count', Config.DEFAULT_MAX_HOURLY_NOTIFICATIONS)
        if max_hourly:
            hour_ago = datetime.utcnow() - timedelta(hours=1)
            hourly_count = self.session.query(Notification).filter(
                and_(
                    Notification.recipient_id == user_id,
                    Notification.type == notification_type,
                    Notification.create_time >= hour_ago
                )
            ).count()
            
            if hourly_count >= max_hourly:
                return False
        
        return True
    
    def cleanup_old_notifications(self) -> Dict:
        """清理过期和旧通知"""
        try:
            now = datetime.utcnow()
            
            # 清理过期通知
            expired_count = self.session.query(Notification).filter(
                and_(
                    Notification.expire_time.isnot(None),
                    Notification.expire_time < now
                )
            ).delete()
            
            # 清理超过保留期的已读通知
            read_cutoff = now - timedelta(days=Config.READ_NOTIFICATION_RETENTION_DAYS)
            old_read_count = self.session.query(Notification).filter(
                and_(
                    Notification.status == NotificationStatus.READ,
                    Notification.update_time < read_cutoff
                )
            ).delete()
            
            # 清理超过保留期的已删除通知
            deleted_cutoff = now - timedelta(days=Config.NOTIFICATION_RETENTION_DAYS)
            old_deleted_count = self.session.query(Notification).filter(
                and_(
                    Notification.status == NotificationStatus.DELETED,
                    Notification.update_time < deleted_cutoff
                )
            ).delete()
            
            self.session.commit()
            
            total_cleaned = expired_count + old_read_count + old_deleted_count
            logger.info(f"清理通知完成: 过期 {expired_count}, 旧已读 {old_read_count}, 旧已删除 {old_deleted_count}")
            
            return success_result({
                'expired_count': expired_count,
                'old_read_count': old_read_count,
                'old_deleted_count': old_deleted_count,
                'total_cleaned': total_cleaned
            }, f"清理完成，共清理 {total_cleaned} 条通知")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"清理通知失败: {str(e)}")
            return error_result(f"清理通知失败: {str(e)}")


# 创建全局服务实例
notification_service = NotificationService()
