Page({
  data: {
    tabs: ['咨询师', '课程', '文章', '视频'],
    currentTab: 0,
    refreshing: false,
    counselors: [],
    courses: [],
    articles: [],
    videos: []
  },

  onLoad() {
    this.loadData()
  },

  onShow() {
    // 页面显示时刷新数据
    this.loadData()
  },

  // 加载数据
  async loadData() {
    wx.showLoading({
      title: '加载中...'
    })

    try {
      const userId = wx.getStorageSync('userId')
      if (!userId) {
        wx.hideLoading()
        return
      }

      // 根据当前标签页加载对应数据
      switch (this.data.currentTab) {
        case 0:
          await this.loadCounselors()
          break
        case 1:
          await this.loadCourses()
          break
        case 2:
          await this.loadArticles()
          break
        case 3:
          await this.loadVideos()
          break
      }
    } catch (error) {
      console.error('加载收藏数据失败:', error)
      wx.showToast({
        title: '加载失败，请重试',
        icon: 'none'
      })
    } finally {
      wx.hideLoading()
      if (this.data.refreshing) {
        wx.stopPullDownRefresh()
        this.setData({
          refreshing: false
        })
      }
    }
  },

  // 加载收藏的咨询师
  async loadCounselors() {
    const userId = wx.getStorageSync('userId')
    // TODO: 调用获取收藏咨询师列表接口
    const res = await wx.cloud.callFunction({
      name: 'getFavoriteCounselors',
      data: { userId }
    })
    this.setData({
      counselors: res.result.data || []
    })
  },

  // 加载收藏的课程
  async loadCourses() {
    const userId = wx.getStorageSync('userId')
    // TODO: 调用获取收藏课程列表接口
    const res = await wx.cloud.callFunction({
      name: 'getFavoriteCourses',
      data: { userId }
    })
    this.setData({
      courses: res.result.data || []
    })
  },

  // 加载收藏的文章
  async loadArticles() {
    const userId = wx.getStorageSync('userId')
    // TODO: 调用获取收藏文章列表接口
    const res = await wx.cloud.callFunction({
      name: 'getFavoriteArticles',
      data: { userId }
    })
    this.setData({
      articles: res.result.data || []
    })
  },

  // 加载收藏的视频
  async loadVideos() {
    const userId = wx.getStorageSync('userId')
    // TODO: 调用获取收藏视频列表接口
    const res = await wx.cloud.callFunction({
      name: 'getFavoriteVideos',
      data: { userId }
    })
    this.setData({
      videos: res.result.data || []
    })
  },

  // 切换标签页
  switchTab(e) {
    const index = e.currentTarget.dataset.index
    this.setData({
      currentTab: index
    })
    this.loadData()
  },

  // 滑动切换标签页
  onSwiperChange(e) {
    const index = e.detail.current
    this.setData({
      currentTab: index
    })
    this.loadData()
  },

  // 下拉刷新
  onRefresh() {
    this.setData({
      refreshing: true
    })
    this.loadData()
  },

  // 跳转到咨询师详情
  navigateToCounselor(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/counselor/detail/index?id=${id}`
    })
  },

  // 跳转到课程详情
  navigateToCourse(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/course/detail/index?id=${id}`
    })
  },

  // 跳转到文章详情
  navigateToArticle(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/article/detail/index?id=${id}`
    })
  },

  // 跳转到视频详情
  navigateToVideo(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/video/detail/index?id=${id}`
    })
  },

  // 跳转到咨询师列表
  navigateToCounselors() {
    wx.switchTab({
      url: '/pages/counselor/index'
    })
  },

  // 跳转到课程列表
  navigateToCourses() {
    wx.switchTab({
      url: '/pages/course/index'
    })
  },

  // 跳转到文章列表
  navigateToArticles() {
    wx.switchTab({
      url: '/pages/article/index'
    })
  },

  // 跳转到视频列表
  navigateToVideos() {
    wx.switchTab({
      url: '/pages/video/index'
    })
  }
}) 