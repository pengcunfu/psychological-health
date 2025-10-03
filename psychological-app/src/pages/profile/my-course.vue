<template>
  <view class="container">
    <!-- <Navbar
      title="我的课程"
      :showLeft="true"
      :showRight="false"
      @leftClick="goBack"
    /> -->
    
    <view class="tab-section">
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'all' }" 
        @click="switchTab('all')"
      >
        全部
      </view>
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'learning' }" 
        @click="switchTab('learning')"
      >
        学习中
      </view>
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'completed' }" 
        @click="switchTab('completed')"
      >
        已完成
      </view>
    </view>

    <view class="content-section">
      <view v-if="courses.length > 0">
        <view 
          class="course-card" 
          v-for="(item, index) in courses" 
          :key="index"
          @click="navigateToCourse(item)"
        >
          <image class="course-image" :src="item.cover || '/static/images/default-course.png'" mode="aspectFill"></image>
          <view class="course-info">
            <text class="course-name">{{ item.name }}</text>
            <view class="course-progress">
              <view class="progress-bar">
                <view class="progress-inner" :style="{ width: item.progress + '%' }"></view>
              </view>
              <text class="progress-text">{{ item.progress }}%</text>
            </view>
            <view class="course-stats">
              <view class="stat-item">
                <u-icon name="clock" size="24" color="#999"></u-icon>
                <text class="stat-text">{{ item.duration || '0小时' }}</text>
              </view>
              <view class="stat-item">
                <u-icon name="file-text" size="24" color="#999"></u-icon>
                <text class="stat-text">{{ item.lesson_count || 0 }}课时</text>
              </view>
              <text class="course-status" :class="`status-${item.status}`">{{ getStatusText(item.status) }}</text>
            </view>
          </view>
        </view>
      </view>
      <view v-else class="empty-content">
        <u-empty mode="list" icon="order" :text="`暂无${getTabText()}课程`"></u-empty>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad, onPullDownRefresh, onReachBottom } from '@dcloudio/uni-app'
import { request } from '@/utils/request'
import { checkLogin } from '@/utils/auth'
import Navbar from '@/components/Navbar.vue'

// 检查登录状态
if (!checkLogin()) {
  // 在 setup 语法糖中，无法直接返回空对象，需要处理登录跳转
  uni.redirectTo({
    url: '/pages/login'
  })
}

const activeTab = ref('all')
const courses = ref([])
const pagination = ref({
  page: 1,
  per_page: 10,
  total: 0,
  total_pages: 0
})
const loading = ref(false)

// 返回上一页
const goBack = () => {
  uni.navigateBack()
}
// 获取课程列表
const fetchCourses = async (reset = false) => {
  if (loading.value) return
  
  if (reset) {
    pagination.value.page = 1
    courses.value = []
  }
  
  loading.value = true
  
  try {
    // 根据当前标签页确定状态过滤
    let status = ''
    switch (activeTab.value) {
      case 'all':
        status = ''
        break
      case 'learning':
        status = 'learning'
        break
      case 'completed':
        status = 'completed'
        break
    }
    
    const res = await request({
      url: '/user/course',
      method: 'GET',
      data: {
        page: pagination.value.page,
        per_page: pagination.value.per_page,
        status: status
      }
    })
    
    if (res.code === 200 && res.success) {
      const newList = res.data.list || []
      courses.value = reset ? newList : [...courses.value, ...newList]
      
      pagination.value.total = res.data.total || 0
      pagination.value.total_pages = res.data.pages || 0
    } else {
      uni.showToast({
        title: res.message || '获取课程列表失败',
        icon: 'none'
      })
    }
  } catch (error) {
    console.error('获取课程列表失败:', error)
    uni.showToast({
      title: '获取课程列表失败，请稍后重试',
      icon: 'none'
    })
  } finally {
    loading.value = false
    
    // 停止下拉刷新
    uni.stopPullDownRefresh()
  }
}

// 切换标签页
const switchTab = (tab) => {
  activeTab.value = tab
  fetchCourses(true)
}

// 获取状态文本
const getStatusText = (status) => {
  switch (status) {
    case 'not_started':
      return '未开始'
    case 'learning':
      return '学习中'
    case 'completed':
      return '已完成'
    default:
      return '未知状态'
  }
}

// 获取当前标签页文本
const getTabText = () => {
  switch (activeTab.value) {
    case 'all':
      return ''
    case 'learning':
      return '学习中'
    case 'completed':
      return '已完成'
    default:
      return ''
  }
}

// 跳转到课程详情或学习页面
const navigateToCourse = (course) => {
  if (course.last_learn_lesson_id) {
    // 继续上次学习
    uni.navigateTo({
      url: `/pages/course/play/index?course_id=${course.id}&lesson_id=${course.last_learn_lesson_id}`
    })
  } else {
    // 查看课程详情
    uni.navigateTo({
      url: `/pages/course/detail?id=${course.id}`
    })
  }
}

// 页面加载
onLoad(() => {
  fetchCourses(true)
})

// 下拉刷新
onPullDownRefresh(() => {
  fetchCourses(true)
})

// 上拉加载更多
onReachBottom(() => {
  if (loading.value) return
  
  if (pagination.value.page < pagination.value.total_pages) {
    pagination.value.page++
    fetchCourses()
  }
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 30rpx;
}

.tab-section {
  display: flex;
  background-color: #fff;
  position: sticky;
  top: 0;
  z-index: 10;

  .tab-item {
    flex: 1;
    text-align: center;
    padding: 30rpx 0;
    font-size: 28rpx;
    color: #666;
    position: relative;

    &.active {
      color: #4A90E2;
      font-weight: bold;

      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60rpx;
        height: 4rpx;
        background-color: #4A90E2;
      }
    }
  }
}

.content-section {
  padding: 20rpx 30rpx;
}

.course-card {
  display: flex;
  background-color: #fff;
  border-radius: 20rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);

  .course-image {
    width: 200rpx;
    height: 200rpx;
    border-radius: 10rpx;
    background-color: #f0f0f0;
  }

  .course-info {
    flex: 1;
    margin-left: 20rpx;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    .course-name {
      font-size: 32rpx;
      font-weight: bold;
      color: #333;
      margin-bottom: 20rpx;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
}

.course-progress {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.progress-bar {
  flex: 1;
  height: 10rpx;
  background-color: #f0f0f0;
  border-radius: 10rpx;
  overflow: hidden;
  margin-right: 20rpx;
}

.progress-inner {
  height: 100%;
  background-color: #4A90E2;
  border-radius: 10rpx;
}

.progress-text {
  font-size: 24rpx;
  color: #4A90E2;
  width: 60rpx;
  text-align: right;
}

.course-stats {
  display: flex;
  align-items: center;
}

.stat-item {
  display: flex;
  align-items: center;
  margin-right: 30rpx;
}

.stat-text {
  font-size: 24rpx;
  color: #999;
  margin-left: 10rpx;
}

.course-status {
  font-size: 24rpx;
  margin-left: auto;
  padding: 4rpx 10rpx;
  border-radius: 4rpx;
}

.status-not_started {
  color: #999;
  background-color: #f5f5f5;
}

.status-learning {
  color: #4A90E2;
  background-color: rgba(74, 144, 226, 0.1);
}

.status-completed {
  color: #52c41a;
  background-color: rgba(82, 196, 26, 0.1);
}

.empty-content {
  padding: 100rpx 0;
  text-align: center;
}
</style> 