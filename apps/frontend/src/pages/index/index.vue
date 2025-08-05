<template>
  <view class="container tab-page">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="logo">
        <view class="logo-icon">心</view>
        <view class="logo-text">心理健康</view>
      </view>
      <view class="search-bar" @click="navigateTo('/pages/search/index')">
        <u-icon name="search" size="32" color="#999"></u-icon>
        <text class="search-text">搜索咨询师、课程</text>
      </view>
      <view class="message-icon" @click="navigateTo('/pages/message/index')">
        <u-icon name="bell" size="48" color="#333"></u-icon>
        <view class="message-dot"></view>
      </view>
    </view>

    <!-- 轮播图 -->
    <view class="banner">
      <swiper class="swiper" autoplay :interval="3000" :duration="300" circular indicator-dots v-if="bannerList.length > 0">
        <swiper-item v-for="(item, index) in bannerList" :key="item.id || index" @click="handleBannerClick(item)">
          <image 
            :src="item.image_url" 
            class="banner-image" 
            mode="aspectFill"
            @error="onImageError"
            @load="onImageLoad"
          ></image>
          <view v-if="item.title" class="banner-title">{{ item.title }}</view>
        </swiper-item>
      </swiper>
      <view v-else class="banner-loading">
        <text>轮播图加载中...</text>
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
        <text class="section-more" @click="navigateTo('/pages/counselor/index')">
          查看全部
          <u-icon name="arrow-right" size="24" color="#999"></u-icon>
        </text>
      </view>
      
      <scroll-view class="counselor-list" scroll-x="true" show-scrollbar="false">
        <view 
          class="counselor-card" 
          v-for="(item, index) in counselorList" 
          :key="index"
          @click="navigateTo(`/pages/counselor/detail/index?id=${item.id}`)"
        >
          <image class="counselor-img" :src="item.avatar || '/static/images/default-avatar.png'" mode="aspectFill"></image>
          <view class="counselor-info">
            <text class="counselor-name">{{ item.name }}</text>
            <text class="counselor-title">{{ item.title }}</text>
            <view class="counselor-rating">
              <u-icon name="star-fill" color="#ff9800" size="24"></u-icon>
              <text class="rating-text">{{ item.rating }} ({{ item.consultation_count }})</text>
            </view>
            <text class="counselor-price">¥{{ item.price }}<text class="price-unit">/次</text></text>
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- 推荐课程 -->
    <view class="section">
      <view class="section-header">
        <view class="section-title">
          <view class="section-title-icon"></view>
          推荐课程
        </view>
        <text class="section-more" @click="navigateTo('/pages/course/index')">
          查看全部
          <u-icon name="arrow-right" size="24" color="#999"></u-icon>
        </text>
      </view>
      
      <view class="course-list">
        <view 
          class="course-card" 
          v-for="(item, index) in courseList" 
          :key="index" 
          @click="navigateTo(`/pages/course/detail/index?id=${item.id}`)"
        >
          <image class="course-img" :src="item.cover || '/static/images/default-course.png'" mode="aspectFill"></image>
          <view class="course-info">
            <text class="course-name">{{ item.name }}</text>
            <view class="course-stats">
              <view class="course-rating">
                <u-icon name="star-fill" color="#ff9800" size="24"></u-icon>
                <text class="rating-text">{{ item.rating || '4.8' }}</text>
              </view>
              <text class="course-count">{{ item.sales || 0 }}人学习</text>
            </view>
            <text class="course-price" v-if="item.price > 0">¥{{ item.price }}</text>
            <text class="course-free" v-else>免费</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 心理测评推荐 -->
    <view class="section">
      <view class="section-header">
        <view class="section-title">
          <view class="section-title-icon"></view>
          心理测评
        </view>
        <text class="section-more" @click="navigateTo('/pages/assessment/index')">
          查看全部
          <u-icon name="arrow-right" size="24" color="#999"></u-icon>
        </text>
      </view>
      
      <view class="course-list">
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
    </view>

    <!-- 自定义TabBar -->
    <TabBar />
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { request } from '@/utils/request'
import { bannerAPI } from '@/api/banner'
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
const assessmentList = ref([
  {
    id: 1,
    name: '抑郁症筛查量表（PHQ-9）',
    duration: 5,
    price: 0,
    cover: 'https://via.placeholder.com/240x160/4A90E2/FFFFFF?text=抑郁测试'
  },
  {
    id: 2,
    name: '广泛性焦虑障碍量表（GAD-7）',
    duration: 3,
    price: 0,
    cover: 'https://via.placeholder.com/240x160/52C41A/FFFFFF?text=焦虑测试'
  },
  {
    id: 3,
    name: '大五人格测试（Big Five）',
    duration: 15,
    price: 19,
    cover: 'https://via.placeholder.com/240x160/FA8C16/FFFFFF?text=人格测试'
  }
])

// 获取咨询师列表
const fetchCounselors = async () => {
  try {
    const res = await request({
      url: '/counselor',
      method: 'GET',
      data: {
        page: 1,
        per_page: 5
      }
    })
    
    if (res.code === 200 && res.success) {
      counselorList.value = res.data.counselors || []
    }
  } catch (error) {
    console.error('获取咨询师列表失败:', error)
    // 模拟数据
    counselorList.value = [
      {
        id: 1,
        name: '张医生',
        title: '心理咨询师 · 婚恋情感',
        rating: 4.9,
        consultation_count: 128,
        price: 300,
        avatar: 'https://via.placeholder.com/280x280/4A90E2/FFFFFF?text=张医生'
      },
      {
        id: 2,
        name: '李医生',
        title: '心理咨询师 · 青少年心理',
        rating: 4.8,
        consultation_count: 96,
        price: 280,
        avatar: 'https://via.placeholder.com/280x280/52C41A/FFFFFF?text=李医生'
      },
      {
        id: 3,
        name: '王医生',
        title: '心理咨询师 · 职场压力',
        rating: 4.7,
        consultation_count: 85,
        price: 320,
        avatar: 'https://via.placeholder.com/280x280/FA8C16/FFFFFF?text=王医生'
      },
      {
        id: 4,
        name: '赵医生',
        title: '心理咨询师 · 抑郁焦虑',
        rating: 4.9,
        consultation_count: 142,
        price: 350,
        avatar: 'https://via.placeholder.com/280x280/EB2F96/FFFFFF?text=赵医生'
      }
    ]
  }
}

