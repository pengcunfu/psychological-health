from typing import List
from sqlalchemy import Column, String, Integer, Float, Text
from pcf_flask_helper.model.base import BaseModel
from pcf_flask_helper.common import process_image_url
import json


class Counselor(BaseModel):
    """咨询师信息实体"""
    __tablename__ = 'counselors'

    id = Column(String(50), primary_key=True)  # 咨询师ID
    name = Column(String(100), nullable=False)  # 咨询师姓名
    avatar = Column(String(255))  # 头像URL
    title = Column(String(100))  # 职称
    phone = Column(String(20))  # 手机号
    email = Column(String(100))  # 邮箱
    tags_json = Column(Text)  # 专业领域标签（JSON格式存储）
    specialty = Column(Text)  # 专业领域描述
    bio = Column(Text)  # 个人简介
    price = Column(Float, default=0.0)  # 咨询价格（每小时）
    rating = Column(Float, default=0.0)  # 评分
    consultation_count = Column(Integer, default=0)  # 咨询次数
    introduction = Column(Text)  # 简介
    status = Column(Integer, default=1)  # 状态（0-离职，1-在职）

    @property
    def tags(self) -> List[str]:
        """获取专业领域标签列表"""
        if self.tags_json:
            return json.loads(self.tags_json)
        return []

    @tags.setter
    def tags(self, value: List[str]):
        """设置专业领域标签列表"""
        self.tags_json = json.dumps(value) if value else None

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'avatar': process_image_url(self.avatar),
            'title': self.title,
            'phone': self.phone,
            'code': self.email,
            'tags': self.tags,
            'specialty': self.specialty,
            'bio': self.bio,
            'price': self.price,
            'rating': self.rating,
            'consultation_count': self.consultation_count,
            'introduction': self.introduction,
            'status': self.status,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
