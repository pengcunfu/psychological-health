<template>
  <view class="container">
    <!-- <Navbar
      title="帮助中心"
      :showLeft="true"
      :showRight="false"
      @leftClick="goBack"
    /> -->
    
    <!-- 搜索框 -->
    <view class="search-box">
      <view class="search-input">
        <SvgIcon name="search" :size="32" color="#999" class="search-icon" />
        <input 
          v-model="searchKeyword" 
          type="text" 
          placeholder="搜索问题"
          @input="handleSearch"
          class="search-text"
        />
      </view>
    </view>
    
    <!-- 常见问题分类 -->
    <view class="help-section">
      <view class="help-header">常见问题分类</view>
      
      <view class="help-item" @click="showToast('账号问题页面开发中')">
        <SvgIcon name="account" path="profile" class="help-icon" :size="32" color="#4A90E2" />
        <view class="help-content">
          <view class="help-title">账号问题</view>
          <view class="help-desc">注册、登录、找回密码等</view>
        </view>
        <SvgIcon name="arrow-right" :size="32" color="#ccc" />
      </view>
      
      <view class="help-item" @click="showToast('咨询问题页面开发中')">
        <view class="help-icon" style="display: flex; align-items: center; justify-content: center;">
          <text style="font-size: 18px;">💬</text>
        </view>
        <view class="help-content">
          <view class="help-title">咨询问题</view>
          <view class="help-desc">预约、取消、咨询流程等</view>
        </view>
        <SvgIcon name="arrow-right" :size="32" color="#ccc" />
      </view>
      
      <view class="help-item" @click="showToast('课程问题页面开发中')">
        <SvgIcon name="book" path="profile" class="help-icon" :size="32" color="#4A90E2" />
        <view class="help-content">
          <view class="help-title">课程问题</view>
          <view class="help-desc">购买、学习、退款等</view>
        </view>
        <SvgIcon name="arrow-right" :size="32" color="#ccc" />
      </view>
      
      <view class="help-item" @click="showToast('测评问题页面开发中')">
        <SvgIcon name="checkmark-circle" path="profile" class="help-icon" :size="32" color="#4A90E2" />
        <view class="help-content">
          <view class="help-title">测评问题</view>
          <view class="help-desc">测评流程、结果解读等</view>
        </view>
        <SvgIcon name="arrow-right" :size="32" color="#ccc" />
      </view>
      
      <view class="help-item" @click="showToast('支付问题页面开发中')">
        <view class="help-icon" style="display: flex; align-items: center; justify-content: center;">
          <text style="font-size: 18px;">💳</text>
        </view>
        <view class="help-content">
          <view class="help-title">支付问题</view>
          <view class="help-desc">支付方式、发票、退款等</view>
        </view>
        <SvgIcon name="arrow-right" :size="32" color="#ccc" />
      </view>
    </view>
    
    <!-- 热门问题 -->
    <view class="help-section">
      <view class="help-header">热门问题</view>
      
      <view class="faq-list">
        <view 
          v-for="(faq, index) in filteredFaqList" 
          :key="index" 
          class="faq-item"
          :class="{ active: faq.isExpanded }"
        >
          <view class="faq-question" @click="toggleFaq(index)">
            <view class="faq-question-text">{{ faq.question }}</view>
            <view class="faq-toggle" :class="{ active: faq.isExpanded }">
              <SvgIcon name="arrow-down" :size="32" color="#999" />
            </view>
          </view>
          <view v-if="faq.isExpanded" class="faq-answer">
            {{ faq.answer }}
          </view>
        </view>
      </view>
    </view>
    
    <!-- 联系我们 -->
    <view class="contact-section">
      <view class="contact-title">联系我们</view>
      <view class="contact-methods">
        <view class="contact-method" @click="makePhoneCall">
          <view class="contact-icon">
            <text style="font-size: 18px; color: #4A90E2;">📞</text>
          </view>
          <view class="contact-text">电话咨询</view>
        </view>
        
        <view class="contact-method" @click="showToast('在线客服功能开发中')">
          <view class="contact-icon">
            <text style="font-size: 18px; color: #4A90E2;">💬</text>
          </view>
          <view class="contact-text">在线客服</view>
        </view>
        
        <view class="contact-method" @click="sendEmail">
          <view class="contact-icon">
            <text style="font-size: 18px; color: #4A90E2;">📧</text>
          </view>
          <view class="contact-text">邮件咨询</view>
        </view>
      </view>
      <view class="contact-time">客服时间：周一至周日 9:00-22:00</view>
    </view>
    
    <!-- 底部空间 -->
    <view style="height: 40rpx;"></view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import SvgIcon from '@/components/SvgIcon.vue'
import Navbar from '@/components/Navbar.vue'

// 搜索关键词
const searchKeyword = ref('')

