from sqlalchemy import Column, String
from pcf_flask_helper.model.base import BaseModel


class DiseaseTags(BaseModel):
    """疾病标签实体"""
    __tablename__ = 'disease_tags'
    
    id = Column(String(50), primary_key=True)  # 标签ID
    name = Column(String(100), nullable=False)  # 标签名称
    description = Column(String(500))  # 标签描述

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }