import uuid
from flask import Blueprint, request, g
from sqlalchemy import and_, or_, func
from models.social_topic import SocialTopic
from models.base import db
from form.social import SocialTopicQueryForm, SocialTopicCreateForm, SocialTopicUpdateForm
from utils.json_result import JsonResult
from utils.validate import validate_args
from utils.auth_helper import is_manager_user, get_user_id

social_topic_bp = Blueprint('social_topic', __name__, url_prefix='/social-topic')


@social_topic_bp.route('', methods=['GET'])
def get_social_topics():
    """获取话题列表"""
    form = validate_args(SocialTopicQueryForm)
    
    query = SocialTopic.query
    
    # 搜索条件
    if form.name.data:
        query = query.filter(SocialTopic.name.like(f'%{form.name.data}%'))
    
    if form.status.data:
        query = query.filter(SocialTopic.status == form.status.data)
    else:
        # 默认只显示启用的话题
        query = query.filter(SocialTopic.status == 'active')
    
    if form.is_hot.data is not None:
        query = query.filter(SocialTopic.is_hot == form.is_hot.data)
    
    if form.is_featured.data is not None:
        query = query.filter(SocialTopic.is_featured == form.is_featured.data)
    
    if form.keyword.data:
        keyword = f'%{form.keyword.data}%'
        query = query.filter(
            or_(
                SocialTopic.name.like(keyword),
                SocialTopic.description.like(keyword)
            )
        )
    
    # 排序
    sort_by = form.sort_by.data or 'sort_order'
    sort_order = form.sort_order.data or 'desc'
    
    valid_sort_fields = {
        'sort_order': SocialTopic.sort_order,
        'post_count': SocialTopic.post_count,
        'participant_count': SocialTopic.participant_count,
        'view_count': SocialTopic.view_count,
        'create_time': SocialTopic.create_time,
        'update_time': SocialTopic.update_time
    }
    
    if sort_by in valid_sort_fields:
        sort_column = valid_sort_fields[sort_by]
        if sort_order.lower() == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    
    # 分页
    page = form.page.data or 1
    per_page = form.per_page.data or 20
    per_page = min(per_page, 100)
    
    pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    topics = []
    for topic in pagination.items:
        topic_data = topic.to_dict()
        topics.append(topic_data)
    
    return JsonResult.success({
        'list': topics,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    })


@social_topic_bp.route('/hot', methods=['GET'])
def get_hot_topics():
    """获取热门话题"""
    limit = request.args.get('limit', 10, type=int)
    limit = min(limit, 50)
    
    topics = SocialTopic.query.filter(
        SocialTopic.status == 'active',
        SocialTopic.is_hot == True
    ).order_by(
        SocialTopic.participant_count.desc(),
        SocialTopic.post_count.desc()
    ).limit(limit).all()
    
    topic_list = [topic.to_simple_dict() for topic in topics]
    
    return JsonResult.success(topic_list)


@social_topic_bp.route('/<topic_id>', methods=['GET'])
def get_social_topic_detail(topic_id):
    """获取话题详情"""
    topic = SocialTopic.query.filter_by(id=topic_id).first()
    if not topic:
        return JsonResult.error('话题不存在', 404)
    
    # 增加浏览次数
    topic.view_count = (topic.view_count or 0) + 1
    db.session.commit()
    
    return JsonResult.success(topic.to_dict())


