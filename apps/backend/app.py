from flask import Flask
from flask_cors import CORS

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
from api.role import role_bp
from api.banner import banner_bp
from api.group import group_bp
from api.menu import menu_bp
from api.workspace import workspace_bp
from api import index, static_files, session_stats, redis_health

from utils.config import Config
from utils.redis_client import init_redis
from utils.swagger_config import api_bp
from utils.logger_client import init_logging
from models.base import db
from middleware.global_exception_handler import GlobalExceptionHandler

# 初始化日志配置
init_logging()

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

# 注册路由
app.add_url_rule('/', 'index', index)
app.add_url_rule('/static/<path:filename>', 'static_files', static_files)
app.add_url_rule('/api/session/stats', 'session_stats', session_stats)
app.add_url_rule('/api/health/redis', 'redis_health', redis_health)

# 初始化全局异常处理器（这是关键步骤）
exception_handler = GlobalExceptionHandler()
exception_handler.init_app(app)

with app.app_context():
    # 创建数据库表
    db.create_all()
    # 初始化Redis
    init_redis()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=config.DEBUG)
