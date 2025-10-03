import api from '@/utils/api'

// 公告管理API
export const announcementAPI = {
    // 获取公告列表
    getAnnouncements: (params) => api.get('/announcement', { params }),

    // 获取公告详情
    getAnnouncement: (id) => api.get(`/announcement/${id}`),

    // 创建公告
    createAnnouncement: (data) => api.post('/announcement', data),

    // 更新公告
    updateAnnouncement: (id, data) => api.put(`/announcement/${id}`, data),

    // 删除公告
    deleteAnnouncement: (id) => api.delete(`/announcement/${id}`),

    // 置顶公告
    pinAnnouncement: (id, isPinned) => api.put(`/announcement/${id}/pin`, { is_pinned: isPinned })
}

// 分类管理API
export const categoryAPI = {
    // 获取分类列表
    getCategories: (params) => api.get('/category', { params }),

    // 获取分类详情
    getCategory: (id) => api.get(`/category/${id}`),

    // 创建分类
    createCategory: (data) => api.post('/category', data),

    // 更新分类
    updateCategory: (id, data) => api.put(`/category/${id}`, data),

    // 删除分类
    deleteCategory: (id) => api.delete(`/category/${id}`),

    // 获取分类下的项目
    getCategoryItems: (id, params) => api.get(`/category/${id}/items`, { params })
}

// 轮播图管理API
export const bannerAPI = {
    // 获取轮播图列表
    getBanners: (params) => api.get('/banner', { params }),

    // 获取轮播图详情
    getBanner: (id) => api.get(`/banner/${id}`),

    // 创建轮播图
    createBanner: (data) => api.post('/banner', data),

    // 更新轮播图
    updateBanner: (id, data) => api.put(`/banner/${id}`, data),

    // 删除轮播图
    deleteBanner: (id) => api.delete(`/banner/${id}`)
}

export default { announcementAPI, categoryAPI, bannerAPI } 