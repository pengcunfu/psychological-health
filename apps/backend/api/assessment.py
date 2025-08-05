import uuid
from datetime import datetime
from flask import Blueprint, request, g
from sqlalchemy import and_, or_
from models import Assessment, AssessmentQuestion, AssessmentOption, AssessmentRecord, AssessmentAnswer
from models.base import db
from form.assessment import (
    AssessmentQueryForm, AssessmentCreateForm, AssessmentUpdateForm,
    AssessmentQuestionCreateForm, AssessmentQuestionUpdateForm,
    AssessmentStartForm, AssessmentSubmitForm, AssessmentRecordQueryForm
)
from utils.json_result import JsonResult
from utils.validate import validate_args
from middleware.auth import auth_required
import json

assessment_bp = Blueprint('assessment', __name__, url_prefix='/assessment')


@assessment_bp.route('', methods=['GET'])
def get_assessments():
    """获取测评列表"""
    form = validate_args(AssessmentQueryForm)
    query = Assessment.query
    
    # 搜索条件
    if form.name.data:
        query = query.filter(Assessment.name.like(f'%{form.name.data}%'))
    
    if form.category.data:
        query = query.filter(Assessment.category == form.category.data)
    
    if form.difficulty.data:
        query = query.filter(Assessment.difficulty == form.difficulty.data)
    
    if form.is_free.data is not None:
        query = query.filter(Assessment.is_free == form.is_free.data)
    
    if form.status.data:
        query = query.filter(Assessment.status == form.status.data)
    else:
        # 默认只显示已发布的测评
        query = query.filter(Assessment.status == 'published')
    
    if form.keyword.data:
        keyword = f'%{form.keyword.data}%'
        query = query.filter(
            or_(
                Assessment.name.like(keyword),
                Assessment.subtitle.like(keyword),
                Assessment.description.like(keyword)
            )
        )
    
    # 排序逻辑
    sort_by = form.sort_by.data or 'sort_order'
    sort_order = form.sort_order.data or 'asc'
    
    valid_sort_fields = {
        'create_time': Assessment.create_time,
        'update_time': Assessment.update_time,
        'name': Assessment.name,
        'rating': Assessment.rating,
        'price': Assessment.price,
        'participant_count': Assessment.participant_count,
        'sort_order': Assessment.sort_order
    }
    
    if sort_by not in valid_sort_fields:
        sort_by = 'sort_order'
    
    sort_column = valid_sort_fields[sort_by]
    
    if sort_order.lower() == 'desc':
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # 分页
    pagination = query.paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )
    
    assessments_data = [assessment.to_dict() for assessment in pagination.items]
    
    return JsonResult.success({
        'list': assessments_data,
        'total': pagination.total,
        'page': form.page.data,
        'per_page': form.per_page.data,
        'pages': pagination.pages,
        'sort_by': sort_by,
        'sort_order': sort_order
    })


@assessment_bp.route('/<assessment_id>', methods=['GET'])
def get_assessment_detail(assessment_id):
    """获取测评详情"""
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    if not assessment:
        return JsonResult.error('测评不存在', 404)
    
    # 获取题目列表（按顺序）
    questions = AssessmentQuestion.query.filter_by(assessment_id=assessment_id)\
        .order_by(AssessmentQuestion.question_order.asc()).all()
    
    assessment_data = assessment.to_dict()
    assessment_data['questions'] = [q.to_dict() for q in questions]
    
    return JsonResult.success(assessment_data)


@assessment_bp.route('', methods=['POST'])
@auth_required
def create_assessment():
    """创建测评"""
    form = validate_args(AssessmentCreateForm)
    
    # 检查ID是否已存在
    existing = Assessment.query.filter_by(id=form.id.data).first()
    if existing:
        return JsonResult.error('测评ID已存在')
    
    # 处理标签
    tags = []
    if form.tags.data:
        tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
    
    assessment = Assessment(
        id=form.id.data,
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
        return JsonResult.success(assessment.to_dict(), '创建成功')
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'创建失败: {str(e)}')


