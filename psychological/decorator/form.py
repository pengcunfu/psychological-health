"""
表单验证装饰器模块
提供简洁的表单验证装饰器

使用示例:
    @validate_form(UserCreateForm)
    def create_user(form):
        # form 是验证后的表单实例
        pass
"""

from functools import wraps
from typing import Type, Callable
from flask import request
from psychological.form.base import BaseForm
from psychological.utils.validate import validate_form as _validate_form, ValidationError
from psychological.utils.json_result import JsonResult


def validate_form(form_class: Type[BaseForm], 
                  inject_form: bool = True,
                  form_param_name: str = 'form') -> Callable:
    """
    表单验证装饰器
    自动根据请求方法选择验证方式：GET使用查询参数，其他使用JSON数据
    
    Args:
        form_class: 要验证的表单类
        inject_form: 是否将验证后的表单注入到函数参数中
        form_param_name: 注入的表单参数名称
    
    Returns:
        装饰器函数
    
    Examples:
        @validate_form(UserCreateForm)
        def create_user(form):
            # GET请求时验证查询参数，POST/PUT等验证JSON数据
            user = User(name=form.name.data)
            return JsonResult.success(user.to_dict())
        
        @validate_form(UserCreateForm, inject_form=False)
        def create_user():
            # 不注入form，但会验证数据
            data = request.get_json()
            return JsonResult.success(data)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # 使用现有的validate_form函数进行验证
                form = _validate_form(form_class)
                
                # 是否注入表单到函数参数
                if inject_form:
                    kwargs[form_param_name] = form
                
                return func(*args, **kwargs)
                
            except ValidationError as e:
                return JsonResult.error(e.message, e.status_code)
            except Exception as e:
                return JsonResult.error(f'表单验证失败: {str(e)}', 500)
        
        return wrapper
    return decorator
