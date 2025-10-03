from wtforms import StringField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from pcf_flask_helper.form.base import BaseForm


class GroupQueryForm(BaseForm):
    page = IntegerField(validators=[Optional(), NumberRange(min=1, message='页码必须大于等于1')])
    per_page = IntegerField(validators=[Optional(), NumberRange(min=1, message='每页数量必须大于等于1')])
    title = StringField(validators=[Optional(), Length(max=200, message='群组标题长度不能超过200个字符')])

class GroupCreateForm(BaseForm):
    title = StringField(validators=[DataRequired(message='群组标题不能为空'), Length(max=200, message='群组标题长度不能超过200个字符')])
    cover_image = StringField(validators=[Optional(), Length(max=255, message='封面图片URL长度不能超过255个字符')])
    counselor_id = StringField(validators=[DataRequired(message='导师ID不能为空'), Length(max=50, message='导师ID长度不能超过50个字符')])
    counselor_name = StringField(validators=[DataRequired(message='导师姓名不能为空'), Length(max=100, message='导师姓名长度不能超过100个字符')])
    price = FloatField(validators=[Optional(), NumberRange(min=0, message='价格必须大于等于0')])
    capacity = IntegerField(validators=[Optional(), NumberRange(min=1, message='人数容量必须大于等于1')])
    location = StringField(validators=[Optional(), Length(max=200, message='地点长度不能超过200个字符')])
    city = StringField(validators=[Optional(), Length(max=100, message='城市长度不能超过100个字符')])
    type = SelectField(validators=[Optional()], choices=[('online', '线上'), ('offline', '线下')])
    start_date = StringField(validators=[Optional(), Length(max=20, message='开始日期长度不能超过20个字符')])
    duration = StringField(validators=[Optional(), Length(max=100, message='持续时间长度不能超过100个字符')])
    schedule = StringField(validators=[Optional(), Length(max=200, message='时间安排长度不能超过200个字符')])
    description = StringField(validators=[Optional(), Length(max=500, message='描述长度不能超过500个字符')])
    status = IntegerField(validators=[Optional(), NumberRange(min=0, max=2, message='状态值必须在0-2之间')])


class GroupUpdateForm(BaseForm):
    title = StringField(validators=[Optional(), Length(max=200, message='群组标题长度不能超过200个字符')])
    cover_image = StringField(validators=[Optional(), Length(max=255, message='封面图片URL长度不能超过255个字符')])
    counselor_id = StringField(validators=[Optional(), Length(max=50, message='导师ID长度不能超过50个字符')])
    counselor_name = StringField(validators=[Optional(), Length(max=100, message='导师姓名长度不能超过100个字符')])
    price = FloatField(validators=[Optional(), NumberRange(min=0, message='价格必须大于等于0')])
    capacity = IntegerField(validators=[Optional(), NumberRange(min=1, message='人数容量必须大于等于1')])
    location = StringField(validators=[Optional(), Length(max=200, message='地点长度不能超过200个字符')])
    city = StringField(validators=[Optional(), Length(max=100, message='城市长度不能超过100个字符')])
    type = SelectField(validators=[Optional()], choices=[('online', '线上'), ('offline', '线下')])
    start_date = StringField(validators=[Optional(), Length(max=20, message='开始日期长度不能超过20个字符')])
    duration = StringField(validators=[Optional(), Length(max=100, message='持续时间长度不能超过100个字符')])
    schedule = StringField(validators=[Optional(), Length(max=200, message='时间安排长度不能超过200个字符')])
    description = StringField(validators=[Optional(), Length(max=500, message='描述长度不能超过500个字符')])
    status = IntegerField(validators=[Optional(), NumberRange(min=0, max=2, message='状态值必须在0-2之间')])