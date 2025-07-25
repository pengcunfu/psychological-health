Page({
  data: {
    counselorName: '王医生',
    counselorAvatar: 'https://randomuser.me/api/portraits/women/68.jpg',
    currentDate: '',
    todayAppointments: {
      pending: 3,
      completed: 2
    },
    pendingRequests: 5,
    unreadMessages: 8,
    todaySchedule: [
      {
        timeSlot: '09:00-10:00',
        clientName: '张先生',
        serviceType: '个人咨询',
        status: 'pending'
      },
      {
        timeSlot: '11:00-12:00',
        clientName: '李女士',
        serviceType: '情绪管理',
        status: 'completed'
      },
      {
        timeSlot: '14:00-15:00',
        clientName: '刘先生',
        serviceType: '压力疏导',
        status: 'pending'
      },
      {
        timeSlot: '16:00-17:00',
        clientName: '陈女士',
        serviceType: '关系咨询',
        status: 'pending'
      }
    ],
    income: {
      weekly: 2800,
      monthly: 12600
    },
    latestReviews: [
      {
        clientName: '匿名用户',
        rating: 5,
        content: '非常专业的咨询，给了我很多实用的建议，感谢医生！',
        time: '2小时前'
      },
      {
        clientName: '李**',
        rating: 4.5,
        content: '咨询过程很舒适，医生很有耐心。下次还会继续预约。',
        time: '昨天'
      }
    ]
  },

  onLoad() {
    this.setCurrentDate();
    this.fetchDashboardData();
  },

  onShow() {
    // 每次页面显示时刷新数据
    this.fetchDashboardData();
  },

  setCurrentDate() {
    const date = new Date();
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    const weekday = weekdays[date.getDay()];
    this.setData({
      currentDate: `${year}年${month}月${day}日 ${weekday}`
    });
  },

  getStatusText(status) {
    const statusMap = {
      pending: '待接待',
      completed: '已完成',
      canceled: '已取消'
    };
    return statusMap[status] || status;
  },

  navigateTo(e) {
    const url = e.currentTarget.dataset.url;
    wx.navigateTo({ url });
  },

  async fetchDashboardData() {
    try {
      wx.showLoading({
        title: '加载中...',
        mask: true
      });

      // TODO: 替换为实际的API调用
      // const response = await wx.cloud.callFunction({
      //   name: 'getCounselorDashboard'
      // });
      
      // 模拟API响应数据
      const mockData = {
        counselorInfo: {
          name: '王医生',
          avatar: 'https://randomuser.me/api/portraits/women/68.jpg'
        },
        todayAppointments: {
          pending: 3,
          completed: 2
        },
        pendingRequests: 5,
        unreadMessages: 8,
        todaySchedule: [
          {
            timeSlot: '09:00-10:00',
            clientName: '张先生',
            serviceType: '个人咨询',
            status: 'pending'
          },
          {
            timeSlot: '11:00-12:00',
            clientName: '李女士',
            serviceType: '情绪管理',
            status: 'completed'
          }
        ],
        income: {
          weekly: 2800,
          monthly: 12600
        },
        latestReviews: [
          {
            clientName: '匿名用户',
            rating: 5,
            content: '非常专业的咨询，给了我很多实用的建议，感谢医生！',
            time: '2小时前'
          }
        ]
      };

      // 更新页面数据
      this.setData({
        counselorName: mockData.counselorInfo.name,
        counselorAvatar: mockData.counselorInfo.avatar,
        todayAppointments: mockData.todayAppointments,
        pendingRequests: mockData.pendingRequests,
        unreadMessages: mockData.unreadMessages,
        todaySchedule: mockData.todaySchedule,
        income: mockData.income,
        latestReviews: mockData.latestReviews
      });

    } catch (error) {
      console.error('获取仪表盘数据失败:', error);
      wx.showToast({
        title: '获取数据失败',
        icon: 'none'
      });
    } finally {
      wx.hideLoading();
    }
  }
});