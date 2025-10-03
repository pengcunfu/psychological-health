from pcf_flask_helper.mail import EmailService, EmailConfig, EmailProvider
from psychological.config import cfg


# 初始化邮件服务
def get_email_service() -> EmailService:
    """获取邮件服务实例"""
    email_config = EmailConfig(
        sender_email=cfg.get("email.sender_email"),
        sender_password=cfg.get("email.sender_password"),
        sender_name=cfg.get("email.sender_name", "心理健康平台")
    )

    smtp_provider = EmailProvider(
        smtp_server=cfg.get("email.smtp_server", "smtp.qq.com"),
        smtp_port=cfg.get("email.smtp_port", 587),
        use_tls=cfg.get("email.use_tls", True),
        use_ssl=cfg.get("email.use_ssl", False)
    )

    return EmailService(email_config, smtp_provider)


def send_verification_code(to_email: str, verification_code,
                           expires_minutes: int = 7200) -> bool:
    """
    发送验证码邮件

    Args:
        to_email: 收件人邮箱
        verification_code: 验证码，如果不提供则自动生成
        expires_minutes: 验证码有效期（分钟），默认从配置读取

    Returns:
        str: 生成的验证码

    Raises:
        Exception: 发送失败时抛出异常
    """

    try:
        # 获取邮件服务
        email_service = get_email_service()

        # 读取模板文件
        import os
        template_path = os.path.join(os.path.dirname(__file__), "verification_code.html")
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()

        # 获取模板配置
        template_config = {
            "verification_code": verification_code,
            "expires_minutes": str(expires_minutes)
        }

        return email_service.send_template_email(to_email, "邮箱验证码", html_template, template_config)
    except Exception as e:
        raise Exception(f"发送验证码邮件失败: {str(e)}") from e


def send_welcome_email(to_email: str, username: str) -> bool:
    """
    发送欢迎邮件

    Args:
        to_email: 收件人邮箱
        username: 用户名

    Returns:
        bool: 成功返回True

    Raises:
        Exception: 发送失败时抛出异常
    """
    try:
        # 获取邮件服务
        email_service = get_email_service()

        # 读取模板文件
        import os
        template_path = os.path.join(os.path.dirname(__file__), "welcome.html")
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()

        # 获取模板配置
        template_config = {
            "username": username
        }

        return email_service.send_template_email(to_email, "欢迎加入心理健康平台", html_template, template_config)

    except Exception as e:
        raise Exception(f"发送欢迎邮件失败: {str(e)}") from e


def send_password_reset(to_email: str, reset_code: str, expires_minutes: int = 7200) -> bool:
    """
    发送密码重置邮件

    Args:
        to_email: 收件人邮箱
        reset_code: 重置码，如果不提供则自动生成
        expires_minutes: 重置码有效期（分钟）

    Returns:
        str: 生成的重置码

    Raises:
        Exception: 发送失败时抛出异常
    """

    try:
        # 获取邮件服务
        email_service = get_email_service()

        # 读取模板文件
        import os
        template_path = os.path.join(os.path.dirname(__file__), "password_reset.html")
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()

        # 获取模板配置
        template_config = {
            "reset_code": reset_code,
            "expires_minutes": str(expires_minutes)
        }

        return email_service.send_template_email(to_email, "密码重置验证码", html_template, template_config)

    except Exception as e:
        raise Exception(f"发送密码重置邮件失败: {str(e)}") from e


def send_appointment_reminder(to_email: str, appointment_time: str,
                              doctor_name: str, location: str) -> bool:
    """
    发送预约提醒邮件

    Args:
        to_email: 收件人邮箱
        appointment_time: 预约时间
        doctor_name: 医生姓名
        location: 预约地点

    Returns:
        bool: 成功返回True

    Raises:
        Exception: 发送失败时抛出异常
    """
    try:
        # 获取邮件服务
        email_service = get_email_service()

        # 读取模板文件
        import os
        template_path = os.path.join(os.path.dirname(__file__), "appointment_reminder.html")
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()

        template_config = {
            "appointment_time": appointment_time,
            "doctor_name": doctor_name,
            "location": location
        }

        return email_service.send_template_email(to_email, "预约提醒", html_template, template_config)
    except Exception as e:
        raise Exception(f"发送预约提醒邮件失败: {str(e)}") from e


def send_order_notification(to_email: str, order_number: str, order_status: str,
                            order_time: str, service_name: str,
                            order_amount: str) -> bool:
    """
    发送订单通知邮件

    Args:
        to_email: 收件人邮箱
        order_number: 订单号
        order_status: 订单状态 (支付成功/已完成/待支付/已取消)
        order_time: 订单时间
        service_name: 服务名称
        order_amount: 订单金额

    Returns:
        bool: 成功返回True

    Raises:
        Exception: 发送失败时抛出异常
    """
    try:
        # 根据订单状态确定样式类
        status_class = 'pending'
        if order_status in ['支付成功', '已完成']:
            status_class = 'success'
        elif order_status == '待支付':
            status_class = 'pending'
        elif order_status == '已取消':
            status_class = 'cancelled'

        # 准备模板配置
        template_config = {
            "order_number": order_number,
            "order_status": order_status,
            "status_class": status_class,
            "order_time": order_time,
            "service_name": service_name,
            "order_amount": order_amount
        }

        # 获取邮件服务
        email_service = get_email_service()

        # 读取模板文件
        import os
        template_path = os.path.join(os.path.dirname(__file__), "order_notification.html")
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()

        return email_service.send_template_email(to_email, "订单通知", html_template, template_config)
    except Exception as e:
        raise Exception(f"发送订单通知邮件失败: {str(e)}") from e
