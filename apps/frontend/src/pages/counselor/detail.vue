<template>
  <view class="container">
    <!-- 加载状态 -->
    <view v-if="loading" class="loading-container">
      <up-loading-page :loading="true" loading-text="加载中..."></up-loading-page>
    </view>

    <!-- 主要内容 -->
    <view v-else-if="counselorInfo.id" class="content">
      <!-- 咨询师头部大图 -->
      <view class="counselor-hero">
        <image 
          class="hero-avatar" 
          :src="counselorInfo.avatar || '/static/images/default-avatar.png'" 
          mode="aspectFill"
          @error="onAvatarError"
        />
        <view class="hero-overlay">
          <!-- 保障信息条 -->
          <view class="guarantee-bar">
            <up-icon name="shield-checkmark" size="16" color="#fff"></up-icon>
            <text class="guarantee-text">甄选头部师资 · 限时免费取消 · 隐私加密保护</text>
            <up-icon name="arrow-right" size="14" color="#fff"></up-icon>
          </view>
        </view>
      </view>

      <!-- 咨询师基本信息 -->
      <view class="counselor-info-card">
        <view class="counselor-header">
          <view class="counselor-main">
            <view class="name-section">
              <text class="counselor-name">{{ counselorInfo.name || '未知咨询师' }}</text>
              <view class="counselor-badge" v-if="counselorInfo.title">
                <up-icon name="checkmark-circle" size="16" color="#faad14"></up-icon>
                <text class="badge-text">{{ counselorInfo.title }}</text>
              </view>
            </view>
            <text class="counselor-subtitle">{{ counselorInfo.specialty || '国家二级心理咨询师' }}</text>
            <text class="counselor-service">视频咨询</text>
          </view>
          <view class="price-section">
            <view class="price-line">
              <text class="price-symbol">¥</text>
              <text class="price-amount">{{ counselorInfo.price || 600 }}</text>
              <text class="price-unit">/次</text>
            </view>
          </view>
        </view>

        <!-- 咨询经验条 -->
        <view class="experience-bar">
          <up-icon name="star" size="16" color="#faad14"></up-icon>
          <text class="experience-text">咨询经验 · {{ getExperienceText() }}</text>
          <up-icon name="arrow-right" size="12" color="#999"></up-icon>
        </view>

        <!-- 统计数据 -->
        <view class="stats-row">
          <view class="stat-item">
            <text class="stat-label">从业时长</text>
            <view class="stat-value-line">
              <text class="stat-number">{{ getWorkYears() }}</text>
              <text class="stat-unit">年</text>
            </view>
          </view>
          <view class="stat-item">
            <text class="stat-label">咨询经验</text>
            <view class="stat-value-line">
              <text class="stat-number">{{ counselorInfo.consultation_count || 4600 }}</text>
              <text class="stat-unit">+小时</text>
            </view>
          </view>
          <view class="stat-item">
            <text class="stat-label">1对1督导</text>
            <view class="stat-value-line">
              <text class="stat-number">{{ getSupervisoryHours() }}</text>
              <text class="stat-unit">+小时</text>
            </view>
          </view>
          <view class="stat-item">
            <text class="stat-label">团体咨询</text>
            <view class="stat-value-line">
              <text class="stat-number">{{ getGroupHours() }}</text>
              <text class="stat-unit">+小时</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 个人简介卡片 -->
      <view class="intro-card">
        <view class="card-header">
          <view class="section-indicator"></view>
          <text class="card-title">个人简介</text>
        </view>
        
        <view class="intro-content">
          <!-- 个人头衔 -->
          <view class="intro-section">
            <text class="intro-subtitle">个人头衔：</text>
            <view class="intro-tags">
              <text class="intro-tag">{{ counselorInfo.title || '国家二级心理咨询师' }}</text>
              <text class="intro-tag">初级心理治疗师</text>
              <text class="intro-tag">中国艾利克森注册催眠治疗师</text>
            </view>
          </view>

          <!-- 咨询师介绍 -->
          <view class="intro-section" v-if="counselorInfo.introduction">
            <text class="intro-text">{{ counselorInfo.introduction }}</text>
          </view>

          <!-- 个人简介 -->
          <view class="intro-section" v-if="counselorInfo.bio">
            <text class="intro-text">{{ counselorInfo.bio }}</text>
          </view>

          <!-- 专业领域 -->
          <view class="intro-section" v-if="displayTags.length > 0">
            <text class="intro-subtitle">专业领域：</text>
            <view class="specialty-tags">
              <text class="specialty-tag" v-for="(tag, index) in displayTags" :key="index">
                {{ tag }}
              </text>
            </view>
          </view>

          <!-- 教育背景 -->
          <view class="intro-section">
            <text class="intro-subtitle">教育背景：</text>
            <view class="education-list">
              <view class="education-item" v-for="(edu, index) in education" :key="index">
                <text class="edu-period">{{ edu.year }}</text>
                <text class="edu-detail">{{ edu.school }} {{ edu.degree }}</text>
              </view>
            </view>
          </view>

          <!-- 联系信息 -->
          <view class="intro-section" v-if="counselorInfo.phone || counselorInfo.email">
            <text class="intro-subtitle">联系方式：</text>
            <view class="contact-info">
              <view class="contact-item" v-if="counselorInfo.phone">
                <up-icon name="phone" size="16" color="#666"></up-icon>
                <text class="contact-text">{{ counselorInfo.phone }}</text>
              </view>
              <view class="contact-item" v-if="counselorInfo.email">
                <up-icon name="email" size="16" color="#666"></up-icon>
                <text class="contact-text">{{ counselorInfo.email }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 评价卡片 -->
      <view class="reviews-card" v-if="comments.length > 0">
        <view class="card-header">
          <view class="section-indicator"></view>
          <text class="card-title">用户评价</text>
          <text class="review-count">({{ commentCount }}条)</text>
        </view>
        
        <view class="reviews-content">
          <view class="review-item" v-for="(comment, index) in comments.slice(0, 3)" :key="index">
            <view class="review-header">
              <u-avatar :src="comment.user_avatar || '/static/images/default-avatar.png'" size="60"></u-avatar>
              <view class="review-user">
                <text class="review-username">{{ comment.username || '匿名用户' }}</text>
                <view class="review-rating">
                  <u-rate :value="comment.rating || 5" readonly size="12" active-color="#faad14"></u-rate>
                  <text class="review-time">{{ formatDate(comment.create_time) }}</text>
                </view>
              </view>
            </view>
            <text class="review-text">{{ comment.content || '用户给出了好评' }}</text>
          </view>
          
          <view class="view-more" v-if="commentCount > 3" @click="viewAllReviews">
            <text class="view-more-text">查看全部{{ commentCount }}条评价</text>
            <up-icon name="arrow-right" size="14" color="#4A90E2"></up-icon>
          </view>
        </view>
      </view>

      <!-- 底部安全距离 -->
      <view class="bottom-safe-area"></view>
    </view>

    <!-- 错误状态 -->
    <view v-else-if="error" class="error-container">
      <up-empty 
        text="咨询师信息加载失败"
        icon="https://cdn.uviewui.com/uview/empty/error.png"
        iconSize="120"
        textSize="16"
        textColor="#999999"
        marginTop="100"
      >
        <template #button>
          <up-button
            text="重新加载"
            type="primary"
            size="normal"
            @click="fetchCounselorInfo"
            :customStyle="{
              marginTop: '30rpx',
              width: '200rpx',
              borderRadius: '22rpx',
              background: '#4A90E2'
            }"
          ></up-button>
        </template>
      </up-empty>
    </view>

    <!-- 固定底部操作栏 -->
    <view v-if="counselorInfo.id && !loading" class="fixed-bottom-bar">
      <view class="bottom-actions">
        <view class="favorite-btn" @click="toggleFavorite">
          <up-icon 
            :name="isFavorite ? 'heart-fill' : 'heart'" 
            :color="isFavorite ? '#ff6b6b' : '#666'" 
            size="24"
          ></up-icon>
          <text class="favorite-text">收藏</text>
        </view>
        <button 
          class="appointment-btn" 
          @click="handleAppointment" 
          :disabled="counselorInfo.status !== 1"
        >
          {{ counselorInfo.status === 1 ? '立即预约' : '暂不可预约' }}
        </button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { counselorAPI } from '@/api/counselor'
