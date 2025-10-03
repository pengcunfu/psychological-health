import api from '@/utils/api'

// 评价管理API
export const reviewAPI = {
    // 获取评价列表
    getReviews: (params) => api.get('/review', { params }),

    // 获取评价详情
    getReview: (id) => api.get(`/review/${id}`),

    // 审核评价
    auditReview: (id, status) => api.put(`/review/${id}/audit`, { status }),

    // 删除评价
    deleteReview: (id) => api.delete(`/review/${id}`),

    // 回复评价
    replyReview: (id, content) => api.post(`/review/${id}/reply`, { content })
}

// 预约管理API
export const appointmentAPI = {
    // 获取预约列表
    getAppointments: (params) => api.get('/appointment', { params }),

    // 获取预约详情
    getAppointment: (id) => api.get(`/appointment/${id}`),

    // 创建预约
    createAppointment: (data) => api.post('/appointment', data),

    // 更新预约
    updateAppointment: (id, data) => api.put(`/appointment/${id}`, data),

    // 更新预约状态
    updateAppointmentStatus: (id, status) => api.put(`/appointment/${id}/status`, { status }),

    // 取消预约
    cancelAppointment: (id, reason) => api.post(`/appointment/${id}/cancel`, { reason }),

    // 获取可用时间段
    getAvailableTimeSlots: (params) => api.get('/appointment/available-slots', { params })
}

// 心理测评管理API
export const assessmentAPI = {
    // 获取测评列表
    getAssessments: (params) => api.get('/assessment', { params }),

    // 获取测评详情
    getAssessment: (id) => api.get(`/assessment/${id}`),

    // 创建测评
    createAssessment: (data) => api.post('/assessment', data),

    // 更新测评
    updateAssessment: (id, data) => api.put(`/assessment/${id}`, data),

    // 删除测评
    deleteAssessment: (id) => api.delete(`/assessment/${id}`),

    // 获取测评题目列表
    getQuestions: (assessmentId) => api.get(`/assessment/${assessmentId}/questions`),

    // 创建测评题目
    createQuestion: (assessmentId, data) => api.post(`/assessment/${assessmentId}/questions`, data),

    // 更新测评题目
    updateQuestion: (assessmentId, questionId, data) => api.put(`/assessment/${assessmentId}/questions/${questionId}`, data),

    // 删除测评题目
    deleteQuestion: (assessmentId, questionId) => api.delete(`/assessment/${assessmentId}/questions/${questionId}`),

    // 获取题目选项列表
    getOptions: (assessmentId, questionId) => api.get(`/assessment/${assessmentId}/questions/${questionId}/options`),

    // 批量保存题目选项
    saveOptions: (assessmentId, questionId, options) => api.post(`/assessment/${assessmentId}/questions/${questionId}/options`, options),

    // 删除选项
    deleteOption: (assessmentId, questionId, optionId) => api.delete(`/assessment/${assessmentId}/questions/${questionId}/options/${optionId}`),

    // 获取测评记录列表
    getRecords: (params) => api.get('/assessment/records', { params }),

    // 获取测评记录详情
    getRecord: (recordId) => api.get(`/assessment/records/${recordId}`),

    // 获取测评统计数据
    getStats: (assessmentId) => api.get(`/assessment/${assessmentId}/stats`)
}

export default { reviewAPI, appointmentAPI, assessmentAPI } 