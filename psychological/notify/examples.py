"""
通知系统使用示例
展示如何在业务代码中集成和使用通知功能
"""
from datetime import datetime, timedelta

from .service import notification_service
from .manager import notification_manager
from .triggers import notification_triggers
from .types import NotificationType, NotificationPriority


class NotificationExamples:
    """通知系统使用示例类"""
    
    @staticmethod
    def example_appointment_workflow():
        """预约流程通知示例"""
        print("=== 预约流程通知示例 ===")
        
        # 模拟预约数据
        user_id = "user123"
        appointment_id = "appt456"
        appointment_time = "2024-01-15 14:30:00"
        counselor_name = "张医生"
        location = "心理咨询室A"
        
        # 1. 预约确认通知
        result = notification_triggers.on_appointment_confirmed(
            appointment_id=appointment_id,
            user_id=user_id,
            appointment_time=appointment_time,
            counselor_name=counselor_name,
            location=location
        )
        print(f"预约确认通知: {result}")
        
        # 2. 设置预约提醒（提前1小时）
        result = notification_triggers.on_appointment_reminder(
            appointment_id=appointment_id,
            user_id=user_id,
            appointment_time=appointment_time,
            counselor_name=counselor_name,
            location=location,
            reminder_minutes=60
        )
        print(f"预约提醒设置: {result}")
        
        # 3. 如果需要取消预约
        cancel_reason = "咨询师临时有事"
        result = notification_triggers.on_appointment_cancelled(
            appointment_id=appointment_id,
            user_id=user_id,
            appointment_time=appointment_time,
            counselor_name=counselor_name,
            cancel_reason=cancel_reason
        )
        print(f"取消预约通知: {result}")
    
    @staticmethod
    def example_order_workflow():
        """订单流程通知示例"""
        print("\n=== 订单流程通知示例 ===")
        
        # 模拟订单数据
        user_id = "user123"
        order_id = "order789"
        order_number = "ORD202401150001"
        product_name = "心理健康评估课程"
        amount = 199.00
        
        # 1. 订单支付成功通知
        result = notification_triggers.on_order_paid(
            order_id=order_id,
            user_id=user_id,
            order_number=order_number,
            product_name=product_name,
            amount=amount
        )
        print(f"支付成功通知: {result}")
        
        # 2. 如果需要退款
        refund_amount = 199.00
        result = notification_triggers.on_order_refunded(
            order_id=order_id,
            user_id=user_id,
            order_number=order_number,
            refund_amount=refund_amount
        )
        print(f"退款通知: {result}")
    
    @staticmethod
    def example_social_notifications():
        """社交互动通知示例"""
        print("\n=== 社交互动通知示例 ===")
        
        # 模拟用户数据
        user_a = "user123"  # 内容作者
        user_b = "user456"  # 互动用户
        user_b_name = "李小明"
        
        # 1. 关注通知
        result = notification_triggers.on_user_followed(
            follower_id=user_b,
            following_id=user_a,
            follower_name=user_b_name
        )
        print(f"关注通知: {result}")
        
        # 2. 点赞通知
        result = notification_triggers.on_content_liked(
            content_id="post123",
            content_type="帖子",
            content_preview="分享我的心理健康体验...",
            liker_id=user_b,
            liker_name=user_b_name,
            author_id=user_a
        )
        print(f"点赞通知: {result}")
        
        # 3. 评论通知
        result = notification_triggers.on_content_commented(
            content_id="post123",
            content_type="帖子",
            comment_id="comment789",
            comment_content="很有帮助的分享，谢谢！",
            commenter_id=user_b,
            commenter_name=user_b_name,
            author_id=user_a
        )
        print(f"评论通知: {result}")
    
    @staticmethod
    def example_system_notifications():
        """系统通知示例"""
        print("\n=== 系统通知示例 ===")
        
        # 1. 系统公告（广播通知）
        user_ids = ["user123", "user456", "user789"]
        result = notification_triggers.on_system_announcement(
            title="系统维护通知",
            content="系统将于今晚23:00进行维护升级，预计持续2小时。",
            summary="今晚23:00系统维护",
            user_ids=user_ids,
            is_broadcast=True
        )
        print(f"系统公告: {result}")
        
        # 2. 安全登录通知
        result = notification_triggers.on_security_login(
            user_id="user123",
            login_time="2024-01-15 08:30:00",
            login_location="北京市",
            device_info="iPhone 15 Pro"
        )
        print(f"安全登录通知: {result}")
    
    @staticmethod
    def example_custom_notification():
        """自定义通知示例"""
        print("\n=== 自定义通知示例 ===")
        
        # 1. 直接创建通知
        result = notification_service.create_notification(
            recipient_id="user123",
            title="欢迎加入心理健康平台",
            content="感谢您的加入，开始您的心理健康之旅吧！",
            summary="欢迎新用户",
            notification_type=NotificationType.SYSTEM,
            priority=NotificationPriority.NORMAL,
            action_url="/profile/complete"
        )
        print(f"自定义通知: {result}")
        
        # 2. 定时通知
        scheduled_time = datetime.utcnow() + timedelta(hours=1)
        result = notification_manager.schedule_notification(
            recipient_id="user123",
            scheduled_time=scheduled_time,
            title="记得完成今日心理测评",
            content="坚持每日测评，了解您的心理状态变化。"
        )
        print(f"定时通知: {result}")
        
        # 3. 批量通知
        user_ids = ["user123", "user456", "user789"]
        result = notification_manager.broadcast_notification(
            user_ids=user_ids,
            title="新课程上线通知",
            content="《压力管理技巧》课程现已上线，快来学习吧！",
            notification_type=NotificationType.COURSE,
            priority=NotificationPriority.NORMAL
        )
        print(f"批量通知: {result}")
    
    @staticmethod
    def example_notification_management():
        """通知管理示例"""
        print("\n=== 通知管理示例 ===")
        
        user_id = "user123"
        
        # 1. 获取用户通知列表
        result = notification_service.get_user_notifications(
            user_id=user_id,
            page=1,
            per_page=10
        )
        print(f"通知列表: {len(result['data']['notifications']) if result['code'] == 200 else 0} 条")
        
        # 2. 获取未读数量
        result = notification_service.get_unread_count(user_id)
        if result['code'] == 200:
            print(f"未读通知: {result['data']['total_unread']} 条")
        
        # 3. 标记所有通知为已读
        result = notification_service.mark_all_as_read(user_id)
        print(f"标记已读: {result}")
        
        # 4. 获取通知统计
        result = notification_manager.get_notification_statistics(user_id=user_id)
        if result['code'] == 200:
            summary = result['data']['summary']
            print(f"通知统计: 总计{summary['total_count']}条，阅读率{summary['read_rate']}%")
    
    @staticmethod
    def example_notification_config():
        """通知配置示例"""
        print("\n=== 通知配置示例 ===")
        
        user_id = "user123"
        
        # 1. 获取用户通知配置
        result = notification_manager.get_user_notification_config(user_id)
        print(f"用户配置: {result}")
        
        # 2. 更新通知配置
        config_data = {
            'in_app_enabled': True,
            'email_enabled': True,
            'sms_enabled': False,
            'push_enabled': True,
            'quiet_start_time': '22:00',
            'quiet_end_time': '08:00',
            'max_daily_count': 20,
            'max_hourly_count': 5
        }
        
        result = notification_manager.update_user_notification_config(
            user_id=user_id,
            notification_type=NotificationType.SOCIAL_LIKE,
            config_data=config_data
        )
        print(f"配置更新: {result}")
    
    @staticmethod
    def run_all_examples():
        """运行所有示例"""
        print("🚀 通知系统使用示例演示")
        print("=" * 50)
        
        try:
            NotificationExamples.example_appointment_workflow()
            NotificationExamples.example_order_workflow()
            NotificationExamples.example_social_notifications()
            NotificationExamples.example_system_notifications()
            NotificationExamples.example_custom_notification()
            NotificationExamples.example_notification_management()
            NotificationExamples.example_notification_config()
            
            print("\n✅ 所有示例演示完成")
            
        except Exception as e:
            print(f"\n❌ 示例演示出错: {str(e)}")


