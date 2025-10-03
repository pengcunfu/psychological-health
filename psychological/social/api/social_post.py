"""
社交帖子
"""
import uuid
from datetime import datetime, timedelta
from flask import Blueprint, request, g
from sqlalchemy import and_, or_, func
from psychological.models.social_post import SocialPost
from psychological.models.social_topic import SocialTopic
from psychological.models.social_follow import UserSocialStats
from psychological.models.user import User
from psychological.models.base import db
from psychological.form.social import SocialPostQueryForm, SocialPostCreateForm, SocialPostUpdateForm
from pcf_flask_helper.common import json_success, json_error
from psychological.utils.validate import validate_args
from psychological.utils.auth_helper import is_manager_user, assert_current_user_id

social_post_bp = Blueprint('social_post', __name__, url_prefix='/social-post')


@social_post_bp.route('', methods=['GET'])
def get_social_posts():
    """获取帖子列表"""
    form = validate_args(SocialPostQueryForm)
    current_user_id = assert_current_user_id()
    is_manager = is_manager_user()

    query = SocialPost.query

    # 权限过滤：普通用户只能看到已发布的帖子
    if not is_manager:
        query = query.filter(
            SocialPost.status == 'published',
            SocialPost.audit_status == 'approved'
        )

    # 搜索条件
    if form.user_id.data:
        query = query.filter(SocialPost.user_id == form.user_id.data)

    if form.category.data:
        query = query.filter(SocialPost.category == form.category.data)

    if form.status.data:
        query = query.filter(SocialPost.status == form.status.data)

    if form.audit_status.data:
        query = query.filter(SocialPost.audit_status == form.audit_status.data)

    if form.is_top.data is not None:
        query = query.filter(SocialPost.is_top == form.is_top.data)

    if form.is_featured.data is not None:
        query = query.filter(SocialPost.is_featured == form.is_featured.data)

    if form.topic.data:
        # 搜索包含特定话题的帖子
        query = query.filter(SocialPost._topics.like(f'%"{form.topic.data}"%'))

    if form.keyword.data:
        keyword = f'%{form.keyword.data}%'
        query = query.filter(
            or_(
                SocialPost.title.like(keyword),
                SocialPost.content.like(keyword)
            )
        )

    # 时间范围过滤
    if form.start_date.data:
        try:
            start_date = datetime.strptime(form.start_date.data, '%Y-%m-%d')
            query = query.filter(SocialPost.create_time >= start_date)
        except ValueError:
            pass

    if form.end_date.data:
        try:
            end_date = datetime.strptime(form.end_date.data, '%Y-%m-%d')
            query = query.filter(SocialPost.create_time <= end_date)
        except ValueError:
            pass

    # 排序
    sort_by = form.sort_by.data or 'create_time'
    sort_order = form.sort_order.data or 'desc'

    valid_sort_fields = {
        'create_time': SocialPost.create_time,
        'update_time': SocialPost.update_time,
        'hot_score': SocialPost.hot_score,
        'like_count': SocialPost.like_count,
        'comment_count': SocialPost.comment_count,
        'view_count': SocialPost.view_count
    }

    if sort_by in valid_sort_fields:
        sort_column = valid_sort_fields[sort_by]
        if sort_order.lower() == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

    # 置顶帖子优先
    query = query.order_by(SocialPost.is_top.desc())

    # 分页
    page = form.page.data or 1
    per_page = form.per_page.data or 10
    per_page = min(per_page, 50)

    pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    posts = []
    for post in pagination.items:
        post_data = post.to_list_dict()

        # 添加用户信息
        user = User.query.filter_by(id=post.user_id).first()
        if user and not post.is_anonymous:
            post_data['user_info'] = {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar
            }
        elif post.is_anonymous:
            post_data['user_info'] = {
                'id': 'anonymous',
                'username': '匿名用户',
                'avatar': None
            }

        # 检查当前用户是否点赞了这个帖子
        if current_user_id:
            from models.social_like import SocialLike
            like = SocialLike.query.filter_by(
                user_id=current_user_id,
                target_id=post.id,
                target_type='post',
                status='active'
            ).first()
            post_data['is_liked'] = bool(like)
        else:
            post_data['is_liked'] = False

        posts.append(post_data)

    return json_success({
        'list': posts,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })


