from .course import course_bp
from .course_outline import course_outline_bp
from .course_subscription import course_subscription_bp
from flask import current_app


def register_course_blueprints():
    """注册所有课程相关的API蓝图"""
    current_app.register_blueprint(course_bp)
    current_app.register_blueprint(course_outline_bp)
    current_app.register_blueprint(course_subscription_bp)


__all__ = [
    'course_bp',
    'course_outline_bp',
    'course_subscription_bp',
    'register_course_blueprints'
]
