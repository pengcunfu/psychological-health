"""
课程订阅
"""
from flask import Blueprint
from ..models import CourseSubscription, Course
from psychological.system.models import User
from pcf_flask_helper.model.base import db
from pcf_flask_helper.common import json_success, json_error
from pcf_flask_helper.form.validate import assert_id_exists
from pcf_flask_helper.model.query import create_query_builder
from psychological.utils.auth_helper import get_roles, assert_current_user_id, is_manager_user
from ..form import (
    CourseSubscriptionCreateForm,
    CourseSubscriptionUpdateForm,
    CourseSubscriptionListForm,
    ProgressUpdateForm,
    SubscriptionExtendForm,
    SubscriptionCancelForm
)
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required
import uuid

course_subscription_bp = Blueprint('course_subscription', __name__, url_prefix='/course-subscription')


@course_subscription_bp.route('', methods=['GET'])
@validate_form(CourseSubscriptionListForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("course_subscription:get_course_subscriptions")
def get_course_subscriptions(form):
    """获取课程订阅列表（支持权限控制）"""
    # 获取当前用户信息
    current_user_id = assert_current_user_id()
    user_roles = get_roles()
    has_manage_permission = is_manager_user()

    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(CourseSubscription) \
        .unless(has_manage_permission, CourseSubscription.user_id == current_user_id) \
        .when(has_manage_permission and form.user_id.data, CourseSubscription.user_id == form.user_id.data) \
        .when(form.course_id.data, CourseSubscription.course_id == form.course_id.data) \
        .when(form.status.data, CourseSubscription.status == form.status.data) \
        .when(form.subscription_type.data, CourseSubscription.subscription_type == form.subscription_type.data) \
        .order_by(CourseSubscription.subscription_date.desc()) \
        .paginate(form.page.data or 1, form.per_page.data or 10, 100)

    subscriptions_data = []
    for subscription in result['items']:
        subscription_dict = subscription.to_dict()

        # 根据权限决定是否显示用户信息
        if has_manage_permission:
            # 管理员可以看到用户信息
            user = User.query.filter_by(id=subscription.user_id).first()
            if user:
                subscription_dict['user_info'] = {
                    'username': user.username,
                    'phone': user.phone,
                    'email': user.email
                }

        # 添加课程信息
        course = Course.query.filter_by(id=subscription.course_id).first()
        if course:
            subscription_dict['course_info'] = {
                'title': course.title,
                'teacher': course.teacher,
                'cover_image': course.cover_image
            }

        subscriptions_data.append(subscription_dict)

    return json_success({
        'list': subscriptions_data,
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages'],
        'user_roles': user_roles,
        'has_manage_permission': has_manage_permission
    })


@course_subscription_bp.route('/<subscription_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("course_subscription:get_subscription_detail")
def get_subscription_detail(subscription_id):
    """获取订阅详情（支持权限控制）"""
    assert_id_exists(subscription_id, "订阅ID不能为空")

    current_user_id = assert_current_user_id()
    has_manage_permission = is_manager_user()

    subscription = CourseSubscription.query.filter_by(id=subscription_id).first()
    if not subscription:
        return json_error('订阅记录不存在')

    # 权限检查：管理员可以查看所有，普通用户只能查看自己的
    if not has_manage_permission:
        if subscription.user_id != current_user_id:
            return json_error('无权限查看该订阅记录', 403)

    subscription_dict = subscription.to_dict()

    # 添加课程详细信息
    course = Course.query.filter_by(id=subscription.course_id).first()
    if course:
        subscription_dict['course_info'] = course.to_dict()

    # 管理员可以看到用户信息
    if has_manage_permission:
        user = User.query.filter_by(id=subscription.user_id).first()
        if user:
            subscription_dict['user_info'] = {
                'id': user.id,
                'username': user.username,
                'phone': user.phone,
                'email': user.email
            }

    return json_success(subscription_dict)


@course_subscription_bp.route('', methods=['POST'])
@validate_form(CourseSubscriptionCreateForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("course_subscription:create_subscription")
def create_subscription(form):
    """创建课程订阅（普通用户只能为自己创建）"""
    current_user_id = assert_current_user_id()
    has_manage_permission = is_manager_user()

    # 生成唯一ID
    subscription_id = str(uuid.uuid4())

    # 检查课程是否存在
    course = Course.query.filter_by(id=form.course_id.data).first()
    if not course:
        return json_error('课程不存在')

    # 确定用户ID
    target_user_id = current_user_id
    if has_manage_permission and hasattr(form, 'user_id') and form.user_id.data:
        # 管理员可以为指定用户创建订阅
        target_user_id = form.user_id.data
        user = User.query.filter_by(id=target_user_id).first()
        if not user:
            return json_error('指定的用户不存在')

    # 检查是否已有有效订阅
    existing = create_query_builder(CourseSubscription) \
        .filter(
        CourseSubscription.user_id == target_user_id,
        CourseSubscription.course_id == form.course_id.data,
        CourseSubscription.status == 'active'
    ) \
        .first()
    if existing:
        return json_error('您已经订阅了该课程')

    # 创建订阅记录
    subscription = CourseSubscription(
        id=subscription_id,
        user_id=target_user_id,
        course_id=form.course_id.data,
        subscription_type=form.subscription_type.data or 'standard',
        paid_price=form.paid_price.data,
        original_price=form.original_price.data,
        discount_amount=form.discount_amount.data or 0.0,
        order_id=form.order_id.data,
        payment_method=form.payment_method.data,
        payment_transaction_id=form.payment_transaction_id.data,
        notes=form.notes.data
    )

    db.session.add(subscription)
    db.session.commit()

    return json_success(subscription.to_dict(), '订阅创建成功')


@course_subscription_bp.route('/<subscription_id>', methods=['PUT'])
@validate_form(CourseSubscriptionUpdateForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("course_subscription:update_subscription")
def update_subscription(subscription_id, form):
    """更新订阅信息（支持权限控制）"""
    assert_id_exists(subscription_id, "订阅ID不能为空")

    current_user_id = assert_current_user_id()
    has_manage_permission = is_manager_user()

    subscription = CourseSubscription.query.filter_by(id=subscription_id).first()
    if not subscription:
        return json_error('订阅记录不存在')

    # 权限检查：管理员可以修改所有，普通用户只能修改自己的
    if not has_manage_permission:
        if subscription.user_id != current_user_id:
            return json_error('无权限修改该订阅记录', 403)

    # 更新字段
    if form.subscription_type.data:
        subscription.subscription_type = form.subscription_type.data

    if form.status.data:
        subscription.status = form.status.data

    if form.completed_lessons.data is not None:
        subscription.completed_lessons = form.completed_lessons.data
        # 简单的进度计算
        if form.completed_lessons.data > 0:
            subscription.progress_percentage = min(form.completed_lessons.data * 10, 100)

    if form.total_study_time.data is not None:
        subscription.total_study_time = form.total_study_time.data

    if form.notes.data is not None:
        subscription.notes = form.notes.data

    try:
        db.session.commit()
        return json_success(subscription.to_dict(), '订阅更新成功')
    except Exception as e:
        db.session.rollback()
        return json_error(f'更新失败: {str(e)}')


@course_subscription_bp.route('/<subscription_id>/progress', methods=['PUT'])
@validate_form(ProgressUpdateForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("course_subscription:update_progress")
def update_progress(subscription_id, form):
    """更新学习进度（用户只能更新自己的）"""
    assert_id_exists(subscription_id, "订阅ID不能为空")

    current_user_id = assert_current_user_id()

    subscription = CourseSubscription.query.filter_by(id=subscription_id).first()
    if not subscription:
        return json_error('订阅记录不存在')

    # 权限检查：只能更新自己的进度
    if subscription.user_id != current_user_id:
        return json_error('无权限更新该订阅的学习进度', 403)

    # 检查订阅是否有效
    if not subscription.is_active():
        return json_error('订阅已失效，无法更新学习进度')

    try:
        subscription.update_progress(
            completed_lessons=form.completed_lessons.data,
            study_time_minutes=form.study_time_minutes.data
        )
        db.session.commit()
        return json_success(subscription.to_dict(), '学习进度更新成功')
    except Exception as e:
        db.session.rollback()
        return json_error(f'更新失败: {str(e)}')


@course_subscription_bp.route('/<subscription_id>/extend', methods=['PUT'])
@validate_form(SubscriptionExtendForm)
@role_required(['admin', 'manager'])
@permission_required("course_subscription:extend_subscription")
def extend_subscription(subscription_id, form):
    """延长订阅（管理员操作）"""
    assert_id_exists(subscription_id, "订阅ID不能为空")

    subscription = CourseSubscription.query.filter_by(id=subscription_id).first()
    if not subscription:
        return json_error('订阅记录不存在')

    try:
        subscription.extend_subscription(days=form.days.data)
        db.session.commit()
        return json_success(subscription.to_dict(), f'订阅已延长{form.days.data}天')
    except Exception as e:
        db.session.rollback()
        return json_error(f'延长失败: {str(e)}')


@course_subscription_bp.route('/<subscription_id>/cancel', methods=['PUT'])
@validate_form(SubscriptionCancelForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("course_subscription:cancel_subscription")
def cancel_subscription(subscription_id, form):
    """取消订阅（用户可以取消自己的，管理员可以取消任何）"""
    assert_id_exists(subscription_id, "订阅ID不能为空")

    current_user_id = assert_current_user_id()
    has_manage_permission = is_manager_user()

    subscription = CourseSubscription.query.filter_by(id=subscription_id).first()
    if not subscription:
        return json_error('订阅记录不存在')

    # 权限检查
    if not has_manage_permission:
        if subscription.user_id != current_user_id:
            return json_error('无权限取消该订阅', 403)

    if subscription.status == 'cancelled':
        return json_error('订阅已经被取消')

    try:
        subscription.cancel_subscription(reason=form.reason.data)
        db.session.commit()
        return json_success(subscription.to_dict(), '订阅已取消')
    except Exception as e:
        db.session.rollback()
        return json_error(f'取消失败: {str(e)}')


@course_subscription_bp.route('/<subscription_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("course_subscription:delete_subscription")
def delete_subscription(subscription_id):
    """删除订阅记录（管理员专用）"""
    assert_id_exists(subscription_id, "订阅ID不能为空")

    subscription = CourseSubscription.query.filter_by(id=subscription_id).first()
    if not subscription:
        return json_error('订阅记录不存在')

    try:
        db.session.delete(subscription)
        db.session.commit()
        return json_success(message='订阅记录删除成功')
    except Exception as e:
        db.session.rollback()
        return json_error(f'删除失败: {str(e)}')


@course_subscription_bp.route('/my', methods=['GET'])
@validate_form(CourseSubscriptionListForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("course_subscription:get_my_subscriptions")
def get_my_subscriptions(form):
    """获取当前用户的订阅列表"""
    current_user_id = assert_current_user_id()

    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(CourseSubscription) \
        .filter(CourseSubscription.user_id == current_user_id) \
        .when(form.status.data, CourseSubscription.status == form.status.data) \
        .when(form.subscription_type.data, CourseSubscription.subscription_type == form.subscription_type.data) \
        .order_by(CourseSubscription.subscription_date.desc()) \
        .paginate(form.page.data or 1, form.per_page.data or 10, 100)

    subscriptions_data = []
    for subscription in result['items']:
        subscription_dict = subscription.to_simple_dict()

        # 添加课程信息
        course = Course.query.filter_by(id=subscription.course_id).first()
        if course:
            subscription_dict['course_info'] = {
                'title': course.title,
                'teacher': course.teacher,
                'cover_image': course.cover_image,
                'lesson_count': course.lesson_count
            }

        subscriptions_data.append(subscription_dict)

    return json_success({
        'list': subscriptions_data,
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@course_subscription_bp.route('/stats', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("course_subscription:get_subscription_stats")
def get_subscription_stats():
    """获取订阅统计信息（支持权限）"""
    current_user_id = assert_current_user_id()
    has_manage_permission = is_manager_user()

    if has_manage_permission:
        # 管理员看全局统计
        base_builder = create_query_builder(CourseSubscription)
    else:
        # 普通用户看自己的统计
        base_builder = create_query_builder(CourseSubscription).filter(CourseSubscription.user_id == current_user_id)

    total_count = base_builder.count()
    active_count = base_builder.filter(CourseSubscription.status == 'active').count()
    expired_count = base_builder.filter(CourseSubscription.status == 'expired').count()
    cancelled_count = base_builder.filter(CourseSubscription.status == 'cancelled').count()

    # 计算总收入（仅管理员）
    total_revenue = 0
    if has_manage_permission:
        result = db.session.query(db.func.sum(CourseSubscription.paid_price)).filter(
            CourseSubscription.status != 'cancelled'
        ).scalar()
        total_revenue = float(result) if result else 0

    return json_success({
        'total_count': total_count,
        'active_count': active_count,
        'expired_count': expired_count,
        'cancelled_count': cancelled_count,
        'total_revenue': total_revenue if has_manage_permission else None,
        'is_global_stats': has_manage_permission
    })