@social_post_bp.route('/recommend', methods=['GET'])
def get_recommend_posts():
    """获取推荐帖子"""
    current_user_id = assert_current_user_id()
    limit = request.args.get('limit', 10, type=int)
    limit = min(limit, 20)

    # 基于热度评分的推荐算法
    query = SocialPost.query.filter(
        SocialPost.status == 'published',
        SocialPost.audit_status == 'approved'
    )

    # 如果用户已登录，可以基于用户行为进行个性化推荐
    if current_user_id:
        # 简单的推荐：最近7天的热门帖子
        week_ago = datetime.now() - timedelta(days=7)
        query = query.filter(SocialPost.create_time >= week_ago)

    posts = query.order_by(
        SocialPost.hot_score.desc(),
        SocialPost.create_time.desc()
    ).limit(limit).all()

    post_list = []
    for post in posts:
        post_data = post.to_list_dict()

        # 添加用户信息
        user = User.query.filter_by(id=post.user_id).first()
        if user and not post.is_anonymous:
            post_data['user_info'] = {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar
            }
        elif post.is_anonymous:
            post_data['user_info'] = {
                'id': 'anonymous',
                'username': '匿名用户',
                'avatar': None
            }

        post_list.append(post_data)

    return json_success(post_list)


@social_post_bp.route('/following', methods=['GET'])
def get_following_posts():
    """获取关注用户的帖子"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return json_error('用户未登录', 401)

    form = validate_args(SocialPostQueryForm)

    # 获取关注的用户ID列表
    from models.social_follow import SocialFollow
    following_users = db.session.query(SocialFollow.following_id).filter(
        SocialFollow.follower_id == current_user_id,
        SocialFollow.status == 'active'
    ).subquery()

    query = SocialPost.query.filter(
        SocialPost.user_id.in_(following_users),
        SocialPost.status == 'published',
        SocialPost.audit_status == 'approved'
    )

    # 分页
    page = form.page.data or 1
    per_page = form.per_page.data or 10
    per_page = min(per_page, 50)

    pagination = query.order_by(SocialPost.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    posts = []
    for post in pagination.items:
        post_data = post.to_list_dict()

        # 添加用户信息
        user = User.query.filter_by(id=post.user_id).first()
        if user:
            post_data['user_info'] = {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar
            }

        posts.append(post_data)

    return json_success({
        'list': posts,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })


@social_post_bp.route('/<post_id>', methods=['GET'])
def get_social_post_detail(post_id):
    """获取帖子详情"""
    current_user_id = assert_current_user_id()
    is_manager = is_manager_user()

    post = SocialPost.query.filter_by(id=post_id).first()
    if not post:
        return json_error('帖子不存在', 404)

    # 权限检查
    if not is_manager and (post.status != 'published' or post.audit_status != 'approved'):
        # 只有作者本人和管理员可以查看非发布状态的帖子
        if not current_user_id or post.user_id != current_user_id:
            return json_error('无权访问该帖子', 403)

    # 增加浏览次数（不是作者本人）
    if not current_user_id or post.user_id != current_user_id:
        post.increment_view()

        # 更新用户统计
        user_stats = UserSocialStats.query.filter_by(user_id=post.user_id).first()
        if user_stats:
            user_stats.add_view_count(1)

        # 更新热度评分
        post.update_hot_score()
        db.session.commit()

    post_data = post.to_dict()

    # 添加用户信息
    user = User.query.filter_by(id=post.user_id).first()
    if user and not post.is_anonymous:
        post_data['user_info'] = {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar
        }
    elif post.is_anonymous:
        post_data['user_info'] = {
            'id': 'anonymous',
            'username': '匿名用户',
            'avatar': None
        }

    # 检查当前用户是否点赞了这个帖子
    if current_user_id:
        from models.social_like import SocialLike
        like = SocialLike.query.filter_by(
            user_id=current_user_id,
            target_id=post.id,
            target_type='post',
            status='active'
        ).first()
        post_data['is_liked'] = bool(like)
    else:
        post_data['is_liked'] = False

    return json_success(post_data)


@social_post_bp.route('', methods=['POST'])
def create_social_post():
    """创建帖子"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return json_error('用户未登录', 401)

    form = validate_args(SocialPostCreateForm)

    try:
        post = SocialPost(
            id=str(uuid.uuid4()),
            user_id=current_user_id,
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            location=form.location.data,
            is_anonymous=form.is_anonymous.data or False,
            status='published' if not form.is_draft.data else 'draft'
        )

        # 设置话题
        if form.topics.data:
            post.topics = form.topics.data

            # 更新话题统计
            for topic_name in form.topics.data:
                topic = SocialTopic.query.filter_by(name=topic_name).first()
                if topic:
                    topic.post_count = (topic.post_count or 0) + 1
                    topic.participant_count = (topic.participant_count or 0) + 1

        # 设置图片和视频
        if form.images.data:
            post.images = form.images.data

        if form.videos.data:
            post.videos = form.videos.data

        db.session.add(post)

        # 更新用户统计
        user_stats = UserSocialStats.query.filter_by(user_id=current_user_id).first()
        if not user_stats:
            user_stats = UserSocialStats(
                id=str(uuid.uuid4()),
                user_id=current_user_id
            )
            db.session.add(user_stats)

        user_stats.increment_post()

        db.session.commit()

        return json_success(post.to_dict(), message='帖子发布成功')

    except Exception as e:
        db.session.rollback()
        return json_error(f'发布失败: {str(e)}')


