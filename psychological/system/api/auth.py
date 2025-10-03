"""
登录认证API
提供用户登录、注册、密码重置等认证相关功能
"""
from flask import Blueprint, request, send_file, make_response
import uuid
from psychological.models.user import User
from psychological.models.role import Role
from psychological.models.user_role import UserRole
from psychological.models.base import db
from pcf_flask_helper.common import json_success, json_error
from psychological.utils.auth_manager import AuthManager
from psychological.utils.query import create_query_builder, assert_not_exists, assert_exists
from psychological.utils.model_helper import update_model_fields
from pcf_flask_helper.verify_code import VerifyCodeGenerator
from psychological.utils.auth import hash_password, generate_token, verify_password
from psychological.utils.image import process_image_url
from psychological.utils.cache.verify_code_cache import verify_code_cache
from psychological.utils.auth_helper import assert_current_user_id
from psychological.form.auth import LoginForm, UserLoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required

login_bp = Blueprint('auth', __name__, url_prefix='/auth')


@login_bp.route('/login', methods=['POST'])
@validate_form(LoginForm)
def login(form):
    """用户登录"""

    username = form.username.data
    password = form.password.data
    verify_code = form.verify_code.data

    # 从cookie中获取验证码UUID
    verify_code_uuid = request.cookies.get('verify_code_uuid')
    if not verify_code_uuid:
        return json_error("验证码已过期，请重新获取", 400)

    if not verify_code_cache.verify_code(verify_code_uuid, verify_code):
        return json_error("验证码错误", 400)

    # 查找用户
    user = assert_exists(User, User.username == username, "用户不存在")

    if not verify_password(password, user.password_hash):
        return json_error("用户名或密码错误", 401)

    # 生成访问令牌
    token = generate_token()

    # 获取用户角色信息
    user_roles = create_query_builder(Role) \
        .join(UserRole) \
        .filter(UserRole.user_id == user.id) \
        .all()

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
        return json_error("会话创建失败，请重试", 500)

    # 创建响应并清除验证码cookie
    response = make_response(json_success({
        'token': token,
        'user': user_data,
        'expires_in': 7200  # 2小时
    }, "登录成功"))

    # 登录成功后清除验证码cookie
    response.set_cookie('verify_code_uuid', '', expires=0)

    return response


@login_bp.route('/user-login', methods=['POST'])
@validate_form(UserLoginForm)
def user_login(form):
    """通用账户登录（支持用户名、手机号、邮箱）"""

    account = form.account.data
    password = form.password.data

    # 判断账户类型并查找用户
    # 检查是否为邮箱格式
    if '@' in account:
        user = assert_exists(User, User.email == account, "账户或密码错误", 401)
    # 检查是否为手机号格式
    elif account.isdigit() and len(account) == 11 and account.startswith('1'):
        user = assert_exists(User, User.phone == account, "账户或密码错误", 401)
    # 否则按用户名查找
    else:
        user = assert_exists(User, User.username == account, "账户或密码错误", 401)

    if not verify_password(password, user.password_hash):
        return json_error("账户或密码错误", 401)

    # 获取用户角色信息
    user_roles = create_query_builder(Role) \
        .join(UserRole) \
        .filter(UserRole.user_id == user.id) \
        .all()

    # 检查用户是否具有'user'角色
    has_user_role = any(role.code == 'user' for role in user_roles)
    if not has_user_role:
        return json_error("账户或密码错误", 401)

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
        return json_error("会话创建失败，请重试", 500)

    # 创建响应并清除验证码cookie
    response = make_response(json_success({
        'token': token,
        'user': user_data,
        'roles': roles_data,
        'expires_in': 7200  # 2小时
    }, "登录成功"))

    # 登录成功后清除验证码cookie
    response.set_cookie('verify_code_uuid', '', expires=0)

    return response


@login_bp.route('/logout', methods=['POST'])
@role_required(['admin', 'manager', 'user'])
@permission_required("auth:logout")
def logout():
    """用户登出"""
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token[7:]
        AuthManager.destroy_session(token)

    return json_success(None, "登出成功")


