"""
疾病标签API
提供疾病标签的增删改查功能
"""
from flask import Blueprint
import uuid

from psychological.models.disease_tags import DiseaseTags
from psychological.models.base import db
from pcf_flask_helper.common import json_success, json_error
from psychological.utils.validate import assert_id_exists
from psychological.utils.query import create_query_builder
from psychological.utils.model_helper import update_model_fields
from psychological.form.disease_tags import DiseaseTagsQueryForm, DiseaseTagsCreateForm
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required

disease_tags_bp = Blueprint('disease_tag', __name__, url_prefix='/disease-tag')


@disease_tags_bp.route('', methods=['GET'])
@validate_form(DiseaseTagsQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("disease_tags:get_disease_tags")
def get_disease_tags(form):
    """获取疾病标签列表"""
    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(DiseaseTags) \
        .when(form.name.data, DiseaseTags.name.like(f'%{form.name.data}%')) \
        .order_by(DiseaseTags.create_time.desc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return json_success({
        'list': [tag.to_dict() for tag in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@disease_tags_bp.route('/<tag_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("disease_tags:get_disease_tag")
def get_disease_tag(tag_id):
    """获取单个疾病标签详情"""
    assert_id_exists(tag_id, "疾病标签ID不能为空")
    
    tag = DiseaseTags.query.filter_by(id=tag_id).first()
    if not tag:
        return json_error('疾病标签不存在', 404)

    return json_success(tag.to_dict())


@disease_tags_bp.route('', methods=['POST'])
@validate_form(DiseaseTagsCreateForm)
@role_required(['admin', 'manager'])
@permission_required("disease_tags:create_disease_tag")
def create_disease_tag(form):
    """创建疾病标签"""
    # 检查标签名称是否已存在
    existing_tag = create_query_builder(DiseaseTags) \
        .filter(DiseaseTags.name == form.name.data) \
        .first()
    if existing_tag:
        return json_error('标签名称已存在', 400)

    # 创建疾病标签
    tag = DiseaseTags(
        id=str(uuid.uuid4()),
        name=form.name.data,
        description=form.description.data
    )

    db.session.add(tag)
    db.session.commit()

    return json_success(tag.to_dict(), '疾病标签创建成功', 201)


@disease_tags_bp.route('/<tag_id>', methods=['PUT'])
@validate_form(DiseaseTagsCreateForm)
@role_required(['admin', 'manager'])
@permission_required("disease_tags:update_disease_tag")
def update_disease_tag(tag_id, form):
    """更新疾病标签"""
    assert_id_exists(tag_id, "疾病标签ID不能为空")
    
    tag = DiseaseTags.query.filter_by(id=tag_id).first()
    if not tag:
        return json_error('疾病标签不存在', 404)

    # 检查新名称是否与其他标签重复
    if form.name.data and form.name.data != tag.name:
        existing_tag = create_query_builder(DiseaseTags) \
            .filter(DiseaseTags.name == form.name.data) \
            .first()
        if existing_tag:
            return json_error('标签名称已存在', 400)

    # 使用统一的更新函数
    update_model_fields(tag, form)

    db.session.commit()

    return json_success(tag.to_dict(), '疾病标签更新成功')


@disease_tags_bp.route('/<tag_id>', methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("disease_tags:delete_disease_tag")
def delete_disease_tag(tag_id):
    """删除疾病标签"""
    assert_id_exists(tag_id, "疾病标签ID不能为空")
    
    tag = DiseaseTags.query.filter_by(id=tag_id).first()
    if not tag:
        return json_error('疾病标签不存在', 404)

    db.session.delete(tag)
    db.session.commit()

    return json_success(None, '疾病标签删除成功')
