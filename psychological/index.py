from flask import Blueprint, redirect, send_from_directory, current_app
import os
from psychological.utils.session import get_session_manager, is_redis_available
from pcf_flask_helper.common import json_success, json_error
from .utils.auth_manager import AuthManager

# 创建索引蓝图
index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    """首页显示网站启动成功信息"""
    return json_success({
        'message': '心理健康平台启动成功',
        'status': 'running',
        'version': '1.0.0',
        'description': '心理健康管理系统 API 服务已正常运行'
    })


@index_bp.route('/static/<path:filename>')
def static_files(filename):
    """静态文件CDN访问"""
    # Flask应用在psychological目录下，静态文件在项目根目录的static文件夹
    project_root = os.path.dirname(current_app.root_path)
    static_dir = os.path.join(project_root, 'static')
    
    # 检查文件是否存在
    file_path = os.path.join(static_dir, filename)
    if not os.path.exists(file_path):
        return json_error(f'静态文件不存在: {filename}', code=404)
    
    return send_from_directory(static_dir, filename)


@index_bp.route('/favicon.ico')
def favicon():
    """网站图标"""
    # 尝试从static目录返回favicon
    project_root = os.path.dirname(current_app.root_path)
    static_dir = os.path.join(project_root, 'static')
    favicon_path = os.path.join(static_dir, 'favicon.png')
    
    if os.path.exists(favicon_path):
        return send_from_directory(static_dir, 'favicon.png')
    else:
        # 如果没有favicon文件，返回一个空的204响应
        from flask import Response
        return Response(status=204)


@index_bp.route('/api/session/stats')
def session_stats():
    """获取会话统计信息"""

    stats = AuthManager.get_session_stats()
    return json_success(stats)


@index_bp.route('/api/health/redis')
def redis_health():
    """Redis健康检查"""
    try:
        available = is_redis_available()
        session_manager = get_session_manager()

        if available:
            return json_success({
                'status': 'healthy',
                'message': 'Redis连接正常',
                'session_count': session_manager.get_session_count()
            })
        else:
            return json_error({
                'status': 'error',
                'message': 'Redis连接失败',
                'session_count': 0
            }, code=503)
    except Exception as e:
        return json_error({
            'status': 'error',
            'message': f'Redis检查失败: {str(e)}'
        }, code=500)


def register_index_blueprints():
    """注册索引蓝图"""
    current_app.register_blueprint(index_bp)
