/**
 * 评价管理API类
 */
class ReviewApi {
  /**
   * 获取咨询师评价列表
   * @param {Object} params - 查询参数 {targetId, targetType, page, pageSize}
   * @returns {Promise} - 评价列表
   */
  static getCounselorReviews(params) {
    return request({
      url: '/review/list',
      method: 'GET',
      params
    });
  }

  /**
   * 提交咨询师评价
   * @param {Object} data - 评价数据 {counselorId, content, rating, orderId}
   * @returns {Promise} - 提交结果
   */
  static submitCounselorReview(data) {
    return request({
      url: '/review/submit',
      method: 'POST',
      data
    });
  }
}

// 默认导出
export default {
  ReviewApi,
};