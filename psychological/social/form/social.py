from wtforms import StringField, IntegerField, FloatField, TextAreaField, BooleanField, SelectField, FieldList
from wtforms.validators import DataRequired, Optional, Length, NumberRange
from .base import BaseForm


# 话题相关表单
class SocialTopicQueryForm(BaseForm):
    """话题查询表单"""
    page = IntegerField('页码', [Optional()], default=1)
    per_page = IntegerField('每页数量', [Optional()], default=20)
    name = StringField('话题名称', [Optional()])
    status = SelectField('状态', [Optional()], choices=[
        ('', '全部'),
        ('active', '启用'),
        ('inactive', '禁用')
    ], default='')
    is_hot = BooleanField('是否热门', [Optional()])
    is_featured = BooleanField('是否精选', [Optional()])
    keyword = StringField('搜索关键词', [Optional()])
    sort_by = StringField('排序字段', [Optional()], default='sort_order')
    sort_order = StringField('排序方向', [Optional()], default='desc')


class SocialTopicCreateForm(BaseForm):
    """话题创建表单"""
    name = StringField('话题名称', [DataRequired(), Length(1, 100)])
    description = TextAreaField('话题描述', [Optional()])
    cover_image = StringField('封面图片', [Optional(), Length(max=255)])
    color = StringField('话题颜色', [Optional(), Length(max=20)])
    sort_order = IntegerField('排序权重', [Optional(), NumberRange(min=0)])
    is_hot = BooleanField('是否热门', [Optional()])
    is_featured = BooleanField('是否精选', [Optional()])
    status = SelectField('状态', [Optional()], choices=[
        ('active', '启用'),
        ('inactive', '禁用')
    ], default='active')


class SocialTopicUpdateForm(BaseForm):
    """话题更新表单"""
    name = StringField('话题名称', [Optional(), Length(1, 100)])
    description = TextAreaField('话题描述', [Optional()])
    cover_image = StringField('封面图片', [Optional(), Length(max=255)])
    color = StringField('话题颜色', [Optional(), Length(max=20)])
    sort_order = IntegerField('排序权重', [Optional(), NumberRange(min=0)])
    is_hot = BooleanField('是否热门', [Optional()])
    is_featured = BooleanField('是否精选', [Optional()])
    status = SelectField('状态', [Optional()], choices=[
        ('active', '启用'),
        ('inactive', '禁用')
    ])


# 帖子相关表单
class SocialPostQueryForm(BaseForm):
    """帖子查询表单"""
    page = IntegerField('页码', [Optional()], default=1)
    per_page = IntegerField('每页数量', [Optional()], default=10)
    user_id = StringField('用户ID', [Optional()])
    category = StringField('分类', [Optional()])
    status = SelectField('状态', [Optional()], choices=[
        ('', '全部'),
        ('draft', '草稿'),
        ('published', '已发布'),
        ('hidden', '隐藏'),
        ('deleted', '已删除')
    ], default='')
    audit_status = SelectField('审核状态', [Optional()], choices=[
        ('', '全部'),
        ('pending', '待审核'),
        ('approved', '通过'),
        ('rejected', '拒绝')
    ], default='')
    is_top = BooleanField('是否置顶', [Optional()])
    is_featured = BooleanField('是否精选', [Optional()])
    topic = StringField('话题', [Optional()])
    keyword = StringField('搜索关键词', [Optional()])
    start_date = StringField('开始日期', [Optional()])
    end_date = StringField('结束日期', [Optional()])
    sort_by = StringField('排序字段', [Optional()], default='create_time')
    sort_order = StringField('排序方向', [Optional()], default='desc')


class SocialPostCreateForm(BaseForm):
    """帖子创建表单"""
    title = StringField('标题', [Optional(), Length(max=200)])
    content = TextAreaField('内容', [DataRequired()])
    category = StringField('分类', [Optional(), Length(max=50)])
    topics = FieldList(StringField('话题', [Length(max=50)]), min_entries=0)
    images = FieldList(StringField('图片', [Length(max=255)]), min_entries=0)
    videos = FieldList(StringField('视频', [Length(max=255)]), min_entries=0)
    location = StringField('位置', [Optional(), Length(max=200)])
    is_anonymous = BooleanField('是否匿名', [Optional()], default=False)
    is_draft = BooleanField('是否草稿', [Optional()], default=False)


