<template>
  <view class="profile-page">
    <!-- 顶部个人信息区域 -->
    <view class="profile-header" @click="navigateTo('/pages/profile/edit/index')">
      <view class="avatar-container">
        <view class="avatar" mode="aspectFill">
          <text>用户头像</text>
        </view>
      </view>
      <view class="user-info">
        <text class="username">张三</text>
        <text class="user-id">ID: 12345678</text>
      </view>
    </view>

    <!-- 我的服务区域 -->
    <view class="card-section">
      <view class="section-title">我的服务</view>
      
      <view class="section-items">
        <view class="menu-item" @click="navigateTo('/pages/profile/MyCourse/index')">
          <view class="icon-wrap course-icon"></view>
          <text class="item-text">我的课程</text>
          <text class="item-arrow">›</text>
        </view>
        
        <view class="menu-item" @click="navigateTo('/pages/profile/MyFavorite/index')">
          <view class="icon-wrap favorite-icon"></view>
          <text class="item-text">我的收藏</text>
          <text class="item-arrow">›</text>
        </view>

        <view class="menu-item" @click="navigateTo('/pages/profile/BecomeCounselor/index')">
          <view class="icon-wrap become-counselor-icon"></view>
          <text class="item-text">成为咨询师</text>
          <text class="item-arrow">›</text>
        </view>
      </view>
    </view>

    <!-- 设置与帮助区域 -->
    <view class="card-section">
      <view class="section-title">设置与帮助</view>
      
      <view class="section-items">
        <view class="menu-item" @click="navigateTo('/pages/profile/CustomService/index')">
          <view class="icon-wrap service-icon"></view>
          <text class="item-text">联系客服</text>
          <text class="item-arrow">›</text>
        </view>
        
        <view class="menu-item" @click="navigateTo('/pages/profile/privacy/index')">
          <view class="icon-wrap privacy-icon"></view>
          <text class="item-text">隐私协议</text>
          <text class="item-arrow">›</text>
        </view>
        
        <view class="menu-item" @click="navigateTo('/pages/profile/agreement/index')">
          <view class="icon-wrap agreement-icon"></view>
          <text class="item-text">用户协议</text>
          <text class="item-arrow">›</text>
        </view>
      </view>
    </view>
    
    <!-- 退出登录 -->
    <view class="logout-btn" @click="logout">
      退出登录
    </view>
  </view>
</template>

<script setup>
import { onLoad } from '@dcloudio/uni-app'

// 页面加载
onLoad(() => {
  console.log('我的')
})

// 页面跳转方法
const navigateTo = (url) => {
  uni.navigateTo({
    url
  })
}

// 退出登录
const logout = () => {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        // 执行退出登录操作
        uni.removeStorageSync('token')
        uni.removeStorageSync('userInfo')
        
        
        // 跳转到登录页
        uni.reLaunch({
          url: '/pages/login/index'
        })
      }
    }
  })
}
</script>

<style lang="scss" scoped>
@import '@/static/theme.scss';

.profile-page {
  min-height: 100vh;
  background-color: $mg-gray-100;
  padding-bottom: 40rpx;
}

// 顶部个人信息区域
.profile-header {
  background-color: $mg-primary;
  padding: 60rpx 40rpx;
  display: flex;
  align-items: center;
  position: relative;
  
  .avatar-container {
    width: 140rpx;
    height: 140rpx;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.2);
    border: 4rpx solid $mg-white;
    overflow: hidden;
    
    .avatar {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24rpx;
      color: $mg-white;
    }
  }
  
  .user-info {
    margin-left: 30rpx;
    
    .username {
      font-size: 40rpx;
      color: $mg-white;
      font-weight: 500;
      margin-bottom: 10rpx;
    }
    
    .user-id {
      font-size: 28rpx;
      color: rgba(255, 255, 255, 0.8);
    }
  }
}

// 卡片区域
.card-section {
  margin: 24rpx 24rpx 0;
  background-color: $mg-white;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
  
  .section-title {
    font-size: 32rpx;
    font-weight: 500;
    color: $mg-text-primary;
    padding: 30rpx 24rpx 20rpx;
  }
  
  .section-items {
    .menu-item {
      display: flex;
      align-items: center;
      padding: 30rpx 24rpx;
      position: relative;
      
      &:after {
        content: '';
        position: absolute;
        left: 90rpx;
        right: 0;
        bottom: 0;
        height: 1rpx;
        background-color: $mg-border-light;
      }
      
      &:last-child:after {
        display: none;
      }
      
      .icon-wrap {
        width: 60rpx;
        height: 60rpx;
        border-radius: 50%;
        background-color: rgba($mg-primary, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 24rpx;
        position: relative;
        
        // 所有图标共用样式
        &:before {
          content: '';
          position: absolute;
          width: 32rpx;
          height: 32rpx;
          background-color: $mg-primary;
          border-radius: 3px;
        }
        
        // 课程图标
        &.course-icon:before {
          mask-size: cover;
          -webkit-mask-size: cover;
          mask-position: center;
          -webkit-mask-position: center;
          mask-repeat: no-repeat;
          -webkit-mask-repeat: no-repeat;
          mask-image: url('data:image/svg+xml;utf8,<svg t="1620000000000" class="icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path d="M832 64H192c-17.7 0-32 14.3-32 32v832c0 17.7 14.3 32 32 32h640c17.7 0 32-14.3 32-32V96c0-17.7-14.3-32-32-32z m-260 72h96v209.9L621.5 312 572 347.4V136z" fill="#333333"></path></svg>');
          -webkit-mask-image: url('data:image/svg+xml;utf8,<svg t="1620000000000" class="icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path d="M832 64H192c-17.7 0-32 14.3-32 32v832c0 17.7 14.3 32 32 32h640c17.7 0 32-14.3 32-32V96c0-17.7-14.3-32-32-32z m-260 72h96v209.9L621.5 312 572 347.4V136z" fill="#333333"></path></svg>');
        }
        
        // 收藏图标
        &.favorite-icon:before {
          mask-size: cover;
          -webkit-mask-size: cover;
          mask-position: center;
          -webkit-mask-position: center;
          mask-repeat: no-repeat;
          -webkit-mask-repeat: no-repeat;
          mask-image: url('data:image/svg+xml;utf8,<svg t="1620000000000" class="icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path d="M512 736.4l-288 160.9 72-315.6L48 357.6l316.8-24L512 32l147.2 301.6 316.8 24-248 224.1 72 315.6z" fill="#333333"></path></svg>');
          -webkit-mask-image: url('data:image/svg+xml;utf8,<svg t="1620000000000" class="icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path d="M512 736.4l-288 160.9 72-315.6L48 357.6l316.8-24L512 32l147.2 301.6 316.8 24-248 224.1 72 315.6z" fill="#333333"></path></svg>');
        }
        
        // 客服图标
        &.service-icon:before {
          mask-size: cover;
          -webkit-mask-size: cover;
          mask-position: center;
          -webkit-mask-position: center;
          mask-repeat: no-repeat;
          -webkit-mask-repeat: no-repeat;
          mask-image: url('data:image/svg+xml;utf8,<svg t="1620000000000" class="icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path d="M512 64c-247.42 0-448 200.58-448 448 0 247.42 200.58 448 448 448s448-200.58 448-448c0-247.42-200.58-448-448-448z m0 820c-205.5 0-372-166.5-372-372s166.5-372 372-372 372 166.5 372 372-166.5 372-372 372z M696.946 258.944a289.328 289.328 0 0 0-184.97-66.592c-160.662 0-291.328 130.662-291.328 291.328 0 160.656 130.666 291.328 291.328 291.328 160.666 0 291.328-130.672 291.328-291.328 0-65.624-21.742-126.178-58.46-174.96-4.704-4.75-10.986-7.352-17.464-7.352-6.476 0-12.758 2.602-17.464 7.352a24.64 24.64 0 0 0 0 34.936 240.94 240.94 0 0 1 51.326 149.352c0 133.786-108.954 242.746-242.746 242.746s-242.746-108.96-242.746-242.746c0-133.786 108.954-242.746 242.746-242.746 59.33 0 116.644 21.504 161.432 60.576a24.642 24.642 0 0 0 34.936 0c9.658-9.656 9.658-25.282 0-34.934 0 0-0.002-0.002-0.002-0.004a289.262 289.262 0 0 0-13.916-16.956zM512 480a31.994 31.994 0 0 0-32 32v160a32 32 0 0 0 64 0V512a31.994 31.994 0 0 0-32-32z m0-160a31.994 31.994 0 0 0-32 32v32a32 32 0 0 0 64 0v-32a31.994 31.994 0 0 0-32-32z" fill="#333333"></path></svg>');
          -webkit-mask-image: url('data:image/svg+xml;utf8,<svg t="1620000000000" class="icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path d="M512 64c-247.42 0-448 200.58-448 448 0 247.42 200.58 448 448 448s448-200.58 448-448c0-247.42-200.58-448-448-448z m0 820c-205.5 0-372-166.5-372-372s166.5-372 372-372 372 166.5 372 372-166.5 372-372 372z M696.946 258.944a289.328 289.328 0 0 0-184.97-66.592c-160.662 0-291.328 130.662-291.328 291.328 0 160.656 130.666 291.328 291.328 291.328 160.666 0 291.328-130.672 291.328-291.328 0-65.624-21.742-126.178-58.46-174.96-4.704-4.75-10.986-7.352-17.464-7.352-6.476 0-12.758 2.602-17.464 7.352a24.64 24.64 0 0 0 0 34.936 240.94 240.94 0 0 1 51.326 149.352c0 133.786-108.954 242.746-242.746 242.746s-242.746-108.96-242.746-242.746c0-133.786 108.954-242.746 242.746-242.746 59.33 0 116.644 21.504 161.432 60.576a24.642 24.642 0 0 0 34.936 0c9.658-9.656 9.658-25.282 0-34.934 0 0-0.002-0.002-0.002-0.004a289.262 289.262 0 0 0-13.916-16.956zM512 480a31.994 31.994 0 0 0-32 32v160a32 32 0 0 0 64 0V512a31.994 31.994 0 0 0-32-32z m0-160a31.994 31.994 0 0 0-32 32v32a32 32 0 0 0 64 0v-32a31.994 31.994 0 0 0-32-32z" fill="#333333"></path></svg>');
        }
        
        // 隐私图标
        &.privacy-icon:before {
          mask-size: cover;
          -webkit-mask-size: cover;
          mask-position: center;
          -webkit-mask-position: center;
          mask-repeat: no-repeat;
          -webkit-mask-repeat: no-repeat;
          mask-image: url('data:image/svg+xml;utf8,<svg t="1620000000000" class="icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path d="M512 170.666667c-117.824 0-213.333333 95.509333-213.333333 213.333333 0 87.466667 52.736 162.816 128 196.096V661.333333a85.333333 85.333333 0 0 0 85.333333 85.333334 85.333333 85.333333 0 0 0 85.333333-85.333334v-81.237333c75.264-33.28 128-108.629333 128-196.096 0-117.824-95.509333-213.333333-213.333333-213.333333z m0 384a170.666667 170.666667 0 1 1 0-341.333334 170.666667 170.666667 0 0 1 0 341.333334z" fill="#333333"></path></svg>');
          -webkit-mask-image: url('data:image/svg+xml;utf8,<svg t="1620000000000" class="icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path d="M512 170.666667c-117.824 0-213.333333 95.509333-213.333333 213.333333 0 87.466667 52.736 162.816 128 196.096V661.333333a85.333333 85.333333 0 0 0 85.333333 85.333334 85.333333 85.333333 0 0 0 85.333333-85.333334v-81.237333c75.264-33.28 128-108.629333 128-196.096 0-117.824-95.509333-213.333333-213.333333-213.333333z m0 384a170.666667 170.666667 0 1 1 0-341.333334 170.666667 170.666667 0 0 1 0 341.333334z" fill="#333333"></path></svg>');
        }
        
        // 协议图标
        &.agreement-icon:before {
          mask-size: cover;
          -webkit-mask-size: cover;
          mask-position: center;
          -webkit-mask-position: center;
          mask-repeat: no-repeat;
          -webkit-mask-repeat: no-repeat;
          mask-image: url('data:image/svg+xml;utf8,<svg t="1620000000000" class="icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path d="M853.333333 960H170.666667V64h469.333333l213.333333 213.333333v682.666667zM213.333333 917.333333h597.333334V298.666667H618.666667V128H213.333333v789.333333z m128-170.666666v-42.666667h341.333334v42.666667H341.333333z m0-128v-42.666667h341.333334v42.666667H341.333333z m0-128v-42.666667h341.333334v42.666667H341.333333z" fill="#333333"></path></svg>');
          -webkit-mask-image: url('data:image/svg+xml;utf8,<svg t="1620000000000" class="icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path d="M853.333333 960H170.666667V64h469.333333l213.333333 213.333333v682.666667zM213.333333 917.333333h597.333334V298.666667H618.666667V128H213.333333v789.333333z m128-170.666666v-42.666667h341.333334v42.666667H341.333333z m0-128v-42.666667h341.333334v42.666667H341.333333z m0-128v-42.666667h341.333334v42.666667H341.333333z" fill="#333333"></path></svg>');
        }
      }
      
      .item-text {
        flex: 1;
        font-size: 30rpx;
        color: $mg-text-primary;
      }
      
      .item-arrow {
        font-size: 36rpx;
        color: $mg-text-tertiary;
        margin-left: 20rpx;
      }
    }
  }
}

// 退出登录按钮
.logout-btn {
  margin: 60rpx 24rpx 0;
  height: 90rpx;
  line-height: 90rpx;
  text-align: center;
  font-size: 32rpx;
  color: $mg-accent;
  background-color: $mg-white;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}
</style>