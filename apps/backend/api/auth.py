"""
登录认证API
提供用户登录、注册、密码重置等认证相关功能

接口列表：
- POST /login - 用户登录
- POST /register - 用户注册
- POST /logout - 用户登出
- POST /reset-password - 重置密码
- POST /verify-code - 验证码验证
- POST /send-code - 发送验证码
- GET /user/info - 获取当前用户信息
- POST /refresh-token - 刷新访问令牌
"""
from flask import Blueprint, request, jsonify, session, send_file, current_app, g
from datetime import datetime
import hashlib
import uuid
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from models.role import Role
from models.user_role import UserRole
from models.user_password import UserPassword
from utils.json_result import JsonResult
from middleware.auth import AuthMiddleware, login_required
from models.base import db
from utils.verify_code import VerifyCodeGenerator

login_bp = Blueprint('login', __name__, url_prefix='/auth')


def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.md5(password.encode()).hexdigest()


def generate_token() -> str:
    """生成访问令牌"""
    return str(uuid.uuid4()).replace('-', '')


@login_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        if not data:
            return JsonResult.error("请求数据不能为空", 400)

        username = data.get('username')
        password = data.get('password')
        verify_code = data.get('verify_code')

        if not username or not password:
            return JsonResult.error("用户名和密码不能为空", 400)
            
        # 如果提供了验证码，则验证它
        if verify_code:
            stored_code = session.get('verify_code')
            if not stored_code or stored_code.lower() != verify_code.lower():
                return JsonResult.error("验证码错误", 400)
            # 验证成功后清除会话中的验证码，防止重复使用
            session.pop('verify_code', None)

        # 查找用户
        user = User.query.filter_by(username=username).first()
        if not user:
            return JsonResult.error("用户名或密码错误", 401)

        # 验证密码
        user_password = UserPassword.query.filter_by(user_id=user.id).first()
        if not user_password:
            return JsonResult.error("用户名或密码错误", 401)

        hashed_password = hash_password(password)
        if user_password.password_hash != hashed_password:
            return JsonResult.error("用户名或密码错误", 401)

        # 生成访问令牌
        token = generate_token()

        # 获取用户角色信息
        user_roles_query = db.session.query(UserRole, Role).join(
            Role, UserRole.role_id == Role.id
        ).filter(UserRole.user_id == user.id)

        user_roles = [role for _, role in user_roles_query.all()]

        # 创建会话
        user_data = {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'phone': user.phone,
            'email': user.email,
            'roles': [{
                'id': role.id,
                'name': role.name,
                'code': role.code
            } for role in user_roles]
        }

        AuthMiddleware.create_session(user.id, token, user_data)

        return JsonResult.success({
            'token': token,
            'user': user_data,
            'expires_in': 7200  # 2小时
        }, "登录成功")

    except SQLAlchemyError as e:
        return JsonResult.error(f"数据库操作失败: {str(e)}")
    except Exception as e:
        return JsonResult.error(f"登录失败: {str(e)}")


@login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """用户登出"""
    try:
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]
            AuthMiddleware.destroy_session(token)

        return JsonResult.success(None, "登出成功")

    except Exception as e:
        return JsonResult.error(f"登出失败: {str(e)}")


@login_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        if not data:
            return JsonResult.error("请求数据不能为空", 400)

        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')
        email = data.get('email')

        if not username or not password:
            return JsonResult.error("用户名和密码不能为空", 400)

        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return JsonResult.error("用户名已存在", 400)

        # 检查手机号是否已存在
        if phone:
            existing_phone = User.query.filter_by(phone=phone).first()
            if existing_phone:
                return JsonResult.error("手机号已存在", 400)

        # 检查邮箱是否已存在
        if email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                return JsonResult.error("邮箱已存在", 400)

        # 创建新用户
        user_id = str(uuid.uuid4())
        new_user = User(
            id=user_id,
            username=username,
            avatar=data.get('avatar', '/static/images/default_avatar.png'),
            phone=phone or '',
            email=email or ''
        )

        # 保存用户
        db.session.add(new_user)
        db.session.flush()  # 获取用户ID

        # 保存密码
        user_password = UserPassword(
            id=str(uuid.uuid4()),
            user_id=user_id,
            password_hash=hash_password(password)
        )
        db.session.add(user_password)

        # 分配默认角色（普通用户）
        default_role = Role.query.filter_by(code='user', is_default=True).first()
        if default_role:
            user_role = UserRole(
                id=str(uuid.uuid4()),
                user_id=user_id,
                role_id=default_role.id
            )
            db.session.add(user_role)

        db.session.commit()

        return JsonResult.success({
            'id': new_user.id,
            'username': new_user.username,
            'avatar': new_user.avatar,
            'phone': new_user.phone,
            'email': new_user.email
        }, "注册成功", 201)

    except SQLAlchemyError as e:
        db.session.rollback()
        return JsonResult.error(f"数据库操作失败: {str(e)}")
    except Exception as e:
        return JsonResult.error(f"注册失败: {str(e)}")


