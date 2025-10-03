"""
数据初始化模块
统一的数据初始化入口
"""
import click
from flask.cli import with_appcontext

from pcf_flask_helper.model.base import db
from .admin import create_roles, create_users
from .common import create_counselors, create_consultants
from .menu import create_menus

from loguru import logger


def register_init_command(app):
    """注册初始化命令"""

    @app.cli.command()
    @with_appcontext
    def init():
        """统一初始化系统数据（用户角色、咨询师、咨询人、菜单）"""
        try:
            click.echo('开始初始化心理健康平台系统...')

            # 1. 创建数据库表
            click.echo('\n1. 创建数据库表...')
            db.create_all()
            click.echo('   数据库表创建成功')

            # 2. 创建系统角色
            click.echo('\n2. 创建系统角色...')
            create_roles()

            # 3. 创建系统用户
            click.echo('\n3. 创建系统用户...')
            create_users()

            # 4. 创建咨询师数据
            click.echo('\n4. 创建咨询师数据...')
            create_counselors()

            # 5. 创建咨询人数据
            click.echo('\n5. 创建咨询人数据...')
            create_consultants()

            # 6. 创建菜单系统
            click.echo('\n6. 创建菜单系统...')
            create_menus()

            # 7. 提交事务
            db.session.commit()

            # 8. 显示初始化结果
            click.echo('\n系统初始化完成！')
            click.echo('警告: 请在生产环境中及时修改默认密码！')
            click.echo('系统已准备就绪，可以开始使用了！')

            logger.info("系统初始化完成")

        except Exception as e:
            db.session.rollback()
            click.echo(f'系统初始化失败: {str(e)}', err=True)
            logger.error(f"系统初始化失败: {e}")
            import traceback
            traceback.print_exc()
