const { getResource } = require('../../utils/util')

Page({
  data: {
    counselorId: null,
    selectedType: null,
    selectedMethod: null,
    selectedTimeSlot: null,
    totalPrice: 0,
    canSubmit: false,
    accountInfo: null,

    // 咨询类型列表
    consultTypes: [
      { id: 1, name: '个人成长', price: 800 },
      { id: 2, name: '情感咨询', price: 800 },
      { id: 3, name: '职业规划', price: 800 }
    ],

    // 咨询方式列表
    consultMethods: [
      { id: 1, name: '视频', icon: getResource('images/video.png') },
      { id: 2, name: '语音', icon: getResource('images/audio.png') }
    ],

    // 可约时间列表
    availableDates: [
      {
        date: '6-29',
        week: '周日',
        isFull: true,
        slots: []
      },
      {
        date: '6-30',
        week: '周一',
        isFull: false,
        slots: [
          { time: '16:00', selected: false, disabled: false },
          { time: '17:00', selected: false, disabled: false }
        ]
      },
      {
        date: '7-1',
        week: '周二',
        isFull: false,
        slots: []
      },
      {
        date: '7-2',
        week: '周三',
        isFull: false,
        slots: [
          { time: '9:00', selected: false, disabled: false },
          { time: '11:00', selected: false, disabled: false }
        ]
      },
      {
        date: '7-3',
        week: '周四',
        isFull: true,
        slots: []
      }
    ]
  },

  onLoad(options) {
    if (options.counselorId) {
      this.setData({
        counselorId: options.counselorId
      });
      this.loadAvailableTime(options.counselorId);
    }
  },

  // 加载可约时间
  loadAvailableTime(counselorId) {
    // TODO: 从服务器获取咨询师可约时间
  },

  // 新增账户
  onAddAccount() {
    const appointmentId = new Date().getTime(); // 生成临时ID
    wx.navigateTo({
      url: `/pages/account/add?appointmentId=${appointmentId}`
    });
  },

  // 选择咨询类型
  onSelectType(e) {
    const typeId = e.currentTarget.dataset.id;
    this.setData({
      selectedType: typeId
    });
    this.updateSubmitState();
  },

  // 选择咨询方式
  onSelectMethod(e) {
    const methodId = e.currentTarget.dataset.id;
    this.setData({
      selectedMethod: methodId
    });
    this.updateSubmitState();
  },

  // 选择时间段
  onSelectTimeSlot(e) {
    const { date, time } = e.currentTarget.dataset;
    
    // 更新选中状态
    const availableDates = this.data.availableDates.map(dateItem => {
      if (dateItem.date === date) {
        return {
          ...dateItem,
          slots: dateItem.slots.map(slot => ({
            ...slot,
            selected: slot.time === time
          }))
        };
      }
      return {
        ...dateItem,
        slots: dateItem.slots.map(slot => ({
          ...slot,
          selected: false
        }))
      };
    });

    this.setData({
      availableDates,
      selectedTimeSlot: { date, time }
    });
    this.updateSubmitState();
  },

  // 更新提交按钮状态
  updateSubmitState() {
    const { selectedType, selectedMethod, selectedTimeSlot, accountInfo } = this.data;
    const canSubmit = selectedType && selectedMethod && selectedTimeSlot && accountInfo;
    
    let totalPrice = 0;
    if (selectedType) {
      const selectedTypeInfo = this.data.consultTypes.find(type => type.id === selectedType);
      totalPrice = selectedTypeInfo ? selectedTypeInfo.price : 0;
    }

    this.setData({
      canSubmit,
      totalPrice
    });
  },

  // 提交订单
  onSubmit() {
    if (!this.data.canSubmit) {
      return;
    }

    const { counselorId, selectedType, selectedMethod, selectedTimeSlot, totalPrice, accountInfo } = this.data;

    const orderData = {
      counselorId,
      consultType: selectedType,
      consultMethod: selectedMethod,
      appointmentDate: selectedTimeSlot.date,
      appointmentTime: selectedTimeSlot.time,
      price: totalPrice,
      accountInfo
    };

    // TODO: 调用创建订单接口
    console.log('提交订单数据：', orderData);
    
    wx.showLoading({
      title: '提交中...'
    });

    // 模拟提交
    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '预约成功',
        icon: 'success',
        duration: 2000,
        success: () => {
          // 延迟跳转，让用户看到成功提示
          setTimeout(() => {
            wx.redirectTo({
              url: '/pages/order/detail?id=123' // TODO: 替换为实际订单ID
            });
          }, 2000);
        }
      });
    }, 1500);
  }
});