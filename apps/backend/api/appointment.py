"""
预约管理API
提供咨询预约的增删改查功能，包含权限控制

接口列表：
- GET /appointment - 获取预约列表（管理员可查看全部，普通用户只能查看自己相关的）
- GET /appointment/my - 获取我的预约列表（当前用户作为用户或咨询师的预约）
- GET /appointment/as-user - 获取作为用户的预约列表
- GET /appointment/as-counselor - 获取作为咨询师的预约列表
- GET /appointment/<appointment_id> - 获取单个预约详情（权限控制）
- POST /appointment - 创建预约（普通用户只能为自己创建）
- PUT /appointment/<appointment_id> - 更新预约（权限控制）
- DELETE /appointment/<appointment_id> - 删除预约（仅管理员或预约创建者）
- POST /appointment/<appointment_id>/confirm - 确认预约（仅咨询师或管理员）
- POST /appointment/<appointment_id>/complete - 完成预约（仅咨询师或管理员）
- POST /appointment/<appointment_id>/cancel - 取消预约（用户、咨询师或管理员）

权限说明：
- 管理员（admin/manager角色）：可以执行所有操作，查看所有预约
- 普通用户：只能查看和操作自己相关的预约（作为用户或咨询师）
- 咨询师：可以确认、完成、取消自己的预约，不能查看其他咨询师的预约
- 用户：可以创建、取消自己的预约，不能查看其他用户的预约
"""
from datetime import datetime
from flask import Blueprint, request
from models.appointment import Appointment
from models.base import db
from utils.json_result import JsonResult
from form.appointment import AppointmentCreateForm, AppointmentUpdateForm, AppointmentQueryForm
from utils.validate import validate_data, validate_args, check_id
from utils.auth_helper import is_manager_user, get_user_id

appointment_bp = Blueprint('appointment', __name__, url_prefix='/appointment')


@appointment_bp.route('', methods=['GET'])
def get_appointments():
    """获取预约列表"""
    # 使用表单验证查询参数
    form = validate_args(AppointmentQueryForm)
    
    current_user_id = get_user_id()

    # 构建查询
    query = Appointment.query
    
    # 权限控制：普通用户只能查看自己相关的预约
    if not is_manager_user():
        # 普通用户只能查看自己作为用户或咨询师的预约
        query = query.filter(
            (Appointment.user_id == current_user_id) | 
            (Appointment.counselor_id == current_user_id)
        )

    if form.user_id.data:
        # 普通用户不能查询其他用户的预约
        if not is_manager_user() and form.user_id.data != current_user_id:
            return JsonResult.error('权限不足，只能查看自己的预约', 403)
        query = query.filter(Appointment.user_id == form.user_id.data)
        
    if form.counselor_id.data:
        # 普通用户不能查询其他咨询师的预约
        if not is_manager_user() and form.counselor_id.data != current_user_id:
            return JsonResult.error('权限不足，只能查看自己的预约', 403)
        query = query.filter(Appointment.counselor_id == form.counselor_id.data)
        
    if form.status.data is not None:
        query = query.filter(Appointment.status == form.status.data)

    # 分页查询
    pagination = query.order_by(Appointment.appointment_time.desc()).paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )

    appointments = [appointment.to_dict() for appointment in pagination.items]

    return JsonResult.success({
        'list': appointments,
        'total': pagination.total,
        'page': form.page.data,
        'per_page': form.per_page.data,
        'pages': pagination.pages
    })


@appointment_bp.route('/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """获取单个预约详情"""
    check_id(appointment_id, "预约ID不能为空")
    current_user_id = get_user_id()
    
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)
    
    # 权限控制：普通用户只能查看自己相关的预约
    if not is_manager_user():
        if appointment.user_id != current_user_id and appointment.counselor_id != current_user_id:
            return JsonResult.error('权限不足，只能查看自己的预约', 403)

    return JsonResult.success(appointment.to_dict())


