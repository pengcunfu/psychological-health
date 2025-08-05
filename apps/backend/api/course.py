"""
课程管理API
提供课程的增删改查功能

接口列表：
- GET /course - 获取课程列表
- GET /course/<course_id> - 获取单个课程详情
- POST /course - 创建课程
- PUT /course/<course_id> - 更新课程
- DELETE /course/<course_id> - 删除课程
- GET /course/category/<category_id> - 获取分类下的课程
- POST /course/<course_id>/cover - 上传课程封面
"""
from unicodedata import category
from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
import uuid

from models.course import Course
from models.base import db
from utils.json_result import JsonResult
from form.course import CourseQueryForm, CourseCreateForm, CourseUpdateForm
from utils.validate import validate_data, validate_args
from utils.model_helper import update_model_from_form
from utils.image import process_course_images

course_bp = Blueprint('course', __name__, url_prefix='/course')


@course_bp.route('', methods=['GET'])
def get_courses():
    """获取课程列表"""
    form = validate_args(CourseQueryForm)

    page = form.page.data
    per_page = form.per_page.data
    title = form.title.data
    status = form.status.data

    # 构建查询
    query = Course.query

    if title:
        query = query.filter(Course.title.like(f'%{title}%'))
    
    if status:
        query = query.filter(Course.status == status)

    # 分页查询
    pagination = query.order_by(Course.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    courses = [course.to_dict() for course in pagination.items]
    # 处理课程数据中的图片URL
    processed_courses = process_course_images(courses)

    return JsonResult.success({
        'list': processed_courses,
        'total': pagination.total,
        'page': page,
        'per_page': per_page
    })


@course_bp.route('/<course_id>', methods=['GET'])
def get_course(course_id):
    """获取单个课程详情"""
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return JsonResult.error('课程不存在', 404)

    # 处理课程数据中的图片URL
    course_data = process_course_images(course.to_dict())
    return JsonResult.success(course_data)


@course_bp.route('', methods=['POST'])
def create_course():
    """创建课程"""
    form = validate_data(CourseCreateForm)

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

    return JsonResult.success(course.to_dict(), '创建课程成功', 201)


@course_bp.route('/<course_id>', methods=['PUT'])
def update_course(course_id):
    """更新课程"""
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return JsonResult.error('课程不存在', 404)

    form = validate_data(CourseUpdateForm)

    # 处理标签数据
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

    # 更新其他字段
    update_model_from_form(course, form, exclude_fields=['tags'])

    db.session.commit()

    return JsonResult.success(course.to_dict(), '更新课程成功')


@course_bp.route('/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    """删除课程"""
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return JsonResult.error('课程不存在', 404)

    db.session.delete(course)
    db.session.commit()

    return JsonResult.success(None, '删除课程成功')