// FAQ数据
const faqList = ref([
  {
    question: '如何预约心理咨询？',
    answer: '您可以在"咨询预约"页面浏览心理咨询师，选择合适的咨询师后，点击"立即预约"，选择咨询时间和方式（线上/线下），完成支付即可成功预约。预约成功后，您可以在"我的预约"中查看预约详情。',
    isExpanded: true
  },
  {
    question: '如何退款？',
    answer: '未使用的课程和咨询服务可以申请退款。咨询服务需在预约时间24小时前取消才能获得全额退款，课程在购买后7天内且未观看超过20%的内容可申请退款。请在"我的订单"中找到相应订单，点击"申请退款"，填写退款原因后提交申请。退款将在3-5个工作日内退回原支付账户。',
    isExpanded: false
  },
  {
    question: '心理测评结果如何解读？',
    answer: '完成心理测评后，系统会自动生成测评报告，包含分数、等级和相应的解释说明。您可以在"我的测评"页面查看详细报告。如需专业解读，可以预约心理咨询师进行一对一解读服务，帮助您更全面地了解测评结果并提供专业建议。',
    isExpanded: false
  },
  {
    question: '忘记密码怎么办？',
    answer: '在登录页面点击"忘记密码"，输入您注册时使用的手机号或邮箱，系统会发送验证码。输入验证码后，您可以设置新密码。如果您无法收到验证码，请联系客服获取帮助。',
    isExpanded: false
  },
  {
    question: '如何保障隐私安全？',
    answer: '我们高度重视用户隐私保护，采用多重加密技术保护您的个人信息和咨询内容。所有咨询师都签署了保密协议，确保您的咨询内容不会被泄露。您可以在"安全设置"中管理隐私选项，如调整个人资料可见范围、开启登录保护等。',
    isExpanded: false
  }
])

// 过滤后的FAQ列表
const filteredFaqList = computed(() => {
  if (!searchKeyword.value) {
    return faqList.value
  }
  
  return faqList.value.filter(faq => 
    faq.question.includes(searchKeyword.value) || 
    faq.answer.includes(searchKeyword.value)
  )
})

// 返回上一页
const goBack = () => {
  uni.navigateBack()
}

// 显示提示
const showToast = (message) => {
  uni.showToast({
    title: message,
    icon: 'none'
  })
}

// 搜索处理
const handleSearch = (e) => {
  searchKeyword.value = e.detail.value
}

// 切换FAQ展开状态
const toggleFaq = (index) => {
  const actualIndex = faqList.value.findIndex(faq => faq === filteredFaqList.value[index])
  if (actualIndex !== -1) {
    faqList.value[actualIndex].isExpanded = !faqList.value[actualIndex].isExpanded
  }
}

// 拨打电话
const makePhoneCall = () => {
  uni.makePhoneCall({
    phoneNumber: '400-123-4567',
    success: () => {
    },
    fail: () => {
      uni.showToast({
        title: '拨打电话失败',
        icon: 'none'
      })
    }
  })
}

// 发送邮件
const sendEmail = () => {
  // #ifdef H5
  window.location.href = 'mailto:support@example.com'
  // #endif
  
  // #ifdef APP-PLUS || MP
  uni.showToast({
    title: '请发送邮件至：support@example.com',
    icon: 'none',
    duration: 3000
  })
  // #endif
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  color: #333;
}

.search-box {
  background-color: #fff;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.search-input {
  display: flex;
  align-items: center;
  background-color: #f5f7fa;
  border-radius: 40rpx;
  padding: 16rpx 30rpx;
}

.search-icon {
  margin-right: 16rpx;
}

.search-text {
  flex: 1;
  border: none;
  background-color: transparent;
  font-size: 28rpx;
  color: #333;
  outline: none;
}

.search-text::placeholder {
  color: #999;
}

.help-section {
  background-color: #fff;
  margin-bottom: 20rpx;
}

.help-header {
  padding: 30rpx;
  font-size: 28rpx;
  color: #999;
  border-bottom: 1rpx solid #f0f0f0;
}

.help-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
  transition: background-color 0.2s;
}

.help-item:last-child {
  border-bottom: none;
}

.help-item:active {
  background-color: #f8f9fa;
}

.help-icon {
  width: 48rpx;
  height: 48rpx;
  margin-right: 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.help-content {
  flex: 1;
}

.help-title {
  font-size: 32rpx;
  color: #333;
}

.help-desc {
  font-size: 24rpx;
  color: #999;
  margin-top: 8rpx;
}

.faq-list {
  padding: 30rpx;
}

.faq-item {
  margin-bottom: 30rpx;
  background-color: #fff;
  border-radius: 16rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.05);
  overflow: hidden;
}

.faq-question {
  padding: 30rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.faq-question-text {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
  flex: 1;
}

.faq-toggle {
  width: 32rpx;
  height: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s;
}

.faq-toggle.active {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 30rpx 30rpx;
  font-size: 28rpx;
  color: #666;
  border-top: 1rpx solid #f0f0f0;
  line-height: 1.6;
}

.contact-section {
  background-color: #fff;
  margin-bottom: 20rpx;
  padding: 30rpx;
  text-align: center;
}

.contact-title {
  font-size: 32rpx;
  color: #333;
  margin-bottom: 20rpx;
  font-weight: bold;
}

.contact-methods {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30rpx;
}

.contact-method {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.2s;
}

.contact-method:active {
  transform: scale(0.95);
}

.contact-icon {
  width: 80rpx;
  height: 80rpx;
  background-color: #f0f7ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16rpx;
}

.contact-text {
  font-size: 24rpx;
  color: #666;
}

.contact-time {
  font-size: 24rpx;
  color: #999;
}
</style>
