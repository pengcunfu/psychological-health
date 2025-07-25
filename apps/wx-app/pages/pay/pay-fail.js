Page({
  data: {
    orderNo: '',
    serviceName: '',
    amount: '',
    createTime: '',
    failReason: '',
    fromPage: ''
  },

  onLoad(options) {
    const {
      orderNo,
      serviceName,
      amount,
      createTime,
      failReason,
      fromPage
    } = options

    this.setData({
      orderNo: orderNo || '',
      serviceName: serviceName || '',
      amount: amount || '0.00',
      createTime: createTime || '',
      failReason: decodeURIComponent(failReason || ''),
      fromPage: fromPage || ''
    })
  },

  // 返回按钮点击
  goBack() {
    // 如果有指定返回页面，则跳转到指定页面
    if (this.data.fromPage) {
      wx.redirectTo({
        url: this.data.fromPage
      })
      return
    }

    // 否则返回上一页
    const pages = getCurrentPages()
    if (pages.length > 1) {
      wx.navigateBack()
    } else {
      wx.switchTab({
        url: '/pages/index/index'
      })
    }
  },

  // 重新支付
  async retryPay() {
    if (!this.data.orderNo) {
      wx.showToast({
        title: '订单信息不完整',
        icon: 'none'
      })
      return
    }

    wx.showLoading({
      title: '加载中...'
    })

    try {
      // 获取支付参数
      const res = await wx.cloud.callFunction({
        name: 'getPayParams',
        data: {
          orderNo: this.data.orderNo
        }
      })

      if (!res.result || !res.result.payParams) {
        throw new Error('获取支付参数失败')
      }

      // 发起支付
      await wx.requestPayment({
        ...res.result.payParams,
        success: () => {
          // 支付成功，跳转到支付成功页
          wx.redirectTo({
            url: `/pages/pay/pay-success?orderNo=${this.data.orderNo}&serviceName=${this.data.serviceName}&amount=${this.data.amount}`
          })
        },
        fail: (error) => {
          console.error('支付失败:', error)
          // 更新失败原因
          this.setData({
            failReason: '支付未完成，请重试'
          })
        }
      })
    } catch (error) {
      console.error('重新支付失败:', error)
      wx.showToast({
        title: '支付失败，请重试',
        icon: 'none'
      })
    } finally {
      wx.hideLoading()
    }
  },

  // 联系客服
  contactService() {
    wx.navigateTo({
      url: '/pages/contact/service/index'
    })
  }
}) 