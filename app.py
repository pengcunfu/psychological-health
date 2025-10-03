from flask import Flask
from flask_cors import CORS

from .appointment.api import register_appointment_blueprints
from .course.api import register_course_blueprints
from .system.api import register_system_blueprints
from .social.api import register_social_blueprints
from .index import register_index_blueprints

from pcf_flask_helper.model.base import db
from .middleware.global_exception_handler import GlobalExceptionHandler
from .commands.data_init import register_init_command
from .config import cfg

app = Flask(__name__, static_folder=None)  # 禁用Flask内置静态文件处理
CORS(app)

# 加载配置
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.get("mysql.uri")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = cfg.get("app.secret_key")

# 禁用CSRF保护（纯API项目）
app.config['WTF_CSRF_ENABLED'] = False

# 文件上传配置
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

db.init_app(app)
# 初始化全局异常处理器（这是关键步骤）
exception_handler = GlobalExceptionHandler()
exception_handler.init_app(app)
# 注册CLI命令
register_init_command(app)

# 注册蓝图
with app.app_context():
    register_appointment_blueprints()
    register_course_blueprints()
    register_system_blueprints()
    register_social_blueprints()
    register_index_blueprints()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=cfg.get("app.debug"))
