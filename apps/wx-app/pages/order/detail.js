Page({
  data: {
    loading: true,
    orderDetail: null,
    orderStatusMap: {
      UNPAID: {
        text: '待支付',
        color: '#ff9500'
      },
      PAID: {
        text: '已支付',
        color: '#07c160'
      },
      COMPLETED: {
        text: '已完成',
        color: '#07c160'
      },
      CANCELLED: {
        text: '已取消',
        color: '#999999'
      },
      REFUNDING: {
        text: '退款中',
        color: '#ff9500'
      },
      REFUNDED: {
        text: '已退款',
        color: '#999999'
      }
    }
  },

  onLoad(options) {
    if (options.orderId) {
      this.loadOrderDetail(options.orderId);
    } else {
      wx.showToast({
        title: '订单ID不存在',
        icon: 'none'
      });
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
    }
  },

  async loadOrderDetail(orderId) {
    try {
      // TODO: Replace with actual API call
      const res = await wx.cloud.callFunction({
        name: 'getOrderDetail',
        data: { orderId }
      });

      if (res.result && res.result.data) {
        this.setData({
          orderDetail: res.result.data,
          loading: false
        });
      } else {
        throw new Error('获取订单详情失败');
      }
    } catch (error) {
      console.error('加载订单详情失败:', error);
      wx.showToast({
        title: '加载订单详情失败',
        icon: 'none'
      });
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
    }
  },

  copyOrderNo() {
    const { orderNo } = this.data.orderDetail;
    wx.setClipboardData({
      data: orderNo,
      success: () => {
        wx.showToast({
          title: '复制成功',
          icon: 'success'
        });
      }
    });
  },

  async cancelOrder() {
    try {
      await wx.showModal({
        title: '提示',
        content: '确定要取消该订单吗？',
        confirmText: '确定',
        cancelText: '再想想'
      });

      // TODO: Replace with actual API call
      await wx.cloud.callFunction({
        name: 'cancelOrder',
        data: { orderId: this.data.orderDetail._id }
      });

      wx.showToast({
        title: '取消成功',
        icon: 'success'
      });

      // 重新加载订单详情
      this.loadOrderDetail(this.data.orderDetail._id);
    } catch (error) {
      console.error('取消订单失败:', error);
      wx.showToast({
        title: '取消订单失败',
        icon: 'none'
      });
    }
  },

  async goToPay() {
    try {
      // TODO: Replace with actual payment API call
      const res = await wx.cloud.callFunction({
        name: 'createPayment',
        data: { orderId: this.data.orderDetail._id }
      });

      if (res.result && res.result.payment) {
        await wx.requestPayment(res.result.payment);
        
        wx.showToast({
          title: '支付成功',
          icon: 'success'
        });

        // 重新加载订单详情
        this.loadOrderDetail(this.data.orderDetail._id);
      } else {
        throw new Error('创建支付失败');
      }
    } catch (error) {
      console.error('支付失败:', error);
      if (error.errMsg !== 'requestPayment:fail cancel') {
        wx.showToast({
          title: '支付失败',
          icon: 'none'
        });
      }
    }
  },

  goToService() {
    const { serviceId } = this.data.orderDetail;
    wx.navigateTo({
      url: `/pages/service/detail/detail?id=${serviceId}`
    });
  },

  contactProvider() {
    const { providerId } = this.data.orderDetail;
    // TODO: Implement provider contact logic
    wx.showToast({
      title: '联系咨询师功能开发中',
      icon: 'none'
    });
  },

  goToChat() {
    const { providerId } = this.data.orderDetail;
    wx.navigateTo({
      url: `/pages/chat/chat?targetId=${providerId}`
    });
  },

  formatDate(timestamp) {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
  },

  formatPrice(price) {
    return price ? (price / 100).toFixed(2) : '0.00';
  }
}); 