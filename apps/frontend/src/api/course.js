import { request } from '@/utils/request'

/**
 * 课程相关API
 */
export const courseAPI = {
  /**
   * 获取课程列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.per_page - 每页数量
   * @param {string} params.name - 课程名称（可选）
   * @param {number} params.category_id - 分类ID（可选）
   * @param {number} params.status - 状态（可选）
   * @returns {Promise} API响应
   */
  getCourses(params = {}) {
    return request({
      url: '/course',
      method: 'GET',
      data: {
        page: 1,
        per_page: 10,
        ...params
      }
    })
  },

  /**
   * 获取单个课程详情
   * @param {string} courseId - 课程ID
   * @returns {Promise} API响应
   */
  getCourseDetail(courseId) {
    return request({
      url: `/course/${courseId}`,
      method: 'GET'
    })
  },

  /**
   * 创建课程
   * @param {Object} data - 课程数据
   * @returns {Promise} API响应
   */
  createCourse(data) {
    return request({
      url: '/course',
      method: 'POST',
      data
    })
  },

  /**
   * 更新课程信息
   * @param {string} courseId - 课程ID
   * @param {Object} data - 更新数据
   * @returns {Promise} API响应
   */
  updateCourse(courseId, data) {
    return request({
      url: `/course/${courseId}`,
      method: 'PUT',
      data
    })
  },

  /**
   * 删除课程
   * @param {string} courseId - 课程ID
   * @returns {Promise} API响应
   */
  deleteCourse(courseId) {
    return request({
      url: `/course/${courseId}`,
      method: 'DELETE'
    })
  }
} 