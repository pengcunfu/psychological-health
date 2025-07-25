Page({
  data: {
    tabs: [
      { name: '全部', status: '' },
      { name: '待付款', status: 'pending' },
      { name: '已完成', status: 'completed' },
      { name: '已取消', status: 'cancelled' }
    ],
    currentTab: 0,
    orderList: [],
    page: 1,
    pageSize: 10,
    hasMore: true,
    loadMoreStatus: 'loadmore',
    refreshing: false,
    statusMap: {
      'pending': '待付款',
      'paid': '已支付',
      'completed': '已完成',
      'cancelled': '已取消'
    }
  },

  onLoad() {
    this.loadOrders();
    // 临时使用模拟数据
    this.setData({
      orderList: this.mockOrders
    });
  },

  // 切换标签页
  switchTab(e) {
    const index = e.currentTarget.dataset.index;
    if (this.data.currentTab === index) return;
    
    this.setData({
      currentTab: index
    });
    this.resetList();
    this.loadOrders();
  },

  // 重置列表
  resetList() {
    this.setData({
      orderList: [],
      page: 1,
      hasMore: true,
      loadMoreStatus: 'loadmore'
    });
  },

  // 加载订单列表
  async loadOrders() {
    try {
      const { currentTab, tabs, page, pageSize } = this.data;
      const status = tabs[currentTab].status;

      // TODO: Replace with actual API call
      const res = await wx.cloud.callFunction({
        name: 'getOrders',
        data: {
          status,
          page,
          pageSize
        }
      });

      if (res.result && res.result.data) {
        this.setData({
          orderList: page === 1 ? res.result.data : [...this.data.orderList, ...res.result.data],
          hasMore: res.result.data.length === pageSize
        });
      }
    } catch (error) {
      console.error('加载订单列表失败:', error);
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    }
  },

  // 上拉加载更多
  loadMore() {
    if (!this.data.hasMore || this.data.loadMoreStatus === 'loading') return;
    
    this.setData({
      page: this.data.page + 1,
      loadMoreStatus: 'loading'
    });
    
    this.loadOrders().finally(() => {
      this.setData({
        loadMoreStatus: 'loadmore'
      });
    });
  },

  // 下拉刷新
  async onRefresh() {
    if (this.data.refreshing) return;
    
    this.setData({
      refreshing: true
    });
    
    this.resetList();
    await this.loadOrders();
    
    this.setData({
      refreshing: false
    });
  },

  // 支付订单
  payOrder(e) {
    const order = e.currentTarget.dataset.order;
    wx.navigateTo({
      url: '/pages/order/PayPedding/pay'
    });
  },

  // 取消订单
  async cancelOrder(e) {
    const order = e.currentTarget.dataset.order;
    try {
      const res = await wx.showModal({
        title: '提示',
        content: '确定要取消该订单吗？',
        confirmText: '确定',
        cancelText: '再想想'
      });

      if (res.confirm) {
        // TODO: Replace with actual API call
        await wx.cloud.callFunction({
          name: 'cancelOrder',
          data: { orderId: order.id }
        });

        wx.showToast({
          title: '取消成功',
          icon: 'success'
        });

        // 刷新订单列表
        this.resetList();
        this.loadOrders();
      }
    } catch (error) {
      console.error('取消订单失败:', error);
      wx.showToast({
        title: '取消失败',
        icon: 'none'
      });
    }
  },

  // 查看订单详情
  viewOrderDetails(e) {
    const order = e.currentTarget.dataset.order;
    wx.navigateTo({
      url: `/pages/order/detail/detail?id=${order.id}`
    });
  },

  // 学习课程
  studyCourse(e) {
    const order = e.currentTarget.dataset.order;
    wx.navigateTo({
      url: `/pages/course/study?id=${order.courseId}`
    });
  },

  // 模拟数据
  mockOrders: [
    {
      id: '1',
      orderNo: '042410621773',
      status: 'pending',
      type: 'counseling',
      title: '心理咨询服务（线上）',
      providerName: '李瑞峰',
      providerTitle: '高级心理咨询师',
      appointmentTime: '2023-10-10 14:00-14:50',
      price: 900
    },
    {
      id: '2',
      orderNo: '042410620981',
      status: 'paid',
      type: 'course',
      title: '情绪管理与心理健康',
      content: '12课时 | 共3小时',
      purchaseTime: '2023-09-25 18:30',
      price: 299,
      courseId: '101'
    },
    {
      id: '3',
      orderNo: '042410618765',
      status: 'completed',
      type: 'counseling',
      title: '心理咨询服务（线上）',
      providerName: '陈丽萍',
      providerTitle: '中级心理咨询师',
      appointmentTime: '2023-09-15 10:00-10:50',
      price: 600
    }
  ]
}); 