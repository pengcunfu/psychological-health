<template>
  <view class="favorite-page">    
    <!-- 分类标签 -->
    <view class="tabs">
      <view 
        v-for="(tab, index) in tabs" 
        :key="index" 
        class="tab-item" 
        :class="{ active: currentTab === index }"
        @click="switchTab(index)"
      >
        {{ tab.name }}
      </view>
    </view>
    
    <!-- 收藏列表 -->
    <scroll-view 
      scroll-y 
      class="favorite-list" 
      @scrolltolower="loadMore" 
      :refresher-enabled="true"
      :refresher-triggered="refreshing" 
      @refresherrefresh="onRefresh"
    >
      <!-- 空状态 -->
      <view v-if="favoriteList.length === 0" class="empty-list">
        <image class="empty-icon" src="/static/icons/empty-favorite.png" mode="aspectFit"></image>
        <text class="empty-text">暂无收藏内容</text>
        <text class="empty-tip">收藏喜欢的咨询师或课程，方便随时查看</text>
        <button class="empty-btn" @click="goToDiscover">去浏览</button>
      </view>
      
      <!-- 咨询师列表 -->
      <view v-else-if="currentTab === 0" class="counselor-list">
        <view 
          v-for="(item, index) in favoriteList" 
          :key="index" 
          class="counselor-item"
          @click="goToDetail('counselor', item.id)"
        >
          <view class="counselor-card">
            <image class="counselor-avatar" :src="item.avatar" mode="aspectFill"></image>
            <view class="counselor-info">
              <view class="counselor-header">
                <text class="counselor-name">{{ item.name }}</text>
                <view class="counselor-verified" v-if="item.isVerified">
                  <text class="verified-icon iconfont">&#xe6ba;</text>
                  <text class="verified-text">已认证</text>
                </view>
              </view>
              <text class="counselor-title">{{ item.title }}</text>
              <view class="counselor-tags">
                <text 
                  v-for="(tag, i) in item.tags" 
                  :key="i" 
                  class="tag-item"
                >{{ tag }}</text>
              </view>
              <view class="counselor-price">
                <text class="price-label">咨询费用：</text>
                <text class="price-value">¥{{ item.price }}/次</text>
              </view>
            </view>
          </view>
          <view class="action-bar">
            <view class="action-btn like-btn" @click.stop="removeFavorite(item.id)">
              <text class="iconfont">&#xe6a3;</text>
              <text>取消收藏</text>
            </view>
            <view class="action-btn appoint-btn" @click.stop="makeAppointment(item.id)">
              <text>立即预约</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 课程列表 -->
      <view v-else class="course-list">
        <view 
          v-for="(item, index) in favoriteList" 
          :key="index" 
          class="course-item"
          @click="goToDetail('course', item.id)"
        >
          <view class="course-card">
            <image class="course-cover" :src="item.coverImage" mode="aspectFill"></image>
            <view class="course-info">
              <text class="course-title">{{ item.title }}</text>
              <view class="course-meta">
                <text class="course-teacher">{{ item.teacher }}</text>
                <text class="course-length">{{ item.lessonCount }}课时</text>
              </view>
              <view class="course-stats">
                <text class="stats-item">
                  <text class="iconfont">&#xe6b8;</text>
                  <text>{{ item.studentCount }}</text>
                </text>
                <text class="stats-item">
                  <text class="iconfont">&#xe6c8;</text>
                  <text>{{ item.rating }}</text>
                </text>
              </view>
              <view class="course-price">
                <text class="price-value">¥{{ item.price }}</text>
                <text class="original-price" v-if="item.originalPrice">¥{{ item.originalPrice }}</text>
              </view>
            </view>
          </view>
          <view class="action-bar">
            <view class="action-btn like-btn" @click.stop="removeFavorite(item.id)">
              <text class="iconfont">&#xe6a3;</text>
              <text>取消收藏</text>
            </view>
            <view class="action-btn buy-btn" @click.stop="buyCourse(item.id)">
              <text>立即购买</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 加载更多 -->
      <view v-if="favoriteList.length > 0 && hasMore" class="loading-more">
        <u-loadmore :status="loadMoreStatus" />
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';

// 标签页
const tabs = [
  { name: '咨询师', type: 'counselor' },
  { name: '课程', type: 'course' }
];

// 响应式数据
const currentTab = ref(0);
const favoriteList = ref([]);
const page = ref(1);
const pageSize = ref(10);
const hasMore = ref(true);
const loadMoreStatus = ref('loadmore');
const refreshing = ref(false);

// 切换标签页
const switchTab = (index) => {
  if (currentTab.value === index) return;
  currentTab.value = index;
  resetList();
  loadFavorites();
};

// 重置列表
const resetList = () => {
  favoriteList.value = [];
  page.value = 1;
  hasMore.value = true;
  loadMoreStatus.value = 'loadmore';
};

