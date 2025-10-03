from sqlalchemy import Column, String, ForeignKey
from pcf_flask_helper.model.base import BaseModel


class UserRole(BaseModel):
    """用户角色关联表"""
    __tablename__ = 'user_roles'
    
    id = Column(String(50), primary_key=True)  # 关联ID
    user_id = Column(String(50), ForeignKey('users.id'), nullable=False)  # 用户ID
    role_id = Column(String(50), ForeignKey('roles.id'), nullable=False)  # 角色ID
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role_id': self.role_id,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }