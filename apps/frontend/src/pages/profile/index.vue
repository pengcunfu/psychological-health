<template>
  <view class="container tab-page">
    <view class="header">
      <view class="user-info" @click="goToEditProfile">
        <u-avatar :src="userInfo.avatar || '/static/images/default-avatar.png'" size="160"></u-avatar>
        <view class="user-detail">
          <text class="username">{{ userInfo.username || '未登录' }}</text>
          <text class="user-id">ID: {{ userInfo.id || '-' }}</text>
        </view>
        <u-icon name="arrow-right" color="#fff" size="30"></u-icon>
      </view>
    </view>

    <view class="menu-section">
      <view class="section-title">我的服务</view>
      <view class="menu-grid">
        <view class="menu-item" @click="navigateTo('/pages/order/index')">
          <u-icon name="shopping-cart" size="60" color="#4A90E2"></u-icon>
          <text class="menu-text">我的订单</text>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/appointment/index')">
          <u-icon name="calendar" size="60" color="#52c41a"></u-icon>
          <text class="menu-text">我的预约</text>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/profile/MyCourse/index')">
          <u-icon name="book" size="60" color="#faad14"></u-icon>
          <text class="menu-text">我的课程</text>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/profile/MyFavorite/index')">
          <u-icon name="star" size="60" color="#f5222d"></u-icon>
          <text class="menu-text">我的收藏</text>
        </view>
      </view>
    </view>

    <view class="list-section">
      <view class="section-title">账户设置</view>
      <view class="list-group">
        <view class="list-item" @click="navigateTo('/pages/profile/edit/index')">
          <u-icon name="account" size="40" color="#4A90E2"></u-icon>
          <text class="item-text">个人资料</text>
          <u-icon name="arrow-right" color="#ccc" size="30"></u-icon>
        </view>
        <view class="list-item" @click="navigateTo('/pages/profile/security/index')">
          <u-icon name="lock" size="40" color="#52c41a"></u-icon>
          <text class="item-text">账号安全</text>
          <u-icon name="arrow-right" color="#ccc" size="30"></u-icon>
        </view>
        <view class="list-item" @click="navigateTo('/pages/profile/BecomeCounselor/index')">
          <u-icon name="medal" size="40" color="#faad14"></u-icon>
          <text class="item-text">成为咨询师</text>
          <u-icon name="arrow-right" color="#ccc" size="30"></u-icon>
        </view>
      </view>
    </view>

    <view class="list-section">
      <view class="section-title">关于我们</view>
      <view class="list-group">
        <view class="list-item" @click="navigateTo('/pages/profile/ContactUs/index')">
          <u-icon name="phone" size="40" color="#4A90E2"></u-icon>
          <text class="item-text">联系我们</text>
          <u-icon name="arrow-right" color="#ccc" size="30"></u-icon>
        </view>
        <view class="list-item" @click="navigateTo('/pages/profile/agreement/index')">
          <u-icon name="file-text" size="40" color="#52c41a"></u-icon>
          <text class="item-text">用户协议</text>
          <u-icon name="arrow-right" color="#ccc" size="30"></u-icon>
        </view>
        <view class="list-item" @click="navigateTo('/pages/profile/privacy/index')">
          <u-icon name="shield" size="40" color="#faad14"></u-icon>
          <text class="item-text">隐私政策</text>
          <u-icon name="arrow-right" color="#ccc" size="30"></u-icon>
        </view>
      </view>
    </view>

    <view class="logout-btn" @click="handleLogout" v-if="isLoggedIn">退出登录</view>
    <view class="login-btn" @click="goToLogin" v-else>立即登录</view>
  </view>
</template>

<script>
import { computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'

export default {
  setup() {
    const userStore = useUserStore()
    
    // 用户信息
    const userInfo = computed(() => userStore.userInfo || {})
    
    // 是否已登录
    const isLoggedIn = computed(() => userStore.isLoggedIn)
    
    // 页面跳转
    const navigateTo = (url) => {
      // 检查是否需要登录
      if (!isLoggedIn.value && url !== '/pages/profile/agreement/index' && url !== '/pages/profile/privacy/index' && url !== '/pages/profile/ContactUs/index') {
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
      // 获取用户信息
      if (isLoggedIn.value) {
        userStore.getUserInfo()
      }
    })
    
    return {
      userInfo,
      isLoggedIn,
      navigateTo,
      goToEditProfile,
      goToLogin,
      handleLogout
    }
  }
}
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 30rpx;
}

.header {
  background-color: #4A90E2;
  padding: 60rpx 30rpx;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-detail {
  flex: 1;
  margin-left: 30rpx;
}

.username {
  font-size: 40rpx;
  color: #fff;
  font-weight: bold;
  display: block;
  margin-bottom: 10rpx;
}

.user-id {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
}

.menu-section {
  background-color: #fff;
  border-radius: 20rpx;
  margin: -40rpx 30rpx 30rpx;
  padding: 30rpx;
  position: relative;
  z-index: 1;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
}

.menu-grid {
  display: flex;
  flex-wrap: wrap;
}

.menu-item {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx 0;
}

.menu-text {
  font-size: 24rpx;
  color: #666;
  margin-top: 10rpx;
}

.list-section {
  background-color: #fff;
  border-radius: 20rpx;
  margin: 0 30rpx 30rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.list-group {
  border-radius: 10rpx;
  overflow: hidden;
}

.list-item {
  display: flex;
  align-items: center;
  padding: 30rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.list-item:last-child {
  border-bottom: none;
}

.item-text {
  flex: 1;
  font-size: 28rpx;
  color: #333;
  margin-left: 20rpx;
}

.logout-btn, .login-btn {
  width: 90%;
  height: 90rpx;
  line-height: 90rpx;
  background-color: #fff;
  color: #f5222d;
  font-size: 32rpx;
  text-align: center;
  border-radius: 10rpx;
  margin: 60rpx auto;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.login-btn {
  background-color: #4A90E2;
  color: #fff;
}
</style> 