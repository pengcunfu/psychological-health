Page({
  data: {
    orderInfo: {
      price: 900.00,
      serviceType: '咨询服务费用',
      orderNumber: '202310159374559',
      orderTime: '2023-10-15 14:35:26',
      counselorName: '李瑞峰',
      counselorTitle: '高级心理咨询师',
      serviceTitle: '一对一心理咨询（50分钟）',
      appointmentTime: '2023-10-18 14:00-14:50'
    },
    paymentMethod: 'wechat'
  },

  onLoad(options) {
    if (options.orderId) {
      this.loadOrderInfo(options.orderId);
    } else {
      wx.showToast({
        title: '订单参数错误',
        icon: 'none'
      });
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
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
      } else {
        throw new Error('获取订单信息失败');
      }
    } catch (error) {
      console.error('加载订单信息失败:', error);
      wx.showToast({
        title: '加载订单信息失败',
        icon: 'none'
      });
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
    }
  },

  selectPayment(e) {
    const method = e.currentTarget.dataset.method;
    this.setData({
      paymentMethod: method
    });
  },

  copyOrderNumber() {
    const { orderNumber } = this.data.orderInfo;
    wx.setClipboardData({
      data: orderNumber,
      success: () => {
        wx.showToast({
          title: '订单号已复制',
          icon: 'success'
        });
      }
    });
  },

  async confirmPayment() {
    const { paymentMethod } = this.data;
    
    try {
      if (paymentMethod === 'wechat') {
        wx.showLoading({
          title: '正在调起微信支付...'
        });

        // TODO: Replace with actual payment API call
        const res = await wx.cloud.callFunction({
          name: 'createPayment',
          data: {
            orderId: this.data.orderInfo.orderNumber,
            paymentMethod: 'wechat'
          }
        });

        if (res.result && res.result.payment) {
          await wx.requestPayment(res.result.payment);
          
          wx.hideLoading();
          wx.showToast({
            title: '支付成功',
            icon: 'success'
          });

          // 跳转到支付成功页面
          wx.redirectTo({
            url: '/pages/order/PaySuccess/index'
          });
        } else {
          throw new Error('创建支付失败');
        }
      } else if (paymentMethod === 'alipay') {
        wx.showToast({
          title: '暂不支持支付宝支付',
          icon: 'none'
        });
      }
    } catch (error) {
      console.error('支付失败:', error);
      wx.hideLoading();
      
      if (error.errMsg !== 'requestPayment:fail cancel') {
        wx.showToast({
          title: '支付失败',
          icon: 'none'
        });
      }
    }
  }
}); 