import api from '@/utils/api'

// 测评记录管理API
export const assessmentRecordAPI = {
  // 获取测评记录列表
  getAssessmentRecords: (params) => api.get('/assessment-record', { params }),

  // 获取测评记录详情
  getAssessmentRecord: (id) => api.get(`/assessment-record/${id}`),

  // 创建测评记录
  createAssessmentRecord: (data) => api.post('/assessment-record', data),

  // 更新测评记录
  updateAssessmentRecord: (id, data) => api.put(`/assessment-record/${id}`, data),

  // 删除测评记录
  deleteAssessmentRecord: (id) => api.delete(`/assessment-record/${id}`),

  // 获取我的测评记录
  getMyAssessmentRecords: (params) => api.get('/assessment-record/my', { params }),

  // 获取测评记录统计
  getAssessmentRecordStats: () => api.get('/assessment-record/stats'),

  // 导出测评记录
  exportAssessmentRecords: (params) => api.get('/assessment-record/export', { params, responseType: 'blob' })
}

// 测评管理API  
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

  // 发布测评
  publishAssessment: (id) => api.put(`/assessment/${id}/publish`),

  // 获取测评题目
  getAssessmentQuestions: (id) => api.get(`/assessment/${id}/questions`),

  // 更新测评题目
  updateAssessmentQuestions: (id, data) => api.put(`/assessment/${id}/questions`, data)
} 