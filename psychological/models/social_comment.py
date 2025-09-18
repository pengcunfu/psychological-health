import uuid
import json
from datetime import datetime
from typing import List
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from .base import BaseModel


class SocialComment(BaseModel):
    """社区评论"""
    __tablename__ = 'social_comments'
    
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = Column(String(50), nullable=False, comment='帖子ID')
    user_id = Column(String(50), nullable=False, comment='评论用户ID')
    parent_id = Column(String(50), comment='父评论ID（用于回复）')
    reply_to_user_id = Column(String(50), comment='回复的用户ID')
    
    content = Column(Text, nullable=False, comment='评论内容')
    
    # 媒体内容（评论也可以包含图片）
    _images = Column('images', Text, comment='图片列表（JSON存储）')
    
    # 状态和属性
    status = Column(String(20), default='published', comment='状态：published已发布，hidden隐藏，deleted已删除')
    is_anonymous = Column(Boolean, default=False, comment='是否匿名评论')
    
    # 统计数据
    like_count = Column(Integer, default=0, comment='点赞数')
    reply_count = Column(Integer, default=0, comment='回复数量')
    
    # 位置信息（可选）
    location = Column(String(200), comment='评论位置')
    
    # 审核信息
    audit_status = Column(String(20), default='approved', comment='审核状态：pending待审核，approved通过，rejected拒绝')
    audit_reason = Column(Text, comment='审核原因')
    audited_by = Column(String(50), comment='审核人ID')
    audited_at = Column(DateTime, comment='审核时间')
    
    @property
    def images(self) -> List[str]:
        """获取图片列表"""
        if self._images:
            return json.loads(self._images)
        return []
    
    @images.setter
    def images(self, value: List[str]):
        """设置图片列表"""
        self._images = json.dumps(value) if value else None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'parent_id': self.parent_id,
            'reply_to_user_id': self.reply_to_user_id,
            'content': self.content,
            'images': self.images,
            'status': self.status,
            'is_anonymous': self.is_anonymous,
            'like_count': self.like_count,
            'reply_count': self.reply_count,
            'location': self.location,
            'audit_status': self.audit_status,
            'audit_reason': self.audit_reason,
            'audited_by': self.audited_by,
            'audited_at': self.audited_at.isoformat() if self.audited_at else None,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
    
    def to_tree_dict(self):
        """用于评论树结构的字典"""
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'parent_id': self.parent_id,
            'reply_to_user_id': self.reply_to_user_id,
            'content': self.content,
            'images': self.images,
            'is_anonymous': self.is_anonymous,
            'like_count': self.like_count,
            'reply_count': self.reply_count,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'replies': []  # 子评论列表，由业务层填充
        }
    
    def increment_like(self):
        """增加点赞数"""
        self.like_count = (self.like_count or 0) + 1
    
    def decrement_like(self):
        """减少点赞数"""
        self.like_count = max((self.like_count or 0) - 1, 0)
    
    def increment_reply(self):
        """增加回复数"""
        self.reply_count = (self.reply_count or 0) + 1
    
    def decrement_reply(self):
        """减少回复数"""
        self.reply_count = max((self.reply_count or 0) - 1, 0)
    
    def is_reply(self):
        """判断是否为回复评论"""
        return self.parent_id is not None 