from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional

from .base import BaseForm


class UserFavoriteCreateForm(BaseForm):
    user_id = StringField(
        validators=[DataRequired(message='用户ID不能为空'), Length(min=1, max=50, message='用户ID长度为1-50个字符')])
    item_id = StringField(validators=[DataRequired(message='收藏项ID不能为空'),
                                      Length(min=1, max=50, message='收藏项ID长度为1-50个字符')])
    item_type = StringField(validators=[DataRequired(message='收藏项类型不能为空'),
                                        Length(min=1, max=50, message='收藏项类型长度为1-50个字符')])


class UserFavoriteQueryForm(BaseForm):
    page = IntegerField(validators=[Optional()])
    per_page = IntegerField(validators=[Optional()])
    user_id = StringField(validators=[Optional(), Length(min=1, max=50, message='用户ID长度为1-50个字符')])
    item_type = StringField(validators=[Optional(), Length(min=1, max=50, message='收藏项类型长度为1-50个字符')])
    item_id = StringField(validators=[Optional(), Length(min=1, max=50, message='收藏项ID长度为1-50个字符')])

    def get_page(self):
        return self.page.data or 1

    def get_per_page(self):
        return self.per_page.data or 10

    def get_user_id(self):
        return self.user_id.data

    def get_item_type(self):
        return self.item_type.data

    def get_item_id(self):
        return self.item_id.data
