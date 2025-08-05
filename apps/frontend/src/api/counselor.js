import { request } from '@/utils/request'

/**
 * 咨询师相关API
 */
export const counselorAPI = {
  /**
   * 获取咨询师列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.per_page - 每页数量
   * @param {string} params.name - 咨询师姓名（可选）
   * @param {string} params.title - 职称（可选）
   * @param {string} params.keyword - 搜索关键词（可选）
   * @param {string} params.sort_by - 排序字段：rating(评分), price(价格), created_at(创建时间)（可选）
   * @param {string} params.sort_order - 排序方向：asc(升序), desc(降序)（可选）
   * @param {number} params.status - 状态（可选）
   * @returns {Promise} API响应
   */
  getCounselors(params = {}) {
    console.log('发送咨询师列表请求，参数:', params)
    return request({
      url: '/counselor',
      method: 'GET',
      data: {
        page: 1,
        per_page: 10,
        ...params
      }
    })
  },

  /**
   * 获取单个咨询师详情
   * @param {string} counselorId - 咨询师ID
   * @returns {Promise} API响应
   */
  getCounselorDetail(counselorId) {
    return request({
      url: `/counselor/${counselorId}`,
      method: 'GET'
    })
  },

  /**
   * 创建咨询师
   * @param {Object} data - 咨询师数据
   * @returns {Promise} API响应
   */
  createCounselor(data) {
    return request({
      url: '/counselor',
      method: 'POST',
      data
    })
  },

  /**
   * 更新咨询师信息
   * @param {string} counselorId - 咨询师ID
   * @param {Object} data - 更新数据
   * @returns {Promise} API响应
   */
  updateCounselor(counselorId, data) {
    return request({
      url: `/counselor/${counselorId}`,
      method: 'PUT',
      data
    })
  },

  /**
   * 删除咨询师
   * @param {string} counselorId - 咨询师ID
   * @returns {Promise} API响应
   */
  deleteCounselor(counselorId) {
    return request({
      url: `/counselor/${counselorId}`,
      method: 'DELETE'
    })
  }
} 