"""
疾病标签API
提供疾病标签的增删改查功能

接口列表：
- GET /disease-tags - 获取疾病标签列表
- GET /disease-tags/<tag_id> - 获取单个疾病标签详情
- POST /disease-tags - 创建疾病标签
- PUT /disease-tags/<tag_id> - 更新疾病标签
- DELETE /disease-tags/<tag_id> - 删除疾病标签
"""
from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
import uuid

from models.disease_tags import DiseaseTags
from models.base import db
from utils.json_result import JsonResult
from form.disease_tags import DiseaseTagsQueryForm, DiseaseTagsCreateForm
from utils.validate import validate_data, validate_args
from utils.model_helper import update_model_from_form

disease_tags_bp = Blueprint('disease_tag', __name__, url_prefix='/disease-tag')


@disease_tags_bp.route('', methods=['GET'])
def get_disease_tags():
    """获取疾病标签列表"""
    form = validate_args(DiseaseTagsQueryForm)

    query = DiseaseTags.query

    name = form.name.data
    if name:
        query = query.filter(DiseaseTags.name.like(f'%{name}%'))

    page = form.page.data
    per_page = form.per_page.data

    pagination = query.order_by(DiseaseTags.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    tags = [tag.to_dict() for tag in pagination.items]

    return JsonResult.success({
        'list': tags,
        'total': pagination.total,
        'page': page,
        'per_page': per_page
    })


@disease_tags_bp.route('/<tag_id>', methods=['GET'])
def get_disease_tag(tag_id):
    """获取单个疾病标签详情"""
    tag = DiseaseTags.query.filter_by(id=tag_id).first()
    if not tag:
        return JsonResult.error('疾病标签不存在', 404)

    return JsonResult.success(tag.to_dict())


@disease_tags_bp.route('', methods=['POST'])
def create_disease_tag():
    """创建疾病标签"""
    form = validate_data(DiseaseTagsCreateForm)

    # 检查标签名称是否已存在
    existing_tag = DiseaseTags.query.filter_by(name=form.name.data).first()
    if existing_tag:
        return JsonResult.error('标签名称已存在', 400)

    # 创建疾病标签
    tag = DiseaseTags(
        id=str(uuid.uuid4()),
        name=form.name.data,
        description=form.description.data
    )

    db.session.add(tag)
    db.session.commit()

    return JsonResult.success(tag.to_dict(), '疾病标签创建成功', 201)


@disease_tags_bp.route('/<tag_id>', methods=['PUT'])
def update_disease_tag(tag_id):
    """更新疾病标签"""
    tag = DiseaseTags.query.filter_by(id=tag_id).first()
    if not tag:
        return JsonResult.error('疾病标签不存在', 404)

    form = validate_data(DiseaseTagsCreateForm)

    # 检查新名称是否与其他标签重复
    if form.name.data and form.name.data != tag.name:
        existing_tag = DiseaseTags.query.filter_by(name=form.name.data).first()
        if existing_tag:
            return JsonResult.error('标签名称已存在', 400)

    # 更新字段
    update_model_from_form(tag, form)

    db.session.commit()

    return JsonResult.success(tag.to_dict(), '疾病标签更新成功')


@disease_tags_bp.route('/<tag_id>', methods=['DELETE'])
def delete_disease_tag(tag_id):
    """删除疾病标签"""
    tag = DiseaseTags.query.filter_by(id=tag_id).first()
    if not tag:
        return JsonResult.error('疾病标签不存在', 404)

    db.session.delete(tag)
    db.session.commit()

    return JsonResult.success(None, '疾病标签删除成功')
