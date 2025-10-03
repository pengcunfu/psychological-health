from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SelectField, FieldList
from wtforms.validators import DataRequired, Optional, Length
from pcf_flask_helper.form.base import BaseForm


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
