from sqlalchemy import Column, String, Integer
from .base import BaseModel


class Announcement(BaseModel):
    """公告实体"""
    __tablename__ = 'announcements'

    id = Column(String(50), primary_key=True)  # 公告ID
    counselor_id = Column(String(50), nullable=False)  # 咨询师ID
    service_id = Column(String(50), nullable=False)  # 服务ID
    user_id = Column(String(50), nullable=False)  # 用户ID
    date = Column(String(20), nullable=False)  # 日期
    note = Column(String(500))  # 备注
    time_slot = Column(String(50), nullable=False)  # 时间段
    status = Column(Integer, default=1)  # 状态

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'counselor_id': self.counselor_id,
            'service_id': self.service_id,
            'user_id': self.user_id,
            'date': self.date,
            'note': self.note,
            'time_slot': self.time_slot,
            'status': self.status,
            'create_time': self.create_time.isoformat() if self.create_time else None
        }
