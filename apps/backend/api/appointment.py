"""
预约管理API
提供咨询预约的增删改查功能

接口列表：
- GET /appointment - 获取预约列表
- GET /appointment/<appointment_id> - 获取单个预约详情
- POST /appointment - 创建预约
- PUT /appointment/<appointment_id> - 更新预约
- DELETE /appointment/<appointment_id> - 删除预约
- PUT /appointment/<appointment_id>/status - 更新预约状态
- GET /appointment/user/<user_id> - 获取用户的预约列表
- GET /appointment/counselor/<counselor_id> - 获取咨询师的预约列表
"""
from datetime import datetime
from flask import Blueprint, request
from models.appointment import Appointment
from models.base import db
from utils.json_result import JsonResult
from form.appointment import AppointmentCreateForm, AppointmentUpdateForm, AppointmentQueryForm
from utils.validate import validate_data, validate_args

appointment_bp = Blueprint('appointment', __name__, url_prefix='/appointment')


@appointment_bp.route('', methods=['GET'])
def get_appointments():
    """获取预约列表"""
    # 使用表单验证查询参数
    form = validate_args(AppointmentQueryForm)

    # 构建查询
    query = Appointment.query

    if form.user_id.data:
        query = query.filter(Appointment.user_id == form.user_id.data)
    if form.counselor_id.data:
        query = query.filter(Appointment.counselor_id == form.counselor_id.data)
    if form.status.data is not None:
        query = query.filter(Appointment.status == form.status.data)

    # 分页查询
    pagination = query.order_by(Appointment.appointment_time.desc()).paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )

    appointments = [appointment.to_dict() for appointment in pagination.items]

    return JsonResult.success({
        'appointments': appointments,
        'total': pagination.total,
        'page': form.page.data,
        'per_page': form.per_page.data,
        'pages': pagination.pages
    })


@appointment_bp.route('/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """获取单个预约详情"""
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)

    return JsonResult.success(appointment.to_dict())


@appointment_bp.route('', methods=['POST'])
def create_appointment():
    """创建预约"""
    form = validate_data(AppointmentCreateForm)

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
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)

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
    """删除预约"""
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)

    db.session.delete(appointment)
    db.session.commit()

    return JsonResult.success(None, '预约删除成功')


@appointment_bp.route('/<appointment_id>/confirm', methods=['POST'])
def confirm_appointment(appointment_id):
    """确认预约"""
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)

    appointment.confirm()
    appointment.update_time = datetime.utcnow()
    db.session.commit()

    return JsonResult.success(appointment.to_dict(), '预约确认成功')


@appointment_bp.route('/<appointment_id>/complete', methods=['POST'])
def complete_appointment(appointment_id):
    """完成预约"""
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)

    appointment.complete()
    appointment.update_time = datetime.utcnow()
    db.session.commit()

    return JsonResult.success(appointment.to_dict(), '预约完成成功')


@appointment_bp.route('/<appointment_id>/cancel', methods=['POST'])
def cancel_appointment(appointment_id):
    """取消预约"""
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return JsonResult.error('预约不存在', 404)

    appointment.cancel()
    appointment.update_time = datetime.utcnow()
    db.session.commit()

    return JsonResult.success(appointment.to_dict(), '预约取消成功')
