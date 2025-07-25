from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
import uuid

from models.course import Course
from models.base import db
from utils.json_result import JsonResult
from form.course import CourseQueryForm, CourseCreateForm, CourseUpdateForm

course_bp = Blueprint('course', __name__, url_prefix='/courses')


@course_bp.route('', methods=['GET'])
def get_courses():
    """获取课程列表"""
    form = CourseQueryForm(request.args)
    if not form.validate():
        return JsonResult.error('参数验证失败', form.errors)

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

    return JsonResult.success('获取课程列表成功', {
        'courses': courses,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@course_bp.route('/<course_id>', methods=['GET'])
def get_course(course_id):
    """获取单个课程详情"""
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return JsonResult.error('课程不存在')

    return JsonResult.success('获取课程详情成功', course.to_dict())


@course_bp.route('', methods=['POST'])
def create_course():
    """创建课程"""
    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空')

    form = CourseCreateForm(data)
    if not form.validate():
        return JsonResult.error('参数验证失败', form.errors)

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

    return JsonResult.success('创建课程成功', course.to_dict())


@course_bp.route('/<course_id>', methods=['PUT'])
def update_course(course_id):
    """更新课程"""
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return JsonResult.error('课程不存在')

    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空')

    form = CourseUpdateForm(data)
    if not form.validate():
        return JsonResult.error('参数验证失败', form.errors)

    # 更新字段
    if form.title.data:
        course.title = form.title.data
    if form.description.data:
        course.description = form.description.data
    if form.price.data is not None:
        course.price = form.price.data
    if form.score.data is not None:
        course.score = form.score.data
    if form.cover_image.data:
        course.cover_image = form.cover_image.data
    if form.video_url.data:
        course.video_url = form.video_url.data
    if form.category_id.data is not None:
        course.category_id = form.category_id.data
    if form.counselor_id.data is not None:
        course.counselor_id = form.counselor_id.data

    db.session.commit()

    return JsonResult.success('更新课程成功', course.to_dict())


@course_bp.route('/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    """删除课程"""
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return JsonResult.error('课程不存在')

    db.session.delete(course)
    db.session.commit()

    return JsonResult.success('删除课程成功')
