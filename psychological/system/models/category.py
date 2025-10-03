from sqlalchemy import Column, String, Integer
from pcf_flask_helper.model.base import BaseModel


class Category(BaseModel):
    """分类实体"""
    __tablename__ = 'categories'

    id = Column(String(50), primary_key=True)  # 分类ID
    name = Column(String(100), nullable=False)  # 分类名称
    type = Column(String(50), default='course')  # 分类类型（course-课程分类，counselor-咨询师分类，article-文章分类）
    icon = Column(String(255))  # 图标URL
    path = Column(String(255))  # 跳转路径
    description = Column(String(500))  # 分类描述
    sort_order = Column(Integer, default=0)  # 排序顺序
    status = Column(Integer, default=1)  # 状态（0-禁用，1-启用）

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'icon': self.icon,
            'path': self.path,
            'description': self.description,
            'sort_order': self.sort_order,
            'status': self.status,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
