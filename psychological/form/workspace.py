from wtforms import StringField, IntegerField, SelectField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, NumberRange, Regexp
from .base import BaseForm
from psychological.models.workspace import Workspace


class WorkspaceQueryForm(BaseForm):
    """工作室查询表单"""
    page = IntegerField('页码', [
        Optional(),
        NumberRange(min=1, message='页码必须大于0')
    ], default=1)
    
    per_page = IntegerField('每页数量', [
        Optional(),
        NumberRange(min=1, max=100, message='每页数量必须在1-100之间')
    ], default=10)
    
    name = StringField('工作室名称', [
        Optional(),
        Length(max=200, message='名称长度不能超过200个字符')
    ])
    
    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])


class WorkspaceCreateForm(BaseForm):
    """工作室创建表单"""
    name = StringField('工作室名称', [
        DataRequired(message='名称是必填项'),
        Length(min=1, max=200, message='名称长度必须在1-200个字符之间'),
        Regexp(r'^[a-zA-Z0-9_\u4e00-\u9fa5\s-]+$', message='名称只能包含字母、数字、下划线、中文、空格和短横线')
    ])
    
    cover_image = StringField('封面图片', [
        Optional(),
        Length(max=255, message='封面图片URL长度不能超过255个字符')
    ])
    
    address = StringField('详细地址', [
        Optional(),
        Length(max=500, message='地址长度不能超过500个字符')
    ])
    
    distance = FloatField('距离', [
        Optional(),
        NumberRange(min=0, message='距离必须大于等于0')
    ])
    
    business_hours = StringField('营业时间', [
        Optional(),
        Length(max=200, message='营业时间长度不能超过200个字符')
    ])
    
    environment_images = StringField('环境照片', [
        Optional()
    ])
    
    introduction = TextAreaField('工作室简介', [
        Optional(),
        Length(max=2000, message='简介长度不能超过2000个字符')
    ])
    
    slogan = StringField('工作室寄语', [
        Optional(),
        Length(max=500, message='寄语长度不能超过500个字符')
    ])
    
    latitude = FloatField('纬度', [
        Optional(),
        NumberRange(min=-90, max=90, message='纬度必须在-90到90之间')
    ])
    
    longitude = FloatField('经度', [
        Optional(),
        NumberRange(min=-180, max=180, message='经度必须在-180到180之间')
    ])
    
    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ], default=1)
    
    sort_order = IntegerField('排序', [
        Optional(),
        NumberRange(min=0, max=9999, message='排序值必须在0-9999之间')
    ], default=100)
    
    def validate_name_unique(self):
        """验证工作室名称唯一性"""
        existing = Workspace.query.filter_by(name=self.name.data).first()
        return existing is not None


class WorkspaceUpdateForm(BaseForm):
    """工作室更新表单"""
    name = StringField('工作室名称', [
        Optional(),
        Length(min=1, max=200, message='名称长度必须在1-200个字符之间'),
        Regexp(r'^[a-zA-Z0-9_\u4e00-\u9fa5\s-]+$', message='名称只能包含字母、数字、下划线、中文、空格和短横线')
    ])
    
    cover_image = StringField('封面图片', [
        Optional(),
        Length(max=255, message='封面图片URL长度不能超过255个字符')
    ])
    
    address = StringField('详细地址', [
        Optional(),
        Length(max=500, message='地址长度不能超过500个字符')
    ])
    
    distance = FloatField('距离', [
        Optional(),
        NumberRange(min=0, message='距离必须大于等于0')
    ])
    
    business_hours = StringField('营业时间', [
        Optional(),
        Length(max=200, message='营业时间长度不能超过200个字符')
    ])
    
    environment_images = StringField('环境照片', [
        Optional()
    ])
    
    introduction = TextAreaField('工作室简介', [
        Optional(),
        Length(max=2000, message='简介长度不能超过2000个字符')
    ])
    
    slogan = StringField('工作室寄语', [
        Optional(),
        Length(max=500, message='寄语长度不能超过500个字符')
    ])
    
    latitude = FloatField('纬度', [
        Optional(),
        NumberRange(min=-90, max=90, message='纬度必须在-90到90之间')
    ])
    
    longitude = FloatField('经度', [
        Optional(),
        NumberRange(min=-180, max=180, message='经度必须在-180到180之间')
    ])
    
    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])
    
    sort_order = IntegerField('排序', [
        Optional(),
        NumberRange(min=0, max=9999, message='排序值必须在0-9999之间')
    ])
    
    def validate_name_unique(self, workspace_id=None):
        """验证工作室名称唯一性（排除自己）"""
        if self.name.data:
            query = Workspace.query.filter_by(name=self.name.data)
            if workspace_id:
                query = query.filter(Workspace.id != workspace_id)
            existing = query.first()
            return existing is not None
        return False