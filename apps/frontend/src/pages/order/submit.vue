<template>
  <view class="container">
    <!-- 自定义导航栏 -->
    <view class="custom-navbar">
      <view class="navbar-content">
        <view class="navbar-left" @click="goBack">
          <up-icon name="arrow-left" size="20" color="#333"></up-icon>
        </view>
        <view class="navbar-title"></view>
        <view class="navbar-right">
          <up-icon name="more-dot-fill" size="20" color="#333"></up-icon>
          <up-icon name="scan" size="20" color="#333" style="margin-left: 15rpx;"></up-icon>
        </view>
      </view>
    </view>

    <!-- 支付倒计时区域 -->
    <view class="payment-header">
      <view class="payment-title">待支付，剩余 <text class="countdown-text">{{ countdownDisplay }}</text></view>
      <view class="payment-subtitle">请您尽快支付，逾期可能会被约走哦</view>
    </view>

    <!-- 主要内容 -->
    <view class="content">
      <!-- 咨询师信息卡片 -->
      <view class="counselor-card">
        <image :src="orderData.counselor?.avatar || '/static/images/default-avatar.png'" class="counselor-avatar" mode="aspectFill" />
        <view class="counselor-info">
          <view class="counselor-name">{{ orderData.counselor?.name || '明翠莲' }}</view>
          <view class="counselor-arrow">
            <up-icon name="arrow-right" size="16" color="#999"></up-icon>
          </view>
        </view>
      </view>

      <!-- 订单详情 -->
      <view class="order-details">
        <view class="detail-section">
          <view class="detail-label">咨询人</view>
          <view class="detail-value">{{ orderData.consultant?.name || '彭存福' }}</view>
        </view>

        <view class="detail-section">
          <view class="detail-value consultation-info">
            {{ getConsultationTypeText() }} · {{ getConsultationMethodText() }} · {{ getConsultantTypeText() }}
          </view>
        </view>

        <view class="detail-section">
          <view class="detail-label">咨询时间</view>
          <view class="detail-value">{{ getConsultationTimeText() }}</view>
        </view>

        <view class="detail-section">
          <view class="detail-label">订单金额</view>
          <view class="detail-value price-text">¥{{ orderData.total_price || 600 }}</view>
        </view>

        <view class="cancellation-policy">
          {{ getCancellationPolicyText() }}
        </view>
      </view>

      <!-- 特别约定 -->
      <view class="special-agreement">
        <view class="agreement-title">特别约定</view>
        <view class="agreement-content">
          <text>我擅长的咨询流派是心理动力学，主要采用谈话咨询，一般一周1-2次。个体咨询我一般和18岁以上的成年人工作，50分钟/次。</text>
        </view>
        
        <view class="agreement-content">
          <text class="content-title">咨询的基本流程：</text>
        </view>
        
        <view class="agreement-content">
          <text class="step-text">1. 初始访谈阶段：所用时间大约是2-4个小节，我会请您谈一下您的生活发生了什么，促使您在这个时候决定咨询，您内心的冲突或遇到的问题是什么，您咨询的目标是什么，跟随着您的脚步，我会适时了解您的生活现状及过往经历的一些人物、事件及环境，这样做是因为要更好地理解您，我需要对您有更多的了解。咨询中我会跟您一起讨论制定我们的咨询计划，包括咨询的设置，如：时间、频率等事项。在这个过程中，您有任</text>
        </view>

        <view class="agreement-checkbox">
          <view class="checkbox-item" @click="toggleAgreement">
            <up-icon 
              :name="agreedToTerms ? 'checkbox-mark' : 'checkbox'" 
              size="16" 
              :color="agreedToTerms ? '#4A90E2' : '#999'"
            ></up-icon>
            <text class="checkbox-text">我同意并签署《心理咨询知情同意书》</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 固定底部支付区域 -->
    <view class="fixed-bottom">
      <view class="more-options" @click="showMoreOptions">
        <up-icon name="more-circle" size="20" color="#666"></up-icon>
        <text class="more-text">更多</text>
      </view>
      <button class="pay-btn" :disabled="!canPay" @click="handlePayment">
        确认支付 ¥{{ orderData.total_price || 600 }}
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

// 页面数据
const orderData = ref({})
const agreedToTerms = ref(false)
const countdown = ref(14 * 60 + 56) // 14分56秒，单位：秒
let countdownTimer = null

// 计算属性
const countdownDisplay = computed(() => {
  const minutes = Math.floor(countdown.value / 60)
  const seconds = countdown.value % 60
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
})

const canPay = computed(() => {
  return agreedToTerms.value && countdown.value > 0
})

// 方法
const goBack = () => {
  uni.navigateBack()
}

const toggleAgreement = () => {
  agreedToTerms.value = !agreedToTerms.value
}

const getConsultationTypeText = () => {
  const typeMap = {
    'individual': '个体咨询',
    'couple': '情侣咨询',
    'family': '家庭咨询'
  }
  return typeMap[orderData.value.consultation_type] || '个体咨询'
}

