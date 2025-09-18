<template>
  <view class="container">
    <view class="content">
      <view class="title">咨询预约协议书</view>
      
      <view class="section">
        <view class="section-title">一、咨询服务内容</view>
        <view class="section-content">
          <text>1. 本平台提供专业的心理咨询服务，包括但不限于情感咨询、职业发展咨询、人际关系咨询、心理健康评估等。</text>
          <text>2. 咨询师将根据您的具体情况，采用专业的心理咨询技术和方法，为您提供个性化的咨询服务。</text>
          <text>3. 咨询过程中，咨询师将严格遵守职业道德规范，保护您的隐私和权益。</text>
        </view>
      </view>

      <view class="section">
        <view class="section-title">二、咨询预约规则</view>
        <view class="section-content">
          <text>1. 请提前至少24小时预约咨询时间，如需取消或更改预约，请提前12小时通知。</text>
          <text>2. 迟到超过15分钟将视为自动取消本次咨询，咨询费用不予退还。</text>
          <text>3. 如因咨询师原因需要调整时间，我们将提前通知您并协商调整。</text>
          <text>4. 每次咨询时长为50分钟，如需延长请提前告知咨询师。</text>
        </view>
      </view>

      <view class="section">
        <view class="section-title">三、保密协议</view>
        <view class="section-content">
          <text>1. 咨询师对您在咨询过程中透露的所有信息严格保密。</text>
          <text>2. 除非您书面同意或法律要求，咨询师不会向任何第三方透露您的信息。</text>
          <text>3. 咨询记录将安全保存，仅用于咨询服务的持续性和专业性提升。</text>
          <text>4. 平台采用先进的数据加密技术保护您的个人信息安全。</text>
        </view>
      </view>

      <view class="section">
        <view class="section-title">四、权利与义务</view>
        <view class="section-content">
          <view class="subsection">
            <text class="subsection-title">您的权利：</text>
            <text>• 有权了解咨询师的专业资质和咨询方法</text>
            <text>• 有权随时终止咨询关系</text>
            <text>• 有权要求咨询师对咨询过程保密</text>
            <text>• 有权对咨询服务提出意见和建议</text>
          </view>
          <view class="subsection">
            <text class="subsection-title">您的义务：</text>
            <text>• 如实提供个人信息和相关情况</text>
            <text>• 按时参加预约的咨询</text>
            <text>• 配合咨询师的专业建议和安排</text>
            <text>• 按约定支付咨询费用</text>
          </view>
        </view>
      </view>

      <view class="section">
        <view class="section-title">五、费用说明</view>
        <view class="section-content">
          <text>1. 咨询费用按次收取，具体价格请参考平台公示价格。</text>
          <text>2. 如需取消预约，请提前12小时通知，否则将收取50%的咨询费用。</text>
          <text>3. 因不可抗力因素导致无法进行咨询，双方可协商调整时间或退费。</text>
          <text>4. 平台支持多种支付方式，支付成功后即确认预约。</text>
        </view>
      </view>

      <view class="section">
        <view class="section-title">六、特别提醒</view>
        <view class="section-content">
          <text>1. 心理咨询不能替代医疗治疗，如有严重心理疾病请及时就医。</text>
          <text>2. 咨询效果因人而异，需要一定时间和过程，请保持耐心。</text>
          <text>3. 如在咨询过程中出现危机情况，咨询师有权采取必要的干预措施。</text>
          <text>4. 未成年人咨询需监护人同意并可能需要监护人参与。</text>
        </view>
      </view>

      <view class="section">
        <view class="section-title">七、争议解决</view>
        <view class="section-content">
          <text>1. 如对咨询服务有异议，可通过平台客服进行投诉和反馈。</text>
          <text>2. 双方应本着诚信、友好的原则协商解决争议。</text>
          <text>3. 如协商不成，可向相关行业协会或司法机关寻求解决。</text>
        </view>
      </view>

      <view class="footer">
        <view class="footer-text">本协议自您确认同意之日起生效</view>
        <view class="footer-text">如有疑问，请联系客服：400-XXX-XXXX</view>
        <view class="update-time">最后更新时间：{{ updateTime }}</view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

// 更新时间
const updateTime = ref('2024年1月15日')

// 页面加载
onLoad(() => {
  uni.setNavigationBarTitle({
    title: '咨询预约协议书'
  })
})
</script>

<style lang="scss" scoped>
// SCSS 变量定义
$primary-color: #007AFF;
$white: #FFFFFF;
$text-primary: #1C1C1E;
$text-secondary: #48484A;
$text-tertiary: #8E8E93;
$bg-primary: #FFFFFF;
$bg-secondary: #F2F2F7;
$border-color: #E5E5EA;

.container {
  min-height: 100vh;
  background-color: $bg-secondary;
  padding: 20rpx;
}

.content {
  background-color: $white;
  border-radius: 16rpx;
  padding: 40rpx;
  box-shadow: 0 2rpx 20rpx rgba(0, 0, 0, 0.05);
}

.title {
  font-size: 40rpx;
  font-weight: bold;
  color: $text-primary;
  text-align: center;
  margin-bottom: 40rpx;
  padding-bottom: 20rpx;
  border-bottom: 2rpx solid $primary-color;
}

.section {
  margin-bottom: 40rpx;
  
  &:last-child {
    margin-bottom: 0;
  }

  .section-title {
    font-size: 32rpx;
    font-weight: 600;
    color: $text-primary;
    margin-bottom: 20rpx;
    padding-left: 20rpx;
    position: relative;

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 50%;
      transform: translateY(-50%);
      width: 6rpx;
      height: 24rpx;
      background-color: $primary-color;
      border-radius: 3rpx;
    }
  }

  .section-content {
    padding-left: 20rpx;
    line-height: 1.8;

    text {
      display: block;
      font-size: 28rpx;
      color: $text-secondary;
      margin-bottom: 16rpx;

      &:last-child {
        margin-bottom: 0;
      }
    }

    .subsection {
      margin-bottom: 24rpx;

      &:last-child {
        margin-bottom: 0;
      }

      .subsection-title {
        font-size: 30rpx;
        font-weight: 600;
        color: $text-primary;
        margin-bottom: 12rpx !important;
      }

      text:not(.subsection-title) {
        padding-left: 20rpx;
        position: relative;

        &::before {
          content: '';
          position: absolute;
          left: 8rpx;
          top: 50%;
          transform: translateY(-50%);
          width: 4rpx;
          height: 4rpx;
          background-color: $primary-color;
          border-radius: 50%;
        }
      }
    }
  }
}

.footer {
  margin-top: 60rpx;
  padding-top: 30rpx;
  border-top: 1rpx solid $border-color;
  text-align: center;

  .footer-text {
    font-size: 26rpx;
    color: $text-tertiary;
    margin-bottom: 12rpx;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .update-time {
    font-size: 24rpx;
    color: $text-tertiary;
    margin-top: 20rpx;
    font-style: italic;
  }
}
</style>
