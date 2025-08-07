from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    """用户信息实体"""
    __tablename__ = 'users'

    id = Column(String(50), primary_key=True)  # 用户ID
    username = Column(String(100), nullable=False)  # 用户名
    avatar = Column(String(255))  # 头像URL
    phone = Column(String(20))  # 手机号
    email = Column(String(100))  # 邮箱

    # 关系
    consultants = relationship("Consultant", back_populates="user")

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'avatar': self.avatar,
            'phone': self.phone,
            'email': self.email,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
