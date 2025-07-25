// pages/order/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    statusList: [{
      label: '全部',
      value: 'all'
    }, {
      label: '预约中',
      value: 'pending'
    }, {
      label: '进行中',
      value: 'ongoing'
    }, {
      label: '已完成',
      value: 'completed'
    }, {
      label: '已取消',
      value: 'cancelled'
    }],
    currentStatus: 'all',
    orderList: [],
    loading: false,
    refreshing: false,
    page: 1,
    pageSize: 10,
    hasMore: true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.loadOrders()
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    // 每次显示页面时刷新订单列表
    this.refreshOrders()
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },

  // 切换状态标签
  onTabChange(e) {
    const status = e.currentTarget.dataset.status
    this.setData({
      currentStatus: status,
      page: 1,
      orderList: []
    }, () => {
      this.loadOrders()
    })
  },

  // 加载订单列表
  async loadOrders() {
    if (this.data.loading) return
    
    this.setData({ loading: true })
    
    try {
      // TODO: 替换为实际的API调用
      const mockOrders = [{
        orderId: '031909438261',
        userName: '张三',
        createTime: '2022/03/19 09:57',
        type: '电话',
        appointmentDate: '2022-03-19 星期六',
        appointmentTime: '11:00-11:50',
        amount: '0.00',
        paymentMethod: '微信支付',
        status: 'pending',
        statusText: '预约中'
      }, {
        orderId: '031909475260',
        userName: '张三',
        createTime: '2022/03/19 09:33',
        type: '视频',
        appointmentDate: '2022-03-19 星期六',
        appointmentTime: '10:00-10:50',
        amount: '0.00',
        paymentMethod: '微信支付',
        status: 'pending',
        statusText: '预约中'
      }]

      // 模拟加载延迟
      await new Promise(resolve => setTimeout(resolve, 500))

      this.setData({
        orderList: this.data.page === 1 ? mockOrders : [...this.data.orderList, ...mockOrders],
        loading: false,
        hasMore: mockOrders.length === this.data.pageSize
      })
    } catch (error) {
      console.error('加载订单列表失败:', error)
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败，请重试',
        icon: 'none'
      })
    }
  },

  // 刷新订单列表
  async refreshOrders() {
    this.setData({
      page: 1,
      refreshing: true
    })
    
    await this.loadOrders()
    
    this.setData({ refreshing: false })
  },

  // 加载更多订单
  async onLoadMore() {
    if (this.data.loading || !this.data.hasMore) return
    
    this.setData({
      page: this.data.page + 1
    })
    
    await this.loadOrders()
  },

  // 查看订单详情
  onViewDetail(e) {
    const orderId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/order/detail/index?id=${orderId}`
    })
  },

  // 查看预约信息
  onViewAppointment(e) {
    const orderId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/order/appointment/index?id=${orderId}`
    })
  },

  // 开始咨询
  onStartConsultation(e) {
    const { id, type } = e.currentTarget.dataset
    
    if (type === '电话') {
      // 拨打电话
      wx.makePhoneCall({
        phoneNumber: '10086', // TODO: 替换为实际的电话号码
        fail(error) {
          console.error('拨打电话失败:', error)
          wx.showToast({
            title: '拨打电话失败，请重试',
            icon: 'none'
          })
        }
      })
    } else {
      // 进入咨询页面
      wx.navigateTo({
        url: `/pages/consultation/index?orderId=${id}`
      })
    }
  }
})