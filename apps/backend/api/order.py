"""
订单管理API
提供订单的增删改查及状态管理功能

接口列表：
- GET /order - 获取订单列表
- GET /order/<order_id> - 获取单个订单详情
- POST /order - 创建订单
- PUT /order/<order_id> - 更新订单
- DELETE /order/<order_id> - 删除订单
- PUT /order/<order_id>/status - 更新订单状态
- POST /order/<order_id>/pay - 支付订单
- POST /order/<order_id>/cancel - 取消订单
- POST /order/<order_id>/refund - 退款订单
- GET /order/user/<user_id> - 获取用户的订单列表
- GET /order/stats - 获取订单统计数据
"""
from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
import uuid
from models.order import Order
from models.user import User
from utils.json_result import JsonResult
from models.base import db
from form.order import OrderQueryForm, OrderCreateForm, OrderUpdateForm

order_bp = Blueprint('order', __name__, url_prefix='/order')


@order_bp.route('', methods=['GET'])
def get_orders():
    """获取订单列表"""
    # 使用表单验证查询参数
    form = OrderQueryForm(data=request.args)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 构建查询
    query = Order.query

    if form.get_user_id():
        query = query.filter(Order.user_id == form.get_user_id())
    if form.get_product_id():
        query = query.filter(Order.product_id == form.get_product_id())
    if form.get_type():
        query = query.filter(Order.type == form.get_type())
    if form.get_status():
        query = query.filter(Order.status == form.get_status())

    # 分页查询
    pagination = query.order_by(Order.create_time.desc()).paginate(
        page=form.get_page(),
        per_page=form.get_per_page(),
        error_out=False
    )

    return JsonResult.success({
        'orders': [order.to_dict() for order in pagination.items],
        'total': pagination.total,
        'page': form.get_page(),
        'per_page': form.get_per_page(),
        'pages': pagination.pages
    })


@order_bp.route('/<order_id>', methods=['GET'])
def get_order(order_id):
    """获取单个订单详情"""
    if not order_id or not order_id.strip():
        return JsonResult.error('订单ID不能为空', 400)

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return JsonResult.error('订单不存在', 404)

    return JsonResult.success(order.to_dict())


@order_bp.route('', methods=['POST'])
def create_order():
    """创建订单"""
    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    # 使用表单验证数据
    form = OrderCreateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 验证用户是否存在
    user = User.query.filter_by(id=form.user_id.data).first()
    if not user:
        return JsonResult.error('用户不存在', 400)

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

    return JsonResult.success(order.to_dict(), '订单创建成功', 201)


@order_bp.route('/<order_id>', methods=['PUT'])
def update_order(order_id):
    """更新订单"""
    if not order_id or not order_id.strip():
        return JsonResult.error('订单ID不能为空', 400)

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return JsonResult.error('订单不存在', 404)

    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    # 使用表单验证数据
    form = OrderUpdateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 更新订单信息
    if form.product_id.data is not None:
        order.product_id = form.product_id.data
    if form.type.data is not None:
        order.type = form.type.data
    if form.amount.data is not None:
        order.amount = form.amount.data
    if form.status.data is not None:
        order.status = form.status.data

    db.session.commit()
    return JsonResult.success(order.to_dict(), '订单更新成功')


@order_bp.route('/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    """删除订单"""
    if not order_id or not order_id.strip():
        return JsonResult.error('订单ID不能为空', 400)

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return JsonResult.error('订单不存在', 404)

    # 检查订单状态，已支付的订单不能删除
    if order.status in ['paid', 'completed']:
        return JsonResult.error('已支付或已完成的订单不能删除', 400)

    db.session.delete(order)
    db.session.commit()
    return JsonResult.success(None, '订单删除成功')


@order_bp.route('/<order_id>/pay', methods=['POST'])
def pay_order(order_id):
    """支付订单"""
    if not order_id or not order_id.strip():
        return JsonResult.error('订单ID不能为空', 400)

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return JsonResult.error('订单不存在', 404)

    if order.status != 'pending':
        return JsonResult.error('只有待支付的订单才能进行支付', 400)

    # 更新订单状态为已支付
    order.status = 'paid'
    db.session.commit()

    return JsonResult.success(order.to_dict(), '订单支付成功')


@order_bp.route('/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """取消订单"""
    if not order_id or not order_id.strip():
        return JsonResult.error('订单ID不能为空', 400)

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return JsonResult.error('订单不存在', 404)

    if order.status not in ['pending', 'paid']:
        return JsonResult.error('只有待支付或已支付的订单才能取消', 400)

    # 更新订单状态
    if order.status == 'paid':
        order.status = 'refunded'  # 已支付的订单取消后变为已退款
    else:
        order.status = 'cancelled'  # 待支付的订单直接取消

    db.session.commit()

    return JsonResult.success(order.to_dict(), '订单取消成功')


@order_bp.route('/<order_id>/complete', methods=['POST'])
def complete_order(order_id):
    """完成订单"""
    if not order_id or not order_id.strip():
        return JsonResult.error('订单ID不能为空', 400)

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return JsonResult.error('订单不存在', 404)

    if order.status != 'paid':
        return JsonResult.error('只有已支付的订单才能完成', 400)

    # 更新订单状态为已完成
    order.status = 'completed'
    db.session.commit()

    return JsonResult.success(order.to_dict(), '订单完成成功')
