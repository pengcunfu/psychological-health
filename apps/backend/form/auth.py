from wtforms import StringField, IntegerField, BooleanField, DateField, TextAreaField
from wtforms.validators import Optional, NumberRange, Length, DataRequired, Email, Regexp
from wtforms.fields import FieldList

from .base import BaseForm


class LoginForm(BaseForm):
    """用户登录表单"""
    username = StringField('用户名', [
        DataRequired(message='用户名不能为空'),
        Length(max=50, message='用户名长度不能超过50个字符')
    ])
    password = StringField('密码', [
        DataRequired(message='密码不能为空'),
        # Length(min=6, max=20, message='密码长度必须在6-20个字符之间')
    ])
    verify_code = StringField('验证码', [
        Optional(),
        Length(min=4, max=6, message='验证码长度必须在4-6个字符之间')
    ])


class PhoneLoginForm(BaseForm):
    """手机号登录表单"""
    phone = StringField('手机号', [
        DataRequired(message='手机号不能为空'),
        Regexp(r'^1[3-9]\d{9}$', message='手机号格式不正确')
    ])
    password = StringField('密码', [
        DataRequired(message='密码不能为空'),
        Length(min=6, max=20, message='密码长度必须在6-20个字符之间')
    ])


class RegisterForm(BaseForm):
    """用户注册表单"""
    username = StringField('用户名', [
        DataRequired(message='用户名不能为空'),
        Length(min=2, max=50, message='用户名长度必须在2-50个字符之间'),
        Regexp(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', message='用户名只能包含字母、数字、下划线和中文')
    ])
    password = StringField('密码', [
        DataRequired(message='密码不能为空'),
        Length(min=6, max=20, message='密码长度必须在6-20个字符之间')
    ])
    phone = StringField('手机号', [
        Optional(),
        Regexp(r'^1[3-9]\d{9}$', message='手机号格式不正确')
    ])
    email = StringField('邮箱', [
        Optional(),
        Email(message='邮箱格式不正确'),
        Length(max=100, message='邮箱长度不能超过100个字符')
    ])
    avatar = StringField('头像', [
        Optional(),
        Length(max=255, message='头像路径长度不能超过255个字符')
    ])


class UpdateProfileForm(BaseForm):
    """更新用户信息表单"""
    avatar = StringField('头像', [
        Optional(),
        Length(max=255, message='头像路径长度不能超过255个字符')
    ])
    phone = StringField('手机号', [
        Optional(),
        Regexp(r'^1[3-9]\d{9}$', message='手机号格式不正确')
    ])
    email = StringField('邮箱', [
        Optional(),
        Email(message='邮箱格式不正确'),
        Length(max=100, message='邮箱长度不能超过100个字符')
    ])
    real_name = StringField('真实姓名', [
        Optional(),
        Length(max=100, message='真实姓名长度不能超过100个字符')
    ])
    gender = IntegerField('性别', [
        Optional(),
        NumberRange(min=0, max=2, message='性别值必须为0、1或2')
    ])
    birth_date = DateField('出生日期', [
        Optional()
    ])
    brief_introduction = TextAreaField('个人简介', [
        Optional(),
        Length(max=500, message='个人简介长度不能超过500个字符')
    ])


class ChangePasswordForm(BaseForm):
    """修改密码表单"""
    old_password = StringField('旧密码', [
        DataRequired(message='旧密码不能为空'),
        Length(min=6, max=20, message='旧密码长度必须在6-20个字符之间')
    ])
    new_password = StringField('新密码', [
        DataRequired(message='新密码不能为空'),
        Length(min=6, max=20, message='新密码长度必须在6-20个字符之间')
    ])


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