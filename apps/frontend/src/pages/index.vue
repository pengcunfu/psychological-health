<template>
  <view class="container tab-page">
    <!-- 顶部导航 -->
    <view class="header-wrapper">
      <view class="header-content">
        <view class="search-bar" @click="handleSearchBarClick">
          <SvgIcon name="search" :size="22" color="#999" />
          <text class="search-text">搜索咨询师、课程</text>
        </view>
      </view>
    </view>

    <!-- 轮播图 -->
    <Banner :bannerData="bannerList" @bannerClick="handleBannerClick" @bannerChange="handleBannerChange"
      @imageLoad="onImageLoad" @imageError="onImageError" />

    <!-- 功能导航 -->
    <NavigationMenu @menuClick="handleMenuClick" />

    <!-- 推荐咨询师 -->
    <view class="section">
      <view class="section-header">
        <view class="section-title">
          <view class="section-title-icon"></view>
          推荐咨询师
        </view>
        <view class="section-more" @click="navigateTo('/pages/counselor/index')">
          <text>查看全部</text>
          <SvgIcon name="arrow-right" :size="24" color="#999" :offsetY="-1" :offsetX="1"></SvgIcon>
        </view>
      </view>

      <view class="counselor-list" v-if="counselorList.length > 0">
        <CounselorCard v-for="(item, index) in counselorList" :key="index" :counselor="item"
          @click="handleCounselorClick" />
      </view>
      <view v-else class="section-empty">
        <up-empty text="暂无推荐咨询师" icon="https://cdn.uviewui.com/uview/empty/list.png" iconSize="100" textSize="14"
          textColor="#999999" marginTop="40" />
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
          <SvgIcon name="arrow-right" :size="24" color="#999" :offsetY="-1" :offsetX="1"></SvgIcon>
        </view>
      </view>

      <view class="course-list" v-if="courseList.length > 0">
        <CourseCard v-for="(item, index) in courseList" :key="index" :course="item" @click="handleCourseClick" />
      </view>
      <view v-else class="section-empty">
        <up-empty text="暂无推荐课程" icon="https://cdn.uviewui.com/uview/empty/list.png" iconSize="100" textSize="14"
          textColor="#999999" marginTop="40" />
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
          <SvgIcon name="arrow-right" :size="24" color="#999" :offsetY="-1" :offsetX="1"></SvgIcon>
        </view>
      </view>

      <view class="assessment-list" v-if="assessmentList.length > 0">
        <AssessmentCard v-for="(item, index) in assessmentList" :key="index" :assessment="item"
          @click="handleAssessmentClick" />
      </view>
      <view v-else class="section-empty">
        <up-empty text="暂无心理测评" icon="https://cdn.uviewui.com/uview/empty/list.png" iconSize="100" textSize="14"
          textColor="#999999" marginTop="40" />
      </view>
    </view>

    <!-- TabBar -->
    <!-- <TabBar2 /> -->
  </view>
</template>

<script setup>
import { ref, computed, onMounted, getCurrentInstance } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { bannerAPI } from '@/api/banner'
import { counselorAPI } from '@/api/counselor'
import { courseAPI } from '@/api/course'
import { assessmentAPI } from '@/api/assessment'
import { navigateTo } from '@/utils/link'

