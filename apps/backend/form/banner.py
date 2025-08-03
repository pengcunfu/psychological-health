from form.base import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, URL, Regexp
import re


class BannerQueryForm(BaseForm):
    page = IntegerField(validators=[Optional(), NumberRange(min=1, message='页码必须大于等于1')])
    per_page = IntegerField(validators=[Optional(), NumberRange(min=1, message='每页数量必须大于等于1')])
    title = StringField(validators=[Optional(), Length(max=100, message='标题长度不能超过100个字符')])


# 自定义URL验证器，支持相对路径和绝对URL
def validate_url_or_path(message=None):
    if message is None:
        message = '图片URL或路径格式不正确'
    
    def _validate(form, field):
        if not field.data:
            return
        
        url = field.data
        # 允许相对路径（以/开头）或完整URL（以http开头）
        if url.startswith('/') or url.startswith('http://') or url.startswith('https://'):
            return
        else:
            raise ValueError(message)
    
    return _validate


class BannerCreateForm(BaseForm):
    title = StringField(
        validators=[DataRequired(message='标题不能为空'), Length(max=100, message='标题长度不能超过100个字符')])
    image_url = StringField(validators=[DataRequired(message='图片URL不能为空'), validate_url_or_path()])
    link_url = StringField(validators=[Optional(), URL(message='链接URL格式不正确')])
    sort_order = IntegerField(validators=[Optional(), NumberRange(min=0, message='排序值不能小于0')])


class BannerUpdateForm(BaseForm):
    title = StringField(validators=[Optional(), Length(max=100, message='标题长度不能超过100个字符')])
    image_url = StringField(validators=[Optional(), validate_url_or_path()])
    link_url = StringField(validators=[Optional(), URL(message='链接URL格式不正确')])
    sort_order = IntegerField(validators=[Optional(), NumberRange(min=0, message='排序值不能小于0')])
