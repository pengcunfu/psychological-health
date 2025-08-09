<template>
  <view class="container tab-page">
    <!-- 用户资料 -->
    <view class="user-profile" @click="goToEditProfile">
      <image class="user-avatar" :src="userInfo.avatar || '/static/wx/images/default-avatar.png'" mode="aspectFill">
      </image>
      <view class="user-info">
        <view class="user-name">{{ userInfo.phone || userInfo.name || '138****1234' }}</view>
        <view class="user-id">ID: {{ userInfo.id || '12345678' }}</view>
      </view>
      <view class="profile-arrow">
        <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
      </view>
    </view>

    <!-- 我的服务导航 -->
    <view class="nav-grid">
      <view 
        class="nav-item" 
        v-for="(item, index) in myServicesMenuItems" 
        :key="index" 
        @click="handleMenuClick(item)"
      >
        <view class="nav-icon" :style="{ backgroundColor: item.bgColor }">
          <SvgIcon 
            :name="item.iconName" 
            path="profile"
            :size="40"
            :color="item.color"
          />
        </view>
        <text class="nav-text">{{ item.name }}</text>
      </view>
    </view>

    <!-- 其他功能 -->
    <view class="menu-section">
      <view class="menu-item" @click="navigateTo('/pages/profile/message')">
        <view class="item-icon">
          <SvgIcon name="notification" path="profile" :size="32" color="#FF6B35" />
        </view>
        <view class="item-text">消息中心</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>

      <view class="menu-item" @click="navigateTo('/pages/order/index')">
        <view class="item-icon">
          <SvgIcon name="bookmark" path="profile" :size="32" color="#13C2C2" />
        </view>
        <view class="item-text">订单管理</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>

      <view class="menu-item" @click="navigateTo('/pages/consultant/index')">
        <view class="item-icon">
          <SvgIcon name="account" path="profile" :size="32" color="#722ED1" />
        </view>
        <view class="item-text">咨询人管理</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>

      <view class="menu-item" @click="navigateTo('/pages/profile/setting')">
        <view class="item-icon">
          <SvgIcon name="setting" path="profile" :size="32" color="#722ED1" />
        </view>
        <view class="item-text">系统设置</view>
        <view class="item-arrow">
          <SvgIcon name="arrow-right" path="profile" :size="28" color="#999" />
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { redirectToLogin } from '@/utils/auth'
import SvgIcon from '@/components/SvgIcon.vue'

const userStore = useUserStore()

// 用户信息
const userInfo = computed(() => userStore.userInfo || {})

// 是否已登录
const isLoggedIn = computed(() => userStore.isLoggedIn)

// 我的服务菜单数据
const myServicesMenuItems = ref([
  { 
    name: '我的预约', 
    color: '#1890ff', 
    bgColor: '#e6f7ff',
    url: '/pages/profile/my-appointment',
    iconName: 'calendar'
  },
  { 
    name: '我的课程', 
    color: '#52c41a', 
    bgColor: '#f6ffed',
    url: '/pages/profile/my-course',
    iconName: 'book'
  },
  { 
    name: '我的测评', 
    color: '#fa8c16', 
    bgColor: '#fff7e6',
    url: '/pages/profile/my-assessment',
    iconName: 'checkmark-circle'
  },
  { 
    name: '我的收藏', 
    color: '#eb2f96', 
    bgColor: '#fff0f6',
    url: '/pages/profile/my-favorite',
    iconName: 'bookmark'
  }
])

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
  if (!isLoggedIn.value) {
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

// 处理导航菜单点击
const handleMenuClick = (item) => {
  if (item.url) {
    navigateTo(item.url)
  }
}

// 跳转到编辑个人资料页
const goToEditProfile = () => {
  if (!isLoggedIn.value) {
    uni.navigateTo({
      url: '/pages/login'
    })
    return
  }

  uni.navigateTo({
    url: '/pages/profile/edit'
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

// 菜单项
.menu-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
  position: relative;
  transition: background-color 0.2s;

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background: #f8f9fa;
  }
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

// 导航网格样式 (基于 NavigationMenu.vue)
.nav-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  margin: 0 20rpx 20rpx;
  padding: 20rpx;
  background-color: #fff;
  border-radius: 16rpx;
  overflow: hidden;

  .nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20rpx;
    transition: transform 0.2s ease;

    &:active {
      transform: scale(0.95);

      .nav-icon {
        transform: scale(0.9);
      }
    }

    .nav-icon {
      width: 80rpx;
      height: 80rpx;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 12rpx;
      transition: all 0.3s ease;
    }

    .nav-text {
      font-size: 24rpx;
      color: #333;
      text-align: center;
      line-height: 1.2;
    }
  }
}
</style>