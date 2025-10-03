import api from '@/utils/api'

// 咨询师管理API
export const counselorAPI = {
    // 获取咨询师列表
    getCounselors: (params) => api.get('/counselor', { params }),

    // 获取咨询师详情
    getCounselor: (id) => api.get(`/counselor/${id}`),

    // 创建咨询师
    createCounselor: (data) => api.post('/counselor', data),

    // 更新咨询师
    updateCounselor: (id, data) => api.put(`/counselor/${id}`, data),

    // 删除咨询师
    deleteCounselor: (id) => api.delete(`/counselor/${id}`),

    // 更新咨询师状态
    updateCounselorStatus: (id, status) => api.put(`/counselor/${id}/status`, { status }),

    // 获取咨询师评价
    getCounselorReviews: (id, params) => api.get(`/counselor/${id}/reviews`, { params }),

    // 上传头像
    uploadAvatar: (id, formData) => api.post(`/counselor/${id}/avatar`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }),

    // 获取咨询师可用时间
    getAvailableTimes: (id, params) => api.get(`/counselor/${id}/available-times`, { params })
}

export default counselorAPI
