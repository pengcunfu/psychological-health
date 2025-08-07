import api from '@/utils/api'

// 咨询人管理API
export const consultantAPI = {
    // 获取咨询人列表
    getConsultants: (params) => api.get('/consultant', { params }),

    // 获取咨询人详情
    getConsultant: (id) => api.get(`/consultant/${id}`),

    // 创建咨询人
    createConsultant: (data) => api.post('/consultant', data),

    // 更新咨询人
    updateConsultant: (id, data) => api.put(`/consultant/${id}`, data),

    // 删除咨询人
    deleteConsultant: (id) => api.delete(`/consultant/${id}`),

    // 设置默认咨询人
    setDefaultConsultant: (id) => api.put(`/consultant/${id}/set-default`),

    // 获取默认咨询人
    getDefaultConsultant: () => api.get('/consultant/default'),

    // 获取咨询人选项列表（用于下拉选择）
    getConsultantOptions: () => api.get('/consultant/options'),

    // 获取咨询人相关枚举值
    getConsultantEnums: () => api.get('/consultant/enums'),

    // 获取咨询人统计信息
    getConsultantStats: () => api.get('/consultant/stats')
}

// 导出单独的咨询人API函数，以便在其他组件中直接使用
export const getConsultants = (params) => consultantAPI.getConsultants(params)
export const getConsultant = (id) => consultantAPI.getConsultant(id)
export const createConsultant = (data) => consultantAPI.createConsultant(data)
export const updateConsultant = (id, data) => consultantAPI.updateConsultant(id, data)
export const deleteConsultant = (id) => consultantAPI.deleteConsultant(id)
export const setDefaultConsultant = (id) => consultantAPI.setDefaultConsultant(id)
export const getDefaultConsultant = () => consultantAPI.getDefaultConsultant()
export const getConsultantOptions = () => consultantAPI.getConsultantOptions()
export const getConsultantEnums = () => consultantAPI.getConsultantEnums()
export const getConsultantStats = () => consultantAPI.getConsultantStats()

export default consultantAPI
