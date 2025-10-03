from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SelectField, FieldList
from wtforms.validators import DataRequired, Optional, Length
from pcf_flask_helper.form.base import BaseForm


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
