<template>
  <view class="container">
    <Navbar 
      title="支付失败" 
      :show-left="false" 
      :show-right="true" 
      right-icon="home" 
      @right-click="goHome" 
    />

    <!-- 失败状态区域 -->
    <view class="error-header">
      <view class="error-icon">
        <up-icon name="close-circle-fill" size="80" color="#ff4d4f"></up-icon>
      </view>
      <view class="error-title">支付失败</view>
      <view class="error-subtitle">很抱歉，您的支付未能成功</view>
      <view class="error-reason">{{ errorReason || '网络异常，请稍后重试' }}</view>
    </view>

    <!-- 主要内容 -->
    <view class="content">
      <!-- 订单信息卡片 -->
      <view class="order-card">
        <view class="order-title">订单信息</view>
        <view class="order-details">
          <view class="detail-row">
            <view class="detail-label">订单号</view>
            <view class="detail-value">{{ orderInfo.order_no || 'PY202508091100001' }}</view>
          </view>
          <view class="detail-row">
            <view class="detail-label">咨询师</view>
            <view class="detail-value">{{ orderInfo.counselor?.name || '明翠莲' }}</view>
          </view>
          <view class="detail-row">
            <view class="detail-label">咨询时间</view>
            <view class="detail-value">{{ getConsultationTime() }}</view>
          </view>
          <view class="detail-row">
            <view class="detail-label">支付金额</view>
            <view class="detail-value price-text">¥{{ orderInfo.total_price || 600 }}</view>
          </view>
        </view>
      </view>

      <!-- 解决方案 -->
      <view class="solution-card">
        <view class="solution-title">解决方案</view>
        <view class="solution-list">
          <view class="solution-item">
            <up-icon name="checkmark-circle" size="16" color="#52c41a"></up-icon>
            <text class="solution-text">检查网络连接是否正常</text>
          </view>
          <view class="solution-item">
            <up-icon name="checkmark-circle" size="16" color="#52c41a"></up-icon>
            <text class="solution-text">确认银行卡余额是否充足</text>
          </view>
          <view class="solution-item">
            <up-icon name="checkmark-circle" size="16" color="#52c41a"></up-icon>
            <text class="solution-text">联系银行确认是否限制交易</text>
          </view>
          <view class="solution-item">
            <up-icon name="checkmark-circle" size="16" color="#52c41a"></up-icon>
            <text class="solution-text">尝试使用其他支付方式</text>
          </view>
        </view>
      </view>

      <!-- 联系客服 -->
      <view class="contact-card">
        <view class="contact-title">需要帮助？</view>
        <view class="contact-content">
          <text>如果问题仍未解决，请联系我们的客服团队，我们将竭诚为您服务。</text>
        </view>
        <view class="contact-info">
          <view class="contact-item" @click="callService">
            <up-icon name="phone" size="16" color="#4A90E2"></up-icon>
            <text class="contact-text">400-123-4567</text>
          </view>
          <view class="contact-item" @click="chatService">
            <up-icon name="chat" size="16" color="#4A90E2"></up-icon>
            <text class="contact-text">在线客服</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 固定底部操作区域 -->
    <view class="fixed-bottom">
      <button class="action-btn secondary-btn" @click="viewOrderDetail">
        查看订单
      </button>
      <button class="action-btn primary-btn" @click="retryPayment">
        重新支付
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import Navbar from '@/components/Navbar.vue'

// 页面数据
const orderInfo = ref({})
const errorReason = ref('')

// 获取咨询时间
const getConsultationTime = () => {
  return '2025年8月9日(周六) 11:00-11:50'
}

// 返回首页
const goHome = () => {
  uni.reLaunch({
    url: '/pages/index'
  })
}

// 重新支付
const retryPayment = () => {
  uni.navigateBack()
}

// 查看订单详情
const viewOrderDetail = () => {
  uni.navigateTo({
    url: '/pages/profile/my-appointment'
  })
}

// 拨打客服电话
const callService = () => {
  uni.makePhoneCall({
    phoneNumber: '400-123-4567'
  })
}

// 在线客服
const chatService = () => {
  uni.showToast({
    title: '客服功能开发中',
    icon: 'none'
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
  
  if (options.reason) {
    errorReason.value = decodeURIComponent(options.reason)
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
  padding-top: 88rpx; /* 为Navbar留出空间 */
  padding-bottom: 120rpx;
}

.error-header {
  background-color: #fff;
  padding: 60rpx 30rpx 40rpx;
  text-align: center;
  margin-bottom: 20rpx;
}

.error-icon {
  margin-bottom: 20rpx;
}

.error-title {
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.error-subtitle {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 20rpx;
}

.error-reason {
  font-size: 24rpx;
  color: #ff4d4f;
  background-color: #fff2f0;
  padding: 10rpx 20rpx;
  border-radius: 20rpx;
  display: inline-block;
}

.content {
  padding: 0 20rpx;
}

.order-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.order-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 25rpx;
}

.order-details {
  // 样式继承自pay-success.vue
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

.price-text {
  color: #ff4d4f;
  font-weight: bold;
  font-size: 32rpx;
}

.solution-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.solution-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 20rpx;
}

.solution-list {
  line-height: 1.6;
}

.solution-item {
  display: flex;
  align-items: center;
  margin-bottom: 15rpx;
}

.solution-item:last-child {
  margin-bottom: 0;
}

.solution-text {
  font-size: 26rpx;
  color: #666;
  margin-left: 10rpx;
}

.contact-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.contact-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 15rpx;
}

.contact-content {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20rpx;
}

.contact-info {
  display: flex;
  gap: 30rpx;
}

.contact-item {
  display: flex;
  align-items: center;
  padding: 15rpx 20rpx;
  background-color: #f0f7ff;
  border-radius: 8rpx;
  flex: 1;
  justify-content: center;
}

.contact-text {
  font-size: 24rpx;
  color: #4A90E2;
  margin-left: 8rpx;
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
