"""
课程管理API
提供课程的增删改查功能
"""
from flask import Blueprint
import uuid

from ..models import Course
from pcf_flask_helper.model.base import db
from pcf_flask_helper.common import json_success, json_error
from pcf_flask_helper.form.validate import assert_id_exists
from pcf_flask_helper.model.query import create_query_builder
from psychological.utils.model_helper import update_model_fields
from ..form import CourseQueryForm, CourseCreateForm, CourseUpdateForm
from psychological.utils.decorator import validate_form
from psychological.utils.decorator.permission import role_required, permission_required

course_bp = Blueprint('course', __name__, url_prefix='/course')


@course_bp.route('', methods=['GET'])
@validate_form(CourseQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("course:get_courses")
def get_courses(form):
    """获取课程列表"""
    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(Course) \
        .when(form.title.data, Course.title.like(f'%{form.title.data}%')) \
        .when(form.status.data, Course.status == form.status.data) \
        .order_by(Course.create_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    courses = [course.to_dict() for course in result['items']]

    return json_success({
        'list': courses,
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@course_bp.route('/<course_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("course:get_course")
def get_course(course_id):
    """获取单个课程详情"""
    assert_id_exists(course_id, "课程ID不能为空")
    
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return json_error('课程不存在', 404)

    return json_success(course.to_dict())


@course_bp.route('', methods=['POST'])
@validate_form(CourseCreateForm)
@role_required(['admin', 'manager'])
@permission_required("course:create_course")
def create_course(form):
    """创建课程"""
    # 处理标签数据
    tags_data = []
    if form.tags.data:
        import json
        try:
            if isinstance(form.tags.data, str):
                tags_data = json.loads(form.tags.data) if form.tags.data.strip() else []
            elif isinstance(form.tags.data, list):
                tags_data = form.tags.data
        except (json.JSONDecodeError, TypeError):
            tags_data = []

    # 创建课程
    course = Course(
        id=str(uuid.uuid4()),
        title=form.title.data,
        subtitle=form.subtitle.data or '',
        description=form.description.data or '',
        content=form.content.data or '',
        price=form.price.data or 0.0,
        original_price=form.price.data or 0.0,
        duration=form.duration.data or 60,
        status=form.status.data or 'draft',
        rating=0.0,
        cover_image=form.cover_image.data or '',
        teacher=form.teacher.data or '默认讲师',  # 必填字段默认值
        teacher_title=form.teacher_title.data or '资深讲师',
        teacher_avatar=form.teacher_avatar.data or '',
        lesson_count=0,
        student_count=0,
    )
    
    # 设置标签
    if tags_data:
        course.tags = tags_data

    db.session.add(course)
    db.session.commit()

    return json_success(course.to_dict(), '创建课程成功', 201)


@course_bp.route('/<course_id>', methods=['PUT'])
@validate_form(CourseUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("course:update_course")
def update_course(course_id, form):
    """更新课程"""
    assert_id_exists(course_id, "课程ID不能为空")
    
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return json_error('课程不存在', 404)

    # 处理标签数据（特殊字段需要单独处理）
    if form.tags.data is not None:
        import json
        try:
            if isinstance(form.tags.data, str):
                tags_data = json.loads(form.tags.data) if form.tags.data.strip() else []
            elif isinstance(form.tags.data, list):
                tags_data = form.tags.data
            else:
                tags_data = []
            course.tags = tags_data
        except (json.JSONDecodeError, TypeError):
            course.tags = []

    # 使用统一的更新函数更新其他字段
    update_model_fields(course, form, exclude_fields=['tags'])

    db.session.commit()

    return json_success(course.to_dict(), '更新课程成功')


@course_bp.route('/<course_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("course:delete_course")
def delete_course(course_id):
    """删除课程"""
    assert_id_exists(course_id, "课程ID不能为空")
    
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return json_error('课程不存在', 404)

    db.session.delete(course)
    db.session.commit()

    return json_success(None, '删除课程成功')