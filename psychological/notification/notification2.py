"""
通知系统命令行工具
"""
import click
from flask.cli import with_appcontext
from datetime import datetime

from ..notify.migrations import (
    migrate_notification_system,
    cleanup_notification_data,
    update_notification_templates,
    check_notification_system
)
from ..notify.service import notification_service
from ..notify.manager import notification_manager

from loguru import logger


@click.group()
def notification():
    """通知系统管理命令"""
    pass


@notification.command()
@with_appcontext
def init():
    """初始化通知系统"""
    try:
        click.echo("正在初始化通知系统...")
        migrate_notification_system()
        click.echo("✅ 通知系统初始化完成")
    except Exception as e:
        click.echo(f"❌ 通知系统初始化失败: {str(e)}")


@notification.command()
@with_appcontext
def check():
    """检查通知系统状态"""
    try:
        click.echo("正在检查通知系统状态...")
        check_notification_system()
        click.echo("✅ 通知系统状态检查完成")
    except Exception as e:
        click.echo(f"❌ 检查失败: {str(e)}")


@notification.command()
@with_appcontext
def update_templates():
    """更新通知模板"""
    try:
        click.echo("正在更新通知模板...")
        update_notification_templates()
        click.echo("✅ 通知模板更新完成")
    except Exception as e:
        click.echo(f"❌ 更新失败: {str(e)}")


@notification.command()
@click.confirmation_option(prompt='确定要清理所有通知数据吗？此操作不可恢复！')
@with_appcontext
def cleanup():
    """清理通知数据"""
    try:
        click.echo("正在清理通知数据...")
        cleanup_notification_data()
        click.echo("✅ 通知数据清理完成")
    except Exception as e:
        click.echo(f"❌ 清理失败: {str(e)}")


@notification.command()
@with_appcontext
def cleanup_old():
    """清理过期和旧通知"""
    try:
        click.echo("正在清理过期和旧通知...")
        result = notification_service.cleanup_old_notifications()

        if result['code'] == 200:
            data = result['data']
            click.echo(f"✅ 清理完成:")
            click.echo(f"   - 过期通知: {data['expired_count']} 条")
            click.echo(f"   - 旧已读通知: {data['old_read_count']} 条")
            click.echo(f"   - 旧已删除通知: {data['old_deleted_count']} 条")
            click.echo(f"   - 总计清理: {data['total_cleaned']} 条")
        else:
            click.echo(f"❌ 清理失败: {result['message']}")

    except Exception as e:
        click.echo(f"❌ 清理失败: {str(e)}")


@notification.command()
@with_appcontext
def process_scheduled():
    """处理定时通知"""
    try:
        click.echo("正在处理定时通知...")
        result = notification_manager.process_scheduled_notifications()

        if result['code'] == 200:
            processed_count = result['data']['processed_count']
            click.echo(f"✅ 处理完成: {processed_count} 条定时通知")
        else:
            click.echo(f"❌ 处理失败: {result['message']}")

    except Exception as e:
        click.echo(f"❌ 处理失败: {str(e)}")


@notification.command()
@click.option('--user-id', required=True, help='用户ID')
@click.option('--title', required=True, help='通知标题')
@click.option('--content', help='通知内容')
@click.option('--type', default='system', help='通知类型')
@click.option('--priority', default='normal', help='优先级')
@with_appcontext
def send(user_id, title, content, type, priority):
    """发送测试通知"""
    try:
        from ..notify.types import NotificationType, NotificationPriority

        click.echo(f"正在发送通知给用户 {user_id}...")

        result = notification_service.create_notification(
            recipient_id=user_id,
            title=title,
            content=content,
            notification_type=NotificationType(type),
            priority=NotificationPriority(priority)
        )

        if result['code'] == 200:
            click.echo(f"✅ 通知发送成功: {result['data']['id']}")
        else:
            click.echo(f"❌ 发送失败: {result['message']}")

    except Exception as e:
        click.echo(f"❌ 发送失败: {str(e)}")


@notification.command()
@click.option('--template-code', required=True, help='模板代码')
@click.option('--user-id', required=True, help='用户ID')
@click.option('--variables', help='模板变量(JSON格式)')
@with_appcontext
def send_template(template_code, user_id, variables):
    """使用模板发送通知"""
    try:
        import json

        variables_data = {}
        if variables:
            variables_data = json.loads(variables)

        click.echo(f"正在使用模板 {template_code} 发送通知给用户 {user_id}...")

        result = notification_service.create_notification_from_template(
            template_code=template_code,
            recipient_id=user_id,
            variables=variables_data
        )

        if result['code'] == 200:
            click.echo(f"✅ 通知发送成功: {result['data']['id']}")
        else:
            click.echo(f"❌ 发送失败: {result['message']}")

    except Exception as e:
        click.echo(f"❌ 发送失败: {str(e)}")


@notification.command()
@click.option('--user-id', help='指定用户ID（可选）')
@click.option('--days', default=30, help='统计天数')
@with_appcontext
def stats(user_id, days):
    """查看通知统计"""
    try:
        from datetime import timedelta

        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        click.echo(f"正在获取最近 {days} 天的通知统计...")

        result = notification_manager.get_notification_statistics(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )

        if result['code'] == 200:
            data = result['data']
            summary = data['summary']

            click.echo(f"✅ 统计结果 ({data['period']['start_date']} 至 {data['period']['end_date']}):")
            click.echo(f"   - 总通知数: {summary['total_count']}")
            click.echo(f"   - 未读数: {summary['unread_count']}")
            click.echo(f"   - 已读数: {summary['read_count']}")
            click.echo(f"   - 阅读率: {summary['read_rate']}%")

            click.echo("\n按类型统计:")
            for type_name, count in data['type_stats'].items():
                if count > 0:
                    click.echo(f"   - {type_name}: {count}")

            click.echo("\n按优先级统计:")
            for priority, count in data['priority_stats'].items():
                if count > 0:
                    click.echo(f"   - {priority}: {count}")

        else:
            click.echo(f"❌ 获取统计失败: {result['message']}")

    except Exception as e:
        click.echo(f"❌ 获取统计失败: {str(e)}")


@notification.command()
@click.option('--user-id', required=True, help='用户ID')
@with_appcontext
def unread(user_id):
    """查看用户未读通知数"""
    try:
        click.echo(f"正在获取用户 {user_id} 的未读通知数...")

        result = notification_service.get_unread_count(user_id)

        if result['code'] == 200:
            data = result['data']
            click.echo(f"✅ 未读通知统计:")
            click.echo(f"   - 总未读数: {data['total_unread']}")

            click.echo("\n按类型统计:")
            for type_name, count in data['type_counts'].items():
                if count > 0:
                    click.echo(f"   - {type_name}: {count}")

        else:
            click.echo(f"❌ 获取失败: {result['message']}")

    except Exception as e:
        click.echo(f"❌ 获取失败: {str(e)}")


# 注册命令组
def register_notification_commands(app):
    """注册通知相关命令"""
    app.cli.add_command(notification)
