from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError
from models.review import Review
from models.order import Order
from models.counselor import Counselor
from .base import BaseForm


class ReviewCreateForm(BaseForm):
    """评价创建表单"""
    counselor_id = StringField('咨询师ID', validators=[
        DataRequired(message='咨询师ID不能为空'),
        Length(min=1, max=36, message='咨询师ID长度必须在1-36个字符之间')
    ])

    order_id = StringField('订单ID', validators=[
        DataRequired(message='订单ID不能为空'),
        Length(min=1, max=36, message='订单ID长度必须在1-36个字符之间')
    ])

    content = TextAreaField('评价内容', validators=[
        Optional(),
        Length(max=1000, message='评价内容不能超过1000个字符')
    ])

    rating = IntegerField('评分', validators=[
        Optional(),
        NumberRange(min=1, max=5, message='评分必须在1-5之间')
    ], default=5)

    def validate_order_id(self, field):
        """验证订单是否存在且未被评价"""
        # 检查订单是否存在
        order = Order.query.filter_by(id=field.data).first()
        if not order:
            raise ValidationError('订单不存在')

        # 检查订单是否已有评价
        existing_review = Review.query.filter_by(order_id=field.data).first()
        if existing_review:
            raise ValidationError('该订单已有评价')

    def validate_counselor_id(self, field):
        """验证咨询师是否存在"""
        counselor = Counselor.query.filter_by(id=field.data).first()
        if not counselor:
            raise ValidationError('咨询师不存在')


class ReviewUpdateForm(BaseForm):
    """评价更新表单"""
    content = TextAreaField('评价内容', validators=[
        Optional(),
        Length(max=1000, message='评价内容不能超过1000个字符')
    ])

    rating = IntegerField('评分', validators=[
        Optional(),
        NumberRange(min=1, max=5, message='评分必须在1-5之间')
    ])

    def __init__(self, review_id=None, *args, **kwargs):
        super(ReviewUpdateForm, self).__init__(*args, **kwargs)
        self.review_id = review_id


class ReviewQueryForm(BaseForm):
    """评价查询表单"""
    page = IntegerField('页码', validators=[
        Optional(),
        NumberRange(min=1, message='页码必须大于0')
    ], default=1)

    per_page = IntegerField('每页数量', validators=[
        Optional(),
        NumberRange(min=1, max=100, message='每页数量必须在1-100之间')
    ], default=10)

    counselor_id = StringField('咨询师ID', validators=[
        Optional(),
        Length(min=1, max=36, message='咨询师ID长度必须在1-36个字符之间')
    ])

    order_id = StringField('订单ID', validators=[
        Optional(),
        Length(min=1, max=36, message='订单ID长度必须在1-36个字符之间')
    ])

    def get_page(self):
        return self.page.data if self.page.data is not None else 1

    def get_per_page(self):
        return self.per_page.data if self.per_page.data is not None else 10

    def get_counselor_id(self):
        return self.counselor_id.data

    def get_order_id(self):
        return self.order_id.data

    def validate_counselor_id(self, field):
        """验证咨询师是否存在（如果提供了ID）"""
        if field.data:
            counselor = Counselor.query.filter_by(id=field.data).first()
            if not counselor:
                raise ValidationError('咨询师不存在')

    def validate_order_id(self, field):
        """验证订单是否存在（如果提供了ID）"""
        if field.data:
            order = Order.query.filter_by(id=field.data).first()
            if not order:
                raise ValidationError('订单不存在')