// 加载收藏列表
const loadFavorites = () => {
  const type = tabs[currentTab.value].type;
  
  // 模拟加载数据
  // 实际开发中这里会调用API获取数据
  setTimeout(() => {
    if (type === 'counselor') {
      favoriteList.value = mockCounselors;
    } else {
      favoriteList.value = mockCourses;
    }
    
    refreshing.value = false;
  }, 1000);
};

// 上拉加载更多
const loadMore = () => {
  if (!hasMore.value) return;
  
  loadMoreStatus.value = 'loading';
  
  // 模拟加载更多数据
  setTimeout(() => {
    // 假设没有更多数据了
    hasMore.value = false;
    loadMoreStatus.value = 'nomore';
  }, 1000);
};

// 下拉刷新
const onRefresh = () => {
  refreshing.value = true;
  resetList();
  loadFavorites();
};

// 取消收藏
const removeFavorite = (id) => {
  uni.showModal({
    title: '取消收藏',
    content: '确定要取消收藏该内容吗？',
    success: (res) => {
      if (res.confirm) {
        // 模拟取消收藏
        favoriteList.value = favoriteList.value.filter(item => item.id !== id);
        uni.showToast({
          title: '已取消收藏',
          icon: 'success'
        });
      }
    }
  });
};

// 跳转详情页
const goToDetail = (type, id) => {
  if (type === 'counselor') {
    uni.navigateTo({
      url: `/pages/counselor/detail/index?id=${id}`
    });
  } else {
    uni.navigateTo({
      url: `/pages/course/detail/index?id=${id}`
    });
  }
};

// 预约咨询
const makeAppointment = (id) => {
  uni.navigateTo({
    url: `/pages/counselor/appointment/index?id=${id}`
  });
};

// 购买课程
const buyCourse = (id) => {
  uni.navigateTo({
    url: `/pages/course/buy/index?id=${id}`
  });
};

// 去发现页
const goToDiscover = () => {
  uni.switchTab({
    url: '/pages/discover/index'
  });
};

// 页面加载时获取收藏列表
onMounted(() => {
  loadFavorites();
});

// 模拟数据
const mockCounselors = [
  {
    id: '1',
    name: '李瑞峰',
    title: '高级心理咨询师',
    isVerified: true,
    avatar: '/static/images/counselor1.jpg',
    tags: ['抑郁症', '青少年心理', '婚姻情感'],
    price: 900
  },
  {
    id: '2',
    name: '王晓华',
    title: '资深心理咨询师',
    isVerified: true,
    avatar: '/static/images/counselor2.jpg',
    tags: ['焦虑症', '强迫症', '职场压力'],
    price: 800
  },
  {
    id: '3',
    name: '张明',
    title: '心理治疗师',
    isVerified: false,
    avatar: '/static/images/counselor3.jpg',
    tags: ['睡眠障碍', '心理创伤', '人际关系'],
    price: 700
  }
];

const mockCourses = [
  {
    id: '1',
    title: '情绪管理与心理健康',
    teacher: '李瑞峰',
    lessonCount: 12,
    studentCount: 2354,
    rating: 4.9,
    coverImage: '/static/images/course1.jpg',
    price: 299,
    originalPrice: 399
  },
  {
    id: '2',
    title: '走出抑郁：认知行为疗法',
    teacher: '王晓华',
    lessonCount: 8,
    studentCount: 1688,
    rating: 4.8,
    coverImage: '/static/images/course2.jpg',
    price: 199,
    originalPrice: 299
  },
  {
    id: '3',
    title: '亲子沟通技巧提升',
    teacher: '张明',
    lessonCount: 10,
    studentCount: 3201,
    rating: 4.7,
    coverImage: '/static/images/course3.jpg',
    price: 249
  }
];
</script>

<style lang="scss" scoped>
@import '@/static/theme.scss';

.favorite-page {
  min-height: 100vh;
  background-color: $mg-bg-secondary;
  display: flex;
  flex-direction: column;
}

// 页面标题
.page-header {
  height: 100rpx;
  background-color: $mg-primary;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .page-title {
    font-size: 36rpx;
    color: $mg-white;
    font-weight: 500;
  }
}

