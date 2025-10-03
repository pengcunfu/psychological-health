from pcf_flask_helper.form.base import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Optional, Length, NumberRange


class MenuQueryForm(BaseForm):
    keyword = StringField(validators=[Optional(), Length(max=100)])
    page = IntegerField(validators=[Optional(), NumberRange(min=1)], default=1)
    size = IntegerField(validators=[Optional(), NumberRange(min=1, max=100)], default=10)




class MenuCreateForm(BaseForm):
    name = StringField(validators=[InputRequired(message="菜单名称是必填项"), Length(max=100, message="菜单名称长度不能超过100个字符")])
    path = StringField(validators=[Optional(), Length(max=255, message="路径长度不能超过255个字符")])
    icon = StringField(validators=[Optional(), Length(max=100, message="图标长度不能超过100个字符")])
    parent_id = StringField(validators=[Optional(), Length(max=36, message="父级菜单ID长度不能超过36个字符")])
    level = IntegerField(validators=[Optional(), NumberRange(min=0, message="菜单层级不能小于0")])
    sort_order = IntegerField(validators=[Optional(), NumberRange(min=0, message="排序值不能小于0")])
    menu_type = IntegerField(validators=[Optional(), NumberRange(min=0, max=2, message="菜单类型必须在0-2之间")])
    permission = StringField(validators=[Optional(), Length(max=100, message="权限标识长度不能超过100个字符")])
    component = StringField(validators=[Optional(), Length(max=255, message="组件路径长度不能超过255个字符")])
    is_external = IntegerField(validators=[Optional(), NumberRange(min=0, max=1, message="是否外链必须为0或1")])
    is_visible = IntegerField(validators=[Optional(), NumberRange(min=0, max=1, message="是否显示必须为0或1")])
    is_cache = IntegerField(validators=[Optional(), NumberRange(min=0, max=1, message="是否缓存必须为0或1")])
    status = IntegerField(validators=[Optional(), NumberRange(min=0, max=1, message="状态必须为0或1")])
    remark = StringField(validators=[Optional(), Length(max=500, message="备注长度不能超过500个字符")])


class MenuUpdateForm(BaseForm):
    name = StringField(validators=[Optional(), Length(max=100, message="菜单名称长度不能超过100个字符")])
    path = StringField(validators=[Optional(), Length(max=255, message="路径长度不能超过255个字符")])
    icon = StringField(validators=[Optional(), Length(max=100, message="图标长度不能超过100个字符")])
    parent_id = StringField(validators=[Optional(), Length(max=36, message="父级菜单ID长度不能超过36个字符")])
    level = IntegerField(validators=[Optional(), NumberRange(min=0, message="菜单层级不能小于0")])
    sort_order = IntegerField(validators=[Optional(), NumberRange(min=0, message="排序值不能小于0")])
    menu_type = IntegerField(validators=[Optional(), NumberRange(min=0, max=2, message="菜单类型必须在0-2之间")])
    permission = StringField(validators=[Optional(), Length(max=100, message="权限标识长度不能超过100个字符")])
    component = StringField(validators=[Optional(), Length(max=255, message="组件路径长度不能超过255个字符")])
    is_external = IntegerField(validators=[Optional(), NumberRange(min=0, max=1, message="是否外链必须为0或1")])
    is_visible = IntegerField(validators=[Optional(), NumberRange(min=0, max=1, message="是否显示必须为0或1")])
    is_cache = IntegerField(validators=[Optional(), NumberRange(min=0, max=1, message="是否缓存必须为0或1")])
    status = IntegerField(validators=[Optional(), NumberRange(min=0, max=1, message="状态必须为0或1")])
    remark = StringField(validators=[Optional(), Length(max=500, message="备注长度不能超过500个字符")])