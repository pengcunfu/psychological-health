from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import Optional, NumberRange, Length, DataRequired
from wtforms.fields import FieldList

from .base import BaseForm


class UserQueryForm(BaseForm):
    """用户查询表单"""
    page = IntegerField('页码', [
        Optional(),
        NumberRange(min=1, message='页码必须大于0')
    ])

    size = IntegerField('每页数量', [
        Optional(),
        NumberRange(min=1, max=100, message='每页数量必须在1-100之间')
    ])

    keyword = StringField('关键词', [
        Optional(),
        Length(max=255, message='关键词长度不能超过255个字符')
    ])


class RoleCreateForm(BaseForm):
    """角色创建表单"""
    name = StringField('角色名称', [
        DataRequired(message='角色名称不能为空'),
        Length(max=50, message='角色名称长度不能超过50个字符')
    ])
    code = StringField('角色编码', [
        DataRequired(message='角色编码不能为空'),
        Length(max=50, message='角色编码长度不能超过50个字符')
    ])
    description = StringField('角色描述', [
        Optional(),
        Length(max=255, message='角色描述长度不能超过255个字符')
    ])
    sort_order = IntegerField('排序', [
        Optional(),
        NumberRange(min=0, message='排序值不能小于0')
    ])
    data_scope = IntegerField('数据范围', [
        Optional(),
        NumberRange(min=1, max=5, message='数据范围值必须在1-5之间')
    ])
    menu_ids = FieldList(StringField('菜单ID'), [
        Optional()
    ])
    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])
    is_default = BooleanField('是否默认', [
        Optional()
    ])
    remark = StringField('备注', [
        Optional(),
        Length(max=255, message='备注长度不能超过255个字符')
    ])


class RoleUpdateForm(BaseForm):
    """角色更新表单"""
    name = StringField('角色名称', [
        Optional(),
        Length(max=50, message='角色名称长度不能超过50个字符')
    ])
    code = StringField('角色编码', [
        Optional(),
        Length(max=50, message='角色编码长度不能超过50个字符')
    ])
    description = StringField('角色描述', [
        Optional(),
        Length(max=255, message='角色描述长度不能超过255个字符')
    ])
    sort_order = IntegerField('排序', [
        Optional(),
        NumberRange(min=0, message='排序值不能小于0')
    ])
    data_scope = IntegerField('数据范围', [
        Optional(),
        NumberRange(min=1, max=5, message='数据范围值必须在1-5之间')
    ])
    menu_ids = FieldList(StringField('菜单ID'), [
        Optional()
    ])
    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])
    is_default = BooleanField('是否默认', [
        Optional()
    ])
    remark = StringField('备注', [
        Optional(),
        Length(max=255, message='备注长度不能超过255个字符')
    ])


class RoleQueryForm(BaseForm):
    """角色查询表单"""
    page = IntegerField('页码', [Optional(), NumberRange(min=1, message='页码不能小于1')])
    size = IntegerField('每页数量', [Optional(), NumberRange(min=1, message='每页数量不能小于1')])
    keyword = StringField('关键词', [Optional(), Length(max=100, message='关键词长度不能超过100个字符')])


class MenuCreateForm(BaseForm):
    """菜单创建表单"""
    name = StringField('菜单名称', [DataRequired(), Length(max=50, message='菜单名称长度不能超过50个字符')])
    path = StringField('菜单路径', [Optional(), Length(max=255, message='菜单路径长度不能超过255个字符')])
    icon = StringField('菜单图标', [Optional(), Length(max=50, message='菜单图标长度不能超过50个字符')])
    parent_id = StringField('父菜单ID', [Optional(), Length(max=36, message='父菜单ID长度不能超过36个字符')])
    level = IntegerField('菜单层级', [Optional(), NumberRange(min=1, message='菜单层级不能小于1')])
    sort_order = IntegerField('排序', [Optional(), NumberRange(min=0, message='排序值不能小于0')])
    menu_type = IntegerField('菜单类型', [Optional(), NumberRange(min=1, max=3, message='菜单类型值必须在1-3之间')])
    permission = StringField('权限标识', [Optional(), Length(max=100, message='权限标识长度不能超过100个字符')])
    component = StringField('组件路径', [Optional(), Length(max=255, message='组件路径长度不能超过255个字符')])
    is_external = BooleanField('是否外链', [Optional()])
    is_visible = BooleanField('是否可见', [Optional()])
    is_cache = BooleanField('是否缓存', [Optional()])
    status = IntegerField('状态', [Optional(), NumberRange(min=0, max=1, message='状态值必须为0或1')])
    remark = StringField('备注', [Optional(), Length(max=255, message='备注长度不能超过255个字符')])


class MenuUpdateForm(BaseForm):
    """菜单更新表单"""
    name = StringField('菜单名称', [Optional(), Length(max=50, message='菜单名称长度不能超过50个字符')])
    path = StringField('菜单路径', [Optional(), Length(max=255, message='菜单路径长度不能超过255个字符')])
    icon = StringField('菜单图标', [Optional(), Length(max=50, message='菜单图标长度不能超过50个字符')])
    parent_id = StringField('父菜单ID', [Optional(), Length(max=36, message='父菜单ID长度不能超过36个字符')])
    level = IntegerField('菜单层级', [Optional(), NumberRange(min=1, message='菜单层级不能小于1')])
    sort_order = IntegerField('排序', [Optional(), NumberRange(min=0, message='排序值不能小于0')])
    menu_type = IntegerField('菜单类型', [Optional(), NumberRange(min=1, max=3, message='菜单类型值必须在1-3之间')])
    permission = StringField('权限标识', [Optional(), Length(max=100, message='权限标识长度不能超过100个字符')])
    component = StringField('组件路径', [Optional(), Length(max=255, message='组件路径长度不能超过255个字符')])
    is_external = BooleanField('是否外链', [Optional()])
    is_visible = BooleanField('是否可见', [Optional()])
    is_cache = BooleanField('是否缓存', [Optional()])
    status = IntegerField('状态', [Optional(), NumberRange(min=0, max=1, message='状态值必须为0或1')])
    remark = StringField('备注', [Optional(), Length(max=255, message='备注长度不能超过255个字符')])





class MenuQueryForm(BaseForm):
    """菜单查询表单"""
    page = IntegerField('页码', [Optional(), NumberRange(min=1, message='页码不能小于1')])
    size = IntegerField('每页数量', [Optional(), NumberRange(min=1, message='每页数量不能小于1')])
    keyword = StringField('关键词', [Optional(), Length(max=100, message='关键词长度不能超过100个字符')])