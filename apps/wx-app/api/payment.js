/**
 * 支付管理API类
 */
class PaymentApi {
  /**
   * 创建支付订单
   * @param {Object} data - 支付信息 {orderId, paymentMethod}
   * @returns {Promise} - 支付参数
   */
  static createPayment(data) {
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
  static getPaymentStatus(orderId) {
    return request({
      url: '/payment/status',
      method: 'GET',
      params: {
        orderId
      }
    });
  }

  /**
   * 申请退款
   * @param {Object} data - 退款信息 {orderId, reason}
   * @returns {Promise} - 退款结果
   */
  static requestRefund(data) {
    return request({
      url: '/payment/refund',
      method: 'POST',
      data
    });
  }
}

// 默认导出
export default {
  PaymentApi,
};