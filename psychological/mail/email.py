"""
邮箱验证码发送服务
支持发送验证码邮件，包含HTML模板和邮件配置
"""

import smtplib
import os
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Optional, Dict, Any
from ..utils.config import get_config


class EmailService:
    """邮箱服务类，用于发送验证码邮件"""
    
    def __init__(self):
        """初始化邮箱服务"""
        self.config = get_config()
        self.email_config = self.config.get('code', {})
        self._validate_config()
    
    def _validate_config(self):
        """验证邮箱配置"""
        required_fields = ['smtp_server', 'smtp_port', 'sender_email', 'sender_password']
        for field in required_fields:
            if not self.email_config.get(field):
                raise ValueError(f"邮箱配置缺少必要字段: {field}")
    
    def generate_verification_code(self, length: int = 6) -> str:
        """
        生成验证码
        
        Args:
            length: 验证码长度，默认6位
            
        Returns:
            str: 生成的验证码
        """
        return ''.join(random.choices(string.digits, k=length))
    
    def load_email_template(self, template_name: str = 'verification_code.html') -> str:
        """
        加载邮件HTML模板
        
        Args:
            template_name: 模板文件名
            
        Returns:
            str: HTML模板内容
        """
        template_path = os.path.join(os.path.dirname(__file__), template_name)
        
        if not os.path.exists(template_path):
            # 如果模板不存在，返回默认模板
            return self._get_default_template()
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"加载邮件模板失败: {e}")
            return self._get_default_template()
    
    def _get_default_template(self) -> str:
        """获取默认邮件模板"""
        return """
        <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #333; text-align: center;">验证码</h2>
                <p style="color: #666; font-size: 16px;">您的验证码是：</p>
                <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0;">
                    <span style="font-size: 24px; font-weight: bold; color: #007bff; letter-spacing: 2px;">{verification_code}</span>
                </div>
                <p style="color: #666; font-size: 14px;">验证码有效期为 {expires_minutes} 分钟，请及时使用。</p>
                <p style="color: #999; font-size: 12px; margin-top: 30px;">如果您没有请求此验证码，请忽略此邮件。</p>
            </div>
        </body>
        </html>
        """
    
    def send_verification_code(self, to_email: str, verification_code: str = None, 
                             expires_minutes: int = 10, subject: str = "邮箱验证码") -> Dict[str, Any]:
        """
        发送验证码邮件
        
        Args:
            to_email: 收件人邮箱
            verification_code: 验证码，如果不提供则自动生成
            expires_minutes: 验证码有效期（分钟）
            subject: 邮件主题
            
        Returns:
            dict: 发送结果 {'success': bool, 'message': str, 'code': str}
        """
        try:
            # 如果没有提供验证码，则生成一个
            if not verification_code:
                verification_code = self.generate_verification_code()
            
            # 加载邮件模板
            html_template = self.load_email_template()
            
            # 替换模板中的变量
            html_content = html_template.format(
                verification_code=verification_code,
                expires_minutes=expires_minutes
            )
            
            # 创建邮件
            message = MIMEMultipart('alternative')
            message['From'] = Header(f"{self.email_config.get('sender_name', '心理健康平台')} <{self.email_config['sender_email']}>", 'utf-8')
            message['To'] = Header(to_email, 'utf-8')
            message['Subject'] = Header(subject, 'utf-8')
            
            # 添加HTML内容
            html_part = MIMEText(html_content, 'html', 'utf-8')
            message.attach(html_part)
            
            # 发送邮件
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                # 启用安全传输
                if self.email_config.get('use_tls', True):
                    server.starttls()
                
                # 登录
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                
                # 发送邮件
                server.send_message(message)
            
            return {
                'success': True,
                'message': '验证码发送成功',
                'code': verification_code
            }
            
        except smtplib.SMTPAuthenticationError:
            return {
                'success': False,
                'message': '邮箱认证失败，请检查邮箱配置',
                'code': verification_code
            }
        except smtplib.SMTPRecipientsRefused:
            return {
                'success': False,
                'message': '收件人邮箱地址无效',
                'code': verification_code
            }
        except smtplib.SMTPServerDisconnected:
            return {
                'success': False,
                'message': '邮件服务器连接失败',
                'code': verification_code
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'发送邮件失败: {str(e)}',
                'code': verification_code
            }
    
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
            welcome_template = """
            <html>
            <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #333; text-align: center;">欢迎加入心理健康平台</h2>
                    <p style="color: #666; font-size: 16px;">亲爱的 {username}，</p>
                    <p style="color: #666; font-size: 16px;">欢迎您注册我们的心理健康平台！我们很高兴您的加入。</p>
                    <div style="background-color: #e8f5e8; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <p style="color: #2d5a2d; margin: 0;">在这里，您可以：</p>
                        <ul style="color: #2d5a2d; margin: 10px 0;">
                            <li>获得专业的心理健康咨询</li>
                            <li>参加心理健康课程</li>
                            <li>进行心理健康测评</li>
                            <li>与专业咨询师交流</li>
                        </ul>
                    </div>
                    <p style="color: #666; font-size: 14px;">如果您有任何问题，请随时联系我们的客服团队。</p>
                    <p style="color: #999; font-size: 12px; margin-top: 30px;">祝您身心健康！</p>
                </div>
            </body>
            </html>
            """
            
            html_content = welcome_template.format(username=username or "用户")
            
            message = MIMEMultipart('alternative')
            message['From'] = Header(f"{self.email_config.get('sender_name', '心理健康平台')} <{self.email_config['sender_email']}>", 'utf-8')
            message['To'] = Header(to_email, 'utf-8')
            message['Subject'] = Header("欢迎加入心理健康平台", 'utf-8')
            
            html_part = MIMEText(html_content, 'html', 'utf-8')
            message.attach(html_part)
            
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                if self.email_config.get('use_tls', True):
                    server.starttls()
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                server.send_message(message)
            
            return {
                'success': True,
                'message': '欢迎邮件发送成功'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'发送欢迎邮件失败: {str(e)}'
            }


# 创建全局邮箱服务实例
email_service = EmailService() 