# 在其他业务模块中集成通知的示例
class BusinessIntegrationExamples:
    """业务集成示例"""
    
    @staticmethod
    def appointment_service_example():
        """预约服务集成示例"""
        print("\n=== 预约服务集成示例 ===")
        
        # 在预约确认的业务逻辑中添加通知
        def confirm_appointment(appointment_id, user_id):
            """确认预约（伪代码）"""
            try:
                # 1. 更新预约状态
                # appointment.status = 'confirmed'
                # db.session.commit()
                
                # 2. 发送确认通知
                notification_triggers.on_appointment_confirmed(
                    appointment_id=appointment_id,
                    user_id=user_id,
                    appointment_time="2024-01-15 14:30:00",
                    counselor_name="张医生",
                    location="心理咨询室A"
                )
                
                # 3. 设置提醒通知
                notification_triggers.on_appointment_reminder(
                    appointment_id=appointment_id,
                    user_id=user_id,
                    appointment_time="2024-01-15 14:30:00",
                    counselor_name="张医生",
                    location="心理咨询室A",
                    reminder_minutes=60
                )
                
                return {"success": True, "message": "预约确认成功"}
                
            except Exception as e:
                return {"success": False, "message": str(e)}
        
        # 示例调用
        result = confirm_appointment("appt123", "user456")
        print(f"预约确认结果: {result}")
    
    @staticmethod
    def user_registration_example():
        """用户注册集成示例"""
        print("\n=== 用户注册集成示例 ===")
        
        def register_user(username, email):
            """用户注册（伪代码）"""
            try:
                # 1. 创建用户
                user_id = "new_user_123"
                # user = User(username=username, email=email)
                # db.session.add(user)
                # db.session.commit()
                
                # 2. 发送欢迎通知
                notification_service.create_notification(
                    recipient_id=user_id,
                    title="欢迎加入心理健康平台！",
                    content=f"亲爱的 {username}，欢迎您加入我们的心理健康大家庭。开始您的心理健康之旅吧！",
                    notification_type=NotificationType.ACCOUNT,
                    priority=NotificationPriority.NORMAL,
                    action_url="/guide/getting-started"
                )
                
                # 3. 发送欢迎邮件（如果需要）
                # email_service.send_welcome_email(email, username)
                
                return {"success": True, "user_id": user_id}
                
            except Exception as e:
                return {"success": False, "message": str(e)}
        
        # 示例调用
        result = register_user("新用户", "newuser@example.com")
        print(f"用户注册结果: {result}")


if __name__ == "__main__":
    # 运行示例
    NotificationExamples.run_all_examples()
    BusinessIntegrationExamples.appointment_service_example()
    BusinessIntegrationExamples.user_registration_example()
