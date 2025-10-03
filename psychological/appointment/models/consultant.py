from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import uuid
import enum

from pcf_flask_helper.model.base import BaseModel


class GenderEnum(enum.Enum):
    """性别枚举"""
    MALE = "male"
    FEMALE = "female"


class RelationshipEnum(enum.Enum):
    """关系枚举"""
    SELF = "self"  # 本人
    SPOUSE = "spouse"  # 配偶
    CHILD = "child"  # 子女
    PARENT = "parent"  # 父母
    SIBLING = "sibling"  # 兄弟姐妹
    FRIEND = "friend"  # 朋友
    OTHER = "other"  # 其他


class Consultant(BaseModel):
    """咨询人信息模型"""
    __tablename__ = 'consultants'
    
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), ForeignKey('users.id'), nullable=True, comment='用户ID')
    
    # 基本信息
    real_name = Column(String(50), nullable=False, comment='真实姓名')
    birth_year = Column(Integer, nullable=True, comment='出生年份')
    birth_month = Column(Integer, nullable=True, comment='出生月份')
    gender = Column(Enum(GenderEnum), nullable=False, comment='性别')
    phone = Column(String(20), nullable=False, comment='联系方式')
    
    # 紧急联系人信息
    emergency_name = Column(String(50), nullable=False, comment='紧急联系人姓名')
    emergency_relationship = Column(Enum(RelationshipEnum), nullable=False, comment='与紧急联系人的关系')
    emergency_phone = Column(String(20), nullable=False, comment='紧急联系人电话')
    
    # 其他信息
    notes = Column(Text, nullable=True, comment='备注信息')
    is_default = Column(Integer, default=0, comment='是否为默认咨询人(0-否, 1-是)')
    status = Column(Integer, default=1, comment='状态(0-禁用, 1-启用)')
    
    # 时间戳
    create_time = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    user = relationship("User", back_populates="consultants")
    appointments = relationship("Appointment", back_populates="consultant")
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'real_name': self.real_name,
            'birth_year': self.birth_year,
            'birth_month': self.birth_month,
            'birth_date': f"{self.birth_year}年{self.birth_month}月" if self.birth_year and self.birth_month else None,
            'gender': self.gender.value if self.gender else None,
            'gender_text': '男' if self.gender == GenderEnum.MALE else '女' if self.gender == GenderEnum.FEMALE else None,
            'phone': self.phone,
            'emergency_name': self.emergency_name,
            'emergency_relationship': self.emergency_relationship.value if self.emergency_relationship else None,
            'emergency_relationship_text': self._get_relationship_text(self.emergency_relationship),
            'emergency_phone': self.emergency_phone,
            'notes': self.notes,
            'is_default': self.is_default,
            'status': self.status,
            'status_text': '启用' if self.status == 1 else '禁用',
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        }
    
    def _get_relationship_text(self, relationship):
        """获取关系文本"""
        relationship_map = {
            RelationshipEnum.SELF: '本人',
            RelationshipEnum.SPOUSE: '配偶',
            RelationshipEnum.CHILD: '子女',
            RelationshipEnum.PARENT: '父母',
            RelationshipEnum.SIBLING: '兄弟姐妹',
            RelationshipEnum.FRIEND: '朋友',
            RelationshipEnum.OTHER: '其他'
        }
        return relationship_map.get(relationship, '未知')
    
    def __repr__(self):
        return f'<Consultant {self.real_name}>'
