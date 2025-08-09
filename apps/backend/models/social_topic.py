import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from .base import BaseModel


class SocialTopic(BaseModel):
    """社区话题"""
    __tablename__ = 'social_topics'
    
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True, comment='话题名称')
    description = Column(Text, comment='话题描述')
    cover_image = Column(String(255), comment='话题封面图片')
    color = Column(String(20), default='#1890ff', comment='话题颜色')
    sort_order = Column(Integer, default=0, comment='排序权重')
    is_hot = Column(Boolean, default=False, comment='是否热门话题')
    is_featured = Column(Boolean, default=False, comment='是否精选话题')
    status = Column(String(20), default='active', comment='状态：active启用，inactive禁用')
    
    # 统计字段
    post_count = Column(Integer, default=0, comment='帖子数量')
    participant_count = Column(Integer, default=0, comment='参与人数')
    view_count = Column(Integer, default=0, comment='浏览次数')
    
    # 管理员信息
    created_by = Column(String(50), comment='创建者ID')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cover_image': self.cover_image,
            'color': self.color,
            'sort_order': self.sort_order,
            'is_hot': self.is_hot,
            'is_featured': self.is_featured,
            'status': self.status,
            'post_count': self.post_count,
            'participant_count': self.participant_count,
            'view_count': self.view_count,
            'created_by': self.created_by,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
    
    def to_simple_dict(self):
        """简化的字典表示"""
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'post_count': self.post_count,
            'participant_count': self.participant_count
        } 