"""
社交关注
"""
import uuid
from flask import Blueprint, request
from ..models import SocialFollow, UserSocialStats
from psychological.system.models import User
from pcf_flask_helper.model.base import db
from ..form import SocialFollowCreateForm
from pcf_flask_helper.common import json_success, json_error
from pcf_flask_helper.form.validate import validate_args
from psychological.utils.auth_helper import assert_current_user_id

social_follow_bp = Blueprint('social_follow', __name__, url_prefix='/social-follow')


@social_follow_bp.route('/toggle', methods=['POST'])
def toggle_follow():
    """切换关注状态"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return json_error('用户未登录', 401)

    form = validate_args(SocialFollowCreateForm)

    # 不能关注自己
    if current_user_id == form.following_id.data:
        return json_error('不能关注自己', 400)

    # 验证被关注用户是否存在
    following_user = User.query.filter_by(id=form.following_id.data).first()
    if not following_user:
        return json_error('用户不存在', 404)

    try:
        # 查找现有关注记录
        existing_follow = SocialFollow.query.filter_by(
            follower_id=current_user_id,
            following_id=form.following_id.data
        ).first()

        if existing_follow:
            if existing_follow.is_active():
                # 取消关注
                existing_follow.cancel()

                # 更新统计
                follower_stats = UserSocialStats.query.filter_by(user_id=current_user_id).first()
                if follower_stats:
                    follower_stats.decrement_following()

                following_stats = UserSocialStats.query.filter_by(user_id=form.following_id.data).first()
                if following_stats:
                    following_stats.decrement_follower()

                message = '取消关注成功'
                is_following = False
            else:
                # 重新关注
                existing_follow.reactivate()

                # 更新统计
                follower_stats = UserSocialStats.query.filter_by(user_id=current_user_id).first()
                if not follower_stats:
                    follower_stats = UserSocialStats(
                        id=str(uuid.uuid4()),
                        user_id=current_user_id
                    )
                    db.session.add(follower_stats)
                follower_stats.increment_following()

                following_stats = UserSocialStats.query.filter_by(user_id=form.following_id.data).first()
                if not following_stats:
                    following_stats = UserSocialStats(
                        id=str(uuid.uuid4()),
                        user_id=form.following_id.data
                    )
                    db.session.add(following_stats)
                following_stats.increment_follower()

                message = '关注成功'
                is_following = True
        else:
            # 创建新关注记录
            new_follow = SocialFollow(
                id=str(uuid.uuid4()),
                follower_id=current_user_id,
                following_id=form.following_id.data,
                source=form.source.data
            )
            db.session.add(new_follow)

            # 更新统计
            follower_stats = UserSocialStats.query.filter_by(user_id=current_user_id).first()
            if not follower_stats:
                follower_stats = UserSocialStats(
                    id=str(uuid.uuid4()),
                    user_id=current_user_id
                )
                db.session.add(follower_stats)
            follower_stats.increment_following()

            following_stats = UserSocialStats.query.filter_by(user_id=form.following_id.data).first()
            if not following_stats:
                following_stats = UserSocialStats(
                    id=str(uuid.uuid4()),
                    user_id=form.following_id.data
                )
                db.session.add(following_stats)
            following_stats.increment_follower()

            message = '关注成功'
            is_following = True

        db.session.commit()

        return json_success({
            'is_following': is_following,
            'message': message
        })

    except Exception as e:
        db.session.rollback()
        return json_error(f'操作失败: {str(e)}')


@social_follow_bp.route('/check', methods=['POST'])
def check_follow_status():
    """检查关注状态"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return json_error('用户未登录', 401)

    form = validate_args(SocialFollowCreateForm)

    follow = SocialFollow.query.filter_by(
        follower_id=current_user_id,
        following_id=form.following_id.data,
        status='active'
    ).first()

    return json_success({
        'is_following': bool(follow),
        'follow_id': follow.id if follow else None
    })


@social_follow_bp.route('/followers', methods=['GET'])
def get_followers():
    """获取粉丝列表"""
    current_user_id = assert_current_user_id()
    user_id = request.args.get('user_id', current_user_id)

    if not user_id:
        return json_error('用户ID不能为空', 400)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)

    pagination = SocialFollow.query.filter_by(
        following_id=user_id,
        status='active'
    ).order_by(SocialFollow.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    followers = []
    for follow in pagination.items:
        follow_data = follow.to_dict()

        # 添加粉丝用户信息
        user = User.query.filter_by(id=follow.follower_id).first()
        if user:
            user_dict = user.to_dict()
            follow_data['user_info'] = {
                'id': user_dict['id'],
                'username': user_dict['username'],
                'avatar': user_dict['avatar']
            }

        followers.append(follow_data)

    return json_success({
        'list': followers,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })


@social_follow_bp.route('/following', methods=['GET'])
def get_following():
    """获取关注列表"""
    current_user_id = assert_current_user_id()
    user_id = request.args.get('user_id', current_user_id)

    if not user_id:
        return json_error('用户ID不能为空', 400)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)

    pagination = SocialFollow.query.filter_by(
        follower_id=user_id,
        status='active'
    ).order_by(SocialFollow.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    following = []
    for follow in pagination.items:
        follow_data = follow.to_dict()

        # 添加被关注用户信息
        user = User.query.filter_by(id=follow.following_id).first()
        if user:
            user_dict = user.to_dict()
            follow_data['user_info'] = {
                'id': user_dict['id'],
                'username': user_dict['username'],
                'avatar': user_dict['avatar']
            }

        following.append(follow_data)

    return json_success({
        'list': following,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })


@social_follow_bp.route('/stats/<user_id>', methods=['GET'])
def get_user_social_stats(user_id):
    """获取用户社区统计"""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json_error('用户不存在', 404)

    stats = UserSocialStats.query.filter_by(user_id=user_id).first()
    if not stats:
        # 创建默认统计记录
        stats = UserSocialStats(
            id=str(uuid.uuid4()),
            user_id=user_id
        )
        db.session.add(stats)
        db.session.commit()

    stats_data = stats.to_dict()
    user_dict = user.to_dict()
    stats_data['user_info'] = {
        'id': user_dict['id'],
        'username': user_dict['username'],
        'avatar': user_dict['avatar']
    }

    return json_success(stats_data)
