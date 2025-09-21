"""
通知相关表单验证
"""
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, DateTimeField, SelectField
from wtforms.fields import FieldList
from wtforms.validators import DataRequired, Length, Optional, NumberRange, ValidationError
import json


class NotificationQueryForm(FlaskForm):
    """通知查询表单"""
    status = SelectField('状态', choices=[
        ('', '全部'),
        ('unread', '未读'),
        ('read', '已读'),
        ('archived', '已归档')
    ], validators=[Optional()])
    
    type = SelectField('类型', choices=[
        ('', '全部'),
        ('system', '系统通知'),
        ('announcement', '公告通知'),
        ('appointment', '预约通知'),
        ('order', '订单通知'),
        ('course', '课程通知'),
        ('assessment', '测评通知'),
        ('social_follow', '关注通知'),
        ('social_like', '点赞通知'),
        ('social_comment', '评论通知'),
        ('account', '账户通知'),
        ('security', '安全通知'),
        ('reminder', '提醒通知'),
        ('promotion', '推广通知')
    ], validators=[Optional()])
    
    page = IntegerField('页码', default=1, validators=[NumberRange(min=1)])
    per_page = IntegerField('每页数量', default=20, validators=[NumberRange(min=1, max=100)])
    include_expired = BooleanField('包含过期通知', default=False)


class NotificationCreateForm(FlaskForm):
    """通知创建表单"""
    recipient_id = StringField('接收者ID', validators=[DataRequired(), Length(max=50)])
    
    # 直接创建字段
    title = StringField('标题', validators=[Optional(), Length(max=200)])
    content = TextAreaField('内容', validators=[Optional(), Length(max=5000)])
    summary = StringField('摘要', validators=[Optional(), Length(max=500)])
    
    # 模板创建字段
    template_code = StringField('模板代码', validators=[Optional(), Length(max=100)])
    variables = TextAreaField('模板变量', validators=[Optional()])
    
    # 通知属性
    type = SelectField('类型', choices=[
        ('system', '系统通知'),
        ('announcement', '公告通知'),
        ('appointment', '预约通知'),
        ('order', '订单通知'),
        ('course', '课程通知'),
        ('assessment', '测评通知'),
        ('social_follow', '关注通知'),
        ('social_like', '点赞通知'),
        ('social_comment', '评论通知'),
        ('account', '账户通知'),
        ('security', '安全通知'),
        ('reminder', '提醒通知'),
        ('promotion', '推广通知')
    ], default='system', validators=[DataRequired()])
    
    priority = SelectField('优先级', choices=[
        ('low', '低'),
        ('normal', '普通'),
        ('high', '高'),
        ('urgent', '紧急')
    ], default='normal', validators=[Optional()])
    
    # 关联信息
    related_id = StringField('关联对象ID', validators=[Optional(), Length(max=50)])
    related_type = StringField('关联对象类型', validators=[Optional(), Length(max=50)])
    action_url = StringField('动作URL', validators=[Optional(), Length(max=500)])
    
    # 时间配置
    scheduled_time = DateTimeField('定时发送时间', validators=[Optional()])
    expire_time = DateTimeField('过期时间', validators=[Optional()])
    
    def validate_variables(self, field):
        """验证模板变量格式"""
        if field.data:
            try:
                json.loads(field.data)
            except json.JSONDecodeError:
                raise ValidationError('模板变量必须是有效的JSON格式')
    
    def validate(self):
        """自定义验证"""
        if not super().validate():
            return False
        
        # 模板创建和直接创建必须选择一种
        if self.template_code.data:
            # 使用模板创建
            if not self.template_code.data:
                self.template_code.errors.append('使用模板创建时模板代码不能为空')
                return False
        else:
            # 直接创建
            if not self.title.data:
                self.title.errors.append('直接创建时标题不能为空')
                return False
        
        # 验证定时发送时间
        if self.scheduled_time.data and self.scheduled_time.data <= datetime.utcnow():
            self.scheduled_time.errors.append('定时发送时间必须晚于当前时间')
            return False
        
        return True


