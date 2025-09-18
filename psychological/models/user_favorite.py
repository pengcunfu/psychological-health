from datetime import datetime
from sqlalchemy import Column, String, DateTime, func
from .base import BaseModel


class UserFavorite(BaseModel):
    """
    用户收藏实体
    id: 收藏ID
    user_id: 用户ID
    item_id: 收藏项ID
    item_type: 收藏项类型
    create_time: 创建时间
    """
    __tablename__ = 'user_favorites'
    
    id = Column(String(50), primary_key=True)  # 收藏ID
    user_id = Column(String(50), nullable=False)  # 用户ID
    item_id = Column(String(50), nullable=False)  # 收藏项ID
    item_type = Column(String(50), nullable=False)  # 收藏项类型

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'item_type': self.item_type,
            'create_time': self.create_time.isoformat() if self.create_time else None
        }