from .base import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, Text, func


class CourseOutline(BaseModel):
    """课程大纲实体"""
    __tablename__ = 'course_outlines'

    course_id = Column(String(50), nullable=False)  # 课程ID
    title = Column(String(200), nullable=False)  # 章节标题
    content = Column(Text)  # 章节内容
    video_url = Column(String(500))  # 视频链接
    sort_order = Column(Integer, default=0)  # 排序序号

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'content': self.content,
            'video_url': self.video_url,
            'sort_order': self.sort_order,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }

