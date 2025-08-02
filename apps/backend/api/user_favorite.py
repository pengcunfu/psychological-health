"""
用户收藏API
提供用户收藏功能的管理

接口列表：
- GET /user-favorite - 获取收藏列表
- GET /user-favorite/<favorite_id> - 获取单个收藏详情
- POST /user-favorite - 创建收藏
- DELETE /user-favorite/<favorite_id> - 删除收藏
- GET /user-favorite/user/<user_id> - 获取用户的收藏列表
- GET /user-favorite/check - 检查是否已收藏
"""
import uuid

from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError

from models.user_favorite import UserFavorite
from models.base import db
from utils.json_result import JsonResult
from form.user_favorite import UserFavoriteCreateForm, UserFavoriteQueryForm

user_favorite_bp = Blueprint('user_favorite', __name__, url_prefix='/user-favorite')


@user_favorite_bp.route('', methods=['GET'])
def get_user_favorites():
    """获取用户收藏列表"""
    # 获取查询参数
    form = UserFavoriteQueryForm(data=request.args)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 构建查询
    query = UserFavorite.query

    if form.get_user_id():
        query = query.filter(UserFavorite.user_id == form.get_user_id())
    if form.get_item_type():
        query = query.filter(UserFavorite.item_type == form.get_item_type())
    if form.get_item_id():
        query = query.filter(UserFavorite.item_id == form.get_item_id())

    # 分页查询
    pagination = query.order_by(UserFavorite.create_time.desc()).paginate(
        page=form.get_page(), per_page=form.get_per_page(), error_out=False
    )

    favorites = [favorite.to_dict() for favorite in pagination.items]

    return JsonResult.success({
        'favorites': favorites,
        'total': pagination.total,
        'page': form.get_page(),
        'per_page': form.get_per_page(),
        'pages': pagination.pages
    })


@user_favorite_bp.route('/<favorite_id>', methods=['GET'])
def get_user_favorite(favorite_id):
    """获取单个用户收藏详情"""
    favorite = UserFavorite.query.filter_by(id=favorite_id).first()
    if not favorite:
        return JsonResult.error('收藏不存在', 404)

    return JsonResult.success(favorite.to_dict())


@user_favorite_bp.route('', methods=['POST'])
def create_user_favorite():
    """创建用户收藏"""
    data = request.get_json()
    form = UserFavoriteCreateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 检查是否已经收藏
    existing_favorite = UserFavorite.query.filter(
        UserFavorite.user_id == form.user_id.data,
        UserFavorite.item_id == form.item_id.data,
        UserFavorite.item_type == form.item_type.data
    ).first()

    if existing_favorite:
        return JsonResult.error('已经收藏过该项目', 400)

    # 创建收藏
    favorite = UserFavorite(
        id=str(uuid.uuid4()),
        user_id=form.user_id.data,
        item_id=form.item_id.data,
        item_type=form.item_type.data
    )

    db.session.add(favorite)
    db.session.commit()

    return JsonResult.success(favorite.to_dict(), '收藏创建成功', 201)


@user_favorite_bp.route('/<favorite_id>', methods=['DELETE'])
def delete_user_favorite(favorite_id):
    """删除用户收藏"""
    favorite = UserFavorite.query.filter_by(id=favorite_id).first()
    if not favorite:
        return JsonResult.error('收藏不存在', 404)

    db.session.delete(favorite)
    db.session.commit()

    return JsonResult.success(None, '收藏删除成功')


@user_favorite_bp.route('/check', methods=['POST'])
def check_user_favorite():
    """检查是否已收藏"""
    data = request.get_json()
    form = UserFavoriteCreateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 检查是否已收藏
    favorite = UserFavorite.query.filter(
        UserFavorite.user_id == form.user_id.data,
        UserFavorite.item_id == form.item_id.data,
        UserFavorite.item_type == form.item_type.data
    ).first()

    is_favorited = favorite is not None
    result = {
        'is_favorited': is_favorited,
        'favorite_id': favorite.id if favorite else None
    }

    return JsonResult.success(result)


@user_favorite_bp.route('/toggle', methods=['POST'])
def toggle_user_favorite():
    """切换收藏状态"""
    data = request.get_json()
    form = UserFavoriteCreateForm(data=data)
    if not form.validate():
        return JsonResult.error(f'参数验证失败: {form.get_first_error()}', 400)

    # 检查是否已收藏
    favorite = UserFavorite.query.filter(
        UserFavorite.user_id == form.user_id.data,
        UserFavorite.item_id == form.item_id.data,
        UserFavorite.item_type == form.item_type.data
    ).first()

    if favorite:
        # 已收藏，删除收藏
        db.session.delete(favorite)
        db.session.commit()
        return JsonResult.success({
            'is_favorited': False,
            'message': '取消收藏成功'
        })
    else:
        # 未收藏，添加收藏
        new_favorite = UserFavorite(
            id=str(uuid.uuid4()),
            user_id=form.user_id.data,
            item_id=form.item_id.data,
            item_type=form.item_type.data
        )

        db.session.add(new_favorite)
        db.session.commit()

        return JsonResult.success({
            'is_favorited': True,
            'favorite_id': new_favorite.id,
            'message': '收藏成功'
        })
