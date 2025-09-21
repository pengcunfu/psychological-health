"""
邮件发送服务模块
支持发送各种类型的邮件，包含HTML模板和完整的错误处理
"""

import smtplib
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from .config import (
    smtp_config,
    email_config,
    email_templates,
    verification_code_config
)
from loguru import logger


def generate_verification_code(length: int = None) -> str:
    """
    生成验证码
    
    Args:
        length: 验证码长度，默认从配置读取
        
    Returns:
        str: 生成的验证码
    """
    if not length:
        length = verification_code_config.length

    chars = verification_code_config.chars
    return ''.join(random.choice(chars) for _ in range(length))


def load_email_template(template_name: str) -> str:
    """
    加载邮件HTML模板
    
    Args:
        template_name: 模板文件名
        
    Returns:
        str: HTML模板内容
        
    Raises:
        FileNotFoundError: 模板文件不存在
        Exception: 读取模板文件失败
    """
    template_path = os.path.join(os.path.dirname(__file__), template_name)

    if not os.path.exists(template_path):
        error_msg = f"邮件模板文件不存在: {template_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        error_msg = f"加载邮件模板失败: {template_name}, 错误: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg) from e


class EmailService:
    """邮件服务类，用于发送各种类型的邮件"""

    def __init__(self):
        """初始化邮件服务"""
        self.email_config = email_config
        self.smtp_provider = smtp_config.get(email_config.provider)
        self._validate_config()

    def _validate_config(self):
        """验证邮件配置"""
        if not self.smtp_provider:
            raise ValueError(f"不支持的邮件服务商: {self.email_config.provider}")

        if not self.email_config.sender_email:
            raise ValueError("邮件配置缺少必要字段: sender_email")

        if not self.email_config.sender_password:
            raise ValueError("邮件配置缺少必要字段: sender_password")

    def send_email(self, to_email: str, subject: str, html_content: str,
                   text_content: str = None) -> bool:
        """
        发送邮件的通用函数
        
        Args:
            to_email: 收件人邮箱
            subject: 邮件主题
            html_content: HTML内容
            text_content: 纯文本内容（可选）
            
        Returns:
            bool: 成功返回True
            
        Raises:
            ValueError: 参数验证失败
            smtplib.SMTPAuthenticationError: 邮箱认证失败
            smtplib.SMTPRecipientsRefused: 收件人邮箱地址无效
            smtplib.SMTPServerDisconnected: 邮件服务器连接失败
            Exception: 其他发送失败情况
        """
        # 参数验证
        if not to_email:
            raise ValueError("收件人邮箱不能为空")

        if not subject:
            raise ValueError("邮件主题不能为空")

        if not html_content:
            raise ValueError("邮件内容不能为空")

        try:
            # 创建邮件
            message = MIMEMultipart('alternative')
            message['From'] = Header(f"{self.email_config.sender_name} <{self.email_config.sender_email}>", 'utf-8')
            message['To'] = Header(to_email, 'utf-8')
            message['Subject'] = Header(subject, 'utf-8')

            # 添加纯文本内容（如果提供）
            if text_content:
                text_part = MIMEText(text_content, 'plain', 'utf-8')
                message.attach(text_part)

            # 添加HTML内容
            html_part = MIMEText(html_content, 'html', 'utf-8')
            message.attach(html_part)

            # 发送邮件
            with smtplib.SMTP(self.smtp_provider.smtp_server, self.smtp_provider.smtp_port) as server:
                # 启用安全传输
                if self.smtp_provider.use_tls:
                    server.starttls()

                # 登录
                server.login(self.email_config.sender_email, self.email_config.sender_password)

                # 发送邮件
                server.send_message(message)

            logger.info(f"邮件发送成功: {to_email}, 主题: {subject}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            error_msg = "邮箱认证失败，请检查邮箱配置"
            logger.error(f"{error_msg}: {e}")
            raise smtplib.SMTPAuthenticationError(e.smtp_code, error_msg) from e
        except smtplib.SMTPRecipientsRefused as e:
            error_msg = "收件人邮箱地址无效"
            logger.error(f"{error_msg}: {e}")
            raise smtplib.SMTPRecipientsRefused(e.recipients) from e
        except smtplib.SMTPServerDisconnected as e:
            error_msg = "邮件服务器连接失败"
            logger.error(f"{error_msg}: {e}")
            raise smtplib.SMTPServerDisconnected(error_msg) from e
        except Exception as e:
            error_msg = f"发送邮件失败: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) from e

    def send_verification_code(self, to_email: str, verification_code: str = None,
                               expires_minutes: int = None) -> str:
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
        # 如果没有提供验证码，则生成一个
        if not verification_code:
            verification_code = generate_verification_code()

        # 如果没有提供过期时间，使用配置中的默认值
        if not expires_minutes:
            expires_minutes = verification_code_config.expire_minutes

        try:
            # 获取模板配置
            template_config = email_templates.get('verification_code')
            template_file = template_config.template_file

            # 加载邮件模板
            html_template = load_email_template(template_file)

            # 替换模板中的变量
            html_content = html_template.replace('{verification_code}', verification_code)
            html_content = html_content.replace('{expires_minutes}', str(expires_minutes))

            # 获取邮件主题
            subject = template_config.subject

            # 发送邮件
            self.send_email(to_email, subject, html_content)

            return verification_code

        except Exception as e:
            error_msg = f"发送验证码邮件失败: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) from e

    def send_welcome_email(self, to_email: str, username: str = None) -> bool:
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
            # 获取模板配置
            template_config = email_templates.get('welcome')
            template_file = template_config.template_file

            # 加载邮件模板
            html_template = load_email_template(template_file)

            # 替换模板中的变量
            html_content = html_template.replace('{username}', username)

            # 获取邮件主题
            subject = template_config.subject

            return self.send_email(to_email, subject, html_content)

        except Exception as e:
            error_msg = f"发送欢迎邮件失败: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) from e

    def send_password_reset(self, to_email: str, reset_code: str = None,
                            expires_minutes: int = None) -> str:
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
        if not reset_code:
            reset_code = generate_verification_code()

        if not expires_minutes:
            expires_minutes = verification_code_config.expire_minutes

        try:
            # 获取模板配置
            template_config = email_templates.get('password_reset')
            template_file = template_config.template_file

            # 加载邮件模板
            html_template = load_email_template(template_file)

            # 替换模板中的变量
            html_content = html_template.replace('{reset_code}', reset_code)
            html_content = html_content.replace('{expires_minutes}', str(expires_minutes))

            # 获取邮件主题
            subject = template_config.subject

            self.send_email(to_email, subject, html_content)

            return reset_code

        except Exception as e:
            error_msg = f"发送密码重置邮件失败: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) from e

    def send_appointment_reminder(self, to_email: str, appointment_time: str,
                                  doctor_name: str, location: str = None) -> bool:
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
            # 获取模板配置
            template_config = email_templates.get('appointment_reminder')
            template_file = template_config.template_file

            # 加载邮件模板
            html_template = load_email_template(template_file)

            # 准备模板变量
            location_row = ''
            if location:
                location_row = f'''
                <div class="detail-row">
                    <span class="detail-icon">📍</span>
                    <span class="detail-label">咨询地点：</span>
                    <span class="detail-value">{location}</span>
                </div>'''

            # 替换模板中的变量
            html_content = html_template.replace('{appointment_time}', appointment_time)
            html_content = html_content.replace('{doctor_name}', doctor_name)
            html_content = html_content.replace('{location_row}', location_row)

            # 获取邮件主题
            subject = template_config.subject

            return self.send_email(to_email, subject, html_content)

        except Exception as e:
            error_msg = f"发送预约提醒邮件失败: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) from e

    def send_order_notification(self, to_email: str, order_number: str, order_status: str,
                                order_time: str = None, service_name: str = None,
                                order_amount: str = None) -> bool:
        """
        发送订单通知邮件
        
        Args:
            to_email: 收件人邮箱
            order_number: 订单号
            order_status: 订单状态
            order_time: 订单时间
            service_name: 服务名称
            order_amount: 订单金额
            
        Returns:
            bool: 成功返回True
            
        Raises:
            Exception: 发送失败时抛出异常
        """
        try:
            # 获取模板配置
            template_config = email_templates.get('order_notification')
            template_file = template_config.template_file

            # 加载邮件模板
            html_template = load_email_template(template_file)

            # 准备订单状态相关的样式和内容
            status_class = 'pending'
            status_content = ''

            if order_status == '支付成功' or order_status == '已完成':
                status_class = 'success'
                status_content = '''
                <div class="next-steps">
                    <div class="next-steps-title">接下来您可以</div>
                    <ul class="next-steps-list">
                        <li>在"我的订单"中查看服务详情</li>
                        <li>联系客服安排具体的服务时间</li>
                        <li>准备相关的咨询问题和材料</li>
                        <li>关注平台消息获取服务更新</li>
                        </ul>
                    </div>
                '''
            elif order_status == '待支付':
                status_class = 'pending'
                status_content = '''
                <div class="payment-info">
                    <div class="payment-title">支付提醒</div>
                    <p class="payment-text">
                        您的订单还未完成支付，请尽快完成支付以享受我们的专业服务。
                        如果您在支付过程中遇到问题，请联系客服获得帮助。
                    </p>
                </div>
                '''
            elif order_status == '已取消':
                status_class = 'cancelled'
                status_content = '''
                <div class="next-steps">
                    <div class="next-steps-title">订单已取消</div>
                    <ul class="next-steps-list">
                        <li>如果您仍需要相关服务，可以重新下单</li>
                        <li>如有疑问，请联系客服了解详情</li>
                        <li>退款将在3-5个工作日内原路返回</li>
                    </ul>
                </div>
                '''

            # 替换模板中的变量
            html_content = html_template.replace('{order_number}', order_number)
            html_content = html_content.replace('{order_status}', order_status)
            html_content = html_content.replace('{order_status_class}', status_class)
            html_content = html_content.replace('{order_time}', order_time)
            html_content = html_content.replace('{service_name}', service_name)
            html_content = html_content.replace('{order_amount}', order_amount)
            html_content = html_content.replace('{status_specific_content}', status_content)

            # 获取邮件主题
            subject = template_config.subject

            return self.send_email(to_email, subject, html_content)

        except Exception as e:
            error_msg = f"发送订单通知邮件失败: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) from e
