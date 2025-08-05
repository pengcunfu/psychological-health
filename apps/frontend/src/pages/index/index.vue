<template>
  <view class="container tab-page">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="logo">
        <view class="logo-icon">心</view>
        <view class="logo-text">心理健康</view>
      </view>
      <view class="search-bar" @click="navigateTo('/pages/search/index')">
        <u-icon name="search" size="22" color="#999"></u-icon>
        <text class="search-text">搜索咨询师、课程</text>
      </view>
      <view class="message-icon" @click="navigateTo('/pages/message/index')">
        <u-icon name="bell" size="22" color="#333"></u-icon>
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
          <u-icon name="arrow-right" size="16" color="#999"></u-icon>
        </view>
      </view>
      
      <scroll-view class="counselor-list" scroll-x="true" show-scrollbar="false" v-if="counselorList.length > 0">
        <view 
          class="counselor-card" 
          v-for="(item, index) in counselorList" 
          :key="index"
          @click="navigateTo(`/pages/counselor/detail/index?id=${item.id}`)"
        >
          <image class="counselor-avatar" :src="item.avatar || '/static/images/default-avatar.png'" mode="aspectFill"></image>
          <view class="counselor-info">
            <text class="counselor-name">{{ item.name }}</text>
            <text class="counselor-title">{{ item.title }}</text>
            <view class="counselor-rating">
              <u-icon name="star-fill" color="#ff9800" size="16"></u-icon>
              <text class="rating-text">{{ item.rating }} ({{ item.consultation_count }})</text>
            </view>
            <text class="counselor-price">¥{{ item.price }}<text class="price-unit">/次</text></text>
          </view>
        </view>
      </scroll-view>
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
          <u-icon name="arrow-right" size="16" color="#999"></u-icon>
        </view>
      </view>
      
      <view class="course-list" v-if="courseList.length > 0">
        <view 
          class="course-card" 
          v-for="(item, index) in courseList" 
          :key="index" 
          @click="navigateTo(`/pages/course/detail/index?id=${item.id}`)"
        >
          <image class="course-img" :src="item.cover_image || '/static/images/default-course.png'" mode="aspectFill"></image>
          <view class="course-info">
            <text class="course-name">{{ item.title }}</text>
            <view class="course-stats">
              <view class="course-rating">
                <u-icon name="star-fill" color="#ff9800" size="24"></u-icon>
                <text class="rating-text">{{ item.rating || '4.8' }}</text>
              </view>
              <text class="course-count">{{ item.student_count || 0 }}人学习</text>
            </view>
            <text class="course-price" v-if="item.price > 0">¥{{ item.price }}</text>
            <text class="course-free" v-else>免费</text>
          </view>
        </view>
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
          <u-icon name="arrow-right" size="16" color="#999"></u-icon>
        </view>
      </view>
      
      <view class="course-list" v-if="assessmentList.length > 0">
        <view 
          class="course-card" 
          v-for="(item, index) in assessmentList" 
          :key="index" 
          @click="navigateTo(`/pages/assessment/detail/index?id=${item.id}`)"
        >
          <image class="course-img" :src="item.cover || '/static/images/default-assessment.png'" mode="aspectFill"></image>
          <view class="course-info">
            <text class="course-name">{{ item.name }}</text>
            <view class="course-stats">
              <text class="course-count">时长约{{ item.duration || 5 }}分钟</text>
            </view>
            <text class="course-price" v-if="item.price > 0">¥{{ item.price }}</text>
            <text class="course-free" v-else>免费</text>
          </view>
        </view>
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

import TabBar from '@/components/TabBar/index.vue'
import SvgIcon from '@/components/SvgIcon/index.vue'

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
  flex-direction: row;
  width: 100%;
  white-space: nowrap;
  padding: 0 30rpx 0 0;
}

.counselor-card {
  flex: 0 0 280rpx;
  width: 280rpx;
  margin-right: 24rpx;
  border-radius: 16rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.05);
  background-color: #fff;
  overflow: hidden;
  display: inline-block;
  vertical-align: top;
}

.counselor-card:last-child {
  margin-right: 30rpx;
}

.counselor-avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  margin: 20rpx auto 16rpx auto;
  display: block;
}

.counselor-info {
  padding: 0 16rpx 20rpx 16rpx;
  text-align: center;
}

.counselor-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

.counselor-title {
  font-size: 24rpx;
  color: #666;
  margin-bottom: 8rpx;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

.counselor-rating {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  color: #ff9800;
  margin-bottom: 8rpx;
}

.rating-text {
  margin-left: 6rpx;
  font-size: 22rpx;
}

.counselor-price {
  font-size: 24rpx;
  color: #ff4d4f;
  font-weight: bold;
}

.price-unit {
  font-size: 20rpx;
  color: #999;
  font-weight: normal;
}

// 课程列表样式
.course-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.course-card {
  display: flex;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.05);
  background-color: #fff;
}

.course-img {
  width: 240rpx;
  height: 160rpx;
}

.course-info {
  flex: 1;
  padding: 20rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.course-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.course-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8rpx;
}

.course-rating {
  display: flex;
  align-items: center;
  font-size: 24rpx;
  color: #ff9800;
}

.course-count {
  font-size: 24rpx;
  color: #999;
}

.course-price {
  font-size: 28rpx;
  color: #ff4d4f;
  font-weight: bold;
}

.course-free {
  font-size: 28rpx;
  color: #52c41a;
  font-weight: bold;
}
</style>
