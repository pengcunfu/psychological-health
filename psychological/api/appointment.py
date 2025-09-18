"""
预约管理API
提供咨询预约的增删改查功能，包含权限控制
"""
from datetime import datetime
from flask import Blueprint
from psychological.models.appointment import Appointment
from psychological.models.base import db
from psychological.utils.json_result import JsonResult
from psychological.form.appointment import AppointmentCreateForm, AppointmentUpdateForm, AppointmentQueryForm
from psychological.utils.validate import assert_id_exists
from psychological.utils.auth_helper import is_manager_user, assert_current_user_id
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required
from psychological.utils.query import create_query_builder, assert_exists, assert_not_exists

appointment_bp = Blueprint('appointment', __name__, url_prefix='/appointment')


@appointment_bp.route('', methods=['GET'])
@validate_form(AppointmentQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("appointment:get_appointments")
def get_appointments(form):
    """获取预约列表"""

    current_user_id = assert_current_user_id()
    is_manager = is_manager_user()

    # 权限检查：普通用户不能查询其他用户的预约
    if not is_manager:
        if form.user_id.data and form.user_id.data != current_user_id:
            return JsonResult.error('权限不足，只能查看自己的预约', 403)
        if form.counselor_id.data and form.counselor_id.data != current_user_id:
            return JsonResult.error('权限不足，只能查看自己的预约', 403)

    # 一行搞定所有条件和分页！
    result = create_query_builder(Appointment) \
        .unless(is_manager,
                (Appointment.user_id == current_user_id) | (
                        Appointment.counselor_id == current_user_id)
                ) \
        .when(form.user_id.data, Appointment.user_id == form.user_id.data) \
        .when(form.counselor_id.data, Appointment.counselor_id == form.counselor_id.data) \
        .when(form.status.data is not None, Appointment.status == form.status.data) \
        .order_by(Appointment.appointment_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return JsonResult.success({
        'list': [appointment.to_dict() for appointment in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@appointment_bp.route('/<appointment_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("appointment:get_appointment")
def get_appointment(appointment_id):
    """获取单个预约详情"""
    assert_id_exists(appointment_id, "预约ID不能为空")
    current_user_id = assert_current_user_id()

    appointment = assert_exists(Appointment, Appointment.id == appointment_id, "预约不存在")

    # 权限控制：普通用户只能查看自己相关的预约
    if not is_manager_user():
        if appointment.user_id != current_user_id and appointment.counselor_id != current_user_id:
            raise ValueError("权限不足，只能查看自己的预约")

    return JsonResult.success(appointment.to_dict())


@appointment_bp.route('', methods=['POST'])
@validate_form(AppointmentCreateForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("appointment:create_appointment")
def create_appointment(form):
    """创建预约"""
    current_user_id = assert_current_user_id()

    # 权限控制：普通用户只能为自己创建预约
    if not is_manager_user():
        if form.user_id.data != current_user_id:
            return JsonResult.error('权限不足，只能为自己创建预约', 403)

    # 获取验证后的预约时间
    appointment_time = form.appointment_time.data

    # 检查同一时间段是否已有预约
    assert_not_exists(
        Appointment,
        [Appointment.counselor_id == form.counselor_id.data,
         Appointment.appointment_time == appointment_time,
         Appointment.status.in_([0, 1])],  # 待确认或已确认
        "该时间段已有预约"
    )

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
@validate_form(AppointmentUpdateForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("appointment:update_appointment")
def update_appointment(appointment_id, form):
    """更新预约"""
    assert_id_exists(appointment_id, "预约ID不能为空")
    current_user_id = assert_current_user_id()

    appointment = assert_exists(Appointment, Appointment.id == appointment_id, "预约不存在")

    # 权限控制：普通用户只能更新自己相关的预约
    if not is_manager_user():
        if appointment.user_id != current_user_id and appointment.counselor_id != current_user_id:
            raise ValueError("权限不足，只能更新自己的预约")

    # 更新预约时间
    if form.appointment_time.data:
        new_time = form.appointment_time.data

        # 检查新时间是否与其他预约冲突
        assert_not_exists(
            Appointment,
            [Appointment.counselor_id == appointment.counselor_id,
             Appointment.appointment_time == new_time,
             Appointment.status.in_([0, 1]),
             Appointment.id != appointment_id],
            "该时间段已有预约"
        )

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
@role_required(['admin', 'manager', 'user'])
@permission_required("appointment:delete_appointment")
def delete_appointment(appointment_id):
    """删除预约（仅管理员或预约创建者）"""
    assert_id_exists(appointment_id, "预约ID不能为空")
    current_user_id = assert_current_user_id()

    appointment = assert_exists(Appointment, Appointment.id == appointment_id, "预约不存在")

    # 权限控制：只有管理员或预约的用户可以删除预约
    if not is_manager_user():
        if appointment.user_id != current_user_id:
            raise ValueError("权限不足，只能删除自己创建的预约")

    db.session.delete(appointment)
    db.session.commit()

    return JsonResult.success(None, '预约删除成功')


@appointment_bp.route('/<appointment_id>/confirm', methods=['POST'])
@role_required(['admin', 'manager', 'counselor'])
@permission_required("appointment:confirm_appointment")
def confirm_appointment(appointment_id):
    """确认预约（仅咨询师或管理员）"""
    assert_id_exists(appointment_id, "预约ID不能为空")
    current_user_id = assert_current_user_id()

    appointment = assert_exists(Appointment, Appointment.id == appointment_id, "预约不存在")

    # 权限控制：只有咨询师或管理员可以确认预约
    if not is_manager_user():
        if appointment.counselor_id != current_user_id:
            raise ValueError("权限不足，只有咨询师可以确认预约")

    try:
        appointment.confirm()
        appointment.update_time = datetime.utcnow()
        db.session.commit()
        return JsonResult.success(appointment.to_dict(), '预约确认成功')
    except ValueError as e:
        return JsonResult.error(str(e), 400)


@appointment_bp.route('/<appointment_id>/complete', methods=['POST'])
@role_required(['admin', 'manager', 'counselor'])
@permission_required("appointment:complete_appointment")
def complete_appointment(appointment_id):
    """完成预约（仅咨询师或管理员）"""
    assert_id_exists(appointment_id, "预约ID不能为空")
    current_user_id = assert_current_user_id()

    appointment = assert_exists(Appointment, Appointment.id == appointment_id, "预约不存在")

    # 权限控制：只有咨询师或管理员可以完成预约
    if not is_manager_user():
        if appointment.counselor_id != current_user_id:
            raise ValueError("权限不足，只有咨询师可以完成预约")

    try:
        appointment.complete()
        appointment.update_time = datetime.utcnow()
        db.session.commit()
        return JsonResult.success(appointment.to_dict(), '预约完成成功')
    except ValueError as e:
        return JsonResult.error(str(e), 400)


@appointment_bp.route('/<appointment_id>/cancel', methods=['POST'])
@role_required(['admin', 'manager', 'user', 'counselor'])
@permission_required("appointment:cancel_appointment")
def cancel_appointment(appointment_id):
    """取消预约（用户、咨询师或管理员）"""
    assert_id_exists(appointment_id, "预约ID不能为空")
    current_user_id = assert_current_user_id()

    appointment = assert_exists(Appointment, Appointment.id == appointment_id, "预约不存在")

    # 权限控制：用户、咨询师或管理员都可以取消预约
    if not is_manager_user():
        if appointment.user_id != current_user_id and appointment.counselor_id != current_user_id:
            raise ValueError("权限不足，只能取消自己的预约")

    try:
        appointment.cancel()
        appointment.update_time = datetime.utcnow()
        db.session.commit()
        return JsonResult.success(appointment.to_dict(), '预约取消成功')
    except ValueError as e:
        return JsonResult.error(str(e), 400)


@appointment_bp.route('/my', methods=['GET'])
@validate_form(AppointmentQueryForm)
@role_required(['admin', 'manager', 'user', 'counselor'])
@permission_required("appointment:get_my_appointments")
def get_my_appointments(form):
    """获取我的预约列表（当前用户作为用户或咨询师的预约）"""

    current_user_id = assert_current_user_id()

    result = create_query_builder(Appointment) \
        .filter((Appointment.user_id == current_user_id) | (Appointment.counselor_id == current_user_id)) \
        .when(form.status.data, Appointment.status == form.status.data) \
        .order_by(Appointment.appointment_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return JsonResult.success({
        'list': [appointment.to_dict() for appointment in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@appointment_bp.route('/as-user', methods=['GET'])
@validate_form(AppointmentQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("appointment:get_user_appointments")
def get_user_appointments(form):
    """获取作为用户的预约列表"""

    current_user_id = assert_current_user_id()

    result = create_query_builder(Appointment) \
        .filter(Appointment.user_id == current_user_id) \
        .when(form.status.data, Appointment.status == form.status.data) \
        .when(form.counselor_id.data, Appointment.counselor_id == form.counselor_id.data) \
        .order_by(Appointment.appointment_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return JsonResult.success({
        'list': [appointment.to_dict() for appointment in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@appointment_bp.route('/as-counselor', methods=['GET'])
@validate_form(AppointmentQueryForm)
@role_required(['admin', 'manager', 'counselor'])
@permission_required("appointment:get_counselor_appointments")
def get_counselor_appointments(form):
    """获取作为咨询师的预约列表"""

    current_user_id = assert_current_user_id()

    result = create_query_builder(Appointment) \
        .filter(Appointment.counselor_id == current_user_id) \
        .when(form.status.data, Appointment.status == form.status.data) \
        .when(form.user_id.data, Appointment.user_id == form.user_id.data) \
        .order_by(Appointment.appointment_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return JsonResult.success({
        'list': [appointment.to_dict() for appointment in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })
