<template>
  <view class="container tab-page">
    <!-- 顶部导航栏 -->
    <view class="header">
      <view class="header-title">个人中心</view>
      <view class="header-icon" @click="goToSettings">
        <SvgIcon name="setting" path="profile" :size="32" color="#333" />
      </view>
    </view>

    <!-- 用户资料 -->
    <view class="user-profile" @click="goToEditProfile">
      <image class="user-avatar" :src="userInfo.avatar || '/static/images/default-avatar.png'" mode="aspectFill">
      </image>
      <view class="user-info">
        <view class="user-name">{{ userInfo.username || userInfo.name || '张三' }}</view>
        <view class="user-id">ID: {{ userInfo.id || '12345678' }}</view>
      </view>
      <view class="profile-arrow">
        <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
      </view>
    </view>

    <!-- 心理服务 -->
    <view class="menu-section">
      <view class="section-title">心理服务</view>

      <view class="menu-item" @click="navigateTo('/pages/appointment/index')">
        <view class="item-icon">
          <SvgIcon name="calendar" path="profile" :size="32" color="#4A90E2" />
        </view>
        <view class="item-text">我的预约</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>

      <view class="menu-item" @click="navigateTo('/pages/profile/MyCourse/index')">
        <view class="item-icon">
          <SvgIcon name="book" path="profile" :size="32" color="#52C41A" />
        </view>
        <view class="item-text">我的课程</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>

      <view class="menu-item" @click="navigateTo('/pages/profile/evaluation/index')">
        <view class="item-icon">
          <SvgIcon name="checkmark-circle" path="profile" :size="32" color="#FA8C16" />
        </view>
        <view class="item-text">我的测评</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>

      <view class="menu-item" @click="navigateTo('/pages/profile/MyFavorite/index')">
        <view class="item-icon">
          <SvgIcon name="bookmark" path="profile" :size="32" color="#EB2F96" />
        </view>
        <view class="item-text">我的收藏</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>
    </view>

    <!-- 账户管理 -->
    <view class="menu-section">
      <view class="section-title">账户管理</view>

      <view class="menu-item" @click="navigateTo('/pages/profile/edit/index')">
        <view class="item-icon">
          <SvgIcon name="account" path="profile" :size="32" color="#722ED1" />
        </view>
        <view class="item-text">个人资料</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>

      <view class="menu-item" @click="navigateTo('/pages/profile/security/index')">
        <view class="item-icon">
          <SvgIcon name="shield" path="profile" :size="32" color="#F5222D" />
        </view>
        <view class="item-text">安全设置</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>
    </view>

    <!-- 其他 -->
    <view class="menu-section">
      <view class="section-title">其他</view>

      <view class="menu-item" @click="navigateTo('/pages/profile/help/index')">
        <view class="item-icon">
          <SvgIcon name="help-circle" path="profile" :size="32" color="#1890FF" />
        </view>
        <view class="item-text">帮助中心</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>

      <view class="menu-item" @click="navigateTo('/pages/profile/ContactUs/index')">
        <view class="item-icon">
          <SvgIcon name="info-circle" path="profile" :size="32" color="#13C2C2" />
        </view>
        <view class="item-text">关于我们</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>

      <view class="menu-item" @click="navigateTo('/pages/profile/settings/index')">
        <view class="item-icon">
          <SvgIcon name="setting" path="profile" :size="32" color="#999" />
        </view>
        <view class="item-text">设置</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>
    </view>

    <!-- 退出登录按钮 -->
    <view class="logout-section">
      <view class="logout-btn" @click="handleLogout" v-if="isLoggedIn">
        退出登录
      </view>
      <view class="login-btn" @click="goToLogin" v-else>
        立即登录
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { checkLogin, redirectToLogin } from '@/utils/auth'
import SvgIcon from '@/components/SvgIcon/index.vue'

const userStore = useUserStore()

// 用户信息
const userInfo = computed(() => userStore.userInfo || {})

// 是否已登录
const isLoggedIn = computed(() => userStore.isLoggedIn)

