<template>
  <view class="profile-container">
    <!-- 顶部个人信息 -->
    <view class="profile-header" style="background-color: #F9EFD6;">
      <view class="user-info">
        <view class="avatar-container">
          <image class="avatar" :src="counselorInfo.avatar" mode="aspectFill"></image>
          <view class="edit-avatar" @click="changeAvatar">
            <view class="edit-icon"></view>
          </view>
        </view>
        <view class="basic-info">
          <view class="name-container">
            <text class="name">{{counselorInfo.name}}</text>
            <view class="verified-badge" v-if="counselorInfo.isVerified">已认证</view>
          </view>
          <view class="title">{{counselorInfo.title}}</view>
          <view class="specialties">
            <text class="specialty-tag" v-for="(specialty, index) in counselorInfo.specialties" :key="index">{{specialty}}</text>
          </view>
        </view>
      </view>
      
      <view class="profile-stats">
        <view class="stat-item">
          <text class="stat-value">{{counselorInfo.sessionsCount}}</text>
          <text class="stat-label">咨询总数</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">{{counselorInfo.clientCount}}</text>
          <text class="stat-label">服务客户</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">{{counselorInfo.rating.toFixed(1)}}</text>
          <text class="stat-label">平均评分</text>
        </view>
      </view>
    </view>

    <!-- 个人简介 -->
    <view class="section profile-bio" style="background-color: #F9EFD6;">
      <view class="section-header">
        <text class="section-title">个人简介</text>
        <view class="edit-button" @click="editSection('bio')">编辑</view>
      </view>
      <view class="section-content bio-content">
        <text>{{counselorInfo.bio}}</text>
      </view>
    </view>

    <!-- 专业资质 -->
    <view class="section qualifications" style="background-color: #EAF7EA;">
      <view class="section-header">
        <text class="section-title">专业资质</text>
        <view class="edit-button" @click="editSection('qualifications')">编辑</view>
      </view>
      <view class="section-content">
        <view class="qualification-item" v-for="(qual, index) in counselorInfo.qualifications" :key="index">
          <view class="qualification-icon" :class="getQualificationIcon(qual.type)"></view>
          <view class="qualification-details">
            <text class="qualification-title">{{qual.title}}</text>
            <text class="qualification-org">{{qual.organization}}</text>
            <text class="qualification-date">{{qual.date}}</text>
          </view>
          <view class="verification-status" :class="{ verified: qual.verified }">
            {{qual.verified ? '已验证' : '待验证'}}
          </view>
        </view>
      </view>
    </view>

    <!-- 收费标准 -->
    <view class="section pricing" style="background-color: #E7F3FE;">
      <view class="section-header">
        <text class="section-title">收费标准</text>
        <view class="edit-button" @click="editSection('pricing')">编辑</view>
      </view>
      <view class="section-content">
        <view class="pricing-item" v-for="(price, index) in counselorInfo.pricing" :key="index">
          <view class="service-type">{{price.serviceType}}</view>
          <view class="service-duration">{{price.duration}}分钟</view>
          <view class="service-price">¥{{price.price}}</view>
        </view>
      </view>
    </view>

    <!-- 账户设置 -->
    <view class="settings-section" style="background-color: #F9EFD6;">
      <view class="setting-item" @click="navigateTo('/pages/counselor/settings/personal')">
        <view class="setting-icon personal"></view>
        <view class="setting-text">个人资料设置</view>
        <view class="arrow-icon"></view>
      </view>
      <view class="setting-item" @click="navigateTo('/pages/counselor/settings/account')">
        <view class="setting-icon account"></view>
        <view class="setting-text">账户与安全</view>
        <view class="arrow-icon"></view>
      </view>
      <view class="setting-item" @click="navigateTo('/pages/counselor/settings/payment')">
        <view class="setting-icon payment"></view>
        <view class="setting-text">收款设置</view>
        <view class="arrow-icon"></view>
      </view>
      <view class="setting-item" @click="navigateTo('/pages/counselor/settings/notification')">
        <view class="setting-icon notification"></view>
        <view class="setting-text">通知设置</view>
        <view class="arrow-icon"></view>
      </view>
      <view class="setting-item" @click="navigateTo('/pages/counselor/settings/privacy')">
        <view class="setting-icon privacy"></view>
        <view class="setting-text">隐私设置</view>
        <view class="arrow-icon"></view>
      </view>
    </view>

    <!-- 底部按钮 -->
    <view class="bottom-buttons">
      <button class="preview-button" @click="previewPublicProfile">预览公开主页</button>
      <button class="logout-button" @click="logout">退出登录</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      counselorInfo: {
        name: '王晓华',
        title: '心理咨询师 / 高级婚姻家庭咨询师',
        avatar: 'https://randomuser.me/api/portraits/women/68.jpg',
        isVerified: true,
        specialties: ['抑郁症', '焦虑障碍', '婚姻家庭', '青少年心理'],
        sessionsCount: 286,
        clientCount: 78,
        rating: 4.8,
        bio: '从业8年，毕业于北京师范大学心理学专业，拥有国家二级心理咨询师资格证书和美国婚姻家庭治疗协会（AAMFT）认证资格。擅长抑郁症、焦虑障碍的认知行为治疗，以及婚姻关系、亲子关系的系统式家庭治疗。我相信每个人都有自愈的能力，作为咨询师，我的职责是陪伴并激发来访者内在的力量，共同面对困境，找到成长的方向。',
        qualifications: [
          {
            type: 'degree',
            title: '心理学硕士',
            organization: '北京师范大学',
            date: '2015年',
            verified: true
          },
          {
            type: 'certificate',
            title: '国家二级心理咨询师',
            organization: '中国心理卫生协会',
            date: '2016年',
            verified: true
          },
          {
            type: 'certificate',
            title: '婚姻家庭治疗师认证',
            organization: 'AAMFT',
            date: '2018年',
            verified: true
          },
          {
            type: 'certificate',
            title: 'CBT认知行为治疗培训',
            organization: '中国认知行为治疗联盟',
            date: '2017年',
            verified: false
          }
        ],
        pricing: [
          {
            serviceType: '个人咨询',
            duration: 50,
            price: 500
          },
          {
            serviceType: '婚姻咨询',
            duration: 80,
            price: 800
          },
          {
            serviceType: '家庭咨询',
            duration: 90,
            price: 1000
          },
          {
            serviceType: '短时干预',
            duration: 30,
            price: 300
          }
        ]
      }
    }
  },
  methods: {
    changeAvatar() {
      uni.showActionSheet({
        itemList: ['拍照', '从相册选择'],
        success: (res) => {
          if (res.tapIndex === 0) {
            // 拍照
            this.takePhoto();
          } else if (res.tapIndex === 1) {
            // 从相册选择
            this.chooseFromAlbum();
          }
        }
      });
    },
    takePhoto() {
      // 调用相机API
      uni.showToast({
        title: '此功能暂未实现',
        icon: 'none'
      });
    },
    chooseFromAlbum() {
      // 调用相册选择API
      uni.showToast({
        title: '此功能暂未实现',
        icon: 'none'
      });
    },
    editSection(section) {
      uni.navigateTo({
        url: `/pages/counselor/edit/${section}`
      });
    },
    getQualificationIcon(type) {
      const iconMap = {
        'degree': 'icon-degree',
        'certificate': 'icon-certificate',
        'license': 'icon-license',
        'training': 'icon-training'
      };
      return iconMap[type] || 'icon-certificate';
    },
    navigateTo(url) {
      uni.navigateTo({
        url
      });
    },
    previewPublicProfile() {
      uni.navigateTo({
        url: `/pages/counselor/detail/index?id=self&preview=true`
      });
    },
    logout() {
      uni.showModal({
        title: '确认退出',
        content: '您确定要退出登录吗？',
        success: (res) => {
          if (res.confirm) {
            // 执行退出逻辑
            uni.clearStorageSync();
            uni.reLaunch({
              url: '/pages/login/index'
            });
          }
        }
      });
    }
  }
}
</script>

