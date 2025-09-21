"""
通知系统类型定义
"""
import enum


class NotificationType(enum.Enum):
    """通知类型枚举"""
    # 系统通知
    SYSTEM = "system"  # 系统通知
    ANNOUNCEMENT = "announcement"  # 公告通知
    
    # 业务通知
    APPOINTMENT = "appointment"  # 预约相关通知
    ORDER = "order"  # 订单相关通知
    COURSE = "course"  # 课程相关通知
    ASSESSMENT = "assessment"  # 测评相关通知
    
    # 社交通知
    SOCIAL_FOLLOW = "social_follow"  # 关注通知
    SOCIAL_LIKE = "social_like"  # 点赞通知
    SOCIAL_COMMENT = "social_comment"  # 评论通知
    SOCIAL_POST = "social_post"  # 帖子通知
    
    # 账户通知
    ACCOUNT = "account"  # 账户相关通知
    SECURITY = "security"  # 安全通知
    
    # 其他
    REMINDER = "reminder"  # 提醒通知
    PROMOTION = "promotion"  # 推广通知


class NotificationPriority(enum.Enum):
    """通知优先级"""
    LOW = "low"  # 低优先级
    NORMAL = "normal"  # 普通优先级
    HIGH = "high"  # 高优先级
    URGENT = "urgent"  # 紧急


class NotificationStatus(enum.Enum):
    """通知状态"""
    UNREAD = "unread"  # 未读
    READ = "read"  # 已读
    ARCHIVED = "archived"  # 已归档
    DELETED = "deleted"  # 已删除


class NotificationChannel(enum.Enum):
    """通知渠道"""
    IN_APP = "in_app"  # 站内通知
    EMAIL = "email"  # 邮件
    SMS = "sms"  # 短信
    PUSH = "push"  # 推送通知


class NotificationAction(enum.Enum):
    """通知动作类型"""
    NONE = "none"  # 无动作
    CLICK = "click"  # 点击
    REDIRECT = "redirect"  # 跳转
    MODAL = "modal"  # 弹窗
    DOWNLOAD = "download"  # 下载