@login_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """获取当前用户信息"""
    try:
        current_user = AuthMiddleware.get_current_user()
        if not current_user:
            return JsonResult.error("获取用户信息失败")

        return JsonResult.success(current_user['user_data'])

    except Exception as e:
        return JsonResult.error(f"获取用户信息失败: {str(e)}")


@login_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """更新当前用户信息"""
    try:
        current_user = AuthMiddleware.get_current_user()
        if not current_user:
            return JsonResult.error("获取用户信息失败", 401)

        user_id = current_user['user_id']
        data = request.get_json()
        if not data:
            return JsonResult.error("请求数据不能为空", 400)

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return JsonResult.error("用户不存在", 404)

        # 更新用户信息
        if 'avatar' in data:
            user.avatar = data['avatar']
        if 'phone' in data:
            # 检查手机号是否已被其他用户使用
            existing_phone = User.query.filter(
                User.phone == data['phone'],
                User.id != user_id
            ).first()
            if existing_phone:
                return JsonResult.error("手机号已被其他用户使用", 400)
            user.phone = data['phone']
        if 'email' in data:
            # 检查邮箱是否已被其他用户使用
            existing_email = User.query.filter(
                User.email == data['email'],
                User.id != user_id
            ).first()
            if existing_email:
                return JsonResult.error("邮箱已被其他用户使用", 400)
            user.email = data['email']

        db.session.commit()

        return JsonResult.success({
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'phone': user.phone,
            'email': user.email
        }, "更新成功")

    except SQLAlchemyError as e:
        db.session.rollback()
        return JsonResult.error(f"数据库操作失败: {str(e)}")
    except Exception as e:
        return JsonResult.error(f"更新用户信息失败: {str(e)}")


@login_bp.route('/change-password', methods=['PUT'])
@login_required
def change_password():
    """修改密码"""
    try:
        current_user = AuthMiddleware.get_current_user()
        if not current_user:
            return JsonResult.error("获取用户信息失败", 401)

        user_id = current_user['user_id']
        data = request.get_json()
        if not data:
            return JsonResult.error("请求数据不能为空", 400)

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not old_password or not new_password:
            return JsonResult.error("旧密码和新密码不能为空", 400)

        # 验证旧密码
        user_password = UserPassword.query.filter_by(user_id=user_id).first()
        if not user_password:
            return JsonResult.error("用户密码信息不存在", 404)

        old_hashed = hash_password(old_password)
        if user_password.password_hash != old_hashed:
            return JsonResult.error("旧密码错误", 400)

        # 更新密码
        user_password.password_hash = hash_password(new_password)
        db.session.commit()

        return JsonResult.success(None, "密码修改成功")

    except SQLAlchemyError as e:
        db.session.rollback()
        return JsonResult.error(f"数据库操作失败: {str(e)}")
    except Exception as e:
        return JsonResult.error(f"修改密码失败: {str(e)}")


@login_bp.route('/refresh-token', methods=['POST'])
@login_required
def refresh_token():
    """刷新访问令牌"""
    try:
        current_user = AuthMiddleware.get_current_user()
        if not current_user:
            return JsonResult.error("获取用户信息失败")

        # 生成新的访问令牌
        new_token = generate_token()
        old_token = current_user['token']

        # 销毁旧会话
        AuthMiddleware.destroy_session(old_token)

        # 创建新会话
        AuthMiddleware.create_session(
            current_user['user_id'],
            new_token,
            current_user['user_data']
        )

        return JsonResult.success({
            'token': new_token,
            'expires_in': 7200  # 2小时
        }, "令牌刷新成功")

    except Exception as e:
        return JsonResult.error(f"刷新令牌失败: {str(e)}")


@login_bp.route('/verify-code', methods=['GET'])
def get_verify_code():
    """获取验证码"""
    try:
        # 创建验证码生成器
        generator = VerifyCodeGenerator()
        # 生成验证码
        code, image_stream = generator.generate()
        
        # 将验证码存储在会话中，以便后续验证
        session['verify_code'] = code
        
        # 返回验证码图片
        response = send_file(
            image_stream,
            mimetype='image/png'
        )
        # 禁用缓存
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        return JsonResult.error(f"获取验证码失败: {str(e)}")
