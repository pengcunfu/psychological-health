"""
通知管理器 - 高级通知功能
提供批量通知、定时通知、通知统计等功能
"""
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
from sqlalchemy import and_, or_, func, desc

from ..models.base import db
from ..utils.logger_client import get_logger
from ..utils.json_result import success_result, error_result
from .models import Notification, NotificationTemplate, NotificationConfig
from .service import NotificationService
from .types import NotificationType, NotificationPriority, NotificationStatus
from .config import NotificationConfig as Config

logger = get_logger(__name__)


class NotificationManager:
    """通知管理器"""
    
    def __init__(self):
        """初始化通知管理器"""
        self.service = NotificationService()
        self.session = db.session
    
    def broadcast_notification(self,
                             user_ids: List[str],
                             title: str,
                             content: str = None,
                             template_code: str = None,
                             variables: dict = None,
                             **kwargs) -> Dict:
        """
        批量发送通知
        
        Args:
            user_ids: 用户ID列表
            title: 通知标题
            content: 通知内容
            template_code: 模板代码
            variables: 模板变量
            **kwargs: 其他参数
            
        Returns:
            Dict: 发送结果
        """
        try:
            if not user_ids:
                return error_result("用户列表不能为空")
            
            if len(user_ids) > Config.MAX_BATCH_SIZE:
                return error_result(f"批量发送数量不能超过 {Config.MAX_BATCH_SIZE}")
            
            success_count = 0
            failed_count = 0
            failed_users = []
            
            for user_id in user_ids:
                try:
                    if template_code:
                        result = self.service.create_notification_from_template(
                            template_code=template_code,
                            recipient_id=user_id,
                            variables=variables,
                            **kwargs
                        )
                    else:
                        result = self.service.create_notification(
                            recipient_id=user_id,
                            title=title,
                            content=content,
                            is_broadcast=True,
                            **kwargs
                        )
                    
                    if result['code'] == 200:
                        success_count += 1
                    else:
                        failed_count += 1
                        failed_users.append({
                            'user_id': user_id,
                            'error': result['message']
                        })
                        
                except Exception as e:
                    failed_count += 1
                    failed_users.append({
                        'user_id': user_id,
                        'error': str(e)
                    })
            
            logger.info(f"批量发送通知完成: 成功 {success_count}, 失败 {failed_count}")
            
            return success_result({
                'total_count': len(user_ids),
                'success_count': success_count,
                'failed_count': failed_count,
                'failed_users': failed_users
            }, f"批量发送完成，成功 {success_count} 条，失败 {failed_count} 条")
            
        except Exception as e:
            logger.error(f"批量发送通知失败: {str(e)}")
            return error_result(f"批量发送通知失败: {str(e)}")
    
    def schedule_notification(self,
                            recipient_id: str,
                            scheduled_time: datetime,
                            title: str,
                            content: str = None,
                            template_code: str = None,
                            variables: dict = None,
                            **kwargs) -> Dict:
        """
        定时发送通知
        
        Args:
            recipient_id: 接收者ID
            scheduled_time: 定时发送时间
            title: 通知标题
            content: 通知内容
            template_code: 模板代码
            variables: 模板变量
            **kwargs: 其他参数
            
        Returns:
            Dict: 创建结果
        """
        try:
            if scheduled_time <= datetime.utcnow():
                return error_result("定时时间必须晚于当前时间")
            
            if template_code:
                result = self.service.create_notification_from_template(
                    template_code=template_code,
                    recipient_id=recipient_id,
                    variables=variables,
                    scheduled_time=scheduled_time,
                    **kwargs
                )
            else:
                result = self.service.create_notification(
                    recipient_id=recipient_id,
                    title=title,
                    content=content,
                    scheduled_time=scheduled_time,
                    **kwargs
                )
            
            if result['code'] == 200:
                logger.info(f"定时通知创建成功: {result['data']['id']}, 发送时间: {scheduled_time}")
            
            return result
            
        except Exception as e:
            logger.error(f"创建定时通知失败: {str(e)}")
            return error_result(f"创建定时通知失败: {str(e)}")
    
    def process_scheduled_notifications(self) -> Dict:
        """
        处理定时通知
        
        Returns:
            Dict: 处理结果
        """
        try:
            now = datetime.utcnow()
            
            # 查询需要发送的定时通知
            scheduled_notifications = self.session.query(Notification).filter(
                and_(
                    Notification.scheduled_time.isnot(None),
                    Notification.scheduled_time <= now,
                    Notification.status == NotificationStatus.UNREAD
                )
            ).all()
            
            if not scheduled_notifications:
                return success_result({'processed_count': 0}, "没有需要处理的定时通知")
            
            processed_count = 0
            for notification in scheduled_notifications:
                try:
                    # 清除定时标记，使通知立即可见
                    notification.scheduled_time = None
                    processed_count += 1
                    
                except Exception as e:
                    logger.error(f"处理定时通知 {notification.id} 失败: {str(e)}")
            
            self.session.commit()
            
            logger.info(f"处理定时通知完成: {processed_count} 条")
            return success_result({
                'processed_count': processed_count
            }, f"成功处理 {processed_count} 条定时通知")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"处理定时通知失败: {str(e)}")
            return error_result(f"处理定时通知失败: {str(e)}")
    
    def get_notification_statistics(self, 
                                  user_id: str = None,
                                  start_date: datetime = None,
                                  end_date: datetime = None) -> Dict:
        """
        获取通知统计信息
        
        Args:
            user_id: 用户ID（可选）
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            Dict: 统计信息
        """
        try:
            # 设置默认时间范围（最近30天）
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = end_date - timedelta(days=30)
            
            # 构建基础查询
            query = self.session.query(Notification).filter(
                and_(
                    Notification.create_time >= start_date,
                    Notification.create_time <= end_date
                )
            )
            
            if user_id:
                query = query.filter(Notification.recipient_id == user_id)
            
            # 总数统计
            total_count = query.count()
            unread_count = query.filter(Notification.status == NotificationStatus.UNREAD).count()
            read_count = query.filter(Notification.status == NotificationStatus.READ).count()
            
            # 按类型统计
            type_stats = {}
            for notification_type in NotificationType:
                count = query.filter(Notification.type == notification_type).count()
                type_stats[notification_type.value] = count
            
            # 按优先级统计
            priority_stats = {}
            for priority in NotificationPriority:
                count = query.filter(Notification.priority == priority).count()
                priority_stats[priority.value] = count
            
            # 按日期统计（最近7天）
            daily_stats = []
            for i in range(7):
                date = (end_date - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
                next_date = date + timedelta(days=1)
                
                daily_count = query.filter(
                    and_(
                        Notification.create_time >= date,
                        Notification.create_time < next_date
                    )
                ).count()
                
                daily_stats.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'count': daily_count
                })
            
            daily_stats.reverse()  # 按时间正序
            
            # 热门通知类型（点击率高的）
            popular_types = self.session.query(
                Notification.type,
                func.count(Notification.id).label('total'),
                func.count(Notification.read_time).label('read')
            ).filter(
                and_(
                    Notification.create_time >= start_date,
                    Notification.create_time <= end_date
                )
            ).group_by(Notification.type).all()
            
            popular_stats = []
            for type_name, total, read in popular_types:
                if total > 0:
                    read_rate = (read / total) * 100
                    popular_stats.append({
                        'type': type_name.value,
                        'total': total,
                        'read': read,
                        'read_rate': round(read_rate, 2)
                    })
            
            popular_stats.sort(key=lambda x: x['read_rate'], reverse=True)
            
            return success_result({
                'summary': {
                    'total_count': total_count,
                    'unread_count': unread_count,
                    'read_count': read_count,
                    'read_rate': round((read_count / total_count * 100) if total_count > 0 else 0, 2)
                },
                'type_stats': type_stats,
                'priority_stats': priority_stats,
                'daily_stats': daily_stats,
                'popular_types': popular_stats,
                'period': {
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d')
                }
            })
            
        except Exception as e:
            logger.error(f"获取通知统计失败: {str(e)}")
            return error_result(f"获取通知统计失败: {str(e)}")
    
    def create_notification_template(self,
                                   name: str,
                                   code: str,
                                   notification_type: NotificationType,
                                   title_template: str,
                                   content_template: str = None,
                                   summary_template: str = None,
                                   description: str = None,
                                   **kwargs) -> Dict:
        """
        创建通知模板
        
        Args:
            name: 模板名称
            code: 模板代码
            notification_type: 通知类型
            title_template: 标题模板
            content_template: 内容模板
            summary_template: 摘要模板
            description: 模板描述
            **kwargs: 其他参数
            
        Returns:
            Dict: 创建结果
        """
        try:
            # 检查模板代码是否已存在
            existing = self.session.query(NotificationTemplate).filter_by(code=code).first()
            if existing:
                return error_result(f"模板代码 '{code}' 已存在")
            
            # 创建模板
            template = NotificationTemplate(
                id=str(uuid.uuid4()),
                name=name,
                code=code,
                type=notification_type,
                title_template=title_template,
                content_template=content_template,
                summary_template=summary_template,
                description=description,
                **kwargs
            )
            
            self.session.add(template)
            self.session.commit()
            
            logger.info(f"创建通知模板成功: {template.code}")
            return success_result(template.to_dict(), "模板创建成功")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"创建通知模板失败: {str(e)}")
            return error_result(f"创建通知模板失败: {str(e)}")
    
    def update_user_notification_config(self,
                                      user_id: str,
                                      notification_type: NotificationType,
                                      config_data: dict) -> Dict:
        """
        更新用户通知配置
        
        Args:
            user_id: 用户ID
            notification_type: 通知类型
            config_data: 配置数据
            
        Returns:
            Dict: 更新结果
        """
        try:
            # 查找现有配置
            config = self.session.query(NotificationConfig).filter_by(
                user_id=user_id,
                type=notification_type
            ).first()
            
            if not config:
                # 创建新配置
                config = NotificationConfig(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    type=notification_type
                )
                self.session.add(config)
            
            # 更新配置字段
            for key, value in config_data.items():
                if hasattr(config, key):
                    setattr(config, key, value)
            
            self.session.commit()
            
            logger.info(f"更新用户 {user_id} 的 {notification_type.value} 通知配置")
            return success_result(config.to_dict(), "配置更新成功")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"更新用户通知配置失败: {str(e)}")
            return error_result(f"更新用户通知配置失败: {str(e)}")
    
    def get_user_notification_config(self, user_id: str) -> Dict:
        """
        获取用户通知配置
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 用户配置
        """
        try:
            configs = self.session.query(NotificationConfig).filter_by(
                user_id=user_id
            ).all()
            
            config_dict = {}
            for config in configs:
                config_dict[config.type.value] = config.to_dict()
            
            # 补充缺失的默认配置
            for notification_type in NotificationType:
                if notification_type.value not in config_dict:
                    config_dict[notification_type.value] = {
                        'type': notification_type.value,
                        'in_app_enabled': True,
                        'email_enabled': True,
                        'sms_enabled': False,
                        'push_enabled': True,
                        'min_priority': 'low'
                    }
            
            return success_result(config_dict)
            
        except Exception as e:
            logger.error(f"获取用户通知配置失败: {str(e)}")
            return error_result(f"获取用户通知配置失败: {str(e)}")


# 创建全局管理器实例
notification_manager = NotificationManager()
