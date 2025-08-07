from flask import Flask, request, g
from sqlalchemy.exc import SQLAlchemyError
from utils.json_result import JsonResult
from utils.logger_client import get_logger
from utils.exceptions import UnauthorizedError, PermissionDeniedError, ValidationError, ResourceNotFoundError
from models.base import db
import traceback


class GlobalExceptionHandler:
    """全局异常处理器"""
    
    def __init__(self, app: Flask = None):
        self.app = app
        self.logger = get_logger(__name__)
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """初始化全局异常处理"""
        self.app = app
        
        # 注册全局异常处理器
        app.register_error_handler(SQLAlchemyError, self.handle_sqlalchemy_error)
        app.register_error_handler(ValueError, self.handle_value_error)
        app.register_error_handler(KeyError, self.handle_key_error)
        app.register_error_handler(PermissionError, self.handle_permission_error)
        app.register_error_handler(FileNotFoundError, self.handle_not_found_error)
        app.register_error_handler(UnauthorizedError, self.handle_unauthorized_error)
        app.register_error_handler(PermissionDeniedError, self.handle_permission_denied_error)
        app.register_error_handler(ValidationError, self.handle_validation_error)
        app.register_error_handler(ResourceNotFoundError, self.handle_resource_not_found_error)
        app.register_error_handler(Exception, self.handle_general_error)
        
        # 注册请求前后处理
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """请求前处理"""
        # 可以在这里添加请求日志、验证等逻辑
        pass
    
    def after_request(self, response):
        """请求后处理"""
        # 可以在这里添加响应日志等逻辑
        return response
    
    def handle_sqlalchemy_error(self, error: SQLAlchemyError):
        """处理SQLAlchemy数据库异常"""
        db.session.rollback()
        self._log_error(error, "数据库操作异常")
        return JsonResult.error(f'数据库操作失败: {str(error)}', 500)
    
    def handle_value_error(self, error: ValueError):
        """处理参数验证异常"""
        self._log_error(error, "参数验证异常")
        return JsonResult.error(f'参数验证失败: {str(error)}', 400)
    
    def handle_key_error(self, error: KeyError):
        """处理缺少必要参数异常"""
        self._log_error(error, "缺少必要参数")
        return JsonResult.error(f'缺少必要参数: {str(error)}', 400)
    
    def handle_permission_error(self, error: PermissionError):
        """处理权限异常"""
        self._log_error(error, "权限不足")
        return JsonResult.error(f'权限不足: {str(error)}', 403)
    
    def handle_not_found_error(self, error: FileNotFoundError):
        """处理资源不存在异常"""
        self._log_error(error, "资源不存在")
        return JsonResult.error(f'资源不存在: {str(error)}', 404)
    
    def handle_unauthorized_error(self, error: UnauthorizedError):
        """处理用户未登录异常"""
        self._log_error(error, "用户未登录")
        return JsonResult.error(error.message, error.code)
    
    def handle_permission_denied_error(self, error: PermissionDeniedError):
        """处理权限不足异常"""
        self._log_error(error, "权限不足")
        return JsonResult.error(error.message, error.code)
    
    def handle_validation_error(self, error: ValidationError):
        """处理数据验证异常"""
        self._log_error(error, "数据验证异常")
        return JsonResult.error(error.message, error.code)
    
    def handle_resource_not_found_error(self, error: ResourceNotFoundError):
        """处理资源不存在异常"""
        self._log_error(error, "资源不存在")
        return JsonResult.error(error.message, error.code)
    
    def handle_general_error(self, error: Exception):
        """处理通用异常"""
        # 如果是SQLAlchemy异常，先回滚事务
        if hasattr(db, 'session'):
            try:
                db.session.rollback()
            except:
                pass
        
        self._log_error(error, "系统异常")
        
        # 根据请求路径生成更友好的错误消息
        operation_name = self._get_operation_name_from_path()
        return JsonResult.error(f'{operation_name}失败: {str(error)}', 500)
    
    def _log_error(self, error: Exception, error_type: str):
        """记录错误日志"""
        try:
            # 获取请求信息
            method = request.method if request else 'UNKNOWN'
            path = request.path if request else 'UNKNOWN'
            user_id = getattr(g, 'current_user', {}).get('id', 'ANONYMOUS') if hasattr(g, 'current_user') else 'ANONYMOUS'
            
            # 记录详细错误信息
            self.logger.error(f"""
{error_type}:
- 用户ID: {user_id}
- 请求方法: {method}
- 请求路径: {path}
- 错误类型: {type(error).__name__}
- 错误信息: {str(error)}
- 错误堆栈: {traceback.format_exc()}
            """)
        except Exception as log_error:
            # 如果日志记录失败，至少打印基本错误信息
            print(f"日志记录失败: {log_error}, 原始错误: {error}")
    
    def _get_operation_name_from_path(self) -> str:
        """根据请求路径生成操作名称"""
        if not request:
            return "操作"
        
        path = request.path
        method = request.method
        
        # 根据路径和方法推断操作类型
        operation_map = {
            ('GET', 'announcements'): '获取公告列表',
            ('POST', 'announcements'): '创建公告',
            ('PUT', 'announcements'): '更新公告',
            ('DELETE', 'announcements'): '删除公告',
            ('GET', 'users'): '获取用户列表',
            ('POST', 'users'): '创建用户',
            ('PUT', 'users'): '更新用户',
            ('DELETE', 'users'): '删除用户',
            ('GET', 'counselors'): '获取咨询师列表',
            ('POST', 'counselors'): '创建咨询师',
            ('PUT', 'counselors'): '更新咨询师',
            ('DELETE', 'counselors'): '删除咨询师',
            ('GET', 'appointments'): '获取预约列表',
            ('POST', 'appointments'): '创建预约',
            ('PUT', 'appointments'): '更新预约',
            ('DELETE', 'appointments'): '删除预约',
            ('GET', 'courses'): '获取课程列表',
            ('POST', 'courses'): '创建课程',
            ('PUT', 'courses'): '更新课程',
            ('DELETE', 'courses'): '删除课程',
            ('GET', 'orders'): '获取订单列表',
            ('POST', 'orders'): '创建订单',
            ('PUT', 'orders'): '更新订单',
            ('DELETE', 'orders'): '删除订单',
        }
        
        # 提取路径中的资源名称
        for resource in ['announcements', 'users', 'counselors', 'appointments', 'courses', 'orders']:
            if resource in path:
                return operation_map.get((method, resource), f'{resource}操作')
        
        return "API操作"


# 创建全局实例
global_exception_handler = GlobalExceptionHandler()