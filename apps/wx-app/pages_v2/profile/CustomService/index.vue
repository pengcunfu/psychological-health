<template>
    <view class="contact-us-page">
      <!-- 顶部背景 -->
      <view class="page-header">
        <text class="page-title">联系客服</text>
      </view>
      
      <!-- 联系方式卡片 -->
      <view class="contact-card">
        <view class="card-title-row">
          <view class="dot"></view>
          <text class="card-title">联系方式</text>
        </view>
        
        <view class="contact-methods">
          <view class="contact-item" @click="makePhoneCall">
            <view class="contact-icon">
              <text class="iconfont">&#xe6b9;</text>
            </view>
            <view class="contact-info">
              <text class="contact-label">客服电话</text>
              <text class="contact-value">400-123-4567</text>
            </view>
            <text class="contact-action">拨打</text>
          </view>
          
          <view class="contact-item" @click="copyEmail">
            <view class="contact-icon">
              <text class="iconfont">&#xe69f;</text>
            </view>
            <view class="contact-info">
              <text class="contact-label">电子邮箱</text>
              <text class="contact-value">support@meiguang.com</text>
            </view>
            <text class="contact-action">复制</text>
          </view>
          
          <view class="contact-item" @click="copyWechat">
            <view class="contact-icon">
              <text class="iconfont">&#xe6b3;</text>
            </view>
            <view class="contact-info">
              <text class="contact-label">微信公众号</text>
              <text class="contact-value">美广心理健康</text>
            </view>
            <text class="contact-action">复制</text>
          </view>
        </view>
      </view>
      
      <!-- 客服时间卡片 -->
      <view class="service-hours-card">
        <view class="card-title-row">
          <view class="dot"></view>
          <text class="card-title">客服时间</text>
        </view>
        
        <view class="service-hours">
          <view class="time-item">
            <text class="day">周一至周五</text>
            <text class="hours">9:00 - 18:00</text>
          </view>
          <view class="time-item">
            <text class="day">周六至周日</text>
            <text class="hours">10:00 - 17:00</text>
          </view>
          <view class="time-item">
            <text class="day">节假日</text>
            <text class="hours">10:00 - 16:00</text>
          </view>
        </view>
      </view>
      
      <!-- 在线留言 -->
      <view class="message-card">
        <view class="card-title-row">
          <view class="dot"></view>
          <text class="card-title">在线留言</text>
        </view>
        
        <view class="message-form">
          <view class="form-item">
            <text class="form-label">问题类型</text>
            <view class="select-box" @click="showPicker">
              <text class="select-value">{{ messageForm.type || '请选择问题类型' }}</text>
              <text class="iconfont">&#xe6e1;</text>
            </view>
          </view>
          
          <view class="form-item">
            <text class="form-label">留言内容</text>
            <textarea class="message-textarea" 
              v-model="messageForm.content" 
              placeholder="请详细描述您遇到的问题，以便我们更好地为您解决"
              maxlength="500"
              show-confirm-bar="false"
            ></textarea>
            <text class="word-count">{{ messageForm.content.length }}/500</text>
          </view>
          
          <view class="form-item">
            <text class="form-label">联系方式</text>
            <input class="contact-input" 
              v-model="messageForm.contact" 
              placeholder="请留下您的手机号或微信，方便我们回复您"
            />
          </view>
          
          <button class="submit-btn" @click="submitMessage">提交留言</button>
        </view>
      </view>
      
      <!-- 常见问题 -->
      <view class="faq-card">
        <view class="card-title-row">
          <view class="dot"></view>
          <text class="card-title">常见问题</text>
        </view>
        
        <view class="faq-list">
          <view class="faq-item" v-for="(item, index) in faqs" :key="index" @click="toggleFaq(index)">
            <view class="faq-question">
              <text class="question-text">{{ item.question }}</text>
              <text class="iconfont">{{ item.isOpen ? '&#xe68d;' : '&#xe68e;' }}</text>
            </view>
            <view class="faq-answer" v-if="item.isOpen">
              <text>{{ item.answer }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </template>
  
  <script setup>
  import { ref, reactive } from 'vue';
  
  // 留言表单
  const messageForm = reactive({
    type: '',
    content: '',
    contact: ''
  });
  
  // 问题类型选项
  const problemTypes = [
    '账号问题',
    '支付问题',
    '课程问题',
    '咨询预约问题',
    '其他问题'
  ];
  
  // 常见问题
  const faqs = reactive([
    {
      question: '如何修改预约时间？',
      answer: '您可以在"我的-订单"中找到待咨询的订单，点击"查看详情"，然后选择"修改预约"进行时间调整。请注意，距离咨询开始前24小时内的调整可能会收取一定费用。',
      isOpen: false
    },
    {
      question: '忘记密码怎么办？',
      answer: '您可以在登录页面点击"忘记密码"，通过绑定的手机号接收验证码重置密码。如果您无法收到验证码，请联系客服协助处理。',
      isOpen: false
    },
    {
      question: '如何申请退款？',
      answer: '对于未开始的课程或咨询，您可以在"我的-订单"中找到相应订单，点击"申请退款"并填写退款原因。根据购买时间的不同，退款规则可能有所差异，详情可参考退款政策。',
      isOpen: false
    },
    {
      question: '课程有效期是多久？',
      answer: '大多数课程的有效期为购买后的365天，特殊课程会在课程详情页注明有效期。过期后，您将无法继续观看课程内容，建议在有效期内完成学习。',
      isOpen: false
    }
  ]);
  
  // 展开/折叠FAQ
  const toggleFaq = (index) => {
    faqs[index].isOpen = !faqs[index].isOpen;
  };
  
  // 显示问题类型选择器
  const showPicker = () => {
    uni.showActionSheet({
      itemList: problemTypes,
      success: (res) => {
        messageForm.type = problemTypes[res.tapIndex];
      }
    });
  };
  
  // 拨打电话
  const makePhoneCall = () => {
    uni.makePhoneCall({
      phoneNumber: '4001234567',
      fail: () => {
        uni.showToast({
          title: '拨打失败，请手动拨打400-123-4567',
          icon: 'none'
        });
      }
    });
  };
  
  // 复制邮箱
  const copyEmail = () => {
    uni.setClipboardData({
      data: 'support@meiguang.com',
      success: () => {
        uni.showToast({
          title: '邮箱已复制',
          icon: 'success'
        });
      }
    });
  };
  
  // 复制微信
  const copyWechat = () => {
    uni.setClipboardData({
      data: '美广心理健康',
      success: () => {
        uni.showToast({
          title: '微信公众号已复制',
          icon: 'success'
        });
      }
    });
  };
  
  // 提交留言
  const submitMessage = () => {
    if (!messageForm.type) {
      return uni.showToast({
        title: '请选择问题类型',
        icon: 'none'
      });
    }
    
    if (!messageForm.content.trim()) {
      return uni.showToast({
        title: '请输入留言内容',
        icon: 'none'
      });
    }
    
    if (!messageForm.contact) {
      return uni.showToast({
        title: '请留下您的联系方式',
        icon: 'none'
      });
    }
    
    // 模拟提交
    uni.showLoading({
      title: '提交中'
    });
    
    setTimeout(() => {
      uni.hideLoading();
      uni.showToast({
        title: '留言提交成功',
        icon: 'success'
      });
      
      // 清空表单
      messageForm.type = '';
      messageForm.content = '';
      messageForm.contact = '';
    }, 1500);
  };
  </script>
  
  <style lang="scss" scoped>
  @import '@/static/theme.scss';
  
  .contact-us-page {
    min-height: 100vh;
    background-color: $mg-bg-secondary;
    padding-bottom: 40rpx;
  }
  
  // 页面头部
  .page-header {
    height: 200rpx;
    background-color: $mg-primary;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    
    .page-title {
      font-size: 36rpx;
      color: $mg-white;
      font-weight: 500;
    }
  }
  
  // 卡片通用样式
  .contact-card,
  .service-hours-card,
  .message-card,
  .faq-card {
    margin: 30rpx;
    background-color: $mg-white;
    border-radius: 12rpx;
    padding: 30rpx;
    box-shadow: 0 2rpx 12rpx $mg-shadow-color;
  }
  
  // 卡片标题行
  .card-title-row {
    display: flex;
    align-items: center;
    margin-bottom: 24rpx;
    
    .dot {
      width: 12rpx;
      height: 12rpx;
      background-color: $mg-primary;
      border-radius: 50%;
      margin-right: 12rpx;
    }
    
    .card-title {
      font-size: 32rpx;
      font-weight: 500;
      color: $mg-text-primary;
    }
  }
  
  // 联系方式
  .contact-methods {
    .contact-item {
      display: flex;
      align-items: center;
      padding: 24rpx 0;
      border-bottom: 1px solid $mg-border-light;
      
      &:last-child {
        border-bottom: none;
      }
      
      .contact-icon {
        width: 80rpx;
        height: 80rpx;
        background-color: rgba($mg-primary, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 20rpx;
        
        .iconfont {
          font-size: 40rpx;
          color: $mg-primary;
        }
      }
      
      .contact-info {
        flex: 1;
        
        .contact-label {
          font-size: 28rpx;
          color: $mg-text-secondary;
          margin-bottom: 6rpx;
        }
        
        .contact-value {
          font-size: 30rpx;
          color: $mg-text-primary;
          font-weight: 500;
        }
      }
      
      .contact-action {
        font-size: 28rpx;
        color: $mg-primary;
        padding: 8rpx 20rpx;
        border: 1px solid $mg-primary;
        border-radius: 30rpx;
      }
    }
  }
  
  // 客服时间
  .service-hours {
    .time-item {
      display: flex;
      justify-content: space-between;
      padding: 16rpx 0;
      
      .day {
        font-size: 28rpx;
        color: $mg-text-primary;
      }
      
      .hours {
        font-size: 28rpx;
        color: $mg-text-secondary;
      }
    }
  }
  
  // 留言表单
  .message-form {
    .form-item {
      margin-bottom: 24rpx;
      position: relative;
      
      .form-label {
        font-size: 28rpx;
        color: $mg-text-secondary;
        margin-bottom: 12rpx;
        display: block;
      }
      
      .select-box {
        height: 80rpx;
        border: 1px solid $mg-border-medium;
        border-radius: 8rpx;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 24rpx;
        
        .select-value {
          font-size: 28rpx;
          color: $mg-text-primary;
        }
        
        .iconfont {
          font-size: 24rpx;
          color: $mg-text-tertiary;
        }
      }
      
      .message-textarea {
        width: 100%;
        height: 240rpx;
        border: 1px solid $mg-border-medium;
        border-radius: 8rpx;
        padding: 20rpx;
        font-size: 28rpx;
        color: $mg-text-primary;
        box-sizing: border-box;
      }
      
      .word-count {
        position: absolute;
        right: 20rpx;
        bottom: 20rpx;
        font-size: 24rpx;
        color: $mg-text-tertiary;
      }
      
      .contact-input {
        height: 80rpx;
        border: 1px solid $mg-border-medium;
        border-radius: 8rpx;
        padding: 0 24rpx;
        font-size: 28rpx;
        color: $mg-text-primary;
      }
    }
    
    .submit-btn {
      margin-top: 40rpx;
      width: 100%;
      height: 88rpx;
      background-color: $mg-primary;
      color: $mg-white;
      border-radius: 44rpx;
      font-size: 32rpx;
      font-weight: 500;
      display: flex;
      align-items: center;
      justify-content: center;
      border: none;
    }
  }
  
  // 常见问题
  .faq-list {
    .faq-item {
      border-bottom: 1px solid $mg-border-light;
      padding: 24rpx 0;
      
      &:last-child {
        border-bottom: none;
      }
      
      .faq-question {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .question-text {
          font-size: 28rpx;
          color: $mg-text-primary;
          font-weight: 500;
        }
        
        .iconfont {
          font-size: 26rpx;
          color: $mg-text-tertiary;
        }
      }
      
      .faq-answer {
        margin-top: 16rpx;
        padding: 16rpx;
        background-color: $mg-bg-secondary;
        border-radius: 8rpx;
        
        text {
          font-size: 26rpx;
          color: $mg-text-secondary;
          line-height: 1.6;
        }
      }
    }
  }
  </style>
  