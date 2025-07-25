const app = getApp()
const recorderManager = wx.getRecorderManager()

Page({
  data: {
    counselorId: '',
    counselorName: '',
    counselorAvatar: '',
    userId: '',
    userAvatar: '',
    messages: [],
    inputContent: '',
    isVoiceMode: false,
    showMore: false,
    showCancelTip: false,
    scrollIntoView: '',
    hasMore: false,
    refreshing: false,
    pageSize: 20,
    currentPage: 1,
    isRecording: false,
    startY: 0
  },

  onLoad(options) {
    const { counselorId } = options
    this.setData({
      counselorId,
      userId: wx.getStorageSync('userId'),
      userAvatar: wx.getStorageSync('userAvatar')
    })
    
    this.loadCounselorInfo()
    this.loadMessages()
    this.initRecorder()
    this.connectSocket()
  },

  onUnload() {
    this.closeSocket()
  },

  // 加载咨询师信息
  async loadCounselorInfo() {
    try {
      const res = await wx.cloud.callFunction({
        name: 'getCounselorInfo',
        data: { counselorId: this.data.counselorId }
      })
      
      if (res.result) {
        this.setData({
          counselorName: res.result.name,
          counselorAvatar: res.result.avatar
        })
      }
    } catch (error) {
      console.error('加载咨询师信息失败:', error)
    }
  },

  // 加载消息历史
  async loadMessages() {
    wx.showLoading({
      title: '加载中...'
    })

    try {
      const res = await wx.cloud.callFunction({
        name: 'getMessageHistory',
        data: {
          counselorId: this.data.counselorId,
          userId: this.data.userId,
          page: this.data.currentPage,
          pageSize: this.data.pageSize
        }
      })

      const messages = res.result.data.map(msg => {
        return {
          ...msg,
          timeStr: this.formatTime(msg.timestamp),
          showTime: this.shouldShowTime(msg.timestamp)
        }
      })

      this.setData({
        messages: [...messages, ...this.data.messages],
        hasMore: res.result.hasMore
      })

      if (this.data.currentPage === 1) {
        this.scrollToBottom()
      }
    } catch (error) {
      console.error('加载消息历史失败:', error)
      wx.showToast({
        title: '加载失败，请重试',
        icon: 'none'
      })
    } finally {
      wx.hideLoading()
      if (this.data.refreshing) {
        wx.stopPullDownRefresh()
        this.setData({ refreshing: false })
      }
    }
  },

  // 初始化录音管理器
  initRecorder() {
    recorderManager.onStart(() => {
      this.setData({ isRecording: true })
    })

    recorderManager.onStop(async (res) => {
      if (!this.data.showCancelTip && res.duration > 1000) {
        try {
          const fileID = await this.uploadVoiceFile(res.tempFilePath)
          this.sendMessage('voice', fileID, Math.floor(res.duration / 1000))
        } catch (error) {
          console.error('上传语音失败:', error)
          wx.showToast({
            title: '发送失败，请重试',
            icon: 'none'
          })
        }
      }
      this.setData({
        isRecording: false,
        showCancelTip: false
      })
    })

    recorderManager.onError((error) => {
      console.error('录音错误:', error)
      wx.showToast({
        title: '录音失败，请重试',
        icon: 'none'
      })
      this.setData({ isRecording: false })
    })
  },

  // WebSocket连接
  connectSocket() {
    const socket = this.socket = wx.connectSocket({
      url: 'wss://your-domain.com/ws',
      header: {
        'content-type': 'application/json',
        'Authorization': wx.getStorageSync('token')
      }
    })

    socket.onOpen(() => {
      console.log('WebSocket连接已建立')
    })

    socket.onMessage((res) => {
      const message = JSON.parse(res.data)
      this.addMessage(message)
    })

    socket.onClose(() => {
      console.log('WebSocket连接已关闭')
      setTimeout(() => this.connectSocket(), 3000)
    })

    socket.onError((error) => {
      console.error('WebSocket错误:', error)
    })
  },

  closeSocket() {
    if (this.socket) {
      this.socket.close()
    }
  },

  // 发送消息
  async sendMessage(type = 'text', content = this.data.inputContent, duration) {
    if (!content) return

    const message = {
      id: Date.now().toString(),
      type,
      content,
      duration,
      fromId: this.data.userId,
      toId: this.data.counselorId,
      timestamp: Date.now(),
      status: 'sending'
    }

    // 添加到消息列表
    this.addMessage(message)
    this.setData({ inputContent: '', showMore: false })
    this.scrollToBottom()

    try {
      // 发送到服务器
      await this.socket.send({
        data: JSON.stringify(message)
      })
      
      // 更新消息状态为已发送
      this.updateMessageStatus(message.id, 'sent')
    } catch (error) {
      console.error('发送消息失败:', error)
      this.updateMessageStatus(message.id, 'failed')
    }
  },

  // 重发消息
  async resendMessage(e) {
    const messageId = e.currentTarget.dataset.id
    const message = this.data.messages.find(msg => msg.id === messageId)
    if (message) {
      this.updateMessageStatus(messageId, 'sending')
      await this.sendMessage(message.type, message.content, message.duration)
    }
  },

  // 添加消息到列表
  addMessage(message) {
    const messages = [...this.data.messages]
    message.timeStr = this.formatTime(message.timestamp)
    message.showTime = this.shouldShowTime(message.timestamp, messages)
    messages.push(message)
    this.setData({ messages })
  },

  // 更新消息状态
  updateMessageStatus(messageId, status) {
    const messages = this.data.messages.map(msg => {
      if (msg.id === messageId) {
        return { ...msg, status }
      }
      return msg
    })
    this.setData({ messages })
  },

  // 上传语音文件
  async uploadVoiceFile(tempFilePath) {
    const res = await wx.cloud.uploadFile({
      cloudPath: `voice/${Date.now()}.mp3`,
      filePath: tempFilePath
    })
    return res.fileID
  },

  // 选择图片
  async chooseImage() {
    try {
      const res = await wx.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera']
      })

      wx.showLoading({ title: '发送中...' })
      const fileID = await wx.cloud.uploadFile({
        cloudPath: `images/${Date.now()}.jpg`,
        filePath: res.tempFilePaths[0]
      })
      
      await this.sendMessage('image', fileID)
    } catch (error) {
      console.error('发送图片失败:', error)
      wx.showToast({
        title: '发送失败，请重试',
        icon: 'none'
      })
    } finally {
      wx.hideLoading()
    }
  },

  // 预览图片
  previewImage(e) {
    const url = e.currentTarget.dataset.url
    wx.previewImage({
      urls: [url]
    })
  },

  // 播放语音
  async playVoice(e) {
    const url = e.currentTarget.dataset.url
    const innerAudioContext = wx.createInnerAudioContext()
    innerAudioContext.src = url
    innerAudioContext.play()
  },

  // 开始录音
  startRecording() {
    this.setData({
      startY: 0,
      showCancelTip: false
    })
    
    recorderManager.start({
      duration: 60000,
      format: 'mp3'
    })
  },

  // 停止录音
  stopRecording() {
    recorderManager.stop()
  },

  // 录音手指移动
  onTouchMove(e) {
    if (!this.data.startY) {
      this.setData({ startY: e.touches[0].clientY })
    }

    const moveY = e.touches[0].clientY
    const showCancelTip = this.data.startY - moveY > 100

    if (showCancelTip !== this.data.showCancelTip) {
      this.setData({ showCancelTip })
    }
  },

  // 输入框输入
  onInput(e) {
    this.setData({
      inputContent: e.detail.value
    })
  },

  // 切换输入模式
  switchInputMode() {
    this.setData({
      isVoiceMode: !this.data.isVoiceMode,
      showMore: false
    })
  },

  // 显示更多功能面板
  showMoreActions() {
    this.setData({
      showMore: !this.data.showMore
    })
  },

  // 开始视频通话
  startVideoCall() {
    wx.navigateTo({
      url: `/pages/video-call/index?counselorId=${this.data.counselorId}`
    })
  },

  // 预约咨询
  makeAppointment() {
    wx.navigateTo({
      url: `/pages/counselor/appointments/appointment?counselorId=${this.data.counselorId}`
    })
  },

  // 下拉刷新
  onRefresh() {
    this.setData({
      refreshing: true,
      currentPage: this.data.currentPage + 1
    })
    this.loadMessages()
  },

  // 滚动到顶部加载更多
  onScrollToUpper() {
    if (this.data.hasMore) {
      this.setData({
        currentPage: this.data.currentPage + 1
      })
      this.loadMessages()
    }
  },

  // 滚动到底部
  scrollToBottom() {
    const messages = this.data.messages
    if (messages.length > 0) {
      this.setData({
        scrollIntoView: `msg-${messages[messages.length - 1].id}`
      })
    }
  },

  // 格式化时间
  formatTime(timestamp) {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now - date

    // 今天的消息只显示时间
    if (diff < 24 * 60 * 60 * 1000 && date.getDate() === now.getDate()) {
      return date.toLocaleTimeString('zh-CN', { hour12: false, hour: '2-digit', minute: '2-digit' })
    }

    // 昨天的消息显示"昨天"
    if (diff < 48 * 60 * 60 * 1000 && date.getDate() === now.getDate() - 1) {
      return `昨天 ${date.toLocaleTimeString('zh-CN', { hour12: false, hour: '2-digit', minute: '2-digit' })}`
    }

    // 其他显示完整日期
    return date.toLocaleString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    })
  },

  // 判断是否显示时间
  shouldShowTime(timestamp, messages = this.data.messages) {
    if (messages.length === 0) return true
    const lastMessage = messages[messages.length - 1]
    return !lastMessage || timestamp - lastMessage.timestamp > 5 * 60 * 1000
  }
}) 