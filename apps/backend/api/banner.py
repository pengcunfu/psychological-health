"""
横幅管理API
提供系统横幅的增删改查功能

接口列表：
- GET /banner - 获取横幅列表
- GET /banner/<banner_id> - 获取单个横幅详情
- POST /banner - 创建横幅
- PUT /banner/<banner_id> - 更新横幅
- DELETE /banner/<banner_id> - 删除横幅
"""
from flask import Blueprint, request
from models.banner import Banner
from form.banner import BannerQueryForm, BannerCreateForm, BannerUpdateForm
from sqlalchemy.exc import SQLAlchemyError
from utils.json_result import JsonResult
from models.base import db
from utils.validate import validate_data, validate_args
from utils.model_helper import update_model_from_form
from utils.image import process_banner_images
import uuid

banner_bp = Blueprint("banner", __name__, url_prefix="/banner")


@banner_bp.route("", methods=['GET'])
def get_banners():
    form = validate_args(BannerQueryForm)

    page = form.page.data
    per_page = form.per_page.data
    title = form.title.data

    query = Banner.query
    if title:
        query = query.filter(Banner.title.like(f'%{title}%'))

    paginate = query.order_by(Banner.sort_order.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    banners = paginate.items

    # 处理轮播图数据中的图片URL
    banners_data = [banner.to_dict() for banner in banners]
    processed_banners = process_banner_images(banners_data)
    
    return JsonResult.success({
        'list': processed_banners,
        'total': paginate.total,
        'page': page,
        'per_page': per_page
    })


@banner_bp.route("/<banner_id>", methods=['GET'])
def get_banner(banner_id):
    banner = Banner.query.get(banner_id)
    if not banner:
        return JsonResult.error("横幅不存在", 404)
    # 处理轮播图数据中的图片URL
    banner_data = process_banner_images(banner.to_dict())
    return JsonResult.success(banner_data)


@banner_bp.route("", methods=['POST'])
def create_banner():
    form = validate_data(BannerCreateForm)

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
    return JsonResult.success(banner.to_dict(), "创建成功", 201)


@banner_bp.route("/<banner_id>", methods=['PUT'])
def update_banner(banner_id):
    banner = Banner.query.get(banner_id)
    if not banner:
        return JsonResult.error("横幅不存在", 404)

    form = validate_data(BannerUpdateForm)

    # 更新字段
    update_model_from_form(banner, form)

    db.session.commit()
    return JsonResult.success(banner.to_dict(), "更新成功")


@banner_bp.route("/<banner_id>", methods=['DELETE'])
def delete_banner(banner_id):
    banner = Banner.query.get(banner_id)
    if not banner:
        return JsonResult.error("横幅不存在", 404)

    db.session.delete(banner)
    db.session.commit()
    return JsonResult.success(None, "删除成功")
