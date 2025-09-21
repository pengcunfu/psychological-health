"""
通知系统配置
"""
from ..config import get_config


class NotificationConfig:
    """通知系统配置类"""
    
    # 基础配置
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # 通知保留时间（天）
    NOTIFICATION_RETENTION_DAYS = 90
    READ_NOTIFICATION_RETENTION_DAYS = 30
    
    # 批量操作限制
    MAX_BATCH_SIZE = 1000
    MAX_BULK_CREATE_SIZE = 500
    
    # 定时任务配置
    CLEANUP_INTERVAL_HOURS = 24  # 清理任务间隔（小时）
    DIGEST_INTERVAL_HOURS = 12   # 摘要通知间隔（小时）
    
    # 频率控制
    DEFAULT_MAX_DAILY_NOTIFICATIONS = 50
    DEFAULT_MAX_HOURLY_NOTIFICATIONS = 10
    
    # 模板渲染配置
    TEMPLATE_MAX_LENGTH = {
        'title': 200,
        'content': 5000,
        'summary': 500
    }
    
    # 通知图标配置
    DEFAULT_ICONS = {
        'system': '⚙️',
        'announcement': '📢',
        'appointment': '📅',
        'order': '🛒',
        'course': '📚',
        'assessment': '📊',
        'social_follow': '👥',
        'social_like': '❤️',
        'social_comment': '💬',
        'social_post': '📝',
        'account': '👤',
        'security': '🔒',
        'reminder': '⏰',
        'promotion': '🎁'
    }
    
    # 通知颜色配置
    DEFAULT_COLORS = {
        'low': '#6B7280',      # 灰色
        'normal': '#3B82F6',   # 蓝色
        'high': '#F59E0B',     # 橙色
        'urgent': '#EF4444'    # 红色
    }
    
    # 系统消息发送者配置
    SYSTEM_SENDER = {
        'id': 'system',
        'name': '心理健康平台',
        'type': 'system'
    }
    
    @classmethod
    def get_database_url(cls):
        """获取数据库连接URL"""
        return get_config('database.url')
    
    @classmethod
    def get_redis_url(cls):
        """获取Redis连接URL"""
        return get_config('redis.url', 'redis://localhost:6379/0')
    
    @classmethod
    def is_debug_mode(cls):
        """是否为调试模式"""
        return get_config('debug', False)
    
    @classmethod
    def get_notification_settings(cls):
        """获取通知设置"""
        return {
            'retention_days': cls.NOTIFICATION_RETENTION_DAYS,
            'read_retention_days': cls.READ_NOTIFICATION_RETENTION_DAYS,
            'max_daily_notifications': cls.DEFAULT_MAX_DAILY_NOTIFICATIONS,
            'max_hourly_notifications': cls.DEFAULT_MAX_HOURLY_NOTIFICATIONS,
            'cleanup_interval_hours': cls.CLEANUP_INTERVAL_HOURS,
            'digest_interval_hours': cls.DIGEST_INTERVAL_HOURS
        }


