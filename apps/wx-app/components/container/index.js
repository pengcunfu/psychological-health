const {
  getResource
} = require('../../utils/util')

Component({
  options: {
    multipleSlots: true // 启用多slot支持
  },

  properties: {
    // 导航栏配置
    showNavBar: {
      type: Boolean,
      value: true
    },
    navBarTitle: {
      type: String,
      value: '武志红心理咨询中心'
    },
    showBack: {
      type: Boolean,
      value: true
    },
    customBack: {
      type: Boolean,
      value: false
    },
    // 是否使用导航栏插槽
    useSlotLeft: {
      type: Boolean,
      value: false
    },
    useSlotCenter: {
      type: Boolean,
      value: false
    },
    useSlotRight: {
      type: Boolean,
      value: false
    },
    // 标签栏配置
    showTabBar: {
      type: Boolean,
      value: false
    },
    // 当前选中的标签页索引
    activeTab: {
      type: Number,
      value: 0
    }
  },

  data: {
    // 标签栏配置
    tabs: [{
        icon: getResource('images/tabbar/home.svg'),
        activeIcon: getResource('images/tabbar/home-active.svg'),
        text: '首页',
        path: '/pages/index/index'
      },
      {
        icon: getResource('images/tabbar/counselor.svg'),
        activeIcon: getResource('images/tabbar/counselor-active.svg'),
        text: '咨询师',
        path: '/pages/workspace/index'
      },
      {
        icon: getResource('images/tabbar/message.svg'),
        activeIcon: getResource('images/tabbar/message-active.svg'),
        text: '消息',
        path: '/pages/message/index'
      },
      {
        icon: getResource('images/tabbar/profile.svg'),
        activeIcon: getResource('images/tabbar/profile-active.svg'),
        text: '我的',
        path: '/pages/profile/user'
      }
    ]
  },

  methods: {
    // 返回按钮点击事件
    onBack() {
      if (this.data.customBack) {
        // 如果使用自定义返回，触发事件让页面处理
        this.triggerEvent('back')
      } else {
        // 默认返回逻辑
        const pages = getCurrentPages()
        if (pages.length > 1) {
          wx.navigateBack()
        } else {
          wx.switchTab({
            url: '/pages/index/index'
          })
        }
      }
    }
  }
})