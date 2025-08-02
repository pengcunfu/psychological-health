"""
课程大纲API
提供课程大纲的增删改查功能

接口列表：
- GET /course_outlines - 获取课程大纲列表
- GET /course_outlines/<outline_id> - 获取单个课程大纲详情
- POST /course_outlines - 创建课程大纲
- PUT /course_outlines/<outline_id> - 更新课程大纲
- DELETE /course_outlines/<outline_id> - 删除课程大纲
"""
from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
import uuid

from models.course_outline import CourseOutline
from models.base import db
from utils.json_result import JsonResult
from form.course_outline import CourseOutlineQueryForm, CourseOutlineCreateForm, CourseOutlineUpdateForm

course_outline_bp = Blueprint('course_outline', __name__, url_prefix='/course_outline')


@course_outline_bp.route('', methods=['GET'])
def get_course_outlines():
    """获取课程大纲列表"""
    form = CourseOutlineQueryForm(request.args)
    if not form.validate():
        return JsonResult.error('参数验证失败', form.errors)

    course_id = form.course_id.data
    outlines = CourseOutline.query.filter_by(course_id=course_id).order_by(CourseOutline.sort_order).all()
    return JsonResult.success('获取课程大纲列表成功', [outline.to_dict() for outline in outlines])


@course_outline_bp.route('/<outline_id>', methods=['GET'])
def get_course_outline(outline_id):
    """获取单个课程大纲"""
    outline = CourseOutline.query.filter_by(id=outline_id).first()
    if not outline:
        return JsonResult.error('课程大纲不存在')
    return JsonResult.success('获取课程大纲成功', outline.to_dict())


@course_outline_bp.route('', methods=['POST'])
def create_course_outline():
    """创建课程大纲"""
    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空')

    form = CourseOutlineCreateForm(data)
    if not form.validate():
        return JsonResult.error('参数验证失败', form.errors)

    outline = CourseOutline(
        id=str(uuid.uuid4()),
        course_id=form.course_id.data,
        title=form.title.data,
        content=form.content.data,
        sort_order=form.sort_order.data if form.sort_order.data is not None else 0
    )
    db.session.add(outline)
    db.session.commit()
    return JsonResult.success('创建课程大纲成功', outline.to_dict())


@course_outline_bp.route('/<outline_id>', methods=['PUT'])
def update_course_outline(outline_id):
    """更新课程大纲"""
    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空')

    form = CourseOutlineUpdateForm(data)
    if not form.validate():
        return JsonResult.error('参数验证失败', form.errors)

    outline = CourseOutline.query.filter_by(id=outline_id).first()
    if not outline:
        return JsonResult.error('课程大纲不存在')

    # 更新课程大纲信息
    if form.title.data:
        outline.title = form.title.data
    if form.content.data:
        outline.content = form.content.data
    if form.sort_order.data is not None:
        outline.sort_order = form.sort_order.data

    db.session.commit()
    return JsonResult.success('更新课程大纲成功', outline.to_dict())


@course_outline_bp.route('/<outline_id>', methods=['DELETE'])
def delete_course_outline(outline_id):
    """删除课程大纲"""
    outline = CourseOutline.query.filter_by(id=outline_id).first()
    if not outline:
        return JsonResult.error('课程大纲不存在')

    db.session.delete(outline)
    db.session.commit()
    return JsonResult.success('删除课程大纲成功')
