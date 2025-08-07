"""
登录认证API
提供用户登录、注册、密码重置等认证相关功能

接口列表：
- POST /login - 用户名登录
- POST /phone-login - 手机号登录
- POST /register - 用户注册
- POST /logout - 用户登出
- POST /reset-password - 重置密码
- POST /verify-code - 验证码验证
- POST /send-code - 发送验证码
- GET /user/info - 获取当前用户信息
- POST /refresh-token - 刷新访问令牌
"""
from flask import Blueprint, request, send_file, make_response
import uuid
from models.user import User
from models.role import Role
from models.user_role import UserRole
from utils.json_result import JsonResult
from utils.auth_manager import AuthManager
from models.base import db
from utils.verify_code import VerifyCodeGenerator
from utils.validate import validate_form
from utils.auth import hash_password, generate_token, verify_password
from form.auth import LoginForm, PhoneLoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm
from utils.image import process_image_url
from utils.cache.verify_code_cache import verify_code_cache

login_bp = Blueprint('auth', __name__, url_prefix='/auth')


@login_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    form = validate_form(LoginForm)

    username = form.username.data
    password = form.password.data
    verify_code = form.verify_code.data

    # 从cookie中获取验证码UUID
    verify_code_uuid = request.cookies.get('verify_code_uuid')
    if not verify_code_uuid:
        return JsonResult.error("验证码已过期，请重新获取", 400)

    if not verify_code_cache.verify_code(verify_code_uuid, verify_code):
        return JsonResult.error("验证码错误", 400)

    # 查找用户
    user = User.query.filter_by(username=username).first()
    if not user:
        return JsonResult.error("用户名或密码错误", 401)

    if not verify_password(password, user.password_hash):
        return JsonResult.error("用户名或密码错误", 401)

    # 生成访问令牌
    token = generate_token()

    # 获取用户角色信息
    user_roles_query = db.session.query(UserRole, Role).join(
        Role, UserRole.role_id == Role.id
    ).filter(UserRole.user_id == user.id)

    user_roles = [role for _, role in user_roles_query.all()]

    # 创建会话 - user_data包含User模型的所有数据（除了密码）
    user_data = user.to_dict()  # 使用User模型的to_dict方法
    # 处理头像URL
    user_data['avatar'] = process_image_url(user.avatar)

    # 角色信息
    roles_data = [{
        'id': role.id,
        'name': role.name,
        'code': role.code
    } for role in user_roles]
    print("角色信息", roles_data)

    # 创建会话并检查结果
    session_created = AuthManager.create_session(user.id, token, user_data, roles_data)
    if not session_created:
        return JsonResult.error("会话创建失败，请重试", 500)

    # 创建响应并清除验证码cookie
    response = make_response(JsonResult.success({
        'token': token,
        'user': user_data,
        'expires_in': 7200  # 2小时
    }, "登录成功"))

    # 登录成功后清除验证码cookie
    response.set_cookie('verify_code_uuid', '', expires=0)

    return response


@login_bp.route('/phone-login', methods=['POST'])
def phone_login():
    """手机号登录"""
    form = validate_form(PhoneLoginForm)

    phone = form.phone.data
    password = form.password.data

    # 通过手机号查找用户
    user = User.query.filter_by(phone=phone).first()
    if not user:
        return JsonResult.error("手机号或密码错误", 401)

    if not verify_password(password, user.password_hash):
        return JsonResult.error("手机号或密码错误", 401)

    # 获取用户角色信息
    user_roles_query = db.session.query(UserRole, Role).join(
        Role, UserRole.role_id == Role.id
    ).filter(UserRole.user_id == user.id)

    user_roles = [role for _, role in user_roles_query.all()]
    
    # 检查用户是否具有'user'角色
    has_user_role = any(role.code == 'user' for role in user_roles)
    if not has_user_role:
        return JsonResult.error("手机号或密码错误", 401)

    # 生成访问令牌
    token = generate_token()

    # 创建会话 - user_data包含User模型的所有数据（除了密码）
    user_data = user.to_dict()  # 使用User模型的to_dict方法
    # 处理头像URL
    user_data['avatar'] = process_image_url(user.avatar)

    # 角色信息
    roles_data = [{
        'id': role.id,
        'name': role.name,
        'code': role.code
    } for role in user_roles]

    # 创建会话并检查结果
    session_created = AuthManager.create_session(user.id, token, user_data, roles_data)
    if not session_created:
        return JsonResult.error("会话创建失败，请重试", 500)

    # 创建响应并清除验证码cookie
    response = make_response(JsonResult.success({
        'token': token,
        'user': user_data,
        'roles': roles_data,
        'expires_in': 7200  # 2小时
    }, "登录成功"))

    # 登录成功后清除验证码cookie
    response.set_cookie('verify_code_uuid', '', expires=0)

    return response


@login_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token[7:]
        AuthManager.destroy_session(token)

    return JsonResult.success(None, "登出成功")


@login_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    form = validate_form(RegisterForm)

    username = form.username.data
    password = form.password.data
    phone = form.phone.data
    email = form.email.data

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
        avatar=form.avatar.data or process_image_url(
            '/static/images/default_avatar.png'),
        phone=phone or '',
        email=email or '',
        password_hash=hash_password(password)
    )

    # 保存用户
    db.session.add(new_user)
    db.session.flush()  # 获取用户ID

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


@login_bp.route('/profile', methods=['GET'])
def get_profile():
    """获取当前用户信息"""
    current_user = AuthManager.get_current_user()
    if not current_user:
        return JsonResult.error("获取用户信息失败")

    return JsonResult.success(current_user['user'])


