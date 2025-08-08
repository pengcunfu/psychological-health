<template>
  <view class="container">
    <!-- 导航栏 -->
    <Navbar title="设置" />
    
    <!-- 账号设置 -->
    <view class="settings-section">
      <view class="settings-header">账号设置</view>
      
      <view class="settings-item" @click="navigateTo('/pages/profile/edit')">
        <SvgIcon name="account" path="profile" class="settings-icon" :size="32" color="#4A90E2" />
        <view class="settings-content">
          <view class="settings-title">个人资料</view>
          <view class="settings-desc">修改个人信息和头像</view>
        </view>
        <view class="settings-right">
          <SvgIcon name="arrow-right" :size="16" color="#ccc" />
        </view>
      </view>
      
      <view class="settings-item" @click="navigateTo('/pages/profile/security')">
        <SvgIcon name="shield" path="profile" class="settings-icon" :size="32" color="#4A90E2" />
        <view class="settings-content">
          <view class="settings-title">安全设置</view>
          <view class="settings-desc">修改密码、实名认证、隐私保护</view>
        </view>
        <view class="settings-right">
          <SvgIcon name="arrow-right" :size="16" color="#ccc" />
        </view>
      </view>
      
      <view class="settings-item" @click="showToast('通知设置功能即将开放')">
        <SvgIcon name="notification" class="settings-icon" :size="32" color="#4A90E2" />
        <view class="settings-content">
          <view class="settings-title">通知设置</view>
          <view class="settings-desc">消息提醒、推送设置</view>
        </view>
        <view class="settings-right">
          <view class="badge badge-new">新</view>
          <SvgIcon name="arrow-right" :size="16" color="#ccc" />
        </view>
      </view>
    </view>
    
    <!-- 通用设置 -->
    <view class="settings-section">
      <view class="settings-header">通用设置</view>
      
      <view class="settings-item">
        <SvgIcon name="setting" class="settings-icon" :size="32" color="#4A90E2" />
        <view class="settings-content">
          <view class="settings-title">深色模式</view>
        </view>
        <view class="settings-right">
          <switch 
            :checked="darkMode" 
            @change="toggleDarkMode" 
            color="#4A90E2"
            style="transform: scale(0.8);"
          />
        </view>
      </view>
      
      <view class="settings-item" @click="showToast('语言设置功能即将开放')">
        <view class="settings-icon" style="display: flex; align-items: center; justify-content: center;">
          <text style="font-size: 20px;">🌐</text>
        </view>
        <view class="settings-content">
          <view class="settings-title">语言</view>
        </view>
        <view class="settings-right">
          <view class="settings-value">简体中文</view>
          <SvgIcon name="arrow-right" :size="16" color="#ccc" />
        </view>
      </view>
      
      <view class="settings-item" @click="showToast('字体设置功能即将开放')">
        <view class="settings-icon" style="display: flex; align-items: center; justify-content: center;">
          <text style="font-size: 18px; font-weight: bold;">T</text>
        </view>
        <view class="settings-content">
          <view class="settings-title">字体大小</view>
        </view>
        <view class="settings-right">
          <view class="settings-value">标准</view>
          <SvgIcon name="arrow-right" :size="16" color="#ccc" />
        </view>
      </view>
      
      <view class="settings-item">
        <view class="settings-icon" style="display: flex; align-items: center; justify-content: center;">
          <text style="font-size: 18px;">⚠️</text>
        </view>
        <view class="settings-content">
          <view class="settings-title">开发者模式</view>
        </view>
        <view class="settings-right">
          <switch 
            :checked="developerMode" 
            @change="toggleDeveloperMode" 
            color="#4A90E2"
            style="transform: scale(0.8);"
          />
        </view>
      </view>
    </view>
    
    <!-- 其他设置 -->
    <view class="settings-section">
      <view class="settings-header">其他</view>
      
      <view class="settings-item" @click="clearCache">
        <view class="settings-icon" style="display: flex; align-items: center; justify-content: center;">
          <text style="font-size: 18px;">🗑️</text>
        </view>
        <view class="settings-content">
          <view class="settings-title">清除缓存</view>
          <view class="settings-desc">清除应用缓存数据</view>
        </view>
        <view class="settings-right">
          <view class="settings-value">{{ cacheSize }}</view>
          <SvgIcon name="arrow-right" :size="16" color="#ccc" />
        </view>
      </view>
      
      <view class="settings-item" @click="navigateTo('/pages/profile/contact-us')">
        <SvgIcon name="info-circle" path="profile" class="settings-icon" :size="32" color="#4A90E2" />
        <view class="settings-content">
          <view class="settings-title">关于我们</view>
        </view>
        <view class="settings-right">
          <SvgIcon name="arrow-right" :size="16" color="#ccc" />
        </view>
      </view>
      
      <view class="settings-item" @click="navigateTo('/pages/profile/help-center')">
        <SvgIcon name="help-circle" path="profile" class="settings-icon" :size="32" color="#4A90E2" />
        <view class="settings-content">
          <view class="settings-title">帮助中心</view>
        </view>
        <view class="settings-right">
          <SvgIcon name="arrow-right" :size="16" color="#ccc" />
        </view>
      </view>
      
      <view class="settings-item" @click="showToast('意见反馈功能即将开放')">
        <view class="settings-icon" style="display: flex; align-items: center; justify-content: center;">
          <text style="font-size: 18px;">💬</text>
        </view>
        <view class="settings-content">
          <view class="settings-title">意见反馈</view>
        </view>
        <view class="settings-right">
          <SvgIcon name="arrow-right" :size="16" color="#ccc" />
        </view>
      </view>
      
      <view class="settings-item">
        <view class="settings-icon" style="display: flex; align-items: center; justify-content: center;">
          <text style="font-size: 18px;">📋</text>
        </view>
        <view class="settings-content">
          <view class="settings-title">版本信息</view>
        </view>
        <view class="settings-right">
          <view class="settings-value">v1.2.3</view>
        </view>
      </view>
    </view>
    
    <!-- 退出登录按钮 -->
    <view class="logout-section">
      <view class="logout-button" @click="handleLogout">
        退出登录
      </view>
    </view>
    
    <!-- 底部空间 -->
    <view style="height: 40rpx;"></view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/store/user'
