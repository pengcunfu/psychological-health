<template>
  <view class="container">
    <!-- 自定义导航栏 -->
    <view class="custom-navbar">
      <view class="navbar-content">
        <view class="navbar-left">
          <!-- 空白区域，不显示返回按钮 -->
        </view>
        <view class="navbar-title">支付成功</view>
        <view class="navbar-right">
          <up-icon name="home" size="20" color="#333" @click="goHome"></up-icon>
        </view>
      </view>
    </view>

    <!-- 成功状态区域 -->
    <view class="success-header">
      <view class="success-icon">
        <up-icon name="checkmark-circle-fill" size="80" color="#52c41a"></up-icon>
      </view>
      <view class="success-title">支付成功</view>
      <view class="success-subtitle">您的咨询预约已确认</view>
      <view class="order-number">订单号：{{ orderInfo.order_no || 'PY202508091100001' }}</view>
    </view>

    <!-- 主要内容 -->
    <view class="content">
      <!-- 咨询师信息卡片 -->
      <view class="counselor-card">
        <image 
          :src="orderInfo.counselor?.avatar || '/static/images/default-avatar.png'" 
          class="counselor-avatar" 
          mode="aspectFill" 
        />
        <view class="counselor-info">
          <view class="counselor-name">{{ orderInfo.counselor?.name || '明翠莲' }}</view>
          <view class="counselor-title">心理咨询师</view>
        </view>
        <view class="contact-btn" @click="contactCounselor">
          <up-icon name="chat" size="16" color="#4A90E2"></up-icon>
          <text class="contact-text">联系</text>
        </view>
      </view>

      <!-- 预约详情 -->
      <view class="appointment-details">
        <view class="details-title">预约详情</view>
        
        <view class="detail-row">
          <view class="detail-label">咨询人</view>
          <view class="detail-value">{{ orderInfo.consultant?.name || '彭存福' }}</view>
        </view>
        
        <view class="detail-row">
          <view class="detail-label">咨询类型</view>
          <view class="detail-value">{{ getConsultationInfo() }}</view>
        </view>
        
        <view class="detail-row">
          <view class="detail-label">咨询时间</view>
          <view class="detail-value time-highlight">{{ getConsultationTime() }}</view>
        </view>
        
        <view class="detail-row">
          <view class="detail-label">支付金额</view>
          <view class="detail-value price-highlight">¥{{ orderInfo.total_price || 600 }}</view>
        </view>
      </view>

      <!-- 温馨提示 -->
      <view class="tips-card">
        <view class="tips-title">
          <up-icon name="info-circle" size="16" color="#1890ff"></up-icon>
          <text class="tips-title-text">温馨提示</text>
        </view>
        <view class="tips-content">
          <view class="tip-item">• 请提前5-10分钟准备好咨询环境</view>
          <view class="tip-item">• 确保网络连接稳定，建议使用WiFi</view>
          <view class="tip-item">• 如需取消或改期，请提前24小时联系咨询师</view>
          <view class="tip-item">• 咨询过程中请保持专注，避免外界干扰</view>
        </view>
      </view>

      <!-- 咨询准备 -->
      <view class="preparation-card">
        <view class="preparation-title">咨询前准备</view>
        <view class="preparation-content">
          <text>建议您在咨询前思考以下问题，这将有助于提高咨询效果：</text>
        </view>
        <view class="preparation-list">
          <view class="preparation-item">1. 您希望通过咨询解决什么问题？</view>
          <view class="preparation-item">2. 这个问题对您的生活造成了什么影响？</view>
          <view class="preparation-item">3. 您对咨询有什么期待？</view>
          <view class="preparation-item">4. 您是否有其他想要分享的情况？</view>
        </view>
      </view>
    </view>

    <!-- 固定底部操作区域 -->
    <view class="fixed-bottom">
      <button class="action-btn secondary-btn" @click="viewMyAppointments">
        我的预约
      </button>
      <button class="action-btn primary-btn" @click="addToCalendar">
        添加到日历
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

// 页面数据
const orderInfo = ref({})

// 获取咨询信息
const getConsultationInfo = () => {
  const typeMap = {
    'individual': '个体咨询',
    'couple': '情侣咨询',
    'family': '家庭咨询'
  }
  
  const methodMap = {
    'video': '视频咨询',
    'audio': '语音咨询',
    'offline': '面对面咨询'
  }
  
  const type = typeMap[orderInfo.value.consultation_type] || '个体咨询'
  const method = methodMap[orderInfo.value.consultation_method] || '视频咨询'
  
  return `${type} · ${method}`
}

