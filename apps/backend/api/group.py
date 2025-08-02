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

group_bp = Blueprint('group', __name__, url_prefix='/group')


@group_bp.route('', methods=['GET'])
def get_groups():
    """获取群组列表"""
    form = GroupQueryForm(request.args)
    if not form.validate():
        return JsonResult.error('参数验证失败', form.errors)

    page = form.page.data
    per_page = form.per_page.data
    name = form.name.data

    # 构建查询
    query = Group.query

    if name:
        query = query.filter(Group.name.like(f'%{name}%'))

    # 分页查询
    pagination = query.order_by(Group.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    groups = [group.to_dict() for group in pagination.items]

    return JsonResult.success('获取群组列表成功', {
        'groups': groups,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@group_bp.route('/<group_id>', methods=['GET'])
def get_group(group_id):
    """获取单个群组详情"""
    group = Group.query.filter_by(id=group_id).first()
    if not group:
        return JsonResult.error('群组不存在')

    return JsonResult.success('获取群组详情成功', group.to_dict())


@group_bp.route('', methods=['POST'])
def create_group():
    """创建群组"""
    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空')

    form = GroupCreateForm(data)
    if not form.validate():
        return JsonResult.error('参数验证失败', form.errors)

    # 检查群组名称是否已存在
    existing_group = Group.query.filter_by(name=form.name.data).first()
    if existing_group:
        return JsonResult.error('群组名称已存在')

    # 创建群组
    group = Group(
        id=str(uuid.uuid4()),
        name=form.name.data,
        description=form.description.data or ''
    )

    db.session.add(group)
    db.session.commit()

    return JsonResult.success('创建群组成功', group.to_dict())


@group_bp.route('/<group_id>', methods=['PUT'])
def update_group(group_id):
    """更新群组"""
    group = Group.query.filter_by(id=group_id).first()
    if not group:
        return JsonResult.error('群组不存在')

    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空')

    form = GroupUpdateForm(data)
    if not form.validate():
        return JsonResult.error('参数验证失败', form.errors)

    # 更新字段
    if form.name.data:
        # 检查新名称是否与其他群组重复
        if form.name.data != group.name:
            existing_group = Group.query.filter_by(name=form.name.data).first()
            if existing_group:
                return JsonResult.error('群组名称已存在')
        group.name = form.name.data
    if form.description.data:
        group.description = form.description.data

    db.session.commit()

    return JsonResult.success('更新群组成功', group.to_dict())


@group_bp.route('/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    """删除群组"""
    group = Group.query.filter_by(id=group_id).first()
    if not group:
        return JsonResult.error('群组不存在')

    db.session.delete(group)
    db.session.commit()

    return JsonResult.success('删除群组成功')