class SocialPostUpdateForm(BaseForm):
    """帖子更新表单"""
    title = StringField('标题', [Optional(), Length(max=200)])
    content = TextAreaField('内容', [Optional()])
    category = StringField('分类', [Optional(), Length(max=50)])
    topics = FieldList(StringField('话题', [Length(max=50)]), min_entries=0)
    images = FieldList(StringField('图片', [Length(max=255)]), min_entries=0)
    videos = FieldList(StringField('视频', [Length(max=255)]), min_entries=0)
    location = StringField('位置', [Optional(), Length(max=200)])
    status = SelectField('状态', [Optional()], choices=[
        ('draft', '草稿'),
        ('published', '已发布'),
        ('hidden', '隐藏'),
        ('deleted', '已删除')
    ])
    is_top = BooleanField('是否置顶', [Optional()])
    is_featured = BooleanField('是否精选', [Optional()])
    audit_status = SelectField('审核状态', [Optional()], choices=[
        ('pending', '待审核'),
        ('approved', '通过'),
        ('rejected', '拒绝')
    ])
    audit_reason = TextAreaField('审核原因', [Optional()])


# 评论相关表单
class SocialCommentQueryForm(BaseForm):
    """评论查询表单"""
    page = IntegerField('页码', [Optional()], default=1)
    per_page = IntegerField('每页数量', [Optional()], default=20)
    post_id = StringField('帖子ID', [Optional()])
    user_id = StringField('用户ID', [Optional()])
    parent_id = StringField('父评论ID', [Optional()])
    status = SelectField('状态', [Optional()], choices=[
        ('', '全部'),
        ('published', '已发布'),
        ('hidden', '隐藏'),
        ('deleted', '已删除')
    ], default='')
    audit_status = SelectField('审核状态', [Optional()], choices=[
        ('', '全部'),
        ('pending', '待审核'),
        ('approved', '通过'),
        ('rejected', '拒绝')
    ], default='')
    keyword = StringField('搜索关键词', [Optional()])
    sort_by = StringField('排序字段', [Optional()], default='create_time')
    sort_order = StringField('排序方向', [Optional()], default='desc')


class SocialCommentCreateForm(BaseForm):
    """评论创建表单"""
    post_id = StringField('帖子ID', [DataRequired(), Length(1, 50)])
    content = TextAreaField('评论内容', [DataRequired()])
    parent_id = StringField('父评论ID', [Optional(), Length(1, 50)])
    reply_to_user_id = StringField('回复用户ID', [Optional(), Length(1, 50)])
    images = FieldList(StringField('图片', [Length(max=255)]), min_entries=0)
    location = StringField('位置', [Optional(), Length(max=200)])
    is_anonymous = BooleanField('是否匿名', [Optional()], default=False)


class SocialCommentUpdateForm(BaseForm):
    """评论更新表单"""
    content = TextAreaField('评论内容', [Optional()])
    images = FieldList(StringField('图片', [Length(max=255)]), min_entries=0)
    status = SelectField('状态', [Optional()], choices=[
        ('published', '已发布'),
        ('hidden', '隐藏'),
        ('deleted', '已删除')
    ])
    audit_status = SelectField('审核状态', [Optional()], choices=[
        ('pending', '待审核'),
        ('approved', '通过'),
        ('rejected', '拒绝')
    ])
    audit_reason = TextAreaField('审核原因', [Optional()])


# 点赞相关表单
class SocialLikeCreateForm(BaseForm):
    """点赞创建表单"""
    target_id = StringField('目标ID', [DataRequired(), Length(1, 50)])
    target_type = SelectField('目标类型', [DataRequired()], choices=[
        ('post', '帖子'),
        ('comment', '评论')
    ])


# 关注相关表单
class SocialFollowCreateForm(BaseForm):
    """关注创建表单"""
    following_id = StringField('被关注用户ID', [DataRequired(), Length(1, 50)])
    source = StringField('关注来源', [Optional(), Length(max=50)])


class SocialFollowQueryForm(BaseForm):
    """关注查询表单"""
    page = IntegerField('页码', [Optional()], default=1)
    per_page = IntegerField('每页数量', [Optional()], default=20)
    follower_id = StringField('关注者ID', [Optional()])
    following_id = StringField('被关注者ID', [Optional()])
    status = SelectField('状态', [Optional()], choices=[
        ('', '全部'),
        ('active', '有效'),
        ('cancelled', '已取消')
    ], default='active')
    follow_type = SelectField('关注类型', [Optional()], choices=[
        ('', '全部'),
        ('normal', '普通关注'),
        ('mutual', '互相关注')
    ], default='')
    source = StringField('关注来源', [Optional()]) 