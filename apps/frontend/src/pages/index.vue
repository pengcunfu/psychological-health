<template>
  <view class="container tab-page">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="logo">
        <view class="logo-icon">心</view>
        <view class="logo-text">美光心理</view>
      </view>
      <view class="search-bar" @click="navigateTo('/pages/search')">
        <up-icon name="search" size="22" color="#999"></up-icon>
        <text class="search-text">搜索咨询师、课程</text>
      </view>
      <view class="message-icon" @click="navigateTo('/pages/message')">
        <up-icon name="bell" size="22" color="#333"></up-icon>
        <view class="message-dot"></view>
      </view>
    </view>

    <!-- 轮播图 -->
    <view class="banner">
      <swiper 
        v-if="bannerList.length > 0"
        :autoplay="true"
        :interval="3000"
        :duration="300"
        :circular="true"
        indicator-dots
        indicator-active-color="#4A90E2"
        indicator-color="rgba(255, 255, 255, 0.5)"
        class="swiper-container"
        @change="handleBannerChange"
      >
        <swiper-item 
          v-for="(item, index) in bannerList" 
          :key="item.id || index"
          @tap="() => handleBannerClick(index)"
        >
          <view class="swiper-item">
            <image 
              :src="item.image_url" 
              mode="aspectFill"
              class="swiper-image"
            />
            <view v-if="item.title" class="swiper-title">{{ item.title }}</view>
          </view>
        </swiper-item>
      </swiper>
      <view v-else class="banner-empty">
        <u-empty 
          text="暂无轮播图"
          icon="https://cdn.uviewui.com/uview/empty/list.png"
          iconSize="80"
          textSize="12"
          textColor="#999999"
          marginTop="50"
        />
      </view>
    </view>

    <!-- 功能导航 -->
    <view class="nav-grid">
      <view class="nav-item" v-for="(item, index) in menuList" :key="index" @click="navigateTo(item.url)">
        <view class="nav-icon" :style="{ backgroundColor: item.bgColor }">
          <SvgIcon 
            :name="item.iconName" 
            path="index"
            :size="48"
            :color="item.color"
            :fallbackIcon="item.fallbackIcon"
          />
        </view>
        <text class="nav-text">{{ item.name }}</text>
      </view>
    </view>

    <!-- 推荐咨询师 -->
    <view class="section">
      <view class="section-header">
        <view class="section-title">
          <view class="section-title-icon"></view>
          推荐咨询师
        </view>
        <view class="section-more" @click="navigateTo('/pages/counselor/index')">
          <text>查看全部</text>
          <up-icon name="arrow-right" size="16" color="#999"></up-icon>
        </view>
      </view>
      
      <view class="counselor-list" v-if="counselorList.length > 0">
        <CounselorCard 
          v-for="(item, index) in counselorList" 
          :key="index"
          :counselor="item"
          @click="handleCounselorClick"
        />
      </view>
      <view v-else class="section-empty">
        <u-empty 
          text="暂无推荐咨询师"
          icon="https://cdn.uviewui.com/uview/empty/list.png"
          iconSize="100"
          textSize="14"
          textColor="#999999"
          marginTop="40"
        />
      </view>
    </view>

    <!-- 推荐课程 -->
    <view class="section">
      <view class="section-header">
        <view class="section-title">
          <view class="section-title-icon"></view>
          推荐课程
        </view>
        <view class="section-more" @click="navigateTo('/pages/course/index')">
          <text>查看全部</text>
          <up-icon name="arrow-right" size="16" color="#999"></up-icon>
        </view>
      </view>
      
      <view class="course-list" v-if="courseList.length > 0">
        <CourseCard 
          v-for="(item, index) in courseList" 
          :key="index"
          :course="item"
          @click="handleCourseClick"
        />
      </view>
      <view v-else class="section-empty">
        <u-empty 
          text="暂无推荐课程"
          icon="https://cdn.uviewui.com/uview/empty/list.png"
          iconSize="100"
          textSize="14"
          textColor="#999999"
          marginTop="40"
        />
      </view>
    </view>

    <!-- 心理测评推荐 -->
    <view class="section">
      <view class="section-header">
        <view class="section-title">
          <view class="section-title-icon"></view>
          心理测评
        </view>
        <view class="section-more" @click="navigateTo('/pages/assessment/index')">
          <text>查看全部</text>
          <up-icon name="arrow-right" size="16" color="#999"></up-icon>
        </view>
      </view>
      
      <view class="assessment-list" v-if="assessmentList.length > 0">
        <AssessmentCard 
          v-for="(item, index) in assessmentList" 
          :key="index"
          :assessment="item"
          @click="handleAssessmentClick"
        />
      </view>
      <view v-else class="section-empty">
        <u-empty 
          text="暂无心理测评"
          icon="https://cdn.uviewui.com/uview/empty/list.png"
          iconSize="100"
          textSize="14"
          textColor="#999999"
          marginTop="40"
        />
      </view>
    </view>

    <!-- 自定义TabBar -->
    <TabBar />
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { bannerAPI } from '@/api/banner'
import { counselorAPI } from '@/api/counselor'
import { courseAPI } from '@/api/course'
import { preprocessUrl, handleUrlNavigation, navigateTo } from '@/utils/link'

