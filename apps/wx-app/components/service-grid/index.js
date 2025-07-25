const {
  getResource
} = require('../../utils/util')

Component({
  properties: {
    services: {
      type: Array,
      value: []
    },
    columns: {
      type: Number,
      value: 4
    },
    title: {
      type: String,
      value: ''
    },
    iconSize: {
      type: String,
      value: '60rpx'
    },
    textSize: {
      type: String,
      value: '24rpx'
    }
  },

  data: {
    defaultServices: [{
        id: 1,
        name: '找咨询师',
        icon: getResource('images/services/counselor.png'),
        url: '/pages/counselor/index',
        isTabBar: false
      },
      {
        id: 2,
        name: '心理测评',
        icon: getResource('images/services/check.png'),
        url: '/pages/test/index',
        isTabBar: false
      },
      {
        id: 3,
        name: '视频咨询',
        icon: getResource('images/services/video.png'),
        url: '/pages/video/index',
        isTabBar: false
      },
      {
        id: 4,
        name: '团体咨询',
        icon: getResource('images/services/group.png'),
        url: '/pages/group/index',
        isTabBar: false
      },
      {
        id: 5,
        name: '工作室',
        icon: getResource('images/services/workspace.png'),
        url: '/pages/workspace/index',
        isTabBar: false
      },
      {
        id: 6,
        name: '预约管理',
        icon: getResource('images/services/appointment.png'),
        url: '/pages/appointment/index',
        isTabBar: false
      },
      {
        id: 7,
        name: '在线咨询',
        icon: getResource('images/services/available.png'),
        url: '/pages/online/index',
        isTabBar: false
      },
      {
        id: 8,
        name: '个人成长',
        icon: getResource('images/services/growth.png'),
        url: '/pages/growth/index',
        isTabBar: false
      },
      {
        id: 9,
        name: '优惠活动',
        icon: getResource('images/services/discount.png'),
        url: '/pages/discount/index',
        isTabBar: false
      },
      {
        id: 10,
        name: '儿童心理',
        icon: getResource('images/services/children.png'),
        url: '/pages/children/index',
        isTabBar: false
      }
    ]
  },

  lifetimes: {
    attached() {
      // 如果没有传入服务数据，使用默认数据
      if (!this.data.services || this.data.services.length === 0) {
        this.setData({
          services: this.data.defaultServices
        });
      }
    }
  },

  methods: {
    // 点击服务项目
    onServiceTap(e) {
      const index = e.currentTarget.dataset.index;
      const service = this.data.services[index];

      if (service.path) {
        // 判断是否为 tabBar 页面
        const tabBarPages = [
          '/pages/index/index',
          '/pages/workspace/index',
          '/pages/message/index',
          '/pages/profile/user'
        ];

        if (tabBarPages.includes(service.path)) {
          wx.switchTab({
            url: service.path,
            fail: (err) => {
              console.error('跳转失败:', err);
              wx.showToast({
                title: '页面跳转失败',
                icon: 'none'
              });
            }
          });
        } else {
          wx.navigateTo({
            url: service.path,
            fail: (err) => {
              console.error('跳转失败:', err);
              wx.showToast({
                title: '页面跳转失败',
                icon: 'none'
              });
            }
          });
        }
      }

      // 触发点击事件，让父组件也能处理
      this.triggerEvent('serviceclick', {
        service,
        index
      });
    }
  }
});