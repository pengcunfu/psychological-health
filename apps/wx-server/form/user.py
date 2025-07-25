from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, Optional, Regexp, NumberRange
from .base import BaseForm
from models.user import User


class UserCreateForm(BaseForm):
    """用户创建表单"""
    username = StringField('用户名', [
        DataRequired(message='用户名不能为空'),
        Length(min=2, max=50, message='用户名长度必须在2-50个字符之间'),
        Regexp(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', message='用户名只能包含字母、数字、下划线和中文')
    ])

    avatar = StringField('头像URL', [
        Optional(),
        Length(max=500, message='头像URL长度不能超过500个字符')
    ])

    phone = StringField('手机号', [
        Optional(),
        Regexp(r'^1[3-9]\d{9}$', message='请输入正确的手机号格式')
    ])

    email = StringField('邮箱', [
        Optional(),
        Email(message='请输入正确的邮箱格式'),
        Length(max=100, message='邮箱长度不能超过100个字符')
    ])


class UserUpdateForm(BaseForm):
    """用户更新表单"""
    username = StringField('用户名', [
        Optional(),
        Length(min=2, max=50, message='用户名长度必须在2-50个字符之间'),
        Regexp(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', message='用户名只能包含字母、数字、下划线和中文')
    ])

    avatar = StringField('头像URL', [
        Optional(),
        Length(max=500, message='头像URL长度不能超过500个字符')
    ])

    phone = StringField('手机号', [
        Optional(),
        Regexp(r'^1[3-9]\d{9}$', message='请输入正确的手机号格式')
    ])

    email = StringField('邮箱', [
        Optional(),
        Email(message='请输入正确的邮箱格式'),
        Length(max=100, message='邮箱长度不能超过100个字符')
    ])


class UserQueryForm(BaseForm):
    """用户查询表单"""
    page = IntegerField('页码', [
        Optional(),
        NumberRange(min=1, message='页码必须大于0')
    ], default=1)

    per_page = IntegerField('每页数量', [
        Optional(),
        NumberRange(min=1, max=100, message='每页数量必须在1-100之间')
    ], default=10)

    username = StringField('用户名搜索', [
        Optional(),
        Length(max=50, message='搜索关键词长度不能超过50个字符')
    ])
    
    phone = StringField('手机号搜索', [
        Optional(),
        Length(max=20, message='手机号长度不能超过20个字符')
    ])
    
    email = StringField('邮箱搜索', [
        Optional(),
        Length(max=100, message='邮箱长度不能超过100个字符')
    ])
    
    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])