import TabBar from '@/components/TabBar.vue'
import SvgIcon from '@/components/SvgIcon.vue'
import CounselorCard from '@/components/CounselorCard.vue'
import CourseCard from '@/components/CourseCard.vue'
import AssessmentCard from '@/components/AssessmentCard.vue'

const userStore = useUserStore()

// 用户信息
const userInfo = computed(() => {
  return {
    ...userStore.userInfo,
    isLoggedIn: userStore.isLoggedIn
  }
})

// 轮播图数据
const bannerList = ref([])

// 菜单数据 - 使用本地SVG图标和uview图标作为备用
const menuList = ref([
  { 
    name: '咨询预约', 
    color: '#1890ff', 
    bgColor: '#e6f7ff',
    url: '/pages/counselor/index',
    iconName: 'counselor',
    fallbackIcon: 'calendar-fill'
  },
  { 
    name: '课程学习', 
    color: '#eb2f96', 
    bgColor: '#fff0f6',
    url: '/pages/course/index',
    iconName: 'course',
    fallbackIcon: 'play-circle-fill'
  },
  { 
    name: '心理测评', 
    color: '#52c41a', 
    bgColor: '#f6ffed',
    url: '/pages/assessment/index',
    iconName: 'evaluate',
    fallbackIcon: 'checkmark-circle-fill'
  },
  { 
    name: '互动社区', 
    color: '#fa8c16', 
    bgColor: '#fff7e6',
    url: '/pages/community/index',
    iconName: 'community',
    fallbackIcon: 'account-fill'
  }
])

// 咨询师数据
const counselorList = ref([])

// 课程数据
const courseList = ref([])

// 测评数据
const assessmentList = ref([])

// 获取咨询师列表
const fetchCounselors = async () => {
  try {
    const res = await counselorAPI.getCounselors({
      page: 1,
      per_page: 5
    })
    
    if (res.code === 200 && res.success && res.data) {
      counselorList.value = res.data.list || []
    } else {
      counselorList.value = []
    }
  } catch (error) {
    console.error('获取咨询师列表失败:', error)
    counselorList.value = []
  }
}

// 获取课程列表
const fetchCourses = async () => {
  try {
    const res = await courseAPI.getCourses({
      page: 1,
      per_page: 4
    })
    
    console.log('课程API响应:', res)
    
    if (res.code === 200 && res.success && res.data && res.data.list) {
      // 处理课程数据，确保rating有默认值
      courseList.value = res.data.list.map(course => ({
        ...course,
        rating: course.rating || 4.8, // 如果rating为0，使用默认值4.8
        student_count: course.student_count || 0
      }))
      console.log('处理后的课程列表:', courseList.value)
    } else {
      console.log('API返回数据格式异常')
      courseList.value = []
    }
  } catch (error) {
    console.error('获取课程列表失败:', error)
    courseList.value = []
  }
}

// 获取轮播图数据
const fetchBanners = async () => {
  try {
    const res = await bannerAPI.getBanners({
      page: 1,
      per_page: 10
    })
    
    if (res.code === 200 && res.success && res.data) {
      bannerList.value = res.data.list || []
    } else {
      bannerList.value = []
    }
  } catch (error) {
    console.error('获取轮播图失败:', error)
    bannerList.value = []
  }
}

