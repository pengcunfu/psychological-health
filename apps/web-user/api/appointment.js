import request from '../utils/request';

/**
 * 创建预约
 * @param {Object} data - 预约信息 {counselorId, serviceId, userId, date, timeSlot, note}
 * @returns {Promise} - 创建结果
 */
export function createAppointment(data) {
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
export function getUserAppointments(userId, params = {}) {
  return request({
    url: '/orders/appointments',
    method: 'GET',
    params: { ...params, userId }
  });
}

/**
 * 获取预约详情
 * @param {String} orderId - 订单ID
 * @returns {Promise} - 预约详情
 */
export function getAppointmentDetail(orderId) {
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
export function cancelAppointment(appointmentId) {
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
export function updateAppointment(appointmentId, data) {
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
export function getAppointmentStatistics(userId) {
  return request({
    url: '/appointment/statistics',
    method: 'GET',
    params: { userId }
  });
}

/**
 * 创建支付订单
 * @param {Object} data - 支付信息 {orderId, paymentMethod}
 * @returns {Promise} - 支付参数
 */
export function createPayment(data) {
  return request({
    url: '/payment/create',
    method: 'POST',
    data
  });
}

/**
 * 查询支付状态
 * @param {String} orderId - 订单ID
 * @returns {Promise} - 支付状态
 */
export function getPaymentStatus(orderId) {
  return request({
    url: '/payment/status',
    method: 'GET',
    params: { orderId }
  });
}

/**
 * 申请退款
 * @param {Object} data - 退款信息 {orderId, reason}
 * @returns {Promise} - 退款结果
 */
export function requestRefund(data) {
  return request({
    url: '/payment/refund',
    method: 'POST',
    data
  });
}

export default {
  createAppointment,
  getUserAppointments,
  getAppointmentDetail,
  cancelAppointment,
  updateAppointment,
  getAppointmentStatistics,
  createPayment,
  getPaymentStatus,
  requestRefund
}; 