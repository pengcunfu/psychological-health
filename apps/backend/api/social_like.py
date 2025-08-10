"""
社交点赞
"""
import uuid
from flask import Blueprint, request, g
from sqlalchemy import and_, or_
from models.social_like import SocialLike
from models.social_post import SocialPost
from models.social_comment import SocialComment
from models.social_follow import UserSocialStats
from models.base import db
from form.social import SocialLikeCreateForm
from utils.json_result import JsonResult
from utils.validate import validate_args
from utils.auth_helper import assert_current_user_id

social_like_bp = Blueprint('social_like', __name__, url_prefix='/social-like')


@social_like_bp.route('/toggle', methods=['POST'])
def toggle_like():
    """切换点赞状态"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return JsonResult.error('用户未登录', 401)
    
    form = validate_args(SocialLikeCreateForm)
    
    # 验证目标是否存在
    if form.target_type.data == 'post':
        target = SocialPost.query.filter_by(id=form.target_id.data).first()
        if not target:
            return JsonResult.error('帖子不存在', 404)
    elif form.target_type.data == 'comment':
        target = SocialComment.query.filter_by(id=form.target_id.data).first()
        if not target:
            return JsonResult.error('评论不存在', 404)
    else:
        return JsonResult.error('无效的点赞类型', 400)
    
    try:
        # 查找现有的点赞记录
        existing_like = SocialLike.query.filter_by(
            user_id=current_user_id,
            target_id=form.target_id.data,
            target_type=form.target_type.data
        ).first()
        
        if existing_like:
            if existing_like.is_active():
                # 取消点赞
                existing_like.cancel()
                
                # 更新目标统计
                if form.target_type.data == 'post':
                    target.decrement_like()
                    target.update_hot_score()
                    
                    # 更新被点赞用户的统计
                    user_stats = UserSocialStats.query.filter_by(user_id=target.user_id).first()
                    if user_stats:
                        user_stats.decrement_like_received()
                    
                    # 更新点赞用户的统计
                    liker_stats = UserSocialStats.query.filter_by(user_id=current_user_id).first()
                    if liker_stats:
                        liker_stats.decrement_like_given()
                        
                elif form.target_type.data == 'comment':
                    target.decrement_like()
                
                message = '取消点赞成功'
                is_liked = False
            else:
                # 重新激活点赞
                existing_like.reactivate()
                
                # 更新目标统计
                if form.target_type.data == 'post':
                    target.increment_like()
                    target.update_hot_score()
                    
                    # 更新被点赞用户的统计
                    user_stats = UserSocialStats.query.filter_by(user_id=target.user_id).first()
                    if user_stats:
                        user_stats.increment_like_received()
                    
                    # 更新点赞用户的统计
                    liker_stats = UserSocialStats.query.filter_by(user_id=current_user_id).first()
                    if liker_stats:
                        liker_stats.increment_like_given()
                        
                elif form.target_type.data == 'comment':
                    target.increment_like()
                
                message = '点赞成功'
                is_liked = True
        else:
            # 创建新的点赞记录
            new_like = SocialLike(
                id=str(uuid.uuid4()),
                user_id=current_user_id,
                target_id=form.target_id.data,
                target_type=form.target_type.data
            )
            db.session.add(new_like)
            
            # 更新目标统计
            if form.target_type.data == 'post':
                target.increment_like()
                target.update_hot_score()
                
                # 更新被点赞用户的统计
                user_stats = UserSocialStats.query.filter_by(user_id=target.user_id).first()
                if not user_stats:
                    user_stats = UserSocialStats(
                        id=str(uuid.uuid4()),
                        user_id=target.user_id
                    )
                    db.session.add(user_stats)
                user_stats.increment_like_received()
                
                # 更新点赞用户的统计
                liker_stats = UserSocialStats.query.filter_by(user_id=current_user_id).first()
                if not liker_stats:
                    liker_stats = UserSocialStats(
                        id=str(uuid.uuid4()),
                        user_id=current_user_id
                    )
                    db.session.add(liker_stats)
                liker_stats.increment_like_given()
                
            elif form.target_type.data == 'comment':
                target.increment_like()
            
            message = '点赞成功'
            is_liked = True
        
        db.session.commit()
        
        return JsonResult.success({
            'is_liked': is_liked,
            'like_count': target.like_count,
            'message': message
        })
    
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'操作失败: {str(e)}')


@social_like_bp.route('/check', methods=['POST'])
def check_like_status():
    """检查点赞状态"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return JsonResult.error('用户未登录', 401)
    
    form = validate_args(SocialLikeCreateForm)
    
    # 查找点赞记录
    like = SocialLike.query.filter_by(
        user_id=current_user_id,
        target_id=form.target_id.data,
        target_type=form.target_type.data,
        status='active'
    ).first()
    
    return JsonResult.success({
        'is_liked': bool(like),
        'like_id': like.id if like else None
    })


