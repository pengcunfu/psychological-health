<template>
  <view class="course-player">
    <!-- 视频播放器 -->
    <view class="video-container">
      <view class="video-player">
        <view class="play-button" @click="togglePlay">
          <text class="iconfont play-icon">&#xe600;</text>
        </view>
      </view>
    </view>
    
    <!-- 课程章节信息 -->
    <view class="chapter-info">
      <view class="chapter-title">{{ currentChapter.title }}</view>
      <view class="chapter-progress">
        <text>{{ currentChapter.lessonCount }}课时</text>
        <text class="dot-separator">•</text>
        <text>{{ currentChapter.duration }}</text>
        <text class="dot-separator">•</text>
        <text>已学习{{ currentChapter.progress }}%</text>
      </view>
      <view class="progress-bar">
        <view class="progress-inner" :style="{ width: currentChapter.progress + '%' }"></view>
      </view>
    </view>
    
    <!-- 标签导航 -->
    <view class="tab-navigation">
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
    
    <!-- 内容区域 -->
    <scroll-view class="content-scroll" scroll-y>
      <!-- 章节内容 -->
      <view v-if="currentTab === 0" class="lessons-content">
        <view 
          v-for="(lesson, index) in lessonList" 
          :key="index"
          class="lesson-item"
          @click="selectLesson(lesson)"
        >
          <view class="lesson-number">
            <text>{{ lesson.index }}</text>
          </view>
          <view class="lesson-info">
            <view class="lesson-title">{{ lesson.title }}</view>
            <view class="lesson-duration">{{ lesson.duration }}</view>
          </view>
          <view class="lesson-status" :class="getLessonStatusClass(lesson.status)">
            {{ getLessonStatusText(lesson.status) }}
          </view>
        </view>
      </view>
      
      <!-- 评论内容 -->
      <view v-if="currentTab === 1" class="comments-content">
        <view class="empty-content">
          <text>暂无评论</text>
        </view>
      </view>
      
      <!-- 资料内容 -->
      <view v-if="currentTab === 2" class="materials-content">
        <view class="empty-content">
          <text>暂无资料</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue';

// 标签页数据
const tabs = ['章节', '评论', '资料'];
const currentTab = ref(0);

// 当前章节信息
const currentChapter = reactive({
  title: '第一章：认识情绪',
  lessonCount: 3,
  duration: '45分钟',
  progress: 30
});

// 课程列表数据
const lessonList = ref([
  {
    index: 1,
    title: '1.1 什么是情绪',
    duration: '15分钟',
    status: 'inProgress'
  },
  {
    index: 2,
    title: '1.2 情绪的分类',
    duration: '15分钟',
    status: 'notStarted'
  },
  {
    index: 3,
    title: '1.3 情绪与健康的关系',
    duration: '15分钟',
    status: 'notStarted'
  },
  {
    index: 4,
    title: '2.1 情绪的生理基础',
    duration: '15分钟',
    status: 'notStarted'
  },
  {
    index: 5,
    title: '2.2 情绪的认知因素',
    duration: '15分钟',
    status: 'notStarted'
  },
  {
    index: 6,
    title: '3.1 认知偏差与情绪',
    duration: '15分钟',
    status: 'notStarted'
  }
]);

// 切换标签页
const switchTab = (index) => {
  currentTab.value = index;
};

// 返回上一页
const goBack = () => {
  uni.navigateBack();
};

// 切换播放状态
const togglePlay = () => {
  console.log('切换播放/暂停');
  // 这里添加视频播放逻辑
};

// 选择课程
const selectLesson = (lesson) => {
  console.log('选择课程', lesson);
  // 这里添加选择课程的逻辑
};

// 获取课程状态文本
const getLessonStatusText = (status) => {
  const statusMap = {
    completed: '已完成',
    inProgress: '学习中',
    notStarted: '未学习'
  };
  return statusMap[status] || '未学习';
};

// 获取课程状态样式类
const getLessonStatusClass = (status) => {
  const classMap = {
    completed: 'status-completed',
    inProgress: 'status-in-progress',
    notStarted: 'status-not-started'
  };
  return classMap[status] || '';
};
</script>

<style lang="scss" scoped>
@import '@/static/theme.scss';

.course-player {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: $mg-white;
}

// 导航栏
.nav-bar {
  display: flex;
  align-items: center;
  height: 90rpx;
  padding: 0 20rpx;
  background-color: $mg-white;
  position: relative;
  
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

// 视频播放器
.video-container {
  width: 100%;
  height: 422rpx;
  background-color: #000;
  position: relative;
  
  .video-player {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    
    .play-button {
      width: 100rpx;
      height: 100rpx;
      border-radius: 50%;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      
      .play-icon {
        font-size: 50rpx;
        color: $mg-white;
      }
    }
  }
}

// 课程章节信息
.chapter-info {
  padding: 30rpx;
  
  .chapter-title {
    font-size: 36rpx;
    font-weight: bold;
    color: $mg-text-primary;
    margin-bottom: 16rpx;
  }
  
  .chapter-progress {
    display: flex;
    align-items: center;
    font-size: 28rpx;
    color: $mg-text-secondary;
    margin-bottom: 20rpx;
    
    .dot-separator {
      margin: 0 16rpx;
    }
  }
  
  .progress-bar {
    height: 8rpx;
    width: 100%;
    background-color: $mg-gray-200;
    border-radius: 4rpx;
    overflow: hidden;
    
    .progress-inner {
      height: 100%;
      background-color: $mg-primary;
      border-radius: 4rpx;
    }
  }
}

// 标签导航
.tab-navigation {
  display: flex;
  border-bottom: 1px solid $mg-border-light;
  
  .tab-item {
    flex: 1;
    display: flex;
    justify-content: center;
    padding: 24rpx 0;
    position: relative;
    
    .tab-text {
      font-size: 30rpx;
      color: $mg-text-secondary;
    }
    
    &.active {
      .tab-text {
        color: $mg-primary;
        font-weight: 500;
      }
      
      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 40rpx;
        height: 4rpx;
        background-color: $mg-primary;
      }
    }
  }
}

// 内容区域
.content-scroll {
  flex: 1;
}

// 课程列表
.lessons-content {
  padding-bottom: env(safe-area-inset-bottom);
  
  .lesson-item {
    display: flex;
    align-items: center;
    padding: 30rpx;
    border-bottom: 1px solid $mg-border-light;
    
    .lesson-number {
      width: 60rpx;
      height: 60rpx;
      border-radius: 50%;
      background-color: $mg-primary-light;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 24rpx;
      
      text {
        color: $mg-white;
        font-size: 28rpx;
      }
    }
    
    .lesson-info {
      flex: 1;
      
      .lesson-title {
        font-size: 30rpx;
        color: $mg-text-primary;
        margin-bottom: 8rpx;
      }
      
      .lesson-duration {
        font-size: 24rpx;
        color: $mg-text-tertiary;
      }
    }
    
    .lesson-status {
      font-size: 28rpx;
      
      &.status-in-progress {
        color: $mg-primary;
      }
      
      &.status-completed {
        color: $mg-success;
      }
      
      &.status-not-started {
        color: $mg-text-tertiary;
      }
    }
  }
}

// 空内容提示
.empty-content {
  padding: 60rpx 0;
  text-align: center;
  color: $mg-text-tertiary;
  font-size: 28rpx;
}
</style>