@login_bp.route('/register', methods=['POST'])
@validate_form(RegisterForm)
def register(form):
    """用户注册"""

    # 检查用户名是否已存在
    assert_not_exists(User, User.username == form.username.data, "用户名已存在")

    # 检查手机号是否已存在
    if form.phone.data:
        assert_not_exists(User, User.phone == form.phone.data, "手机号已存在")

    # 检查邮箱是否已存在
    if form.email.data:
        assert_not_exists(User, User.email == form.email.data, "邮箱已存在")

    # 创建新用户
    user_id = str(uuid.uuid4())
    new_user = User(
        id=user_id,
        username=form.username.data,
        avatar=form.avatar.data or process_image_url(
            '/static/images/default_avatar.png'),
        phone=form.phone.data or '',
        email=form.email.data or '',
        password_hash=hash_password(form.password.data)
    )

    try:
        # 保存用户
        db.session.add(new_user)
        db.session.flush()  # 获取用户ID

        # 分配默认角色（普通用户）
        default_role = assert_exists(Role, Role.code == 'user', "系统错误：默认用户角色不存在", 500)

        user_role = UserRole(
            id=str(uuid.uuid4()),
            user_id=user_id,
            role_id=default_role.id
        )
        db.session.add(user_role)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return json_error(f"注册失败: {str(e)}", 500)

    return json_success({
        'id': new_user.id,
        'username': new_user.username,
        'avatar': new_user.avatar,
        'phone': new_user.phone,
        'code': new_user.email
    }, "注册成功", 201)


@login_bp.route('/profile', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("auth:get_profile")
def get_profile():
    """获取当前用户信息"""
    _ = assert_current_user_id()

    current_user = AuthManager.get_current_user()
    if not current_user:
        return json_error("获取用户信息失败")

    return json_success(current_user['user'])


@login_bp.route('/profile', methods=['PUT'])
@validate_form(UpdateProfileForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("auth:update_profile")
def update_profile(form):
    """更新当前用户信息"""

    current_user = AuthManager.get_current_user()
    if not current_user:
        return json_error("获取用户信息失败", 401)

    user_id = current_user['user_id']
    user = assert_exists(User, User.id == user_id, "用户不存在")

    # 检查手机号和邮箱唯一性（如果有更新的话）
    if form.phone.data:
        assert_not_exists(User, [User.phone == form.phone.data, User.id != user_id], "手机号已被其他用户使用")

    if form.email.data:
        assert_not_exists(User, [User.email == form.email.data, User.id != user_id], "邮箱已被其他用户使用")

    # 使用update_model_from_form简化更新逻辑
    update_model_fields(user, form)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return json_error(f"更新失败: {str(e)}", 500)

    # 更新Redis中的用户会话信息
    updated_user_data = user.to_dict()
    updated_user_data['avatar'] = user.avatar

    # 获取用户角色信息
    user_roles = create_query_builder(Role) \
        .join(UserRole) \
        .filter(UserRole.user_id == user.id) \
        .all()
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

    return json_success(updated_user_data, "更新成功")


@login_bp.route('/change-password', methods=['PUT'])
@validate_form(ChangePasswordForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("auth:change_password")
def change_password(form):
    """修改密码"""

    current_user = AuthManager.get_current_user()
    if not current_user:
        return json_error("获取用户信息失败", 401)

    user_id = current_user['user_id']
    old_password = form.old_password.data
    new_password = form.new_password.data

    # 获取用户信息
    user = assert_exists(User, User.id == user_id, "用户不存在")

    # 验证旧密码
    if not user.password_hash:
        return json_error("用户密码信息不存在", 404)

    if not verify_password(old_password, user.password_hash):
        return json_error("旧密码错误", 400)

    # 检查新密码是否与当前密码相同
    if verify_password(new_password, user.password_hash):
        return json_error("新密码不能与当前密码相同", 400)

    # 更新密码
    user.password_hash = hash_password(new_password)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return json_error(f"密码修改失败: {str(e)}", 500)

    return json_success(None, "密码修改成功")


@login_bp.route('/refresh-token', methods=['POST'])
@role_required(['admin', 'manager', 'user'])
@permission_required("auth:refresh_token")
def refresh_token():
    """刷新访问令牌"""
    current_user = AuthManager.get_current_user()
    if not current_user:
        return json_error("获取用户信息失败")

    # 生成新的访问令牌
    new_token = generate_token()
    old_token = current_user['token']

    # 销毁旧会话
    AuthManager.destroy_session(old_token)

    # 获取用户最新信息
    user = assert_exists(User, User.id == current_user['user_id'], "用户不存在")

    # 获取用户角色信息
    user_roles = create_query_builder(Role) \
        .join(UserRole) \
        .filter(UserRole.user_id == user.id) \
        .all()

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
        return json_error("令牌刷新失败，请重新登录", 500)

    return json_success({
        'token': new_token,
        'user': user_data,
        'roles': roles_data,
        'expires_in': 7200  # 2小时
    }, "令牌刷新成功")


@login_bp.route('/verify-code', methods=['GET'])
def get_verify_code():
    """获取验证码（公开接口）"""
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
