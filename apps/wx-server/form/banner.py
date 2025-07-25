from form.base import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, URL

class BannerQueryForm(BaseForm):
    page = IntegerField(validators=[Optional(), NumberRange(min=1, message='页码必须大于等于1')])
    per_page = IntegerField(validators=[Optional(), NumberRange(min=1, message='每页数量必须大于等于1')])
    title = StringField(validators=[Optional(), Length(max=100, message='标题长度不能超过100个字符')])

class BannerCreateForm(BaseForm):
    title = StringField(validators=[DataRequired(message='标题不能为空'), Length(max=100, message='标题长度不能超过100个字符')])
    image_url = StringField(validators=[DataRequired(message='图片URL不能为空'), URL(message='图片URL格式不正确')])
    link_url = StringField(validators=[Optional(), URL(message='链接URL格式不正确')])
    sort_order = IntegerField(validators=[Optional(), NumberRange(min=0, message='排序值不能小于0')])

class BannerUpdateForm(BaseForm):
    title = StringField(validators=[Optional(), Length(max=100, message='标题长度不能超过100个字符')])
    image_url = StringField(validators=[Optional(), URL(message='图片URL格式不正确')])
    link_url = StringField(validators=[Optional(), URL(message='链接URL格式不正确')])
    sort_order = IntegerField(validators=[Optional(), NumberRange(min=0, message='排序值不能小于0')])