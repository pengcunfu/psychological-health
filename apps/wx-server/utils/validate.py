from flask import request
from typing import Type, TypeVar
from form.base import BaseForm

T = TypeVar('T', bound=BaseForm)


class ValidationError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def check_id(form_id, message: str = "ID is required"):
    if not form_id or not form_id.strip():
        raise ValidationError(message)


def validate_args(base_form: Type[T]) -> T:
    form = base_form(data=request.args)
    if not form.validate():
        raise ValidationError(f'参数验证失败: {form.get_first_error()}')
    return form


def validate_data(base_form: Type[T]) -> T:
    data = request.get_json()
    if not data:
        raise ValidationError("请求数据不能为空")

    # 使用表单验证
    form = base_form(data=data)
    if not form.validate():
        raise ValidationError(f"参数验证失败: {form.get_first_error()}")

    return form
