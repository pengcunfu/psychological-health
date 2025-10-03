"""
测评记录
"""
import uuid
from datetime import datetime, timedelta
from flask import Blueprint
from sqlalchemy import func
from psychological.appointment.models import AssessmentRecord, Assessment, AssessmentAnswer
from psychological.system.models import User
from pcf_flask_helper.model.base import db
from psychological.appointment.form import AssessmentRecordQueryForm, AssessmentRecordCreateForm, AssessmentRecordUpdateForm
from pcf_flask_helper.common import json_success, json_error
from psychological.utils.auth_helper import is_manager_user, assert_current_user_id
from psychological.utils.decorator.form import validate_form
from psychological.utils.decorator.permission import role_required, permission_required
from pcf_flask_helper.model.query import create_query_builder

assessment_record_bp = Blueprint(
    'assessment_record', __name__, url_prefix='/assessment-record')


@assessment_record_bp.route('', methods=['GET'])
@validate_form(AssessmentRecordQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("assessment_record:get_assessment_records")
def get_assessment_records(form):
    """获取测评记录列表（管理员可查看所有，普通用户只能查看自己的）"""
    is_manager = is_manager_user()
    current_user_id = assert_current_user_id()

    if not current_user_id:
        return json_error('用户未登录', 401)

    # 构建查询
    builder = create_query_builder(AssessmentRecord) \
        .unless(is_manager, AssessmentRecord.user_id == current_user_id) \
        .when(form.user_id.data and is_manager, AssessmentRecord.user_id == form.user_id.data) \
        .when(form.assessment_id.data, AssessmentRecord.assessment_id == form.assessment_id.data) \
        .when(form.status.data, AssessmentRecord.status == form.status.data) \
        .when(form.result_level.data, AssessmentRecord.result_level.like(f'%{form.result_level.data}%'))

    # 日期范围过滤
    if form.start_date.data:
        try:
            start_date = datetime.strptime(form.start_date.data, '%Y-%m-%d')
            builder.filter(AssessmentRecord.create_time >= start_date)
        except ValueError:
            pass

    if form.end_date.data:
        try:
            end_date = datetime.strptime(form.end_date.data, '%Y-%m-%d')
            builder.filter(AssessmentRecord.create_time <= end_date)
        except ValueError:
            pass

    # 测评名称搜索
    if form.assessment_name.data:
        assessment_ids = db.session.query(Assessment.id).filter(
            Assessment.name.like(f'%{form.assessment_name.data}%')
        ).subquery()
        builder.filter(AssessmentRecord.assessment_id.in_(assessment_ids))

    # 动态排序
    valid_sort_fields = {
        'create_time': AssessmentRecord.create_time,
        'update_time': AssessmentRecord.update_time,
        'start_time': AssessmentRecord.start_time,
        'complete_time': AssessmentRecord.complete_time,
        'total_score': AssessmentRecord.total_score
    }

    sort_by = form.sort_by.data or 'create_time'
    sort_order = form.sort_order.data or 'desc'

    if sort_by in valid_sort_fields:
        sort_expr = valid_sort_fields[sort_by].desc() if sort_order.lower() == 'desc' else valid_sort_fields[
            sort_by].asc()
        builder.order_by(sort_expr)

    # 分页查询
    result = builder.paginate(form.page.data or 1, form.per_page.data or 10, 100)

    records = []
    for record in result['items']:
        record_data = record.to_dict()

        # 添加测评信息
        if record.assessment:
            record_data['assessment_info'] = {
                'id': record.assessment.id,
                'name': record.assessment.name,
                'category': record.assessment.category,
                'difficulty': record.assessment.difficulty
            }

        # 添加用户信息（仅管理员可见）
        if is_manager:
            user = User.query.filter_by(id=record.user_id).first()
            if user:
                record_data['user_info'] = {
                    'id': user.id,
                    'username': user.username,
                    'phone': user.phone,
                    'email': user.email
                }

        records.append(record_data)

    return json_success({
        'list': records,
        'page': result['page'],
        'per_page': result['per_page'],
        'total': result['total'],
        'pages': result['pages'],
        'has_manage_permission': is_manager
    })


@assessment_record_bp.route('/<record_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("assessment_record:get_assessment_record_detail")
def get_assessment_record_detail(record_id):
    """获取测评记录详情"""
    is_manager = is_manager_user()
    current_user_id = assert_current_user_id()

    if not current_user_id:
        return json_error('用户未登录', 401)

    query = AssessmentRecord.query.filter_by(id=record_id)

    # 如果不是管理员，只能查看自己的记录
    if not is_manager:
        query = query.filter(AssessmentRecord.user_id == current_user_id)

    record = query.first()

    if not record:
        return json_error('测评记录不存在', 404)

    record_data = record.to_dict()

    # 添加测评信息
    if record.assessment:
        record_data['assessment_info'] = record.assessment.to_dict()

    # 添加用户信息（仅管理员可见）
    if is_manager:
        user = User.query.filter_by(id=record.user_id).first()
        if user:
            record_data['user_info'] = {
                'id': user.id,
                'username': user.username,
                'phone': user.phone,
                'email': user.email
            }

    # 添加答案详情
    answers = AssessmentAnswer.query.filter_by(record_id=record_id).all()
    record_data['answers'] = [answer.to_dict() for answer in answers]

    return json_success(record_data)


@assessment_record_bp.route('', methods=['POST'])
@validate_form(AssessmentRecordCreateForm)
@role_required(['admin', 'manager'])
@permission_required("assessment_record:create_assessment_record")
def create_assessment_record(form):
    """创建测评记录（仅管理员）"""

    # 验证用户和测评是否存在
    user = User.query.filter_by(id=form.user_id.data).first()
    if not user:
        return json_error('用户不存在')

    assessment = Assessment.query.filter_by(id=form.assessment_id.data).first()
    if not assessment:
        return json_error('测评不存在')

    # 创建测评记录
    record = AssessmentRecord(
        id=str(uuid.uuid4()),
        user_id=form.user_id.data,
        assessment_id=form.assessment_id.data,
        status=form.status.data or 'in_progress',
        start_time=datetime.now(),
        total_score=form.total_score.data or 0,
        max_score=form.max_score.data or 0,
        result_level=form.result_level.data,
        result_description=form.result_description.data,
        result_suggestion=form.result_suggestion.data,
        is_anonymous=form.is_anonymous.data or False
    )

    if form.status.data == 'completed' and not record.complete_time:
        record.complete_time = datetime.now()

    db.session.add(record)
    db.session.commit()

    return json_success(record.to_dict(), message='测评记录创建成功')


@assessment_record_bp.route('/<record_id>', methods=['PUT'])
@validate_form(AssessmentRecordUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("assessment_record:update_assessment_record")
def update_assessment_record(record_id, form):
    """更新测评记录（仅管理员）"""

    record = AssessmentRecord.query.filter_by(id=record_id).first()
    if not record:
        return json_error('测评记录不存在', 404)

    # 更新字段
    if form.status.data:
        record.status = form.status.data
        if form.status.data == 'completed' and not record.complete_time:
            record.complete_time = datetime.now()

    if form.total_score.data is not None:
        record.total_score = form.total_score.data

    if form.max_score.data is not None:
        record.max_score = form.max_score.data

    if form.result_level.data:
        record.result_level = form.result_level.data

    if form.result_description.data:
        record.result_description = form.result_description.data

    if form.result_suggestion.data:
        record.result_suggestion = form.result_suggestion.data

    if form.is_anonymous.data is not None:
        record.is_anonymous = form.is_anonymous.data

    db.session.commit()

    return json_success(record.to_dict(), message='测评记录更新成功')


@assessment_record_bp.route('/<record_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("assessment_record:delete_assessment_record")
def delete_assessment_record(record_id):
    """删除测评记录（仅管理员）"""
    record = AssessmentRecord.query.filter_by(id=record_id).first()
    if not record:
        return json_error('测评记录不存在', 404)

    # 删除相关的答案记录
    AssessmentAnswer.query.filter_by(record_id=record_id).delete()

    # 删除测评记录
    db.session.delete(record)
    db.session.commit()

    return json_success(message='测评记录删除成功')


@assessment_record_bp.route('/my', methods=['GET'])
@validate_form(AssessmentRecordQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("assessment_record:get_my_assessment_records")
def get_my_assessment_records(form):
    """获取我的测评记录"""
    current_user_id = assert_current_user_id()

    if not current_user_id:
        return json_error('用户未登录', 401)

    result = create_query_builder(AssessmentRecord) \
        .filter(AssessmentRecord.user_id == current_user_id) \
        .when(form.assessment_id.data, AssessmentRecord.assessment_id == form.assessment_id.data) \
        .when(form.status.data, AssessmentRecord.status == form.status.data) \
        .order_by(AssessmentRecord.create_time.desc()) \
        .paginate(form.page.data or 1, form.per_page.data or 10, 100)

    records = []
    for record in result['items']:
        record_data = record.to_dict()

        # 添加测评信息
        if record.assessment:
            record_data['assessment_info'] = {
                'id': record.assessment.id,
                'name': record.assessment.name,
                'category': record.assessment.category,
                'difficulty': record.assessment.difficulty
            }

        records.append(record_data)

    return json_success({
        'list': records,
        'page': result['page'],
        'per_page': result['per_page'],
        'total': result['total'],
        'pages': result['pages']
    })


@assessment_record_bp.route('/stats', methods=['GET'])
@role_required(['admin', 'manager'])
@permission_required("assessment_record:get_assessment_record_stats")
def get_assessment_record_stats():
    """获取测评记录统计信息（仅管理员）"""
    # 总记录数
    total_records = AssessmentRecord.query.count()

    # 各状态记录数
    completed_records = AssessmentRecord.query.filter_by(
        status='completed').count()
    in_progress_records = AssessmentRecord.query.filter_by(
        status='in_progress').count()
    expired_records = AssessmentRecord.query.filter_by(
        status='expired').count()

    # 平均分（只计算已完成的记录）
    avg_score_result = db.session.query(func.avg(AssessmentRecord.total_score)).filter(
        AssessmentRecord.status == 'completed',
        AssessmentRecord.total_score > 0
    ).scalar()
    average_score = round(avg_score_result, 1) if avg_score_result else 0

    # 最近7天新增记录
    week_ago = datetime.now() - timedelta(days=7)
    recent_records = AssessmentRecord.query.filter(
        AssessmentRecord.create_time >= week_ago
    ).count()

    return json_success({
        'total_records': total_records,
        'completed_records': completed_records,
        'in_progress_records': in_progress_records,
        'expired_records': expired_records,
        'average_score': average_score,
        'recent_records': recent_records
    })


@assessment_record_bp.route('/export', methods=['GET'])
@role_required(['admin', 'manager'])
@permission_required("assessment_record:export_assessment_records")
def export_assessment_records():
    """导出测评记录（仅管理员）"""
    # 这里可以实现Excel导出功能
    return json_error('导出功能待实现')
