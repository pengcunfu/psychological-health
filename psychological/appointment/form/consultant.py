from wtforms import StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Regexp
from pcf_flask_helper.form.base import BaseForm
import re


class ConsultantCreateForm(BaseForm):
    """创建咨询人表单"""
    
    # 用户关联
    user_id = StringField('用户ID', [
        Optional(),
        Length(max=50, message='用户ID长度不能超过50个字符')
    ])
    
    # 基本信息
    real_name = StringField('真实姓名', [
        DataRequired(message='真实姓名不能为空'),
        Length(2, 50, message='真实姓名长度应在2-50个字符之间')
    ])
    
    birth_year = IntegerField('出生年份', [
        Optional(),
        NumberRange(min=1900, max=2024, message='出生年份应在1900-2024之间')
    ])
    
    birth_month = IntegerField('出生月份', [
        Optional(),
        NumberRange(min=1, max=12, message='出生月份应在1-12之间')
    ])
    
    gender = SelectField('性别', [
        DataRequired(message='请选择性别')
    ], choices=[
        ('male', '男'),
        ('female', '女')
    ])
    
    phone = StringField('联系方式', [
        DataRequired(message='联系方式不能为空'),
        Length(11, 11, message='请输入正确的手机号码'),
        Regexp(r'^1[3-9]\d{9}$', message='请输入正确的手机号码格式')
    ])
    
    # 紧急联系人信息
    emergency_name = StringField('紧急联系人姓名', [
        DataRequired(message='紧急联系人姓名不能为空'),
        Length(2, 50, message='紧急联系人姓名长度应在2-50个字符之间')
    ])
    
    emergency_relationship = SelectField('与紧急联系人的关系', [
        DataRequired(message='请选择与紧急联系人的关系')
    ], choices=[
        ('self', '本人'),
        ('spouse', '配偶'),
        ('child', '子女'),
        ('parent', '父母'),
        ('sibling', '兄弟姐妹'),
        ('friend', '朋友'),
        ('other', '其他')
    ])
    
    emergency_phone = StringField('紧急联系人电话', [
        DataRequired(message='紧急联系人电话不能为空'),
        Length(11, 11, message='请输入正确的手机号码'),
        Regexp(r'^1[3-9]\d{9}$', message='请输入正确的手机号码格式')
    ])
    
    # 其他信息
    notes = TextAreaField('备注信息', [
        Optional(),
        Length(max=500, message='备注信息不能超过500个字符')
    ])
    
    is_default = IntegerField('是否为默认咨询人', [
        Optional(),
        NumberRange(min=0, max=1, message='默认咨询人标识错误')
    ])
    
    def validate_phone(self, field):
        """验证手机号码"""
        if not re.match(r'^1[3-9]\d{9}$', field.data):
            raise ValueError('请输入正确的手机号码格式')
    
    def validate_emergency_phone(self, field):
        """验证紧急联系人手机号码"""
        if not re.match(r'^1[3-9]\d{9}$', field.data):
            raise ValueError('请输入正确的紧急联系人手机号码格式')


class ConsultantUpdateForm(BaseForm):
    """更新咨询人表单"""
    
    # 用户关联
    user_id = StringField('用户ID', [
        Optional(),
        Length(max=50, message='用户ID长度不能超过50个字符')
    ])
    
    # 基本信息
    real_name = StringField('真实姓名', [
        DataRequired(message='真实姓名不能为空'),
        Length(2, 50, message='真实姓名长度应在2-50个字符之间')
    ])
    
    birth_year = IntegerField('出生年份', [
        Optional(),
        NumberRange(min=1900, max=2024, message='出生年份应在1900-2024之间')
    ])
    
    birth_month = IntegerField('出生月份', [
        Optional(),
        NumberRange(min=1, max=12, message='出生月份应在1-12之间')
    ])
    
    gender = SelectField('性别', [
        DataRequired(message='请选择性别')
    ], choices=[
        ('male', '男'),
        ('female', '女')
    ])
    
    phone = StringField('联系方式', [
        DataRequired(message='联系方式不能为空'),
        Length(11, 11, message='请输入正确的手机号码'),
        Regexp(r'^1[3-9]\d{9}$', message='请输入正确的手机号码格式')
    ])
    
    # 紧急联系人信息
    emergency_name = StringField('紧急联系人姓名', [
        DataRequired(message='紧急联系人姓名不能为空'),
        Length(2, 50, message='紧急联系人姓名长度应在2-50个字符之间')
    ])
    
    emergency_relationship = SelectField('与紧急联系人的关系', [
        DataRequired(message='请选择与紧急联系人的关系')
    ], choices=[
        ('self', '本人'),
        ('spouse', '配偶'),
        ('child', '子女'),
        ('parent', '父母'),
        ('sibling', '兄弟姐妹'),
        ('friend', '朋友'),
        ('other', '其他')
    ])
    
    emergency_phone = StringField('紧急联系人电话', [
        DataRequired(message='紧急联系人电话不能为空'),
        Length(11, 11, message='请输入正确的手机号码'),
        Regexp(r'^1[3-9]\d{9}$', message='请输入正确的手机号码格式')
    ])
    
    # 其他信息
    notes = TextAreaField('备注信息', [
        Optional(),
        Length(max=500, message='备注信息不能超过500个字符')
    ])
    
    is_default = IntegerField('是否为默认咨询人', [
        Optional(),
        NumberRange(min=0, max=1, message='默认咨询人标识错误')
    ])
    
    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值错误')
    ])


class ConsultantListForm(BaseForm):
    """咨询人列表查询表单"""
    
    keyword = StringField('关键词', [
        Optional(),
        Length(max=50, message='关键词不能超过50个字符')
    ])
    
    gender = SelectField('性别', [Optional()], choices=[
        ('', '全部'),
        ('male', '男'),
        ('female', '女')
    ])
    
    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值错误')
    ])
    
    page = IntegerField('页码', [
        Optional(),
        NumberRange(min=1, message='页码必须大于0')
    ])
    
    per_page = IntegerField('每页数量', [
        Optional(),
        NumberRange(min=1, max=100, message='每页数量应在1-100之间')
    ])
