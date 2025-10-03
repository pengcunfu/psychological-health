from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length
from pcf_flask_helper.form.base import BaseForm


class SocialLikeCreateForm(BaseForm):
    """点赞创建表单"""
    target_id = StringField('目标ID', [DataRequired(), Length(1, 50)])
    target_type = SelectField('目标类型', [DataRequired()], choices=[
        ('post', '帖子'),
        ('comment', '评论')
    ])
