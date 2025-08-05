<template>
  <view class="container">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="header-title">消息</view>
      <view class="header-actions">
        <u-icon name="search" size="40" color="#333" @click="navigateTo('/pages/search/index')"></u-icon>
      </view>
    </view>

    <!-- 选项卡 -->
    <view class="tab-bar">
      <view 
        class="tab" 
        :class="{ active: activeTab === index }" 
        v-for="(tab, index) in tabs" 
        :key="index"
        @click="switchTab(index)"
      >
        {{ tab }}
      </view>
    </view>

    <!-- 消息列表 -->
    <view class="message-list">
      <view 
        v-for="(message, index) in filteredMessages" 
        :key="index"
        class="message-item"
        :class="{ 'system-message': message.type === 'system' }"
        @click="handleMessageClick(message)"
      >
        <!-- 头像或系统图标 -->
        <image 
          v-if="message.avatar" 
          class="avatar" 
          :src="message.avatar" 
          mode="aspectFill"
        ></image>
        <view v-else class="system-icon">
          <u-icon :name="getSystemIcon(message.messageType)" size="40" color="#4A90E2"></u-icon>
        </view>

        <!-- 消息内容 -->
        <view class="message-content">
          <view class="message-header">
            <text class="message-name">{{ message.name }}</text>
            <text class="message-time">{{ message.time }}</text>
          </view>
          <text class="message-preview">{{ message.preview }}</text>
          <view class="message-meta">
            <text class="message-type">{{ message.messageType }}</text>
            <view v-if="message.unreadCount > 0" class="message-badge">
              {{ message.unreadCount }}
            </view>
          </view>
        </view>
      </view>

      <!-- 空状态 -->
      <view v-if="filteredMessages.length === 0" class="empty-state">
        <u-icon name="inbox" size="160" color="#ccc"></u-icon>
        <text class="empty-text">暂无消息</text>
      </view>
    </view>

    <!-- 自定义TabBar -->
    <TabBar />
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { navigateTo } from '@/utils/link'
import TabBar from '@/components/TabBar/index.vue'

// 选项卡数据
const tabs = ref(['全部', '系统通知', '咨询消息', '课程提醒'])
const activeTab = ref(0)

// 消息数据
const messages = ref([
  {
    id: 1,
    type: 'system',
    name: '系统通知',
    time: '10:30',
    preview: '您的会员即将到期，续费可享受8折优惠，点击查看详情。',
    messageType: '系统通知',
    unreadCount: 1,
    avatar: null
  },
  {
    id: 2,
    type: 'counselor',
    name: '张医生',
    time: '昨天',
    preview: '您好，关于您上次提到的睡眠问题，我有一些建议可以分享给您。',
    messageType: '咨询消息',
    unreadCount: 2,
    avatar: 'https://via.placeholder.com/80x80/4A90E2/FFFFFF/?text=张医生'
  },
  {
    id: 3,
    type: 'course',
    name: '课程提醒',
    time: '周一',
    preview: '您报名的《情绪管理》课程今天有新的课节更新，请及时学习。',
    messageType: '课程提醒',
    unreadCount: 0,
    avatar: null
  },
  {
    id: 4,
    type: 'system',
    name: '测评结果',
    time: '06-15',
    preview: '您的"抑郁症筛查量表(PHQ-9)"测评结果已生成，点击查看详情。',
    messageType: '测评通知',
    unreadCount: 0,
    avatar: null
  },
  {
    id: 5,
    type: 'counselor',
    name: '李医生',
    time: '06-10',
    preview: '感谢您的咨询，希望我的建议对您有所帮助。如有其他问题，随时联系我。',
    messageType: '咨询消息',
    unreadCount: 0,
    avatar: 'https://via.placeholder.com/80x80/52C41A/FFFFFF/?text=李医生'
  },
  {
    id: 6,
    type: 'system',
    name: '活动通知',
    time: '06-05',
    preview: '6月15日晚8点，"如何缓解职场压力"线上讲座即将开始，点击预约。',
    messageType: '活动通知',
    unreadCount: 0,
    avatar: null
  }
])

