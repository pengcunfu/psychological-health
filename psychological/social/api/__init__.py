from .social_topic import social_topic_bp
from .social_post import social_post_bp
from .social_comment import social_comment_bp
from .social_like import social_like_bp
from .social_follow import social_follow_bp
from flask import current_app


def register_social_blueprints():
    """注册所有社交相关的API蓝图"""
    current_app.register_blueprint(social_topic_bp)
    current_app.register_blueprint(social_post_bp)
    current_app.register_blueprint(social_comment_bp)
    current_app.register_blueprint(social_like_bp)
    current_app.register_blueprint(social_follow_bp)


__all__ = [
    # Blueprints
    'social_topic_bp',
    'social_post_bp',
    'social_comment_bp',
    'social_like_bp',
    'social_follow_bp',
    
    # Registration function
    'register_social_blueprints'
]
