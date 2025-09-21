from .email import EmailService

# 创建全局邮件服务实例
email_service = EmailService()


# 便捷函数
def send_email(to_email: str, subject: str, html_content: str, text_content: str = None) -> bool:
    """
    发送邮件的便捷函数
    
    Args:
        to_email: 收件人邮箱
        subject: 邮件主题
        html_content: HTML内容
        text_content: 纯文本内容
        
    Returns:
        bool: 成功返回True
        
    Raises:
        Exception: 发送失败时抛出异常
    """
    return email_service.send_email(to_email, subject, html_content, text_content)


def send_verification_code(to_email: str, verification_code: str = None,
                           expires_minutes: int = None) -> str:
    """
    发送验证码邮件的便捷函数
    
    Args:
        to_email: 收件人邮箱
        verification_code: 验证码
        expires_minutes: 过期时间（分钟）
        
    Returns:
        str: 生成的验证码
        
    Raises:
        Exception: 发送失败时抛出异常
    """
    return email_service.send_verification_code(to_email, verification_code, expires_minutes)


def send_welcome_email(to_email: str, username: str = None) -> bool:
    """
    发送欢迎邮件的便捷函数
    
    Returns:
        bool: 成功返回True
        
    Raises:
        Exception: 发送失败时抛出异常
    """
    return email_service.send_welcome_email(to_email, username)


def send_password_reset(to_email: str, reset_code: str = None,
                        expires_minutes: int = None) -> str:
    """
    发送密码重置邮件的便捷函数
    
    Returns:
        str: 生成的重置码
        
    Raises:
        Exception: 发送失败时抛出异常
    """
    return email_service.send_password_reset(to_email, reset_code, expires_minutes)


def send_appointment_reminder(to_email: str, appointment_time: str,
                              doctor_name: str, location: str = None) -> bool:
    """
    发送预约提醒邮件的便捷函数
    
    Returns:
        bool: 成功返回True
        
    Raises:
        Exception: 发送失败时抛出异常
    """
    return email_service.send_appointment_reminder(to_email, appointment_time, doctor_name, location)


def send_order_notification(to_email: str, order_number: str, order_status: str,
                            order_time: str = None, service_name: str = None,
                            order_amount: str = None) -> bool:
    """
    发送订单通知邮件的便捷函数
    
    Returns:
        bool: 成功返回True
        
    Raises:
        Exception: 发送失败时抛出异常
    """
    return email_service.send_order_notification(to_email, order_number, order_status,
                                                 order_time, service_name, order_amount)