// 根据当前选项卡过滤消息
const filteredMessages = computed(() => {
  if (activeTab.value === 0) {
    return messages.value // 全部
  } else if (activeTab.value === 1) {
    return messages.value.filter(msg => msg.type === 'system') // 系统通知
  } else if (activeTab.value === 2) {
    return messages.value.filter(msg => msg.type === 'counselor') // 咨询消息
  } else if (activeTab.value === 3) {
    return messages.value.filter(msg => msg.type === 'course') // 课程提醒
  }
  return messages.value
})

// 切换选项卡
const switchTab = (index) => {
  activeTab.value = index
}

// 获取系统图标
const getSystemIcon = (messageType) => {
  switch (messageType) {
    case '系统通知':
      return 'bell-fill'
    case '课程提醒':
      return 'clock-fill'
    case '测评通知':
      return 'checkmark-circle-fill'
    case '活动通知':
      return 'calendar-fill'
    default:
      return 'bell-fill'
  }
}

// 处理消息点击
const handleMessageClick = (message) => {
  console.log('点击消息:', message)
  
  // 根据消息类型跳转到不同页面
  switch (message.type) {
    case 'counselor':
      // 跳转到聊天详情页
      navigateTo(`/pages/chat/index?id=${message.id}&name=${message.name}`)
      break
    case 'course':
      // 跳转到课程详情页
      navigateTo(`/pages/course/detail/index?id=${message.id}`)
      break
    case 'system':
      // 根据系统消息类型进行不同处理
      if (message.messageType === '测评通知') {
        navigateTo(`/pages/assessment/result/index?id=${message.id}`)
      } else {
        // 其他系统消息显示详情
        uni.showModal({
          title: message.name,
          content: message.preview,
          showCancel: false
        })
      }
      break
    default:
      uni.showToast({
        title: '功能开发中',
        icon: 'none'
      })
  }
  
  // 标记为已读
  if (message.unreadCount > 0) {
    message.unreadCount = 0
  }
}

onLoad(() => {
  // 页面加载时的逻辑
})
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

// 顶部导航样式
.header {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 88rpx;
  background-color: #fff;
  border-bottom: 2rpx solid #f0f0f0;
  position: sticky;
  top: 0;
  z-index: 10;
  position: relative;
}

.header-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.header-actions {
  position: absolute;
  right: 30rpx;
  display: flex;
  align-items: center;
}

// 选项卡样式
.tab-bar {
  display: flex;
  background-color: #fff;
  border-bottom: 2rpx solid #f0f0f0;
  padding: 0 10rpx;
}

.tab {
  flex: 1;
  text-align: center;
  padding: 20rpx 0;
  font-size: 26rpx;
  color: #666;
  position: relative;
}

.tab.active {
  color: #4A90E2;
  font-weight: bold;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 32rpx;
  height: 4rpx;
  background-color: #4A90E2;
  border-radius: 2rpx;
}

// 消息列表样式
.message-list {
  padding: 16rpx 20rpx;
  padding-bottom: 120rpx; /* 为TabBar留出空间 */
}

.message-item {
  display: flex;
  padding: 20rpx;
  background-color: #fff;
  margin-bottom: 16rpx;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 4rpx rgba(0,0,0,0.05);
}

.system-message {
  background-color: #f9fbff;
}

.avatar, .system-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  margin-right: 20rpx;
  flex-shrink: 0;
}

.avatar {
  object-fit: cover;
}

.system-icon {
  background-color: #e6f0fc;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-content {
  flex: 1;
  overflow: hidden;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6rpx;
}

.message-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
}

.message-time {
  font-size: 24rpx;
  color: #999;
}

.message-preview {
  font-size: 26rpx;
  color: #666;
  line-height: 1.4;
  margin-bottom: 6rpx;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.message-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.message-type {
  font-size: 24rpx;
  color: #4A90E2;
}

.message-badge {
  background-color: #ff4d4f;
  color: #fff;
  font-size: 20rpx;
  min-width: 32rpx;
  height: 32rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 8rpx;
}

// 空状态样式
.empty-state {
  padding: 120rpx 0;
  text-align: center;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
  margin-top: 30rpx;
  display: block;
}
</style> 