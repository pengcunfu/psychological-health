from typing import List
import json
from sqlalchemy import Column, String, Integer, DateTime, Float, Text, func
from pcf_flask_helper.model.base import BaseModel


class Course(BaseModel):
    """课程信息实体"""
    __tablename__ = 'courses'

    id = Column(String(50), primary_key=True)  # 课程ID
    title = Column(String(200), nullable=False)  # 课程标题
    subtitle = Column(String(300))  # 课程副标题
    cover_image = Column(String(255))  # 课程封面图片URL
    teacher = Column(String(100), nullable=False)  # 教师姓名
    teacher_title = Column(String(100))  # 教师职称
    teacher_avatar = Column(String(255))  # 教师头像URL
    price = Column(Float, default=0.0)  # 课程现价
    original_price = Column(Float, default=0.0)  # 课程原价
    lesson_count = Column(Integer, default=0)  # 课时数量
    student_count = Column(Integer, default=0)  # 学生数量
    rating = Column(Float, default=0.0)  # 课程评分
    duration = Column(Integer, default=60)  # 课程时长（分钟）
    status = Column(String(20), default='draft')  # 课程状态：draft草稿，published已发布，archived已归档
    _tags = Column('tags', Text)  # 课程标签列表（JSON存储）
    description = Column(Text)  # 课程描述
    content = Column(Text)  # 课程详细内容

    @property
    def tags(self) -> List[str]:
        """获取标签列表"""
        if self._tags:
            return json.loads(self._tags)
        return []

    @tags.setter
    def tags(self, value: List[str]):
        """设置标签列表"""
        self._tags = json.dumps(value) if value else None

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'cover_image': self.cover_image,
            'teacher': self.teacher,
            'teacher_title': self.teacher_title,
            'teacher_avatar': self.teacher_avatar,
            'price': self.price,
            'original_price': self.original_price,
            'lesson_count': self.lesson_count,
            'student_count': self.student_count,
            'rating': self.rating,
            'duration': self.duration,
            'status': self.status,
            'tags': self.tags,
            'description': self.description,
            'content': self.content,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
