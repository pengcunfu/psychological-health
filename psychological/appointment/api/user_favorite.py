"""
用户收藏API
提供用户收藏功能的管理
"""
import uuid

from flask import Blueprint
from ..models import UserFavorite
from pcf_flask_helper.model.base import db
from pcf_flask_helper.common import json_success
from pcf_flask_helper.form.validate import assert_id_exists
from pcf_flask_helper.model.query import create_query_builder, assert_exists, assert_not_exists
from psychological.utils.auth_helper import assert_current_user_id
from ..form import UserFavoriteCreateForm, UserFavoriteQueryForm
from psychological.decorator.form import validate_form
from psychological.decorator.permission import role_required, permission_required

user_favorite_bp = Blueprint('user_favorite', __name__, url_prefix='/user-favorite')


@user_favorite_bp.route('', methods=['GET'])
@validate_form(UserFavoriteQueryForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("user_favorite:get_user_favorites")
def get_user_favorites(form):
    """获取用户收藏列表"""
    current_user_id = assert_current_user_id()
    
    # 使用QueryBuilder构建查询并分页
    result = create_query_builder(UserFavorite) \
        .filter(UserFavorite.user_id == current_user_id) \
        .when(form.item_type.data, UserFavorite.item_type == form.item_type.data) \
        .when(form.item_id.data, UserFavorite.item_id == form.item_id.data) \
        .order_by(UserFavorite.create_time.desc()) \
        .paginate(form.page.data or 1, form.per_page.data or 10, 100)

    return json_success({
        'favorites': [favorite.to_dict() for favorite in result['items']],
        'total': result['total'],
        'page': result['page'],
        'per_page': result['per_page'],
        'pages': result['pages']
    })


@user_favorite_bp.route('/<favorite_id>', methods=['GET'])
@role_required(['admin', 'manager', 'user'])
@permission_required("user_favorite:get_user_favorite")
def get_user_favorite(favorite_id):
    """获取单个用户收藏详情"""
    assert_id_exists(favorite_id, "收藏ID不能为空")
    current_user_id = assert_current_user_id()

    favorite = assert_exists(
        UserFavorite, 
        [UserFavorite.id == favorite_id, UserFavorite.user_id == current_user_id],
        "收藏不存在或无权限访问"
    )

    return json_success(favorite.to_dict())


@user_favorite_bp.route('', methods=['POST'])
@validate_form(UserFavoriteCreateForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("user_favorite:create_user_favorite")
def create_user_favorite(form):
    """创建用户收藏"""
    current_user_id = assert_current_user_id()
    
    # 检查是否已经收藏
    assert_not_exists(
        UserFavorite,
        [UserFavorite.user_id == current_user_id,
         UserFavorite.item_id == form.item_id.data,
         UserFavorite.item_type == form.item_type.data],
        "已经收藏过该项目"
    )

    # 创建收藏
    favorite = UserFavorite(
        id=str(uuid.uuid4()),
        user_id=current_user_id,
        item_id=form.item_id.data,
        item_type=form.item_type.data
    )

    db.session.add(favorite)
    db.session.commit()

    return json_success(favorite.to_dict(), '收藏创建成功', 201)


@user_favorite_bp.route('/<favorite_id>', methods=['DELETE'])
@role_required(['admin', 'manager', 'user'])
@permission_required("user_favorite:delete_user_favorite")
def delete_user_favorite(favorite_id):
    """删除用户收藏"""
    assert_id_exists(favorite_id, "收藏ID不能为空")
    current_user_id = assert_current_user_id()

    favorite = assert_exists(
        UserFavorite,
        [UserFavorite.id == favorite_id, UserFavorite.user_id == current_user_id],
        "收藏不存在或无权限访问"
    )

    db.session.delete(favorite)
    db.session.commit()

    return json_success(None, '收藏删除成功')


@user_favorite_bp.route('/check', methods=['POST'])
@validate_form(UserFavoriteCreateForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("user_favorite:check_user_favorite")
def check_user_favorite(form):
    """检查是否已收藏"""
    current_user_id = assert_current_user_id()
    
    # 检查是否已收藏
    favorite = create_query_builder(UserFavorite) \
        .filter(
        UserFavorite.user_id == current_user_id,
        UserFavorite.item_id == form.item_id.data,
        UserFavorite.item_type == form.item_type.data
    ) \
        .first()

    is_favorited = favorite is not None
    result = {
        'is_favorited': is_favorited,
        'favorite_id': favorite.id if favorite else None
    }

    return json_success(result)


@user_favorite_bp.route('/toggle', methods=['POST'])
@validate_form(UserFavoriteCreateForm)
@role_required(['admin', 'manager', 'user'])
@permission_required("user_favorite:toggle_user_favorite")
def toggle_user_favorite(form):
    """切换收藏状态"""
    current_user_id = assert_current_user_id()
    
    # 检查是否已收藏
    favorite = create_query_builder(UserFavorite) \
        .filter(
        UserFavorite.user_id == current_user_id,
        UserFavorite.item_id == form.item_id.data,
        UserFavorite.item_type == form.item_type.data
    ) \
        .first()

    if favorite:
        # 已收藏，删除收藏
        db.session.delete(favorite)
        db.session.commit()
        return json_success({
            'is_favorited': False,
            'message': '取消收藏成功'
        })
    else:
        # 未收藏，添加收藏
        new_favorite = UserFavorite(
            id=str(uuid.uuid4()),
            user_id=current_user_id,
            item_id=form.item_id.data,
            item_type=form.item_type.data
        )

        db.session.add(new_favorite)
        db.session.commit()

        return json_success({
            'is_favorited': True,
            'favorite_id': new_favorite.id,
            'message': '收藏成功'
        })
