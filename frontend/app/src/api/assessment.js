/**
 * 测评相关API接口
 */
import { request } from '@/utils/request'

export const assessmentAPI = {
  // 获取测评列表
  getAssessments: (params) => {
    return request({
      url: '/assessment',
      method: 'get',
      params
    })
  },

  // 获取测评详情
  getAssessment: (assessmentId) => {
    return request({
      url: `/assessment/${assessmentId}`,
      method: 'get'
    })
  },

  // 创建测评
  createAssessment: (data) => {
    return request({
      url: '/assessment',
      method: 'post',
      data
    })
  },

  // 更新测评
  updateAssessment: (assessmentId, data) => {
    return request({
      url: `/assessment/${assessmentId}`,
      method: 'put',
      data
    })
  },

  // 删除测评
  deleteAssessment: (assessmentId) => {
    return request({
      url: `/assessment/${assessmentId}`,
      method: 'delete'
    })
  },

  // 创建测评题目
  createQuestion: (assessmentId, data) => {
    return request({
      url: `/assessment/${assessmentId}/questions`,
      method: 'post',
      data
    })
  },

  // 更新测评题目
  updateQuestion: (assessmentId, questionId, data) => {
    return request({
      url: `/assessment/${assessmentId}/questions/${questionId}`,
      method: 'put',
      data
    })
  },

  // 删除测评题目
  deleteQuestion: (assessmentId, questionId) => {
    return request({
      url: `/assessment/${assessmentId}/questions/${questionId}`,
      method: 'delete'
    })
  },

  // 获取题目选项列表
  getOptions: (assessmentId, questionId) => {
    return request({
      url: `/assessment/${assessmentId}/questions/${questionId}/options`,
      method: 'get'
    })
  },

  // 批量保存题目选项
  saveOptions: (assessmentId, questionId, options) => {
    return request({
      url: `/assessment/${assessmentId}/questions/${questionId}/options`,
      method: 'post',
      data: options
    })
  },

  // 删除选项
  deleteOption: (assessmentId, questionId, optionId) => {
    return request({
      url: `/assessment/${assessmentId}/questions/${questionId}/options/${optionId}`,
      method: 'delete'
    })
  },

  // 开始测评
  startAssessment: (data) => {
    return request({
      url: '/assessment/start',
      method: 'post',
      data
    })
  },

  // 提交测评
  submitAssessment: (data) => {
    return request({
      url: '/assessment/submit',
      method: 'post',
      data
    })
  },

  // 获取测评记录列表
  getRecords: (params) => {
    return request({
      url: '/assessment/records',
      method: 'get',
      params
    })
  },

  // 获取测评记录详情
  getRecord: (recordId) => {
    return request({
      url: `/assessment/records/${recordId}`,
      method: 'get'
    })
  }
}

export default assessmentAPI
