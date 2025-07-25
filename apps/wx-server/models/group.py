from sqlalchemy import Column, String, Integer, Float, Text
from .base import BaseModel


class Group(BaseModel):
    """团体小组实体"""
    __tablename__ = 'groups'
    
    id = Column(String(50), primary_key=True)  # 小组ID
    title = Column(String(200), nullable=False)  # 小组标题
    cover_image = Column(String(255))  # 封面图片URL
    counselor_id = Column(String(50), nullable=False)  # 导师ID
    counselor_name = Column(String(100), nullable=False)  # 导师姓名
    price = Column(Float, default=0.0)  # 价格（元/人）
    capacity = Column(Integer, default=0)  # 人数容量
    enrolled = Column(Integer, default=0)  # 已报名人数
    location = Column(String(200))  # 地点
    city = Column(String(100))  # 城市
    type = Column(String(50))  # 类型（线上/线下）
    start_date = Column(String(20))  # 开始日期
    duration = Column(String(100))  # 持续时间（如：共20次）
    schedule = Column(String(200))  # 时间安排（如：每周一19:00-20:30）
    description = Column(Text)  # 课程介绍
    status = Column(Integer, default=1)  # 状态（0-未开始，1-报名中，2-已结束）

    def get_remaining_slots(self) -> int:
        """获取剩余名额"""
        return self.capacity - self.enrolled

    def is_full(self) -> bool:
        """检查是否已满员"""
        return self.enrolled >= self.capacity
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'cover_image': self.cover_image,
            'counselor_id': self.counselor_id,
            'counselor_name': self.counselor_name,
            'price': self.price,
            'capacity': self.capacity,
            'enrolled': self.enrolled,
            'location': self.location,
            'city': self.city,
            'type': self.type,
            'start_date': self.start_date,
            'duration': self.duration,
            'schedule': self.schedule,
            'description': self.description,
            'status': self.status,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }