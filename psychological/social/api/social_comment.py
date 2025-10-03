"""
社交评论
"""
import uuid
from flask import Blueprint

from psychological.system.models import User
from pcf_flask_helper.model.base import db
from pcf_flask_helper.common import json_success, json_error
from pcf_flask_helper.form.validate import validate_args
from psychological.utils.auth_helper import is_manager_user, assert_current_user_id

from ..models import SocialComment, SocialPost, UserSocialStats, SocialLike
from ..form import SocialCommentQueryForm, SocialCommentCreateForm

social_comment_bp = Blueprint('social_comment', __name__, url_prefix='/social-comment')


@social_comment_bp.route('', methods=['GET'])
def get_social_comments():
    """获取评论列表"""
    form = validate_args(SocialCommentQueryForm)

    query = SocialComment.query

    # 普通用户只能看到已发布的评论
    if not is_manager_user():
        query = query.filter(
            SocialComment.status == 'published',
            SocialComment.audit_status == 'approved'
        )

    # 搜索条件
    if form.post_id.data:
        query = query.filter(SocialComment.post_id == form.post_id.data)

    if form.user_id.data:
        query = query.filter(SocialComment.user_id == form.user_id.data)

    if form.parent_id.data:
        query = query.filter(SocialComment.parent_id == form.parent_id.data)

    if form.status.data:
        query = query.filter(SocialComment.status == form.status.data)

    if form.audit_status.data:
        query = query.filter(SocialComment.audit_status == form.audit_status.data)

    if form.keyword.data:
        keyword = f'%{form.keyword.data}%'
        query = query.filter(SocialComment.content.like(keyword))

    # 排序
    sort_by = form.sort_by.data or 'create_time'
    if sort_by == 'create_time':
        if form.sort_order.data == 'asc':
            query = query.order_by(SocialComment.create_time.asc())
        else:
            query = query.order_by(SocialComment.create_time.desc())

    # 分页
    page = form.page.data or 1
    per_page = form.per_page.data or 20
    per_page = min(per_page, 100)

    pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    comments = []
    for comment in pagination.items:
        comment_data = comment.to_dict()

        # 添加用户信息
        if not comment.is_anonymous:
            user = User.query.filter_by(id=comment.user_id).first()
            if user:
                comment_data['user_info'] = {
                    'id': user.id,
                    'username': user.username,
                    'avatar': user.avatar
                }
        else:
            comment_data['user_info'] = {
                'id': 'anonymous',
                'username': '匿名用户',
                'avatar': None
            }

        comments.append(comment_data)

    return json_success({
        'list': comments,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })


@social_comment_bp.route('', methods=['POST'])
def create_social_comment():
    """创建评论"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return json_error('用户未登录', 401)

    form = validate_args(SocialCommentCreateForm)

    # 验证帖子是否存在
    post = SocialPost.query.filter_by(id=form.post_id.data).first()
    if not post:
        return json_error('帖子不存在', 404)

    # 如果是回复评论，验证父评论是否存在
    if form.parent_id.data:
        parent_comment = SocialComment.query.filter_by(id=form.parent_id.data).first()
        if not parent_comment:
            return json_error('父评论不存在', 404)

    try:
        comment = SocialComment(
            id=str(uuid.uuid4()),
            post_id=form.post_id.data,
            user_id=current_user_id,
            parent_id=form.parent_id.data,
            reply_to_user_id=form.reply_to_user_id.data,
            content=form.content.data,
            location=form.location.data,
            is_anonymous=form.is_anonymous.data or False
        )

        if form.images.data:
            comment.images = form.images.data

        db.session.add(comment)

        # 更新帖子评论数
        post.increment_comment()

        # 更新父评论回复数
        if form.parent_id.data:
            parent_comment.increment_reply()

        # 更新用户统计
        user_stats = UserSocialStats.query.filter_by(user_id=current_user_id).first()
        if not user_stats:
            user_stats = UserSocialStats(
                id=str(uuid.uuid4()),
                user_id=current_user_id
            )
            db.session.add(user_stats)
        user_stats.increment_comment()

        db.session.commit()

        return json_success(comment.to_dict(), message='评论发布成功')

    except Exception as e:
        db.session.rollback()
        return json_error(f'发布失败: {str(e)}')


@social_comment_bp.route('/<comment_id>', methods=['DELETE'])
def delete_social_comment(comment_id):
    """删除评论"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return json_error('用户未登录', 401)

    comment = SocialComment.query.filter_by(id=comment_id).first()
    if not comment:
        return json_error('评论不存在', 404)

    # 权限检查
    if comment.user_id != current_user_id and not is_manager_user():
        return json_error('无权删除该评论', 403)

    try:
        # 更新帖子评论数
        post = SocialPost.query.filter_by(id=comment.post_id).first()
        if post:
            post.decrement_comment()

        # 更新父评论回复数
        if comment.parent_id:
            parent_comment = SocialComment.query.filter_by(id=comment.parent_id).first()
            if parent_comment:
                parent_comment.decrement_reply()

        # 删除相关点赞
        SocialLike.query.filter_by(target_id=comment_id, target_type='comment').delete()

        # 更新用户统计
        user_stats = UserSocialStats.query.filter_by(user_id=comment.user_id).first()
        if user_stats:
            user_stats.decrement_comment()

        db.session.delete(comment)
        db.session.commit()

        return json_success(message='评论删除成功')

    except Exception as e:
        db.session.rollback()
        return json_error(f'删除失败: {str(e)}')
