"""
课程大纲API
提供课程大纲的增删改查功能

接口列表：
- GET /course_outlines - 获取课程大纲列表
- GET /course_outlines/<outline_id> - 获取单个课程大纲详情
- POST /course_outlines - 创建课程大纲
- PUT /course_outlines/<outline_id> - 更新课程大纲
- DELETE /course_outlines/<outline_id> - 删除课程大纲
- GET /courses - 获取课程列表
"""
from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
import uuid

from models.course_outline import CourseOutline
from models.course import Course
from models.base import db
from utils.json_result import JsonResult
from form.course_outline import CourseQueryForm, CourseOutlineQueryForm, CourseOutlineCreateForm, CourseOutlineUpdateForm
from utils.validate import validate_data, validate_args
from utils.model_helper import update_model_from_form

course_outline_bp = Blueprint('course-outline', __name__, url_prefix='/course-outline')


@course_outline_bp.route('/courses', methods=['GET'])
def get_courses():
    """获取课程列表"""
    form = validate_args(CourseQueryForm)
    
    page = form.page.data or 1
    per_page = form.per_page.data or 1000
    
    # 分页查询
    pagination = Course.query.order_by(Course.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    course_list = [course.to_dict() for course in pagination.items]
    
    return JsonResult.success({
        'courses': course_list,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@course_outline_bp.route('', methods=['GET'])
def get_course_outlines():
    """获取课程大纲列表"""
    form = validate_args(CourseOutlineQueryForm)

    course_id = form.course_id.data
    outlines = CourseOutline.query.filter_by(course_id=course_id).order_by(CourseOutline.sort_order).all()
    
    return JsonResult.success([outline.to_dict() for outline in outlines])


@course_outline_bp.route('/<outline_id>', methods=['GET'])
def get_course_outline(outline_id):
    """获取单个课程大纲"""
    outline = CourseOutline.query.filter_by(id=outline_id).first()
    if not outline:
        return JsonResult.error('课程大纲不存在', 404)
    
    return JsonResult.success(outline.to_dict())


@course_outline_bp.route('', methods=['POST'])
def create_course_outline():
    """创建课程大纲"""
    form = validate_data(CourseOutlineCreateForm)

    outline = CourseOutline(
        id=str(uuid.uuid4()),
        course_id=form.course_id.data,
        title=form.title.data,
        content=form.content.data,
        video_url=form.video_url.data,
        sort_order=form.sort_order.data if form.sort_order.data is not None else 0
    )
    
    db.session.add(outline)
    db.session.commit()
    
    return JsonResult.success(outline.to_dict(), '创建课程大纲成功', 201)


@course_outline_bp.route('/<outline_id>', methods=['PUT'])
def update_course_outline(outline_id):
    """更新课程大纲"""
    outline = CourseOutline.query.filter_by(id=outline_id).first()
    if not outline:
        return JsonResult.error('课程大纲不存在', 404)

    form = validate_data(CourseOutlineUpdateForm)

    # 使用统一的模型更新方法
    update_model_from_form(outline, form)

    db.session.commit()
    
    return JsonResult.success(outline.to_dict(), '更新课程大纲成功')


@course_outline_bp.route('/<outline_id>', methods=['DELETE'])
def delete_course_outline(outline_id):
    """删除课程大纲"""
    outline = CourseOutline.query.filter_by(id=outline_id).first()
    if not outline:
        return JsonResult.error('课程大纲不存在', 404)

    db.session.delete(outline)
    db.session.commit()
    
    return JsonResult.success(None, '删除课程大纲成功')