@appointment_bp.route('', methods=['POST'])
def create_appointment():
    """创建预约"""
    form = validate_data(AppointmentCreateForm)
    current_user_id = get_user_id()
    
    # 权限控制：普通用户只能为自己创建预约
    if not is_manager_user():
        if form.user_id.data != current_user_id:
            return JsonResult.error('权限不足，只能为自己创建预约', 403)

    # 获取验证后的预约时间
    appointment_time = form.appointment_time.data

    # 检查同一时间段是否已有预约
    existing_appointment = Appointment.query.filter(
        Appointment.counselor_id == form.counselor_id.data,
        Appointment.appointment_time == appointment_time,
        Appointment.status.in_([0, 1])  # 待确认或已确认
    ).first()

    if existing_appointment:
        return JsonResult.error('该时间段已有预约', 400)

    # 创建预约
    appointment = Appointment(
        user_id=form.user_id.data,
        counselor_id=form.counselor_id.data,
        appointment_time=appointment_time,
        status=form.status.data or 0  # 默认为待确认
    )

    db.session.add(appointment)
    db.session.commit()

    return JsonResult.success(appointment.to_dict(), '预约创建成功', 201)


@appointment_bp.route('/<appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """更新预约"""
    check_id(appointment_id, "预约ID不能为空")
    current_user_id = get_user_id()
    
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)
    
    # 权限控制：普通用户只能更新自己相关的预约
    if not is_manager_user():
        if appointment.user_id != current_user_id and appointment.counselor_id != current_user_id:
            return JsonResult.error('权限不足，只能更新自己的预约', 403)

    form = validate_data(AppointmentUpdateForm)

    # 更新预约时间
    if form.appointment_time.data:
        new_time = form.appointment_time.data

        # 检查新时间是否与其他预约冲突
        existing_appointment = Appointment.query.filter(
            Appointment.counselor_id == appointment.counselor_id,
            Appointment.appointment_time == new_time,
            Appointment.status.in_([0, 1]),
            Appointment.id != appointment_id
        ).first()

        if existing_appointment:
            return JsonResult.error('该时间段已有预约', 400)

        appointment.appointment_time = new_time

    # 更新状态
    if form.status.data is not None:
        new_status = form.status.data

        try:
            if new_status == 1:  # 确认
                appointment.confirm()
            elif new_status == 2:  # 完成
                appointment.complete()
            elif new_status == 3:  # 取消
                appointment.cancel()
            else:
                appointment.status = new_status
        except ValueError as e:
            return JsonResult.error(str(e), 400)

    db.session.commit()

    return JsonResult.success(appointment.to_dict(), '预约更新成功')


@appointment_bp.route('/<appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """删除预约（仅管理员或预约创建者）"""
    check_id(appointment_id, "预约ID不能为空")
    current_user_id = get_user_id()
    
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)
    
    # 权限控制：只有管理员或预约的用户可以删除预约
    if not is_manager_user():
        if appointment.user_id != current_user_id:
            return JsonResult.error('权限不足，只能删除自己创建的预约', 403)

    db.session.delete(appointment)
    db.session.commit()

    return JsonResult.success(None, '预约删除成功')


@appointment_bp.route('/<appointment_id>/confirm', methods=['POST'])
def confirm_appointment(appointment_id):
    """确认预约（仅咨询师或管理员）"""
    check_id(appointment_id, "预约ID不能为空")
    current_user_id = get_user_id()
    
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)
    
    # 权限控制：只有咨询师或管理员可以确认预约
    if not is_manager_user():
        if appointment.counselor_id != current_user_id:
            return JsonResult.error('权限不足，只有咨询师可以确认预约', 403)

    try:
        appointment.confirm()
        appointment.update_time = datetime.utcnow()
        db.session.commit()
        return JsonResult.success(appointment.to_dict(), '预约确认成功')
    except ValueError as e:
        return JsonResult.error(str(e), 400)