class NotificationBulkCreateForm(FlaskForm):
    """批量通知创建表单"""
    user_ids = FieldList(StringField('用户ID', validators=[DataRequired()]), min_entries=1)
    
    # 通知内容
    title = StringField('标题', validators=[Optional(), Length(max=200)])
    content = TextAreaField('内容', validators=[Optional(), Length(max=5000)])
    
    # 模板创建字段
    template_code = StringField('模板代码', validators=[Optional(), Length(max=100)])
    variables = TextAreaField('模板变量', validators=[Optional()])
    
    # 通知属性
    type = SelectField('类型', choices=[
        ('system', '系统通知'),
        ('announcement', '公告通知'),
        ('appointment', '预约通知'),
        ('order', '订单通知'),
        ('course', '课程通知'),
        ('assessment', '测评通知'),
        ('social_follow', '关注通知'),
        ('social_like', '点赞通知'),
        ('social_comment', '评论通知'),
        ('account', '账户通知'),
        ('security', '安全通知'),
        ('reminder', '提醒通知'),
        ('promotion', '推广通知')
    ], default='system', validators=[DataRequired()])
    
    priority = SelectField('优先级', choices=[
        ('low', '低'),
        ('normal', '普通'),
        ('high', '高'),
        ('urgent', '紧急')
    ], default='normal', validators=[Optional()])
    
    # 时间配置
    scheduled_time = DateTimeField('定时发送时间', validators=[Optional()])
    expire_time = DateTimeField('过期时间', validators=[Optional()])
    
    def validate_variables(self, field):
        """验证模板变量格式"""
        if field.data:
            try:
                json.loads(field.data)
            except json.JSONDecodeError:
                raise ValidationError('模板变量必须是有效的JSON格式')
    
    def validate_user_ids(self, field):
        """验证用户ID列表"""
        if len(field.data) > 1000:
            raise ValidationError('批量发送用户数量不能超过1000')


class NotificationUpdateForm(FlaskForm):
    """通知更新表单"""
    title = StringField('标题', validators=[Optional(), Length(max=200)])
    content = TextAreaField('内容', validators=[Optional(), Length(max=5000)])
    summary = StringField('摘要', validators=[Optional(), Length(max=500)])
    
    priority = SelectField('优先级', choices=[
        ('low', '低'),
        ('normal', '普通'),
        ('high', '高'),
        ('urgent', '紧急')
    ], validators=[Optional()])
    
    expire_time = DateTimeField('过期时间', validators=[Optional()])
    is_pinned = BooleanField('是否置顶', default=False)


class NotificationMarkReadForm(FlaskForm):
    """标记通知已读表单"""
    notification_ids = FieldList(StringField('通知ID'), min_entries=0)
    type = SelectField('类型', choices=[
        ('', '全部'),
        ('system', '系统通知'),
        ('announcement', '公告通知'),
        ('appointment', '预约通知'),
        ('order', '订单通知'),
        ('course', '课程通知'),
        ('assessment', '测评通知'),
        ('social_follow', '关注通知'),
        ('social_like', '点赞通知'),
        ('social_comment', '评论通知'),
        ('account', '账户通知'),
        ('security', '安全通知'),
        ('reminder', '提醒通知'),
        ('promotion', '推广通知')
    ], validators=[Optional()])


