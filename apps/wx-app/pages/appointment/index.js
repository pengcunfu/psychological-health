const { getResource } = require('../../utils/util');

Page({
  data: {
    counselorId: null,
    isFavorite: false,
    isIntroExpanded: false,
    counselor: {
      name: '郭万梅',
      price: 800,
      location: '上海·中山公园工作室',
      yearsOfExperience: 10,
      consultationHours: 6000,
      oneOnOneHours: 140,
      groupHours: 100,
      qualifications: [
        '注册心理师',
        '国家二级心理咨询师',
        '中国生命关怀协会会员',
        '中国生命关怀协会静观专业委员会委员'
      ],
      introduction: '我在心理咨询行业工作了十余年，有着丰富的咨询经验。文学出身的我发现了我对这个世界和人性的复杂性具有敏锐的感知力和共情性，心理实践与发展使我获益了我深厚冷静的理性思维源泉。心理咨询其实是一场我们如何诚实面对自己的学习，我们如何认识和看待自己，如何认识看待自己与他人的关系，可能是我们终生的学习以及，也可以说所有的心理问题几乎都出自于此。',
      directions: [
        {
          icon: getResource('images/emotion.png'),
          title: '情绪管理',
          description: '孤独、焦虑情绪、内疚、抑郁情绪、嫉妒、压力调节'
        },
        {
          icon: getResource('images/growth.png'),
          title: '个人成长',
          description: '缺乏安全感、女性成长、自卑、完美主义、咨询师个人经验、拖延'
        },
        {
          icon: getResource('images/health.png'),
          title: '心身健康',
          description: '进食障碍、失眠、产后抑郁情绪、攻击性行为、行为成瘾、强迫'
        }
      ],
      targetGroups: [
        '个体咨询(成人)',
        '个体咨询(少儿17~18岁)'
      ]
    }
  },

  onLoad(options) {
    if (options.counselorId) {
      this.setData({
        counselorId: options.counselorId
      });
      this.loadCounselorData(options.counselorId);
    }
  },

  // 加载咨询师数据
  loadCounselorData(counselorId) {
    // TODO: 从服务器获取咨询师详细信息
    // 目前使用模拟数据
  },

  // 切换收藏状态
  toggleFavorite() {
    const newFavoriteState = !this.data.isFavorite;
    this.setData({
      isFavorite: newFavoriteState
    });

    // TODO: 调用收藏/取消收藏接口
    wx.showToast({
      title: newFavoriteState ? '收藏成功' : '已取消收藏',
      icon: 'success'
    });
  },

  // 切换简介展开状态
  toggleIntro() {
    this.setData({
      isIntroExpanded: !this.data.isIntroExpanded
    });
  },

  // 点击预约按钮
  onBookTap() {
    wx.navigateTo({
      url: `/pages/appointment/add?counselorId=${this.data.counselorId}`
    });
  }
});