// 检查登录状态并处理重定向
const checkLoginStatus = () => {
  if (!isLoggedIn.value) {
    // 显示提示并跳转到登录页
    uni.showToast({
      title: '请先登录',
      icon: 'none'
    })

    setTimeout(() => {
      redirectToLogin('/pages/profile/index')
    }, 1500)
    return false
  }
  return true
}

// 页面跳转
const navigateTo = (url) => {
  // 检查是否需要登录
  if (!isLoggedIn.value &&
    url !== '/pages/profile/agreement/index' &&
    url !== '/pages/profile/privacy/index' &&
    url !== '/pages/profile/ContactUs/index' &&
    url !== '/pages/profile/help/index') {
    uni.showToast({
      title: '请先登录',
      icon: 'none'
    })

    setTimeout(() => {
      uni.navigateTo({
        url: '/pages/login/index'
      })
    }, 1500)
    return
  }

  uni.navigateTo({ url })
}

// 跳转到编辑个人资料页
const goToEditProfile = () => {
  if (!isLoggedIn.value) {
    uni.navigateTo({
      url: '/pages/login/index'
    })
    return
  }

  uni.navigateTo({
    url: '/pages/profile/edit/index'
  })
}

// 跳转到设置页
const goToSettings = () => {
  uni.navigateTo({
    url: '/pages/profile/settings/index'
  })
}

// 跳转到登录页
const goToLogin = () => {
  uni.navigateTo({
    url: '/pages/login/index'
  })
}

// 退出登录
const handleLogout = () => {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: async (res) => {
      if (res.confirm) {
        await userStore.logout()

        uni.showToast({
          title: '已退出登录',
          icon: 'success'
        })

        // 刷新页面
        setTimeout(() => {
          uni.reLaunch({
            url: '/pages/index/index'
          })
        }, 1500)
      }
    }
  })
}

// 页面加载
onLoad(() => {
  // 检查登录状态
  if (!checkLoginStatus()) {
    return
  }

  // 获取用户信息
  if (isLoggedIn.value) {
    userStore.getUserInfo()
  }
})

// 页面显示时也检查登录状态
onShow(() => {
  // 每次页面显示时都检查登录状态
  checkLoginStatus()
})
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 30rpx;
}

// 顶部导航栏
.header {
  padding: 30rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
}

.header-title {
  font-size: 36rpx;
  font-weight: bold;
  flex: 1;
  text-align: center;
  color: #333;
}

.header-icon {
  width: 48rpx;
  height: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

// 用户资料
.user-profile {
  background: #fff;
  padding: 40rpx 30rpx;
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.user-avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  margin-right: 30rpx;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 10rpx;
  color: #333;
}

.user-id {
  font-size: 24rpx;
  color: #999;
}

.profile-arrow {
  width: 32rpx;
  height: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

// 菜单分组
.menu-section {
  background: #fff;
  border-radius: 16rpx;
  margin: 0 20rpx 20rpx;
  overflow: hidden;
}

.section-title {
  font-size: 28rpx;
  color: #999;
  padding: 20rpx 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
  background: #fafafa;
}

// 菜单项
.menu-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
  position: relative;
  transition: background-color 0.2s;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:active {
  background: #f8f9fa;
}

.item-icon {
  width: 48rpx;
  height: 48rpx;
  margin-right: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-text {
  flex: 1;
  font-size: 28rpx;
  color: #333;
}

.item-arrow {
  width: 32rpx;
  height: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

// 退出登录区域
.logout-section {
  padding: 40rpx 30rpx;
}

.logout-btn,
.login-btn {
  width: 100%;
  height: 88rpx;
  line-height: 88rpx;
  background: #fff;
  color: #ff4d4f;
  font-size: 28rpx;
  text-align: center;
  border-radius: 16rpx;
  border: 1rpx solid #f0f0f0;
  transition: all 0.2s;
}

.logout-btn:active {
  background: #fff2f0;
}

.login-btn {
  background: #4A90E2;
  color: #fff;
  border-color: #4A90E2;
}

.login-btn:active {
  background: #357abd;
}
</style>