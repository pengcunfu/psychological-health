const { getResource } = require('../../utils/util')

Page({
  data: {
    messages: [],
    unreadCount: 0,
    loading: false,
    hasMore: true,
    page: 1,
    pageSize: 20
  },

  onLoad() {
    this.loadMessages()
  },

  onShow() {
    // 每次显示页面时更新未读消息数
    this.updateUnreadCount()
  },

  onPullDownRefresh() {
    this.refreshMessages()
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.loadMoreMessages()
    }
  },

  // 加载消息列表
  async loadMessages() {
    if (this.data.loading) return
    
    this.setData({ loading: true })
    
    try {
      // TODO: 替换为实际的API调用
      const mockMessages = [{
        id: 1,
        avatar: getResource('images/test.png'),
        name: '张医生',
        time: '10:30',
        preview: '好的，我们下次咨询时详细讨论这个问题',
        unread: 2
      }, {
        id: 2,
        avatar: getResource('images/test.png'),
        name: '李医生',
        time: '昨天',
        preview: '您最近感觉怎么样？要记得按时休息哦',
        unread: 0
      }, {
        id: 3,
        avatar: getResource('images/test.png'),
        name: '王医生',
        time: '星期一',
        preview: '这是一个很好的开始，继续保持',
        unread: 1
      }]

      this.setData({
        messages: mockMessages,
        loading: false,
        hasMore: mockMessages.length === this.data.pageSize
      })
    } catch (error) {
      console.error('加载消息列表失败:', error)
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败，请重试',
        icon: 'none'
      })
    }
  },

  // 刷新消息列表
  async refreshMessages() {
    this.setData({ page: 1 })
    await this.loadMessages()
    wx.stopPullDownRefresh()
  },

  // 加载更多消息
  async loadMoreMessages() {
    if (this.data.loading || !this.data.hasMore) return
    
    this.setData({
      page: this.data.page + 1
    })
    
    await this.loadMessages()
  },

  // 更新未读消息数
  updateUnreadCount() {
    // TODO: 替换为实际的API调用
    const unreadCount = this.data.messages.reduce((total, msg) => total + (msg.unread || 0), 0)
    this.setData({ unreadCount })
  },

  // 标记所有消息为已读
  async markAllAsRead() {
    try {
      // TODO: 替换为实际的API调用
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const updatedMessages = this.data.messages.map(msg => ({
        ...msg,
        unread: 0
      }))
      
      this.setData({
        messages: updatedMessages,
        unreadCount: 0
      })
      
      wx.showToast({
        title: '已全部标记为已读',
        icon: 'success'
      })
    } catch (error) {
      console.error('标记已读失败:', error)
      wx.showToast({
        title: '操作失败，请重试',
        icon: 'none'
      })
    }
  },

  // 点击消息项
  onMessageTap(e) {
    const { id } = e.currentTarget.dataset
    // TODO: 跳转到聊天详情页
    wx.navigateTo({
      url: `/pages/message/chat/index?id=${id}`
    })
  }
})