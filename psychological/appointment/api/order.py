"""
订单管理API
提供订单的增删改查及状态管理功能
"""
from flask import Blueprint
import uuid
from psychological.models.order import Order
from psychological.models.user import User
from pcf_flask_helper.common import json_success, json_error
from psychological.utils.validate import assert_id_exists
from psychological.utils.query import create_query_builder
from psychological.utils.model_helper import update_model_fields
from psychological.utils.auth_helper import assert_current_user_id, is_manager_user
from psychological.models.base import db
from psychological.form.order import OrderQueryForm, OrderCreateForm, OrderUpdateForm
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required

order_bp = Blueprint('order', __name__, url_prefix='/order')


@order_bp.route('', methods=['GET'])
@validate_form(OrderQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("order:get_orders")
def get_orders(form):
    """获取订单列表"""
    # 获取当前用户信息
    current_user_id = assert_current_user_id()
    is_manager = is_manager_user()

    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(Order) \
        .unless(is_manager, Order.user_id == current_user_id) \
        .when(form.user_id.data, Order.user_id == form.user_id.data) \
        .when(form.product_id.data, Order.product_id == form.product_id.data) \
        .when(form.type.data, Order.type == form.type.data) \
        .when(form.status.data, Order.status == form.status.data) \
        .order_by(Order.create_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return json_success({
        'orders': [order.to_dict() for order in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@order_bp.route('/<order_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("order:get_order")
def get_order(order_id):
    """获取单个订单详情"""
    assert_id_exists(order_id, "订单ID不能为空")

    # 获取当前用户信息
    current_user_id = assert_current_user_id()
    is_manager = is_manager_user()

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return json_error('订单不存在', 404)

    # 权限检查：普通用户只能查看自己的订单
    if not is_manager and order.user_id != current_user_id:
        return json_error('无权限查看该订单', 403)

    return json_success(order.to_dict())


@order_bp.route('', methods=['POST'])
@validate_form(OrderCreateForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("order:create_order")
def create_order(form):
    """创建订单"""
    # 验证用户是否存在
    user = create_query_builder(User) \
        .filter(User.id == form.user_id.data) \
        .first()
    if not user:
        return json_error('用户不存在', 400)

    # 创建订单
    order = Order(
        id=str(uuid.uuid4()),
        user_id=form.user_id.data,
        product_id=form.product_id.data,
        type=form.type.data,
        amount=form.amount.data,
        status=form.status.data or 'pending'
    )

    db.session.add(order)
    db.session.commit()

    return json_success(order.to_dict(), '订单创建成功', 201)


@order_bp.route('/<order_id>', methods=['PUT'])
@validate_form(OrderUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("order:update_order")
def update_order(order_id, form):
    """更新订单"""
    assert_id_exists(order_id, "订单ID不能为空")

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return json_error('订单不存在', 404)

    # 使用统一的更新函数
    update_model_fields(order, form)

    db.session.commit()
    return json_success(order.to_dict(), '订单更新成功')


@order_bp.route('/<order_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("order:delete_order")
def delete_order(order_id):
    """删除订单"""
    assert_id_exists(order_id, "订单ID不能为空")

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return json_error('订单不存在', 404)

    # 检查订单状态，已支付的订单不能删除
    if order.status in ['paid', 'completed']:
        return json_error('已支付或已完成的订单不能删除', 400)

    db.session.delete(order)
    db.session.commit()
    return json_success(None, '订单删除成功')


@order_bp.route('/<order_id>/pay', methods=['POST'])
@role_required(['admin', 'manager', 'user'])
@permission_required("order:pay_order")
def pay_order(order_id):
    """支付订单"""
    assert_id_exists(order_id, "订单ID不能为空")

    # 获取当前用户信息
    current_user_id = assert_current_user_id()
    is_manager = is_manager_user()

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return json_error('订单不存在', 404)

    # 权限检查：普通用户只能支付自己的订单
    if not is_manager and order.user_id != current_user_id:
        return json_error('无权限支付该订单', 403)

    if order.status != 'pending':
        return json_error('只有待支付的订单才能进行支付', 400)

    # 更新订单状态为已支付
    order.status = 'paid'
    db.session.commit()

    return json_success(order.to_dict(), '订单支付成功')


@order_bp.route('/<order_id>/cancel', methods=['POST'])
@role_required(['admin', 'manager', 'user'])
@permission_required("order:cancel_order")
def cancel_order(order_id):
    """取消订单"""
    assert_id_exists(order_id, "订单ID不能为空")

    # 获取当前用户信息
    current_user_id = assert_current_user_id()
    is_manager = is_manager_user()

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return json_error('订单不存在', 404)

    # 权限检查：普通用户只能取消自己的订单
    if not is_manager and order.user_id != current_user_id:
        return json_error('无权限取消该订单', 403)

    if order.status not in ['pending', 'paid']:
        return json_error('只有待支付或已支付的订单才能取消', 400)

    # 更新订单状态
    if order.status == 'paid':
        order.status = 'refunded'  # 已支付的订单取消后变为已退款
    else:
        order.status = 'cancelled'  # 待支付的订单直接取消

    db.session.commit()

    return json_success(order.to_dict(), '订单取消成功')


@order_bp.route('/<order_id>/complete', methods=['POST'])
@role_required(['admin', 'manager'])
@permission_required("order:complete_order")
def complete_order(order_id):
    """完成订单"""
    assert_id_exists(order_id, "订单ID不能为空")

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return json_error('订单不存在', 404)

    if order.status != 'paid':
        return json_error('只有已支付的订单才能完成', 400)

    # 更新订单状态为已完成
    order.status = 'completed'
    db.session.commit()

    return json_success(order.to_dict(), '订单完成成功')
