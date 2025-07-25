from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, func
from .base import BaseModel


class Review(BaseModel):
    """评价实体"""
    __tablename__ = 'reviews'
    
    id = Column(String(50), primary_key=True)  # 评价ID
    counselor_id = Column(String(50), nullable=False)  # 咨询师ID
    order_id = Column(String(50), nullable=False)  # 订单ID
    content = Column(Text)  # 评价内容
    rating = Column(Integer, default=5)  # 评分

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'counselor_id': self.counselor_id,
            'order_id': self.order_id,
            'content': self.content,
            'rating': self.rating,
            'create_time': self.create_time.isoformat() if self.create_time else None
        }