class NotificationConfigForm(FlaskForm):
    """用户通知配置表单"""
    type = SelectField('通知类型', choices=[
        ('system', '系统通知'),
        ('announcement', '公告通知'),
        ('appointment', '预约通知'),
        ('order', '订单通知'),
        ('course', '课程通知'),
        ('assessment', '测评通知'),
        ('social_follow', '关注通知'),
        ('social_like', '点赞通知'),
        ('social_comment', '评论通知'),
        ('account', '账户通知'),
        ('security', '安全通知'),
        ('reminder', '提醒通知'),
        ('promotion', '推广通知')
    ], validators=[DataRequired()])
    
    # 渠道开关
    in_app_enabled = BooleanField('启用站内通知', default=True)
    email_enabled = BooleanField('启用邮件通知', default=True)
    sms_enabled = BooleanField('启用短信通知', default=False)
    push_enabled = BooleanField('启用推送通知', default=True)
    
    # 免打扰时间
    quiet_start_time = StringField('免打扰开始时间', validators=[Optional(), Length(max=5)])
    quiet_end_time = StringField('免打扰结束时间', validators=[Optional(), Length(max=5)])
    
    # 频率控制
    max_daily_count = IntegerField('每日最大通知数', validators=[Optional(), NumberRange(min=1, max=100)])
    max_hourly_count = IntegerField('每小时最大通知数', validators=[Optional(), NumberRange(min=1, max=20)])
    
    # 优先级过滤
    min_priority = SelectField('最低接收优先级', choices=[
        ('low', '低'),
        ('normal', '普通'),
        ('high', '高'),
        ('urgent', '紧急')
    ], default='low', validators=[Optional()])
    
    def validate_quiet_start_time(self, field):
        """验证免打扰开始时间格式"""
        if field.data:
            try:
                datetime.strptime(field.data, '%H:%M')
            except ValueError:
                raise ValidationError('时间格式错误，请使用 HH:MM 格式')
    
    def validate_quiet_end_time(self, field):
        """验证免打扰结束时间格式"""
        if field.data:
            try:
                datetime.strptime(field.data, '%H:%M')
            except ValueError:
                raise ValidationError('时间格式错误，请使用 HH:MM 格式')


class NotificationTemplateCreateForm(FlaskForm):
    """通知模板创建表单"""
    name = StringField('模板名称', validators=[DataRequired(), Length(max=100)])
    code = StringField('模板代码', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('模板描述', validators=[Optional(), Length(max=500)])
    
    type = SelectField('通知类型', choices=[
        ('system', '系统通知'),
        ('announcement', '公告通知'),
        ('appointment', '预约通知'),
        ('order', '订单通知'),
        ('course', '课程通知'),
        ('assessment', '测评通知'),
        ('social_follow', '关注通知'),
        ('social_like', '点赞通知'),
        ('social_comment', '评论通知'),
        ('account', '账户通知'),
        ('security', '安全通知'),
        ('reminder', '提醒通知'),
        ('promotion', '推广通知')
    ], validators=[DataRequired()])
    
    # 模板内容
    title_template = StringField('标题模板', validators=[DataRequired(), Length(max=500)])
    content_template = TextAreaField('内容模板', validators=[Optional(), Length(max=2000)])
    summary_template = StringField('摘要模板', validators=[Optional(), Length(max=1000)])
    
    # 默认配置
    priority = SelectField('默认优先级', choices=[
        ('low', '低'),
        ('normal', '普通'),
        ('high', '高'),
        ('urgent', '紧急')
    ], default='normal', validators=[Optional()])
    
    icon = StringField('默认图标', validators=[Optional(), Length(max=200)])
    color = StringField('默认颜色', validators=[Optional(), Length(max=20)])
    
    # 模板变量定义
    variables = TextAreaField('变量定义', validators=[Optional()])
    
    def validate_variables(self, field):
        """验证变量定义格式"""
        if field.data:
            try:
                json.loads(field.data)
            except json.JSONDecodeError:
                raise ValidationError('变量定义必须是有效的JSON格式')


class NotificationStatsForm(FlaskForm):
    """通知统计查询表单"""
    user_id = StringField('用户ID', validators=[Optional(), Length(max=50)])
    start_date = DateTimeField('开始日期', validators=[Optional()])
    end_date = DateTimeField('结束日期', validators=[Optional()])
    
    def validate_end_date(self, field):
        """验证结束日期"""
        if field.data and self.start_date.data:
            if field.data < self.start_date.data:
                raise ValidationError('结束日期不能早于开始日期')
