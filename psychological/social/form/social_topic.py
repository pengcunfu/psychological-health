from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Optional, Length, NumberRange
from pcf_flask_helper.form.base import BaseForm


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