// 分类标签
.tabs {
  display: flex;
  background-color: $mg-white;
  height: 88rpx;
  border-bottom: 1px solid $mg-border-light;
  
  .tab-item {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 28rpx;
    color: $mg-text-secondary;
    position: relative;
    
    &.active {
      color: $mg-primary;
      font-weight: 500;
      
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

// 收藏列表
.favorite-list {
  flex: 1;
  padding: 20rpx;
  box-sizing: border-box;
}

// 空状态
.empty-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
  
  .empty-icon {
    width: 200rpx;
    height: 200rpx;
    margin-bottom: 30rpx;
  }
  
  .empty-text {
    font-size: 32rpx;
    color: $mg-text-primary;
    font-weight: 500;
    margin-bottom: 16rpx;
  }
  
  .empty-tip {
    font-size: 28rpx;
    color: $mg-text-tertiary;
    margin-bottom: 40rpx;
  }
  
  .empty-btn {
    width: 240rpx;
    height: 80rpx;
    background-color: $mg-primary;
    color: $mg-white;
    font-size: 28rpx;
    border-radius: 40rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
  }
}

// 咨询师卡片
.counselor-item {
  background-color: $mg-white;
  border-radius: 12rpx;
  margin-bottom: 20rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 10rpx $mg-shadow-color;
  
  .counselor-card {
    display: flex;
    padding: 24rpx;
    
    .counselor-avatar {
      width: 120rpx;
      height: 120rpx;
      border-radius: 60rpx;
      margin-right: 20rpx;
    }
    
    .counselor-info {
      flex: 1;
      
      .counselor-header {
        display: flex;
        align-items: center;
        margin-bottom: 10rpx;
        
        .counselor-name {
          font-size: 32rpx;
          font-weight: 500;
          color: $mg-text-primary;
          margin-right: 10rpx;
        }
        
        .counselor-verified {
          display: flex;
          align-items: center;
          background-color: rgba($mg-primary, 0.1);
          padding: 4rpx 10rpx;
          border-radius: 20rpx;
          
          .verified-icon {
            font-size: 24rpx;
            color: $mg-primary;
            margin-right: 4rpx;
          }
          
          .verified-text {
            font-size: 22rpx;
            color: $mg-primary;
          }
        }
      }
      
      .counselor-title {
        font-size: 26rpx;
        color: $mg-text-secondary;
        margin-bottom: 16rpx;
      }
      
      .counselor-tags {
        display: flex;
        flex-wrap: wrap;
        margin-bottom: 16rpx;
        
        .tag-item {
          font-size: 22rpx;
          color: $mg-text-secondary;
          background-color: $mg-bg-secondary;
          padding: 6rpx 16rpx;
          border-radius: 20rpx;
          margin-right: 10rpx;
          margin-bottom: 10rpx;
        }
      }
      
      .counselor-price {
        font-size: 26rpx;
        
        .price-label {
          color: $mg-text-secondary;
        }
        
        .price-value {
          color: $mg-accent;
          font-weight: 500;
        }
      }
    }
  }
  
  .action-bar {
    display: flex;
    border-top: 1px solid $mg-border-light;
    
    .action-btn {
      flex: 1;
      height: 80rpx;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28rpx;
      
      .iconfont {
        font-size: 30rpx;
        margin-right: 8rpx;
      }
      
      &.like-btn {
        color: $mg-text-secondary;
      }
      
      &.appoint-btn {
        background-color: $mg-primary;
        color: $mg-white;
      }
    }
  }
}

// 课程卡片
.course-item {
  background-color: $mg-white;
  border-radius: 12rpx;
  margin-bottom: 20rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 10rpx $mg-shadow-color;
  
  .course-card {
    display: flex;
    padding: 24rpx;
    
    .course-cover {
      width: 200rpx;
      height: 120rpx;
      border-radius: 8rpx;
      margin-right: 20rpx;
    }
    
    .course-info {
      flex: 1;
      
      .course-title {
        font-size: 30rpx;
        font-weight: 500;
        color: $mg-text-primary;
        margin-bottom: 10rpx;
        line-height: 1.4;
        display: -webkit-box;
        --webkit-box-orient: vertical;
        --webkit-line-clamp: 2;
        overflow: hidden;
      }
      
      .course-meta {
        display: flex;
        align-items: center;
        margin-bottom: 10rpx;
        
        .course-teacher {
          font-size: 26rpx;
          color: $mg-text-secondary;
          margin-right: 20rpx;
        }
        
        .course-length {
          font-size: 24rpx;
          color: $mg-text-tertiary;
        }
      }
      
      .course-stats {
        display: flex;
        margin-bottom: 10rpx;
        
        .stats-item {
          font-size: 24rpx;
          color: $mg-text-tertiary;
          margin-right: 20rpx;
          display: flex;
          align-items: center;
          
          .iconfont {
            font-size: 26rpx;
            margin-right: 6rpx;
          }
        }
      }
      
      .course-price {
        .price-value {
          font-size: 30rpx;
          color: $mg-accent;
          font-weight: 500;
          margin-right: 10rpx;
        }
        
        .original-price {
          font-size: 24rpx;
          color: $mg-text-tertiary;
          text-decoration: line-through;
        }
      }
    }
  }
  
  .action-bar {
    display: flex;
    border-top: 1px solid $mg-border-light;
    
    .action-btn {
      flex: 1;
      height: 80rpx;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28rpx;
      
      .iconfont {
        font-size: 30rpx;
        margin-right: 8rpx;
      }
      
      &.like-btn {
        color: $mg-text-secondary;
      }
      
      &.buy-btn {
        background-color: $mg-primary;
        color: $mg-white;
      }
    }
  }
}

// 加载更多
.loading-more {
  padding: 20rpx 0;
  text-align: center;
}
</style>
