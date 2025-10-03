"""
通知系统数据库迁移脚本
"""
from sqlalchemy import text
from pcf_flask_helper.model.base import db
from loguru import logger
from .models import Notification, NotificationTemplate, NotificationConfig
from .config import NOTIFICATION_TEMPLATES
from .types import NotificationType, NotificationPriority, NotificationAction




def create_notification_tables():
    """创建通知相关数据表"""
    try:
        # 创建表结构
        db.create_all()
        
        # 创建索引（如果数据库不支持自动创建）
        db.session.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_recipient_status_time 
        ON notifications (recipient_id, status, create_time);
        """))
        
        db.session.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_type_priority_time 
        ON notifications (type, priority, create_time);
        """))
        
        db.session.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_related_object 
        ON notifications (related_type, related_id);
        """))
        
        db.session.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_scheduled_time 
        ON notifications (scheduled_time);
        """))
        
        db.session.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_user_type 
        ON notification_configs (user_id, type);
        """))
        
        db.session.commit()
        logger.info("通知系统数据表创建成功")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"创建通知系统数据表失败: {str(e)}")
        raise


def init_notification_templates():
    """初始化通知模板数据"""
    try:
        # 检查是否已有模板数据
        existing_count = db.session.query(NotificationTemplate).count()
        if existing_count > 0:
            logger.info(f"通知模板已存在 {existing_count} 条，跳过初始化")
            return
        
        # 插入预定义模板
        template_count = 0
        for template_code, template_config in NOTIFICATION_TEMPLATES.items():
            try:
                template = NotificationTemplate(
                    name=template_config['name'],
                    code=template_code,
                    description=f"系统预定义模板: {template_config['name']}",
                    title_template=template_config['title_template'],
                    content_template=template_config['content_template'],
                    summary_template=template_config.get('summary_template', ''),
                    type=NotificationType(template_config['type']),
                    priority=NotificationPriority.NORMAL,
                    action_type=NotificationAction(template_config.get('action_type', 'none')),
                    action_url_template=template_config.get('action_url_template', ''),
                    icon=template_config.get('icon', '📢'),
                    color=template_config.get('color', '#3B82F6'),
                    is_active=True,
                    version='1.0'
                )
                
                db.session.add(template)
                template_count += 1
                
            except Exception as e:
                logger.error(f"创建模板 {template_code} 失败: {str(e)}")
        
        db.session.commit()
        logger.info(f"成功初始化 {template_count} 个通知模板")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"初始化通知模板失败: {str(e)}")
        raise


def migrate_notification_system():
    """完整的通知系统迁移"""
    try:
        logger.info("开始通知系统数据库迁移...")
        
        # 1. 创建数据表
        create_notification_tables()
        
        # 2. 初始化模板数据
        init_notification_templates()
        
        logger.info("通知系统数据库迁移完成")
        
    except Exception as e:
        logger.error(f"通知系统数据库迁移失败: {str(e)}")
        raise


def cleanup_notification_data():
    """清理通知数据（危险操作，慎用）"""
    try:
        logger.warning("开始清理通知数据...")
        
        # 删除所有通知
        db.session.query(Notification).delete()
        
        # 删除用户配置
        db.session.query(NotificationConfig).delete()
        
        # 删除自定义模板（保留系统模板）
        db.session.query(NotificationTemplate).filter(
            ~NotificationTemplate.code.in_(list(NOTIFICATION_TEMPLATES.keys()))
        ).delete()
        
        db.session.commit()
        logger.info("通知数据清理完成")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"清理通知数据失败: {str(e)}")
        raise


def update_notification_templates():
    """更新通知模板（用于版本升级）"""
    try:
        logger.info("开始更新通知模板...")
        
        updated_count = 0
        for template_code, template_config in NOTIFICATION_TEMPLATES.items():
            template = db.session.query(NotificationTemplate).filter_by(
                code=template_code
            ).first()
            
            if template:
                # 更新现有模板
                template.name = template_config['name']
                template.title_template = template_config['title_template']
                template.content_template = template_config['content_template']
                template.summary_template = template_config.get('summary_template', '')
                template.type = NotificationType(template_config['type'])
                template.action_type = NotificationAction(template_config.get('action_type', 'none'))
                template.action_url_template = template_config.get('action_url_template', '')
                template.icon = template_config.get('icon', '📢')
                template.color = template_config.get('color', '#3B82F6')
                updated_count += 1
            else:
                # 创建新模板
                template = NotificationTemplate(
                    name=template_config['name'],
                    code=template_code,
                    description=f"系统预定义模板: {template_config['name']}",
                    title_template=template_config['title_template'],
                    content_template=template_config['content_template'],
                    summary_template=template_config.get('summary_template', ''),
                    type=NotificationType(template_config['type']),
                    priority=NotificationPriority.NORMAL,
                    action_type=NotificationAction(template_config.get('action_type', 'none')),
                    action_url_template=template_config.get('action_url_template', ''),
                    icon=template_config.get('icon', '📢'),
                    color=template_config.get('color', '#3B82F6'),
                    is_active=True,
                    version='1.0'
                )
                db.session.add(template)
                updated_count += 1
        
        db.session.commit()
        logger.info(f"成功更新 {updated_count} 个通知模板")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新通知模板失败: {str(e)}")
        raise


def check_notification_system():
    """检查通知系统状态"""
    try:
        logger.info("检查通知系统状态...")
        
        # 检查表是否存在
        tables = ['notifications', 'notification_templates', 'notification_configs']
        for table in tables:
            try:
                result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                logger.info(f"表 {table}: {count} 条记录")
            except Exception as e:
                logger.error(f"表 {table} 不存在或访问失败: {str(e)}")
        
        # 检查模板
        template_count = db.session.query(NotificationTemplate).count()
        active_template_count = db.session.query(NotificationTemplate).filter_by(is_active=True).count()
        logger.info(f"通知模板: 总计 {template_count} 个，活跃 {active_template_count} 个")
        
        # 检查通知统计
        total_notifications = db.session.query(Notification).count()
        unread_notifications = db.session.query(Notification).filter_by(status='unread').count()
        logger.info(f"通知: 总计 {total_notifications} 条，未读 {unread_notifications} 条")
        
        logger.info("通知系统状态检查完成")
        
    except Exception as e:
        logger.error(f"检查通知系统状态失败: {str(e)}")
        raise