// 轮播图点击处理
const handleBannerClick = (index) => {
  console.log('轮播图点击事件触发，索引:', index)
  console.log('轮播图数据:', bannerList.value)
  
  const banner = bannerList.value[index]
  console.log('当前点击的轮播图:', banner)
  
  if (banner && banner.link_url) {
    console.log('准备跳转到:', banner.link_url)
    
    // 预处理链接URL
    const processedUrl = preprocessUrl(banner.link_url)
    console.log('处理后的URL:', processedUrl)
    
    // 判断链接类型并执行相应的跳转逻辑
    handleUrlNavigation(processedUrl, banner.title || '加载中...')
  } else {
    console.log('轮播图数据无效或缺少链接')
    uni.showToast({
      title: '链接无效',
      icon: 'none'
    })
  }
}

// 轮播图变化处理
const handleBannerChange = (index) => {
  // 轮播图变化处理
}

// 咨询师卡片点击处理
const handleCounselorClick = (counselor) => {
  console.log('咨询师卡片点击:', counselor)
}

// 课程卡片点击处理
const handleCourseClick = (course) => {
  console.log('课程卡片点击:', course)
}

// 心理测评卡片点击处理
const handleAssessmentClick = (assessment) => {
  console.log('心理测评卡片点击:', assessment)
}




const onImageLoad = (e) => {
  // 图片加载成功
}

const onImageError = (e) => {
  // 图片加载失败
}


onLoad(() => {
  fetchBanners()
  fetchCounselors()
  fetchCourses()
})

onShow(() => {
  // 每次显示页面时更新用户信息
  if (userStore.isLoggedIn) {
    userStore.getUserInfo()
  }
  
  // 触发tabbar页面显示事件
  uni.$emit('tabBarPageShow')
})
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

// 顶部导航样式
.header {
  padding: 30rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff;
  border-bottom: 2rpx solid #f0f0f0;
}

.logo {
  display: flex;
  align-items: center;
}

.logo-icon {
  width: 64rpx;
  height: 64rpx;
  background-color: #4A90E2;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 32rpx;
  font-weight: bold;
  margin-right: 16rpx;
}

.logo-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.search-bar {
  flex: 1;
  height: 72rpx;
  background-color: #f5f5f5;
  border-radius: 36rpx;
  margin: 0 20rpx;
  display: flex;
  align-items: center;
  padding: 0 30rpx;
}

.search-text {
  font-size: 28rpx;
  color: #999;
  margin-left: 16rpx;
}

.message-icon {
  position: relative;
}

.message-dot {
  position: absolute;
  top: 0;
  right: 0;
  width: 16rpx;
  height: 16rpx;
  background-color: #ff4d4f;
  border-radius: 50%;
}

// 轮播图样式
.banner {
  height: 320rpx;
}

.swiper-container {
  height: 320rpx;
}

.swiper-item {
  width: 100%;
  height: 100%;
  position: relative;
}

.swiper-image {
  width: 100%;
  height: 100%;
}

.swiper-title {
  position: absolute;
  bottom: 20rpx;
  left: 20rpx;
  right: 20rpx;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 10rpx 20rpx;
  border-radius: 10rpx;
  font-size: 28rpx;
  text-align: center;
}

.banner-loading {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  color: #999;
  font-size: 28rpx;
}

.banner-empty {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fafafa;
  border-radius: 12rpx;
}

// 功能导航样式
.nav-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  padding: 40rpx 20rpx;
  background-color: #fff;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx;
}

.nav-icon {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16rpx;
}

.nav-text {
  font-size: 24rpx;
  color: #333;
}

// 区块样式
.section {
  margin-top: 20rpx;
  background-color: #fff;
  padding: 30rpx;
}

.section:last-of-type {
  margin-bottom: 120rpx; /* 为TabBar留出空间 */
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
}

.section-title-icon {
  width: 8rpx;
  height: 32rpx;
  background-color: #4A90E2;
  margin-right: 16rpx;
  border-radius: 4rpx;
}

.section-more {
  font-size: 24rpx;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8rpx;
  cursor: pointer;
  
  text {
    font-size: 24rpx;
    color: #999;
  }
}

.section-empty {
  height: 200rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fafafa;
  border-radius: 12rpx;
  margin: 20rpx 0;
}

// 咨询师列表样式
.counselor-list {
  display: flex;
  flex-direction: column;
  width: 100%;
}

// 课程列表样式
.course-list {
  display: flex;
  flex-direction: column;
}

// 心理测评列表样式
.assessment-list {
  display: flex;
  flex-direction: column;
}
</style>
