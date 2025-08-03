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
from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
import uuid

from models.course import Course
from models.base import db
from utils.json_result import JsonResult
from form.course import CourseQueryForm, CourseCreateForm, CourseUpdateForm
from utils.validate import validate_data, validate_args
from utils.model_helper import update_model_from_form

course_bp = Blueprint('course', __name__, url_prefix='/course')


@course_bp.route('', methods=['GET'])
def get_courses():
    """获取课程列表"""
    form = validate_args(CourseQueryForm)

    page = form.page.data
    per_page = form.per_page.data
    title = form.title.data

    # 构建查询
    query = Course.query

    if title:
        query = query.filter(Course.title.like(f'%{title}%'))

    # 分页查询
    pagination = query.order_by(Course.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    courses = [course.to_dict() for course in pagination.items]

    return JsonResult.success({
        'list': courses,
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

    return JsonResult.success(course.to_dict())


@course_bp.route('', methods=['POST'])
def create_course():
    """创建课程"""
    form = validate_data(CourseCreateForm)

    # 创建课程
    course = Course(
        id=str(uuid.uuid4()),
        title=form.title.data,
        description=form.description.data or '',
        price=form.price.data,
        score=form.score.data or 0.0,
        cover_image=form.cover_image.data or '',
        video_url=form.video_url.data or '',
        category_id=form.category_id.data,
        counselor_id=form.counselor_id.data
    )

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

    # 更新字段
    update_model_from_form(course, form)

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
