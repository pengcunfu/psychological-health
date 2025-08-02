<template>
  <view class="course-detail">    
    <!-- 课程封面 - 可能会有图片展示，目前用空白区域 -->
    <view class="course-cover"></view>
    
    <!-- 课程标题区域 -->
    <view class="course-title-section">
      <text class="course-title">情绪管理与心理健康</text>
      
      <!-- 标签区域 -->
      <view class="tag-container">
        <view class="tag">减压</view>
        <view class="tag">情绪管理</view>
        <view class="tag">心理健康</view>
      </view>
      
      <!-- 课程数据统计 -->
      <view class="course-stats">
        <view class="stat-item">
          <text class="stat-value">12</text>
          <text class="stat-label">课时</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">3h</text>
          <text class="stat-label">总时长</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">1689</text>
          <text class="stat-label">学习人数</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">4.9</text>
          <text class="stat-label">评分</text>
        </view>
      </view>
    </view>
    
    <!-- 分割线 -->
    <view class="divider"></view>
    
    <!-- 讲师信息 -->
    <view class="instructor-section">
      <view class="instructor-avatar">
        <text class="instructor-avatar-text">讲师头像</text>
      </view>
      <view class="instructor-info">
        <text class="instructor-name">李明</text>
        <text class="instructor-title">国家二级心理咨询师 | 情绪管理专家</text>
      </view>
    </view>
    
    <!-- 分割线 -->
    <view class="divider"></view>
    
    <!-- 课程介绍 -->
    <view class="course-intro-section">
      <view class="section-title">
        <view class="section-title-bar"></view>
        <text class="section-title-text">课程简介</text>
      </view>
      <text class="course-intro-text">
        本课程系统介绍情绪管理的核心理念和实用技巧，从认知行为疗法的角度出发，帮助你了解情绪的产生机制，掌握调节负面情绪的方法，建立健康的心理状态。适合各类职场人士、学生以及任何希望提升情绪管理能力的人群。
      </text>
    </view>
    
    <!-- 课程大纲 -->
    <view class="course-outline-section">
      <view class="section-title">
        <view class="section-title-bar"></view>
        <text class="section-title-text">课程大纲</text>
      </view>
      
      <!-- 章节列表 -->
      <view class="chapter-list">
        <!-- 第一章 -->
        <view class="chapter-item">
          <view class="chapter-header">
            <view class="chapter-icon">
              <text class="iconfont clock-icon">&#xe74c;</text>
            </view>
            <text class="chapter-title">第一章：认识情绪</text>
            <text class="chapter-duration">3课时 · 45分钟</text>
          </view>
        </view>
        
        <!-- 第二章 -->
        <view class="chapter-item">
          <view class="chapter-header">
            <view class="chapter-icon">
              <text class="iconfont clock-icon">&#xe74c;</text>
            </view>
            <text class="chapter-title">第二章：情绪的产生机制</text>
            <text class="chapter-duration">2课时 · 30分钟</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 底部价格与购买按钮 -->
    <view class="course-footer">
      <view class="price-container">
        <text class="current-price">¥299</text>
        <text class="original-price">¥399</text>
      </view>
      <view class="buy-button" @click="handleBuy">
        <text class="buy-text">立即购买</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue';

// 返回上一页
const goBack = () => {
  uni.navigateBack();
};

// 购买课程
const handleBuy = () => {
  uni.showToast({
    title: '购买功能开发中...',
    icon: 'none'
  });
};
</script>

<style lang="scss" scoped>
@import '@/static/theme.scss';

