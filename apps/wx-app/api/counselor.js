import request from '../utils/request';

/**
 * 咨询师管理API类
 */
class CounselorApi {
  /**
   * 获取咨询师列表
   * @param {Object} params - 查询参数 {page, pageSize, keyword, categoryId, sortBy}
   * @returns {Promise} - 咨询师列表
   */
  static getCounselorList(params) {
    return request({
      url: '/counselor/list',
      method: 'POST',
      data: params
    });
  }

  /**
   * 获取咨询师详情
   * @param {String} id - 咨询师ID
   * @returns {Promise} - 咨询师详情
   */
  static getCounselorDetail(id) {
    return request({
      url: `/counselor/${id}`,
      method: 'GET'
    });
  }

  /**
   * 获取咨询师推荐列表
   * @returns {Promise} - 推荐咨询师列表
   */
  static getRecommendedCounselors() {
    return request({
      url: '/counselor/recommended',
      method: 'GET'
    });
  }

  /**
   * 获取咨询师可预约时间
   * @param {String} id - 咨询师ID
   * @param {String} date - 日期 YYYY-MM-DD
   * @returns {Promise} - 可预约时间列表
   */
  static getCounselorAvailableSlots(id, date) {
    return request({
      url: `/counselor/available-slots`,
      method: 'GET',
      params: {
        id,
        date
      }
    });
  }

  /**
   * 申请成为咨询师
   * @param {Object} data - 申请数据
   * @returns {Promise} - 申请结果
   */
  static applyToBeCounselor(data) {
    return request({
      url: '/counselor/apply',
      method: 'POST',
      data
    });
  }
}


// 默认导出
export default {
  CounselorApi
};