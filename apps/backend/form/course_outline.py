from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from .base import BaseForm


class CourseQueryForm(BaseForm):
    """课程查询表单"""
    page = IntegerField(validators=[Optional(), NumberRange(min=1, message='页码不能小于1')])
    per_page = IntegerField(validators=[Optional(), NumberRange(min=1, max=1000, message='每页数量必须在1-1000之间')])


class CourseOutlineQueryForm(BaseForm):
    """课程大纲查询表单"""
    course_id = StringField(validators=[DataRequired(message='课程ID不能为空'), Length(max=50, message='课程ID长度不能超过50个字符')])


class CourseOutlineCreateForm(BaseForm):
    """课程大纲创建表单"""
    course_id = StringField(validators=[DataRequired(message='课程ID不能为空'), Length(max=50, message='课程ID长度不能超过50个字符')])
    title = StringField(validators=[DataRequired(message='标题不能为空'), Length(max=100, message='标题长度不能超过100个字符')])
    content = StringField(validators=[DataRequired(message='内容不能为空')])
    video_url = StringField(validators=[Optional(), Length(max=500, message='视频链接长度不能超过500个字符')])
    sort_order = IntegerField(validators=[Optional(), NumberRange(min=0, message='排序值不能小于0')])


class CourseOutlineUpdateForm(BaseForm):
    """课程大纲更新表单"""
    title = StringField(validators=[Optional(), Length(max=100, message='标题长度不能超过100个字符')])
    content = StringField(validators=[Optional()])
    video_url = StringField(validators=[Optional(), Length(max=500, message='视频链接长度不能超过500个字符')])
    sort_order = IntegerField(validators=[Optional(), NumberRange(min=0, message='排序值不能小于0')])