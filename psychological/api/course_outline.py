"""
课程大纲API
提供课程大纲的增删改查功能
"""
from flask import Blueprint
import uuid

from psychological.models.course_outline import CourseOutline
from psychological.models.course import Course
from psychological.models.base import db
from psychological.utils.json_result import JsonResult
from psychological.utils.validate import assert_id_exists
from psychological.utils.query import create_query_builder
from psychological.utils.model_helper import update_model_fields
from psychological.form.course_outline import CourseQueryForm, CourseOutlineQueryForm, CourseOutlineCreateForm, CourseOutlineUpdateForm
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required

course_outline_bp = Blueprint('course-outline', __name__, url_prefix='/course-outline')


@course_outline_bp.route('/courses', methods=['GET'])
@validate_form(CourseQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("course_outline:get_courses")
def get_courses(form):
    """获取课程列表"""
    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(Course) \
        .order_by(Course.create_time.desc()) \
        .paginate(form.page.data or 1, form.per_page.data or 1000, 1000)
    
    return JsonResult.success({
        'courses': [course.to_dict() for course in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@course_outline_bp.route('', methods=['GET'])
@validate_form(CourseOutlineQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("course_outline:get_course_outlines")
def get_course_outlines(form):
    """获取课程大纲列表"""
    outlines = create_query_builder(CourseOutline) \
        .filter(CourseOutline.course_id == form.course_id.data) \
        .order_by(CourseOutline.sort_order) \
        .all()
    
    return JsonResult.success([outline.to_dict() for outline in outlines])


@course_outline_bp.route('/<outline_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("course_outline:get_course_outline")
def get_course_outline(outline_id):
    """获取单个课程大纲"""
    assert_id_exists(outline_id, "课程大纲ID不能为空")
    
    outline = CourseOutline.query.filter_by(id=outline_id).first()
    if not outline:
        return JsonResult.error('课程大纲不存在', 404)
    
    return JsonResult.success(outline.to_dict())


@course_outline_bp.route('', methods=['POST'])
@validate_form(CourseOutlineCreateForm)
@role_required(['admin', 'manager'])
@permission_required("course_outline:create_course_outline")
def create_course_outline(form):
    """创建课程大纲"""
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
@validate_form(CourseOutlineUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("course_outline:update_course_outline")
def update_course_outline(outline_id, form):
    """更新课程大纲"""
    assert_id_exists(outline_id, "课程大纲ID不能为空")
    
    outline = CourseOutline.query.filter_by(id=outline_id).first()
    if not outline:
        return JsonResult.error('课程大纲不存在', 404)

    # 使用统一的模型更新方法
    update_model_fields(outline, form)

    db.session.commit()
    
    return JsonResult.success(outline.to_dict(), '更新课程大纲成功')


@course_outline_bp.route('/<outline_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("course_outline:delete_course_outline")
def delete_course_outline(outline_id):
    """删除课程大纲"""
    assert_id_exists(outline_id, "课程大纲ID不能为空")
    
    outline = CourseOutline.query.filter_by(id=outline_id).first()
    if not outline:
        return JsonResult.error('课程大纲不存在', 404)

    db.session.delete(outline)
    db.session.commit()
    
    return JsonResult.success(None, '删除课程大纲成功')
