"""
阿里云短信服务配置
"""

# 阿里云访问密钥配置
ALIYUN_ACCESS_KEY_ID = 'your_access_key_id'  # 阿里云AccessKey ID
ALIYUN_ACCESS_KEY_SECRET = 'your_access_key_secret'  # 阿里云AccessKey Secret

# 短信服务配置
SMS_REGION = 'cn-hangzhou'  # 地域
SMS_ENDPOINT = 'dysmsapi.aliyuncs.com'  # 接入点

# 短信签名和模板配置
SMS_SIGN_NAME = '心理健康平台'  # 短信签名名称

# 短信模板配置
SMS_TEMPLATES = {
    'verification_code': 'SMS_123456789',  # 验证码模板ID
    'appointment_reminder': 'SMS_987654321',  # 预约提醒模板ID
    'login_notification': 'SMS_456789123',  # 登录通知模板ID
    'password_reset': 'SMS_789123456',  # 密码重置模板ID
    'order_notification': 'SMS_321654987',  # 订单通知模板ID
}

# 短信发送限制配置
SMS_RATE_LIMIT = {
    'per_minute': 5,  # 每分钟最多发送条数
    'per_hour': 20,   # 每小时最多发送条数
    'per_day': 100,   # 每天最多发送条数
}

# 验证码配置
VERIFICATION_CODE = {
    'length': 6,      # 验证码长度
    'expire_minutes': 5,  # 验证码过期时间（分钟）
    'chars': '0123456789',  # 验证码字符集
}
