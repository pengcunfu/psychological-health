import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, UniqueConstraint
from pcf_flask_helper.model.base import BaseModel


class SocialFollow(BaseModel):
    """社区用户关注"""
    __tablename__ = 'social_follows'

    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    follower_id = Column(String(50), nullable=False, comment='关注者用户ID')
    following_id = Column(String(50), nullable=False, comment='被关注者用户ID')

    # 关注状态
    status = Column(String(20), default='active', comment='状态：active有效，cancelled已取消')

    # 关注类型（可扩展）
    follow_type = Column(String(20), default='normal', comment='关注类型：normal普通关注，mutual互相关注')

    # 关注来源
    source = Column(String(50), comment='关注来源：profile个人主页，post帖子，search搜索，recommend推荐')

    # 添加唯一约束，防止重复关注
    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='unique_user_follow'),
    )

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'follower_id': self.follower_id,
            'following_id': self.following_id,
            'status': self.status,
            'follow_type': self.follow_type,
            'source': self.source,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }

    def cancel(self):
        """取消关注"""
        self.status = 'cancelled'

    def reactivate(self):
        """重新激活关注"""
        self.status = 'active'

    def is_active(self):
        """判断关注是否有效"""
        return self.status == 'active'


class UserSocialStats(BaseModel):
    """用户社区统计"""
    __tablename__ = 'user_social_stats'

    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), nullable=False, unique=True, comment='用户ID')

    # 发布统计
    post_count = Column(Integer, default=0, comment='发布帖子数')
    comment_count = Column(Integer, default=0, comment='评论数')

    # 互动统计
    like_received_count = Column(Integer, default=0, comment='收到的点赞数')
    like_given_count = Column(Integer, default=0, comment='给出的点赞数')

    # 关注统计
    follower_count = Column(Integer, default=0, comment='粉丝数')
    following_count = Column(Integer, default=0, comment='关注数')

    # 浏览统计
    profile_view_count = Column(Integer, default=0, comment='个人主页浏览次数')
    total_view_count = Column(Integer, default=0, comment='帖子总浏览次数')

    # 活跃度评分
    activity_score = Column(Integer, default=0, comment='活跃度评分')

    # 等级系统（可选）
    level = Column(Integer, default=1, comment='用户等级')
    experience = Column(Integer, default=0, comment='经验值')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_count': self.post_count,
            'comment_count': self.comment_count,
            'like_received_count': self.like_received_count,
            'like_given_count': self.like_given_count,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'profile_view_count': self.profile_view_count,
            'total_view_count': self.total_view_count,
            'activity_score': self.activity_score,
            'level': self.level,
            'experience': self.experience,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }

    def increment_post(self):
        """增加帖子数"""
        self.post_count = (self.post_count or 0) + 1
        self.add_experience(10)  # 发帖获得10经验

    def decrement_post(self):
        """减少帖子数"""
        self.post_count = max((self.post_count or 0) - 1, 0)

    def increment_comment(self):
        """增加评论数"""
        self.comment_count = (self.comment_count or 0) + 1
        self.add_experience(5)  # 评论获得5经验

    def decrement_comment(self):
        """减少评论数"""
        self.comment_count = max((self.comment_count or 0) - 1, 0)

    def increment_like_received(self):
        """增加收到点赞数"""
        self.like_received_count = (self.like_received_count or 0) + 1
        self.add_experience(2)  # 收到点赞获得2经验

    def decrement_like_received(self):
        """减少收到点赞数"""
        self.like_received_count = max((self.like_received_count or 0) - 1, 0)

    def increment_like_given(self):
        """增加给出点赞数"""
        self.like_given_count = (self.like_given_count or 0) + 1
        self.add_experience(1)  # 给出点赞获得1经验

    def decrement_like_given(self):
        """减少给出点赞数"""
        self.like_given_count = max((self.like_given_count or 0) - 1, 0)

    def increment_follower(self):
        """增加粉丝数"""
        self.follower_count = (self.follower_count or 0) + 1
        self.add_experience(15)  # 获得粉丝获得15经验

    def decrement_follower(self):
        """减少粉丝数"""
        self.follower_count = max((self.follower_count or 0) - 1, 0)

    def increment_following(self):
        """增加关注数"""
        self.following_count = (self.following_count or 0) + 1

    def decrement_following(self):
        """减少关注数"""
        self.following_count = max((self.following_count or 0) - 1, 0)

    def increment_profile_view(self):
        """增加个人主页浏览次数"""
        self.profile_view_count = (self.profile_view_count or 0) + 1

    def add_view_count(self, count):
        """增加总浏览次数"""
        self.total_view_count = (self.total_view_count or 0) + count

    def add_experience(self, exp):
        """增加经验值并检查升级"""
        self.experience = (self.experience or 0) + exp
        self.check_level_up()

    def check_level_up(self):
        """检查是否可以升级"""
        # 简单的升级规则：每1000经验升一级
        new_level = (self.experience // 1000) + 1
        if new_level > self.level:
            self.level = new_level

    def update_activity_score(self):
        """更新活跃度评分"""
        # 简单的活跃度计算
        post_score = (self.post_count or 0) * 10
        comment_score = (self.comment_count or 0) * 5
        like_score = (self.like_received_count or 0) * 2
        follower_score = (self.follower_count or 0) * 3

        self.activity_score = post_score + comment_score + like_score + follower_score
