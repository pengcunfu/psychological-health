Page({
  data: {
    // 选项卡数据
    tabs: ['简介', '评价', '预约'],
    currentTab: 0,

    // 咨询师数据
    counselor: {
      id: 'c001',
      name: '李瑞峰',
      level: '高级咨询师',
      title: '中国心理学会注册心理师 | 国家二级心理咨询师',
      expertise: ['焦虑抑郁', '职场压力', '婚恋关系', '个人成长'],
      stats: {
        rating: 4.9,
        experience: '18年',
        sessions: '15700+'
      },
      introduction: {
        expertise: '焦虑抑郁、情绪管理、职场压力、婚恋关系问题、人际关系、自我成长',
        methods: '认知行为疗法(CBT)、接纳与承诺疗法(ACT)、正念减压疗法、叙事疗法'
      },
      service: {
        duration: '50分钟/次',
        type: '线上视频、线下面对面',
        frequency: '建议每周一次，根据具体情况调整',
        refund: '未开始咨询前24小时可全额退款，24小时内退款80%'
      },
      price: 900
    }
  },

  onLoad(options) {
    // 从服务器获取咨询师详情
    this.loadCounselorDetail(options.id);
  },

  // 加载咨询师详情
  loadCounselorDetail(id) {
    // TODO: 替换为实际的API调用
    console.log('加载咨询师ID:', id);
  },

  // 切换选项卡
  switchTab(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({
      currentTab: index
    });
  },

  // 返回上一页
  goBack() {
    wx.navigateBack();
  },

  // 预约咨询师
  handleBooking() {
    wx.navigateTo({
      url: `/pages/counselor/booking/booking?counselorId=${this.data.counselor.id}`
    });
  }
}); 