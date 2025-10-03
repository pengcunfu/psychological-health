"""
通知触发器 - 业务事件通知集成
在各种业务操作中自动触发相应的通知
"""
from datetime import datetime, timedelta
from typing import Dict, Optional

from loguru import logger
from .service import notification_service
from .types import NotificationType, NotificationPriority




class NotificationTriggers:
    """通知触发器类"""
    
    @staticmethod
    def on_appointment_confirmed(appointment_id: str, user_id: str, appointment_time: str, 
                               counselor_name: str, location: str = None) -> Dict:
        """预约确认通知"""
        try:
            variables = {
                'appointment_id': appointment_id,
                'appointment_time': appointment_time,
                'counselor_name': counselor_name,
                'location': location or '线上咨询'
            }
            
            return notification_service.create_notification_from_template(
                template_code='appointment_confirmed',
                recipient_id=user_id,
                variables=variables,
                priority=NotificationPriority.HIGH,
                related_id=appointment_id,
                related_type='appointment'
            )
            
        except Exception as e:
            logger.error(f"发送预约确认通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_appointment_cancelled(appointment_id: str, user_id: str, appointment_time: str,
                               counselor_name: str, cancel_reason: str = None) -> Dict:
        """预约取消通知"""
        try:
            variables = {
                'appointment_id': appointment_id,
                'appointment_time': appointment_time,
                'counselor_name': counselor_name,
                'cancel_reason': cancel_reason or '未说明原因'
            }
            
            return notification_service.create_notification_from_template(
                template_code='appointment_cancelled',
                recipient_id=user_id,
                variables=variables,
                priority=NotificationPriority.HIGH,
                related_id=appointment_id,
                related_type='appointment'
            )
            
        except Exception as e:
            logger.error(f"发送预约取消通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_appointment_reminder(appointment_id: str, user_id: str, appointment_time: str,
                              counselor_name: str, location: str = None, 
                              reminder_minutes: int = 60) -> Dict:
        """预约提醒通知"""
        try:
            # 计算提醒时间
            appointment_dt = datetime.fromisoformat(appointment_time.replace('Z', '+00:00'))
            reminder_time = appointment_dt - timedelta(minutes=reminder_minutes)
            
            variables = {
                'appointment_id': appointment_id,
                'appointment_time': appointment_time,
                'counselor_name': counselor_name,
                'location': location or '线上咨询',
                'reminder_time': f"{reminder_minutes}分钟"
            }
            
            return notification_service.create_notification_from_template(
                template_code='appointment_reminder',
                recipient_id=user_id,
                variables=variables,
                priority=NotificationPriority.HIGH,
                scheduled_time=reminder_time,
                related_id=appointment_id,
                related_type='appointment'
            )
            
        except Exception as e:
            logger.error(f"创建预约提醒通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_order_paid(order_id: str, user_id: str, order_number: str, 
                     product_name: str, amount: float) -> Dict:
        """订单支付成功通知"""
        try:
            variables = {
                'order_id': order_id,
                'order_number': order_number,
                'product_name': product_name,
                'amount': f"{amount:.2f}"
            }
            
            return notification_service.create_notification_from_template(
                template_code='order_paid',
                recipient_id=user_id,
                variables=variables,
                priority=NotificationPriority.HIGH,
                related_id=order_id,
                related_type='order'
            )
            
        except Exception as e:
            logger.error(f"发送订单支付通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_order_refunded(order_id: str, user_id: str, order_number: str, 
                         refund_amount: float) -> Dict:
        """订单退款通知"""
        try:
            variables = {
                'order_id': order_id,
                'order_number': order_number,
                'refund_amount': f"{refund_amount:.2f}"
            }
            
            return notification_service.create_notification_from_template(
                template_code='order_refunded',
                recipient_id=user_id,
                variables=variables,
                priority=NotificationPriority.NORMAL,
                related_id=order_id,
                related_type='order'
            )
            
        except Exception as e:
            logger.error(f"发送订单退款通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_course_subscribed(course_id: str, user_id: str, course_name: str, 
                           instructor_name: str) -> Dict:
        """课程订阅成功通知"""
        try:
            variables = {
                'course_id': course_id,
                'course_name': course_name,
                'instructor_name': instructor_name
            }
            
            return notification_service.create_notification_from_template(
                template_code='course_subscribed',
                recipient_id=user_id,
                variables=variables,
                priority=NotificationPriority.NORMAL,
                related_id=course_id,
                related_type='course'
            )
            
        except Exception as e:
            logger.error(f"发送课程订阅通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_course_completed(course_id: str, user_id: str, course_name: str, 
                          study_duration: str) -> Dict:
        """课程完成通知"""
        try:
            variables = {
                'course_id': course_id,
                'course_name': course_name,
                'study_duration': study_duration
            }
            
            return notification_service.create_notification_from_template(
                template_code='course_completed',
                recipient_id=user_id,
                variables=variables,
                priority=NotificationPriority.NORMAL,
                related_id=course_id,
                related_type='course'
            )
            
        except Exception as e:
            logger.error(f"发送课程完成通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_assessment_completed(record_id: str, user_id: str, assessment_name: str, 
                              completion_time: str) -> Dict:
        """测评完成通知"""
        try:
            variables = {
                'record_id': record_id,
                'assessment_name': assessment_name,
                'completion_time': completion_time
            }
            
            return notification_service.create_notification_from_template(
                template_code='assessment_completed',
                recipient_id=user_id,
                variables=variables,
                priority=NotificationPriority.NORMAL,
                related_id=record_id,
                related_type='assessment'
            )
            
        except Exception as e:
            logger.error(f"发送测评完成通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_user_followed(follower_id: str, following_id: str, follower_name: str) -> Dict:
        """用户关注通知"""
        try:
            variables = {
                'follower_id': follower_id,
                'follower_name': follower_name
            }
            
            return notification_service.create_notification_from_template(
                template_code='social_followed',
                recipient_id=following_id,
                variables=variables,
                priority=NotificationPriority.LOW,
                related_id=follower_id,
                related_type='user'
            )
            
        except Exception as e:
            logger.error(f"发送关注通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_content_liked(content_id: str, content_type: str, content_preview: str,
                        liker_id: str, liker_name: str, author_id: str) -> Dict:
        """内容被点赞通知"""
        try:
            if liker_id == author_id:
                # 自己点赞自己的内容，不发通知
                return {'code': 200, 'message': '跳过自己点赞的通知'}
            
            variables = {
                'content_id': content_id,
                'content_type': content_type,
                'content_preview': content_preview[:50] + '...' if len(content_preview) > 50 else content_preview,
                'liker_id': liker_id,
                'liker_name': liker_name
            }
            
            return notification_service.create_notification_from_template(
                template_code='social_liked',
                recipient_id=author_id,
                variables=variables,
                priority=NotificationPriority.LOW,
                related_id=content_id,
                related_type=content_type
            )
            
        except Exception as e:
            logger.error(f"发送点赞通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_content_commented(content_id: str, content_type: str, comment_id: str,
                           comment_content: str, commenter_id: str, commenter_name: str, 
                           author_id: str) -> Dict:
        """内容被评论通知"""
        try:
            if commenter_id == author_id:
                # 自己评论自己的内容，不发通知
                return {'code': 200, 'message': '跳过自己评论的通知'}
            
            variables = {
                'content_id': content_id,
                'content_type': content_type,
                'comment_id': comment_id,
                'comment_content': comment_content[:100] + '...' if len(comment_content) > 100 else comment_content,
                'commenter_id': commenter_id,
                'commenter_name': commenter_name
            }
            
            return notification_service.create_notification_from_template(
                template_code='social_commented',
                recipient_id=author_id,
                variables=variables,
                priority=NotificationPriority.LOW,
                related_id=content_id,
                related_type=content_type
            )
            
        except Exception as e:
            logger.error(f"发送评论通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_system_announcement(title: str, content: str, summary: str = None,
                             user_ids: list = None, is_broadcast: bool = True) -> Dict:
        """系统公告通知"""
        try:
            if is_broadcast and user_ids:
                # 批量发送
                from .manager import notification_manager
                return notification_manager.broadcast_notification(
                    user_ids=user_ids,
                    template_code='system_announcement',
                    variables={
                        'announcement_title': title,
                        'announcement_content': content,
                        'announcement_summary': summary or title[:100]
                    },
                    priority=NotificationPriority.HIGH
                )
            else:
                # 单个发送（需要指定用户）
                if not user_ids or len(user_ids) != 1:
                    return {'code': 400, 'message': '非广播模式需要指定单个用户ID'}
                
                return notification_service.create_notification_from_template(
                    template_code='system_announcement',
                    recipient_id=user_ids[0],
                    variables={
                        'announcement_title': title,
                        'announcement_content': content,
                        'announcement_summary': summary or title[:100]
                    },
                    priority=NotificationPriority.HIGH
                )
                
        except Exception as e:
            logger.error(f"发送系统公告失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_security_login(user_id: str, login_time: str, login_location: str, 
                         device_info: str) -> Dict:
        """异地登录安全通知"""
        try:
            variables = {
                'login_time': login_time,
                'login_location': login_location,
                'device_info': device_info
            }
            
            return notification_service.create_notification_from_template(
                template_code='security_login',
                recipient_id=user_id,
                variables=variables,
                priority=NotificationPriority.URGENT,
                related_type='security'
            )
            
        except Exception as e:
            logger.error(f"发送安全登录通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}
    
    @staticmethod
    def on_password_changed(user_id: str, change_time: str) -> Dict:
        """密码修改通知"""
        try:
            variables = {
                'change_time': change_time
            }
            
            return notification_service.create_notification_from_template(
                template_code='security_password_changed',
                recipient_id=user_id,
                variables=variables,
                priority=NotificationPriority.HIGH,
                related_type='security'
            )
            
        except Exception as e:
            logger.error(f"发送密码修改通知失败: {str(e)}")
            return {'code': 500, 'message': str(e)}


# 创建全局触发器实例
notification_triggers = NotificationTriggers()
