from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Float, func
from .base import BaseModel


class Order(BaseModel):
    """订单信息实体"""
    __tablename__ = 'orders'
    
    id = Column(String(50), primary_key=True)  # 订单ID
    user_id = Column(String(50), nullable=False)  # 用户ID
    product_id = Column(String(50), nullable=False)  # 商品ID（课程ID或咨询预约ID）
    type = Column(Integer, nullable=False)  # 商品类型（1-课程，2-咨询）
    amount = Column(Float, default=0.0)  # 订单金额
    status = Column(Integer, default=0)  # 支付状态（0-未支付，1-已支付，2-已退款）

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'type': self.type,
            'amount': self.amount,
            'status': self.status,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }