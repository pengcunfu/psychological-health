import {createRouter, createWebHistory} from 'vue-router'
import Login from '@/views/Login.vue'
import Home from '@/views/Home.vue'
import UserProfile from '@/views/UserProfile.vue'
import UserManagement from '@/views/admin/UserManagement.vue'
import CounselorManagement from '@/views/admin/CounselorManagement.vue'
import OrderManagement from '@/views/admin/OrderManagement.vue'
import CourseManagement from '@/views/admin/CourseManagement.vue'
import AnnouncementManagement from '@/views/admin/AnnouncementManagement.vue'
import ReviewManagement from '@/views/admin/ReviewManagement.vue'
import CategoryManagement from '@/views/admin/CategoryManagement.vue'
import AppointmentManagement from '@/views/admin/AppointmentManagement.vue'
import BannerManagement from '@/views/admin/BannerManagement.vue'
import MenuManagement from '@/views/admin/MenuManagement.vue'
import GroupManagement from '@/views/admin/GroupManagement.vue'
import RoleManagement from '@/views/admin/RoleManagement.vue'
import DiseaseTagsManagement from '@/views/admin/DiseaseTagsManagement.vue'
import WorkspaceManagement from '@/views/admin/WorkspaceManagement.vue'
import CourseOutlineManagement from '@/views/admin/CourseOutlineManagement.vue'
import AssessmentManagement from '@/views/admin/AssessmentManagement.vue'
import NotFound from '@/views/common/404.vue'
import Unauthorized from '@/views/common/401.vue'

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: {
            requiresAuth: false
        }
    },
    {
        path: '/',
        component: Home,
        meta: {
            requiresAuth: true
        },
        children: [
            {
                path: '',
                name: 'Dashboard',
                meta: {
                    title: '首页',
                    requiresAuth: true
                }
            },
            {
                path: 'profile',
                name: 'UserProfile',
                component: UserProfile,
                meta: {
                    title: '个人资料',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/users',
                name: 'UserManagement',
                component: UserManagement,
                meta: {
                    title: '用户管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/counselors',
                name: 'CounselorManagement',
                component: CounselorManagement,
                meta: {
                    title: '咨询师管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/orders',
                name: 'OrderManagement',
                component: OrderManagement,
                meta: {
                    title: '订单管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/courses',
                name: 'CourseManagement',
                component: CourseManagement,
                meta: {
                    title: '课程管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/announcements',
                name: 'AnnouncementManagement',
                component: AnnouncementManagement,
                meta: {
                    title: '公告管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/reviews',
                name: 'ReviewManagement',
                component: ReviewManagement,
                meta: {
                    title: '评价管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/categories',
                name: 'CategoryManagement',
                component: CategoryManagement,
                meta: {
                    title: '分类管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/appointments',
                name: 'AppointmentManagement',
                component: AppointmentManagement,
                meta: {
                    title: '预约管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/banners',
                name: 'BannerManagement',
                component: BannerManagement,
                meta: {
                    title: '横幅管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/menus',
                name: 'MenuManagement',
                component: MenuManagement,
                meta: {
                    title: '菜单管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/groups',
                name: 'GroupManagement',
                component: GroupManagement,
                meta: {
                    title: '群组管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/roles',
                name: 'RoleManagement',
                component: RoleManagement,
                meta: {
                    title: '角色管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/disease-tags',
                name: 'DiseaseTagsManagement',
                component: DiseaseTagsManagement,
                meta: {
                    title: '疾病标签管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/workspaces',
                name: 'WorkspaceManagement',
                component: WorkspaceManagement,
                meta: {
                    title: '工作空间管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/course-outlines',
                name: 'CourseOutlineManagement',
                component: CourseOutlineManagement,
                meta: {
                    title: '课程大纲管理',
                    requiresAuth: true
                }
            },
            {
                path: 'admin/assessments',
                name: 'AssessmentManagement',
                component: AssessmentManagement,
                meta: {
                    title: '心理测评管理',
                    requiresAuth: true
                }
            }
        ]
    },
    {
        path: '/401',
        name: 'Unauthorized',
        component: Unauthorized,
        meta: {
            requiresAuth: false
        }
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: NotFound,
        meta: {
            requiresAuth: false
        }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')

    if (to.meta.requiresAuth && !token) {
        next('/login')
    } else if (to.path === '/login' && token) {
        next('/')
    } else {
        next()
    }
})

export default router 