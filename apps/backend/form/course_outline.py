from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from .base import BaseForm


class CourseOutlineQueryForm(BaseForm):
    course_id = StringField(validators=[DataRequired(message='课程ID不能为空'), Length(max=50, message='课程ID长度不能超过50个字符')])


class CourseOutlineCreateForm(BaseForm):
    course_id = StringField(validators=[DataRequired(message='课程ID不能为空'), Length(max=50, message='课程ID长度不能超过50个字符')])
    title = StringField(validators=[DataRequired(message='标题不能为空'), Length(max=100, message='标题长度不能超过100个字符')])
    content = StringField(validators=[DataRequired(message='内容不能为空')])
    sort_order = IntegerField(validators=[Optional(), NumberRange(min=0, message='排序值不能小于0')])


class CourseOutlineUpdateForm(BaseForm):
    title = StringField(validators=[Optional(), Length(max=100, message='标题长度不能超过100个字符')])
    content = StringField(validators=[Optional()])
    sort_order = IntegerField(validators=[Optional(), NumberRange(min=0, message='排序值不能小于0')])