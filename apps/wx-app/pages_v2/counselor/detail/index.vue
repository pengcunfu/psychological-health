<template>
  <view class="counselor-detail">  
    <!-- 咨询师基本信息区域 -->
    <view class="counselor-header">
      <view class="avatar-section">
        <view class="avatar-container">
          <text class="avatar-text">咨询师像</text>
        </view>
      </view>
      
      <view class="counselor-name-section">
        <view class="name-container">
          <text class="counselor-name">李瑞峰</text>
          <view class="verified-badge">
            <text class="iconfont verified-icon">&#xe6ba;</text>
          </view>
        </view>
        
        <view class="counselor-level">
          <text class="level-text">高级咨询师</text>
        </view>
        
        <view class="counselor-title">
          <text>中国心理学会注册心理师 | 国家二级心理咨询师</text>
        </view>
      </view>
      
      <!-- 擅长领域标签 -->
      <view class="expertise-tags">
        <view class="tag">焦虑抑郁</view>
        <view class="tag">职场压力</view>
        <view class="tag">婚恋关系</view>
        <view class="tag">个人成长</view>
      </view>
    </view>
    
    <!-- 咨询师统计数据 -->
    <view class="counselor-stats">
      <view class="stat-item">
        <text class="stat-value">4.9</text>
        <text class="stat-label">评分</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">18年</text>
        <text class="stat-label">从业年限</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">15700+</text>
        <text class="stat-label">咨询小时</text>
      </view>
    </view>
    
    <!-- 选项卡 -->
    <view class="tab-section">
      <view 
        v-for="(tab, index) in tabs" 
        :key="index"
        class="tab-item" 
        :class="{ active: currentTab === index }"
        @click="switchTab(index)"
      >
        <text class="tab-text">{{ tab }}</text>
      </view>
    </view>
    
    <!-- 分割线 -->
    <view class="divider"></view>
    
    <!-- 内容区域 -->
    <view class="content-section">
      <!-- 简介内容 -->
      <view v-if="currentTab === 0" class="intro-content">
        <view class="info-item">
          <text class="info-label">擅长问题</text>
          <text class="info-value">焦虑抑郁、情绪管理、职场压力、婚恋关系问题、人际关系、自我成长</text>
        </view>
        
        <view class="info-item">
          <text class="info-label">咨询方式</text>
          <text class="info-value">认知行为疗法(CBT)、接纳与承诺疗法(ACT)、正念减压疗法、叙事疗法</text>
        </view>
      </view>
      
      <!-- 服务说明 -->
      <view class="service-section">
        <view class="section-title">服务说明</view>
        
        <view class="service-item">
          <text class="service-label">咨询时长</text>
          <text class="service-value">50分钟/次</text>
        </view>
        
        <view class="service-item">
          <text class="service-label">咨询方式</text>
          <text class="service-value">线上视频、线下面对面</text>
        </view>
        
        <view class="service-item">
          <text class="service-label">咨询周期</text>
          <text class="service-value">建议每周一次，根据具体情况调整</text>
        </view>
        
        <view class="service-item">
          <text class="service-label">退款政策</text>
          <text class="service-value">未开始咨询前24小时可全额退款，24小时内退款80%</text>
        </view>
      </view>
    </view>
    
    <!-- 底部价格与预约 -->
    <view class="footer">
      <view class="price-section">
        <text class="price">¥900</text>
        <text class="unit">50分钟/次</text>
      </view>
      
      <button class="book-button" @click="handleBooking">
        立即预约
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue';

// 选项卡数据
const tabs = ['简介', '评价', '预约'];
const currentTab = ref(0);

// 切换选项卡
const switchTab = (index) => {
  currentTab.value = index;
};

// 返回上一页
const goBack = () => {
  uni.navigateBack();
};

// 预约咨询师
const handleBooking = () => {
  uni.navigateTo({
    url: '/pages/counselor/booking/index'
  });
};
</script>

<style lang="scss" scoped>
@import '@/static/theme.scss';

.counselor-detail {
  min-height: 100vh;
  background-color: $mg-bg-secondary;
  display: flex;
  flex-direction: column;
  position: relative;
  padding-bottom: 120rpx;
}

// 导航栏
.nav-bar {
  display: flex;
  align-items: center;
  height: 90rpx;
  padding: 0 20rpx;
  position: relative;
  background: $mg-white;
  
  .nav-left {
    width: 80rpx;
    display: flex;
    align-items: center;
    
    .nav-icon {
      font-size: 44rpx;
      color: $mg-text-primary;
    }
  }
  
  .nav-title {
    flex: 1;
    text-align: center;
    font-size: 36rpx;
    font-weight: 500;
    color: $mg-text-primary;
  }
  
  .nav-right {
    width: 80rpx;
    display: flex;
    justify-content: flex-end;
    
    .more-icon {
      font-size: 44rpx;
      color: $mg-text-primary;
    }
  }
}

