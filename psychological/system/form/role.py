from wtforms import StringField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, NumberRange, ValidationError
from psychological.system.models.role import Role
from pcf_flask_helper.form.base import BaseForm


class RoleQueryForm(BaseForm):
    """角色查询表单"""
    page = IntegerField('页码', validators=[
        Optional(),
        NumberRange(min=1, message='页码必须大于0')
    ], default=1)
    
    per_page = IntegerField('每页数量', validators=[
        Optional(),
        NumberRange(min=1, max=100, message='每页数量必须在1-100之间')
    ], default=10)
    
    keyword = StringField('关键词', validators=[
        Optional(),
        Length(max=100, message='关键词长度不能超过100个字符')
    ])



class RoleCreateForm(BaseForm):
    """角色创建表单"""
    name = StringField('角色名称', validators=[
        DataRequired(message='角色名称不能为空'),
        Length(min=1, max=100, message='角色名称长度必须在1-100个字符之间')
    ])
    
    code = StringField('角色编码', validators=[
        DataRequired(message='角色编码不能为空'),
        Length(min=1, max=50, message='角色编码长度必须在1-50个字符之间')
    ])
    
    description = TextAreaField('角色描述', validators=[
        Optional(),
        Length(max=500, message='角色描述不能超过500个字符')
    ])
    
    sort_order = IntegerField('排序', validators=[
        Optional(),
        NumberRange(min=0, message='排序必须大于等于0')
    ], default=0)
    
    data_scope = IntegerField('数据权限', validators=[
        Optional(),
        NumberRange(min=1, max=5, message='数据权限范围必须在1-5之间')
    ], default=1)
    
    menu_ids = StringField('菜单权限', validators=[
        Optional(),
        Length(max=1000, message='菜单权限数据过长')
    ])
    
    status = IntegerField('状态', validators=[
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ], default=1)
    
    is_default = BooleanField('是否默认角色', default=False)
    
    remark = TextAreaField('备注', validators=[
        Optional(),
        Length(max=500, message='备注不能超过500个字符')
    ])

    def validate_code(self, field):
        """验证角色编码唯一性"""
        existing_role = Role.query.filter_by(code=field.data).first()
        if existing_role:
            raise ValidationError('角色编码已存在')


class RoleUpdateForm(BaseForm):
    """角色更新表单"""
    name = StringField('角色名称', validators=[
        Optional(),
        Length(min=1, max=100, message='角色名称长度必须在1-100个字符之间')
    ])
    
    code = StringField('角色编码', validators=[
        Optional(),
        Length(min=1, max=50, message='角色编码长度必须在1-50个字符之间')
    ])
    
    description = TextAreaField('角色描述', validators=[
        Optional(),
        Length(max=500, message='角色描述不能超过500个字符')
    ])
    
    sort_order = IntegerField('排序', validators=[
        Optional(),
        NumberRange(min=0, message='排序必须大于等于0')
    ])
    
    data_scope = IntegerField('数据权限', validators=[
        Optional(),
        NumberRange(min=1, max=5, message='数据权限范围必须在1-5之间')
    ])
    
    menu_ids = StringField('菜单权限', validators=[
        Optional(),
        Length(max=1000, message='菜单权限数据过长')
    ])
    
    status = IntegerField('状态', validators=[
        Optional(),
        NumberRange(min=0, max=1, message='状态值必须为0或1')
    ])
    
    is_default = BooleanField('是否默认角色')
    
    remark = TextAreaField('备注', validators=[
        Optional(),
        Length(max=500, message='备注不能超过500个字符')
    ])

    def __init__(self, role_id=None, *args, **kwargs):
        super(RoleUpdateForm, self).__init__(*args, **kwargs)
        self.role_id = role_id

    def validate_code(self, field):
        """验证角色编码唯一性（排除自己）"""
        if field.data and self.role_id:
            existing_role = Role.query.filter(
                Role.code == field.data,
                Role.id != self.role_id
            ).first()
            if existing_role:
                raise ValidationError('角色编码已存在')