from wtforms import StringField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, AnyOf, NumberRange, ValidationError
from datetime import datetime

from pcf_flask_helper.form.base import BaseForm


def validate_datetime_format(form, field):
    """验证日期时间格式"""
    if field.data:
        try:
            datetime.strptime(field.data, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValidationError('日期时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式')


class AnnouncementCreateForm(BaseForm):
    """公告创建表单"""
    title = StringField('公告标题', [
        DataRequired(message='公告标题不能为空'),
        Length(max=200, message='公告标题长度不能超过200个字符')
    ])

    type = StringField('公告类型', [
        DataRequired(message='公告类型不能为空'),
        AnyOf(['system', 'activity', 'maintenance', 'notice'], message='公告类型必须是system、activity、maintenance或notice')
    ])

    priority = StringField('优先级', [
        DataRequired(message='优先级不能为空'),
        AnyOf(['low', 'medium', 'high', 'urgent'], message='优先级必须是low、medium、high或urgent')
    ])

    status = StringField('状态', [
        DataRequired(message='状态不能为空'),
        AnyOf(['draft', 'published', 'archived'], message='状态必须是draft、published或archived')
    ])

    summary = TextAreaField('公告摘要', [
        Optional(),
        Length(max=500, message='公告摘要长度不能超过500个字符')
    ])

    content = TextAreaField('公告内容', [
        DataRequired(message='公告内容不能为空'),
        Length(max=5000, message='公告内容长度不能超过5000个字符')
    ])

    start_time = StringField('生效时间', [
        Optional(),
        validate_datetime_format
    ])

    end_time = StringField('失效时间', [
        Optional(),
        validate_datetime_format
    ])

    is_pinned = BooleanField('是否置顶', [
        Optional()
    ])


class AnnouncementUpdateForm(BaseForm):
    """公告更新表单"""
    title = StringField('公告标题', [
        Optional(),
        Length(max=200, message='公告标题长度不能超过200个字符')
    ])

    type = StringField('公告类型', [
        Optional(),
        AnyOf(['system', 'activity', 'maintenance', 'notice'], message='公告类型必须是system、activity、maintenance或notice')
    ])

    priority = StringField('优先级', [
        Optional(),
        AnyOf(['low', 'medium', 'high', 'urgent'], message='优先级必须是low、medium、high或urgent')
    ])

    status = StringField('状态', [
        Optional(),
        AnyOf(['draft', 'published', 'archived'], message='状态必须是draft、published或archived')
    ])

    summary = TextAreaField('公告摘要', [
        Optional(),
        Length(max=500, message='公告摘要长度不能超过500个字符')
    ])

    content = TextAreaField('公告内容', [
        Optional(),
        Length(max=5000, message='公告内容长度不能超过5000个字符')
    ])

    start_time = StringField('生效时间', [
        Optional(),
        validate_datetime_format
    ])

    end_time = StringField('失效时间', [
        Optional(),
        validate_datetime_format
    ])

    is_pinned = BooleanField('是否置顶', [
        Optional()
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

    title = StringField('公告标题', [
        Optional(),
        Length(max=200, message='公告标题长度不能超过200个字符')
    ])

    type = StringField('公告类型', [
        Optional(),
        AnyOf(['system', 'activity', 'maintenance', 'notice'], message='公告类型必须是system、activity、maintenance或notice')
    ])

    status = StringField('状态', [
        Optional(),
        AnyOf(['draft', 'published', 'archived'], message='状态必须是draft、published或archived')
    ])

    priority = StringField('优先级', [
        Optional(),
        AnyOf(['low', 'medium', 'high', 'urgent'], message='优先级必须是low、medium、high或urgent')
    ])
