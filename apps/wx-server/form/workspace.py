from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional, Length, NumberRange, Regexp
from .base import BaseForm
from models.workspace import Workspace


class WorkspaceQueryForm(BaseForm):
    """工作空间查询表单"""
    page = IntegerField('页码', [
        Optional(),
        NumberRange(min=1, message='页码必须大于0')
    ], default=1)
    
    per_page = IntegerField('每页数量', [
        Optional(),
        NumberRange(min=1, max=100, message='每页数量必须在1-100之间')
    ], default=10)
    
    name = StringField('工作空间名称', [
        Optional(),
        Length(max=100, message='名称长度不能超过100个字符')
    ])
    
    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])


class WorkspaceCreateForm(BaseForm):
    """工作空间创建表单"""
    name = StringField('工作空间名称', [
        DataRequired(message='名称是必填项'),
        Length(min=1, max=100, message='名称长度必须在1-100个字符之间'),
        Regexp(r'^[a-zA-Z0-9_\u4e00-\u9fa5\s-]+$', message='名称只能包含字母、数字、下划线、中文、空格和短横线')
    ])
    
    description = StringField('描述', [
        Optional(),
        Length(max=500, message='描述长度不能超过500个字符')
    ])
    
    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ], default=1)
    
    sort_order = IntegerField('排序', [
        Optional(),
        NumberRange(min=0, max=9999, message='排序值必须在0-9999之间')
    ], default=0)
    
    def validate_name(self, field):
        """验证工作空间名称唯一性"""
        existing = Workspace.query.filter_by(name=field.data).first()
        if existing:
            raise ValueError('工作空间名称已存在')


class WorkspaceUpdateForm(BaseForm):
    """工作空间更新表单"""
    name = StringField('工作空间名称', [
        Optional(),
        Length(min=1, max=100, message='名称长度必须在1-100个字符之间'),
        Regexp(r'^[a-zA-Z0-9_\u4e00-\u9fa5\s-]+$', message='名称只能包含字母、数字、下划线、中文、空格和短横线')
    ])
    
    description = StringField('描述', [
        Optional(),
        Length(max=500, message='描述长度不能超过500个字符')
    ])
    
    status = IntegerField('状态', [
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])
    
    sort_order = IntegerField('排序', [
        Optional(),
        NumberRange(min=0, max=9999, message='排序值必须在0-9999之间')
    ])
    
    def __init__(self, workspace_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workspace_id = workspace_id
    
    def validate_name(self, field):
        """验证工作空间名称唯一性（排除自己）"""
        if field.data:
            query = Workspace.query.filter_by(name=field.data)
            if self.workspace_id:
                query = query.filter(Workspace.id != self.workspace_id)
            existing = query.first()
            if existing:
                raise ValueError('工作空间名称已存在')