@social_post_bp.route('/<post_id>', methods=['PUT'])
def update_social_post(post_id):
    """更新帖子"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return json_error('用户未登录', 401)

    form = validate_args(SocialPostUpdateForm)
    is_manager = is_manager_user()

    post = SocialPost.query.filter_by(id=post_id).first()
    if not post:
        return json_error('帖子不存在', 404)

    # 权限检查：只有作者本人和管理员可以编辑
    if post.user_id != current_user_id and not is_manager:
        return json_error('无权编辑该帖子', 403)

    try:
        # 更新字段
        if form.title.data is not None:
            post.title = form.title.data
        if form.content.data:
            post.content = form.content.data
        if form.category.data:
            post.category = form.category.data
        if form.location.data is not None:
            post.location = form.location.data

        # 只有管理员可以修改状态和特殊属性
        if is_manager:
            if form.status.data:
                post.status = form.status.data
            if form.is_top.data is not None:
                post.is_top = form.is_top.data
            if form.is_featured.data is not None:
                post.is_featured = form.is_featured.data
            if form.audit_status.data:
                post.audit_status = form.audit_status.data
                if form.audit_reason.data:
                    post.audit_reason = form.audit_reason.data
                    post.audited_by = current_user_id
                    post.audited_at = datetime.now()

        # 更新话题
        if form.topics.data is not None:
            old_topics = post.topics
            new_topics = form.topics.data

            # 更新话题统计
            for topic_name in old_topics:
                if topic_name not in new_topics:
                    topic = SocialTopic.query.filter_by(name=topic_name).first()
                    if topic:
                        topic.post_count = max((topic.post_count or 0) - 1, 0)

            for topic_name in new_topics:
                if topic_name not in old_topics:
                    topic = SocialTopic.query.filter_by(name=topic_name).first()
                    if topic:
                        topic.post_count = (topic.post_count or 0) + 1

            post.topics = new_topics

        # 更新媒体内容
        if form.images.data is not None:
            post.images = form.images.data
        if form.videos.data is not None:
            post.videos = form.videos.data

        db.session.commit()

        return json_success(post.to_dict(), message='帖子更新成功')

    except Exception as e:
        db.session.rollback()
        return json_error(f'更新失败: {str(e)}')


@social_post_bp.route('/<post_id>', methods=['DELETE'])
def delete_social_post(post_id):
    """删除帖子"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return json_error('用户未登录', 401)

    is_manager = is_manager_user()

    post = SocialPost.query.filter_by(id=post_id).first()
    if not post:
        return json_error('帖子不存在', 404)

    # 权限检查：只有作者本人和管理员可以删除
    if post.user_id != current_user_id and not is_manager:
        return json_error('无权删除该帖子', 403)

    try:
        # 更新话题统计
        for topic_name in post.topics:
            topic = SocialTopic.query.filter_by(name=topic_name).first()
            if topic:
                topic.post_count = max((topic.post_count or 0) - 1, 0)

        # 删除相关的评论和点赞
        from models.social_comment import SocialComment
        from models.social_like import SocialLike

        SocialComment.query.filter_by(post_id=post_id).delete()
        SocialLike.query.filter_by(target_id=post_id, target_type='post').delete()

        # 更新用户统计
        user_stats = UserSocialStats.query.filter_by(user_id=post.user_id).first()
        if user_stats:
            user_stats.decrement_post()

        # 删除帖子
        db.session.delete(post)
        db.session.commit()

        return json_success(message='帖子删除成功')

    except Exception as e:
        db.session.rollback()
        return json_error(f'删除失败: {str(e)}')


