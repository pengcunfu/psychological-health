from typing import List
import json
from sqlalchemy import Column, String, Integer, DateTime, Float, Text, func
from .base import BaseModel


class Workspace(BaseModel):
    """心理工作室实体"""
    __tablename__ = 'workspaces'

    id = Column(String(50), primary_key=True)  # 工作室ID
    name = Column(String(200), nullable=False)  # 工作室名称
    cover_image = Column(String(255))  # 封面图片URL
    address = Column(String(500))  # 详细地址
    distance = Column(Float, default=0.0)  # 距离（单位：km）
    business_hours = Column(String(200))  # 营业时间，例如：周一至周日 9:00-18:00
    _environment_images = Column('environment_images', Text)  # 环境照片URL列表（JSON存储）
    introduction = Column(Text)  # 工作室简介
    slogan = Column(String(500))  # 工作室寄语
    latitude = Column(Float, default=0.0)  # 纬度
    longitude = Column(Float, default=0.0)  # 经度
    status = Column(Integer, default=1)  # 状态（0-关闭，1-营业中）
    sort_order = Column(Integer, default=100)

    @property
    def environment_images(self) -> List[str]:
        """获取环境照片列表"""
        if self._environment_images:
            return json.loads(self._environment_images)
        return []

    @environment_images.setter
    def environment_images(self, value: List[str]):
        """设置环境照片列表"""
        self._environment_images = json.dumps(value) if value else None

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'cover_image': self.cover_image,
            'address': self.address,
            'distance': self.distance,
            'business_hours': self.business_hours,
            'environment_images': self.environment_images,
            'introduction': self.introduction,
            'slogan': self.slogan,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'status': self.status,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
