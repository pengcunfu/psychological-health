import request from '../utils/request';

/**
 * 用户管理API类
 */
class UserApi {
  /**
   * 获取用户资料
   * @param {String} userId - 用户ID
   * @returns {Promise} - 用户资料
   */
  static getUserProfile(userId) {
    return request({
      url: `/user/${userId}`,
      method: 'GET'
    });
  }

  /**
   * 修改用户资料
   * @param {String} userId - 用户ID
   * @param {Object} data - 用户资料 {nickname, avatar, gender, age, bio}
   * @returns {Promise} - 修改结果
   */
  static updateUserProfile(userId, data) {
    return request({
      url: `/user/${userId}`,
      method: 'PUT',
      data
    });
  }

  /**
   * 获取用户统计数据
   * @param {String} userId - 用户ID
   * @returns {Promise} - 统计数据
   */
  static getUserStatistics(userId) {
    return request({
      url: `/user/statistics?userId=${userId}`,
      method: 'GET'
    });
  }
}

// 默认导出
export default {
  UserApi,
};