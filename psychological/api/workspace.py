"""
工作室API
提供工作室的增删改查功能
"""
from flask import Blueprint
from psychological.models import db
from psychological.models.workspace import Workspace
from psychological.form.workspace import WorkspaceQueryForm, WorkspaceCreateForm, WorkspaceUpdateForm
from psychological.utils.json_result import JsonResult
from psychological.utils.validate import assert_id_exists
from psychological.utils.model_helper import update_model_fields
from psychological.utils.query import create_query_builder
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required
import uuid

workspace_bp = Blueprint('workspace', __name__, url_prefix='/workspace')


@workspace_bp.route('', methods=['GET'])
@validate_form(WorkspaceQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("workspace:get_workspaces")
def get_workspaces(form):
    """获取工作室列表"""

    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(Workspace) \
        .when(form.name.data, Workspace.name.like(f'%{form.name.data}%')) \
        .when(form.status.data, Workspace.status == form.status.data) \
        .order_by(Workspace.sort_order.asc(), Workspace.create_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return JsonResult.success({
        'list': [workspace.to_dict() for workspace in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@workspace_bp.route('/<workspace_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("workspace:get_workspace")
def get_workspace(workspace_id):
    """获取单个工作室"""
    assert_id_exists(workspace_id, "工作室ID不能为空")

    workspace = Workspace.query.get(workspace_id)
    if not workspace:
        return JsonResult.error('工作室不存在', 404)

    return JsonResult.success(workspace.to_dict())


@workspace_bp.route('', methods=['POST'])
@validate_form(WorkspaceCreateForm)
@role_required(['admin', 'manager'])
@permission_required("workspace:create_workspace")
def create_workspace(form):
    """创建工作室"""

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
@validate_form(WorkspaceUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("workspace:update_workspace")
def update_workspace(workspace_id, form):
    """更新工作室"""
    assert_id_exists(workspace_id, "工作室ID不能为空")

    workspace = Workspace.query.get(workspace_id)
    if not workspace:
        return JsonResult.error('工作室不存在', 404)

    # 检查名称唯一性（排除当前工作室）
    if form.name.data and form.name.data != workspace.name:
        if form.validate_name_unique(workspace_id):
            return JsonResult.error('工作室名称已存在', 409)
        workspace.name = form.name.data

    # 处理环境照片JSON格式（特殊字段需要单独处理）
    if form.environment_images.data is not None:
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

    # 使用统一的更新函数更新其他字段
    update_model_fields(workspace, form, exclude_fields=['environment_images'])

    db.session.commit()
    return JsonResult.success(workspace.to_dict(), '更新成功')


@workspace_bp.route('/<workspace_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("workspace:delete_workspace")
def delete_workspace(workspace_id):
    """删除工作室"""
    assert_id_exists(workspace_id, "工作室ID不能为空")

    workspace = Workspace.query.get(workspace_id)
    if not workspace:
        return JsonResult.error('工作室不存在', 404)

    db.session.delete(workspace)
    db.session.commit()

    return JsonResult.success(None, '删除成功')