@social_post_bp.route('/my', methods=['GET'])
def get_my_posts():
    """获取我的帖子"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return json_error('用户未登录', 401)

    form = validate_args(SocialPostQueryForm)

    query = SocialPost.query.filter_by(user_id=current_user_id)

    # 状态筛选
    if form.status.data:
        query = query.filter(SocialPost.status == form.status.data)

    # 分页
    page = form.page.data or 1
    per_page = form.per_page.data or 10
    per_page = min(per_page, 50)

    pagination = query.order_by(SocialPost.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    posts = [post.to_list_dict() for post in pagination.items]

    return json_success({
        'list': posts,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })


@social_post_bp.route('/stats', methods=['GET'])
def get_post_stats():
    """获取帖子统计信息（仅管理员）"""
    if not is_manager_user():
        return json_error('权限不足', 403)

    try:
        # 总帖子数
        total_posts = SocialPost.query.count()

        # 各状态帖子数
        published_posts = SocialPost.query.filter_by(status='published').count()
        draft_posts = SocialPost.query.filter_by(status='draft').count()
        hidden_posts = SocialPost.query.filter_by(status='hidden').count()

        # 各审核状态帖子数
        pending_posts = SocialPost.query.filter_by(audit_status='pending').count()
        approved_posts = SocialPost.query.filter_by(audit_status='approved').count()
        rejected_posts = SocialPost.query.filter_by(audit_status='rejected').count()

        # 今日新增帖子
        today = datetime.now().date()
        today_posts = SocialPost.query.filter(
            func.date(SocialPost.create_time) == today
        ).count()

        # 热门帖子
        hot_post = SocialPost.query.filter_by(
            status='published',
            audit_status='approved'
        ).order_by(SocialPost.hot_score.desc()).first()

        return json_success({
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'hidden_posts': hidden_posts,
            'pending_posts': pending_posts,
            'approved_posts': approved_posts,
            'rejected_posts': rejected_posts,
            'today_posts': today_posts,
            'hot_post': hot_post.to_list_dict() if hot_post else None
        })

    except Exception as e:
        return json_error(f'获取统计信息失败: {str(e)}')
