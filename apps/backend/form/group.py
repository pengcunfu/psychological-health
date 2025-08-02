from form.base import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from .base import BaseForm


class GroupQueryForm(BaseForm):
    page = IntegerField(validators=[Optional(), NumberRange(min=1, message='页码必须大于等于1')])
    per_page = IntegerField(validators=[Optional(), NumberRange(min=1, message='每页数量必须大于等于1')])
    name = StringField(validators=[Optional(), Length(max=100, message='群组名称长度不能超过100个字符')])

class GroupCreateForm(BaseForm):
    name = StringField(validators=[DataRequired(message='群组名称不能为空'), Length(max=100, message='群组名称长度不能超过100个字符')])
    description = StringField(validators=[Optional(), Length(max=500, message='描述长度不能超过500个字符')])


class GroupUpdateForm(BaseForm):
    name = StringField(validators=[Optional(), Length(max=100, message='群组名称长度不能超过100个字符')])
    description = StringField(validators=[Optional(), Length(max=500, message='描述长度不能超过500个字符')])