// import TabBar2 from '@/components/TabBar2.vue'
import SvgIcon from '@/components/SvgIcon.vue'
import CounselorCard from '@/components/CounselorCard.vue'
import CourseCard from '@/components/CourseCard.vue'
import AssessmentCard from '@/components/AssessmentCard.vue'
import NavigationMenu from '@/components/NavigationMenu.vue'
import Banner from '@/components/Banner.vue'
import Navbar from '@/components/Navbar.vue'

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


    if (res.code === 200 && res.success && res.data && res.data.list) {
      // 处理课程数据，确保rating有默认值
      courseList.value = res.data.list.map(course => ({
        ...course,
        rating: course.rating || 4.8, // 如果rating为0，使用默认值4.8
        student_count: course.student_count || 0
      }))
    } else {
      courseList.value = []
    }
  } catch (error) {
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

// 获取测评数据
const fetchAssessments = async () => {
  try {
    const res = await assessmentAPI.getAssessments({
      page: 1,
      per_page: 5,
      status: 'published' // 只获取已发布的测评
    })


    if (res.success && res.data) {
      // 处理测评数据，确保所有字段都有默认值
      assessmentList.value = (res.data.list || []).map(assessment => ({
        ...assessment,
        participant_count: assessment.participant_count || 0,
        price: assessment.price || 0,
        difficulty: assessment.difficulty || 'medium'
      }))
    } else {
      assessmentList.value = []
    }
  } catch (error) {
    console.error('获取测评列表失败:', error)
    assessmentList.value = []
  }
}

// 轮播图点击处理
const handleBannerClick = ({ banner, index }) => {
  // Banner 组件已经处理了跳转逻辑，这里可以添加额外的处理，比如统计
}

// 轮播图变化处理
const handleBannerChange = ({ current, banner }) => {
  // 这里可以添加轮播图变化时的处理逻辑，比如埋点统计
}

// 菜单点击处理
const handleMenuClick = (menuItem) => {
  // 这里可以添加额外的点击处理逻辑，比如统计、权限检查等
}

// 咨询师卡片点击处理
const handleCounselorClick = (counselor) => {
}

// 课程卡片点击处理
const handleCourseClick = (course) => {
}

// 心理测评卡片点击处理
const handleAssessmentClick = (assessment) => {

  if (assessment && assessment.id) {
    // 导航到测评详情页
    navigateTo(`/pages/assessment/detail?id=${assessment.id}`)
  } else {
    uni.showToast({
      title: '测评数据异常',
      icon: 'none'
    })
  }
}

// 搜索栏点击处理
const handleSearchBarClick = () => {
  uni.showToast({
    title: '跳转到搜索页面',
    icon: 'none'
  })
  navigateTo('/pages/search')
}




const onImageLoad = (e) => {
  // 图片加载成功
}

const onImageError = (e) => {
  // 图片加载失败
}


onLoad(() => {
  // 获取系统信息，设置状态栏高度
  const systemInfo = uni.getSystemInfoSync()
  const statusBarHeight = systemInfo.statusBarHeight || 0

  // 设置CSS变量
  const style = document.documentElement.style || document.body.style
  if (style) {
    style.setProperty('--status-bar-height', statusBarHeight + 'px')
  }

  fetchBanners()
  fetchCounselors()
  fetchCourses()
  fetchAssessments()
})

onShow(() => {
  // 每次显示页面时更新用户信息
  if (userStore.isLoggedIn) {
    userStore.getUserInfo()
  }
})
</script>

<style lang="scss" scoped>
// SCSS 变量定义
$primary-color: #4A90E2;
$bg-color: #f5f7fa;
$white: #fff;
$gray-light: #f5f5f5;
$gray: #999;
$gray-dark: #333;
$text-color: #333;
$border-radius: 16rpx;
$border-radius-small: 12rpx;
$border-radius-large: 30rpx;
$shadow-light: 0 2rpx 8rpx rgba(0, 0, 0, 0.06);
$red-danger: #ff4d4f;

.container {
  min-height: 100vh;
  background-color: $bg-color;
}

// 顶部导航样式
.header-wrapper {
  background-color: $white;
  box-shadow: $shadow-light;
  position: sticky;
  top: 0;
  z-index: 1000;

  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20rpx 30rpx;
    height: 88rpx;
  }
}

.search-bar {
  flex: 1;
  height: 60rpx;
  background-color: $gray-light;
  border-radius: $border-radius-large;
  display: flex;
  align-items: center;
  padding: 0 24rpx;
  cursor: pointer;
  transition: background-color 0.2s ease;

  &:active {
    background-color: #e8e8e8;
  }

  .search-text {
    font-size: 26rpx;
    color: $gray;
    margin-left: 12rpx;
  }
}



// 轮播图样式 - 已移至 Banner 组件

// 功能导航样式 - 已移至 NavigationMenu 组件

// 区块样式
.section {
  margin: 20rpx;
  border-radius: $border-radius;
  background-color: $white;
  padding: 30rpx;

  &:last-of-type {
    margin-bottom: 120rpx; // 为TabBar留出空间
  }

  &-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;
  }

  &-title {
    font-size: 32rpx;
    font-weight: bold;
    color: $text-color;
    display: flex;
    align-items: center;

    &-icon {
      width: 8rpx;
      height: 32rpx;
      background-color: $primary-color;
      margin-right: 16rpx;
      border-radius: 4rpx;
    }
  }

  &-more {
    font-size: 26rpx;
    color: $gray;
    display: flex;
    align-items: center;
    gap: 8rpx;
    cursor: pointer;

    text {
      font-size: 26rpx;
      color: $gray;
      transform: translate(8rpx, 0rpx);
    }
  }

  &-empty {
    height: 200rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #fafafa;
    border-radius: $border-radius-small;
    margin: 20rpx 0;
  }
}

// 列表样式
.counselor-list,
.course-list,
.assessment-list {
  display: flex;
  flex-direction: column;
}

.counselor-list {
  width: 100%;
}
</style>
