import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, UniqueConstraint
from .base import BaseModel


class SocialLike(BaseModel):
    """社区点赞"""
    __tablename__ = 'social_likes'
    
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), nullable=False, comment='点赞用户ID')
    target_id = Column(String(50), nullable=False, comment='点赞目标ID（帖子或评论）')
    target_type = Column(String(20), nullable=False, comment='点赞类型：post帖子，comment评论')
    
    # 状态
    status = Column(String(20), default='active', comment='状态：active有效，cancelled已取消')
    
    # 添加唯一约束，防止重复点赞
    __table_args__ = (
        UniqueConstraint('user_id', 'target_id', 'target_type', name='unique_user_target_like'),
    )
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_id': self.target_id,
            'target_type': self.target_type,
            'status': self.status,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
    
    def cancel(self):
        """取消点赞"""
        self.status = 'cancelled'
    
    def reactivate(self):
        """重新激活点赞"""
        self.status = 'active'
    
    def is_active(self):
        """判断点赞是否有效"""
        return self.status == 'active' 