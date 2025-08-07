from flask import redirect, send_from_directory
import os

# 首页重定向到Swagger文档
def index():
    """首页重定向到Swagger API文档"""
    return redirect('/api/docs/')


# 配置静态文件CDN访问
def static_files(filename):
    """静态文件CDN访问"""
    from flask import current_app
    static_dir = os.path.join(current_app.root_path, 'static')
    return send_from_directory(static_dir, filename)


# 会话统计API（用于监控）
def session_stats():
    """获取会话统计信息"""
    from utils.auth_manager import AuthManager
    from utils.json_result import JsonResult

    stats = AuthManager.get_session_stats()
    return JsonResult.success(stats)


# Redis健康检查API
def redis_health():
    """Redis健康检查"""
    from utils.redis_client import session_manager
    from utils.json_result import JsonResult

    try:
        is_available = session_manager.redis_client.is_available()
        if is_available:
            return JsonResult.success({
                'status': 'healthy',
                'message': 'Redis连接正常',
                'session_count': session_manager.get_session_count()
            })
        else:
            return JsonResult.error({
                'status': 'degraded',
                'message': 'Redis连接失败，使用内存存储降级模式',
                'session_count': session_manager.get_session_count()
            }, code=503)
    except Exception as e:
        return JsonResult.error({
            'status': 'error',
            'message': f'Redis检查失败: {str(e)}'
        }, code=500)