// 获取咨询时间
const getConsultationTime = () => {
  // 这里应该根据实际预约时间返回
  return '2025年8月9日(周六) 11:00-11:50'
}

// 返回首页
const goHome = () => {
  uni.reLaunch({
    url: '/pages/index'
  })
}

// 联系咨询师
const contactCounselor = () => {
  uni.showActionSheet({
    itemList: ['发送消息', '拨打电话'],
    success: (res) => {
      if (res.tapIndex === 0) {
        // 发送消息
        uni.navigateTo({
          url: `/pages/chat/index?counselor_id=${orderInfo.value.counselor_id}`
        })
      } else if (res.tapIndex === 1) {
        // 拨打电话
        const phone = orderInfo.value.counselor?.phone || '400-123-4567'
        uni.makePhoneCall({
          phoneNumber: phone
        })
      }
    }
  })
}

// 查看我的预约
const viewMyAppointments = () => {
  uni.navigateTo({
    url: '/pages/appointment'
  })
}

// 添加到日历
const addToCalendar = () => {
  // 在真实应用中，这里可以调用系统日历API
  uni.showToast({
    title: '已添加到日历提醒',
    icon: 'success'
  })
}

// 页面加载
onLoad((options) => {
  if (options.data) {
    try {
      orderInfo.value = JSON.parse(decodeURIComponent(options.data))
    } catch (error) {
      console.error('解析订单数据失败:', error)
    }
  }
})

onMounted(() => {
  // 页面加载完成后的处理
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 120rpx;
}

.custom-navbar {
  background-color: #fff;
  padding-top: var(--status-bar-height);
  border-bottom: 1rpx solid #f0f0f0;
}

.navbar-content {
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30rpx;
}

.navbar-left {
  width: 80rpx;
}

.navbar-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  text-align: center;
}

.navbar-right {
  width: 80rpx;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.success-header {
  background-color: #fff;
  padding: 60rpx 30rpx 40rpx;
  text-align: center;
  margin-bottom: 20rpx;
}

.success-icon {
  margin-bottom: 20rpx;
}

.success-title {
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.success-subtitle {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 20rpx;
}

.order-number {
  font-size: 24rpx;
  color: #999;
}

.content {
  padding: 0 20rpx;
}

.counselor-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
}

.counselor-avatar {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  margin-right: 20rpx;
}

.counselor-info {
  flex: 1;
}

.counselor-name {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 5rpx;
}

.counselor-title {
  font-size: 24rpx;
  color: #666;
}

.contact-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15rpx;
  background-color: #f0f7ff;
  border-radius: 8rpx;
  min-width: 80rpx;
}

.contact-text {
  font-size: 20rpx;
  color: #4A90E2;
  margin-top: 5rpx;
}

.appointment-details {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.details-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 25rpx;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-size: 28rpx;
  color: #666;
}

.detail-value {
  font-size: 28rpx;
  color: #333;
  text-align: right;
}

.time-highlight {
  color: #4A90E2;
  font-weight: 600;
}

.price-highlight {
  color: #ff4d4f;
  font-weight: bold;
  font-size: 32rpx;
}

.tips-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.tips-title {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.tips-title-text {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-left: 10rpx;
}

.tips-content {
  line-height: 1.6;
}

.tip-item {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 10rpx;
}

.tip-item:last-child {
  margin-bottom: 0;
}

.preparation-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.preparation-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 15rpx;
}

.preparation-content {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20rpx;
}

.preparation-list {
  line-height: 1.8;
}

.preparation-item {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 10rpx;
}

.preparation-item:last-child {
  margin-bottom: 0;
}

.fixed-bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #fff;
  padding: 25rpx 30rpx;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 20rpx;
  box-sizing: border-box;
  z-index: 100;
  border-top: 1rpx solid #f0f0f0;
}

.action-btn {
  flex: 1;
  height: 80rpx;
  border-radius: 40rpx;
  font-size: 30rpx;
  font-weight: 600;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

.primary-btn {
  background: linear-gradient(135deg, #4A90E2, #1890ff);
  color: #fff;
  box-shadow: 0 4rpx 16rpx rgba(74, 144, 226, 0.4);
}

.secondary-btn {
  background-color: #f5f5f5;
  color: #666;
  border: 1rpx solid #d9d9d9;
}

.secondary-btn:active {
  background-color: #e8e8e8;
}

.primary-btn:active {
  background: linear-gradient(135deg, #357abd, #0e7ce8);
}
</style>
