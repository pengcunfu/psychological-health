<template>
  <view class="container tab-page">
    <!-- 顶部导航栏 -->
    <!-- <Navbar title="课程学习" :showLeft="false" :showRight="true" rightIcon="search" @rightClick="handleSearchClick" /> -->

    <!-- 标签栏 -->
    <view class="tabs">
      <view class="tab active">全部课程</view>
      <view class="tab" @click="navigateToMyCourse">我的课程</view>
    </view>

    <!-- 分类列表 -->
    <view class="category-list">
      <view class="category-item" :class="{ active: activeCategory === 'all' }" @click="setCategory('all')">
        全部
      </view>
      <view class="category-item" :class="{ active: activeCategory === category.id }" v-for="category in categories"
        :key="category.id" @click="setCategory(category.id)">
        {{ category.name }}
      </view>
    </view>

    <!-- 课程列表 -->
    <view class="course-list">
      <CourseCard v-for="(item, index) in courseList" :key="item.id || index" :course="item"
        @click="handleCourseClick" />
    </view>

    <!-- 空状态 -->
    <view v-if="!loading && courseList.length === 0" class="empty-state">
      <view class="empty-content">
        <u-icon name="search" size="60" color="#ccc"></u-icon>
        <text class="empty-title">暂无课程</text>
        <text class="empty-subtitle">试试切换其他分类</text>
        <u-button text="重新加载" type="primary" size="normal" @click="fetchCourses(true)" :customStyle="{
          marginTop: '30rpx',
          width: '160rpx',
          borderRadius: '22rpx',
          background: '#4A90E2'
        }"></u-button>
      </view>
    </view>

    <!-- 加载更多 -->
    <view class="load-more-container">
      <u-loadmore :status="loadMoreStatus" @loadmore="loadMore" :loading-text="'正在加载更多课程...'" :loadmore-text="'上拉加载更多'"
        :nomore-text="'已加载全部课程'" icon-size="20" :margin-top="20" :margin-bottom="20" />
    </view>

    <!-- 自定义TabBar -->
    <!-- <TabBar2 /> -->
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { onLoad, onReachBottom } from '@dcloudio/uni-app'
import { courseAPI } from '@/api/course'
import CourseCard from '@/components/CourseCard.vue'
import Navbar from '@/components/Navbar.vue'
// import TabBar2 from '@/components/TabBar2.vue'

// 搜索关键词
const searchKeyword = ref('')

// 当前选中的分类
const activeCategory = ref('all')

// 分类列表
const categories = ref([
  { id: 'emotion', name: '情绪管理' },
  { id: 'relationship', name: '人际关系' },
  { id: 'workplace', name: '职场压力' },
  { id: 'meditation', name: '冥想放松' },
  { id: 'youth', name: '青少年心理' },
  { id: 'love', name: '婚恋情感' }
])

// 课程列表
const courseList = ref([])

// 加载状态
const loading = ref(false)
const loadMoreStatus = ref('loadmore')

// 分页信息
const pagination = reactive({
  page: 1,
  per_page: 10,
  total: 0,
  total_pages: 0
})

// 返回上一页
const goBack = () => {
  uni.navigateBack()
}

// 搜索按钮点击
const handleSearchClick = () => {
  uni.navigateTo({
    url: '/pages/search'
  })
}

// 跳转到我的课程页面
const navigateToMyCourse = () => {
  uni.navigateTo({
    url: '/pages/profile/my-course'
  })
}

// 设置分类
const setCategory = (categoryId) => {
  activeCategory.value = categoryId
  fetchCourses(true)
}

