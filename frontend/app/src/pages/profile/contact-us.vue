<template>
  <view class="container">
    <!-- 导航栏 -->
    <!-- <Navbar title="联系我们" /> -->
    
    <view class="header-section">
      <image class="banner-image" src="/static/images/contact-us-banner.png" mode="aspectFill"></image>
      <view class="header-content">
        <text class="header-title">联系我们</text>
        <text class="header-subtitle">我们随时为您提供帮助和支持</text>
      </view>
    </view>

    <view class="contact-section">
      <view class="contact-card">
        <view class="contact-item">
          <up-icon name="phone" color="#4A90E2" size="40"></up-icon>
          <view class="contact-info">
            <text class="contact-title">客服热线</text>
            <text class="contact-value">400-123-4567</text>
            <text class="contact-desc">周一至周日 9:00-21:00</text>
          </view>
        </view>
      </view>

      <view class="contact-card">
        <view class="contact-item">
          <up-icon name="email" color="#4A90E2" size="40"></up-icon>
          <view class="contact-info">
            <text class="contact-title">电子邮箱</text>
            <text class="contact-value">support@psychhealth.com</text>
            <text class="contact-desc">我们会在1-2个工作日内回复</text>
          </view>
        </view>
      </view>

      <view class="contact-card">
        <view class="contact-item">
          <up-icon name="weixin-fill" color="#4A90E2" size="40"></up-icon>
          <view class="contact-info">
            <text class="contact-title">微信公众号</text>
            <text class="contact-value">心理健康平台</text>
            <text class="contact-desc">关注获取更多心理健康资讯</text>
          </view>
        </view>
      </view>

      <view class="contact-card">
        <view class="contact-item">
          <up-icon name="home" color="#4A90E2" size="40"></up-icon>
          <view class="contact-info">
            <text class="contact-title">公司地址</text>
            <text class="contact-value">北京市海淀区中关村南大街5号</text>
            <text class="contact-desc">邮编: 100081</text>
          </view>
        </view>
      </view>
    </view>

    <view class="form-section">
      <view class="section-title">在线留言</view>
      <view class="form-content">
        <view class="form-item">
          <text class="form-label">姓名</text>
          <up--input
            v-model="form.name"
            placeholder="请输入您的姓名"
            border="bottom"
          ></up--input>
        </view>
        
        <view class="form-item">
          <text class="form-label">联系方式</text>
          <up--input
            v-model="form.contact"
            placeholder="请输入您的手机号或邮箱"
            border="bottom"
          ></up--input>
        </view>
        
        <view class="form-item">
          <text class="form-label">留言内容</text>
          <up--textarea
            v-model="form.content"
            placeholder="请输入您的留言内容"
            height="200"
            count
            maxlength="500"
          ></up--textarea>
        </view>
        
        <button class="submit-btn" @click="handleSubmit">提交留言</button>
      </view>
    </view>

    <view class="faq-section">
      <view class="section-title">常见问题</view>
      <view class="faq-list">
        <view class="faq-item" v-for="(item, index) in faqList" :key="index" @click="toggleFaq(index)">
          <view class="faq-question">
            <text>{{ item.question }}</text>
            <up-icon :name="item.expanded ? 'arrow-up' : 'arrow-down'" color="#999" size="30"></up-icon>
          </view>
          <view class="faq-answer" v-if="item.expanded">
            <text>{{ item.answer }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { ref, reactive } from 'vue'
import Navbar from '@/components/Navbar.vue' // 导入 Navbar 组件

export default {
  components: { // 注册 Navbar 组件
    Navbar
  },
  setup() {
    const form = reactive({
      name: '',
      contact: '',
      content: ''
    })
    
    const faqList = ref([
      {
        question: '如何预约咨询师？',
        answer: '您可以在"咨询"页面浏览咨询师列表，选择心仪的咨询师后，点击"立即预约"按钮，选择合适的时间段完成预约。',
        expanded: false
      },
      {
        question: '如何支付咨询费用？',
        answer: '平台支持微信支付、支付宝等多种支付方式，您可以在下单时选择适合您的支付方式进行支付。',
        expanded: false
      },
      {
        question: '如何取消预约？',
        answer: '您可以在"我的"-"我的预约"中找到需要取消的预约，点击"取消预约"按钮，按照提示操作即可。请注意，距离预约时间24小时内取消可能会产生部分费用。',
        expanded: false
      },
      {
        question: '忘记密码怎么办？',
        answer: '您可以在登录页面点击"忘记密码"，通过手机验证码或邮箱验证的方式重置密码。',
        expanded: false
      },
      {
        question: '如何成为平台咨询师？',
        answer: '您可以在"我的"-"成为咨询师"页面查看申请条件和流程，按照要求提交相关资质和信息，通过审核后即可成为平台咨询师。',
        expanded: false
      }
    ])
    
    // 展开/收起FAQ
    const toggleFaq = (index) => {
      faqList.value[index].expanded = !faqList.value[index].expanded
    }
    
    // 提交留言
    const handleSubmit = () => {
      // 表单验证
      if (!form.name) {
        uni.showToast({
          title: '请输入您的姓名',
          icon: 'none'
        })
        return
      }
      
      if (!form.contact) {
        uni.showToast({
          title: '请输入您的联系方式',
          icon: 'none'
        })
        return
      }
      
      if (!form.content) {
        uni.showToast({
          title: '请输入留言内容',
          icon: 'none'
        })
        return
      }
      
      // 提交留言
      uni.showLoading({
        title: '提交中...'
      })
      
      setTimeout(() => {
        uni.hideLoading()
        
        uni.showToast({
          title: '留言提交成功',
          icon: 'success'
        })
        
        // 清空表单
        form.name = ''
        form.contact = ''
        form.content = ''
      }, 1500)
    }
    
    return {
      form,
      faqList,
      toggleFaq,
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
  padding-top: 0; /* 移除顶部padding，让NavBar组件自己处理占位 */
}

.header-section {
  position: relative;
  height: 300rpx;
  margin-top: 0; /* 确保header紧贴NavBar占位区域 */
}

.banner-image {
  width: 100%;
  height: 300rpx;
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
  margin-bottom: 10rpx;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.3);
}

.header-subtitle {
  font-size: 28rpx;
  color: #fff;
  display: block;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.3);
}

.contact-section {
  padding: 30rpx;
}

.contact-card {
  background-color: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.contact-item {
  display: flex;
  align-items: center;
}

.contact-info {
  margin-left: 30rpx;
  flex: 1;
}

.contact-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 10rpx;
}

.contact-value {
  font-size: 32rpx;
  color: #4A90E2;
  display: block;
  margin-bottom: 10rpx;
}

.contact-desc {
  font-size: 24rpx;
  color: #999;
}

.form-section, .faq-section {
  background-color: #fff;
  margin: 0 30rpx 30rpx;
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

.form-content {
  margin-bottom: 20rpx;
}

.form-item {
  margin-bottom: 30rpx;
}

.form-label {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.submit-btn {
  width: 100%;
  height: 90rpx;
  background-color: #4A90E2;
  color: white;
  border: none;
  border-radius: 10rpx;
  font-size: 32rpx;
  font-weight: bold;
  margin-top: 20rpx;
}

.faq-list {
  margin-bottom: 20rpx;
}

.faq-item {
  margin-bottom: 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
  padding-bottom: 20rpx;
}

.faq-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  padding: 10rpx 0;
}

.faq-answer {
  font-size: 28rpx;
  color: #666;
  padding: 20rpx 0;
  line-height: 1.6;
}
</style> 