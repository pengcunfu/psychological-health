"""
群组管理API
提供系统群组的增删改查功能

接口列表：
- GET /group - 获取群组列表
- GET /group/<group_id> - 获取单个群组详情
- POST /group - 创建群组
- PUT /group/<group_id> - 更新群组
- DELETE /group/<group_id> - 删除群组
"""
from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
import uuid

from models.group import Group
from models.base import db
from utils.json_result import JsonResult
from form.group import GroupQueryForm, GroupCreateForm, GroupUpdateForm
from utils.validate import validate_data, validate_args
from utils.model_helper import update_model_from_form

group_bp = Blueprint('group', __name__, url_prefix='/group')


@group_bp.route('', methods=['GET'])
def get_groups():
    """获取群组列表"""
    form = validate_args(GroupQueryForm)

    page = form.page.data
    per_page = form.per_page.data
    title = form.title.data

    # 构建查询
    query = Group.query

    if title:
        query = query.filter(Group.title.like(f'%{title}%'))

    # 分页查询
    pagination = query.order_by(Group.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    groups = [group.to_dict() for group in pagination.items]

    return JsonResult.success({
        'list': groups,
        'total': pagination.total,
        'page': page,
        'per_page': per_page
    })


@group_bp.route('/<group_id>', methods=['GET'])
def get_group(group_id):
    """获取单个群组详情"""
    group = Group.query.filter_by(id=group_id).first()
    if not group:
        return JsonResult.error('群组不存在', 404)

    return JsonResult.success(group.to_dict())


@group_bp.route('', methods=['POST'])
def create_group():
    """创建群组"""
    form = validate_data(GroupCreateForm)

    # 检查群组标题是否已存在
    existing_group = Group.query.filter_by(title=form.title.data).first()
    if existing_group:
        return JsonResult.error('群组标题已存在', 400)

    # 创建群组
    group = Group(
        id=str(uuid.uuid4()),
        title=form.title.data,
        description=form.description.data or ''
    )

    db.session.add(group)
    db.session.commit()

    return JsonResult.success(group.to_dict(), '创建群组成功', 201)


@group_bp.route('/<group_id>', methods=['PUT'])
def update_group(group_id):
    """更新群组"""
    group = Group.query.filter_by(id=group_id).first()
    if not group:
        return JsonResult.error('群组不存在', 404)

    form = validate_data(GroupUpdateForm)

    # 检查新标题是否与其他群组重复
    if form.title.data and form.title.data != group.title:
        existing_group = Group.query.filter_by(title=form.title.data).first()
        if existing_group:
            return JsonResult.error('群组标题已存在', 400)

    # 更新字段
    update_model_from_form(group, form)

    db.session.commit()

    return JsonResult.success(group.to_dict(), '更新群组成功')


@group_bp.route('/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    """删除群组"""
    group = Group.query.filter_by(id=group_id).first()
    if not group:
        return JsonResult.error('群组不存在', 404)

    db.session.delete(group)
    db.session.commit()

    return JsonResult.success(None, '删除群组成功')
