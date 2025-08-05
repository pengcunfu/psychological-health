from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean
from .base import BaseModel


class Announcement(BaseModel):
    """公告实体"""
    __tablename__ = 'announcements'

    id = Column(String(50), primary_key=True)  # 公告ID
    title = Column(String(200), nullable=False)  # 公告标题
    type = Column(String(50), nullable=False)  # 公告类型：system, activity, maintenance, notice
    priority = Column(String(50), nullable=False)  # 优先级：low, medium, high, urgent
    status = Column(String(50), nullable=False)  # 状态：draft, published, archived
    summary = Column(Text)  # 公告摘要
    content = Column(Text, nullable=False)  # 公告内容
    start_time = Column(DateTime)  # 生效时间
    end_time = Column(DateTime)  # 失效时间
    is_pinned = Column(Boolean, default=False)  # 是否置顶
    user_id = Column(String(50))  # 用户ID（暂时不传入）

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'priority': self.priority,
            'status': self.status,
            'summary': self.summary,
            'content': self.content,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'is_pinned': self.is_pinned,
            'user_id': self.user_id,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
