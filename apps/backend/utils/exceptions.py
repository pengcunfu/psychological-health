"""
自定义异常类定义
"""


class AuthenticationError(Exception):
    """认证异常基类"""
    def __init__(self, message="认证失败", code=401):
        self.message = message
        self.code = code
        super().__init__(self.message)


class UnauthorizedError(AuthenticationError):
    """用户未登录异常"""
    def __init__(self, message="用户未登录"):
        super().__init__(message, 401)


class PermissionDeniedError(Exception):
    """权限不足异常"""
    def __init__(self, message="权限不足", code=403):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationError(Exception):
    """数据验证异常"""
    def __init__(self, message="数据验证失败", code=400):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ResourceNotFoundError(Exception):
    """资源不存在异常"""
    def __init__(self, message="资源不存在", code=404):
        self.message = message
        self.code = code
        super().__init__(self.message) 