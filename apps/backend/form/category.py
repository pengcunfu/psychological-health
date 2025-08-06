from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators
from wtforms.validators import DataRequired, Length, Optional, NumberRange

from .base import BaseForm


class CategoryCreateForm(BaseForm):
    """分类创建表单"""
    name = StringField('分类名称', [DataRequired(message='分类名称不能为空'), Length(max=100, message='分类名称不能超过100个字符')])
    type = StringField('分类类型', [Optional(), Length(max=50, message='分类类型不能超过50个字符')], default='course')
    icon = StringField('图标', [Optional(), Length(max=255, message='图标URL不能超过255个字符')])
    path = StringField('路径', [Optional(), Length(max=255, message='路径不能超过255个字符')])
    description = StringField('描述', [Optional(), Length(max=500, message='描述不能超过500个字符')])
    sort_order = IntegerField('排序顺序', [Optional(), NumberRange(min=0, message='排序值必须大于等于0')], default=0)
    status = IntegerField('状态', [Optional(), NumberRange(min=0, max=1, message='状态值必须为0或1')], default=1)

class CategoryUpdateForm(BaseForm):
    """分类更新表单"""
    name = StringField('分类名称', [Optional(), Length(max=100, message='分类名称不能超过100个字符')])
    type = StringField('分类类型', [Optional(), Length(max=50, message='分类类型不能超过50个字符')])
    icon = StringField('图标', [Optional(), Length(max=255, message='图标URL不能超过255个字符')])
    path = StringField('路径', [Optional(), Length(max=255, message='路径不能超过255个字符')])
    description = StringField('描述', [Optional(), Length(max=500, message='描述不能超过500个字符')])
    sort_order = IntegerField('排序顺序', [Optional(), NumberRange(min=0, message='排序值必须大于等于0')])
    status = IntegerField('状态', [Optional(), NumberRange(min=0, max=1, message='状态值必须为0或1')])

class CategoryQueryForm(BaseForm):
    """分类查询表单"""
    page = IntegerField('页码', [Optional(), NumberRange(min=1, message='页码必须大于0')], default=1)
    per_page = IntegerField('每页数量', [Optional(), NumberRange(min=1, max=100, message='每页数量必须在1-100之间')], default=10)
    name = StringField('分类名称', [Optional(), Length(max=100, message='分类名称不能超过100个字符')])
    type = StringField('分类类型', [Optional(), Length(max=50, message='分类类型不能超过50个字符')])
    status = IntegerField('状态', [Optional(), NumberRange(min=0, max=1, message='状态值必须为0或1')])

class CategoryStatusUpdateForm(BaseForm):
    """分类状态更新表单"""
    status = IntegerField('状态', [DataRequired(message='状态不能为空')])
