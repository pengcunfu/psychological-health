from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators
from wtforms.validators import DataRequired, Length, Optional, NumberRange

from .base import BaseForm


class CategoryCreateForm(BaseForm):
    """分类创建表单"""
    name = StringField('分类名称', [DataRequired(message='分类名称不能为空')])
    icon = StringField('图标', [Optional()])
    path = StringField('路径', [Optional()])
    description = StringField('描述', [Optional()])
    sort_order = IntegerField('排序顺序', [Optional()], default=0)
    status = IntegerField('状态', [Optional()], default=1)

class CategoryUpdateForm(BaseForm):
    """分类更新表单"""
    name = StringField('分类名称', [Optional()])
    icon = StringField('图标', [Optional()])
    path = StringField('路径', [Optional()])
    description = StringField('描述', [Optional()])
    sort_order = IntegerField('排序顺序', [Optional()])
    status = IntegerField('状态', [Optional()])

class CategoryQueryForm(BaseForm):
    """分类查询表单"""
    page = IntegerField('页码', [Optional()], default=1)
    per_page = IntegerField('每页数量', [Optional()], default=10)
    name = StringField('分类名称', [Optional()])
    status = IntegerField('状态', [Optional()])

class CategoryStatusUpdateForm(BaseForm):
    """分类状态更新表单"""
    status = IntegerField('状态', [DataRequired(message='状态不能为空')])