// 咨询师基本信息区域
.counselor-header {
  padding: 30rpx 40rpx 40rpx;
  background-color: $mg-primary; // 使用主题色变量
  display: flex;
  flex-direction: column;
  
  .avatar-section {
    display: flex;
    justify-content: center;
    
    .avatar-container {
      width: 180rpx;
      height: 180rpx;
      border-radius: 50%;
      background-color: rgba(255, 255, 255, 0.2);
      border: 4rpx solid $mg-white;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      
      .avatar-text {
        font-size: 26rpx;
        color: $mg-white;
      }
    }
  }
  
  .counselor-name-section {
    margin-top: 20rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .name-container {
      display: flex;
      align-items: center;
      
      .counselor-name {
        font-size: 42rpx;
        font-weight: bold;
        color: $mg-white;
      }
      
      .verified-badge {
        margin-left: 12rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        
        .verified-icon {
          font-size: 36rpx;
          color: $mg-white;
        }
      }
    }
    
    .counselor-level {
      margin-top: 10rpx;
      background-color: $mg-accent-light;
      border-radius: 30rpx;
      padding: 6rpx 20rpx;
      
      .level-text {
        font-size: 24rpx;
        color: $mg-white;
      }
    }
    
    .counselor-title {
      margin-top: 16rpx;
      font-size: 26rpx;
      color: rgba(255, 255, 255, 0.9);
      text-align: center;
    }
  }
  
  // 擅长领域标签
  .expertise-tags {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 30rpx;
    
    .tag {
      background-color: rgba(255, 255, 255, 0.2);
      border-radius: 30rpx;
      padding: 8rpx 24rpx;
      margin: 10rpx;
      font-size: 24rpx;
      color: $mg-white;
    }
  }
}

// 咨询师统计数据
.counselor-stats {
  display: flex;
  justify-content: space-around;
  padding: 30rpx 20rpx;
  background-color: $mg-white;
  
  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .stat-value {
      font-size: 36rpx;
      font-weight: bold;
      color: $mg-text-primary;
    }
    
    .stat-label {
      font-size: 24rpx;
      color: $mg-text-tertiary;
      margin-top: 8rpx;
    }
  }
}

// 选项卡
.tab-section {
  display: flex;
  background-color: $mg-white;
  border-bottom: 1rpx solid $mg-border-light;
  
  .tab-item {
    flex: 1;
    display: flex;
    justify-content: center;
    padding: 30rpx 0;
    position: relative;
    
    .tab-text {
      font-size: 30rpx;
      color: $mg-text-secondary;
    }
    
    &.active {
      .tab-text {
        color: $mg-primary; // 使用主题色变量
        font-weight: 500;
      }
      
      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 80rpx;
        right: 80rpx;
        height: 4rpx;
        background-color: $mg-primary; // 使用主题色变量
      }
    }
  }
}

// 分割线
.divider {
  height: 20rpx;
  background-color: $mg-bg-secondary;
}

// 内容区域
.content-section {
  flex: 1;
  background-color: $mg-white;
  
  // 简介内容
  .intro-content {
    padding: 20rpx 40rpx;
    
    .info-item {
      margin-bottom: 40rpx;
      
      .info-label {
        font-size: 28rpx;
        color: $mg-text-tertiary;
        margin-bottom: 16rpx;
        display: block;
      }
      
      .info-value {
        font-size: 30rpx;
        color: $mg-text-primary;
        line-height: 1.6;
      }
    }
  }
  
  // 服务说明
  .service-section {
    padding: 30rpx 40rpx;
    
    .section-title {
      font-size: 32rpx;
      font-weight: bold;
      color: $mg-text-primary;
      margin-bottom: 30rpx;
    }
    
    .service-item {
      display: flex;
      margin-bottom: 30rpx;
      
      .service-label {
        width: 160rpx;
        font-size: 28rpx;
        color: $mg-text-tertiary;
      }
      
      .service-value {
        flex: 1;
        font-size: 28rpx;
        color: $mg-text-primary;
        line-height: 1.5;
      }
    }
  }
}

// 底部价格与预约
.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 120rpx;
  background-color: $mg-white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40rpx;
  box-shadow: 0 -4rpx 10rpx $mg-shadow-color;
  
  .price-section {
    display: flex;
    align-items: baseline;
    
    .price {
      font-size: 42rpx;
      font-weight: bold;
      color: $mg-accent; // 使用主题色变量
    }
    
    .unit {
      font-size: 24rpx;
      color: $mg-text-tertiary;
      margin-left: 10rpx;
    }
  }
  
  .book-button {
    width: 240rpx;
    height: 80rpx;
    background-color: $mg-primary; // 使用主题色变量
    color: $mg-white;
    font-size: 30rpx;
    font-weight: 500;
    border-radius: 40rpx;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