.course-detail {
  min-height: 100vh;
  background-color: $mg-white;
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

// 课程封面
.course-cover {
  width: 100%;
  height: 300rpx;
  background-color: $mg-gray-100;
}

// 课程标题区域
.course-title-section {
  padding: 30rpx 40rpx;
  
  .course-title {
    font-size: 40rpx;
    font-weight: bold;
    color: $mg-text-primary;
    line-height: 1.4;
  }
  
  // 标签区域
  .tag-container {
    display: flex;
    margin-top: 24rpx;
    flex-wrap: wrap;
    
    .tag {
      height: 56rpx;
      padding: 0 24rpx;
      background-color: $mg-bg-gold-light;
      color: $mg-primary;
      border-radius: 28rpx;
      margin-right: 20rpx;
      margin-bottom: 16rpx;
      display: flex;
      align-items: center;
      font-size: 26rpx;
      border: 1rpx solid rgba($mg-primary, 0.2);
    }
  }
  
  // 课程数据统计
  .course-stats {
    display: flex;
    justify-content: space-between;
    margin-top: 40rpx;
    
    .stat-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      flex: 1;
      
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
}

// 分割线
.divider {
  height: 20rpx;
  background-color: $mg-gray-100;
}

// 讲师信息
.instructor-section {
  padding: 30rpx 40rpx;
  display: flex;
  align-items: center;
  
  .instructor-avatar {
    width: 80rpx;
    height: 80rpx;
    background-color: $mg-primary-light;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    
    .instructor-avatar-text {
      font-size: 0;
      color: transparent;
    }
  }
  
  .instructor-info {
    margin-left: 20rpx;
    
    .instructor-name {
      font-size: 32rpx;
      font-weight: 500;
      color: $mg-text-primary;
    }
    
    .instructor-title {
      font-size: 24rpx;
      color: $mg-text-tertiary;
      margin-top: 8rpx;
    }
  }
}

// 课程介绍
.course-intro-section {
  padding: 30rpx 40rpx;
  
  .section-title {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
    
    .section-title-bar {
      width: 6rpx;
      height: 32rpx;
      background-color: $mg-primary;
      border-radius: 3rpx;
    }
    
    .section-title-text {
      font-size: 32rpx;
      font-weight: bold;
      color: $mg-text-primary;
      margin-left: 16rpx;
    }
  }
  
  .course-intro-text {
    font-size: 28rpx;
    color: $mg-text-secondary;
    line-height: 1.6;
  }
}

// 课程大纲
.course-outline-section {
  padding: 30rpx 40rpx;
  
  .section-title {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
    
    .section-title-bar {
      width: 6rpx;
      height: 32rpx;
      background-color: $mg-primary;
      border-radius: 3rpx;
    }
    
    .section-title-text {
      font-size: 32rpx;
      font-weight: bold;
      color: $mg-text-primary;
      margin-left: 16rpx;
    }
  }
  
  // 章节列表
  .chapter-list {
    .chapter-item {
      margin-bottom: 20rpx;
      
      .chapter-header {
        display: flex;
        align-items: center;
        height: 80rpx;
        
        .chapter-icon {
          width: 40rpx;
          height: 40rpx;
          display: flex;
          align-items: center;
          justify-content: center;
          
          .clock-icon {
            font-size: 36rpx;
            color: $mg-text-tertiary;
          }
        }
        
        .chapter-title {
          flex: 1;
          font-size: 28rpx;
          color: $mg-text-primary;
          margin-left: 16rpx;
        }
        
        .chapter-duration {
          font-size: 24rpx;
          color: $mg-text-tertiary;
        }
      }
    }
  }
}

// 底部价格与购买按钮
.course-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100rpx;
  background-color: $mg-white;
  display: flex;
  align-items: center;
  padding: 0 30rpx;
  box-shadow: 0 -4rpx 10rpx $mg-shadow-color;
  
  .price-container {
    flex: 1;
    
    .current-price {
      font-size: 40rpx;
      font-weight: bold;
      color: $mg-accent;
    }
    
    .original-price {
      font-size: 24rpx;
      color: $mg-text-tertiary;
      text-decoration: line-through;
      margin-left: 10rpx;
    }
  }
  
  .buy-button {
    width: 240rpx;
    height: 80rpx;
    background-color: $mg-primary;
    border-radius: 40rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    
    .buy-text {
      color: $mg-white;
      font-size: 30rpx;
      font-weight: 500;
    }
  }
}
</style>
