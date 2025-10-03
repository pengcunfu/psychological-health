from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional, Length
from pcf_flask_helper.form.base import BaseForm


class SocialFollowCreateForm(BaseForm):
    """关注创建表单"""
    following_id = StringField('被关注用户ID', [DataRequired(), Length(1, 50)])
    source = StringField('关注来源', [Optional(), Length(max=50)])


class SocialFollowQueryForm(BaseForm):
    """关注查询表单"""
    page = IntegerField('页码', [Optional()], default=1)
    per_page = IntegerField('每页数量', [Optional()], default=20)
    follower_id = StringField('关注者ID', [Optional()])
    following_id = StringField('被关注者ID', [Optional()])
    status = SelectField('状态', [Optional()], choices=[
        ('', '全部'),
        ('active', '有效'),
        ('cancelled', '已取消')
    ], default='active')
    follow_type = SelectField('关注类型', [Optional()], choices=[
        ('', '全部'),
        ('normal', '普通关注'),
        ('mutual', '互相关注')
    ], default='')
    source = StringField('关注来源', [Optional()])
