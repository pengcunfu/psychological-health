from sqlalchemy import Column, String, Integer, DateTime, func
from .base import BaseModel


class Category(BaseModel):
    """咨询类型实体"""
    __tablename__ = 'categories'

    id = Column(String(50), primary_key=True)  # 类型ID
    name = Column(String(100), nullable=False)  # 类型名称
    icon = Column(String(255))  # 图标URL
    path = Column(String(255))  # 跳转路径
    description = Column(String(500))  # 类型描述
    sort_order = Column(Integer, default=0)  # 排序顺序
    status = Column(Integer, default=1)  # 状态（0-禁用，1-启用）

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'path': self.path,
            'description': self.description,
            'sort_order': self.sort_order,
            'status': self.status,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
