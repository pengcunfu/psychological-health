Page({
  data: {
    orderInfo: {
      orderNo: '202310159374559',
      paymentMethod: '微信支付',
      price: 900.00,
      counselorName: '李瑞峰',
      appointmentTime: '2023-10-18 14:00-14:50'
    }
  },

  onLoad(options) {
    if (options.orderId) {
      this.loadOrderInfo(options.orderId);
    }
  },

  async loadOrderInfo(orderId) {
    try {
      // TODO: Replace with actual API call
      const res = await wx.cloud.callFunction({
        name: 'getOrderInfo',
        data: { orderId }
      });

      if (res.result && res.result.data) {
        this.setData({
          orderInfo: res.result.data
        });
      }
    } catch (error) {
      console.error('加载订单信息失败:', error);
      wx.showToast({
        title: '加载订单信息失败',
        icon: 'none'
      });
    }
  },

  viewOrder() {
    wx.navigateTo({
      url: '/pages/order/index'
    });
  },

  goHome() {
    wx.switchTab({
      url: '/pages/index/index'
    });
  }
}); 