@social_topic_bp.route('', methods=['POST'])
def create_social_topic():
    """创建话题（仅管理员）"""
    if not is_manager_user():
        return JsonResult.error('权限不足', 403)
    
    form = validate_args(SocialTopicCreateForm)
    current_user_id = get_user_id()
    
    # 检查话题名称是否已存在
    existing_topic = SocialTopic.query.filter_by(name=form.name.data).first()
    if existing_topic:
        return JsonResult.error('话题名称已存在')
    
    try:
        topic = SocialTopic(
            id=str(uuid.uuid4()),
            name=form.name.data,
            description=form.description.data,
            cover_image=form.cover_image.data,
            color=form.color.data or '#1890ff',
            sort_order=form.sort_order.data or 0,
            is_hot=form.is_hot.data or False,
            is_featured=form.is_featured.data or False,
            status=form.status.data or 'active',
            created_by=current_user_id
        )
        
        db.session.add(topic)
        db.session.commit()
        
        return JsonResult.success(topic.to_dict(), message='话题创建成功')
    
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'创建失败: {str(e)}')


@social_topic_bp.route('/<topic_id>', methods=['PUT'])
def update_social_topic(topic_id):
    """更新话题（仅管理员）"""
    if not is_manager_user():
        return JsonResult.error('权限不足', 403)
    
    form = validate_args(SocialTopicUpdateForm)
    
    topic = SocialTopic.query.filter_by(id=topic_id).first()
    if not topic:
        return JsonResult.error('话题不存在', 404)
    
    # 检查话题名称是否与其他话题重复
    if form.name.data and form.name.data != topic.name:
        existing_topic = SocialTopic.query.filter(
            SocialTopic.name == form.name.data,
            SocialTopic.id != topic_id
        ).first()
        if existing_topic:
            return JsonResult.error('话题名称已存在')
    
    try:
        # 更新字段
        if form.name.data:
            topic.name = form.name.data
        if form.description.data is not None:
            topic.description = form.description.data
        if form.cover_image.data is not None:
            topic.cover_image = form.cover_image.data
        if form.color.data:
            topic.color = form.color.data
        if form.sort_order.data is not None:
            topic.sort_order = form.sort_order.data
        if form.is_hot.data is not None:
            topic.is_hot = form.is_hot.data
        if form.is_featured.data is not None:
            topic.is_featured = form.is_featured.data
        if form.status.data:
            topic.status = form.status.data
        
        db.session.commit()
        
        return JsonResult.success(topic.to_dict(), message='话题更新成功')
    
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'更新失败: {str(e)}')


@social_topic_bp.route('/<topic_id>', methods=['DELETE'])
def delete_social_topic(topic_id):
    """删除话题（仅管理员）"""
    if not is_manager_user():
        return JsonResult.error('权限不足', 403)
    
    topic = SocialTopic.query.filter_by(id=topic_id).first()
    if not topic:
        return JsonResult.error('话题不存在', 404)
    
    # 检查是否有关联的帖子
    if topic.post_count > 0:
        return JsonResult.error('该话题下还有帖子，无法删除')
    
    try:
        db.session.delete(topic)
        db.session.commit()
        
        return JsonResult.success(message='话题删除成功')
    
    except Exception as e:
        db.session.rollback()
        return JsonResult.error(f'删除失败: {str(e)}')


@social_topic_bp.route('/stats', methods=['GET'])
def get_topic_stats():
    """获取话题统计信息（仅管理员）"""
    if not is_manager_user():
        return JsonResult.error('权限不足', 403)
    
    try:
        # 总话题数
        total_topics = SocialTopic.query.count()
        
        # 活跃话题数
        active_topics = SocialTopic.query.filter_by(status='active').count()
        
        # 热门话题数
        hot_topics = SocialTopic.query.filter_by(is_hot=True).count()
        
        # 精选话题数
        featured_topics = SocialTopic.query.filter_by(is_featured=True).count()
        
        # 最热门的话题
        top_topic = SocialTopic.query.filter_by(status='active').order_by(
            SocialTopic.participant_count.desc()
        ).first()
        
        return JsonResult.success({
            'total_topics': total_topics,
            'active_topics': active_topics,
            'hot_topics': hot_topics,
            'featured_topics': featured_topics,
            'top_topic': top_topic.to_simple_dict() if top_topic else None
        })
    
    except Exception as e:
        return JsonResult.error(f'获取统计信息失败: {str(e)}') 