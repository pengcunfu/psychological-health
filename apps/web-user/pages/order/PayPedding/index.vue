<template>
  <view class="pay-pending-page">
    <!-- 价格显示区域 -->
    <view class="price-header">
      <text class="price-amount">¥{{ orderInfo.price.toFixed(2) }}</text>
      <text class="price-description">{{ orderInfo.serviceType }}</text>
      <view class="payment-timeout">
        <text>支付剩余时间</text>
        <text class="timeout-tag">已超时</text>
      </view>
    </view>
    
    <!-- 订单信息区域 -->
    <view class="order-info-card">
      <view class="card-header">
        <text class="card-title">订单信息</text>
        <text class="copy-btn" @click="copyOrderNumber">复制</text>
      </view>
      
      <view class="info-item">
        <text class="info-label">订单编号</text>
        <text class="info-value">{{ orderInfo.orderNumber }}</text>
      </view>
      
      <view class="info-item">
        <text class="info-label">下单时间</text>
        <text class="info-value">{{ orderInfo.orderTime }}</text>
      </view>
      
      <view class="info-item counselor-item">
        <text class="info-label">咨询师头像</text>
        <view class="counselor-info">
          <text class="counselor-name">{{ orderInfo.counselorName }}</text>
          <text class="counselor-title">{{ orderInfo.counselorTitle }}</text>
        </view>
      </view>
      
      <view class="divider"></view>
      
      <view class="service-details">
        <text class="service-title">{{ orderInfo.serviceTitle }}</text>
        <view class="appointment-time">
          <text>预约时间：{{ orderInfo.appointmentTime }}</text>
        </view>
      </view>
    </view>
    
    <!-- 支付方式区域 -->
    <view class="payment-methods">
      <text class="section-title">选择支付方式</text>
      
      <view class="payment-option" @click="selectPayment('wechat')">
        <view class="option-left">
          <image class="payment-icon" src="/static/icons/wechat-pay.png"></image>
          <text class="payment-name">微信支付</text>
        </view>
        <radio class="payment-radio" :color="'#E2AA59'" :checked="paymentMethod === 'wechat'"></radio>
      </view>
      
      <view class="payment-option" @click="selectPayment('alipay')">
        <view class="option-left">
          <image class="payment-icon" src="/static/icons/alipay.png"></image>
          <text class="payment-name">支付宝</text>
        </view>
        <radio class="payment-radio" :color="'#E2AA59'" :checked="paymentMethod === 'alipay'"></radio>
      </view>
    </view>
    
    <!-- 确认支付按钮 -->
    <view class="confirm-btn-container">
      <button class="confirm-btn" @click="confirmPayment">确认支付</button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue';

// 订单信息
const orderInfo = reactive({
  price: 900,
  serviceType: '咨询服务费用',
  orderNumber: '202310159374559',
  orderTime: '2023-10-15 14:35:26',
  counselorName: '李瑞峰',
  counselorTitle: '高级心理咨询师',
  serviceTitle: '一对一心理咨询（50分钟）',
  appointmentTime: '2023-10-18 14:00-14:50'
});

// 支付方式
const paymentMethod = ref('wechat');

// 选择支付方式
const selectPayment = (method) => {
  paymentMethod.value = method;
};

// 复制订单号
const copyOrderNumber = () => {
  uni.setClipboardData({
    data: orderInfo.orderNumber,
    success: () => {
      uni.showToast({
        title: '订单号已复制',
        icon: 'success'
      });
    }
  });
};

// 确认支付
const confirmPayment = () => {
  // 根据所选支付方式调用对应的支付接口
  if (paymentMethod.value === 'wechat') {
    uni.showLoading({
      title: '正在调起微信支付...'
    });
    // 模拟调用微信支付接口
    setTimeout(() => {
      uni.hideLoading();
      // 实际开发中这里会调用真正的支付API
      uni.showModal({
        title: '支付提示',
        content: '微信支付接口调用成功，等待支付结果',
        showCancel: false
      });
      
      uni.navigateTo({
        url: '/pages/order/PaySuccess/index'
      });
    }, 1500);
  } else {
    uni.showLoading({
      title: '正在调起支付宝支付...'
    });
    
    // 模拟调用支付宝支付接口
    setTimeout(() => {
      uni.hideLoading();
      // 实际开发中这里会调用真正的支付API
      uni.showModal({
        title: '支付提示',
        content: '支付宝支付接口调用成功，等待支付结果',
        showCancel: false
      });
    }, 1500);
  }
};
</script>

