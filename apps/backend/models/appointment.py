from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer

from .base import BaseModel


class Appointment(BaseModel):
    """咨询预约实体"""
    __tablename__ = 'appointments'

    user_id = Column(String(50), nullable=False)  # 用户ID
    counselor_id = Column(String(50), nullable=False)  # 咨询师ID
    appointment_time = Column(DateTime, nullable=False)  # 预约时间
    status = Column(Integer, default=0)  # 预约状态（0-待确认，1-已确认，2-已完成，3-已取消）

    def is_confirmed(self):
        return self.status == 1

    def is_completed(self):
        return self.status == 2

    def is_cancelled(self):
        return self.status == 3

    def confirm(self):
        if self.status != 0:
            raise ValueError("Appointment is already confirmed or completed")
        self.status = 1

    def complete(self):
        if self.status != 1:
            raise ValueError("Appointment must be confirmed before completing")
        self.status = 2

    def cancel(self):
        if self.status not in [0, 1]:
            raise ValueError("Appointment cannot be cancelled from its current status")
        self.status = 3

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'counselor_id': self.counselor_id,
            'appointment_time': self.appointment_time.isoformat() if self.appointment_time else None,
            'status': self.status,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }

    def __str__(self):
        return f"Appointment(id={self.id}, user_id={self.user_id}, counselor_id={self.counselor_id}, appointment_time={self.appointment_time}, status={self.status}, create_time={self.create_time}, update_time={self.update_time})"