// 获取课程列表
const fetchCourses = async (reset = false) => {
  if (reset) {
    pagination.page = 1
    courseList.value = []
  }

  loading.value = true
  loadMoreStatus.value = 'loading'

  try {
    // 构建查询参数
    const params = {
      page: pagination.page,
      per_page: pagination.per_page
    }

    // 添加搜索关键词
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }

    // 添加分类筛选
    if (activeCategory.value !== 'all') {
      params.category = activeCategory.value
    }


    const res = await courseAPI.getCourses(params)


    if (res.code === 200 && res.success && res.data) {
      // 处理课程数据
      let newList = res.data.list || []

      // 数据处理和字段映射
      newList = newList.map(item => {
        const processedItem = {
          ...item,
          // 字段映射和默认值处理
          id: item.id,
          name: item.name || '课程名称',
          cover_image: item.cover_image || '/static/images/default-course.png',
          teacher_name: item.teacher_name || '未知讲师',
          teacher_title: item.teacher_title || '心理咨询师',
          rating: parseFloat(item.rating) || 4.8,
          student_count: parseInt(item.student_count) || 0,
          price: parseFloat(item.price) || 0,
          lesson_count: parseInt(item.lesson_count) || 0,
          duration: item.duration || '60分钟',
          description: item.description || '专业心理课程，帮助您提升心理健康水平'
        }
        return processedItem
      })

      // 更新列表
      courseList.value = reset ? newList : [...courseList.value, ...newList]

      // 更新分页信息
      pagination.total = res.data.total || 0
      pagination.total_pages = res.data.pages || Math.ceil((res.data.total || 0) / pagination.per_page)

      // 更新加载更多状态
      loadMoreStatus.value = pagination.page >= pagination.total_pages ? 'nomore' : 'loadmore'

    } else {

      // 设置为空数组，显示空状态
      if (reset) {
        courseList.value = []
      }
      loadMoreStatus.value = 'nomore'
    }
  } catch (error) {

    // 设置为空数组，显示空状态
    if (reset) {
      courseList.value = []
    }

    loadMoreStatus.value = 'loadmore'
    uni.showToast({
      title: '获取课程列表失败，请稍后重试',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 处理课程卡片点击
const handleCourseClick = (course) => {
  uni.navigateTo({
    url: `/pages/course/detail?id=${course.id}`
  })
}

// 跳转到详情页
const navigateToDetail = (id) => {
  uni.navigateTo({
    url: `/pages/course/detail?id=${id}`
  })
}

// 加载更多
const loadMore = () => {
  if (loadMoreStatus.value === 'loadmore') {
    pagination.page++
    fetchCourses()
  }
}

// 页面加载
onLoad(() => {
  fetchCourses(true)
})

// 下拉加载更多
onReachBottom(() => {
  loadMore()
})
</script>

<style lang="scss" scoped>
// SCSS变量
$primary-color: #4A90E2;
$secondary-color: #1890ff;
$text-color: #333;
$text-light: #666;
$text-lighter: #999;
$bg-color: #f5f7fa;
$white: #fff;
$border-color: #f0f0f0;
$shadow-light: rgba(0, 0, 0, 0.05);
$shadow-medium: rgba(0, 0, 0, 0.08);
$shadow-strong: rgba(0, 0, 0, 0.15);

.container {
  min-height: 100vh;
  background: $bg-color;
  padding-bottom: 120rpx;
  /* 为TabBar留出空间 */
}

// 顶部导航栏样式已由Navbar组件提供

// 标签栏
.tabs {
  display: flex;
  background: $white;
  border-bottom: 1rpx solid $border-color;
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 2rpx 8rpx $shadow-light;

  .tab {
    flex: 1;
    text-align: center;
    padding: 28rpx 0;
    font-size: 30rpx;
    color: $text-light;
    position: relative;
    transition: color 0.3s ease;

    &:active {
      background-color: rgba($primary-color, 0.05);
    }

    &.active {
      color: $primary-color;
      font-weight: bold;

      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 50rpx;
        height: 6rpx;
        background: linear-gradient(90deg, $primary-color, $secondary-color);
        border-radius: 3rpx;
        animation: slideIn 0.3s ease;
      }
    }
  }
}

@keyframes slideIn {
  from {
    width: 0;
  }

  to {
    width: 50rpx;
  }
}

// 分类列表
.category-list {
  display: flex;
  overflow-x: auto;
  padding: 30rpx 30rpx 20rpx;
  background: $white;
  scrollbar-width: none;
  /* Firefox */
  gap: 16rpx;
  border-bottom: 1rpx solid $border-color;

  &::-webkit-scrollbar {
    display: none;
    /* Chrome, Safari, Edge */
  }

  .category-item {
    flex: 0 0 auto;
    padding: 16rpx 28rpx;
    background: #f8f9fa;
    border-radius: 40rpx;
    font-size: 26rpx;
    color: $text-light;
    white-space: nowrap;
    border: 2rpx solid transparent;
    transition: all 0.3s ease;
    box-shadow: 0 2rpx 6rpx $shadow-light;

    &:active {
      transform: scale(0.95);
    }

    &.active {
      background: linear-gradient(135deg, #e6f7ff, #f0f9ff);
      color: $primary-color;
      border-color: #b3d8ff;
      font-weight: 600;
      box-shadow: 0 4rpx 12rpx rgba($primary-color, 0.15);
    }
  }
}

// 课程列表
.course-list {
  margin-top: 10rpx;
}

// 空状态
.empty-state {
  padding: 120rpx 40rpx;
  text-align: center;

  .empty-content {
    background: $white;
    border-radius: 20rpx;
    padding: 80rpx 40rpx;
    box-shadow: 0 8rpx 24rpx $shadow-medium;
    border: 1rpx solid $border-color;

    .empty-title {
      font-size: 32rpx;
      color: $text-color;
      margin: 30rpx 0 12rpx;
      display: block;
      font-weight: 600;
    }

    .empty-subtitle {
      font-size: 26rpx;
      color: $text-lighter;
      display: block;
      line-height: 1.4;
    }
  }
}

// 加载更多
.load-more-container {
  padding: 20rpx 30rpx 40rpx;
  margin-top: 20rpx;
}
</style>