<style lang="scss" scoped>
@import '@/static/theme.scss';

.pay-pending-page {
  min-height: 100vh;
  background-color: $mg-bg-secondary;
  display: flex;
  flex-direction: column;
}

// 价格显示区域
.price-header {
  background-color: $mg-primary; // 使用主题色主色（暖金色）
  padding: 60rpx 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .price-amount {
    font-size: 72rpx;
    color: $mg-white;
    font-weight: 500;
    margin-bottom: 20rpx;
  }
  
  .price-description {
    font-size: 32rpx;
    color: $mg-white;
    margin-bottom: 30rpx;
  }
  
  .payment-timeout {
    display: flex;
    align-items: center;
    
    text {
      font-size: 28rpx;
      color: $mg-white;
    }
    
    .timeout-tag {
      background-color: rgba(255, 255, 255, 0.2);
      padding: 6rpx 20rpx;
      border-radius: 30rpx;
      margin-left: 16rpx;
      font-size: 24rpx;
    }
  }
}

// 订单信息卡片
.order-info-card {
  margin: 30rpx;
  background-color: $mg-white;
  border-radius: 12rpx;
  padding: 30rpx;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30rpx;
    
    .card-title {
      font-size: 32rpx;
      font-weight: 500;
      color: $mg-text-primary;
    }
    
    .copy-btn {
      font-size: 28rpx;
      color: $mg-primary; // 使用主题色主色（暖金色）
    }
  }
  
  .info-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 24rpx;
    
    .info-label {
      font-size: 28rpx;
      color: $mg-text-secondary;
    }
    
    .info-value {
      font-size: 28rpx;
      color: $mg-text-primary;
    }
  }
  
  .counselor-item {
    .counselor-info {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      
      .counselor-name {
        font-size: 28rpx;
        color: $mg-text-primary;
        margin-bottom: 6rpx;
      }
      
      .counselor-title {
        font-size: 24rpx;
        color: $mg-text-tertiary;
      }
    }
  }
  
  .divider {
    height: 1px;
    background-color: $mg-border-light;
    margin: 20rpx 0;
  }
  
  .service-details {
    .service-title {
      font-size: 30rpx;
      color: $mg-text-primary;
      font-weight: 500;
      margin-bottom: 16rpx;
    }
    
    .appointment-time {
      font-size: 28rpx;
      color: $mg-text-secondary;
    }
  }
}

// 支付方式区域
.payment-methods {
  margin: 0 30rpx 30rpx;
  background-color: $mg-white;
  border-radius: 12rpx;
  padding: 30rpx;
  
  .section-title {
    font-size: 32rpx;
    font-weight: 500;
    color: $mg-text-primary;
    margin-bottom: 30rpx;
  }
  
  .payment-option {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20rpx 0;
    border-bottom: 1px solid $mg-border-light;
    
    &:last-child {
      border-bottom: none;
    }
    
    .option-left {
      display: flex;
      align-items: center;
      
      .payment-icon {
        width: 60rpx;
        height: 60rpx;
        margin-right: 20rpx;
      }
      
      .payment-name {
        font-size: 30rpx;
        color: $mg-text-primary;
      }
    }
    
    .payment-radio {
      transform: scale(0.8);
      color: $mg-primary; // 使用主题色主色（暖金色）
    }
  }
}

// 确认支付按钮
.confirm-btn-container {
  padding: 30rpx;
  margin-top: auto;
  
  .confirm-btn {
    width: 100%;
    height: 90rpx;
    background-color: $mg-primary; // 使用主题色主色（暖金色）
    color: $mg-white;
    border-radius: 45rpx;
    font-size: 32rpx;
    font-weight: 500;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
  }
}
</style>
