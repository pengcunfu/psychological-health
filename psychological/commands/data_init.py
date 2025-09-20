"""
数据初始化模块
统一的数据初始化入口
"""
import click
from flask.cli import with_appcontext

from ..models.base import db
from ..utils.logger_client import get_logger
from .admin import create_roles_and_users
from .common import create_counselors, create_consultants
from .menu import create_menus

logger = get_logger(__name__)


@click.group()
def data():
    """数据管理命令组"""
    pass


@data.command()
@with_appcontext
def init():
    """统一初始化系统数据（用户角色、咨询师、咨询人、菜单）"""
    try:
        click.echo('🚀 开始初始化心理健康平台系统...')
        
        # 1. 创建数据库表
        click.echo('\n1️⃣ 创建数据库表...')
        db.create_all()
        click.echo('   ✅ 数据库表创建成功')
        
        # 2. 创建角色和用户
        click.echo('\n2️⃣ 创建系统角色和用户...')
        roles, users = create_roles_and_users()
        
        # 3. 创建咨询师数据
        click.echo('\n3️⃣ 创建咨询师数据...')
        counselors = create_counselors()
        
        # 4. 创建咨询人数据
        click.echo('\n4️⃣ 创建咨询人数据...')
        consultants = create_consultants()
        
        # 5. 创建菜单系统
        click.echo('\n5️⃣ 创建菜单系统...')
        menus = create_menus()
        
        # 6. 提交事务
        db.session.commit()
        
        # 7. 显示初始化结果
        click.echo('\n🎉 系统初始化完成！')
        click.echo('=' * 60)
        click.echo('创建统计:')
        click.echo(f'✅ 角色: {len(roles)} 个')
        click.echo(f'✅ 用户: {len(users)} 个')
        click.echo(f'✅ 咨询师: {len(counselors)} 个')
        click.echo(f'✅ 咨询人: {len(consultants)} 个')
        click.echo(f'✅ 菜单项: {len(menus)} 个')
        click.echo('=' * 60)
        
        # 显示用户信息
        if users:
            click.echo('\n👤 默认账户信息:')
            for user, user_data, role in users:
                click.echo(f'   • {role.name}: {user_data["username"]} / {user_data["password"]}')
        
        # 显示咨询师信息
        if counselors:
            click.echo('\n👨‍⚕️ 咨询师列表:')
            for counselor in counselors:
                click.echo(f'   • {counselor.name} - {counselor.title} (¥{counselor.price}/小时)')
        
        # 显示咨询人信息
        if consultants:
            click.echo('\n👤 咨询人列表:')
            for consultant in consultants:
                click.echo(f'   • {consultant.real_name} - {consultant.gender.value} ({consultant.phone})')
        
        click.echo(f'\n📋 菜单系统已创建，包含完整的权限管理结构')
        click.echo('⚠️  请在生产环境中及时修改默认密码！')
        click.echo('💡 提示: 可通过菜单管理页面查看和编辑菜单结构')
        click.echo('📋 系统已准备就绪，可以开始使用了！')
        
        logger.info("系统初始化完成")
        
    except Exception as e:
        db.session.rollback()
        click.echo(f'❌ 系统初始化失败: {str(e)}', err=True)
        logger.error(f"系统初始化失败: {e}")
        import traceback
        traceback.print_exc()
