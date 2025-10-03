"""
邮件服务配置
"""
from ..config import get_config


class EmailProvider:
    smtp_server: str
    smtp_port: int
    use_tls: bool
    use_ssl: bool

    def __init__(self, smtp_server: str, smtp_port: int, use_tls: bool, use_ssl: bool):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.use_tls = use_tls
        self.use_ssl = use_ssl


# SMTP服务器配置
smtp_config = {
    # QQ邮箱配置示例
    'qq': EmailProvider(smtp_server='smtp.qq.com', smtp_port=587, use_tls=True, use_ssl=False),
    # 163邮箱配置示例
    '163': EmailProvider(smtp_server='smtp.163.com', smtp_port=25, use_tls=True, use_ssl=False),
    # Gmail配置示例
    'gmail': EmailProvider(smtp_server='smtp.gmail.com', smtp_port=587, use_tls=True, use_ssl=False),
    # 企业邮箱配置示例
    'enterprise': EmailProvider(smtp_server='smtp.your-domain.com', smtp_port=587, use_tls=True, use_ssl=False),
}


class EmailConfig:
    provider: str
    sender_email: str
    sender_password: str
    sender_name: str

    def __init__(self, provider: str, sender_email: str, sender_password: str, sender_name: str):
        self.provider = provider
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_name = sender_name


email_config = EmailConfig(
    provider='qq',
    sender_email=get_config('email.sender_email'),
    sender_password=get_config('email.sender_password'),
    sender_name='心理健康平台')


class EmailTemplate:
    subject: str
    template_file: str

    def __init__(self, subject: str, template_file: str):
        self.subject = subject
        self.template_file = template_file


# 邮件模板配置
email_templates = {
    'verification_code': EmailTemplate(subject='邮箱验证码', template_file='verification_code.html'),
    'welcome': EmailTemplate(subject='欢迎加入心理健康平台', template_file='welcome.html'),
    'password_reset': EmailTemplate(subject='密码重置验证码', template_file='password_reset.html'),
    'appointment_reminder': EmailTemplate(subject='预约提醒', template_file='appointment_reminder.html'),
    'order_notification': EmailTemplate(subject='订单通知', template_file='order_notification.html'),
}


class VerificationCodeConfig:
    length: int
    expire_minutes: int
    chars: str

    def __init__(self, length: int, expire_minutes: int, chars: str):
        self.length = length
        self.expire_minutes = expire_minutes
        self.chars = chars


# 验证码配置
verification_code_config = VerificationCodeConfig(
    length=6,  # 验证码长度
    expire_minutes=10,  # 验证码过期时间（分钟）
    chars='0123456789'  # 验证码字符集
)


class EmailRateLimit:
    per_minute: int
    per_hour: int
    per_day: int

    def __init__(self, per_minute: int, per_hour: int, per_day: int):
        self.per_minute = per_minute
        self.per_hour = per_hour
        self.per_day = per_day


# 邮件发送限制配置
email_rate_limit = EmailRateLimit(
    per_minute=10,  # 每分钟最多发送邮件数
    per_hour=100,  # 每小时最多发送邮件数
    per_day=500  # 每天最多发送邮件数
)