@appointment_bp.route('/<appointment_id>/complete', methods=['POST'])
def complete_appointment(appointment_id):
    """完成预约（仅咨询师或管理员）"""
    check_id(appointment_id, "预约ID不能为空")
    current_user_id = get_user_id()
    
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)
    
    # 权限控制：只有咨询师或管理员可以完成预约
    if not is_manager_user():
        if appointment.counselor_id != current_user_id:
            return JsonResult.error('权限不足，只有咨询师可以完成预约', 403)

    try:
        appointment.complete()
        appointment.update_time = datetime.utcnow()
        db.session.commit()
        return JsonResult.success(appointment.to_dict(), '预约完成成功')
    except ValueError as e:
        return JsonResult.error(str(e), 400)


@appointment_bp.route('/<appointment_id>/cancel', methods=['POST'])
def cancel_appointment(appointment_id):
    """取消预约（用户、咨询师或管理员）"""
    check_id(appointment_id, "预约ID不能为空")
    current_user_id = get_user_id()
    
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)
    
    # 权限控制：用户、咨询师或管理员都可以取消预约
    if not is_manager_user():
        if appointment.user_id != current_user_id and appointment.counselor_id != current_user_id:
            return JsonResult.error('权限不足，只能取消自己的预约', 403)

    try:
        appointment.cancel()
        appointment.update_time = datetime.utcnow()
        db.session.commit()
        return JsonResult.success(appointment.to_dict(), '预约取消成功')
    except ValueError as e:
        return JsonResult.error(str(e), 400)


@appointment_bp.route('/my', methods=['GET'])
def get_my_appointments():
    """获取我的预约列表（当前用户作为用户或咨询师的预约）"""
    form = validate_args(AppointmentQueryForm)
    current_user_id = get_user_id()
    
    # 构建查询 - 当前用户作为用户或咨询师的预约
    query = Appointment.query.filter(
        (Appointment.user_id == current_user_id) | 
        (Appointment.counselor_id == current_user_id)
    )
    
    if form.status.data is not None:
        query = query.filter(Appointment.status == form.status.data)
    
    # 分页查询
    pagination = query.order_by(Appointment.appointment_time.desc()).paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )
    
    appointments = [appointment.to_dict() for appointment in pagination.items]
    
    return JsonResult.success({
        'list': appointments,
        'total': pagination.total,
        'page': form.page.data,
        'per_page': form.per_page.data,
        'pages': pagination.pages
    })


@appointment_bp.route('/as-user', methods=['GET'])
def get_user_appointments():
    """获取作为用户的预约列表"""
    form = validate_args(AppointmentQueryForm)
    current_user_id = get_user_id()
    
    # 构建查询 - 当前用户作为用户的预约
    query = Appointment.query.filter(Appointment.user_id == current_user_id)
    
    if form.status.data is not None:
        query = query.filter(Appointment.status == form.status.data)
    if form.counselor_id.data:
        query = query.filter(Appointment.counselor_id == form.counselor_id.data)
    
    # 分页查询
    pagination = query.order_by(Appointment.appointment_time.desc()).paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )
    
    appointments = [appointment.to_dict() for appointment in pagination.items]
    
    return JsonResult.success({
        'list': appointments,
        'total': pagination.total,
        'page': form.page.data,
        'per_page': form.per_page.data,
        'pages': pagination.pages
    })


@appointment_bp.route('/as-counselor', methods=['GET'])
def get_counselor_appointments():
    """获取作为咨询师的预约列表"""
    form = validate_args(AppointmentQueryForm)
    current_user_id = get_user_id()
    
    # 构建查询 - 当前用户作为咨询师的预约
    query = Appointment.query.filter(Appointment.counselor_id == current_user_id)
    
    if form.status.data is not None:
        query = query.filter(Appointment.status == form.status.data)
    if form.user_id.data:
        query = query.filter(Appointment.user_id == form.user_id.data)
    
    # 分页查询
    pagination = query.order_by(Appointment.appointment_time.desc()).paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )
    
    appointments = [appointment.to_dict() for appointment in pagination.items]
    
    return JsonResult.success({
        'list': appointments,
        'total': pagination.total,
        'page': form.page.data,
        'per_page': form.per_page.data,
        'pages': pagination.pages
    })
