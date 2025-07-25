import request from '../utils/request';

/**
 * 公告管理API类
 */
class AnnouncementApi {
  /**
   * 获取公告列表
   * @returns {Promise} - 公告列表
   */
  static getAnnouncementList() {
    return request({
      url: '/announcement/list',
      method: 'GET'
    });
  }

  /**
   * 获取单个公告详情
   * @param {String} id - 公告ID
   * @returns {Promise} - 公告详情
   */
  static getAnnouncementDetail(id) {
    return request({
      url: `/announcement/${id}`,
      method: 'GET'
    });
  }

  /**
   * 获取功能分类列表
   * @returns {Promise} - 功能列表
   */
  static getDiseaseTags() {
    return request({
      url: '/diseaseTags/list',
      method: 'GET'
    });
  }

  /**
   * 获取协议内容
   * @param {String} type - 协议类型 (user, privacy)
   * @returns {Promise} - 协议内容
   */
  static getAgreement(type) {
    return request({
      url: '/config/agreement',
      method: 'GET',
      params: {
        type
      }
    });
  }
}

// 默认导出
export default {
  AnnouncementApi,
};