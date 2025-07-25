/**
 * 通用API类
 */
class CommonApi {
  /**
   * 提交反馈信息
   * @param {Object} data - 反馈数据 {userId, content, contactInfo}
   * @returns {Promise} - 提交结果
   */
  static submitFeedback(data) {
    return request({
      url: '/common/feedback',
      method: 'POST',
      data
    });
  }
}

// 默认导出
export default {
  CommonApi,
};