from wtforms import StringField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional, NumberRange, Length
from pcf_flask_helper.form.base import BaseForm


class OrderQueryForm(BaseForm):
    """订单查询表单"""
    user_id = StringField('用户ID', validators=[Optional(), Length(max=36)])
    product_id = StringField('产品ID', validators=[Optional(), Length(max=36)])
    type = SelectField('订单类型', choices=[('', '全部'), ('course', '课程'), ('consultation', '咨询'), ('service', '服务')], validators=[Optional()])
    status = SelectField('订单状态', choices=[('', '全部'), ('pending', '待支付'), ('paid', '已支付'), ('completed', '已完成'), ('cancelled', '已取消'), ('refunded', '已退款')], validators=[Optional()])
    page = IntegerField('页码', validators=[Optional(), NumberRange(min=1)], default=1)
    per_page = IntegerField('每页数量', validators=[Optional(), NumberRange(min=1, max=100)], default=10)

class OrderCreateForm(BaseForm):
    """订单创建表单"""
    user_id = StringField('用户ID', validators=[DataRequired(message='用户ID不能为空'), Length(max=36)])
    product_id = StringField('产品ID', validators=[DataRequired(message='产品ID不能为空'), Length(max=36)])
    type = SelectField('订单类型', choices=[('course', '课程'), ('consultation', '咨询'), ('service', '服务')], validators=[DataRequired(message='订单类型不能为空')])
    amount = FloatField('订单金额', validators=[DataRequired(message='订单金额不能为空'), NumberRange(min=0, message='订单金额不能为负数')])
    status = SelectField('订单状态', choices=[('pending', '待支付'), ('paid', '已支付'), ('completed', '已完成'), ('cancelled', '已取消'), ('refunded', '已退款')], validators=[Optional()], default='pending')


class OrderUpdateForm(BaseForm):
    """订单更新表单"""
    product_id = StringField('产品ID', validators=[Optional(), Length(max=36)])
    type = SelectField('订单类型', choices=[('course', '课程'), ('consultation', '咨询'), ('service', '服务')], validators=[Optional()])
    amount = FloatField('订单金额', validators=[Optional(), NumberRange(min=0, message='订单金额不能为负数')])
    status = SelectField('订单状态', choices=[('pending', '待支付'), ('paid', '已支付'), ('completed', '已完成'), ('cancelled', '已取消'), ('refunded', '已退款')], validators=[Optional()])