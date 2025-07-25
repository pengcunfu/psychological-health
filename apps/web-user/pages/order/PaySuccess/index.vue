<template>
  <view class="pay-success-page">
    <!-- 成功提示区域 -->
    <view class="success-header">
      <view class="success-icon">
        <view class="icon-circle">
          <text class="iconfont">&#xe605;</text>
        </view>
      </view>
      <text class="success-title">支付成功</text>
      <text class="success-subtitle">咨询预约已确认</text>
    </view>
    
    <!-- 订单信息区域 -->
    <view class="order-info-card">
      <view class="card-title">订单信息</view>
      
      <view class="info-item">
        <text class="info-label">订单编号</text>
        <text class="info-value">{{ orderInfo.orderNo }}</text>
      </view>
      
      <view class="info-item">
        <text class="info-label">支付方式</text>
        <text class="info-value">{{ orderInfo.paymentMethod }}</text>
      </view>
      
      <view class="info-item">
        <text class="info-label">支付金额</text>
        <text class="info-value price">¥{{ orderInfo.price.toFixed(2) }}</text>
      </view>
      
      <view class="info-item">
        <text class="info-label">咨询师</text>
        <text class="info-value">{{ orderInfo.counselorName }}</text>
      </view>
      
      <view class="info-item">
        <text class="info-label">咨询时间</text>
        <text class="info-value">{{ orderInfo.appointmentTime }}</text>
      </view>
    </view>
    
    <!-- 提醒区域 -->
    <view class="reminder-card">
      <view class="reminder-header">
        <text class="iconfont">&#xe60c;</text>
        <text class="reminder-title">提醒</text>
      </view>
      
      <text class="reminder-content">
        咨询开始前15分钟，我们会发送提醒消息，请确保在咨询开始前做好准备，保持网络畅通。
      </text>
    </view>
    
    <!-- 咨询须知 -->
    <view class="notice-section">
      <text class="section-title">咨询须知</text>
      
      <view class="notice-list">
        <view class="notice-item">
          <text class="dot"></text>
          <text class="notice-text">咨询开始前24小时内取消，将收取50%的咨询费用作为违约金</text>
        </view>
        
        <view class="notice-item">
          <text class="dot"></text>
          <text class="notice-text">如需调整咨询时间，请至少提前24小时与咨询师联系</text>
        </view>
        
        <view class="notice-item">
          <text class="dot"></text>
          <text class="notice-text">咨询过程中请保持网络稳定，确保有良好的咨询体验</text>
        </view>
        
        <view class="notice-item">
          <text class="dot"></text>
          <text class="notice-text">如有任何问题，可随时联系客服获取帮助</text>
        </view>
      </view>
    </view>
    
    <!-- 底部按钮 -->
    <view class="button-group">
      <button class="btn btn-outline" @click="viewOrder">查看订单</button>
      <button class="btn btn-primary" @click="goHome">返回首页</button>
    </view>
  </view>
</template>

<script setup>
import { reactive } from 'vue';

// 订单信息
const orderInfo = reactive({
  orderNo: '202310159374559',
  paymentMethod: '微信支付',
  price: 900,
  counselorName: '李瑞峰',
  appointmentTime: '2023-10-18 14:00-14:50'
});

// 查看订单
const viewOrder = () => {
  uni.navigateTo({
    url: '/pages/order/index'
  });
};

// 返回首页
const goHome = () => {
  uni.switchTab({
    url: '/pages/index/index'
  });
};
</script>

<style lang="scss" scoped>
@import '@/static/theme.scss';

.pay-success-page {
  min-height: 100vh;
  background-color: $mg-bg-secondary;
  padding-bottom: 120rpx;
}

// 成功提示区域
.success-header {
  background-color: $mg-primary;
  padding: 60rpx 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .success-icon {
    margin-bottom: 30rpx;
    
    .icon-circle {
      width: 120rpx;
      height: 120rpx;
      background-color: $mg-white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      
      .iconfont {
        color: $mg-primary;
        font-size: 70rpx;
        font-weight: bold;
      }
    }
  }
  
  .success-title {
    font-size: 40rpx;
    color: $mg-white;
    font-weight: 500;
    margin-bottom: 10rpx;
  }
  
  .success-subtitle {
    font-size: 28rpx;
    color: $mg-white;
    opacity: 0.9;
  }
}

// 订单信息卡片
.order-info-card {
  margin: 30rpx;
  background-color: $mg-white;
  border-radius: 12rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 12rpx $mg-shadow-color;
  
  .card-title {
    font-size: 32rpx;
    font-weight: 500;
    color: $mg-text-primary;
    margin-bottom: 24rpx;
  }
  
  .info-item {
    display: flex;
    justify-content: space-between;
    padding: 16rpx 0;
    border-bottom: 1px solid $mg-border-light;
    
    &:last-child {
      border-bottom: none;
    }
    
    .info-label {
      font-size: 28rpx;
      color: $mg-text-secondary;
    }
    
    .info-value {
      font-size: 28rpx;
      color: $mg-text-primary;
      
      &.price {
        color: $mg-accent;
        font-weight: 500;
      }
    }
  }
}

// 提醒卡片
.reminder-card {
  margin: 0 30rpx 30rpx;
  background-color: rgba($mg-primary, 0.1);
  border-radius: 12rpx;
  padding: 24rpx;
  
  .reminder-header {
    display: flex;
    align-items: center;
    margin-bottom: 16rpx;
    
    .iconfont {
      color: $mg-primary;
      font-size: 32rpx;
      margin-right: 10rpx;
    }
    
    .reminder-title {
      font-size: 30rpx;
      font-weight: 500;
      color: $mg-primary;
    }
  }
  
  .reminder-content {
    font-size: 28rpx;
    color: $mg-text-secondary;
    line-height: 1.5;
  }
}

// 咨询须知
.notice-section {
  margin: 30rpx;
  
  .section-title {
    font-size: 32rpx;
    font-weight: 500;
    color: $mg-text-primary;
    margin-bottom: 24rpx;
  }
  
  .notice-list {
    .notice-item {
      display: flex;
      margin-bottom: 20rpx;
      
      .dot {
        width: 10rpx;
        height: 10rpx;
        background-color: $mg-primary;
        border-radius: 50%;
        margin-top: 16rpx;
        margin-right: 16rpx;
        flex-shrink: 0;
      }
      
      .notice-text {
        font-size: 28rpx;
        color: $mg-text-secondary;
        line-height: 1.5;
      }
    }
  }
}

// 底部按钮
.button-group {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  padding: 30rpx;
  background-color: $mg-white;
  box-shadow: 0 -2rpx 10rpx $mg-shadow-color;
  
  .btn {
    flex: 1;
    height: 88rpx;
    border-radius: 44rpx;
    font-size: 30rpx;
    font-weight: 500;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 16rpx;
    
    &.btn-outline {
      background-color: $mg-white;
      color: $mg-primary;
      border: 1px solid $mg-primary;
    }
    
    &.btn-primary {
      background-color: $mg-primary;
      color: $mg-white;
      border: 1px solid $mg-primary;
    }
  }
}
</style>
