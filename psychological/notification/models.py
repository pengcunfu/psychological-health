"""
通知系统数据模型
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, JSON, Index
from sqlalchemy.dialects.mysql import ENUM
from pcf_flask_helper.model.base import BaseModel
from .types import NotificationType, NotificationPriority, NotificationStatus, NotificationAction


class Notification(BaseModel):
    """站内通知模型"""
    __tablename__ = 'notifications'
    
    # 基础字段
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # 通知基本信息
    title = Column(String(200), nullable=False, comment='通知标题')
    content = Column(Text, comment='通知内容')
    summary = Column(String(500), comment='通知摘要')
    
    # 接收方信息
    recipient_id = Column(String(50), nullable=False, comment='接收者用户ID')
    recipient_type = Column(String(20), default='user', comment='接收者类型：user用户，group群组，role角色，all全体')
    
    # 发送方信息
    sender_id = Column(String(50), comment='发送者用户ID')
    sender_type = Column(String(20), default='system', comment='发送者类型：system系统，user用户，admin管理员')
    sender_name = Column(String(100), comment='发送者名称')
    
    # 通知分类
    type = Column(ENUM(NotificationType), nullable=False, default=NotificationType.SYSTEM, comment='通知类型')
    category = Column(String(50), comment='通知分类标识')
    sub_category = Column(String(50), comment='通知子分类')
    
    # 通知属性
    priority = Column(ENUM(NotificationPriority), default=NotificationPriority.NORMAL, comment='优先级')
    status = Column(ENUM(NotificationStatus), default=NotificationStatus.UNREAD, comment='状态')
    
    # 时间信息
    read_time = Column(DateTime, comment='阅读时间')
    scheduled_time = Column(DateTime, comment='定时发送时间')
    expire_time = Column(DateTime, comment='过期时间')
    
    # 关联信息
    related_id = Column(String(50), comment='关联业务对象ID')
    related_type = Column(String(50), comment='关联业务对象类型')
    related_url = Column(String(500), comment='关联URL')
    
    # 动作配置
    action_type = Column(ENUM(NotificationAction), default=NotificationAction.NONE, comment='动作类型')
    action_url = Column(String(500), comment='动作URL')
    action_data = Column(JSON, comment='动作数据')
    
    # 显示配置
    icon = Column(String(200), comment='通知图标')
    image = Column(String(500), comment='通知图片')
    color = Column(String(20), comment='通知颜色')
    
    # 扩展数据
    extra_data = Column(JSON, comment='扩展数据')
    metadata = Column(JSON, comment='元数据')
    
    # 标记字段
    is_pinned = Column(Boolean, default=False, comment='是否置顶')
    is_broadcast = Column(Boolean, default=False, comment='是否广播通知')
    is_silent = Column(Boolean, default=False, comment='是否静默通知')
    
    # 添加索引
    __table_args__ = (
        Index('idx_recipient_status_time', 'recipient_id', 'status', 'create_time'),
        Index('idx_type_priority_time', 'type', 'priority', 'create_time'),
        Index('idx_related_object', 'related_type', 'related_id'),
        Index('idx_scheduled_time', 'scheduled_time'),
    )
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'recipient_id': self.recipient_id,
            'recipient_type': self.recipient_type,
            'sender_id': self.sender_id,
            'sender_type': self.sender_type,
            'sender_name': self.sender_name,
            'type': self.type.value if self.type else None,
            'category': self.category,
            'sub_category': self.sub_category,
            'priority': self.priority.value if self.priority else None,
            'status': self.status.value if self.status else None,
            'read_time': self.read_time.isoformat() if self.read_time else None,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'expire_time': self.expire_time.isoformat() if self.expire_time else None,
            'related_id': self.related_id,
            'related_type': self.related_type,
            'related_url': self.related_url,
            'action_type': self.action_type.value if self.action_type else None,
            'action_url': self.action_url,
            'action_data': self.action_data,
            'icon': self.icon,
            'image': self.image,
            'color': self.color,
            'extra_data': self.extra_data,
            'metadata': self.metadata,
            'is_pinned': self.is_pinned,
            'is_broadcast': self.is_broadcast,
            'is_silent': self.is_silent,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
    
    def mark_as_read(self):
        """标记为已读"""
        if self.status == NotificationStatus.UNREAD:
            self.status = NotificationStatus.READ
            self.read_time = datetime.utcnow()
    
    def mark_as_unread(self):
        """标记为未读"""
        self.status = NotificationStatus.UNREAD
        self.read_time = None
    
    def archive(self):
        """归档通知"""
        self.status = NotificationStatus.ARCHIVED
    
    def is_expired(self):
        """检查是否过期"""
        if not self.expire_time:
            return False
        return datetime.utcnow() > self.expire_time
    
    def is_readable(self):
        """检查是否可读"""
        return not self.is_expired() and self.status != NotificationStatus.DELETED


class NotificationTemplate(BaseModel):
    """通知模板模型"""
    __tablename__ = 'notification_templates'
    
    # 基础字段
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # 模板基本信息
    name = Column(String(100), nullable=False, comment='模板名称')
    code = Column(String(100), nullable=False, unique=True, comment='模板代码')
    description = Column(Text, comment='模板描述')
    
    # 模板内容
    title_template = Column(String(500), comment='标题模板')
    content_template = Column(Text, comment='内容模板')
    summary_template = Column(String(1000), comment='摘要模板')
    
    # 模板分类
    type = Column(ENUM(NotificationType), nullable=False, comment='通知类型')
    category = Column(String(50), comment='分类')
    
    # 模板配置
    priority = Column(ENUM(NotificationPriority), default=NotificationPriority.NORMAL, comment='默认优先级')
    channels = Column(JSON, comment='支持的通知渠道')
    
    # 样式配置
    icon = Column(String(200), comment='默认图标')
    color = Column(String(20), comment='默认颜色')
    
    # 动作配置
    action_type = Column(ENUM(NotificationAction), default=NotificationAction.NONE, comment='默认动作类型')
    action_url_template = Column(String(500), comment='动作URL模板')
    
    # 模板变量
    variables = Column(JSON, comment='模板变量定义')
    default_values = Column(JSON, comment='默认值')
    
    # 状态控制
    is_active = Column(Boolean, default=True, comment='是否启用')
    version = Column(String(20), default='1.0', comment='模板版本')
    
    # 使用统计
    usage_count = Column(Integer, default=0, comment='使用次数')
    last_used_time = Column(DateTime, comment='最后使用时间')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'title_template': self.title_template,
            'content_template': self.content_template,
            'summary_template': self.summary_template,
            'type': self.type.value if self.type else None,
            'category': self.category,
            'priority': self.priority.value if self.priority else None,
            'channels': self.channels,
            'icon': self.icon,
            'color': self.color,
            'action_type': self.action_type.value if self.action_type else None,
            'action_url_template': self.action_url_template,
            'variables': self.variables,
            'default_values': self.default_values,
            'is_active': self.is_active,
            'version': self.version,
            'usage_count': self.usage_count,
            'last_used_time': self.last_used_time.isoformat() if self.last_used_time else None,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
    
    def render_notification_data(self, variables_data: dict) -> dict:
        """渲染通知数据"""
        from string import Template
        
        # 合并默认值和传入变量
        render_data = {}
        if self.default_values:
            render_data.update(self.default_values)
        render_data.update(variables_data or {})
        
        # 渲染各个字段
        result = {}
        
        if self.title_template:
            result['title'] = Template(self.title_template).safe_substitute(render_data)
            
        if self.content_template:
            result['content'] = Template(self.content_template).safe_substitute(render_data)
            
        if self.summary_template:
            result['summary'] = Template(self.summary_template).safe_substitute(render_data)
            
        if self.action_url_template:
            result['action_url'] = Template(self.action_url_template).safe_substitute(render_data)
        
        # 添加其他配置
        result.update({
            'type': self.type,
            'priority': self.priority,
            'icon': self.icon,
            'color': self.color,
            'action_type': self.action_type
        })
        
        return result


class NotificationConfig(BaseModel):
    """通知配置模型"""
    __tablename__ = 'notification_configs'
    
    # 基础字段
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # 配置基本信息
    user_id = Column(String(50), nullable=False, comment='用户ID')
    
    # 通知类型配置
    type = Column(ENUM(NotificationType), nullable=False, comment='通知类型')
    
    # 渠道配置
    in_app_enabled = Column(Boolean, default=True, comment='是否启用站内通知')
    email_enabled = Column(Boolean, default=True, comment='是否启用邮件通知')
    sms_enabled = Column(Boolean, default=False, comment='是否启用短信通知')
    push_enabled = Column(Boolean, default=True, comment='是否启用推送通知')
    
    # 时间配置
    quiet_start_time = Column(String(5), comment='免打扰开始时间 HH:MM')
    quiet_end_time = Column(String(5), comment='免打扰结束时间 HH:MM')
    
    # 频率控制
    max_daily_count = Column(Integer, comment='每日最大通知数量')
    max_hourly_count = Column(Integer, comment='每小时最大通知数量')
    
    # 优先级过滤
    min_priority = Column(ENUM(NotificationPriority), default=NotificationPriority.LOW, comment='最低优先级')
    
    # 唯一约束
    __table_args__ = (
        Index('idx_user_type', 'user_id', 'type', unique=True),
    )
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type.value if self.type else None,
            'in_app_enabled': self.in_app_enabled,
            'email_enabled': self.email_enabled,
            'sms_enabled': self.sms_enabled,
            'push_enabled': self.push_enabled,
            'quiet_start_time': self.quiet_start_time,
            'quiet_end_time': self.quiet_end_time,
            'max_daily_count': self.max_daily_count,
            'max_hourly_count': self.max_hourly_count,
            'min_priority': self.min_priority.value if self.min_priority else None,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
