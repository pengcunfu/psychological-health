"""
群组管理API
提供系统群组的增删改查功能
"""
from flask import Blueprint
import uuid

from ..models import Group
from pcf_flask_helper.model.base import db
from pcf_flask_helper.common import json_success, json_error
from pcf_flask_helper.form.validate import assert_id_exists
from pcf_flask_helper.model.query import create_query_builder
from psychological.utils.model_helper import update_model_fields
from ..form import GroupQueryForm, GroupCreateForm, GroupUpdateForm
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required

group_bp = Blueprint('group', __name__, url_prefix='/group')


@group_bp.route('', methods=['GET'])
@validate_form(GroupQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("group:get_groups")
def get_groups(form):
    """获取群组列表"""
    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(Group) \
        .when(form.title.data, Group.title.like(f'%{form.title.data}%')) \
        .order_by(Group.create_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return json_success({
        'list': [group.to_dict() for group in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@group_bp.route('/<group_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("group:get_group")
def get_group(group_id):
    """获取单个群组详情"""
    assert_id_exists(group_id, "群组ID不能为空")

    group = Group.query.filter_by(id=group_id).first()
    if not group:
        return json_error('群组不存在', 404)

    return json_success(group.to_dict())


@group_bp.route('', methods=['POST'])
@validate_form(GroupCreateForm)
@role_required(['admin', 'manager'])
@permission_required("group:create_group")
def create_group(form):
    """创建群组"""
    # 检查群组标题是否已存在
    existing_group = create_query_builder(Group) \
        .filter(Group.title == form.title.data) \
        .first()
    if existing_group:
        return json_error('群组标题已存在', 400)

    # 创建群组
    group = Group(
        id=str(uuid.uuid4()),
        title=form.title.data,
        cover_image=form.cover_image.data or '',
        counselor_id=form.counselor_id.data,
        counselor_name=form.counselor_name.data,
        price=form.price.data or 0.0,
        capacity=form.capacity.data or 0,
        enrolled=0,  # 新建群组已报名人数为0
        location=form.location.data or '',
        city=form.city.data or '',
        type=form.type.data or '',
        start_date=form.start_date.data or '',
        duration=form.duration.data or '',
        schedule=form.schedule.data or '',
        description=form.description.data or '',
        status=form.status.data if form.status.data is not None else 1  # 默认状态为1（报名中）
    )

    db.session.add(group)
    db.session.commit()

    return json_success(group.to_dict(), '创建群组成功', 201)


@group_bp.route('/<group_id>', methods=['PUT'])
@validate_form(GroupUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("group:update_group")
def update_group(group_id, form):
    """更新群组"""
    assert_id_exists(group_id, "群组ID不能为空")

    group = Group.query.filter_by(id=group_id).first()
    if not group:
        return json_error('群组不存在', 404)

    # 检查新标题是否与其他群组重复
    if form.title.data and form.title.data != group.title:
        existing_group = create_query_builder(Group) \
            .filter(Group.title == form.title.data) \
            .first()
        if existing_group:
            return json_error('群组标题已存在', 400)

    # 使用统一的更新函数，排除enrolled字段
    update_model_fields(group, form, exclude_fields=['enrolled'])

    # 确保enrolled字段不会被表单更新（应该通过其他业务逻辑控制）
    # enrolled字段应该通过报名/取消报名的API来管理，而不是直接更新

    db.session.commit()

    return json_success(group.to_dict(), '更新群组成功')


@group_bp.route('/<group_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("group:delete_group")
def delete_group(group_id):
    """删除群组"""
    assert_id_exists(group_id, "群组ID不能为空")

    group = Group.query.filter_by(id=group_id).first()
    if not group:
        return json_error('群组不存在', 404)

    # 可以添加删除前的业务检查
    # 例如：检查是否有用户已报名该群组
    if group.enrolled > 0:
        return json_error('该群组已有用户报名，无法删除', 400)

    db.session.delete(group)
    db.session.commit()

    return json_success(None, '删除群组成功')