@social_like_bp.route('/my', methods=['GET'])
def get_my_likes():
    """获取我的点赞记录"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return JsonResult.error('用户未登录', 401)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    target_type = request.args.get('target_type')
    
    per_page = min(per_page, 100)
    
    query = SocialLike.query.filter_by(
        user_id=current_user_id,
        status='active'
    )
    
    if target_type:
        query = query.filter_by(target_type=target_type)
    
    pagination = query.order_by(SocialLike.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    likes = []
    for like in pagination.items:
        like_data = like.to_dict()
        
        # 添加目标信息
        if like.target_type == 'post':
            post = SocialPost.query.filter_by(id=like.target_id).first()
            if post:
                like_data['target_info'] = {
                    'id': post.id,
                    'title': post.title,
                    'content': post.content[:100] + '...' if len(post.content or '') > 100 else post.content,
                    'create_time': post.create_time.isoformat() if post.create_time else None
                }
        elif like.target_type == 'comment':
            comment = SocialComment.query.filter_by(id=like.target_id).first()
            if comment:
                like_data['target_info'] = {
                    'id': comment.id,
                    'content': comment.content[:100] + '...' if len(comment.content or '') > 100 else comment.content,
                    'post_id': comment.post_id,
                    'create_time': comment.create_time.isoformat() if comment.create_time else None
                }
        
        likes.append(like_data)
    
    return JsonResult.success({
        'list': likes,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })


@social_like_bp.route('/received', methods=['GET'])
def get_received_likes():
    """获取收到的点赞"""
    current_user_id = assert_current_user_id()
    if not current_user_id:
        return JsonResult.error('用户未登录', 401)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)
    
    # 获取我的帖子的点赞
    my_post_ids = db.session.query(SocialPost.id).filter_by(user_id=current_user_id).subquery()
    post_likes = SocialLike.query.filter(
        SocialLike.target_id.in_(my_post_ids),
        SocialLike.target_type == 'post',
        SocialLike.status == 'active'
    )
    
    # 获取我的评论的点赞
    my_comment_ids = db.session.query(SocialComment.id).filter_by(user_id=current_user_id).subquery()
    comment_likes = SocialLike.query.filter(
        SocialLike.target_id.in_(my_comment_ids),
        SocialLike.target_type == 'comment',
        SocialLike.status == 'active'
    )
    
    # 合并查询
    all_likes_query = post_likes.union(comment_likes)
    
    pagination = all_likes_query.order_by(SocialLike.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    likes = []
    for like in pagination.items:
        like_data = like.to_dict()
        
        # 添加点赞用户信息
        from models.user import User
        liker = User.query.filter_by(id=like.user_id).first()
        if liker:
            like_data['liker_info'] = {
                'id': liker.id,
                'username': liker.username,
                'avatar': liker.avatar
            }
        
        # 添加目标信息
        if like.target_type == 'post':
            post = SocialPost.query.filter_by(id=like.target_id).first()
            if post:
                like_data['target_info'] = {
                    'id': post.id,
                    'title': post.title,
                    'content': post.content[:100] + '...' if len(post.content or '') > 100 else post.content
                }
        elif like.target_type == 'comment':
            comment = SocialComment.query.filter_by(id=like.target_id).first()
            if comment:
                like_data['target_info'] = {
                    'id': comment.id,
                    'content': comment.content[:100] + '...' if len(comment.content or '') > 100 else comment.content,
                    'post_id': comment.post_id
                }
        
        likes.append(like_data)
    
    return JsonResult.success({
        'list': likes,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })


@social_like_bp.route('/target/<target_type>/<target_id>', methods=['GET'])
def get_target_likes(target_type, target_id):
    """获取特定目标的点赞列表"""
    if target_type not in ['post', 'comment']:
        return JsonResult.error('无效的目标类型', 400)
    
    # 验证目标是否存在
    if target_type == 'post':
        target = SocialPost.query.filter_by(id=target_id).first()
    else:
        target = SocialComment.query.filter_by(id=target_id).first()
    
    if not target:
        return JsonResult.error('目标不存在', 404)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)
    
    pagination = SocialLike.query.filter_by(
        target_id=target_id,
        target_type=target_type,
        status='active'
    ).order_by(SocialLike.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    likes = []
    for like in pagination.items:
        like_data = like.to_dict()
        
        # 添加用户信息
        from models.user import User
        user = User.query.filter_by(id=like.user_id).first()
        if user:
            like_data['user_info'] = {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar
            }
        
        likes.append(like_data)
    
    return JsonResult.success({
        'list': likes,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    }) 