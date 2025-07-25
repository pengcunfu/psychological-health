from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, ValidationError
from datetime import datetime

from .base import BaseForm


class AppointmentCreateForm(BaseForm):
    """预约创建表单"""
    user_id = StringField('用户ID', [
        DataRequired(message='用户ID不能为空'),
        Length(max=36, message='用户ID长度不能超过36个字符')
    ])

    counselor_id = StringField('咨询师ID', [
        DataRequired(message='咨询师ID不能为空'),
        Length(max=36, message='咨询师ID长度不能超过36个字符')
    ])

    appointment_time = StringField('预约时间', [
        DataRequired(message='预约时间不能为空')
    ])

    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])

    def validate_appointment_time(self, field):
        """验证预约时间格式和有效性"""
        try:
            appointment_time = datetime.fromisoformat(field.data.replace('Z', '+00:00'))
            if appointment_time <= datetime.utcnow():
                raise ValidationError('预约时间必须在未来')
        except ValueError:
            raise ValidationError('预约时间格式错误，请使用ISO格式')


class AppointmentUpdateForm(BaseForm):
    """预约更新表单"""
    appointment_time = StringField('预约时间', [
        Optional()
    ])

    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=3, message='状态值必须在0-3之间')
    ])

    def validate_appointment_time(self, field):
        """验证预约时间格式和有效性"""
        if field.data:
            try:
                appointment_time = datetime.fromisoformat(field.data.replace('Z', '+00:00'))
                if appointment_time <= datetime.utcnow():
                    raise ValidationError('预约时间必须在未来')
            except ValueError:
                raise ValidationError('预约时间格式错误，请使用ISO格式')

    def validate_status(self, field):
        """验证状态值"""
        if field.data is not None and field.data not in [0, 1, 2, 3]:
            raise ValidationError('状态值无效')


class AppointmentQueryForm(BaseForm):
    """预约查询表单"""
    page = IntegerField('页码', [
        Optional(),
        NumberRange(min=1, message='页码必须大于0')
    ])

    per_page = IntegerField('每页数量', [
        Optional(),
        NumberRange(min=1, max=100, message='每页数量必须在1-100之间')
    ])

    user_id = StringField('用户ID', [
        Optional(),
        Length(max=36, message='用户ID长度不能超过36个字符')
    ])

    counselor_id = StringField('咨询师ID', [
        Optional(),
        Length(max=36, message='咨询师ID长度不能超过36个字符')
    ])

    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=3, message='状态值必须在0-3之间')
    ])
