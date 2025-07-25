from form.base import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class DiseaseTagsQueryForm(BaseForm):
    page = IntegerField(validators=[Optional(), NumberRange(min=1, message='页码必须大于等于1')])
    per_page = IntegerField(validators=[Optional(), NumberRange(min=1, message='每页数量必须大于等于1')])
    name = StringField(validators=[Optional(), Length(max=50, message='标签名称长度不能超过50个字符')])



class DiseaseTagsCreateForm(BaseForm):
    name = StringField(validators=[DataRequired(message='标签名称不能为空'), Length(max=50, message='标签名称长度不能超过50个字符')])
    description = StringField(validators=[Optional(), Length(max=200, message='描述长度不能超过200个字符')])