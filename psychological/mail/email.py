"""
邮件发送服务模块
支持发送各种类型的邮件，包含HTML模板和完整的错误处理
"""

import smtplib
import os
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Optional, Dict, Any

from .config import (
    SMTP_CONFIG, 
    EMAIL_CONFIG, 
    EMAIL_TEMPLATES, 
    VERIFICATION_CODE_CONFIG
)
from ..utils.logger_client import get_logger
from ..utils.json_result import success_result, error_result

logger = get_logger(__name__)


class EmailService:
    """邮件服务类，用于发送各种类型的邮件"""

    def __init__(self):
        """初始化邮件服务"""
        self.email_config = EMAIL_CONFIG
        self.smtp_config = SMTP_CONFIG.get(EMAIL_CONFIG['provider'], {})
        self._validate_config()

    def _validate_config(self):
        """验证邮件配置"""
        if not self.smtp_config:
            raise ValueError(f"不支持的邮件服务商: {EMAIL_CONFIG['provider']}")
        
        required_fields = ['sender_email', 'sender_password']
        for field in required_fields:
            if not self.email_config.get(field):
                raise ValueError(f"邮件配置缺少必要字段: {field}")
    
    def _get_smtp_config(self):
        """获取SMTP配置"""
        return {
            'smtp_server': self.smtp_config['smtp_server'],
            'smtp_port': self.smtp_config['smtp_port'],
            'use_tls': self.smtp_config.get('use_tls', True),
            'use_ssl': self.smtp_config.get('use_ssl', False),
        }

    def generate_verification_code(self, length: int = None) -> str:
        """
        生成验证码
        
        Args:
            length: 验证码长度，默认从配置读取
            
        Returns:
            str: 生成的验证码
        """
        if not length:
            length = VERIFICATION_CODE_CONFIG['length']
        
        chars = VERIFICATION_CODE_CONFIG['chars']
        return ''.join(random.choice(chars) for _ in range(length))

    def load_email_template(self, template_name: str) -> str:
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

    def send_email(self, to_email: str, subject: str, html_content: str, 
                   text_content: str = None) -> Dict[str, Any]:
        """
        发送邮件的通用函数
        
        Args:
            to_email: 收件人邮箱
            subject: 邮件主题
            html_content: HTML内容
            text_content: 纯文本内容（可选）
            
        Returns:
            dict: 发送结果
        """
        try:
            # 参数验证
            if not to_email:
                return error_result("收件人邮箱不能为空")
            
            if not subject:
                return error_result("邮件主题不能为空")
            
            if not html_content:
                return error_result("邮件内容不能为空")

            # 获取SMTP配置
            smtp_config = self._get_smtp_config()

            # 创建邮件
            message = MIMEMultipart('alternative')
            message['From'] = Header(
                f"{self.email_config.get('sender_name', '心理健康平台')} <{self.email_config['sender_email']}>",
                'utf-8')
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
            with smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port']) as server:
                # 启用安全传输
                if smtp_config['use_tls']:
                    server.starttls()

                # 登录
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])

                # 发送邮件
                server.send_message(message)

            logger.info(f"邮件发送成功: {to_email}, 主题: {subject}")
            return success_result("邮件发送成功", {
                'to_email': to_email,
                'subject': subject
            })

        except smtplib.SMTPAuthenticationError as e:
            error_msg = "邮箱认证失败，请检查邮箱配置"
            logger.error(f"{error_msg}: {e}")
            return error_result(error_msg)
        except smtplib.SMTPRecipientsRefused as e:
            error_msg = "收件人邮箱地址无效"
            logger.error(f"{error_msg}: {e}")
            return error_result(error_msg)
        except smtplib.SMTPServerDisconnected as e:
            error_msg = "邮件服务器连接失败"
            logger.error(f"{error_msg}: {e}")
            return error_result(error_msg)
        except Exception as e:
            error_msg = f"发送邮件失败: {str(e)}"
            logger.error(error_msg)
            return error_result(error_msg)
    
    def send_verification_code(self, to_email: str, verification_code: str = None,
                               expires_minutes: int = None) -> Dict[str, Any]:
        """
        发送验证码邮件
        
        Args:
            to_email: 收件人邮箱
            verification_code: 验证码，如果不提供则自动生成
            expires_minutes: 验证码有效期（分钟），默认从配置读取
            
        Returns:
            dict: 发送结果
        """
        try:
            # 如果没有提供验证码，则生成一个
            if not verification_code:
                verification_code = self.generate_verification_code()

            # 如果没有提供过期时间，使用配置中的默认值
            if not expires_minutes:
                expires_minutes = VERIFICATION_CODE_CONFIG['expire_minutes']

            # 获取模板配置
            template_config = EMAIL_TEMPLATES.get('verification_code', {})
            template_file = template_config.get('template_file', 'verification_code.html')
            
            # 加载邮件模板
            html_template = self.load_email_template(template_file)

            # 替换模板中的变量
            html_content = html_template.format(
                verification_code=verification_code,
                expires_minutes=expires_minutes
            )

            # 获取邮件主题
            subject = template_config.get('subject', '邮箱验证码')

            # 发送邮件
            result = self.send_email(to_email, subject, html_content)
            
            # 如果发送成功，添加验证码到返回结果
            if result['code'] == 200:
                result['data']['verification_code'] = verification_code
                result['data']['expires_minutes'] = expires_minutes

            return result

        except Exception as e:
            error_msg = f"发送验证码邮件失败: {str(e)}"
            logger.error(error_msg)
            return error_result(error_msg)

    def send_welcome_email(self, to_email: str, username: str = None) -> Dict[str, Any]:
        """
        发送欢迎邮件
        
        Args:
            to_email: 收件人邮箱
            username: 用户名
            
        Returns:
            dict: 发送结果
        """
        try:
            # 获取模板配置
            template_config = EMAIL_TEMPLATES.get('welcome', {})
            template_file = template_config.get('template_file', 'welcome.html')
            
            # 加载邮件模板
            html_template = self.load_email_template(template_file)

            # 替换模板中的变量
            html_content = html_template.format(username=username or "用户")
            
            # 获取邮件主题
            subject = template_config.get('subject', '欢迎加入心理健康平台')

            return self.send_email(to_email, subject, html_content)

        except Exception as e:
            error_msg = f"发送欢迎邮件失败: {str(e)}"
            logger.error(error_msg)
            return error_result(error_msg)
    
    def send_password_reset(self, to_email: str, reset_code: str = None,
                           expires_minutes: int = None) -> Dict[str, Any]:
        """
        发送密码重置邮件
        
        Args:
            to_email: 收件人邮箱
            reset_code: 重置码，如果不提供则自动生成
            expires_minutes: 重置码有效期（分钟）
            
        Returns:
            dict: 发送结果
        """
        try:
            if not reset_code:
                reset_code = self.generate_verification_code()

            if not expires_minutes:
                expires_minutes = VERIFICATION_CODE_CONFIG['expire_minutes']

            # 获取模板配置
            template_config = EMAIL_TEMPLATES.get('password_reset', {})
            template_file = template_config.get('template_file', 'password_reset.html')
            
            # 加载邮件模板
            html_template = self.load_email_template(template_file)

            # 替换模板中的变量
            html_content = html_template.format(
                reset_code=reset_code,
                expires_minutes=expires_minutes
            )
            
            # 获取邮件主题
            subject = template_config.get('subject', '密码重置验证码')

            result = self.send_email(to_email, subject, html_content)
            
            if result['code'] == 200:
                result['data']['reset_code'] = reset_code
                result['data']['expires_minutes'] = expires_minutes

            return result

        except Exception as e:
            error_msg = f"发送密码重置邮件失败: {str(e)}"
            logger.error(error_msg)
            return error_result(error_msg)
    
    def send_appointment_reminder(self, to_email: str, appointment_time: str, 
                                 doctor_name: str, location: str = None) -> Dict[str, Any]:
        """
        发送预约提醒邮件
        
        Args:
            to_email: 收件人邮箱
            appointment_time: 预约时间
            doctor_name: 医生姓名
            location: 预约地点
            
        Returns:
            dict: 发送结果
        """
        try:
            # 获取模板配置
            template_config = EMAIL_TEMPLATES.get('appointment_reminder', {})
            template_file = template_config.get('template_file', 'appointment_reminder.html')
            
            # 加载邮件模板
            html_template = self.load_email_template(template_file)

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
            html_content = html_template.format(
                appointment_time=appointment_time,
                doctor_name=doctor_name,
                location_row=location_row
            )
            
            # 获取邮件主题
            subject = template_config.get('subject', '预约提醒')

            return self.send_email(to_email, subject, html_content)

        except Exception as e:
            error_msg = f"发送预约提醒邮件失败: {str(e)}"
            logger.error(error_msg)
            return error_result(error_msg)
    
    def send_order_notification(self, to_email: str, order_number: str, order_status: str,
                               order_time: str = None, service_name: str = None, 
                               order_amount: str = None) -> Dict[str, Any]:
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
            dict: 发送结果
        """
        try:
            # 获取模板配置
            template_config = EMAIL_TEMPLATES.get('order_notification', {})
            template_file = template_config.get('template_file', 'order_notification.html')
            
            # 加载邮件模板
            html_template = self.load_email_template(template_file)

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
            html_content = html_template.format(
                order_number=order_number,
                order_status=order_status,
                order_status_class=status_class,
                order_time=order_time or '未知',
                service_name=service_name or '心理健康服务',
                order_amount=order_amount or '未知',
                status_specific_content=status_content
            )
            
            # 获取邮件主题
            subject = template_config.get('subject', '订单通知')

            return self.send_email(to_email, subject, html_content)

        except Exception as e:
            error_msg = f"发送订单通知邮件失败: {str(e)}"
            logger.error(error_msg)
            return error_result(error_msg)


# 创建全局邮件服务实例
email_service = EmailService()


# 便捷函数
def send_email(to_email: str, subject: str, html_content: str, text_content: str = None) -> Dict[str, Any]:
    """
    发送邮件的便捷函数
    
    Args:
        to_email: 收件人邮箱
        subject: 邮件主题
        html_content: HTML内容
        text_content: 纯文本内容
        
    Returns:
        dict: 发送结果
    """
    return email_service.send_email(to_email, subject, html_content, text_content)


def send_verification_code(to_email: str, verification_code: str = None, 
                          expires_minutes: int = None) -> Dict[str, Any]:
    """
    发送验证码邮件的便捷函数
    
    Args:
        to_email: 收件人邮箱
        verification_code: 验证码
        expires_minutes: 过期时间（分钟）
        
    Returns:
        dict: 发送结果
    """
    return email_service.send_verification_code(to_email, verification_code, expires_minutes)


def send_welcome_email(to_email: str, username: str = None) -> Dict[str, Any]:
    """
    发送欢迎邮件的便捷函数
    """
    return email_service.send_welcome_email(to_email, username)


def send_password_reset(to_email: str, reset_code: str = None, 
                       expires_minutes: int = None) -> Dict[str, Any]:
    """
    发送密码重置邮件的便捷函数
    """
    return email_service.send_password_reset(to_email, reset_code, expires_minutes)


def send_appointment_reminder(to_email: str, appointment_time: str, 
                             doctor_name: str, location: str = None) -> Dict[str, Any]:
    """
    发送预约提醒邮件的便捷函数
    """
    return email_service.send_appointment_reminder(to_email, appointment_time, doctor_name, location)


def send_order_notification(to_email: str, order_number: str, order_status: str,
                           order_time: str = None, service_name: str = None, 
                           order_amount: str = None) -> Dict[str, Any]:
    """
    发送订单通知邮件的便捷函数
    """
    return email_service.send_order_notification(to_email, order_number, order_status, 
                                                order_time, service_name, order_amount)


def generate_verification_code(length: int = None) -> str:
    """
    生成验证码的便捷函数
    
    Args:
        length: 验证码长度
        
    Returns:
        str: 验证码
    """
    return email_service.generate_verification_code(length)
