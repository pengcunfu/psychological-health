<template>
  <view class="container">
    <view class="header-section">
      <image class="banner-image" src="/static/images/become-counselor-banner.png" mode="aspectFill"></image>
      <view class="header-content">
        <text class="header-title">成为咨询师</text>
        <text class="header-subtitle">加入我们的专业团队，帮助更多需要心理支持的人</text>
      </view>
    </view>

    <view class="info-section">
      <view class="section-title">申请条件</view>
      <view class="requirement-list">
        <view class="requirement-item">
          <up-icon name="checkmark-circle" color="#4A90E2" size="40"></up-icon>
          <text class="requirement-text">持有心理咨询师资格证书或相关专业资质</text>
        </view>
        <view class="requirement-item">
          <up-icon name="checkmark-circle" color="#4A90E2" size="40"></up-icon>
          <text class="requirement-text">具有2年以上心理咨询工作经验</text>
        </view>
        <view class="requirement-item">
          <up-icon name="checkmark-circle" color="#4A90E2" size="40"></up-icon>
          <text class="requirement-text">良好的沟通能力和职业道德</text>
        </view>
        <view class="requirement-item">
          <up-icon name="checkmark-circle" color="#4A90E2" size="40"></up-icon>
          <text class="requirement-text">能够提供稳定的在线咨询服务</text>
        </view>
      </view>
    </view>

    <view class="info-section">
      <view class="section-title">申请流程</view>
      <view class="process-list">
        <view class="process-item">
          <view class="process-step">1</view>
          <view class="process-content">
            <text class="process-title">提交申请</text>
            <text class="process-desc">填写基本信息和专业资质</text>
          </view>
        </view>
        <view class="process-item">
          <view class="process-step">2</view>
          <view class="process-content">
            <text class="process-title">资质审核</text>
            <text class="process-desc">平台审核您提交的资质证明</text>
          </view>
        </view>
        <view class="process-item">
          <view class="process-step">3</view>
          <view class="process-content">
            <text class="process-title">在线面试</text>
            <text class="process-desc">与平台专业团队进行在线面谈</text>
          </view>
        </view>
        <view class="process-item">
          <view class="process-step">4</view>
          <view class="process-content">
            <text class="process-title">平台培训</text>
            <text class="process-desc">了解平台规则和操作流程</text>
          </view>
        </view>
        <view class="process-item">
          <view class="process-step">5</view>
          <view class="process-content">
            <text class="process-title">正式入驻</text>
            <text class="process-desc">开始在平台提供咨询服务</text>
          </view>
        </view>
      </view>
    </view>

    <view class="info-section">
      <view class="section-title">平台优势</view>
      <view class="advantage-list">
        <view class="advantage-item">
          <up-icon name="star" color="#faad14" size="40"></up-icon>
          <text class="advantage-title">广阔的客户资源</text>
          <text class="advantage-desc">平台拥有大量潜在客户，帮助您快速建立咨询业务</text>
        </view>
        <view class="advantage-item">
          <up-icon name="calendar" color="#52c41a" size="40"></up-icon>
          <text class="advantage-title">灵活的工作时间</text>
          <text class="advantage-desc">自由设置咨询时段，兼顾工作与生活平衡</text>
        </view>
        <view class="advantage-item">
          <up-icon name="rmb-circle" color="#f5222d" size="40"></up-icon>
          <text class="advantage-title">有竞争力的收入</text>
          <text class="advantage-desc">根据专业能力和服务质量获得合理回报</text>
        </view>
        <view class="advantage-item">
          <up-icon name="arrow-upward" color="#4A90E2" size="40"></up-icon>
          <text class="advantage-title">专业成长空间</text>
          <text class="advantage-desc">定期培训和案例研讨，提升专业能力</text>
        </view>
      </view>
    </view>

    <view class="agreement-section">
      <view class="agreement-check">
        <u-checkbox v-model="agreed" shape="circle" activeColor="#4A90E2"></u-checkbox>
        <text class="agreement-text">我已阅读并同意<text class="link-text" @click="navigateToAgreement">《咨询师服务协议》</text></text>
      </view>
    </view>

    <button class="submit-btn" :disabled="!agreed" @click="handleSubmit">立即申请</button>
  </view>
</template>

<script>
import { ref } from 'vue'
import { checkLogin } from '@/utils/auth'

export default {
  setup() {
    // 检查登录状态
    if (!checkLogin()) return {}
    
    const agreed = ref(false)
    
    // 跳转到协议页
    const navigateToAgreement = () => {
      uni.navigateTo({
        url: '/pages/profile/agreement?type=counselor'
      })
    }
    
    // 提交申请
    const handleSubmit = () => {
      if (!agreed.value) {
        uni.showToast({
          title: '请先同意咨询师服务协议',
          icon: 'none'
        })
        return
      }
      
      uni.navigateTo({
        url: '/pages/counselor/apply/index'
      })
    }
    
    return {
      agreed,
      navigateToAgreement,
      handleSubmit
    }
  }
}
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 50rpx;
}

.header-section {
  position: relative;
  height: 400rpx;
}

.banner-image {
  width: 100%;
  height: 400rpx;
  position: absolute;
  top: 0;
  left: 0;
}

.header-content {
  position: absolute;
  bottom: 40rpx;
  left: 40rpx;
  right: 40rpx;
  z-index: 1;
}

.header-title {
  font-size: 48rpx;
  font-weight: bold;
  color: #fff;
  display: block;
  margin-bottom: 20rpx;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.3);
}

.header-subtitle {
  font-size: 28rpx;
  color: #fff;
  display: block;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.3);
}

.info-section {
  background-color: #fff;
  margin: 20rpx 30rpx;
  padding: 30rpx;
  border-radius: 20rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
  position: relative;
  padding-left: 20rpx;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 6rpx;
  height: 30rpx;
  background-color: #4A90E2;
}

.requirement-list {
  margin-bottom: 20rpx;
}

.requirement-item {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.requirement-text {
  font-size: 28rpx;
  color: #333;
  margin-left: 20rpx;
  flex: 1;
}

.process-list {
  margin-bottom: 20rpx;
}

.process-item {
  display: flex;
  margin-bottom: 30rpx;
}

.process-step {
  width: 60rpx;
  height: 60rpx;
  background-color: #4A90E2;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  font-weight: bold;
}

.process-content {
  margin-left: 20rpx;
  flex: 1;
}

.process-title {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
  display: block;
  margin-bottom: 10rpx;
}

.process-desc {
  font-size: 24rpx;
  color: #666;
}

.advantage-list {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -10rpx;
}

.advantage-item {
  width: calc(50% - 20rpx);
  margin: 10rpx;
  background-color: #f9f9f9;
  border-radius: 10rpx;
  padding: 20rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.advantage-title {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
  margin: 20rpx 0 10rpx;
}

.advantage-desc {
  font-size: 24rpx;
  color: #666;
  line-height: 1.5;
}

.agreement-section {
  padding: 30rpx;
}

.agreement-check {
  display: flex;
  align-items: center;
}

.agreement-text {
  font-size: 28rpx;
  color: #666;
  margin-left: 10rpx;
}

.link-text {
  color: #4A90E2;
}

.submit-btn {
  width: 90%;
  height: 90rpx;
  background-color: #4A90E2;
  color: white;
  border: none;
  border-radius: 10rpx;
  font-size: 32rpx;
  font-weight: bold;
  margin: 0 auto;
}

.submit-btn[disabled] {
  background-color: #ccc;
}
</style> 