# 预定义通知模板配置
NOTIFICATION_TEMPLATES = {
    # 预约相关通知
    'appointment_confirmed': {
        'name': '预约确认通知',
        'type': 'appointment',
        'title_template': '您的心理咨询预约已确认',
        'content_template': '您好，您预约的心理咨询已确认。\n\n预约时间：$appointment_time\n咨询师：$counselor_name\n\n请按时参加咨询，如有疑问请联系客服。',
        'summary_template': '预约时间：$appointment_time，咨询师：$counselor_name',
        'action_type': 'redirect',
        'action_url_template': '/appointment/$appointment_id',
        'icon': '📅',
        'color': '#10B981'
    },
    
    'appointment_cancelled': {
        'name': '预约取消通知',
        'type': 'appointment',
        'title_template': '您的心理咨询预约已取消',
        'content_template': '很抱歉，您预约的心理咨询已被取消。\n\n原预约时间：$appointment_time\n咨询师：$counselor_name\n取消原因：$cancel_reason\n\n如需重新预约，请联系客服。',
        'summary_template': '预约已取消，原时间：$appointment_time',
        'action_type': 'redirect',
        'action_url_template': '/appointment/list',
        'icon': '❌',
        'color': '#EF4444'
    },
    
    'appointment_reminder': {
        'name': '预约提醒通知',
        'type': 'reminder',
        'title_template': '咨询预约提醒',
        'content_template': '友情提醒，您有一个心理咨询即将开始。\n\n预约时间：$appointment_time\n咨询师：$counselor_name\n地点：$location\n\n请提前准备，按时参加。',
        'summary_template': '$reminder_time 后开始咨询',
        'action_type': 'redirect',
        'action_url_template': '/appointment/$appointment_id',
        'icon': '⏰',
        'color': '#F59E0B'
    },
    
    # 订单相关通知
    'order_paid': {
        'name': '订单支付成功通知',
        'type': 'order',
        'title_template': '订单支付成功',
        'content_template': '您的订单已支付成功！\n\n订单号：$order_number\n商品：$product_name\n支付金额：￥$amount\n\n感谢您的购买，祝您学习愉快！',
        'summary_template': '订单 $order_number 支付成功',
        'action_type': 'redirect',
        'action_url_template': '/order/$order_id',
        'icon': '✅',
        'color': '#10B981'
    },
    
    'order_refunded': {
        'name': '订单退款通知',
        'type': 'order',
        'title_template': '订单退款处理完成',
        'content_template': '您的订单退款已处理完成。\n\n订单号：$order_number\n退款金额：￥$refund_amount\n\n退款将在3-5个工作日内到账，请注意查收。',
        'summary_template': '订单 $order_number 已退款 ￥$refund_amount',
        'action_type': 'redirect',
        'action_url_template': '/order/$order_id',
        'icon': '💰',
        'color': '#6366F1'
    },
    
    # 课程相关通知
    'course_subscribed': {
        'name': '课程订阅成功通知',
        'type': 'course',
        'title_template': '课程订阅成功',
        'content_template': '恭喜您成功订阅课程！\n\n课程名称：$course_name\n讲师：$instructor_name\n\n现在就可以开始学习了，祝您学习愉快！',
        'summary_template': '已订阅课程：$course_name',
        'action_type': 'redirect',
        'action_url_template': '/course/$course_id',
        'icon': '📚',
        'color': '#8B5CF6'
    },
    
    'course_completed': {
        'name': '课程完成通知',
        'type': 'course',
        'title_template': '恭喜您完成课程学习',
        'content_template': '恭喜您完成了课程学习！\n\n课程名称：$course_name\n学习时长：$study_duration\n完成率：100%\n\n感谢您的坚持学习，继续加油！',
        'summary_template': '已完成课程：$course_name',
        'action_type': 'redirect',
        'action_url_template': '/course/$course_id/certificate',
        'icon': '🎓',
        'color': '#F59E0B'
    },
    
    # 测评相关通知
    'assessment_completed': {
        'name': '测评完成通知',
        'type': 'assessment',
        'title_template': '心理测评报告已生成',
        'content_template': '您的心理测评已完成，报告已生成。\n\n测评名称：$assessment_name\n完成时间：$completion_time\n\n点击查看详细的测评报告和建议。',
        'summary_template': '测评 $assessment_name 已完成',
        'action_type': 'redirect',
        'action_url_template': '/assessment/result/$record_id',
        'icon': '📊',
        'color': '#06B6D4'
    },
    
    # 社交相关通知
    'social_followed': {
        'name': '新关注通知',
        'type': 'social_follow',
        'title_template': '有新用户关注了您',
        'content_template': '$follower_name 关注了您。\n\n点击查看Ta的个人主页，了解更多信息。',
        'summary_template': '$follower_name 关注了您',
        'action_type': 'redirect',
        'action_url_template': '/user/$follower_id',
        'icon': '👥',
        'color': '#EC4899'
    },
    
    'social_liked': {
        'name': '内容被点赞通知',
        'type': 'social_like',
        'title_template': '您的内容收到了点赞',
        'content_template': '$liker_name 赞了您的$content_type。\n\n"$content_preview"\n\n感谢您的精彩分享！',
        'summary_template': '$liker_name 赞了您的$content_type',
        'action_type': 'redirect',
        'action_url_template': '/$content_type/$content_id',
        'icon': '❤️',
        'color': '#EF4444'
    },
    
    'social_commented': {
        'name': '内容被评论通知',
        'type': 'social_comment',
        'title_template': '您的内容收到了评论',
        'content_template': '$commenter_name 评论了您的$content_type。\n\n评论内容：$comment_content\n\n快去看看并回复吧！',
        'summary_template': '$commenter_name 评论了您的$content_type',
        'action_type': 'redirect',
        'action_url_template': '/$content_type/$content_id#comment-$comment_id',
        'icon': '💬',
        'color': '#3B82F6'
    },
    
    # 系统通知
    'system_announcement': {
        'name': '系统公告通知',
        'type': 'announcement',
        'title_template': '$announcement_title',
        'content_template': '$announcement_content',
        'summary_template': '$announcement_summary',
        'action_type': 'modal',
        'icon': '📢',
        'color': '#F59E0B'
    },
    
    'system_maintenance': {
        'name': '系统维护通知',
        'type': 'system',
        'title_template': '系统维护通知',
        'content_template': '系统将于$maintenance_time进行维护升级。\n\n维护时间：$maintenance_duration\n\n维护期间系统将暂停服务，请合理安排使用时间。',
        'summary_template': '系统将于$maintenance_time进行维护',
        'action_type': 'none',
        'icon': '🔧',
        'color': '#6B7280'
    },
    
    # 安全通知
    'security_login': {
        'name': '异地登录通知',
        'type': 'security',
        'title_template': '检测到异地登录',
        'content_template': '检测到您的账户在新设备登录。\n\n登录时间：$login_time\n登录地点：$login_location\n设备信息：$device_info\n\n如非本人操作，请立即修改密码。',
        'summary_template': '检测到$login_location的登录',
        'action_type': 'redirect',
        'action_url_template': '/account/security',
        'icon': '🔒',
        'color': '#EF4444'
    },
    
    'security_password_changed': {
        'name': '密码修改通知',
        'type': 'security',
        'title_template': '密码修改成功',
        'content_template': '您的账户密码已成功修改。\n\n修改时间：$change_time\n\n如非本人操作，请立即联系客服。',
        'summary_template': '密码已于$change_time修改',
        'action_type': 'redirect',
        'action_url_template': '/account/security',
        'icon': '🔐',
        'color': '#10B981'
    }
}
