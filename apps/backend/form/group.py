from form.base import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from .base import BaseForm


class GroupQueryForm(BaseForm):
    page = IntegerField(validators=[Optional(), NumberRange(min=1, message='页码必须大于等于1')])
    per_page = IntegerField(validators=[Optional(), NumberRange(min=1, message='每页数量必须大于等于1')])
    title = StringField(validators=[Optional(), Length(max=200, message='群组标题长度不能超过200个字符')])

class GroupCreateForm(BaseForm):
    title = StringField(validators=[DataRequired(message='群组标题不能为空'), Length(max=200, message='群组标题长度不能超过200个字符')])
    description = StringField(validators=[Optional(), Length(max=500, message='描述长度不能超过500个字符')])


class GroupUpdateForm(BaseForm):
    title = StringField(validators=[Optional(), Length(max=200, message='群组标题长度不能超过200个字符')])
    description = StringField(validators=[Optional(), Length(max=500, message='描述长度不能超过500个字符')])