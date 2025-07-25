Page({
  data: {
    courseDetail: {
      id: '1',
      title: '情绪管理与心理健康',
      tags: ['减压', '情绪管理', '心理健康'],
      lessons: 12,
      duration: 3,
      studentCount: 1689,
      rating: 4.9,
      instructor: {
        name: '李明',
        title: '国家二级心理咨询师 | 情绪管理专家'
      },
      introduction: '本课程系统介绍情绪管理的核心理念和实用技巧，从认知行为疗法的角度出发，帮助你了解情绪的产生机制，掌握调节负面情绪的方法，建立健康的心理状态。适合各类职场人士、学生以及任何希望提升情绪管理能力的人群。',
      chapters: [
        {
          id: 1,
          title: '第一章：认识情绪',
          lessons: 3,
          duration: 45
        },
        {
          id: 2,
          title: '第二章：情绪的产生机制',
          lessons: 2,
          duration: 30
        },
        {
          id: 3,
          title: '第三章：情绪管理技巧',
          lessons: 4,
          duration: 60
        },
        {
          id: 4,
          title: '第四章：压力应对策略',
          lessons: 3,
          duration: 45
        }
      ],
      currentPrice: 299,
      originalPrice: 399
    }
  },

  onLoad(options) {
    const { id } = options;
    console.log('课程ID:', id);
    this.loadCourseDetail(id);
  },

  // 加载课程详情
  async loadCourseDetail(id) {
    try {
      // TODO: Replace with actual API call
      const res = await wx.cloud.callFunction({
        name: 'getCourseDetail',
        data: { id }
      });

      if (res.result && res.result.data) {
        this.setData({
          courseDetail: res.result.data
        });
      }
    } catch (error) {
      console.error('加载课程详情失败:', error);
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    }
  },

  // 购买课程
  handleBuy() {
    const { id, title, currentPrice } = this.data.courseDetail;
    // TODO: 实现购买逻辑
    wx.showModal({
      title: '确认购买',
      content: `是否购买课程《${title}》？`,
      success: (res) => {
        if (res.confirm) {
          // 跳转到订单确认页
          wx.navigateTo({
            url: `/pages/order/confirm/confirm?courseId=${id}&price=${currentPrice}`
          });
        }
      }
    });
  }
}); 