from .announcement import announcements_bp
from .appointment import appointment_bp
from .assessment import assessment_bp
from .assessment_record import assessment_record_bp
from .consultant import consultant_bp
from .counselor import counselor_bp
from .disease_tags import disease_tags_bp
from .order import order_bp
from .review import review_bp
from .user_favorite import user_favorite_bp
from flask import current_app


def register_appointment_blueprints():
    """注册所有预约相关的API蓝图"""
    current_app.register_blueprint(announcements_bp)
    current_app.register_blueprint(appointment_bp)
    current_app.register_blueprint(assessment_bp)
    current_app.register_blueprint(assessment_record_bp)
    current_app.register_blueprint(consultant_bp)
    current_app.register_blueprint(counselor_bp)
    current_app.register_blueprint(disease_tags_bp)
    current_app.register_blueprint(order_bp)
    current_app.register_blueprint(review_bp)
    current_app.register_blueprint(user_favorite_bp)


__all__ = [
    # Blueprints
    'announcements_bp',
    'appointment_bp',
    'assessment_bp',
    'assessment_record_bp',
    'consultant_bp',
    'counselor_bp',
    'disease_tags_bp',
    'order_bp',
    'review_bp',
    'user_favorite_bp',
    
    # Registration function
    'register_appointment_blueprints'
]
