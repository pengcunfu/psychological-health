"""
邮件服务配置类型定义
只包含类型定义，不包含具体配置实例
"""


class EmailProvider:
    """SMTP服务器配置类"""
    
    def __init__(self, smtp_server: str, smtp_port: int, use_tls: bool = True, use_ssl: bool = False):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.use_tls = use_tls
        self.use_ssl = use_ssl


class EmailConfig:
    """邮件配置类"""
    
    def __init__(self, sender_email: str, sender_password: str, sender_name: str):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_name = sender_name