<style lang="scss">
@import "@/static/theme.scss";

.profile-container {
  padding: 30rpx;
  background-color: #f9f9f9;
  min-height: 100vh;
}

.profile-header {
  background: linear-gradient(135deg, #FFFFFF 0%, #F9EFD6 100%) !important;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 6rpx;
    background: linear-gradient(90deg, #E2AA59 0%, #F1C88B 100%);
  }
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 30rpx;
}

.avatar-container {
  position: relative;
  margin-right: 30rpx;
}

.avatar {
  width: 150rpx;
  height: 150rpx;
  border-radius: 75rpx;
  border: 3rpx solid var(--mg-primary-light);
}

.edit-avatar {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 50rpx;
  height: 50rpx;
  background-color: var(--mg-primary);
  border-radius: 25rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
}

.edit-icon {
  width: 24rpx;
  height: 24rpx;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>');
  background-repeat: no-repeat;
  background-size: contain;
}

.basic-info {
  flex: 1;
}

.name-container {
  display: flex;
  align-items: center;
  margin-bottom: 8rpx;
}

.name {
  font-size: 36rpx;
  font-weight: 600;
  color: var(--mg-text-primary);
  margin-right: 16rpx;
}

.verified-badge {
  background-color: var(--mg-primary);
  color: white;
  font-size: 22rpx;
  padding: 4rpx 12rpx;
  border-radius: 20rpx;
}

.title {
  font-size: 28rpx;
  color: var(--mg-text-secondary);
  margin-bottom: 16rpx;
}

.specialties {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.specialty-tag {
  font-size: 24rpx;
  color: var(--mg-primary-dark);
  background-color: var(--mg-bg-gold-light);
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  padding-top: 20rpx;
  border-top: 1px solid var(--mg-border-light);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 36rpx;
  font-weight: 600;
  color: var(--mg-primary);
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: var(--mg-text-tertiary);
}

.section {
  position: relative;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.profile-bio {
  background: linear-gradient(135deg, #FFFFFF 0%, #F9EFD6 100%) !important;
}

.qualifications {
  background: linear-gradient(135deg, #FFFFFF 0%, #EAF7EA 100%) !important;
  
  &::after {
    content: '';
    position: absolute;
    right: 0;
    bottom: 0;
    width: 120rpx;
    height: 120rpx;
    background-image: radial-gradient(circle at bottom right, rgba(76, 175, 80, 0.15) 0%, transparent 70%);
    z-index: 0;
  }
}

.pricing {
  background: linear-gradient(135deg, #FFFFFF 0%, #E7F3FE 100%) !important;
  
  &::after {
    content: '';
    position: absolute;
    right: 0;
    bottom: 0;
    width: 120rpx;
    height: 120rpx;
    background-image: radial-gradient(circle at bottom right, rgba(33, 150, 243, 0.15) 0%, transparent 70%);
    z-index: 0;
  }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 500;
  color: var(--mg-text-primary);
  position: relative;
  padding-left: 20rpx;
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 8rpx;
    height: 32rpx;
    background-color: var(--mg-primary);
    border-radius: 4rpx;
  }
}

.edit-button {
  font-size: 26rpx;
  color: var(--mg-primary);
  padding: 8rpx 16rpx;
  border-radius: 6rpx;
  
  &:active {
    background-color: var(--mg-bg-gold-light);
  }
}

.section-content {
  color: var(--mg-text-secondary);
  font-size: 28rpx;
  line-height: 1.6;
}

.bio-content {
  text-indent: 2em;
}

.qualification-item {
  display: flex;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1px solid var(--mg-border-light);
  
  &:last-child {
    border-bottom: none;
  }
}

.qualification-icon {
  width: 60rpx;
  height: 60rpx;
  margin-right: 20rpx;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-degree {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23E2AA59"><path d="M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82zM12 3L1 9l11 6 9-4.91V17h2V9L12 3z"/></svg>');
}

.icon-certificate {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23E2AA59"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-7 9h-2V5h2v6zm0 4h-2v-2h2v2z"/></svg>');
}

.icon-license {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23E2AA59"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>');
}

.icon-training {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23E2AA59"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>');
}

.qualification-details {
  flex: 1;
}

.qualification-title {
  font-size: 28rpx;
  color: var(--mg-text-primary);
  font-weight: 500;
  display: block;
}

.qualification-org {
  font-size: 26rpx;
  color: var(--mg-text-secondary);
  display: block;
  margin: 4rpx 0;
}

.qualification-date {
  font-size: 24rpx;
  color: var(--mg-text-tertiary);
  display: block;
}

.verification-status {
  font-size: 24rpx;
  padding: 4rpx 12rpx;
  border-radius: 20rpx;
  background-color: var(--mg-gray-200);
  color: var(--mg-text-tertiary);
  
  &.verified {
    background-color: var(--mg-success-light);
    color: var(--mg-success);
  }
}

.pricing-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1px solid var(--mg-border-light);
  
  &:last-child {
    border-bottom: none;
  }
}

.service-type {
  font-size: 28rpx;
  color: var(--mg-text-primary);
  font-weight: 500;
  flex: 1;
}

.service-duration {
  font-size: 26rpx;
  color: var(--mg-text-tertiary);
  margin-right: 30rpx;
}

.service-price {
  font-size: 30rpx;
  font-weight: 600;
  color: var(--mg-primary);
}

.settings-section {
  background: linear-gradient(135deg, #FFFFFF 0%, #F9EFD6 100%) !important;
  border-radius: 16rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
  overflow: hidden;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    right: 0;
    bottom: 0;
    width: 150rpx;
    height: 150rpx;
    background-image: radial-gradient(circle at bottom right, rgba(226, 170, 89, 0.15) 0%, transparent 70%);
    z-index: 0;
  }
}

.setting-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1px solid #E9E9E9;
  position: relative;
  z-index: 1;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:active {
    background-color: rgba(226, 170, 89, 0.15);
  }
}

.setting-icon {
  width: 40rpx;
  height: 40rpx;
  margin-right: 20rpx;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.personal {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23666666"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>');
}

.account {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23666666"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>');
}

.payment {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23666666"><path d="M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z"/></svg>');
}

.notification {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23666666"><path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/></svg>');
}

.privacy {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23666666"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>');
}

.setting-text {
  flex: 1;
  font-size: 28rpx;
  color: var(--mg-text-primary);
}

.arrow-icon {
  width: 16rpx;
  height: 28rpx;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23CCCCCC"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/></svg>');
  background-repeat: no-repeat;
  background-size: contain;
}

.bottom-buttons {
  display: flex;
  gap: 20rpx;
  margin-top: 40rpx;
  margin-bottom: 60rpx;
}

.preview-button, .logout-button {
  flex: 1;
  height: 90rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30rpx;
  border-radius: 45rpx;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.preview-button {
  background: linear-gradient(to right, #F1C88B, #E2AA59);
  color: white;
  border: none;
  
  &:active {
    opacity: 0.9;
    transform: translateY(2rpx);
  }
}

.logout-button {
  background-color: white;
  color: #D19845;
  border: 2rpx solid #E2AA59;
  
  &:active {
    background-color: rgba(226, 170, 89, 0.1);
    transform: translateY(2rpx);
  }
}

@media screen and (max-width: 375px) {
  .profile-container {
    padding: 20rpx;
  }
  
  .name {
    font-size: 32rpx;
  }
  
  .title {
    font-size: 24rpx;
  }
  
  .specialty-tag {
    font-size: 22rpx;
  }
  
  .section-title {
    font-size: 28rpx;
  }
  
  .section-content {
    font-size: 26rpx;
  }
}
</style> 