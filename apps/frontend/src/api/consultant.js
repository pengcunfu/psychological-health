import { request } from '@/utils/request'

/**
 * 咨询人相关API
 */
export const consultantAPI = {
  /**
   * 获取咨询人列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.per_page - 每页数量
   * @param {string} params.name - 咨询人姓名（可选）
   * @param {string} params.phone - 电话号码（可选）
   * @param {string} params.keyword - 搜索关键词（可选）
   * @param {string} params.sort_by - 排序字段：created_at(创建时间), birth_year(出生年份)（可选）
   * @param {string} params.sort_order - 排序方向：asc(升序), desc(降序)（可选）
   * @param {number} params.status - 状态（可选）
   * @param {string} params.user_id - 关联用户ID（可选）
   * @returns {Promise} API响应
   */
  getConsultants(params = {}) {
    return request({
      url: '/consultant',
      method: 'GET',
      data: {
        page: 1,
        per_page: 10,
        ...params
      }
    })
  },

  /**
   * 获取单个咨询人详情
   * @param {string} consultantId - 咨询人ID
   * @returns {Promise} API响应
   */
  getConsultantDetail(consultantId) {
    return request({
      url: `/consultant/${consultantId}`,
      method: 'GET'
    })
  },

  /**
   * 创建咨询人
   * @param {Object} data - 咨询人数据
   * @param {string} data.real_name - 真实姓名
   * @param {string} data.phone - 电话号码
   * @param {number} data.birth_year - 出生年份（可选）
   * @param {number} data.birth_month - 出生月份（可选）
   * @param {string} data.gender - 性别 (male/female)
   * @param {string} data.emergency_name - 紧急联系人姓名
   * @param {string} data.emergency_relationship - 紧急联系人关系
   * @param {string} data.emergency_phone - 紧急联系人电话
   * @param {string} data.notes - 备注（可选）
   * @param {number} data.is_default - 是否默认咨询人（可选）
   * @param {string} data.user_id - 关联用户ID（可选）
   * @returns {Promise} API响应
   */
  createConsultant(data) {
    return request({
      url: '/consultant',
      method: 'POST',
      data
    })
  },

  /**
   * 更新咨询人信息
   * @param {string} consultantId - 咨询人ID
   * @param {Object} data - 更新数据
   * @returns {Promise} API响应
   */
  updateConsultant(consultantId, data) {
    return request({
      url: `/consultant/${consultantId}`,
      method: 'PUT',
      data
    })
  },

  /**
   * 删除咨询人
   * @param {string} consultantId - 咨询人ID
   * @returns {Promise} API响应
   */
  deleteConsultant(consultantId) {
    return request({
      url: `/consultant/${consultantId}`,
      method: 'DELETE'
    })
  },

  /**
   * 设置默认咨询人
   * @param {string} consultantId - 咨询人ID
   * @returns {Promise} API响应
   */
  setDefaultConsultant(consultantId) {
    return request({
      url: `/consultant/${consultantId}/set-default`,
      method: 'PUT'
    })
  },

  /**
   * 获取默认咨询人
   * @returns {Promise} API响应
   */
  getDefaultConsultant() {
    return request({
      url: '/consultant/default',
      method: 'GET'
    })
  },

  /**
   * 获取咨询人选项列表（用于下拉选择）
   * @param {Object} params - 查询参数（可选）
   * @param {string} params.user_id - 用户ID，获取该用户的咨询人列表（可选）
   * @returns {Promise} API响应
   */
  getConsultantOptions(params = {}) {
    return request({
      url: '/consultant/options',
      method: 'GET',
      data: params
    })
  },

  /**
   * 获取咨询人相关枚举值
   * @returns {Promise} API响应
   */
  getConsultantEnums() {
    return request({
      url: '/consultant/enums',
      method: 'GET'
    })
  },

  /**
   * 获取咨询人统计信息
   * @param {Object} params - 查询参数（可选）
   * @param {string} params.user_id - 用户ID，获取该用户的咨询人统计（可选）
   * @returns {Promise} API响应
   */
  getConsultantStats(params = {}) {
    return request({
      url: '/consultant/stats',
      method: 'GET',
      data: params
    })
  }
}

export default consultantAPI