const getConsultationMethodText = () => {
  const methodMap = {
    'video': '视频咨询(APP)',
    'audio': '语音咨询',
    'offline': '面对面咨询'
  }
  return methodMap[orderData.value.consultation_method] || '视频咨询(APP)'
}

const getConsultantTypeText = () => {
  return '个体咨询(成人)'
}

const getConsultationTimeText = () => {
  // 这里应该根据实际选择的时间槽来显示
  return '2025-08-09(周六) 11:00-11:50'
}

const getCancellationPolicyText = () => {
  return '08-08 中午12点前可免费取消，超时取消将全额扣费'
}

const showMoreOptions = () => {
  uni.showActionSheet({
    itemList: ['查看订单详情', '联系客服', '取消订单'],
    success: (res) => {
      switch (res.tapIndex) {
        case 0:
          // 查看订单详情
          break
        case 1:
          // 联系客服
          break
        case 2:
          // 取消订单
          handleCancelOrder()
          break
      }
    }
  })
}

const handleCancelOrder = () => {
  uni.showModal({
    title: '确认取消',
    content: '确定要取消这个订单吗？',
    success: (res) => {
      if (res.confirm) {
        // 处理取消逻辑
        uni.showToast({
          title: '订单已取消',
          icon: 'success'
        })
        setTimeout(() => {
          uni.navigateBack()
        }, 1500)
      }
    }
  })
}

const handlePayment = () => {
  if (!canPay.value) {
    if (!agreedToTerms.value) {
      uni.showToast({
        title: '请先同意知情同意书',
        icon: 'none'
      })
    } else if (countdown.value <= 0) {
      uni.showToast({
        title: '订单已超时',
        icon: 'none'
      })
    }
    return
  }

  // 调用支付接口
  uni.showModal({
    title: '确认支付',
    content: `确认支付 ¥${orderData.value.total_price || 600}？`,
    success: (res) => {
      if (res.confirm) {
        // 这里应该调用实际的支付接口
        uni.showToast({
          title: '支付成功',
          icon: 'success'
        })
        
        setTimeout(() => {
          uni.redirectTo({
            url: `/pages/order/pay-success?data=${encodeURIComponent(JSON.stringify(orderData.value))}`
          })
        }, 1500)
      }
    }
  })
}

// 倒计时功能
const startCountdown = () => {
  countdownTimer = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value--
    } else {
      clearInterval(countdownTimer)
      uni.showToast({
        title: '订单已超时',
        icon: 'none'
      })
    }
  }, 1000)
}

// 页面加载
onLoad((options) => {
  if (options.data) {
    try {
      orderData.value = JSON.parse(decodeURIComponent(options.data))
    } catch (error) {
      console.error('解析订单数据失败:', error)
    }
  }
})

onMounted(() => {
  startCountdown()
})

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
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
  display: flex;
  align-items: center;
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

.payment-header {
  background: linear-gradient(135deg, #87CEEB, #B0E0E6);
  padding: 40rpx 30rpx;
  text-align: center;
}

.payment-title {
  font-size: 36rpx;
  color: #333;
  margin-bottom: 10rpx;
}

.countdown-text {
  color: #ff4d4f;
  font-weight: bold;
}

.payment-subtitle {
  font-size: 24rpx;
  color: #666;
}

.content {
  padding: 20rpx;
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
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  margin-right: 20rpx;
}

.counselor-info {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.counselor-name {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
}

.order-details {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.detail-section {
  margin-bottom: 20rpx;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 5rpx;
}

.detail-value {
  font-size: 28rpx;
  color: #333;
}

.consultation-info {
  color: #666;
  margin-bottom: 10rpx;
}

.price-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #ff4d4f;
}

.cancellation-policy {
  margin-top: 20rpx;
  padding-top: 20rpx;
  border-top: 1rpx solid #f0f0f0;
  font-size: 24rpx;
  color: #999;
}

.special-agreement {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.agreement-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 20rpx;
}

.agreement-content {
  margin-bottom: 15rpx;
  line-height: 1.6;
}

.content-title {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

.step-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
}

.agreement-checkbox {
  margin-top: 30rpx;
  padding-top: 20rpx;
  border-top: 1rpx solid #f0f0f0;
}

.checkbox-item {
  display: flex;
  align-items: center;
}

.checkbox-text {
  font-size: 28rpx;
  color: #333;
  margin-left: 10rpx;
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
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
  z-index: 100;
  border-top: 1rpx solid #f0f0f0;
}

.more-options {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.more-text {
  font-size: 24rpx;
  color: #666;
  margin-top: 5rpx;
}

.pay-btn {
  background: linear-gradient(135deg, #4A90E2, #1890ff);
  color: #fff;
  font-size: 30rpx;
  font-weight: 600;
  padding: 0;
  border-radius: 40rpx;
  border: none;
  width: 280rpx;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 16rpx rgba(74, 144, 226, 0.4);
}

.pay-btn:disabled {
  background: linear-gradient(135deg, #d9d9d9, #f0f0f0);
  color: #999;
  box-shadow: none;
}
</style>
