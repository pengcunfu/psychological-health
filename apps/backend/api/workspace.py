"""
工作室API
提供工作室的增删改查功能

接口列表：
- GET /workspace - 获取工作室列表
- GET /workspace/<workspace_id> - 获取单个工作室详情
- POST /workspace - 创建工作室
- PUT /workspace/<workspace_id> - 更新工作室
- DELETE /workspace/<workspace_id> - 删除工作室
"""
from flask import Blueprint, request
from models import db
from models.workspace import Workspace
from sqlalchemy.exc import SQLAlchemyError
from form.workspace import WorkspaceQueryForm, WorkspaceCreateForm, WorkspaceUpdateForm
from utils.json_result import JsonResult
from utils.validate import validate_args, validate_data
import uuid

workspace_bp = Blueprint('workspace', __name__, url_prefix='/workspace')


@workspace_bp.route('', methods=['GET'])
def get_workspaces():
    """获取工作室列表"""
    form = validate_args(WorkspaceQueryForm)

    page = form.page.data
    per_page = form.per_page.data
    name = form.name.data
    status = form.status.data

    query = Workspace.query

    if name:
        query = query.filter(Workspace.name.like(f'%{name}%'))
    if status is not None:
        query = query.filter(Workspace.status == status)

    paginate = query.order_by(Workspace.sort_order.asc(), Workspace.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return JsonResult.success({
        'list': [workspace.to_dict() for workspace in paginate.items],
        'total': paginate.total,
        'page': page,
        'per_page': per_page
    })


@workspace_bp.route('/<workspace_id>', methods=['GET'])
def get_workspace(workspace_id):
    """获取单个工作室"""
    if not workspace_id or not workspace_id.strip():
        return JsonResult.error('工作室ID不能为空', 400)

    workspace = Workspace.query.get(workspace_id)
    if not workspace:
        return JsonResult.error('工作室不存在', 404)

    return JsonResult.success(workspace.to_dict())


@workspace_bp.route('', methods=['POST'])
def create_workspace():
    """创建工作室"""
    form = validate_data(WorkspaceCreateForm)

    # 检查名称唯一性
    if form.validate_name_unique():
        return JsonResult.error('工作室名称已存在', 409)

    # 处理环境照片JSON格式
    environment_images = []
    if form.environment_images.data:
        try:
            import json
            if isinstance(form.environment_images.data, str):
                environment_images = json.loads(form.environment_images.data)
            elif isinstance(form.environment_images.data, list):
                environment_images = form.environment_images.data
        except (json.JSONDecodeError, TypeError):
            environment_images = []

    workspace = Workspace(
        id=str(uuid.uuid4()),
        name=form.name.data,
        cover_image=form.cover_image.data or '',
        address=form.address.data or '',
        distance=form.distance.data or 0.0,
        business_hours=form.business_hours.data or '',
        introduction=form.introduction.data or '',
        slogan=form.slogan.data or '',
        latitude=form.latitude.data or 0.0,
        longitude=form.longitude.data or 0.0,
        status=form.status.data or 1,
        sort_order=form.sort_order.data or 100
    )
    
    # 设置环境照片
    workspace.environment_images = environment_images

    db.session.add(workspace)
    db.session.commit()

    return JsonResult.success(workspace.to_dict(), '创建成功', 201)


@workspace_bp.route('/<workspace_id>', methods=['PUT'])
def update_workspace(workspace_id):
    """更新工作室"""
    if not workspace_id or not workspace_id.strip():
        return JsonResult.error('工作室ID不能为空', 400)

    form = validate_data(WorkspaceUpdateForm)

    workspace = Workspace.query.get(workspace_id)
    if not workspace:
        return JsonResult.error('工作室不存在', 404)

    # 检查名称唯一性（排除当前工作室）
    if form.name.data and form.name.data != workspace.name:
        if form.validate_name_unique(workspace_id):
            return JsonResult.error('工作室名称已存在', 409)
        workspace.name = form.name.data

    # 更新所有字段
    if form.cover_image.data is not None:
        workspace.cover_image = form.cover_image.data
    if form.address.data is not None:
        workspace.address = form.address.data
    if form.distance.data is not None:
        workspace.distance = form.distance.data
    if form.business_hours.data is not None:
        workspace.business_hours = form.business_hours.data
    if form.environment_images.data is not None:
        # 处理环境照片JSON格式
        try:
            import json
            if isinstance(form.environment_images.data, str):
                environment_images = json.loads(form.environment_images.data)
            elif isinstance(form.environment_images.data, list):
                environment_images = form.environment_images.data
            else:
                environment_images = []
            workspace.environment_images = environment_images
        except (json.JSONDecodeError, TypeError):
            pass
    if form.introduction.data is not None:
        workspace.introduction = form.introduction.data
    if form.slogan.data is not None:
        workspace.slogan = form.slogan.data
    if form.latitude.data is not None:
        workspace.latitude = form.latitude.data
    if form.longitude.data is not None:
        workspace.longitude = form.longitude.data
    if form.status.data is not None:
        workspace.status = form.status.data
    if form.sort_order.data is not None:
        workspace.sort_order = form.sort_order.data

    db.session.commit()
    return JsonResult.success(workspace.to_dict(), '更新成功')


@workspace_bp.route('/<workspace_id>', methods=['DELETE'])
def delete_workspace(workspace_id):
    """删除工作室"""
    if not workspace_id or not workspace_id.strip():
        return JsonResult.error('工作室ID不能为空', 400)

    workspace = Workspace.query.get(workspace_id)
    if not workspace:
        return JsonResult.error('工作室不存在', 404)

    db.session.delete(workspace)
    db.session.commit()

    return JsonResult.success(None, '删除成功')
