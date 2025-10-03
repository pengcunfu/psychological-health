"""
邮件服务模块
只导出核心类，不提供便捷函数
"""

from .email import EmailService
from .config import EmailConfig, EmailProvider

__all__ = ['EmailService', 'EmailConfig', 'EmailProvider']
