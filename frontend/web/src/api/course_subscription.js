import api from '@/utils/api'

// 课程订阅管理API
export const courseSubscriptionAPI = {
    // 获取课程订阅列表
    getCourseSubscriptions: (params) => api.get('/course-subscription', { params }),

    // 获取课程订阅详情
    getCourseSubscription: (id) => api.get(`/course-subscription/${id}`),

    // 创建课程订阅
    createCourseSubscription: (data) => api.post('/course-subscription', data),

    // 更新课程订阅
    updateCourseSubscription: (id, data) => api.put(`/course-subscription/${id}`, data),

    // 删除课程订阅
    deleteCourseSubscription: (id) => api.delete(`/course-subscription/${id}`),

    // 更新学习进度
    updateProgress: (id, data) => api.put(`/course-subscription/${id}/progress`, data),

    // 延长订阅
    extendSubscription: (id, data) => api.put(`/course-subscription/${id}/extend`, data),

    // 取消订阅
    cancelSubscription: (id, data) => api.put(`/course-subscription/${id}/cancel`, data),

    // 获取我的订阅列表
    getMyCourseSubscriptions: (params) => api.get('/course-subscription/my', { params }),

    // 获取订阅统计信息
    getCourseSubscriptionStats: () => api.get('/course-subscription/stats')
} 