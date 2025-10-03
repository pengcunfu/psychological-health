import uuid
import json
from datetime import datetime
from typing import List
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, Float
from .base import BaseModel


class SocialPost(BaseModel):
    """社区帖子"""
    __tablename__ = 'social_posts'
    
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), nullable=False, comment='发布用户ID')
    title = Column(String(200), comment='帖子标题（可为空，纯内容帖子）')
    content = Column(Text, nullable=False, comment='帖子内容')
    category = Column(String(50), comment='帖子分类：心理健康、经验分享、情感倾诉等')
    
    # 话题标签
    _topics = Column('topics', Text, comment='关联话题列表（JSON存储）')
    
    # 媒体内容
    _images = Column('images', Text, comment='图片列表（JSON存储）')
    _videos = Column('videos', Text, comment='视频列表（JSON存储）')
    
    # 状态和属性
    status = Column(String(20), default='published', comment='状态：draft草稿，published已发布，hidden隐藏，deleted已删除')
    is_top = Column(Boolean, default=False, comment='是否置顶')
    is_featured = Column(Boolean, default=False, comment='是否精选')
    is_anonymous = Column(Boolean, default=False, comment='是否匿名发布')
    
    # 统计数据
    view_count = Column(Integer, default=0, comment='浏览次数')
    like_count = Column(Integer, default=0, comment='点赞数')
    comment_count = Column(Integer, default=0, comment='评论数')
    share_count = Column(Integer, default=0, comment='分享数')
    collect_count = Column(Integer, default=0, comment='收藏数')
    
    # 位置信息（可选）
    location = Column(String(200), comment='发布位置')
    
    # 审核信息
    audit_status = Column(String(20), default='approved', comment='审核状态：pending待审核，approved通过，rejected拒绝')
    audit_reason = Column(Text, comment='审核原因')
    audited_by = Column(String(50), comment='审核人ID')
    audited_at = Column(DateTime, comment='审核时间')
    
    # 热度评分（用于推荐算法）
    hot_score = Column(Float, default=0.0, comment='热度评分')
    
    @property
    def topics(self) -> List[str]:
        """获取话题列表"""
        if self._topics:
            return json.loads(self._topics)
        return []
    
    @topics.setter
    def topics(self, value: List[str]):
        """设置话题列表"""
        self._topics = json.dumps(value) if value else None
    
    @property
    def images(self) -> List[str]:
        """获取图片列表"""
        if self._images:
            return json.loads(self._images)
        return []
    
    @images.setter
    def images(self, value: List[str]):
        """设置图片列表"""
        self._images = json.dumps(value) if value else None
    
    @property
    def videos(self) -> List[str]:
        """获取视频列表"""
        if self._videos:
            return json.loads(self._videos)
        return []
    
    @videos.setter
    def videos(self, value: List[str]):
        """设置视频列表"""
        self._videos = json.dumps(value) if value else None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'topics': self.topics,
            'images': self.images,
            'videos': self.videos,
            'status': self.status,
            'is_top': self.is_top,
            'is_featured': self.is_featured,
            'is_anonymous': self.is_anonymous,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'share_count': self.share_count,
            'collect_count': self.collect_count,
            'location': self.location,
            'audit_status': self.audit_status,
            'audit_reason': self.audit_reason,
            'audited_by': self.audited_by,
            'audited_at': self.audited_at.isoformat() if self.audited_at else None,
            'hot_score': self.hot_score,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
    
    def to_list_dict(self):
        """列表页使用的简化字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content[:200] + '...' if len(self.content or '') > 200 else self.content,  # 截取前200字符
            'category': self.category,
            'topics': self.topics,
            'images': self.images[:3],  # 最多显示3张图片
            'is_top': self.is_top,
            'is_featured': self.is_featured,
            'is_anonymous': self.is_anonymous,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'view_count': self.view_count,
            'hot_score': self.hot_score,
            'create_time': self.create_time.isoformat() if self.create_time else None
        }
    
    def increment_view(self):
        """增加浏览次数"""
        self.view_count = (self.view_count or 0) + 1
    
    def increment_like(self):
        """增加点赞数"""
        self.like_count = (self.like_count or 0) + 1
    
    def decrement_like(self):
        """减少点赞数"""
        self.like_count = max((self.like_count or 0) - 1, 0)
    
    def increment_comment(self):
        """增加评论数"""
        self.comment_count = (self.comment_count or 0) + 1
    
    def decrement_comment(self):
        """减少评论数"""
        self.comment_count = max((self.comment_count or 0) - 1, 0)
    
    def update_hot_score(self):
        """更新热度评分（可以根据算法调整）"""
        # 简单的热度计算：点赞*2 + 评论*3 + 浏览*0.1 + 分享*5
        like_score = (self.like_count or 0) * 2
        comment_score = (self.comment_count or 0) * 3
        view_score = (self.view_count or 0) * 0.1
        share_score = (self.share_count or 0) * 5
        
        # 时间衰减因子（帖子越新，热度加成越高）
        if self.create_time:
            hours_passed = (datetime.now() - self.create_time).total_seconds() / 3600
            time_factor = max(1 - hours_passed / (24 * 7), 0.1)  # 7天内衰减到0.1
        else:
            time_factor = 0.1
        
        self.hot_score = (like_score + comment_score + view_score + share_score) * time_factor 