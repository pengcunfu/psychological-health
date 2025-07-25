Page({
  data: {
    // 问题类型选择
    problemTypes: ['预约相关', '账号问题', '支付问题', '其他问题'],
    problemTypeIndex: -1,

    // 留言内容字数
    contentLength: 0,

    // 常见问题列表
    faqList: [
      {
        title: '如何修改预约时间？',
        content: '您可以在"我的预约"中找到需要修改的预约，点击"修改预约"按钮进行时间调整。请注意，预约开始前24小时内不可修改。',
        expanded: false
      },
      {
        title: '忘记密码怎么办？',
        content: '您可以通过手机号验证码登录，或点击登录页面的"忘记密码"，通过手机号重置密码。',
        expanded: false
      },
      {
        title: '如何申请退款？',
        content: '如需退款，请在"我的订单"中找到相应订单，点击"申请退款"。未开始的咨询可全额退款，已开始的咨询将根据实际情况处理。',
        expanded: false
      },
      {
        title: '课程有效期是多久？',
        content: '一般课程的有效期为购买后6个月。具体有效期请以课程详情页显示为准。如有特殊情况，可联系客服处理。',
        expanded: false
      }
    ]
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

  // 选择问题类型
  onProblemTypeChange(e) {
    this.setData({
      problemTypeIndex: e.detail.value
    });
  },

  // 监听留言内容输入
  onContentInput(e) {
    const value = e.detail.value;
    this.setData({
      contentLength: value.length
    });
  },

  // 展开/收起常见问题
  toggleFaq(e) {
    const index = e.currentTarget.dataset.index;
    const faqList = this.data.faqList;
    faqList[index].expanded = !faqList[index].expanded;
    this.setData({ faqList });
  },

  // 提交留言
  onSubmit(e) {
    const formData = e.detail.value;
    
    // 表单验证
    if (this.data.problemTypeIndex === -1) {
      this.showToast('请选择问题类型');
      return;
    }
    if (!formData.content) {
      this.showToast('请输入留言内容');
      return;
    }
    if (!formData.contact) {
      this.showToast('请输入联系方式');
      return;
    }

    // 构建提交数据
    const submitData = {
      type: this.data.problemTypes[this.data.problemTypeIndex],
      content: formData.content,
      contact: formData.contact
    };

    console.log('提交数据：', submitData);

    // TODO: 调用后端API提交数据
    wx.showLoading({
      title: '提交中...',
      mask: true
    });

    // 模拟提交
    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '提交成功',
        icon: 'success',
        duration: 2000,
        success: () => {
          // 重置表单
          this.setData({
            problemTypeIndex: -1,
            contentLength: 0
          });
          // 延迟返回上一页
          setTimeout(() => {
            wx.navigateBack();
          }, 2000);
        }
      });
    }, 1500);
  },

  // 显示提示
  showToast(title) {
    wx.showToast({
      title,
      icon: 'none',
      duration: 2000
    });
  }
}); 