@assessment_bp.route('/<assessment_id>', methods=['PUT'])
@auth_required
def update_assessment(assessment_id):
    """更新测评"""
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    if not assessment:
        return JsonResult.error('测评不存在', 404)
    
    form = validate_args(AssessmentUpdateForm)
    
    # 更新字段
    if form.name.data:
        assessment.name = form.name.data
    if form.subtitle.data is not None:
        assessment.subtitle = form.subtitle.data
    if form.description.data is not None:
        assessment.description = form.description.data
    if form.cover_image.data is not None:
        assessment.cover_image = form.cover_image.data
    if form.price.data is not None:
        assessment.price = form.price.data
    if form.original_price.data is not None:
        assessment.original_price = form.original_price.data
    if form.duration.data is not None:
        assessment.duration = form.duration.data
    if form.difficulty.data:
        assessment.difficulty = form.difficulty.data
    if form.category.data is not None:
        assessment.category = form.category.data
    if form.status.data:
        assessment.status = form.status.data
    if form.instructions.data is not None:
        assessment.instructions = form.instructions.data
    if form.is_free.data is not None:
        assessment.is_free = form.is_free.data
    if form.sort_order.data is not None:
        assessment.sort_order = form.sort_order.data
    
    # 处理标签
    if form.tags.data is not None:
        tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        assessment.tags = tags
    
    try:
        db.session.commit()
        return JsonResult.success(assessment.to_dict(), '更新成功')
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'更新失败: {str(e)}')


@assessment_bp.route('/<assessment_id>', methods=['DELETE'])
@auth_required
def delete_assessment(assessment_id):
    """删除测评"""
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    if not assessment:
        return JsonResult.error('测评不存在', 404)
    
    try:
        db.session.delete(assessment)
        db.session.commit()
        return JsonResult.success(None, '删除成功')
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'删除失败: {str(e)}')


@assessment_bp.route('/<assessment_id>/questions', methods=['POST'])
@auth_required
def create_question(assessment_id):
    """创建测评题目"""
    assessment = Assessment.query.filter_by(id=assessment_id).first()
    if not assessment:
        return JsonResult.error('测评不存在', 404)
    
    form = validate_args(AssessmentQuestionCreateForm)
    
    # 检查题目ID是否已存在
    existing = AssessmentQuestion.query.filter_by(id=form.id.data).first()
    if existing:
        return JsonResult.error('题目ID已存在')
    
    question = AssessmentQuestion(
        id=form.id.data,
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
        assessment.question_count = AssessmentQuestion.query.filter_by(assessment_id=assessment_id).count() + 1
        
        db.session.commit()
        return JsonResult.success(question.to_dict(), '创建成功')
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'创建失败: {str(e)}')


@assessment_bp.route('/<assessment_id>/questions/<question_id>', methods=['PUT'])
@auth_required
def update_question(assessment_id, question_id):
    """更新测评题目"""
    question = AssessmentQuestion.query.filter_by(
        id=question_id, assessment_id=assessment_id
    ).first()
    if not question:
        return JsonResult.error('题目不存在', 404)
    
    form = validate_args(AssessmentQuestionUpdateForm)
    
    # 更新字段
    if form.question_text.data:
        question.question_text = form.question_text.data
    if form.question_type.data:
        question.question_type = form.question_type.data
    if form.question_order.data is not None:
        question.question_order = form.question_order.data
    if form.is_required.data is not None:
        question.is_required = form.is_required.data
    if form.score_weight.data is not None:
        question.score_weight = form.score_weight.data
    if form.dimension.data is not None:
        question.dimension = form.dimension.data
    if form.description.data is not None:
        question.description = form.description.data
    
    try:
        db.session.commit()
        return JsonResult.success(question.to_dict(), '更新成功')
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'更新失败: {str(e)}')


@assessment_bp.route('/<assessment_id>/questions/<question_id>', methods=['DELETE'])
@auth_required
def delete_question(assessment_id, question_id):
    """删除测评题目"""
    question = AssessmentQuestion.query.filter_by(
        id=question_id, assessment_id=assessment_id
    ).first()
    if not question:
        return JsonResult.error('题目不存在', 404)
    
    try:
        db.session.delete(question)
        
        # 更新测评的题目数量
        assessment = Assessment.query.filter_by(id=assessment_id).first()
        if assessment:
            assessment.question_count = AssessmentQuestion.query.filter_by(assessment_id=assessment_id).count() - 1
        
        db.session.commit()
        return JsonResult.success(None, '删除成功')
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'删除失败: {str(e)}')