import SvgIcon from '@/components/SvgIcon.vue'
import Navbar from '@/components/Navbar.vue'

const userStore = useUserStore()

// 设置状态
const darkMode = ref(false)
const developerMode = ref(false)
const cacheSize = ref('23.5MB')

// 计算属性
const isLoggedIn = computed(() => userStore.isLoggedIn)

// goBack函数已移除，NavBar组件会自动处理返回功能

// 页面跳转
const navigateTo = (url) => {
  if (!isLoggedIn.value && url !== '/pages/profile/contact-us') {
    uni.showToast({
      title: '请先登录',
      icon: 'none'
    })
    
    setTimeout(() => {
      uni.navigateTo({
        url: '/pages/login'
      })
    }, 1500)
    return
  }
  
  uni.navigateTo({ url })
}

// 显示提示
const showToast = (message) => {
  uni.showToast({
    title: message,
    icon: 'none'
  })
}

// 切换深色模式
const toggleDarkMode = (e) => {
  darkMode.value = e.detail.value
  // TODO: 实现深色模式逻辑
  showToast(darkMode.value ? '已开启深色模式' : '已关闭深色模式')
}

// 切换开发者模式
const toggleDeveloperMode = (e) => {
  developerMode.value = e.detail.value
  showToast(developerMode.value ? '已开启开发者模式' : '已关闭开发者模式')
}

// 清除缓存
const clearCache = () => {
  uni.showModal({
    title: '提示',
    content: '确定要清除缓存吗？',
    success: (res) => {
      if (res.confirm) {
        // TODO: 实现清除缓存逻辑
        cacheSize.value = '0MB'
        uni.showToast({
          title: '缓存已清除',
          icon: 'success'
        })
      }
    }
  })
}

// 退出登录
const handleLogout = () => {
  if (!isLoggedIn.value) {
    uni.showToast({
      title: '您还未登录',
      icon: 'none'
    })
    return
  }
  
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: async (res) => {
      if (res.confirm) {
        await userStore.logout()
        
        uni.reLaunch({
          url: '/pages/login'
        })
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  color: #333;
  padding-top: 0; /* NavBar组件自己处理占位空间 */
}

// Header样式已移除，使用NavBar组件

.settings-section {
  background-color: #fff;
  margin-bottom: 20rpx;
}

.settings-header {
  padding: 30rpx;
  font-size: 28rpx;
  color: #999;
  border-bottom: 1rpx solid #f0f0f0;
}

.settings-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
  transition: background-color 0.2s;
}

.settings-item:last-child {
  border-bottom: none;
}

.settings-item:active {
  background-color: #f8f9fa;
}

.settings-icon {
  width: 48rpx;
  height: 48rpx;
  margin-right: 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.settings-content {
  flex: 1;
}

.settings-title {
  font-size: 32rpx;
  color: #333;
}

.settings-desc {
  font-size: 32rpx;
  color: #999;
  margin-top: 8rpx;
}

.settings-right {
  display: flex;
  align-items: center;
}

.settings-value {
  font-size: 28rpx;
  color: #999;
  margin-right: 20rpx;
}

.badge {
  display: inline-block;
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  font-size: 32rpx;
  background-color: #f0f7ff;
  color: #4A90E2;
  margin-right: 20rpx;
}

.badge-new {
  background-color: #f6ffed;
  color: #52c41a;
}

.logout-section {
  padding: 30rpx;
}

.logout-button {
  width: 100%;
  height: 88rpx;
  line-height: 88rpx;
  background-color: #fff;
  color: #ff4d4f;
  text-align: center;
  border-radius: 8rpx;
  font-size: 32rpx;
  border: 1rpx solid #f0f0f0;
  transition: all 0.2s;
}

.logout-button:active {
  background-color: #fff2f0;
}
</style>
