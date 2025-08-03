from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

from .base import BaseForm


class AnnouncementCreateForm(BaseForm):
    """公告创建表单"""
    # counselor_id = StringField('咨询师ID', [
    #     DataRequired(message='咨询师ID不能为空'),
    #     Length(max=36, message='咨询师ID长度不能超过36个字符')
    # ])

    # service_id = StringField('服务ID', [
    #     DataRequired(message='服务ID不能为空'),
    #     Length(max=36, message='服务ID长度不能超过36个字符')
    # ])

    user_id = StringField('用户ID', [
        DataRequired(message='用户ID不能为空'),
        Length(max=36, message='用户ID长度不能超过36个字符')
    ])

    date = StringField('日期', [
        DataRequired(message='日期不能为空'),
        Length(max=10, message='日期格式错误')
    ])

    time_slot = StringField('时间段', [
        DataRequired(message='时间段不能为空'),
        Length(max=50, message='时间段长度不能超过50个字符')
    ])

    note = StringField('备注', [
        Optional(),
        Length(max=500, message='备注长度不能超过500个字符')
    ])

    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])


class AnnouncementUpdateForm(BaseForm):
    """公告更新表单"""
    # counselor_id = StringField('咨询师ID', [
    #     Optional(),
    #     Length(max=36, message='咨询师ID长度不能超过36个字符')
    # ])

    # service_id = StringField('服务ID', [
    #     Optional(),
    #     Length(max=36, message='服务ID长度不能超过36个字符')
    # ])

    user_id = StringField('用户ID', [
        Optional(),
        Length(max=36, message='用户ID长度不能超过36个字符')
    ])

    date = StringField('日期', [
        Optional(),
        Length(max=10, message='日期格式错误')
    ])

    time_slot = StringField('时间段', [
        Optional(),
        Length(max=50, message='时间段长度不能超过50个字符')
    ])

    note = StringField('备注', [
        Optional(),
        Length(max=500, message='备注长度不能超过500个字符')
    ])

    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])


class AnnouncementQueryForm(BaseForm):
    """公告查询表单"""
    page = IntegerField('页码', [
        Optional(),
        NumberRange(min=1, message='页码必须大于0')
    ], default=1)

    per_page = IntegerField('每页数量', [
        Optional(),
        NumberRange(min=1, max=100, message='每页数量必须在1-100之间')
    ], default=10)

    # counselor_id = StringField('咨询师ID', [
    #     Optional(),
    #     Length(max=36, message='咨询师ID长度不能超过36个字符')
    # ])

    user_id = StringField('用户ID', [
        Optional(),
        Length(max=36, message='用户ID长度不能超过36个字符')
    ])

    # service_id = StringField('服务ID', [
    #     Optional(),
    #     Length(max=36, message='服务ID长度不能超过36个字符')
    # ])

    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])

    date = StringField('日期', [
        Optional(),
        Length(max=10, message='日期格式错误')
    ])