@assessment_bp.route('/start', methods=['POST'])
@auth_required
def start_assessment():
    """开始测评"""
    form = validate_args(AssessmentStartForm)
    user_id = g.current_user.id
    
    # 检查测评是否存在
    assessment = Assessment.query.filter_by(id=form.assessment_id.data, status='published').first()
    if not assessment:
        return JsonResult.error('测评不存在或未发布', 404)
    
    # 检查是否已有进行中的记录
    existing_record = AssessmentRecord.query.filter_by(
        user_id=user_id,
        assessment_id=form.assessment_id.data,
        status='in_progress'
    ).first()
    
    if existing_record:
        return JsonResult.success(existing_record.to_dict(), '继续之前的测评')
    
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
        return JsonResult.success(record.to_dict(), '测评开始')
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'开始测评失败: {str(e)}')


@assessment_bp.route('/submit', methods=['POST'])
@auth_required
def submit_assessment():
    """提交测评"""
    form = validate_args(AssessmentSubmitForm)
    user_id = g.current_user.id
    
    # 检查测评记录是否存在
    record = AssessmentRecord.query.filter_by(
        user_id=user_id,
        assessment_id=form.assessment_id.data,
        status='in_progress'
    ).first()
    
    if not record:
        return JsonResult.error('测评记录不存在或已完成', 404)
    
    try:
        # 删除之前的答案
        AssessmentAnswer.query.filter_by(record_id=record.id).delete()
        
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
                    option_ids = json.loads(answer_data['option_ids']) if isinstance(answer_data['option_ids'], str) else answer_data['option_ids']
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
        
        return JsonResult.success(record.to_dict(), '测评提交成功')
        
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'提交测评失败: {str(e)}')


@assessment_bp.route('/records', methods=['GET'])
@auth_required
def get_assessment_records():
    """获取测评记录列表"""
    form = validate_args(AssessmentRecordQueryForm)
    user_id = g.current_user.id
    
    query = AssessmentRecord.query.filter_by(user_id=user_id)
    
    # 搜索条件
    if form.assessment_id.data:
        query = query.filter(AssessmentRecord.assessment_id == form.assessment_id.data)
    
    if form.status.data:
        query = query.filter(AssessmentRecord.status == form.status.data)
    
    if form.start_date.data:
        try:
            start_date = datetime.strptime(form.start_date.data, '%Y-%m-%d')
            query = query.filter(AssessmentRecord.create_time >= start_date)
        except ValueError:
            pass
    
    if form.end_date.data:
        try:
            end_date = datetime.strptime(form.end_date.data, '%Y-%m-%d')
            query = query.filter(AssessmentRecord.create_time <= end_date)
        except ValueError:
            pass
    
    # 排序
    sort_by = form.sort_by.data or 'create_time'
    sort_order = form.sort_order.data or 'desc'
    
    valid_sort_fields = {
        'create_time': AssessmentRecord.create_time,
        'update_time': AssessmentRecord.update_time,
        'start_time': AssessmentRecord.start_time,
        'complete_time': AssessmentRecord.complete_time,
        'total_score': AssessmentRecord.total_score
    }
    
    if sort_by in valid_sort_fields:
        sort_column = valid_sort_fields[sort_by]
        if sort_order.lower() == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    
    # 分页
    pagination = query.paginate(
        page=form.page.data, per_page=form.per_page.data, error_out=False
    )
    
    records_data = []
    for record in pagination.items:
        record_dict = record.to_dict()
        # 添加测评基本信息
        if record.assessment:
            record_dict['assessment_info'] = {
                'name': record.assessment.name,
                'cover_image': record.assessment.cover_image,
                'duration': record.assessment.duration
            }
        records_data.append(record_dict)
    
    return JsonResult.success({
        'list': records_data,
        'total': pagination.total,
        'page': form.page.data,
        'per_page': form.per_page.data,
        'pages': pagination.pages
    })


@assessment_bp.route('/records/<record_id>', methods=['GET'])
@auth_required
def get_assessment_record_detail(record_id):
    """获取测评记录详情"""
    user_id = g.current_user.id
    
    record = AssessmentRecord.query.filter_by(
        id=record_id, user_id=user_id
    ).first()
    
    if not record:
        return JsonResult.error('测评记录不存在', 404)
    
    record_data = record.to_dict()
    
    # 添加测评信息
    if record.assessment:
        record_data['assessment_info'] = record.assessment.to_dict()
    
    # 添加答案详情
    answers = AssessmentAnswer.query.filter_by(record_id=record_id).all()
    record_data['answers'] = [answer.to_dict() for answer in answers]
    
    return JsonResult.success(record_data) 