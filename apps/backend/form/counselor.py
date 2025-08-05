from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired, Optional, Length, NumberRange
from .base import BaseForm


class CounselorQueryForm(BaseForm):
    """咨询师查询表单"""
    page = IntegerField('页码', [Optional()], default=1)
    per_page = IntegerField('每页数量', [Optional()], default=10)
    name = StringField('咨询师姓名', [Optional()])
    title = StringField('职称', [Optional()])
    keyword = StringField('搜索关键词', [Optional()])
    sort_by = StringField('排序字段', [Optional()], default='create_time')
    sort_order = StringField('排序方向', [Optional()], default='desc')
    status = IntegerField('状态', [Optional()])


class CounselorCreateForm(BaseForm):
    name = StringField('姓名', validators=[DataRequired(message='姓名不能为空'),
                                           Length(max=100, message='姓名长度不能超过100个字符')])
    avatar = StringField('头像', validators=[Optional(), Length(max=255, message='头像URL长度不能超过255个字符')])
    title = StringField('职称', validators=[Optional(), Length(max=100, message='职称长度不能超过100个字符')])
    price = FloatField('价格', validators=[Optional(), NumberRange(min=0, message='价格不能为负数')])
    rating = FloatField('评分', validators=[Optional(), NumberRange(min=0, max=5, message='评分必须在0到5之间')])
    consultation_count = IntegerField('咨询次数',
                                      validators=[Optional(), NumberRange(min=0, message='咨询次数不能为负数')])
    introduction = StringField('介绍', validators=[Optional()])
    tags = StringField('标签', validators=[Optional()])


class CounselorUpdateForm(BaseForm):
    name = StringField('姓名', validators=[Optional(), Length(max=100, message='姓名长度不能超过100个字符')])
    avatar = StringField('头像', validators=[Optional(), Length(max=255, message='头像URL长度不能超过255个字符')])
    title = StringField('职称', validators=[Optional(), Length(max=100, message='职称长度不能超过100个字符')])
    price = FloatField('价格', validators=[Optional(), NumberRange(min=0, message='价格不能为负数')])
    rating = FloatField('评分', validators=[Optional(), NumberRange(min=0, max=5, message='评分必须在0到5之间')])
    consultation_count = IntegerField('咨询次数',
                                      validators=[Optional(), NumberRange(min=0, message='咨询次数不能为负数')])
    introduction = StringField('介绍', validators=[Optional()])
    tags = StringField('标签', validators=[Optional()])
    status = IntegerField('状态', validators=[Optional()])
