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

from models.disease_tags import DiseaseTags
from models.base import db
from utils.json_result import JsonResult
from form.disease_tags import DiseaseTagsQueryForm

disease_tags_bp = Blueprint('disease_tags', __name__, url_prefix='/disease-tag')


@disease_tags_bp.route('', methods=['GET'])
def get_disease_tags():
    """获取疾病标签列表"""
    form = DiseaseTagsQueryForm(request.args)
    if not form.validate():
        return JsonResult.error(form.get_first_error(), 400)

    query = DiseaseTags.query

    name = form.get_name()
    if name:
        query = query.filter(DiseaseTags.name.like(f'%{name}%'))

    page = form.get_page()
    per_page = form.get_per_page()

    pagination = query.order_by(DiseaseTags.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    tags = [tag.to_dict() for tag in pagination.items]

    return JsonResult.success({
        'tags': tags,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@disease_tags_bp.route('/<tag_id>', methods=['GET'])
def get_disease_tag(tag_id):
    """获取单个疾病标签详情"""
    tag = DiseaseTags.query.filter_by(id=tag_id).first()
    if not tag:
        return JsonResult.error('疾病标签不存在', 404)

    return JsonResult.success(tag.to_dict())


from form.disease_tags import DiseaseTagsCreateForm


@disease_tags_bp.route('', methods=['POST'])
def create_disease_tag():
    """创建疾病标签"""
    form = DiseaseTagsCreateForm(request.get_json())
    if not form.validate():
        return JsonResult.error(form.get_first_error(), 400)

        # 检查标签名称是否已存在
        existing_tag = DiseaseTags.query.filter_by(name=form.name.data).first()
        if existing_tag:
            return JsonResult.error('标签名称已存在', 400)

        # 创建疾病标签
        tag = DiseaseTags(
            name=form.name.data,
            description=form.description.data
        )

        db.session.add(tag)
        db.session.commit()

        return JsonResult.success(tag.to_dict(), '疾病标签创建成功', 201)


@disease_tags_bp.route('/<tag_id>', methods=['PUT'])
def update_disease_tag(tag_id):
    """更新疾病标签"""
    form = DiseaseTagsCreateForm(request.get_json())
    if not form.validate():
        return JsonResult.error(form.get_first_error(), 400)

    tag = DiseaseTags.query.filter_by(id=tag_id).first()
    if not tag:
        return JsonResult.error('疾病标签不存在', 404)

    # 更新字段
    if form.name.data:
        # 检查新名称是否与其他标签重复
        if form.name.data != tag.name:
            existing_tag = DiseaseTags.query.filter_by(name=form.name.data).first()
            if existing_tag:
                return JsonResult.error('标签名称已存在', 400)
        tag.name = form.name.data

    if form.description.data is not None:
        tag.description = form.description.data

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
