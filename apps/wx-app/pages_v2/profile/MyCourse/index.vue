<template>
  <view class="my-course">
    <!-- 用户信息头部 -->
    <view class="user-header">
      <view class="avatar-wrapper">
        <image class="avatar" src="/static/avatar.png"></image>
      </view>
      <view class="user-info">
        <text class="username">张三</text>
        <text class="study-time">学习时长：12小时</text>
      </view>
    </view>
    
    <!-- 学习数据统计 -->
    <view class="stats-section">
      <view class="stat-item">
        <text class="stat-value">5</text>
        <text class="stat-label">已购课程</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">12</text>
        <text class="stat-label">已学课时</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">2</text>
        <text class="stat-label">今日学习</text>
      </view>
    </view>
    
    <!-- 课程分类标签 -->
    <view class="course-tabs">
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
    
    <!-- 课程列表 -->
    <view class="course-list">
      <!-- 课程项1 -->
      <view class="course-item">
        <image class="course-image" src="/static/course-img.png" mode="aspectFill"></image>
        <view class="course-info">
          <view class="course-title">情绪管理与心理健康</view>
          
          <view class="progress-container">
            <view class="progress-bar">
              <view class="progress-inner" style="width: 30%;"></view>
            </view>
            <text class="progress-text">3/10课时</text>
          </view>
          
          <view class="course-footer">
            <text class="last-study">最近学习：今天</text>
            <button class="continue-btn" @click="continueLearning('情绪管理与心理健康')">继续学习</button>
          </view>
        </view>
      </view>
      
      <!-- 课程项2 -->
      <view class="course-item">
        <image class="course-image" src="/static/course-img.png" mode="aspectFill"></image>
        <view class="course-info">
          <view class="course-title">人际关系修复与提升</view>
          
          <view class="progress-container">
            <view class="progress-bar">
              <view class="progress-inner" style="width: 50%;"></view>
            </view>
            <text class="progress-text">4/8课时</text>
          </view>
          
          <view class="course-footer">
            <text class="last-study">最近学习：2天前</text>
            <button class="continue-btn" @click="continueLearning('人际关系修复与提升')">继续学习</button>
          </view>
        </view>
      </view>
      
      <!-- 课程项3 -->
      <view class="course-item">
        <image class="course-image" src="/static/course-img.png" mode="aspectFill"></image>
        <view class="course-info">
          <view class="course-title">压力管理与减压技巧</view>
          
          <view class="progress-container">
            <view class="progress-bar">
              <view class="progress-inner completed" style="width: 100%;"></view>
            </view>
            <text class="progress-text">10/10课时</text>
          </view>
          
          <view class="course-footer">
            <text class="last-study">已完成</text>
            <button class="review-btn" @click="reviewCourse('压力管理与减压技巧')">再次学习</button>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue';

// 标签页数据
const tabs = ['全部', '学习中', '已完成'];
const currentTab = ref(0);

// 切换标签
const switchTab = (index) => {
  currentTab.value = index;
  // 根据选中的标签过滤课程列表
  // 此处可以添加实际的过滤逻辑
};

// 继续学习课程
const continueLearning = (courseName) => {
  console.log(`继续学习：${courseName}`);
  uni.navigateTo({
    url: `/pages/course/play/index?name=${encodeURIComponent(courseName)}`
  });
};

// 复习已完成课程
const reviewCourse = (courseName) => {
  console.log(`再次学习：${courseName}`);
  uni.navigateTo({
    url: `/pages/course/play/index?name=${encodeURIComponent(courseName)}&review=1`
  });
};
</script>

<style lang="scss" scoped>
@import '@/static/theme.scss';

.my-course {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: $mg-bg-secondary;
}

// 用户信息头部
.user-header {
  display: flex;
  align-items: center;
  padding: 40rpx 30rpx;
  background-color: $mg-primary; // 使用主题色变量
  
  .avatar-wrapper {
    width: 120rpx;
    height: 120rpx;
    border-radius: 60rpx;
    overflow: hidden;
    background-color: rgba($mg-white, 0.2);
    border: 2rpx solid $mg-white;
  }
  
  .avatar {
    width: 100%;
    height: 100%;
  }
  
  .user-info {
    margin-left: 20rpx;
    display: flex;
    flex-direction: column;
    
    .username {
      font-size: 36rpx;
      font-weight: 500;
      color: $mg-white;
    }
    
    .study-time {
      font-size: 24rpx;
      color: rgba($mg-white, 0.8);
      margin-top: 10rpx;
    }
  }
}

// 学习数据统计
.stats-section {
  display: flex;
  justify-content: space-around;
  padding: 40rpx 0;
  background-color: $mg-white;
  
  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .stat-value {
      font-size: 40rpx;
      font-weight: bold;
      color: $mg-text-primary;
      line-height: 1.2;
    }
    
    .stat-label {
      font-size: 24rpx;
      color: $mg-text-tertiary;
      margin-top: 10rpx;
    }
  }
}

// 课程分类标签
.course-tabs {
  display: flex;
  background-color: $mg-white;
  padding: 0 30rpx;
  
  .tab-item {
    padding: 20rpx 30rpx;
    position: relative;
    
    .tab-text {
      font-size: 28rpx;
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
        left: 30rpx;
        right: 30rpx;
        height: 6rpx;
        background-color: $mg-primary; // 使用主题色变量
        border-radius: 3rpx 3rpx 0 0;
      }
    }
  }
}

// 分割线
.divider {
  height: 1px;
  background-color: $mg-border-light;
}

// 课程列表
.course-list {
  flex: 1;
  padding: 20rpx 30rpx;
  
  .course-item {
    display: flex;
    background-color: $mg-white;
    border-radius: 12rpx;
    margin-bottom: 30rpx;
    padding: 20rpx;
    box-shadow: 0 2rpx 10rpx $mg-shadow-color;
    
    .course-image {
      width: 160rpx;
      height: 160rpx;
      border-radius: 8rpx;
      background-color: $mg-gray-200;
    }
    
    .course-info {
      flex: 1;
      margin-left: 20rpx;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      
      .course-title {
        font-size: 30rpx;
        font-weight: 500;
        color: $mg-text-primary;
        line-height: 1.4;
      }
      
      .progress-container {
        margin-top: 20rpx;
        display: flex;
        align-items: center;
        
        .progress-bar {
          flex: 1;
          height: 10rpx;
          background-color: $mg-gray-200;
          border-radius: 5rpx;
          overflow: hidden;
          
          .progress-inner {
            height: 100%;
            background-color: $mg-primary; // 使用主题色变量
            border-radius: 5rpx;
            
            &.completed {
              background-color: $mg-primary; // 使用主题色变量
            }
          }
        }
        
        .progress-text {
          font-size: 24rpx;
          color: $mg-text-tertiary;
          margin-left: 16rpx;
          white-space: nowrap;
        }
      }
      
      .course-footer {
        margin-top: 30rpx;
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .last-study {
          font-size: 24rpx;
          color: $mg-text-tertiary;
        }
        
        .continue-btn, .review-btn {
          min-width: 150rpx;
          height: 60rpx;
          line-height: 60rpx;
          text-align: center;
          border-radius: 30rpx;
          font-size: 24rpx;
          padding: 0 20rpx;
        }
        
        .continue-btn {
          background-color: $mg-primary; // 使用主题色变量
          color: $mg-white;
        }
        
        .review-btn {
          background-color: $mg-gray-200;
          color: $mg-text-secondary;
        }
      }
    }
  }
}
</style>
