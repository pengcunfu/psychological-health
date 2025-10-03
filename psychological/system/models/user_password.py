from sqlalchemy import Column, String, ForeignKey
from pcf_flask_helper.model.base import BaseModel


class UserPassword(BaseModel):
    """用户密码表"""
    __tablename__ = 'user_passwords'
    
    id = Column(String(50), primary_key=True)  # 密码记录ID
    user_id = Column(String(50), ForeignKey('users.id'), nullable=False, unique=True)  # 用户ID
    password_hash = Column(String(255), nullable=False)  # 密码哈希值
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }