"""
工作空间API
提供工作空间的增删改查功能

接口列表：
- GET /workspaces - 获取工作空间列表
- GET /workspaces/<workspace_id> - 获取单个工作空间详情
- POST /workspaces - 创建工作空间
- PUT /workspaces/<workspace_id> - 更新工作空间
- DELETE /workspaces/<workspace_id> - 删除工作空间
"""
from flask import Blueprint, request
from models import db
from models.workspace import Workspace
from sqlalchemy.exc import SQLAlchemyError
from form.workspace import WorkspaceQueryForm, WorkspaceCreateForm, WorkspaceUpdateForm
from utils.json_result import JsonResult
import uuid

workspace_bp = Blueprint('workspace', __name__, url_prefix='/workspace')


@workspace_bp.route('', methods=['GET'])
def get_workspaces():
    """获取工作空间列表"""
    form = WorkspaceQueryForm(request.args)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    page = form.get_page()
    per_page = form.get_per_page()
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
    """获取单个工作空间"""
    if not workspace_id or not workspace_id.strip():
        return JsonResult.error('工作空间ID不能为空', 400)

    workspace = Workspace.query.get(workspace_id)
    if not workspace:
        return JsonResult.error('工作空间不存在', 404)

    return JsonResult.success(workspace.to_dict())


@workspace_bp.route('', methods=['POST'])
def create_workspace():
    """创建工作空间"""
    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    form = WorkspaceCreateForm(data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 检查名称唯一性
    if form.validate_name_unique():
        return JsonResult.error('工作空间名称已存在', 409)

    workspace = Workspace(
        id=str(uuid.uuid4()),
        name=form.name.data,
        description=form.description.data,
        status=form.status.data,
        sort_order=form.sort_order.data
    )

    db.session.add(workspace)
    db.session.commit()

    return JsonResult.success(workspace.to_dict(), '创建成功', 201)


@workspace_bp.route('/<workspace_id>', methods=['PUT'])
def update_workspace(workspace_id):
    """更新工作空间"""
    if not workspace_id or not workspace_id.strip():
        return JsonResult.error('工作空间ID不能为空', 400)

    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    form = WorkspaceUpdateForm(data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    workspace = Workspace.query.get(workspace_id)
    if not workspace:
        return JsonResult.error('工作空间不存在', 404)

    # 检查名称唯一性（排除当前工作空间）
    if form.name.data and form.name.data != workspace.name:
        if form.validate_name_unique(workspace_id):
            return JsonResult.error('工作空间名称已存在', 409)
        workspace.name = form.name.data

    if form.description.data is not None:
        workspace.description = form.description.data
    if form.status.data is not None:
        workspace.status = form.status.data
    if form.sort_order.data is not None:
        workspace.sort_order = form.sort_order.data

    db.session.commit()
    return JsonResult.success(workspace.to_dict(), '更新成功')


@workspace_bp.route('/<workspace_id>', methods=['DELETE'])
def delete_workspace(workspace_id):
    """删除工作空间"""
    if not workspace_id or not workspace_id.strip():
        return JsonResult.error('工作空间ID不能为空', 400)

    workspace = Workspace.query.get(workspace_id)
    if not workspace:
        return JsonResult.error('工作空间不存在', 404)

    db.session.delete(workspace)
    db.session.commit()

    return JsonResult.success(None, '删除成功')
