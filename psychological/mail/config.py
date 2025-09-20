"""
邮件服务配置
"""

# SMTP服务器配置
SMTP_CONFIG = {
    # QQ邮箱配置示例
    'qq': {
        'smtp_server': 'smtp.qq.com',
        'smtp_port': 587,
        'use_tls': True,
        'use_ssl': False,
    },
    # 163邮箱配置示例
    '163': {
        'smtp_server': 'smtp.163.com',
        'smtp_port': 25,
        'use_tls': True,
        'use_ssl': False,
    },
    # Gmail配置示例
    'gmail': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'use_tls': True,
        'use_ssl': False,
    },
    # 企业邮箱配置示例
    'enterprise': {
        'smtp_server': 'smtp.your-domain.com',
        'smtp_port': 587,
        'use_tls': True,
        'use_ssl': False,
    }
}

# 邮件发送配置
EMAIL_CONFIG = {
    'provider': 'qq',  # 选择邮件服务商：qq, 163, gmail, enterprise
    'sender_email': 'your_email@qq.com',  # 发件人邮箱
    'sender_password': 'your_email_password',  # 发件人邮箱密码或授权码
    'sender_name': '心理健康平台',  # 发件人名称
}

# 邮件模板配置
EMAIL_TEMPLATES = {
    'verification_code': {
        'subject': '邮箱验证码',
        'template_file': 'verification_code.html'
    },
    'welcome': {
        'subject': '欢迎加入心理健康平台',
        'template_file': 'welcome.html'
    },
    'password_reset': {
        'subject': '密码重置验证码',
        'template_file': 'password_reset.html'
    },
    'appointment_reminder': {
        'subject': '预约提醒',
        'template_file': 'appointment_reminder.html'
    },
    'order_notification': {
        'subject': '订单通知',
        'template_file': 'order_notification.html'
    }
}

# 验证码配置
VERIFICATION_CODE_CONFIG = {
    'length': 6,  # 验证码长度
    'expire_minutes': 10,  # 验证码过期时间（分钟）
    'chars': '0123456789',  # 验证码字符集
}

# 邮件发送限制配置
EMAIL_RATE_LIMIT = {
    'per_minute': 10,  # 每分钟最多发送邮件数
    'per_hour': 100,   # 每小时最多发送邮件数
    'per_day': 500,    # 每天最多发送邮件数
}
