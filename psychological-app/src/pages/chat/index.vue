<template>
  <view class="container">
    <!-- 聊天消息列表 -->
    <scroll-view class="chat-list" scroll-y :scroll-top="scrollTop" scroll-with-animation>
      <view v-for="(message, index) in messages" :key="index" class="message-item">
        <!-- 对方消息 -->
        <view v-if="!message.isSelf" class="message-wrapper message-other">
          <image class="avatar" :src="counselorInfo.avatar || '/static/images/default-avatar.png'" mode="aspectFill"></image>
          <view class="message-content">
            <view class="message-bubble">
              <text class="message-text">{{ message.content }}</text>
            </view>
            <view class="message-time">{{ message.time }}</view>
          </view>
        </view>

        <!-- 自己的消息 -->
        <view v-else class="message-wrapper message-self">
          <view class="message-content">
            <view class="message-bubble">
              <text class="message-text">{{ message.content }}</text>
            </view>
            <view class="message-time">{{ message.time }}</view>
          </view>
          <image class="avatar" :src="userInfo.avatar || '/static/images/default-avatar.png'" mode="aspectFill"></image>
        </view>
      </view>
    </scroll-view>

    <!-- 输入区域 -->
    <view class="input-area">
      <view class="input-wrapper">
        <input 
          v-model="inputText" 
          class="input-field" 
          placeholder="请输入消息..." 
          confirm-type="send"
          @confirm="sendMessage"
          @focus="onInputFocus"
          @blur="onInputBlur"
        />
        <button class="send-btn" :class="{ active: inputText.trim() }" @click="sendMessage">
          发送
        </button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, computed, nextTick, onMounted } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

// 聊天相关数据
const inputText = ref('')
const scrollTop = ref(0)
const counselorInfo = reactive({
  id: '',
  name: '',
  avatar: ''
})

// 用户信息
const userInfo = computed(() => userStore.userInfo || {})

// 消息列表
const messages = ref([
  {
    id: 1,
    content: '您好，欢迎咨询！我是您的专属心理咨询师，有什么可以帮助您的吗？',
    time: '14:30',
    isSelf: false
  },
  {
    id: 2,
    content: '您好，我最近感觉压力很大，经常失眠，不知道该怎么办。',
    time: '14:32',
    isSelf: true
  },
  {
    id: 3,
    content: '我理解您的困扰。压力大导致失眠是很常见的问题。能具体说说是什么原因让您感到压力吗？是工作、学习还是生活方面的？',
    time: '14:33',
    isSelf: false
  },
  {
    id: 4,
    content: '主要是工作方面的压力，最近项目比较多，总是担心完不成任务。',
    time: '14:35',
    isSelf: true
  }
])

// 发送消息
const sendMessage = () => {
  if (!inputText.value.trim()) {
    return
  }

  // 添加用户消息
  const userMessage = {
    id: Date.now(),
    content: inputText.value.trim(),
    time: getCurrentTime(),
    isSelf: true
  }
  
  messages.value.push(userMessage)
  inputText.value = ''

  // 滚动到底部
  scrollToBottom()

  // 模拟咨询师回复（实际开发中应该调用API）
  setTimeout(() => {
    const replyMessage = {
      id: Date.now() + 1,
      content: '我明白了。工作压力确实会影响睡眠质量。建议您可以尝试一些放松技巧，比如深呼吸、冥想等。另外，建立规律的作息时间也很重要。',
      time: getCurrentTime(),
      isSelf: false
    }
    messages.value.push(replyMessage)
    scrollToBottom()
  }, 1500)
}

// 获取当前时间
const getCurrentTime = () => {
  const now = new Date()
  const hours = now.getHours().toString().padStart(2, '0')
  const minutes = now.getMinutes().toString().padStart(2, '0')
  return `${hours}:${minutes}`
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    scrollTop.value = 999999
  })
}

// 输入框聚焦处理
const onInputFocus = () => {
  // 延迟滚动，等待键盘弹出
  setTimeout(() => {
    scrollToBottom()
  }, 300)
}

// 输入框失焦处理
const onInputBlur = () => {
  // 可以在这里处理一些逻辑
}

// 页面加载
onLoad((options) => {
  // 获取传递的咨询师信息
  if (options.id) {
    counselorInfo.id = options.id
  }
  if (options.name) {
    counselorInfo.name = decodeURIComponent(options.name)
  }
  if (options.avatar) {
    counselorInfo.avatar = decodeURIComponent(options.avatar)
  }

  // 设置导航栏标题
  uni.setNavigationBarTitle({
    title: counselorInfo.name || '咨询师聊天'
  })
})

onShow(() => {
  // 页面显示时滚动到底部
  scrollToBottom()
})
</script>

<style lang="scss" scoped>
// SCSS 变量定义
$primary-color: #007AFF;
$white: #FFFFFF;
$gray-light: #f5f7fa;
$gray: #999;
$gray-medium: #666;
$gray-dark: #333;
$text-primary: #1C1C1E;
$text-secondary: #48484A;
$text-tertiary: #8E8E93;
$bg-primary: #FFFFFF;
$bg-secondary: #F2F2F7;
$bg-message-self: #007AFF;
$bg-message-other: #E5E5EA;

.container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: $bg-secondary;
}

// 聊天消息列表
.chat-list {
  flex: 1;
  padding: 20rpx;
  overflow-y: auto;
}

.message-item {
  margin-bottom: 30rpx;
}

.message-wrapper {
  display: flex;
  align-items: flex-end;
  
  &.message-other {
    justify-content: flex-start;
    
    .avatar {
      margin-right: 20rpx;
    }
    
    .message-content {
      max-width: 70%;
      
      .message-bubble {
        background-color: $bg-message-other;
        color: $text-primary;
      }
      
      .message-time {
        text-align: left;
      }
    }
  }
  
  &.message-self {
    justify-content: flex-end;
    
    .avatar {
      margin-left: 20rpx;
    }
    
    .message-content {
      max-width: 70%;
      
      .message-bubble {
        background-color: $bg-message-self;
        color: $white;
      }
      
      .message-time {
        text-align: right;
      }
    }
  }
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  flex-shrink: 0;
}

.message-content {
  display: flex;
  flex-direction: column;
}

.message-bubble {
  padding: 20rpx 30rpx;
  border-radius: 40rpx;
  max-width: 100%;
  word-wrap: break-word;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.message-text {
  font-size: 32rpx;
  line-height: 1.5;
}

.message-time {
  font-size: 24rpx;
  color: $text-tertiary;
  margin-top: 10rpx;
  padding: 0 30rpx;
}

// 输入区域
.input-area {
  background-color: $bg-primary;
  border-top: 1rpx solid #E5E5EA;
  padding: 20rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
}

.input-wrapper {
  display: flex;
  align-items: center;
  background-color: $bg-secondary;
  border-radius: 50rpx;
  padding: 10rpx 20rpx;
}

.input-field {
  flex: 1;
  height: 70rpx;
  line-height: 70rpx;
  font-size: 32rpx;
  color: $text-primary;
  background-color: transparent;
  border: none;
  outline: none;
  
  &::placeholder {
    color: $text-tertiary;
  }
}

.send-btn {
  width: 120rpx;
  height: 60rpx;
  background-color: $text-tertiary;
  color: $white;
  border: none;
  border-radius: 30rpx;
  font-size: 28rpx;
  margin-left: 20rpx;
  transition: all 0.2s ease;
  
  &.active {
    background-color: $primary-color;
  }
  
  &:active {
    transform: scale(0.95);
  }
}
</style>
