from wtforms import StringField, IntegerField, TextAreaField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, AnyOf
from pcf_flask_helper.form.base import BaseForm


class CourseQueryForm(BaseForm):
    page = IntegerField(validators=[Optional(), NumberRange(min=1, message='页码必须大于等于1')])
    per_page = IntegerField(validators=[Optional(), NumberRange(min=1, message='每页数量必须大于等于1')])
    title = StringField(validators=[Optional(), Length(max=100, message='标题长度不能超过100个字符')])
    status = StringField(validators=[Optional(), AnyOf(['draft', 'published', 'archived'], message='状态值无效')])


class CourseCreateForm(BaseForm):
    title = StringField(
        validators=[DataRequired(message='标题不能为空'), Length(max=200, message='标题长度不能超过200个字符')])
    subtitle = StringField(validators=[Optional(), Length(max=300, message='副标题长度不能超过300个字符')])
    description = TextAreaField(validators=[Optional(), Length(max=1000, message='描述长度不能超过1000个字符')])
    content = TextAreaField(validators=[Optional(), Length(max=5000, message='内容长度不能超过5000个字符')])
    price = DecimalField(
        validators=[DataRequired(message='价格不能为空'), NumberRange(min=0, message='价格不能为负数')])
    duration = IntegerField(validators=[Optional(), NumberRange(min=1, message='课程时长必须大于0分钟')])
    status = StringField(validators=[Optional(), AnyOf(['draft', 'published', 'archived'], message='状态值无效')])
    cover_image = StringField(validators=[Optional(), Length(max=255, message='封面图片路径长度不能超过255个字符')])
    teacher = StringField(validators=[Optional(), Length(max=100, message='教师姓名长度不能超过100个字符')])
    teacher_title = StringField(validators=[Optional(), Length(max=100, message='教师职称长度不能超过100个字符')])
    teacher_avatar = StringField(validators=[Optional(), Length(max=255, message='教师头像路径长度不能超过255个字符')])
    tags = StringField(validators=[Optional()])  # 标签以JSON字符串形式传递


class CourseUpdateForm(BaseForm):
    title = StringField(validators=[Optional(), Length(max=200, message='标题长度不能超过200个字符')])
    subtitle = StringField(validators=[Optional(), Length(max=300, message='副标题长度不能超过300个字符')])
    description = TextAreaField(validators=[Optional(), Length(max=1000, message='描述长度不能超过1000个字符')])
    content = TextAreaField(validators=[Optional(), Length(max=5000, message='内容长度不能超过5000个字符')])
    price = DecimalField(validators=[Optional(), NumberRange(min=0, message='价格不能为负数')])
    duration = IntegerField(validators=[Optional(), NumberRange(min=1, message='课程时长必须大于0分钟')])
    status = StringField(validators=[Optional(), AnyOf(['draft', 'published', 'archived'], message='状态值无效')])
    cover_image = StringField(validators=[Optional(), Length(max=255, message='封面图片路径长度不能超过255个字符')])
    teacher = StringField(validators=[Optional(), Length(max=100, message='教师姓名长度不能超过100个字符')])
    teacher_title = StringField(validators=[Optional(), Length(max=100, message='教师职称长度不能超过100个字符')])
    teacher_avatar = StringField(validators=[Optional(), Length(max=255, message='教师头像路径长度不能超过255个字符')])
    tags = StringField(validators=[Optional()])  # 标签以JSON字符串形式传递
