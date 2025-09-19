<template>
  <view class="container">
    <!-- 加载状态 -->
    <view class="loading-state" v-if="loading">
      <u-loading-icon mode="spinner"></u-loading-icon>
      <text class="loading-text">加载中...</text>
    </view>

    <!-- 订单详情内容 -->
    <view v-else-if="orderDetail">
      <!-- 订单状态卡片 -->
      <view class="status-card">
        <view class="status-icon">
          <view class="icon-wrapper" :class="`status-${orderDetail.status}`">
            <u-icon :name="getStatusIcon(orderDetail.status)" size="32" color="#fff"></u-icon>
          </view>
        </view>
        <view class="status-info">
          <text class="status-text">{{ getStatusText(orderDetail.status) }}</text>
          <text class="status-desc">{{ getStatusDesc(orderDetail.status) }}</text>
        </view>
      </view>

      <!-- 订单信息 -->
      <view class="info-section">
        <view class="section-title">订单信息</view>
        <view class="info-item">
          <text class="info-label">订单号</text>
          <text class="info-value">{{ orderDetail.order_number }}</text>
        </view>
        <view class="info-item">
          <text class="info-label">下单时间</text>
          <text class="info-value">{{ formatFullTime(orderDetail.created_at) }}</text>
        </view>
        <view class="info-item" v-if="orderDetail.paid_at">
          <text class="info-label">支付时间</text>
          <text class="info-value">{{ formatFullTime(orderDetail.paid_at) }}</text>
        </view>
        <view class="info-item">
          <text class="info-label">订单金额</text>
          <text class="info-value amount">¥{{ orderDetail.amount }}</text>
        </view>
      </view>

      <!-- 服务信息 -->
      <view class="info-section">
        <view class="section-title">服务信息</view>
        <view class="service-card">
          <view class="service-content">
            <view class="service-title">{{ orderDetail.service_name }}</view>
            <view class="service-details">
              <view class="service-item" v-if="orderDetail.counselor_name">
                <text class="service-label">咨询师：</text>
                <text class="service-value">{{ orderDetail.counselor_name }}</text>
              </view>
              <view class="service-item" v-if="orderDetail.appointment_time">
                <text class="service-label">预约时间：</text>
                <text class="service-value">{{ formatDateTime(orderDetail.appointment_time) }}</text>
              </view>
              <view class="service-item" v-if="orderDetail.duration">
                <text class="service-label">咨询时长：</text>
                <text class="service-value">{{ orderDetail.duration }}分钟</text>
              </view>
              <view class="service-item" v-if="orderDetail.consultation_type">
                <text class="service-label">咨询类型：</text>
                <text class="service-value">{{ orderDetail.consultation_type }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 咨询人信息 -->
      <view class="info-section" v-if="orderDetail.consultant_info">
        <view class="section-title">咨询人信息</view>
        <view class="consultant-card">
          <view class="consultant-info">
            <text class="consultant-name">{{ orderDetail.consultant_info.name }}</text>
            <text class="consultant-details">{{ orderDetail.consultant_info.gender }} · {{ orderDetail.consultant_info.age }}岁</text>
          </view>
          <view class="consultant-phone">{{ formatPhone(orderDetail.consultant_info.phone) }}</view>
        </view>
      </view>

      <!-- 订单进度 -->
      <view class="info-section" v-if="orderTimeline.length > 0">
        <view class="section-title">订单进度</view>
        <view class="timeline">
          <view 
            v-for="(item, index) in orderTimeline" 
            :key="index"
            class="timeline-item"
            :class="{ active: item.active }"
          >
            <view class="timeline-dot">
              <view class="dot-inner"></view>
            </view>
            <view class="timeline-content">
              <text class="timeline-title">{{ item.title }}</text>
              <text class="timeline-time" v-if="item.time">{{ formatFullTime(item.time) }}</text>
              <text class="timeline-desc" v-if="item.desc">{{ item.desc }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="actions-section" v-if="getOrderActions().length > 0">
        <view 
          v-for="action in getOrderActions()" 
          :key="action.key"
          class="action-btn"
          :class="action.type"
          @click="handleAction(action.key)"
        >
          {{ action.label }}
        </view>
      </view>
    </view>

    <!-- 错误状态 -->
    <view class="error-state" v-else>
      <view class="error-icon">❌</view>
      <text class="error-text">订单信息加载失败</text>
      <view class="error-btn" @click="loadOrderDetail">
        <text>重新加载</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

// 响应式数据
const orderId = ref('')
const orderDetail = ref(null)
const loading = ref(false)

// 订单状态映射
const statusMap = {
  'pending': '待付款',
  'paid': '已付款',
  'processing': '处理中',
  'completed': '已完成',
  'cancelled': '已取消',
  'refunded': '已退款'
}

// 订单状态描述
const statusDescMap = {
  'pending': '请在30分钟内完成支付',
  'paid': '订单已支付，等待咨询师确认',
  'processing': '咨询师已确认，请按时参加咨询',
  'completed': '咨询已完成，感谢您的信任',
  'cancelled': '订单已取消',
  'refunded': '订单已退款'
}

// 模拟订单详情数据
const mockOrderDetail = {
  id: 1,
  order_number: 'ORD202401150001',
  status: 'completed',
  amount: 299.00,
  service_name: '心理咨询服务',
  counselor_name: '张医生',
  appointment_time: '2024-01-20 14:00:00',
  duration: 50,
  consultation_type: '个人咨询',
  created_at: '2024-01-15 10:30:00',
  paid_at: '2024-01-15 10:35:00',
  consultant_info: {
    name: '张三',
    gender: '男',
    age: 28,
    phone: '13800138000'
  }
}

// 订单时间轴
const orderTimeline = computed(() => {
  if (!orderDetail.value) return []
  
  const timeline = [
    {
      title: '订单创建',
      time: orderDetail.value.created_at,
      desc: '订单创建成功',
      active: true
    }
  ]
  
  if (orderDetail.value.paid_at) {
    timeline.push({
      title: '支付完成',
      time: orderDetail.value.paid_at,
      desc: '订单支付成功',
      active: true
    })
  }
  
  if (orderDetail.value.status === 'paid' || orderDetail.value.status === 'processing' || orderDetail.value.status === 'completed') {
    timeline.push({
      title: '咨询师确认',
      time: orderDetail.value.confirmed_at || orderDetail.value.paid_at,
      desc: '咨询师已确认预约',
      active: true
    })
  }
  
  if (orderDetail.value.status === 'completed') {
    timeline.push({
      title: '咨询完成',
      time: orderDetail.value.completed_at || orderDetail.value.appointment_time,
      desc: '心理咨询已完成',
      active: true
    })
  }
  
  if (orderDetail.value.status === 'cancelled') {
    timeline.push({
      title: '订单取消',
      time: orderDetail.value.cancelled_at,
      desc: '订单已取消',
      active: true
    })
  }
  
  return timeline
})

// 方法
const getStatusText = (status) => {
  return statusMap[status] || status
}

const getStatusDesc = (status) => {
  return statusDescMap[status] || ''
}

const getStatusIcon = (status) => {
  const iconMap = {
    'pending': 'clock',
    'paid': 'checkmark',
    'processing': 'refresh',
    'completed': 'checkmark-circle',
    'cancelled': 'close',
    'refunded': 'arrow-left'
  }
  return iconMap[status] || 'info'
}

const formatFullTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

const formatDateTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

const formatPhone = (phone) => {
  if (!phone) return ''
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

const getOrderActions = () => {
  if (!orderDetail.value) return []
  
  const actions = []
  
  switch (orderDetail.value.status) {
    case 'pending':
      actions.push(
        { key: 'pay', label: '立即付款', type: 'primary' },
        { key: 'cancel', label: '取消订单', type: 'default' }
      )
      break
    case 'paid':
    case 'processing':
      actions.push(
        { key: 'contact', label: '联系咨询师', type: 'primary' },
        { key: 'reschedule', label: '改期', type: 'default' }
      )
      break
    case 'completed':
      actions.push(
        { key: 'evaluate', label: '评价咨询师', type: 'primary' },
        { key: 'rebuy', label: '再次预约', type: 'default' }
      )
      break
    case 'cancelled':
      actions.push(
        { key: 'rebuy', label: '重新下单', type: 'primary' }
      )
      break
  }
  
  return actions
}

// 加载订单详情
const loadOrderDetail = async () => {
  try {
    loading.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 这里应该调用真实的API
    orderDetail.value = mockOrderDetail
    
  } catch (error) {
    console.error('获取订单详情失败:', error)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 处理操作
const handleAction = (actionKey) => {
  switch (actionKey) {
    case 'pay':
      uni.navigateTo({
        url: `/pages/order/pay?id=${orderId.value}`
      })
      break
    case 'cancel':
      uni.showModal({
        title: '取消订单',
        content: '确定要取消这个订单吗？取消后无法恢复。',
        success: (res) => {
          if (res.confirm) {
            // 处理取消订单逻辑
            uni.showToast({
              title: '订单已取消',
              icon: 'success'
            })
            // 重新加载订单详情
            loadOrderDetail()
          }
        }
      })
      break
    case 'contact':
      uni.showToast({
        title: '联系功能开发中',
        icon: 'none'
      })
      break
    case 'reschedule':
      uni.showToast({
        title: '改期功能开发中',
        icon: 'none'
      })
      break
    case 'evaluate':
      uni.showToast({
        title: '评价功能开发中',
        icon: 'none'
      })
      break
    case 'rebuy':
      uni.switchTab({
        url: '/pages/counselor/index'
      })
      break
  }
}

// 生命周期
onLoad((options) => {
  if (options.id) {
    orderId.value = options.id
    loadOrderDetail()
  } else {
    uni.showToast({
      title: '订单ID缺失',
      icon: 'none'
    })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  }
})
</script>

<style lang="scss" scoped>
// SCSS 变量
$primary-color: #007AFF;
$success-color: #52C41A;
$warning-color: #FA8C16;
$danger-color: #FF3B30;
$text-primary: #1C1C1E;
$text-secondary: #48484A;
$text-tertiary: #8E8E93;
$bg-primary: #FFFFFF;
$bg-secondary: #F2F2F7;
$border-color: #E5E5EA;

.container {
  min-height: 100vh;
  background-color: $bg-secondary;
  padding-bottom: 40rpx;
}

// 状态卡片
.status-card {
  background-color: $bg-primary;
  margin: 20rpx;
  border-radius: 16rpx;
  padding: 40rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);

  .status-icon {
    margin-right: 30rpx;

    .icon-wrapper {
      width: 80rpx;
      height: 80rpx;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;

      &.status-pending {
        background-color: $warning-color;
      }

      &.status-paid {
        background-color: $primary-color;
      }

      &.status-processing {
        background-color: $primary-color;
      }

      &.status-completed {
        background-color: $success-color;
      }

      &.status-cancelled {
        background-color: $text-tertiary;
      }
    }
  }

  .status-info {
    flex: 1;

    .status-text {
      display: block;
      font-size: 32rpx;
      font-weight: 600;
      color: $text-primary;
      margin-bottom: 8rpx;
    }

    .status-desc {
      font-size: 26rpx;
      color: $text-secondary;
    }
  }
}

// 信息区域
.info-section {
  background-color: $bg-primary;
  margin: 20rpx;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);

  .section-title {
    padding: 30rpx 30rpx 20rpx;
    font-size: 30rpx;
    font-weight: 600;
    color: $text-primary;
    border-bottom: 1rpx solid $border-color;
  }

  .info-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24rpx 30rpx;
    border-bottom: 1rpx solid $border-color;

    &:last-child {
      border-bottom: none;
    }

    .info-label {
      font-size: 28rpx;
      color: $text-secondary;
    }

    .info-value {
      font-size: 28rpx;
      color: $text-primary;

      &.amount {
        font-weight: 600;
        color: $danger-color;
      }
    }
  }
}

// 服务卡片
.service-card {
  padding: 30rpx;

  .service-content {
    .service-title {
      font-size: 30rpx;
      font-weight: 600;
      color: $text-primary;
      margin-bottom: 20rpx;
    }

    .service-details {
      .service-item {
        display: flex;
        align-items: center;
        margin-bottom: 12rpx;

        &:last-child {
          margin-bottom: 0;
        }

        .service-label {
          font-size: 26rpx;
          color: $text-secondary;
          width: 140rpx;
          flex-shrink: 0;
        }

        .service-value {
          font-size: 26rpx;
          color: $text-primary;
          flex: 1;
        }
      }
    }
  }
}

// 咨询人卡片
.consultant-card {
  padding: 30rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;

  .consultant-info {
    flex: 1;

    .consultant-name {
      display: block;
      font-size: 28rpx;
      font-weight: 600;
      color: $text-primary;
      margin-bottom: 8rpx;
    }

    .consultant-details {
      font-size: 24rpx;
      color: $text-secondary;
    }
  }

  .consultant-phone {
    font-size: 26rpx;
    color: $text-secondary;
  }
}

// 时间轴
.timeline {
  padding: 20rpx 30rpx 30rpx;

  .timeline-item {
    display: flex;
    align-items: flex-start;
    position: relative;
    padding-bottom: 40rpx;

    &:last-child {
      padding-bottom: 0;

      &::after {
        display: none;
      }
    }

    &::after {
      content: '';
      position: absolute;
      left: 23rpx;
      top: 48rpx;
      width: 2rpx;
      height: calc(100% - 24rpx);
      background-color: $border-color;
    }

    &.active {
      .timeline-dot .dot-inner {
        background-color: $primary-color;
      }

      &::after {
        background-color: $primary-color;
      }
    }

    .timeline-dot {
      width: 48rpx;
      height: 48rpx;
      border-radius: 50%;
      background-color: $bg-secondary;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 20rpx;
      flex-shrink: 0;
      position: relative;
      z-index: 1;

      .dot-inner {
        width: 20rpx;
        height: 20rpx;
        border-radius: 50%;
        background-color: $border-color;
        transition: all 0.2s ease;
      }
    }

    .timeline-content {
      flex: 1;
      padding-top: 4rpx;

      .timeline-title {
        display: block;
        font-size: 28rpx;
        font-weight: 500;
        color: $text-primary;
        margin-bottom: 8rpx;
      }

      .timeline-time {
        display: block;
        font-size: 24rpx;
        color: $text-tertiary;
        margin-bottom: 4rpx;
      }

      .timeline-desc {
        font-size: 24rpx;
        color: $text-secondary;
      }
    }
  }
}

// 操作区域
.actions-section {
  display: flex;
  gap: 20rpx;
  padding: 40rpx 20rpx;

  .action-btn {
    flex: 1;
    text-align: center;
    padding: 24rpx;
    border-radius: 12rpx;
    font-size: 28rpx;
    font-weight: 500;
    transition: all 0.2s ease;

    &.default {
      color: $text-secondary;
      background-color: $bg-primary;
      border: 1rpx solid $border-color;

      &:active {
        background-color: $bg-secondary;
      }
    }

    &.primary {
      color: $bg-primary;
      background: linear-gradient(135deg, $primary-color 0%, #5856D6 100%);
      box-shadow: 0 4rpx 12rpx rgba(0, 122, 255, 0.3);

      &:active {
        transform: scale(0.98);
      }
    }
  }
}

// 加载状态
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120rpx 40rpx;

  .loading-text {
    font-size: 28rpx;
    color: $text-tertiary;
    margin-top: 20rpx;
  }
}

// 错误状态
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120rpx 40rpx;

  .error-icon {
    font-size: 120rpx;
    margin-bottom: 40rpx;
    opacity: 0.3;
  }

  .error-text {
    font-size: 28rpx;
    color: $text-tertiary;
    margin-bottom: 40rpx;
  }

  .error-btn {
    background: linear-gradient(135deg, $primary-color 0%, #5856D6 100%);
    color: #FFFFFF;
    padding: 20rpx 40rpx;
    border-radius: 25rpx;
    font-size: 28rpx;
    font-weight: 500;

    &:active {
      transform: scale(0.95);
    }
  }
}
</style>
