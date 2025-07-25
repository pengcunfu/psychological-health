from wtforms import StringField, IntegerField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from .base import BaseForm


class CourseQueryForm(BaseForm):
    page = IntegerField(validators=[Optional(), NumberRange(min=1, message='页码必须大于等于1')])
    per_page = IntegerField(validators=[Optional(), NumberRange(min=1, message='每页数量必须大于等于1')])
    title = StringField(validators=[Optional(), Length(max=100, message='标题长度不能超过100个字符')])


class CourseCreateForm(BaseForm):
    title = StringField(validators=[DataRequired(message='标题不能为空'), Length(max=100, message='标题长度不能超过100个字符')])
    description = TextAreaField(validators=[Optional(), Length(max=500, message='描述长度不能超过500个字符')])
    price = DecimalField(validators=[DataRequired(message='价格不能为空'), NumberRange(min=0, message='价格不能为负数')])
    score = DecimalField(validators=[Optional(), NumberRange(min=0, max=5, message='评分必须在0到5之间')])
    cover_image = StringField(validators=[Optional(), Length(max=255, message='封面图片路径长度不能超过255个字符')])
    video_url = StringField(validators=[Optional(), Length(max=255, message='视频链接长度不能超过255个字符')])
    category_id = IntegerField(validators=[DataRequired(message='分类ID不能为空'), NumberRange(min=1, message='分类ID必须大于等于1')])
    counselor_id = IntegerField(validators=[DataRequired(message='咨询师ID不能为空'), NumberRange(min=1, message='咨询师ID必须大于等于1')])


class CourseUpdateForm(BaseForm):
    title = StringField(validators=[Optional(), Length(max=100, message='标题长度不能超过100个字符')])
    description = TextAreaField(validators=[Optional(), Length(max=500, message='描述长度不能超过500个字符')])
    price = DecimalField(validators=[Optional(), NumberRange(min=0, message='价格不能为负数')])
    score = DecimalField(validators=[Optional(), NumberRange(min=0, max=5, message='评分必须在0到5之间')])
    cover_image = StringField(validators=[Optional(), Length(max=255, message='封面图片路径长度不能超过255个字符')])
    video_url = StringField(validators=[Optional(), Length(max=255, message='视频链接长度不能超过255个字符')])
    category_id = IntegerField(validators=[Optional(), NumberRange(min=1, message='分类ID必须大于等于1')])
    counselor_id = IntegerField(validators=[Optional(), NumberRange(min=1, message='咨询师ID必须大于等于1')])