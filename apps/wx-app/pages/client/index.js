Page({
  data: {
    // 主题色变量
    themeColors: {
      primary: '#E2AA59',
      primaryDark: '#D19845',
      primaryLight: '#F1C88B',
      primaryBg: '#F9EFD6',
      success: '#4CAF50',
      info: '#2196F3',
      warning: '#FF9800',
      error: '#F44336'
    },
    searchQuery: '',
    activeFilter: 'all',
    pageSize: 10,
    currentPage: 1,
    clients: [
      {
        id: 'c001',
        name: '张女士',
        gender: 'female',
        age: 28,
        phone: '138****1234',
        email: 'zhang@example.com',
        sessionCount: 5,
        firstSession: '2023-06-15',
        lastSession: '2023-09-05',
        nextSession: '2023-09-20',
        tags: ['焦虑症', '工作压力', '需跟进'],
        notes: '对工作压力很敏感，需要帮助建立应对机制',
        avatarColor: '#E2AA59'
      },
      {
        id: 'c002',
        name: '李先生',
        gender: 'male',
        age: 35,
        phone: '139****5678',
        email: 'li@example.com',
        sessionCount: 3,
        firstSession: '2023-07-20',
        lastSession: '2023-09-01',
        nextSession: null,
        tags: ['抑郁症', '家庭问题'],
        notes: '正在经历离婚，需情绪支持',
        avatarColor: '#F44336'
      },
      {
        id: 'c003',
        name: '王女士',
        gender: 'female',
        age: 42,
        phone: '136****9012',
        email: 'wang@example.com',
        sessionCount: 8,
        firstSession: '2023-03-10',
        lastSession: '2023-08-28',
        nextSession: '2023-09-18',
        tags: ['慢性焦虑', '亲子关系'],
        notes: '与青春期孩子存在沟通问题',
        avatarColor: '#4CAF50'
      },
      {
        id: 'c004',
        name: '赵先生',
        gender: 'male',
        age: 31,
        phone: '135****3456',
        email: 'zhao@example.com',
        sessionCount: 2,
        firstSession: '2023-08-05',
        lastSession: '2023-08-19',
        nextSession: '2023-09-15',
        tags: ['职场适应', '社交压力'],
        notes: '刚换工作，面临适应性挑战',
        avatarColor: '#2196F3'
      },
      {
        id: 'c005',
        name: '陈女士',
        gender: 'female',
        age: 27,
        phone: '137****7890',
        email: 'chen@example.com',
        sessionCount: 4,
        firstSession: '2023-05-25',
        lastSession: '2023-08-25',
        nextSession: null,
        tags: ['恋爱问题', '自我认同'],
        notes: '走出失恋阴影，重建自我价值感',
        avatarColor: '#9C27B0'
      }
    ]
  },

  onLoad() {
    // 为每个客户生成头像颜色
    const clients = this.data.clients.map(client => ({
      ...client,
      avatarColor: this.getAvatarColor(client.name)
    }));
    this.setData({ clients });
    this.filterClients();
  },

  // 获取头像背景色
  getAvatarColor(name) {
    const colors = [
      this.data.themeColors.primary,
      this.data.themeColors.error,
      this.data.themeColors.success,
      this.data.themeColors.info,
      '#9C27B0'
    ];

    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }

    return colors[Math.abs(hash) % colors.length];
  },

  // 设置筛选条件
  setFilter(e) {
    const filter = e.currentTarget.dataset.filter;
    this.setData({
      activeFilter: filter,
      currentPage: 1
    });
    this.filterClients();
  },

  // 筛选客户列表
  filterClients() {
    let result = [...this.data.clients];

    // 搜索过滤
    if (this.data.searchQuery) {
      const query = this.data.searchQuery.toLowerCase();
      result = result.filter(client =>
        client.name.toLowerCase().includes(query) ||
        client.phone.includes(query)
      );
    }

    // 标签过滤
    switch (this.data.activeFilter) {
      case 'recent':
        // 最近30天内有咨询的客户
        const thirtyDaysAgo = new Date();
        thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
        result = result.filter(client => {
          const lastSession = new Date(client.lastSession);
          return lastSession >= thirtyDaysAgo;
        });
        break;
      case 'frequent':
        // 咨询次数大于平均值的客户
        const avgSessions = this.data.clients.reduce((sum, client) => sum + client.sessionCount, 0) / this.data.clients.length;
        result = result.filter(client => client.sessionCount > avgSessions);
        break;
      case 'followup':
        // 标记为需要跟进的客户
        result = result.filter(client =>
          client.tags && client.tags.some(tag => tag.includes('跟进'))
        );
        break;
    }

    this.setData({
      filteredClients: result,
      displayClients: result.slice(0, this.data.currentPage * this.data.pageSize)
    });
  },

  // 加载更多
  loadMore() {
    if (this.hasMoreClients()) {
      this.setData({
        currentPage: this.data.currentPage + 1
      });
      this.filterClients();
    }
  },

  // 是否还有更多客户
  hasMoreClients() {
    return this.data.displayClients.length < this.data.filteredClients.length;
  },

  // 查看客户详情
  viewClientDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/counselor/clients/detail?id=${id}`
    });
  },

  // 拨打电话
  callClient(e) {
    const phone = e.currentTarget.dataset.phone.replace(/\*+/g, '0');
    wx.makePhoneCall({
      phoneNumber: phone,
      success: () => {
        console.log('拨打电话成功');
      },
      fail: (err) => {
        console.error('拨打电话失败', err);
        wx.showToast({
          title: '拨打电话失败',
          icon: 'none'
        });
      }
    });
  },

  // 发送消息
  messageClient(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/counselor/messages?clientId=${id}`
    });
  },

  // 预约咨询
  scheduleAppointment(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/counselor/appointments/schedule?clientId=${id}`
    });
  },

  // 查看咨询记录
  viewNotes(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/counselor/clients/notes?clientId=${id}`
    });
  }
}); 