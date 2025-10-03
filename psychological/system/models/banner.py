from pcf_flask_helper.model.base import BaseModel
from sqlalchemy import Column, String, Integer
from pcf_flask_helper.common import process_image_url


class Banner(BaseModel):
    """轮播图实体"""
    __tablename__ = 'banners'

    title = Column(String(100), nullable=False)  # 轮播图标题
    image_url = Column(String(255), nullable=False)  # 图片URL
    link_url = Column(String(255))  # 跳转链接
    sort_order = Column(Integer, default=0)  # 排序顺序
    status = Column(Integer, default=1)  # 状态（0-禁用，1-启用）

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'image_url': process_image_url(self.image_url),
            'link_url': self.link_url,
            'sort_order': self.sort_order,
            'status': self.status,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