import { checkLogin } from '@/utils/auth'

// 页面参数
const counselorId = ref('')

// 数据状态
const loading = ref(true)
const error = ref(false)
const counselorInfo = ref({})
const comments = ref([])
const commentCount = ref(0)
const isFavorite = ref(false)

// 教育背景（前端暂时保留的模拟数据）
const education = ref([
  { year: '2015-2018', school: '北京大学', degree: '心理学博士' },
  { year: '2012-2015', school: '清华大学', degree: '心理学硕士' },
  { year: '2008-2012', school: '复旦大学', degree: '心理学学士' }
])

// 计算属性
const displayTags = computed(() => {
  if (Array.isArray(counselorInfo.value.tags)) {
    return counselorInfo.value.tags.filter(tag => tag && tag.trim())
  } else if (typeof counselorInfo.value.tags === 'string' && counselorInfo.value.tags) {
    return counselorInfo.value.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
  }
  return ['抑郁症咨询', '焦虑症治疗', '人际关系指导', '情感咨询']
})

// 获取咨询师信息
const fetchCounselorInfo = async () => {
  if (!counselorId.value) {
    error.value = true
    loading.value = false
    return
  }

  loading.value = true
  error.value = false

  try {
    const res = await counselorAPI.getCounselorDetail(counselorId.value)
    console.log('咨询师详情API响应:', res)
    
    if (res.success && res.data) {
      counselorInfo.value = {
        ...res.data,
        price: parseFloat(res.data.price) || 600,
        rating: parseFloat(res.data.rating) || 5.0,
        consultation_count: parseInt(res.data.consultation_count) || 4600,
        status: parseInt(res.data.status) || 1
      }
      
      // 获取评价
      await fetchComments()
    } else {
      error.value = true
    }
  } catch (err) {
    console.error('获取咨询师信息失败:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

// 获取评价列表
const fetchComments = async () => {
  try {
    // 暂时使用模拟数据
    comments.value = [
      {
        id: 1,
        username: '用户A***',
        user_avatar: '',
        rating: 5,
        content: '咨询师非常专业，帮助我解决了很多心理问题，非常感谢！态度很好，很有耐心。',
        create_time: '2024-01-15'
      },
      {
        id: 2,
        username: '用户B***',
        user_avatar: '',
        rating: 5,
        content: '服务态度很好，很有耐心，推荐大家来咨询。效果很明显，值得信赖。',
        create_time: '2024-01-10'
      },
      {
        id: 3,
        username: '用户C***',
        user_avatar: '',
        rating: 4,
        content: '专业水平很高，给了很多实用的建议，感觉心情好了很多。',
        create_time: '2024-01-08'
      }
    ]
    commentCount.value = comments.value.length + 15 // 模拟更多评价
  } catch (error) {
    console.error('获取评价列表失败:', error)
  }
}

// 工具函数
const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  const year = d.getFullYear()
  const month = (d.getMonth() + 1).toString().padStart(2, '0')
  const day = d.getDate().toString().padStart(2, '0')
  return `${year}-${month}-${day}`
}

const onAvatarError = () => {
  console.error('Counselor avatar failed to load')
}

const getExperienceText = () => {
  const currentYear = new Date().getFullYear()
  return `${currentYear}通过年审`
}

const getWorkYears = () => {
  return Math.floor((counselorInfo.value.consultation_count || 4600) / 500) || 8
}

const getSupervisoryHours = () => {
  return Math.floor((counselorInfo.value.consultation_count || 4600) * 0.06) || 280
}

const getGroupHours = () => {
  return Math.floor((counselorInfo.value.consultation_count || 4600) * 0.19) || 860
}

// 收藏功能
const toggleFavorite = () => {
  if (!checkLogin()) return
  
  isFavorite.value = !isFavorite.value
  uni.showToast({
    title: isFavorite.value ? '已收藏' : '已取消收藏',
    icon: 'none'
  })
  
  // TODO: 调用收藏API
}

// 查看所有评价
const viewAllReviews = () => {
  uni.navigateTo({
    url: `/pages/counselor/reviews?id=${counselorId.value}`
  })
}

// 预约处理
const handleAppointment = () => {
  if (counselorInfo.value.status !== 1) {
    uni.showToast({
      title: '该咨询师暂时离职，无法预约',
      icon: 'none'
    })
    return
  }

  if (!checkLogin()) return
  
  // 跳转到预约页面
  uni.navigateTo({
    url: `/pages/counselor/appointment-now?counselor_id=${counselorId.value}`
  })
}

// 页面加载
onLoad((options) => {
  if (options.id) {
    counselorId.value = options.id
    fetchCounselorInfo()
  } else {
    error.value = true
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 0;
}

.loading-container, .error-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content {
  padding: 20rpx;
  padding-bottom: 120rpx; // 为固定底部栏留出空间
}

.counselor-hero {
  position: relative;
  height: 500rpx;
  border-radius: 20rpx;
  overflow: hidden;
  margin-bottom: 20rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.15);
}

.hero-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 120rpx;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  display: flex;
  align-items: flex-end;
  padding: 0;
  box-sizing: border-box;
}

.guarantee-bar {
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.9), rgba(24, 144, 255, 0.9));
  padding: 10rpx 20rpx;
  border-radius: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  color: #fff;
  font-weight: 500;
  width: 100%;
  height: 100%;
  backdrop-filter: blur(10rpx);
}