// 获取课程列表
const fetchCourses = async () => {
  try {
    const res = await request({
      url: '/course',
      method: 'GET',
      data: {
        page: 1,
        per_page: 4
      }
    })
    
    if (res.code === 200 && res.success) {
      courseList.value = res.data.list || []
    }
  } catch (error) {
    console.error('获取课程列表失败:', error)
    // 模拟数据
    courseList.value = [
      {
        id: 1,
        name: '情绪管理：如何应对日常压力与焦虑',
        rating: 4.8,
        sales: 2345,
        price: 99,
        cover: 'https://via.placeholder.com/240x160/4A90E2/FFFFFF?text=情绪管理'
      },
      {
        id: 2,
        name: '人际关系：构建健康社交圈的技巧',
        rating: 4.7,
        sales: 1876,
        price: 89,
        cover: 'https://via.placeholder.com/240x160/52C41A/FFFFFF?text=人际关系'
      },
      {
        id: 3,
        name: '自我成长：发现内在力量的旅程',
        rating: 4.9,
        sales: 2103,
        price: 129,
        cover: 'https://via.placeholder.com/240x160/FA8C16/FFFFFF?text=自我成长'
      },
      {
        id: 4,
        name: '冥想入门：21天正念练习指南',
        rating: 4.6,
        sales: 3421,
        price: 0,
        cover: 'https://via.placeholder.com/240x160/EB2F96/FFFFFF?text=冥想入门'
      }
    ]
  }
}

// 获取轮播图数据
const fetchBanners = async () => {
  try {
    const res = await bannerAPI.getBanners({
      page: 1,
      per_page: 10
    })
    
    if (res.code === 200 && res.success) {
      console.log(res.data.list)
      
      // 处理图片URL，添加服务器地址前缀
      const processedBanners = res.data.list.map(banner => ({
        ...banner,
        image_url: banner.image_url.startsWith('http') 
          ? banner.image_url 
          : `http://localhost:5000${banner.image_url}`
      }))
      
      bannerList.value = processedBanners.length > 0 ? processedBanners : getDefaultBanners()
    } else {
      bannerList.value = getDefaultBanners()
    }
  } catch (error) {
    console.error('获取轮播图失败:', error)
    bannerList.value = getDefaultBanners()
  }
}

// 获取默认轮播图数据
const getDefaultBanners = () => {
  return [
    { 
      id: 'default-1',
      title: '心理健康服务',
      image_url: 'https://via.placeholder.com/750x320/4A90E2/FFFFFF?text=心理健康服务',
      link_url: '/pages/counselor/index',
      sort_order: 0,
      status: 1
    },
    { 
      id: 'default-2',
      title: '专业咨询服务',
      image_url: 'https://via.placeholder.com/750x320/52c41a/FFFFFF?text=专业咨询服务',
      link_url: '/pages/course/index',
      sort_order: 1,
      status: 1
    },
    { 
      id: 'default-3',
      title: '心灵成长课程',
      image_url: 'https://via.placeholder.com/750x320/faad14/FFFFFF?text=心灵成长课程',
      link_url: '/pages/assessment/index',
      sort_order: 2,
      status: 1
    }
  ]
}

// 轮播图点击处理
const handleBannerClick = (banner) => {
  if (banner.link_url) {
    // 判断是否是外部链接
    if (banner.link_url.startsWith('http')) {
      // 外部链接，在webview中打开
      uni.navigateTo({
        url: `/pages/webview/index?url=${encodeURIComponent(banner.link_url)}&title=${encodeURIComponent(banner.title || '')}`
      })
    } else {
      // 内部页面跳转
      uni.navigateTo({ url: banner.link_url })
    }
  }
}

// 页面跳转
const navigateTo = (url) => {
  uni.navigateTo({ url })
}


const onImageLoad = (e) => {
  console.log('轮播图图片加载成功:', e)
}

// 测试图标加载
const onImageError = (e) => {
  console.error('图标加载失败:', e)
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

.swiper {
  width: 100%;
  height: 100%;
}

.banner-image {
  width: 100%;
  height: 100%;
}

.banner-title {
  position: absolute;
  bottom: 20rpx;
  left: 20rpx;
  right: 20rpx;
  color: #fff;
  font-size: 28rpx;
  font-weight: bold;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.5);
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.3));
  padding: 20rpx 20rpx 10rpx;
  border-radius: 8rpx;
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
}

// 咨询师列表样式
.counselor-list {
  display: flex;
  white-space: nowrap;
}

.counselor-card {
  flex: 0 0 auto;
  width: 280rpx;
  margin-right: 24rpx;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.05);
  background-color: #fff;
}

.counselor-img {
  width: 100%;
  height: 280rpx;
}

.counselor-info {
  padding: 16rpx;
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
  font-size: 24rpx;
  color: #ff9800;
  margin-bottom: 8rpx;
}

.rating-text {
  margin-left: 8rpx;
}

.counselor-price {
  font-size: 24rpx;
  color: #ff4d4f;
}

.price-unit {
  font-size: 20rpx;
  color: #999;
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
