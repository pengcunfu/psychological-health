const { getResource } = require('../../utils/util')

Page({
  data: {
    currentTab: 'all',
    isRefreshing: false,
    loadingMore: false,
    noMoreData: false,
    page: 1,
    counselors: [
      {
        id: 1,
        name: '朱一村',
        avatar: getResource('images/test.png'),
        tags: ['情感危机', '情绪压力', '婚姻家庭', '亲子教育', '适应困扰', '个人成长', '青少年心理'],
        consultType: '图文 电话 视频 面询'
      },
      {
        id: 2,
        name: '刘刘',
        avatar: getResource('images/test.png'),
        tags: ['情感危机', '情绪压力', '婚姻家庭', '亲子教育', '适应困扰', '个人成长', '青少年心理'],
        consultType: '图文 电话 视频 面询'
      },
      {
        id: 3,
        name: '王笑笑',
        avatar: getResource('images/test.png'),
        tags: ['情感危机', '情绪压力', '婚姻家庭', '亲子教育', '适应困扰', '个人成长', '青少年心理'],
        consultType: '图文 电话 视频 面询'
      },
      {
        id: 4,
        name: '111111',
        avatar: getResource('images/test.png'),
        tags: ['情绪压力', '亲子教育', '适应困扰'],
        consultType: '图文 电话 视频 面询'
      }
    ]
  },

  onLoad() {
    this.loadCounselors()
  },

  // 切换标签
  switchTab(e) {
    const tab = e.currentTarget.dataset.tab
    if (tab === this.data.currentTab) return
    
    this.setData({
      currentTab: tab,
      counselors: [],
      page: 1,
      noMoreData: false
    }, () => {
      this.loadCounselors()
    })
  },

  // 加载咨询师列表
  loadCounselors() {
    if (this.data.loadingMore || this.data.noMoreData) return

    this.setData({ loadingMore: true })

    // TODO: 调用获取咨询师列表接口
    setTimeout(() => {
      // 模拟加载更多数据
      if (this.data.page > 2) {
        this.setData({
          loadingMore: false,
          noMoreData: true
        })
        return
      }

      const newCounselors = this.data.counselors
      this.setData({
        counselors: newCounselors,
        page: this.data.page + 1,
        loadingMore: false
      })
    }, 1000)
  },

  // 下拉刷新
  onRefresh() {
    if (this.data.isRefreshing) return
    
    this.setData({
      isRefreshing: true,
      counselors: [],
      page: 1,
      noMoreData: false
    })

    this.loadCounselors()

    setTimeout(() => {
      this.setData({ isRefreshing: false })
    }, 1000)
  },

  // 上拉加载更多
  onLoadMore() {
    this.loadCounselors()
  },

  // 点击咨询师
  onCounselorTap(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/counselor/detail/index?id=${id}`
    })
  }
})