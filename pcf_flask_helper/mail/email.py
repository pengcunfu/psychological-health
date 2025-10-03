"""
邮件发送服务模块
基于Emails库实现，支持发送各种类型的邮件，包含HTML模板和完整的错误处理
"""

import re
import emails
from emails.template import JinjaTemplate

from .config import EmailConfig, EmailProvider


class EmailService:
    """邮件服务类，基于Emails库实现，用于发送各种类型的邮件"""

    def __init__(self, email_config: EmailConfig, smtp_provider: EmailProvider):
        """
        初始化邮件服务
        
        Args:
            email_config: 邮件配置对象，包含发送者信息
            smtp_provider: SMTP服务器配置对象
        """
        self.email_config = email_config
        self.smtp_provider = smtp_provider
        self._validate_config()

        # 配置SMTP连接参数
        self.smtp_config = {
            'host': self.smtp_provider.smtp_server,
            'port': self.smtp_provider.smtp_port,
            'tls': self.smtp_provider.use_tls,
            'ssl': self.smtp_provider.use_ssl,
            'user': self.email_config.sender_email,
            'password': self.email_config.sender_password,
        }

    def _validate_config(self):
        """验证邮件配置"""
        # 验证SMTP服务器配置
        if not self.smtp_provider:
            raise ValueError("SMTP服务器配置不能为空")

        if not self.smtp_provider.smtp_server:
            raise ValueError("SMTP服务器地址不能为空")

        if not isinstance(self.smtp_provider.smtp_port, int) or self.smtp_provider.smtp_port <= 0:
            raise ValueError("SMTP端口号必须是正整数")

        # 验证邮件配置
        if not self.email_config:
            raise ValueError("邮件配置不能为空")

        if not self.email_config.sender_email:
            raise ValueError("发送者邮箱不能为空")

        if not self.email_config.sender_password:
            raise ValueError("发送者密码不能为空")

        if not self.email_config.sender_name:
            raise ValueError("发送者名称不能为空")

        # 验证邮箱格式
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email_config.sender_email):
            raise ValueError("发送者邮箱格式不正确")

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
            Exception: 发送失败情况
        """
        # 参数验证
        if not to_email:
            raise ValueError("收件人邮箱不能为空")

        if not subject:
            raise ValueError("邮件主题不能为空")

        if not html_content:
            raise ValueError("邮件内容不能为空")

        try:
            # 使用Emails库创建邮件
            message = emails.html(
                html=html_content,
                text=text_content,
                subject=subject,
                mail_from=(self.email_config.sender_name, self.email_config.sender_email)
            )

            # 发送邮件
            response = message.send(
                to=to_email,
                smtp=self.smtp_config
            )

            # 检查发送结果
            if response.status_code not in [250, 251, 252]:
                raise Exception(f"邮件发送失败，状态码: {response.status_code}")

            return True

        except Exception as e:
            raise Exception(f"发送邮件失败: {str(e)}") from e

    def send_template_email(self, to_email: str, subject: str, html_template: str, template_config: dict) -> bool:
        """
        发送模板邮件，使用Jinja2模板引擎
        
        Args:
            to_email: 收件人邮箱
            subject: 邮件主题
            html_template: HTML模板内容（支持Jinja2语法）
            template_config: 模板变量配置字典
            
        Returns:
            bool: 成功返回True
            
        Raises:
            KeyError: 模板变量配置错误
            Exception: 发送失败时抛出异常
        """
        try:
            # 使用Emails库的Jinja2模板功能
            template = JinjaTemplate(html_template)

            # 创建邮件消息，使用模板渲染
            message = emails.html(
                html=template,
                subject=subject,
                mail_from=(self.email_config.sender_name, self.email_config.sender_email)
            )

            # 发送邮件，传入模板变量
            response = message.send(
                to=to_email,
                render=template_config,
                smtp=self.smtp_config
            )

            # 检查发送结果
            if response.status_code not in [250, 251, 252]:
                raise Exception(f"邮件发送失败，状态码: {response.status_code}")

            return True

        except Exception as e:
            # 检查是否是模板变量错误
            if "undefined" in str(e).lower() or "missing" in str(e).lower():
                raise KeyError(f"模板变量配置错误: {str(e)}") from e
            else:
                raise Exception(f"发送模板邮件失败: {str(e)}") from e
