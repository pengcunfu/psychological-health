import request from '../utils/request';

/**
 * 预约管理API类
 */
class AppointmentApi {
  /**
   * 创建预约
   * @param {Object} data - 预约信息 {counselorId, serviceId, userId, date, timeSlot, note}
   * @returns {Promise} - 创建结果
   */
  static createAppointment(data) {
    return request({
      url: '/appointment/create',
      method: 'POST',
      data
    });
  }

  /**
   * 获取用户预约列表
   * @param {String} userId - 用户ID
   * @param {Object} params - 查询参数 {status, page, pageSize}
   * @returns {Promise} - 预约列表
   */
  static getUserAppointments(userId, params = {}) {
    return request({
      url: '/orders/appointments',
      method: 'GET',
      params: {
        ...params,
        userId
      }
    });
  }

  /**
   * 获取预约详情
   * @param {String} orderId - 订单ID
   * @returns {Promise} - 预约详情
   */
  static getAppointmentDetail(orderId) {
    return request({
      url: `/orders/${orderId}`,
      method: 'GET'
    });
  }

  /**
   * 取消预约
   * @param {String} appointmentId - 预约ID
   * @returns {Promise} - 取消结果
   */
  static cancelAppointment(appointmentId) {
    return request({
      url: `/appointment/cancel/${appointmentId}`,
      method: 'PUT'
    });
  }

  /**
   * 更新预约信息
   * @param {String} appointmentId - 预约ID
   * @param {Object} data - 更新数据 {date, timeSlot, note}
   * @returns {Promise} - 更新结果
   */
  static updateAppointment(appointmentId, data) {
    return request({
      url: `/appointment/update/${appointmentId}`,
      method: 'PUT',
      data
    });
  }

  /**
   * 获取用户预约统计
   * @param {String} userId - 用户ID
   * @returns {Promise} - 统计数据
   */
  static getAppointmentStatistics(userId) {
    return request({
      url: '/appointment/statistics',
      method: 'GET',
      params: {
        userId
      }
    });
  }
}

// 默认导出
export default {
  AppointmentApi,
};