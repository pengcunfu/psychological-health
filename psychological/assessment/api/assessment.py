"""
测评管理API
提供心理测评的完整管理功能，包含权限控制
"""
import uuid
from datetime import datetime
from flask import Blueprint, request
from sqlalchemy import or_
from psychological.appointment.models import Assessment, AssessmentQuestion, AssessmentOption, AssessmentRecord, AssessmentAnswer
from pcf_flask_helper.model.base import db
from pcf_flask_helper.common import json_success, json_error
from pcf_flask_helper.form.validate import assert_id_exists
from pcf_flask_helper.model.query import create_query_builder
from psychological.utils.model_helper import update_model_fields
from psychological.utils.auth_helper import is_manager_user, assert_current_user_id
from psychological.appointment.form import (
    AssessmentQueryForm, AssessmentCreateForm, AssessmentUpdateForm,
    AssessmentQuestionCreateForm, AssessmentQuestionUpdateForm,
    AssessmentStartForm, AssessmentSubmitForm, AssessmentRecordQueryForm
)
from psychological.utils.decorator.form import validate_form
from psychological.utils.decorator.permission import role_required, permission_required
import json

assessment_bp = Blueprint('assessment', __name__, url_prefix='/assessment')


@assessment_bp.route('', methods=['GET'])
@validate_form(AssessmentQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("assessment:get_assessments")
def get_assessments(form):
    """获取测评列表"""
    is_manager = is_manager_user()

    # 构建查询
    builder = create_query_builder(Assessment) \
        .unless(is_manager, Assessment.status == 'published') \
        .when(form.name.data, Assessment.name.like(f'%{form.name.data}%')) \
        .when(form.category.data, Assessment.category == form.category.data) \
        .when(form.difficulty.data, Assessment.difficulty == form.difficulty.data) \
        .when(form.is_free.data, Assessment.is_free == form.is_free.data) \
        .when(form.status.data and is_manager, Assessment.status == form.status.data)

    # 关键词搜索
    if form.keyword.data:
        keyword = f'%{form.keyword.data}%'
        builder.filter(
            or_(
                Assessment.name.like(keyword),
                Assessment.subtitle.like(keyword),
                Assessment.description.like(keyword)
            )
        )

    # 动态排序
    valid_sort_fields = {
        'create_time': Assessment.create_time,
        'update_time': Assessment.update_time,
        'name': Assessment.name,
        'rating': Assessment.rating,
        'price': Assessment.price,
        'participant_count': Assessment.participant_count,
        'sort_order': Assessment.sort_order
    }

    sort_by = form.sort_by.data or 'sort_order'
    sort_order = form.sort_order.data or 'asc'

    if sort_by not in valid_sort_fields:
        sort_by = 'sort_order'

    sort_expr = valid_sort_fields[sort_by].desc() if sort_order.lower() == 'desc' else valid_sort_fields[sort_by].asc()

    # 分页查询
    result = builder.order_by(sort_expr).paginate(form.page.data, form.per_page.data, 100)

    assessments_data = [assessment.to_dict() for assessment in result['items']]


    return json_success({
        'list': assessments_data,
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages'],
        'sort_by': sort_by,
        'sort_order': sort_order
    })


@assessment_bp.route('/<assessment_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("assessment:get_assessment_detail")
def get_assessment_detail(assessment_id):
    """获取测评详情"""
    assert_id_exists(assessment_id, "测评ID不能为空")

    # 构建查询
    builder = create_query_builder(Assessment) \
        .filter(Assessment.id == assessment_id) \
        .unless(is_manager_user(), Assessment.status == 'published')

    assessment = builder.first()
    if not assessment:
        return json_error('测评不存在或未发布', 404)

    # 获取题目列表（按顺序）
    questions = create_query_builder(AssessmentQuestion) \
        .filter(AssessmentQuestion.assessment_id == assessment_id) \
        .order_by(AssessmentQuestion.question_order.asc()) \
        .all()

    assessment_data = assessment.to_dict()
    assessment_data['questions'] = [q.to_dict() for q in questions]


    return json_success(assessment_data)


@assessment_bp.route('', methods=['POST'])
@validate_form(AssessmentCreateForm)
@role_required(['admin', 'manager'])
@permission_required("assessment:create_assessment")
def create_assessment(form):
    """创建测评（仅管理员）"""

    # 生成唯一ID
    assessment_id = str(uuid.uuid4())

    # 处理标签
    tags = []
    if form.tags.data:
        tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]

    assessment = Assessment(
        id=assessment_id,
        name=form.name.data,
        subtitle=form.subtitle.data,
        description=form.description.data,
        cover_image=form.cover_image.data,
        price=form.price.data,
        original_price=form.original_price.data,
        duration=form.duration.data,
        difficulty=form.difficulty.data,
        category=form.category.data,
        status=form.status.data,
        instructions=form.instructions.data,
        is_free=form.is_free.data,
        sort_order=form.sort_order.data
    )
    assessment.tags = tags

    try:
        db.session.add(assessment)
        db.session.commit()
        return json_success(assessment.to_dict(), '创建成功')
    except Exception as e:
        db.session.rollback()
        return json_error(f'创建失败: {str(e)}')


@assessment_bp.route('/<assessment_id>', methods=['PUT'])
@validate_form(AssessmentUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("assessment:update_assessment")
def update_assessment(assessment_id, form):
    """更新测评（仅管理员）"""
    assert_id_exists(assessment_id, "测评ID不能为空")
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    if not assessment:
        return json_error('测评不存在', 404)

    # 处理标签（特殊逻辑）
    if form.tags.data is not None:
        tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        assessment.tags = tags

    # 使用update_model_from_form处理其他标准字段
    update_model_fields(assessment, form, exclude_fields=['tags'])

    try:
        db.session.commit()
        return json_success(assessment.to_dict(), '更新成功')
    except Exception as e:
        db.session.rollback()
        return json_error(f'更新失败: {str(e)}')


@assessment_bp.route('/<assessment_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("assessment:delete_assessment")
def delete_assessment(assessment_id):
    """删除测评（仅管理员）"""
    assert_id_exists(assessment_id, "测评ID不能为空")
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    if not assessment:
        return json_error('测评不存在', 404)

    try:
        db.session.delete(assessment)
        db.session.commit()
        return json_success(None, '删除成功')
    except Exception as e:
        db.session.rollback()
        return json_error(f'删除失败: {str(e)}')


@assessment_bp.route('/<assessment_id>/questions', methods=['POST'])
@validate_form(AssessmentQuestionCreateForm)
@role_required(['admin', 'manager'])
@permission_required("assessment:create_question")
def create_question(assessment_id, form):
    """创建测评题目（仅管理员）"""
    assert_id_exists(assessment_id, "测评ID不能为空")
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    if not assessment:
        return json_error('测评不存在', 404)

    # 生成唯一ID
    question_id = str(uuid.uuid4())

    question = AssessmentQuestion(
        id=question_id,
        assessment_id=assessment_id,
        question_text=form.question_text.data,
        question_type=form.question_type.data,
        question_order=form.question_order.data,
        is_required=form.is_required.data,
        score_weight=form.score_weight.data,
        dimension=form.dimension.data,
        description=form.description.data
    )

    try:
        db.session.add(question)

        # 更新测评的题目数量
        assessment.question_count = create_query_builder(AssessmentQuestion) \
                                        .filter(AssessmentQuestion.assessment_id == assessment_id) \
                                        .count() + 1

        db.session.commit()
        return json_success(question.to_dict(), '创建成功')
    except Exception as e:
        db.session.rollback()
        return json_error(f'创建失败: {str(e)}')


@assessment_bp.route('/<assessment_id>/questions/<question_id>', methods=['PUT'])
@validate_form(AssessmentQuestionUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("assessment:update_question")
def update_question(assessment_id, question_id, form):
    """更新测评题目（仅管理员）"""
    assert_id_exists(assessment_id, "测评ID不能为空")
    assert_id_exists(question_id, "题目ID不能为空")
    question = AssessmentQuestion.query.filter_by(
        id=question_id, assessment_id=assessment_id
    ).first()
    if not question:
        return json_error('题目不存在', 404)

    # 使用update_model_from_form简化更新逻辑
    update_model_fields(question, form)

    try:
        db.session.commit()
        return json_success(question.to_dict(), '更新成功')
    except Exception as e:
        db.session.rollback()
        return json_error(f'更新失败: {str(e)}')


@assessment_bp.route('/<assessment_id>/questions/<question_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("assessment:delete_question")
def delete_question(assessment_id, question_id):
    """删除测评题目（仅管理员）"""
    assert_id_exists(assessment_id, "测评ID不能为空")
    assert_id_exists(question_id, "题目ID不能为空")
    question = AssessmentQuestion.query.filter_by(
        id=question_id, assessment_id=assessment_id
    ).first()
    if not question:
        return json_error('题目不存在', 404)

    try:
        db.session.delete(question)

        # 更新测评的题目数量
        assessment = Assessment.query.filter_by(id=assessment_id).first()
        if assessment:
            assessment.question_count = create_query_builder(AssessmentQuestion) \
                                            .filter(AssessmentQuestion.assessment_id == assessment_id) \
                                            .count() - 1

        db.session.commit()
        return json_success(None, '删除成功')
    except Exception as e:
        db.session.rollback()
        return json_error(f'删除失败: {str(e)}')


@assessment_bp.route('/<assessment_id>/questions/<question_id>/options', methods=['GET'])
@role_required(['admin', 'manager'])
@permission_required("assessment:get_question_options")
def get_question_options(assessment_id, question_id):
    """获取题目选项列表（仅管理员）"""
    assert_id_exists(assessment_id, "测评ID不能为空")
    assert_id_exists(question_id, "题目ID不能为空")

    # 检查题目是否存在
    question = AssessmentQuestion.query.filter_by(
        id=question_id, assessment_id=assessment_id
    ).first()
    if not question:
        return json_error('题目不存在', 404)

    # 获取选项列表（按顺序）
    options = create_query_builder(AssessmentOption) \
        .filter(AssessmentOption.question_id == question_id) \
        .order_by(AssessmentOption.option_order.asc()) \
        .all()

    options_data = [option.to_dict() for option in options]
    return json_success(options_data)


@assessment_bp.route('/<assessment_id>/questions/<question_id>/options', methods=['POST'])
@role_required(['admin', 'manager'])
@permission_required("assessment:save_question_options")
def save_question_options(assessment_id, question_id):
    """批量保存题目选项（仅管理员）"""
    assert_id_exists(assessment_id, "测评ID不能为空")
    assert_id_exists(question_id, "题目ID不能为空")

    # 检查题目是否存在
    question = AssessmentQuestion.query.filter_by(
        id=question_id, assessment_id=assessment_id
    ).first()
    if not question:
        return json_error('题目不存在', 404)

    options_data = request.get_json()
    if not options_data or not isinstance(options_data, list):
        return json_error('选项数据格式错误')

    try:
        # 删除现有选项
        create_query_builder(AssessmentOption) \
            .filter(AssessmentOption.question_id == question_id) \
            .delete()

        # 创建新选项
        for i, option_data in enumerate(options_data):
            if not option_data.get('option_text'):
                continue

            option = AssessmentOption(
                id=str(uuid.uuid4()),
                question_id=question_id,
                option_text=option_data['option_text'],
                option_value=option_data.get('option_value', ''),
                score=float(option_data.get('score', 0)),
                option_order=i
            )
            db.session.add(option)

        db.session.commit()
        return json_success(None, '选项保存成功')

    except Exception as e:
        db.session.rollback()
        return json_error(f'保存失败: {str(e)}')


@assessment_bp.route('/<assessment_id>/questions/<question_id>/options/<option_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("assessment:delete_option")
def delete_option(assessment_id, question_id, option_id):
    """删除选项（仅管理员）"""
    assert_id_exists(assessment_id, "测评ID不能为空")
    assert_id_exists(question_id, "题目ID不能为空")
    assert_id_exists(option_id, "选项ID不能为空")

    # 检查题目是否存在
    question = AssessmentQuestion.query.filter_by(
        id=question_id, assessment_id=assessment_id
    ).first()
    if not question:
        return json_error('题目不存在', 404)

    # 检查选项是否存在
    option = AssessmentOption.query.filter_by(
        id=option_id, question_id=question_id
    ).first()
    if not option:
        return json_error('选项不存在', 404)

    try:
        db.session.delete(option)
        db.session.commit()
        return json_success(None, '删除成功')
    except Exception as e:
        db.session.rollback()
        return json_error(f'删除失败: {str(e)}')


@assessment_bp.route('/start', methods=['POST'])
@validate_form(AssessmentStartForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("assessment:start_assessment")
def start_assessment(form):
    """开始测评"""
    user_id = assert_current_user_id()

    # 检查测评是否存在
    assessment = create_query_builder(Assessment) \
        .filter(Assessment.id == form.assessment_id.data, Assessment.status == 'published') \
        .first()
    if not assessment:
        return json_error('测评不存在或未发布', 404)

    # 检查是否已有进行中的记录
    existing_record = create_query_builder(AssessmentRecord) \
        .filter(
        AssessmentRecord.user_id == user_id,
        AssessmentRecord.assessment_id == form.assessment_id.data,
        AssessmentRecord.status == 'in_progress'
    ) \
        .first()

    if existing_record:
        return json_success(existing_record.to_dict(), '继续之前的测评')

    # 创建新的测评记录
    record = AssessmentRecord(
        id=str(uuid.uuid4()),
        user_id=user_id,
        assessment_id=form.assessment_id.data,
        status='in_progress',
        start_time=datetime.utcnow(),
        is_anonymous=form.is_anonymous.data
    )

    try:
        db.session.add(record)
        db.session.commit()
        return json_success(record.to_dict(), '测评开始')
    except Exception as e:
        db.session.rollback()
        return json_error(f'开始测评失败: {str(e)}')


@assessment_bp.route('/submit', methods=['POST'])
@validate_form(AssessmentSubmitForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("assessment:submit_assessment")
def submit_assessment(form):
    """提交测评"""
    user_id = assert_current_user_id()

    # 检查测评记录是否存在
    record = create_query_builder(AssessmentRecord) \
        .filter(
        AssessmentRecord.user_id == user_id,
        AssessmentRecord.assessment_id == form.assessment_id.data,
        AssessmentRecord.status == 'in_progress'
    ) \
        .first()

    if not record:
        return json_error('测评记录不存在或已完成', 404)

    try:
        # 删除之前的答案
        create_query_builder(AssessmentAnswer) \
            .filter(AssessmentAnswer.record_id == record.id) \
            .delete()

        total_score = 0.0
        dimension_scores = {}

        # 保存答案并计算分数
        for answer_data in form.answers.data:
            question = AssessmentQuestion.query.filter_by(
                id=answer_data['question_id'],
                assessment_id=form.assessment_id.data
            ).first()

            if not question:
                continue

            answer = AssessmentAnswer(
                id=str(uuid.uuid4()),
                record_id=record.id,
                question_id=answer_data['question_id'],
                answer_text=answer_data.get('answer_text')
            )

            # 处理选项答案
            if answer_data.get('option_ids'):
                try:
                    option_ids = json.loads(answer_data['option_ids']) if isinstance(answer_data['option_ids'],
                                                                                     str) else answer_data['option_ids']
                    answer.selected_options = option_ids

                    # 计算得分
                    options = AssessmentOption.query.filter(
                        AssessmentOption.id.in_(option_ids)
                    ).all()

                    question_score = sum(option.score for option in options) * question.score_weight
                    answer.score = question_score
                    total_score += question_score

                    # 维度得分统计
                    if question.dimension:
                        if question.dimension not in dimension_scores:
                            dimension_scores[question.dimension] = 0
                        dimension_scores[question.dimension] += question_score

                except (json.JSONDecodeError, TypeError):
                    pass

            db.session.add(answer)

        # 更新测评记录
        record.status = 'completed'
        record.complete_time = datetime.utcnow()
        record.total_score = total_score
        record.dimension_score_dict = dimension_scores

        # 简单的结果评估逻辑（可根据实际需求调整）
        if total_score >= 80:
            record.result_level = 'excellent'
            record.result_description = '心理状态良好'
        elif total_score >= 60:
            record.result_level = 'good'
            record.result_description = '心理状态一般'
        else:
            record.result_level = 'poor'
            record.result_description = '需要关注心理健康'

        # 更新测评参与人数
        assessment = Assessment.query.filter_by(id=form.assessment_id.data).first()
        if assessment:
            assessment.participant_count += 1

        db.session.commit()

        return json_success(record.to_dict(), '测评提交成功')

    except Exception as e:
        db.session.rollback()
        return json_error(f'提交测评失败: {str(e)}')


@assessment_bp.route('/records', methods=['GET'])
@validate_form(AssessmentRecordQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("assessment:get_assessment_records")
def get_assessment_records(form):
    """获取测评记录列表"""
    current_user_id = assert_current_user_id()
    is_manager = is_manager_user()

    # 构建查询
    builder = create_query_builder(AssessmentRecord) \
        .unless(is_manager, AssessmentRecord.user_id == current_user_id) \
        .when(form.user_id.data and is_manager, AssessmentRecord.user_id == form.user_id.data) \
        .when(form.assessment_id.data, AssessmentRecord.assessment_id == form.assessment_id.data) \
        .when(form.status.data, AssessmentRecord.status == form.status.data)

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
    result = builder.paginate(form.page.data, form.per_page.data, 100)

    records_data = []
    for record in result['items']:
        record_dict = record.to_dict()
        # 添加测评基本信息
        if record.assessment:
            record_dict['assessment_info'] = {
                'name': record.assessment.name,
                'cover_image': record.assessment.cover_image,
                'duration': record.assessment.duration
            }
        records_data.append(record_dict)

    return json_success({
        'list': records_data,
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@assessment_bp.route('/records/<record_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("assessment:get_assessment_record_detail")
def get_assessment_record_detail(record_id):
    """获取测评记录详情"""
    assert_id_exists(record_id, "记录ID不能为空")
    current_user_id = assert_current_user_id()

    # 构建查询
    builder = create_query_builder(AssessmentRecord) \
        .filter(AssessmentRecord.id == record_id) \
        .unless(is_manager_user(), AssessmentRecord.user_id == current_user_id)

    record = builder.first()
    if not record:
        return json_error('测评记录不存在或权限不足', 404)

    record_data = record.to_dict()

    # 添加测评信息
    if record.assessment:
        record_data['assessment_info'] = record.assessment.to_dict()

    # 添加答案详情
    answers = create_query_builder(AssessmentAnswer) \
        .filter(AssessmentAnswer.record_id == record_id) \
        .all()
    record_data['answers'] = [answer.to_dict() for answer in answers]

    return json_success(record_data)


@assessment_bp.route('/public', methods=['GET'])
@validate_form(AssessmentQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("assessment:get_public_assessments")
def get_public_assessments(form):
    """获取公开的测评列表（普通用户接口）"""

    # 构建查询
    builder = create_query_builder(Assessment) \
        .filter(Assessment.status == 'published') \
        .when(form.name.data, Assessment.name.like(f'%{form.name.data}%')) \
        .when(form.category.data, Assessment.category == form.category.data) \
        .when(form.difficulty.data, Assessment.difficulty == form.difficulty.data) \
        .when(form.is_free.data is not None, Assessment.is_free == form.is_free.data)

    # 关键词搜索
    if form.keyword.data:
        keyword = f'%{form.keyword.data}%'
        builder.filter(
            or_(
                Assessment.name.like(keyword),
                Assessment.subtitle.like(keyword),
                Assessment.description.like(keyword)
            )
        )

    # 排序逻辑（按推荐度排序）
    valid_sort_fields = {
        'create_time': Assessment.create_time,
        'name': Assessment.name,
        'rating': Assessment.rating,
        'price': Assessment.price,
        'participant_count': Assessment.participant_count,
        'sort_order': Assessment.sort_order
    }

    sort_by = form.sort_by.data or 'sort_order'
    sort_order = form.sort_order.data or 'asc'

    if sort_by not in valid_sort_fields:
        sort_by = 'sort_order'

    sort_expr = valid_sort_fields[sort_by].desc() if sort_order.lower() == 'desc' else valid_sort_fields[sort_by].asc()

    # 分页查询
    result = builder.order_by(sort_expr).paginate(form.page.data, form.per_page.data, 100)

    assessments_data = [assessment.to_dict() for assessment in result['items']]


    return json_success({
        'list': assessments_data,
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages'],
        'sort_by': sort_by,
        'sort_order': sort_order
    })
