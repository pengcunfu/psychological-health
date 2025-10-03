from flask import redirect, send_from_directory
import os
from psychological.utils.session import get_session_manager, is_redis_available
from pcf_flask_helper.common import json_success, json_error


def index():
    """首页重定向到Swagger API文档"""
    return redirect('/api/docs/')


def static_files(filename):
    """静态文件CDN访问"""
    from flask import current_app
    static_dir = os.path.join(current_app.root_path, 'static')
    return send_from_directory(static_dir, filename)


def session_stats():
    """获取会话统计信息"""
    from utils.auth_manager import AuthManager
    from utils.json_result import JsonResult

    stats = AuthManager.get_session_stats()
    return json_success(stats)


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
