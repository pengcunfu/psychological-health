import api from '@/utils/api'

// 收藏管理API
export const favoriteAPI = {
    // 获取收藏列表
    getFavorites: (params) => api.get('/user-favorite', { params }),

    // 获取收藏详情
    getFavorite: (id) => api.get(`/user-favorite/${id}`),

    // 创建收藏
    createFavorite: (data) => api.post('/user-favorite', data),

    // 删除收藏
    deleteFavorite: (id) => api.delete(`/user-favorite/${id}`),

    // 检查收藏状态
    checkFavorite: (data) => api.post('/user-favorite/check', data),

    // 切换收藏状态
    toggleFavorite: (data) => api.post('/user-favorite/toggle', data)
} 