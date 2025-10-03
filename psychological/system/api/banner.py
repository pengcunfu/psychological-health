"""
横幅管理API
提供系统横幅的增删改查功能
"""
from flask import Blueprint
from psychological.models.banner import Banner
from psychological.models.base import db
from pcf_flask_helper.common import json_success, json_error
from psychological.utils.validate import assert_id_exists
from psychological.utils.query import create_query_builder, assert_exists
from psychological.utils.model_helper import update_model_fields
from psychological.utils.image import process_banner_images
from psychological.form.banner import BannerQueryForm, BannerCreateForm, BannerUpdateForm
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required
import uuid

banner_bp = Blueprint("banner", __name__, url_prefix="/banner")


@banner_bp.route("", methods=['GET'])
@validate_form(BannerQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("banner:get_banners")
def get_banners(form):
    """获取横幅列表 - 使用查询参数验证装饰器"""
    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(Banner) \
        .when(form.title.data, Banner.title.like(f'%{form.title.data}%')) \
        .order_by(Banner.sort_order.asc()) \
        .paginate(form.page.data, form.per_page.data, 100)

    return json_success({
        'list': process_banner_images([banner.to_dict() for banner in result['items']]),
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page']
    })


@banner_bp.route("/<banner_id>", methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("banner:get_banner")
def get_banner(banner_id):
    assert_id_exists(banner_id, "横幅ID不能为空")
    
    banner = assert_exists(Banner, Banner.id == banner_id, "横幅不存在")
    # 处理轮播图数据中的图片URL
    return json_success(process_banner_images(banner.to_dict()))


@banner_bp.route("", methods=['POST'])
@validate_form(BannerCreateForm)
@role_required(['admin', 'manager'])
@permission_required("banner:create_banner")
def create_banner(form):
    """创建横幅 - 使用JSON验证和权限装饰器"""
    # 创建横幅
    banner = Banner(
        id=str(uuid.uuid4()),
        title=form.title.data,
        image_url=form.image_url.data,
        link_url=form.link_url.data,
        sort_order=form.sort_order.data if form.sort_order.data is not None else 0,
    )

    db.session.add(banner)
    db.session.commit()
    return json_success(banner.to_dict(), "创建成功", 201)


@banner_bp.route("/<banner_id>", methods=['PUT'])
@validate_form(BannerUpdateForm)
@role_required(['admin', 'manager'])
@permission_required("banner:update_banner")
def update_banner(banner_id, form):
    """更新横幅 - 使用JSON验证和权限装饰器"""
    assert_id_exists(banner_id, "横幅ID不能为空")
    
    banner = assert_exists(Banner, Banner.id == banner_id, "横幅不存在")

    # 更新字段
    update_model_fields(banner, form)

    db.session.commit()
    return json_success(banner.to_dict(), "更新成功")


@banner_bp.route("/<banner_id>", methods=['DELETE'])
@role_required(['admin', 'manager'])
@permission_required("banner:delete_banner")
def delete_banner(banner_id):
    """删除横幅 - 需要管理员权限"""
    assert_id_exists(banner_id, "横幅ID不能为空")
    
    banner = assert_exists(Banner, Banner.id == banner_id, "横幅不存在")

    db.session.delete(banner)
    db.session.commit()
    return json_success(None, "删除成功")
