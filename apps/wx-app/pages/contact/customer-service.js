Page({
  data: {
    // 页面数据
  },

  // 拨打电话
  makePhoneCall() {
    wx.makePhoneCall({
      phoneNumber: '400-123-4567',
      success: () => {
        console.log('拨打电话成功');
      },
      fail: (error) => {
        console.log('拨打电话失败', error);
      }
    });
  },

  // 复制邮箱
  copyEmail() {
    wx.setClipboardData({
      data: 'support@meiguang.com',
      success: () => {
        wx.showToast({
          title: '邮箱已复制',
          icon: 'success'
        });
      }
    });
  },

  // 复制微信
  copyWechat() {
    wx.setClipboardData({
      data: '美广心理健康',
      success: () => {
        wx.showToast({
          title: '公众号已复制',
          icon: 'success'
        });
      }
    });
  },

  // 跳转到在线咨询页面
  navigateToService() {
    wx.navigateTo({
      url: '/pages/contact/service/index'
    });
  }
}); 