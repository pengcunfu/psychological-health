import api from '@/utils/api'

// 订单管理API
export const orderAPI = {
  // 获取订单列表
  getOrders: (params) => api.get('/order', { params }),

  // 获取订单详情
  getOrder: (id) => api.get(`/order/${id}`),

  // 更新订单状态
  updateOrderStatus: (id, status) => api.put(`/order/${id}/status`, { status }),

  // 取消订单
  cancelOrder: (id, reason) => api.post(`/order/${id}/cancel`, { reason }),

  // 退款
  refundOrder: (id, data) => api.post(`/order/${id}/refund`, data),

  // 获取订单统计
  getOrderStats: (params) => api.get('/order/stats', { params })
}

export default orderAPI 