@login_bp.route('/profile', methods=['PUT'])
def update_profile():
    """更新当前用户信息"""
    form = validate_form(UpdateProfileForm)

    current_user = AuthManager.get_current_user()
    if not current_user:
        return JsonResult.error("获取用户信息失败", 401)

    user_id = current_user['user_id']
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return JsonResult.error("用户不存在", 404)

    # 更新用户信息
    if form.avatar.data is not None:
        user.avatar = form.avatar.data
    if form.phone.data:
        # 检查手机号是否已被其他用户使用
        existing_phone = User.query.filter(
            User.phone == form.phone.data,
            User.id != user_id
        ).first()
        if existing_phone:
            return JsonResult.error("手机号已被其他用户使用", 400)
        user.phone = form.phone.data
    if form.email.data:
        # 检查邮箱是否已被其他用户使用
        existing_email = User.query.filter(
            User.email == form.email.data,
            User.id != user_id
        ).first()
        if existing_email:
            return JsonResult.error("邮箱已被其他用户使用", 400)
        user.email = form.email.data
    if form.real_name.data is not None:
        user.real_name = form.real_name.data
    if form.gender.data is not None:
        user.gender = form.gender.data
    if form.birth_date.data is not None:
        user.birth_date = form.birth_date.data
    if form.brief_introduction.data is not None:
        user.brief_introduction = form.brief_introduction.data

    db.session.commit()

    # 更新Redis中的用户会话信息
    updated_user_data = user.to_dict()
    updated_user_data['avatar'] = user.avatar
    
    # 获取用户角色信息
    user_roles_query = db.session.query(UserRole, Role).join(
        Role, UserRole.role_id == Role.id
    ).filter(UserRole.user_id == user.id)

    user_roles = [role for _, role in user_roles_query.all()]
    roles_data = [{
        'id': role.id,
        'name': role.name,
        'code': role.code
    } for role in user_roles]
    
    # 获取当前用户的token
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token[7:]
        # 更新会话中的用户数据
        AuthManager.update_user_session(token, updated_user_data, roles_data)

    return JsonResult.success(updated_user_data, "更新成功")


@login_bp.route('/change-password', methods=['PUT'])
def change_password():
    """修改密码"""
    form = validate_form(ChangePasswordForm)

    current_user = AuthManager.get_current_user()
    if not current_user:
        return JsonResult.error("获取用户信息失败", 401)

    user_id = current_user['user_id']
    old_password = form.old_password.data
    new_password = form.new_password.data

    # 获取用户信息
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return JsonResult.error("用户不存在", 404)

    # 验证旧密码
    if not user.password_hash:
        return JsonResult.error("用户密码信息不存在", 404)

    if not verify_password(old_password, user.password_hash):
        return JsonResult.error("旧密码错误", 400)

    # 检查新密码是否与当前密码相同
    if verify_password(new_password, user.password_hash):
        return JsonResult.error("新密码不能与当前密码相同", 400)

    # 更新密码
    user.password_hash = hash_password(new_password)
    db.session.commit()

    return JsonResult.success(None, "密码修改成功")


@login_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    """刷新访问令牌"""
    current_user = AuthManager.get_current_user()
    if not current_user:
        return JsonResult.error("获取用户信息失败")

    # 生成新的访问令牌
    new_token = generate_token()
    old_token = current_user['token']

    # 销毁旧会话
    AuthManager.destroy_session(old_token)

    # 获取用户最新信息
    user = User.query.filter_by(id=current_user['user_id']).first()
    if not user:
        return JsonResult.error("用户不存在", 404)

    # 获取用户角色信息
    user_roles_query = db.session.query(UserRole, Role).join(
        Role, UserRole.role_id == Role.id
    ).filter(UserRole.user_id == user.id)

    user_roles = [role for _, role in user_roles_query.all()]

    # 创建最新的用户数据
    user_data = user.to_dict()
    user_data['avatar'] = process_image_url(user.avatar)

    # 角色信息
    roles_data = [{
        'id': role.id,
        'name': role.name,
        'code': role.code
    } for role in user_roles]

    # 创建新会话
    session_created = AuthManager.create_session(
        user.id,
        new_token,
        user_data,
        roles_data
    )

    if not session_created:
        return JsonResult.error("令牌刷新失败，请重新登录", 500)

    return JsonResult.success({
        'token': new_token,
        'user': user_data,
        'roles': roles_data,
        'expires_in': 7200  # 2小时
    }, "令牌刷新成功")


@login_bp.route('/verify-code', methods=['GET'])
def get_verify_code():
    """获取验证码"""
    # 生成验证码UUID
    verify_code_uuid = str(uuid.uuid4())

    # 创建验证码生成器
    generator = VerifyCodeGenerator()
    # 生成验证码
    code, image_stream = generator.generate()

    # 将验证码存储到Redis中，使用UUID作为标识符，过期时间5分钟
    verify_code_cache.store_verify_code(verify_code_uuid, code)

    # 返回验证码图片
    response = send_file(
        image_stream,
        mimetype='image/png'
    )

    # 设置验证码UUID到cookie，过期时间5分钟
    response.set_cookie(
        'verify_code_uuid',
        verify_code_uuid,
        max_age=300,  # 5分钟
        httponly=True,  # 防止XSS攻击
        samesite='Lax'  # 跨域兼容性
    )

    # 禁用缓存
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response
