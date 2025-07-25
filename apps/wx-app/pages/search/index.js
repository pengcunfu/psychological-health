const { getResource } = require('../../utils/util')

Page({
  data: {
    searchText: '',
    hotSearchTags: [
      '抑郁情绪',
      '情绪调节',
      '情感危机',
      '夫妻矛盾',
      '专业抑郁类型别',
      '焦虑情绪',
      '精神科医师',
      '恋爱情感',
      '双相障碍'
    ],
    counselors: []
  },

  onLoad(options) {
    // 如果有搜索关键词传入，直接执行搜索
    if (options.keyword) {
      this.setData({
        searchText: options.keyword
      });
      this.searchCounselors(options.keyword);
    }
  },

  // 输入搜索内容
  onSearchInput(e) {
    const value = e.detail.value;
    this.setData({
      searchText: value
    });
    if (value) {
      this.searchCounselors(value);
    } else {
      this.setData({
        counselors: []
      });
    }
  },

  // 点击键盘搜索按钮
  onSearchConfirm(e) {
    const value = e.detail.value;
    if (value) {
      this.searchCounselors(value);
    }
  },

  // 点击取消按钮
  onCancel() {
    wx.navigateBack();
  },

  // 点击热门搜索标签
  onTagTap(e) {
    const tag = e.currentTarget.dataset.tag;
    this.setData({
      searchText: tag
    });
    this.searchCounselors(tag);
  },

  // 点击咨询师
  onCounselorTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/counselor/detail?id=${id}`
    });
  },

  // 搜索咨询师
  searchCounselors(keyword) {
    // TODO: 调用搜索API
    // 这里使用模拟数据
    const mockCounselors = [{
      id: 1,
      name: '张医生',
      avatar: getResource('images/个人成长.png'),
      specialty: '个人成长',
      consultType: '视频/语音'
    }, {
      id: 2,
      name: '李医生',
      avatar: getResource('images/情感咨询.png'),
      specialty: '情感咨询',
      consultType: '视频/语音'
    }];

    this.setData({
      counselors: mockCounselors
    });
  }
});