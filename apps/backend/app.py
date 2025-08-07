from flask import Flask
from flask_cors import CORS
import logging
import os
from api.announcement import announcements_bp
from api.appointment import appointment_bp
from api.assessment import assessment_bp
from api.disease_tags import disease_tags_bp
from api.counselor import counselor_bp
from api.consultant import consultant_bp
from api.course import course_bp
from api.course_outline import course_outline_bp
from api.user_favorite import user_favorite_bp
from api.review import review_bp
from api.order import order_bp
from api.user import user_bp
from api.auth import login_bp
from api.upload import file_upload_bp
from api.category import category_bp
from utils.config import Config
from utils.swagger_config import api_bp
from models.base import db
from middleware.global_exception_handler import GlobalExceptionHandler
from api.role import role_bp
from api.banner import banner_bp
from api.group import group_bp
from api.menu import menu_bp
from api.workspace import workspace_bp

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 加载配置
config = Config.from_yaml()
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG

# 禁用CSRF保护（纯API项目）
app.config['WTF_CSRF_ENABLED'] = False

# 文件上传配置
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

db.init_app(app)

# 初始化Redis连接
def init_redis():
    """初始化Redis连接"""
    try:
        from utils.redis_client import session_manager
        if session_manager.redis_client.is_available():
            logger.info("Redis连接成功，会话将存储到Redis")
        else:
            logger.warning("Redis连接失败，会话将存储到内存（降级模式）")
    except Exception as e:
        logger.error(f"Redis初始化失败: {e}")
        logger.warning("将使用内存存储作为降级方案")

# 注册蓝图
app.register_blueprint(announcements_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(assessment_bp)
app.register_blueprint(disease_tags_bp)
app.register_blueprint(counselor_bp)
app.register_blueprint(consultant_bp)
app.register_blueprint(course_bp)
app.register_blueprint(course_outline_bp)
app.register_blueprint(user_favorite_bp)
app.register_blueprint(review_bp)
app.register_blueprint(order_bp)
app.register_blueprint(user_bp)
app.register_blueprint(category_bp)
app.register_blueprint(login_bp)
app.register_blueprint(file_upload_bp)
app.register_blueprint(api_bp)
app.register_blueprint(role_bp)
app.register_blueprint(banner_bp)
app.register_blueprint(group_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(workspace_bp)

# 初始化全局异常处理器（这是关键步骤）
exception_handler = GlobalExceptionHandler()
exception_handler.init_app(app)


# 首页重定向到Swagger文档
@app.route('/')
def index():
    """首页重定向到Swagger API文档"""
    from flask import redirect
    return redirect('/api/docs/')


# 配置静态文件CDN访问
@app.route('/static/<path:filename>')
def static_files(filename):
    """静态文件CDN访问"""
    from flask import send_from_directory
    import os
    static_dir = os.path.join(app.root_path, 'static')
    return send_from_directory(static_dir, filename)


# 会话统计API（用于监控）
@app.route('/api/session/stats')
def session_stats():
    """获取会话统计信息"""
    from middleware.auth import AuthMiddleware
    from utils.json_result import JsonResult
    
    stats = AuthMiddleware.get_session_stats()
    return JsonResult.success(stats)


# Redis健康检查API
@app.route('/api/health/redis')
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


# 创建数据库表
with app.app_context():
    db.create_all()
    # 初始化Redis
    init_redis()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=config.DEBUG)
