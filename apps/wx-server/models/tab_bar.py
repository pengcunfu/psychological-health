from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func
from .base import BaseModel


class TabBar(BaseModel):
    """底部导航栏实体"""
    __tablename__ = 'tab_bars'
    
    id = Column(String(50), primary_key=True)  # 导航项ID
    icon = Column(String(255))  # 图标URL
    active_icon = Column(String(255))  # 激活态图标URL
    text = Column(String(50), nullable=False)  # 导航文本
    path = Column(String(255))  # 跳转路径
    sort_order = Column(Integer, default=0)  # 排序顺序
    status = Column(Integer, default=1)  # 状态（0-禁用，1-启用）
    role = Column(String(20), default='user')  # 角色（user-普通用户，counselor-咨询师）

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'icon': self.icon,
            'active_icon': self.active_icon,
            'text': self.text,
            'path': self.path,
            'sort_order': self.sort_order,
            'status': self.status,
            'role': self.role,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }