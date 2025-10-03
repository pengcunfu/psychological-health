"""
菜单管理模块
创建菜单系统数据
"""
import click
from pcf_flask_helper.model.base import db
from psychological.system.models import Menu


def create_menus() -> None:
    """创建完整的菜单系统"""
    # 检查是否已有菜单数据，如果有则跳过
    existing_count = db.session.query(Menu).count()
    if existing_count > 0:
        click.echo(f'   警告: 系统中已存在 {existing_count} 个菜单，跳过菜单创建')
        return

    menus_data = [
        # 一级菜单
        {
            'id': 'dashboard',
            'name': '仪表板',
            'path': '/dashboard',
            'icon': 'dashboard',
            'parent_id': '',
            'level': 1,
            'sort_order': 1,
            'menu_type': 2,
            'permission': 'dashboard:view',
            'component': 'Dashboard',
            'is_visible': 1,
            'status': 1,
            'remark': '系统仪表板'
        },

        # 用户管理模块
        {
            'id': 'user_management',
            'name': '用户管理',
            'path': '/user',
            'icon': 'user',
            'parent_id': '',
            'level': 1,
            'sort_order': 2,
            'menu_type': 1,
            'permission': 'user:manage',
            'component': '',
            'is_visible': 1,
            'status': 1,
            'remark': '用户管理模块'
        },
        {
            'id': 'user_list',
            'name': '用户列表',
            'path': '/user/list',
            'icon': 'user-list',
            'parent_id': 'user_management',
            'level': 2,
            'sort_order': 1,
            'menu_type': 2,
            'permission': 'user:get_users',
            'component': 'UserList',
            'is_visible': 1,
            'status': 1,
            'remark': '用户列表页面'
        },
        {
            'id': 'user_create',
            'name': '新增用户',
            'path': '',
            'icon': '',
            'parent_id': 'user_list',
            'level': 3,
            'sort_order': 1,
            'menu_type': 3,
            'permission': 'user:create_user',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '新增用户按钮'
        },
        {
            'id': 'user_update',
            'name': '编辑用户',
            'path': '',
            'icon': '',
            'parent_id': 'user_list',
            'level': 3,
            'sort_order': 2,
            'menu_type': 3,
            'permission': 'user:update_user',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '编辑用户按钮'
        },
        {
            'id': 'user_delete',
            'name': '删除用户',
            'path': '',
            'icon': '',
            'parent_id': 'user_list',
            'level': 3,
            'sort_order': 3,
            'menu_type': 3,
            'permission': 'user:delete_user',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '删除用户按钮'
        },

        # 角色管理
        {
            'id': 'role_list',
            'name': '角色管理',
            'path': '/user/role',
            'icon': 'role',
            'parent_id': 'user_management',
            'level': 2,
            'sort_order': 2,
            'menu_type': 2,
            'permission': 'role:get_roles',
            'component': 'RoleList',
            'is_visible': 1,
            'status': 1,
            'remark': '角色管理页面'
        },
        {
            'id': 'role_create',
            'name': '新增角色',
            'path': '',
            'icon': '',
            'parent_id': 'role_list',
            'level': 3,
            'sort_order': 1,
            'menu_type': 3,
            'permission': 'role:create_role',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '新增角色按钮'
        },
        {
            'id': 'role_update',
            'name': '编辑角色',
            'path': '',
            'icon': '',
            'parent_id': 'role_list',
            'level': 3,
            'sort_order': 2,
            'menu_type': 3,
            'permission': 'role:update_role',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '编辑角色按钮'
        },
        {
            'id': 'role_delete',
            'name': '删除角色',
            'path': '',
            'icon': '',
            'parent_id': 'role_list',
            'level': 3,
            'sort_order': 3,
            'menu_type': 3,
            'permission': 'role:delete_role',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '删除角色按钮'
        },

        # 咨询师管理
        {
            'id': 'counselor_management',
            'name': '咨询师管理',
            'path': '/counselor',
            'icon': 'counselor',
            'parent_id': '',
            'level': 1,
            'sort_order': 3,
            'menu_type': 1,
            'permission': 'counselor:manage',
            'component': '',
            'is_visible': 1,
            'status': 1,
            'remark': '咨询师管理模块'
        },
        {
            'id': 'counselor_list',
            'name': '咨询师列表',
            'path': '/counselor/list',
            'icon': 'counselor-list',
            'parent_id': 'counselor_management',
            'level': 2,
            'sort_order': 1,
            'menu_type': 2,
            'permission': 'counselor:get_counselors',
            'component': 'CounselorList',
            'is_visible': 1,
            'status': 1,
            'remark': '咨询师列表页面'
        },
        {
            'id': 'counselor_create',
            'name': '新增咨询师',
            'path': '',
            'icon': '',
            'parent_id': 'counselor_list',
            'level': 3,
            'sort_order': 1,
            'menu_type': 3,
            'permission': 'counselor:create_counselor',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '新增咨询师按钮'
        },
        {
            'id': 'counselor_update',
            'name': '编辑咨询师',
            'path': '',
            'icon': '',
            'parent_id': 'counselor_list',
            'level': 3,
            'sort_order': 2,
            'menu_type': 3,
            'permission': 'counselor:update_counselor',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '编辑咨询师按钮'
        },
        {
            'id': 'counselor_delete',
            'name': '删除咨询师',
            'path': '',
            'icon': '',
            'parent_id': 'counselor_list',
            'level': 3,
            'sort_order': 3,
            'menu_type': 3,
            'permission': 'counselor:delete_counselor',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '删除咨询师按钮'
        },

        # 咨询人管理
        {
            'id': 'consultant_list',
            'name': '咨询人管理',
            'path': '/counselor/consultant',
            'icon': 'consultant',
            'parent_id': 'counselor_management',
            'level': 2,
            'sort_order': 2,
            'menu_type': 2,
            'permission': 'consultant:get_consultants',
            'component': 'ConsultantList',
            'is_visible': 1,
            'status': 1,
            'remark': '咨询人管理页面'
        },
        {
            'id': 'consultant_create',
            'name': '新增咨询人',
            'path': '',
            'icon': '',
            'parent_id': 'consultant_list',
            'level': 3,
            'sort_order': 1,
            'menu_type': 3,
            'permission': 'consultant:create_consultant',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '新增咨询人按钮'
        },
        {
            'id': 'consultant_update',
            'name': '编辑咨询人',
            'path': '',
            'icon': '',
            'parent_id': 'consultant_list',
            'level': 3,
            'sort_order': 2,
            'menu_type': 3,
            'permission': 'consultant:update_consultant',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '编辑咨询人按钮'
        },
        {
            'id': 'consultant_delete',
            'name': '删除咨询人',
            'path': '',
            'icon': '',
            'parent_id': 'consultant_list',
            'level': 3,
            'sort_order': 3,
            'menu_type': 3,
            'permission': 'consultant:delete_consultant',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '删除咨询人按钮'
        },

        # 预约管理
        {
            'id': 'appointment_management',
            'name': '预约管理',
            'path': '/appointment',
            'icon': 'appointment',
            'parent_id': '',
            'level': 1,
            'sort_order': 4,
            'menu_type': 1,
            'permission': 'appointment:manage',
            'component': '',
            'is_visible': 1,
            'status': 1,
            'remark': '预约管理模块'
        },
        {
            'id': 'appointment_list',
            'name': '预约列表',
            'path': '/appointment/list',
            'icon': 'appointment-list',
            'parent_id': 'appointment_management',
            'level': 2,
            'sort_order': 1,
            'menu_type': 2,
            'permission': 'appointment:get_appointments',
            'component': 'AppointmentList',
            'is_visible': 1,
            'status': 1,
            'remark': '预约列表页面'
        },
        {
            'id': 'appointment_create',
            'name': '新增预约',
            'path': '',
            'icon': '',
            'parent_id': 'appointment_list',
            'level': 3,
            'sort_order': 1,
            'menu_type': 3,
            'permission': 'appointment:create_appointment',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '新增预约按钮'
        },
        {
            'id': 'appointment_update',
            'name': '编辑预约',
            'path': '',
            'icon': '',
            'parent_id': 'appointment_list',
            'level': 3,
            'sort_order': 2,
            'menu_type': 3,
            'permission': 'appointment:update_appointment',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '编辑预约按钮'
        },
        {
            'id': 'appointment_delete',
            'name': '删除预约',
            'path': '',
            'icon': '',
            'parent_id': 'appointment_list',
            'level': 3,
            'sort_order': 3,
            'menu_type': 3,
            'permission': 'appointment:delete_appointment',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '删除预约按钮'
        },

        # 课程管理
        {
            'id': 'course_management',
            'name': '课程管理',
            'path': '/course',
            'icon': 'course',
            'parent_id': '',
            'level': 1,
            'sort_order': 5,
            'menu_type': 1,
            'permission': 'course:manage',
            'component': '',
            'is_visible': 1,
            'status': 1,
            'remark': '课程管理模块'
        },
        {
            'id': 'course_list',
            'name': '课程列表',
            'path': '/course/list',
            'icon': 'course-list',
            'parent_id': 'course_management',
            'level': 2,
            'sort_order': 1,
            'menu_type': 2,
            'permission': 'course:get_courses',
            'component': 'CourseList',
            'is_visible': 1,
            'status': 1,
            'remark': '课程列表页面'
        },
        {
            'id': 'course_create',
            'name': '新增课程',
            'path': '',
            'icon': '',
            'parent_id': 'course_list',
            'level': 3,
            'sort_order': 1,
            'menu_type': 3,
            'permission': 'course:create_course',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '新增课程按钮'
        },
        {
            'id': 'course_update',
            'name': '编辑课程',
            'path': '',
            'icon': '',
            'parent_id': 'course_list',
            'level': 3,
            'sort_order': 2,
            'menu_type': 3,
            'permission': 'course:update_course',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '编辑课程按钮'
        },
        {
            'id': 'course_delete',
            'name': '删除课程',
            'path': '',
            'icon': '',
            'parent_id': 'course_list',
            'level': 3,
            'sort_order': 3,
            'menu_type': 3,
            'permission': 'course:delete_course',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '删除课程按钮'
        },

        # 测评管理
        {
            'id': 'assessment_management',
            'name': '测评管理',
            'path': '/assessment',
            'icon': 'assessment',
            'parent_id': '',
            'level': 1,
            'sort_order': 6,
            'menu_type': 1,
            'permission': 'assessment:manage',
            'component': '',
            'is_visible': 1,
            'status': 1,
            'remark': '测评管理模块'
        },
        {
            'id': 'assessment_list',
            'name': '测评列表',
            'path': '/assessment/list',
            'icon': 'assessment-list',
            'parent_id': 'assessment_management',
            'level': 2,
            'sort_order': 1,
            'menu_type': 2,
            'permission': 'assessment:get_assessments',
            'component': 'AssessmentList',
            'is_visible': 1,
            'status': 1,
            'remark': '测评列表页面'
        },
        {
            'id': 'assessment_create',
            'name': '新增测评',
            'path': '',
            'icon': '',
            'parent_id': 'assessment_list',
            'level': 3,
            'sort_order': 1,
            'menu_type': 3,
            'permission': 'assessment:create_assessment',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '新增测评按钮'
        },
        {
            'id': 'assessment_update',
            'name': '编辑测评',
            'path': '',
            'icon': '',
            'parent_id': 'assessment_list',
            'level': 3,
            'sort_order': 2,
            'menu_type': 3,
            'permission': 'assessment:update_assessment',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '编辑测评按钮'
        },
        {
            'id': 'assessment_delete',
            'name': '删除测评',
            'path': '',
            'icon': '',
            'parent_id': 'assessment_list',
            'level': 3,
            'sort_order': 3,
            'menu_type': 3,
            'permission': 'assessment:delete_assessment',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '删除测评按钮'
        },

        # 订单管理
        {
            'id': 'order_management',
            'name': '订单管理',
            'path': '/order',
            'icon': 'order',
            'parent_id': '',
            'level': 1,
            'sort_order': 7,
            'menu_type': 1,
            'permission': 'order:manage',
            'component': '',
            'is_visible': 1,
            'status': 1,
            'remark': '订单管理模块'
        },
        {
            'id': 'order_list',
            'name': '订单列表',
            'path': '/order/list',
            'icon': 'order-list',
            'parent_id': 'order_management',
            'level': 2,
            'sort_order': 1,
            'menu_type': 2,
            'permission': 'order:get_orders',
            'component': 'OrderList',
            'is_visible': 1,
            'status': 1,
            'remark': '订单列表页面'
        },

        # 内容管理
        {
            'id': 'content_management',
            'name': '内容管理',
            'path': '/content',
            'icon': 'content',
            'parent_id': '',
            'level': 1,
            'sort_order': 8,
            'menu_type': 1,
            'permission': 'content:manage',
            'component': '',
            'is_visible': 1,
            'status': 1,
            'remark': '内容管理模块'
        },
        {
            'id': 'banner_list',
            'name': '横幅管理',
            'path': '/content/banner',
            'icon': 'banner',
            'parent_id': 'content_management',
            'level': 2,
            'sort_order': 1,
            'menu_type': 2,
            'permission': 'banner:get_banners',
            'component': 'BannerList',
            'is_visible': 1,
            'status': 1,
            'remark': '横幅管理页面'
        },
        {
            'id': 'announcement_list',
            'name': '公告管理',
            'path': '/content/announcement',
            'icon': 'announcement',
            'parent_id': 'content_management',
            'level': 2,
            'sort_order': 2,
            'menu_type': 2,
            'permission': 'announcement:get_announcements',
            'component': 'AnnouncementList',
            'is_visible': 1,
            'status': 1,
            'remark': '公告管理页面'
        },
        {
            'id': 'category_list',
            'name': '分类管理',
            'path': '/content/category',
            'icon': 'category',
            'parent_id': 'content_management',
            'level': 2,
            'sort_order': 3,
            'menu_type': 2,
            'permission': 'category:get_categories',
            'component': 'CategoryList',
            'is_visible': 1,
            'status': 1,
            'remark': '分类管理页面'
        },

        # 系统管理
        {
            'id': 'system_management',
            'name': '系统管理',
            'path': '/system',
            'icon': 'system',
            'parent_id': '',
            'level': 1,
            'sort_order': 9,
            'menu_type': 1,
            'permission': 'system:manage',
            'component': '',
            'is_visible': 1,
            'status': 1,
            'remark': '系统管理模块'
        },
        {
            'id': 'menu_list',
            'name': '菜单管理',
            'path': '/system/menu',
            'icon': 'menu',
            'parent_id': 'system_management',
            'level': 2,
            'sort_order': 1,
            'menu_type': 2,
            'permission': 'menu:get_menus',
            'component': 'MenuList',
            'is_visible': 1,
            'status': 1,
            'remark': '菜单管理页面'
        },
        {
            'id': 'menu_create',
            'name': '新增菜单',
            'path': '',
            'icon': '',
            'parent_id': 'menu_list',
            'level': 3,
            'sort_order': 1,
            'menu_type': 3,
            'permission': 'menu:create_menu',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '新增菜单按钮'
        },
        {
            'id': 'menu_update',
            'name': '编辑菜单',
            'path': '',
            'icon': '',
            'parent_id': 'menu_list',
            'level': 3,
            'sort_order': 2,
            'menu_type': 3,
            'permission': 'menu:update_menu',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '编辑菜单按钮'
        },
        {
            'id': 'menu_delete',
            'name': '删除菜单',
            'path': '',
            'icon': '',
            'parent_id': 'menu_list',
            'level': 3,
            'sort_order': 3,
            'menu_type': 3,
            'permission': 'menu:delete_menu',
            'component': '',
            'is_visible': 0,
            'status': 1,
            'remark': '删除菜单按钮'
        }
    ]

    created_menus = []
    for menu_data in menus_data:
        # 检查是否已存在
        existing = db.session.query(Menu).filter_by(id=menu_data['id']).first()
        if existing:
            click.echo(f'   警告: 菜单 "{menu_data["name"]}" 已存在，跳过创建')
            continue

        menu = Menu(
            id=menu_data['id'],
            name=menu_data['name'],
            path=menu_data['path'],
            icon=menu_data['icon'],
            parent_id=menu_data['parent_id'],
            level=menu_data['level'],
            sort_order=menu_data['sort_order'],
            menu_type=menu_data['menu_type'],
            permission=menu_data['permission'],
            component=menu_data['component'],
            is_external=menu_data.get('is_external', 0),
            is_visible=menu_data['is_visible'],
            is_cache=menu_data.get('is_cache', 0),
            status=menu_data['status'],
            remark=menu_data['remark']
        )

        db.session.add(menu)
        created_menus.append(menu)
        click.echo(f'   创建菜单: {menu_data["name"]} (Level {menu_data["level"]})')

    click.echo(f'\n菜单系统创建完成！')
    click.echo(f'菜单项: {len(created_menus)} 个')
    click.echo(f'菜单系统已创建，包含完整的权限管理结构')
    click.echo('提示: 可通过菜单管理页面查看和编辑菜单结构')
    
