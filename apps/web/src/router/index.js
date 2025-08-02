import {createRouter, createWebHistory} from 'vue-router'
import Login from '@/views/Login.vue'
import Home from '@/views/Home.vue'
import UserManagement from '@/views/admin/UserManagement.vue'
import CounselorManagement from '@/views/admin/CounselorManagement.vue'
import OrderManagement from '@/views/admin/OrderManagement.vue'
import CourseManagement from '@/views/admin/CourseManagement.vue'
import AnnouncementManagement from '@/views/admin/AnnouncementManagement.vue'
import ReviewManagement from '@/views/admin/ReviewManagement.vue'
import CategoryManagement from '@/views/admin/CategoryManagement.vue'
import AppointmentManagement from '@/views/admin/AppointmentManagement.vue'

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
            }
        ]
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