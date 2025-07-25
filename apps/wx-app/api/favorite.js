import request from '../utils/request';

/**
 * 收藏管理API类
 */
class FavoriteApi {
  /**
   * 获取收藏列表
   * @param {Object} params - 查询参数 {userId, type, page, pageSize}
   * @returns {Promise} - 收藏列表
   */
  static getFavoriteList(params) {
    const {
      userId,
      type = 'counselor',
      page = 1,
      pageSize = 10
    } = params;
    return request({
      url: `/favorites/${type === 'counselor' ? 'counselors' : 'courses'}`,
      method: 'GET',
      params: {
        userId,
        type,
        page,
        pageSize
      }
    });
  }

  /**
   * 添加收藏
   * @param {Object} data - 收藏信息 {userId, itemId, itemType}
   * @returns {Promise} - 添加结果
   */
  static addFavorite(data) {
    return request({
      url: '/favorites',
      method: 'POST',
      data
    });
  }

  /**
   * 取消收藏
   * @param {String} favoriteId - 收藏ID
   * @returns {Promise} - 取消结果
   */
  static removeFavorite(favoriteId) {
    return request({
      url: `/favorites/${favoriteId}`,
      method: 'DELETE'
    });
  }

  /**
   * 检查是否已收藏
   * @param {Object} params - 查询参数 {userId, id, type}
   * @returns {Promise} - 检查结果
   */
  static checkFavorite(params) {
    return request({
      url: '/favorite/check',
      method: 'GET',
      params
    });
  }
}

// 默认导出
export default {
  FavoriteApi,
};