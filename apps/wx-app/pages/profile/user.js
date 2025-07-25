const { getResource } = require('../../utils/util')

Page({
  data: {
    userInfo: {
      avatar: '',
      name: '',
      counselorTitle: '球球' // 测试数据
    },
    badges: {
      ongoing: 1,  // 测试数据
      orders: 4    // 测试数据
    }
  },

  onLoad() {
    this.loadUserInfo()
  },

  onShow() {
    this.loadBadges()
  },

  // 加载用户信息
  loadUserInfo() {
    // TODO: 调用获取用户信息接口
    // 这里使用模拟数据
    const userInfo = {
      avatar: getResource('images/test.png'),
      name: '元东',
      counselorTitle: '球球'
    }
    this.setData({ userInfo })
  },

  // 加载徽标数据
  loadBadges() {
    // TODO: 调用获取徽标数据接口
    // 这里使用模拟数据
    const badges = {
      ongoing: 1,
      orders: 4
    }
    this.setData({ badges })
  },

  // 扫码
  onScanQRCode() {
    wx.scanCode({
      success: (res) => {
        console.log('扫码结果：', res)
        // TODO: 处理扫码结果
      }
    })
  },

  // 跳转到编辑资料
  onEditProfile() {
    wx.navigateTo({
      url: '/pages/profile/edit/index'
    })
  }
})