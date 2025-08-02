from flask import Blueprint, request
from models.banner import Banner
from form.banner import BannerQueryForm, BannerCreateForm, BannerUpdateForm
from sqlalchemy.exc import SQLAlchemyError
from utils.json_result import JsonResult
from models.base import db

banner_bp = Blueprint("banner", __name__, url_prefix="/banner")


@banner_bp.route("", methods=['GET'])
def get_banners():
    form = BannerQueryForm(data=request.args)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    page = form.page.data
    per_page = form.per_page.data
    title = form.title.data

    query = Banner.query
    if title:
        query = query.filter(Banner.title.like(f'%{title}%'))

    paginate = query.paginate(page=page, per_page=per_page, error_out=False)
    banners = paginate.items

    return JsonResult.success({
        'list': [banner.to_dict() for banner in banners],
        'total_pages': paginate.pages,
        'total_items': paginate.total,
        'page': page,
        'per_page': per_page
    })


@banner_bp.route("/<banner_id>", methods=['GET'])
def get_banner(banner_id):
    banner = Banner.query.get(banner_id)
    if not banner:
        return JsonResult.error("Banner not found", 404)
    return JsonResult.success(banner.to_dict())


@banner_bp.route("", methods=['POST'])
def create_banner():
    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    form = BannerCreateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    title = form.title.data
    image_url = form.image_url.data
    link_url = form.link_url.data
    sort_order = form.sort_order.data if form.sort_order.data is not None else 0

    banner = Banner(
        title=title,
        image_url=image_url,
        link_url=link_url,
        sort_order=sort_order,
    )
    db.session.add(banner)
    db.session.commit()
    return JsonResult.success(banner.to_dict(), "创建成功", 201)


@banner_bp.route("/<banner_id>", methods=['PUT'])
def update_banner(banner_id):
    banner = Banner.query.get(banner_id)
    if not banner:
        return JsonResult.error("Banner not found", 404)

    data = request.get_json()
    if not data:
        return JsonResult.error('请求数据不能为空', 400)

    form = BannerUpdateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    if form.title.data is not None:
        banner.title = form.title.data
    if form.image_url.data is not None:
        banner.image_url = form.image_url.data
    if form.link_url.data is not None:
        banner.link_url = form.link_url.data
    if form.sort_order.data is not None:
        banner.sort_order = form.sort_order.data

    db.session.commit()
    return JsonResult.success(banner.to_dict(), "更新成功")


@banner_bp.route("/<banner_id>", methods=['DELETE'])
def delete_banner(banner_id):
    banner = Banner.query.get(banner_id)
    if not banner:
        return JsonResult.error("Banner not found", 404)

    db.session.delete(banner)
    db.session.commit()
    return JsonResult.success(None, "删除成功")
