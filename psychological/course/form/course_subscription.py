from wtforms import StringField, FloatField, IntegerField, DateTimeField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, NumberRange, Length
from .base import BaseForm


class CourseSubscriptionCreateForm(BaseForm):
    """创建课程订阅表单"""
    course_id = StringField('课程ID', validators=[DataRequired(message='课程ID不能为空')])
    subscription_type = SelectField('订阅类型', 
                                   choices=[('standard', '标准'), ('premium', '高级')],
                                   default='standard',
                                   validators=[Optional()])
    paid_price = FloatField('支付价格', 
                           validators=[DataRequired(message='支付价格不能为空'),
                                     NumberRange(min=0, message='支付价格不能为负数')])
    original_price = FloatField('原价', 
                               validators=[DataRequired(message='原价不能为空'),
                                         NumberRange(min=0, message='原价不能为负数')])
    discount_amount = FloatField('折扣金额', 
                                validators=[Optional(),
                                          NumberRange(min=0, message='折扣金额不能为负数')])
    order_id = StringField('订单ID', validators=[Optional()])
    payment_method = StringField('支付方式', validators=[Optional()])
    payment_transaction_id = StringField('支付交易ID', validators=[Optional()])
    notes = TextAreaField('备注', validators=[Optional(), Length(max=500, message='备注不能超过500字符')])


class CourseSubscriptionUpdateForm(BaseForm):
    """更新课程订阅表单"""
    subscription_type = SelectField('订阅类型', 
                                   choices=[('standard', '标准'), ('premium', '高级')],
                                   validators=[Optional()])
    status = SelectField('状态', 
                        choices=[('active', '有效'), ('expired', '已过期'), ('cancelled', '已取消')],
                        validators=[Optional()])
    completed_lessons = IntegerField('已完成课时', 
                                   validators=[Optional(),
                                             NumberRange(min=0, message='已完成课时不能为负数')])
    total_study_time = IntegerField('总学习时间', 
                                  validators=[Optional(),
                                            NumberRange(min=0, message='学习时间不能为负数')])
    notes = TextAreaField('备注', validators=[Optional(), Length(max=500, message='备注不能超过500字符')])


class CourseSubscriptionListForm(BaseForm):
    """课程订阅列表查询表单"""
    page = IntegerField('页码', validators=[Optional(), NumberRange(min=1, message='页码必须大于0')])
    per_page = IntegerField('每页数量', validators=[Optional(), NumberRange(min=1, max=100, message='每页数量必须在1-100之间')])
    user_id = StringField('用户ID', validators=[Optional()])
    course_id = StringField('课程ID', validators=[Optional()])
    status = SelectField('状态', 
                        choices=[('', '全部'), ('active', '有效'), ('expired', '已过期'), ('cancelled', '已取消')],
                        validators=[Optional()])
    subscription_type = SelectField('订阅类型', 
                                   choices=[('', '全部'), ('standard', '标准'), ('premium', '高级')],
                                   validators=[Optional()])


class ProgressUpdateForm(BaseForm):
    """学习进度更新表单"""
    completed_lessons = IntegerField('已完成课时', 
                                   validators=[Optional(),
                                             NumberRange(min=0, message='已完成课时不能为负数')])
    study_time_minutes = IntegerField('本次学习时间（分钟）', 
                                    validators=[Optional(),
                                              NumberRange(min=0, message='学习时间不能为负数')])


class SubscriptionExtendForm(BaseForm):
    """订阅延期表单"""
    days = IntegerField('延期天数', 
                       validators=[DataRequired(message='延期天数不能为空'),
                                 NumberRange(min=1, max=365, message='延期天数必须在1-365天之间')])


class SubscriptionCancelForm(BaseForm):
    """订阅取消表单"""
    reason = StringField('取消原因', validators=[Optional(), Length(max=200, message='取消原因不能超过200字符')])