.guarantee-text {
  margin: 0 10rpx;
}

.counselor-info-card {
  background-color: #fff;
  padding: 35rpx 30rpx;
  margin-bottom: 20rpx;
  border-radius: 16rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
  border: 1rpx solid rgba(0, 0, 0, 0.05);
}

.counselor-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 25rpx;
}

.counselor-main {
  flex: 1;
}

.name-section {
  display: flex;
  align-items: center;
  margin-bottom: 15rpx;
  flex-wrap: wrap;
  gap: 15rpx;
}

.counselor-name {
  font-size: 44rpx;
  font-weight: bold;
  color: #1a1a1a;
  line-height: 1.2;
}

.counselor-badge {
  display: flex;
  align-items: center;
  background-color: #fffbe6;
  padding: 6rpx 12rpx;
  border-radius: 8rpx;
  border: 1rpx solid #ffe58f;
}

.badge-text {
  font-size: 24rpx;
  color: #faad14;
  font-weight: bold;
}

.counselor-subtitle {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 10rpx;
}

.counselor-service {
  font-size: 28rpx;
  color: #4A90E2;
  background-color: #e6f7ff;
  padding: 6rpx 12rpx;
  border-radius: 8rpx;
  display: inline-block;
}

.price-section {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.price-line {
  display: flex;
  align-items: baseline;
}

.price-symbol {
  font-size: 28rpx;
  color: #ff4d4f;
  font-weight: bold;
  margin-right: 2rpx;
}

.price-amount {
  font-size: 40rpx;
  font-weight: bold;
  color: #ff4d4f;
  line-height: 1;
}

.price-unit {
  font-size: 24rpx;
  color: #999;
  margin-left: 2rpx;
}

.experience-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 25rpx 0;
  padding: 12rpx 20rpx;
  background: linear-gradient(135deg, #f0f9ff, #e6f7ff);
  border-radius: 12rpx;
  border: 1rpx solid #b7eb8f;
  box-shadow: 0 2rpx 8rpx rgba(74, 144, 226, 0.1);
}

.experience-text {
  font-size: 26rpx;
  color: #4A90E2;
  margin: 0 10rpx;
  font-weight: 500;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15rpx;
  margin: 25rpx 0;
  padding: 20rpx 15rpx;
  background: linear-gradient(135deg, #fafbfc, #f5f7fa);
  border-radius: 12rpx;
  border: 1rpx solid #e8f4f8;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.05);
}

.stat-item {
  text-align: left;
  padding: 8rpx 5rpx;
}

.stat-label {
  font-size: 20rpx;
  color: #666;
  margin-bottom: 6rpx;
  font-weight: 400;
  display: block;
}

.stat-value-line {
  display: flex;
  align-items: baseline;
  justify-content: flex-start;
  white-space: nowrap;
  flex-wrap: nowrap;
}

.stat-number {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  line-height: 1.2;
  white-space: nowrap;
}

.stat-unit {
  font-size: 20rpx;
  color: #666;
  margin-left: 2rpx;
  font-weight: 400;
  white-space: nowrap;
}

.intro-card {
  background-color: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.section-indicator {
  width: 6rpx;
  height: 30rpx;
  background-color: #4A90E2;
  margin-right: 10rpx;
  border-radius: 3rpx;
}

.card-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.intro-content {
  font-size: 28rpx;
  color: #666;
  line-height: 1.8;
}

.intro-section {
  margin-bottom: 30rpx;
}

.intro-section:last-child {
  margin-bottom: 0;
}

.intro-subtitle {
  font-size: 28rpx;
  color: #999;
  margin-bottom: 15rpx;
  display: block;
}

.intro-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
}

.intro-tag {
  font-size: 26rpx;
  color: #4A90E2;
  background-color: #e6f7ff;
  padding: 8rpx 12rpx;
  border-radius: 8rpx;
  border: 1rpx solid #91d5ff;
}

.intro-text {
  margin-top: 10rpx;
}

.specialty-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
}

.specialty-tag {
  font-size: 26rpx;
  color: #4A90E2;
  background-color: #e6f7ff;
  padding: 8rpx 12rpx;
  border-radius: 8rpx;
  border: 1rpx solid #91d5ff;
}

.education-list {
  margin-top: 10rpx;
}

.education-item {
  display: flex;
  margin-bottom: 15rpx;
  padding-bottom: 15rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.education-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.edu-period {
  font-size: 26rpx;
  color: #999;
  width: 180rpx;
  flex-shrink: 0;
}

.edu-detail {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
  display: block;
  margin-bottom: 5rpx;
}

.contact-info {
  margin-top: 15rpx;
}

.contact-item {
  display: flex;
  align-items: center;
  margin-bottom: 10rpx;
}

.contact-item:last-child {
  margin-bottom: 0;
}

.contact-text {
  font-size: 28rpx;
  color: #666;
  margin-left: 8rpx;
}

.reviews-card {
  background-color: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.reviews-content {
  margin-top: 20rpx;
}

.review-item {
  padding: 25rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.review-item:last-child {
  border-bottom: none;
}

.review-header {
  display: flex;
  align-items: center;
  margin-bottom: 15rpx;
}

.review-user {
  flex: 1;
  margin-left: 15rpx;
}

.review-username {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
  display: block;
  margin-bottom: 8rpx;
}

.review-rating {
  display: flex;
  align-items: center;
}

.review-time {
  font-size: 24rpx;
  color: #999;
  margin-left: 15rpx;
}

.review-text {
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
}

.view-more {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20rpx;
  color: #4A90E2;
  font-size: 28rpx;
}

.view-more-text {
  margin-right: 10rpx;
}

.bottom-safe-area {
  height: 100rpx; /* 底部安全距离 */
}

.fixed-bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(135deg, #fff, #fafbfc);
  padding: 25rpx 30rpx;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-sizing: border-box;
  z-index: 100;
  border-top: 1rpx solid #f0f0f0;
  backdrop-filter: blur(10rpx);
}

.bottom-actions {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 25rpx;
}

.favorite-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10rpx;
}

.favorite-text {
  font-size: 24rpx;
  color: #666;
  margin-top: 5rpx;
}

.appointment-btn {
  background: linear-gradient(135deg, #4A90E2, #1890ff);
  color: #fff;
  font-size: 30rpx;
  font-weight: 600;
  padding: 0;
  border-radius: 40rpx;
  border: none;
  flex: 1;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 16rpx rgba(74, 144, 226, 0.4);
  transition: all 0.3s ease;
}

.appointment-btn:disabled {
  background: linear-gradient(135deg, #d9d9d9, #f0f0f0);
  color: #999;
  box-shadow: none;
  transform: none;
}
</style> 