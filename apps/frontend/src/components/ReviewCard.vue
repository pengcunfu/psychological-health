<template>
  <view class="reviews-card" v-if="reviews.length > 0">
    <view class="card-header">
      <view class="section-indicator"></view>
      <text class="card-title">用户评价</text>
      <text class="review-count">({{ totalCount }}条)</text>
    </view>
    
    <view class="reviews-content">
      <view class="review-item" v-for="(review, index) in displayReviews" :key="review.id || index">
        <view class="review-header">
          <up-avatar :src="review.user_avatar || defaultAvatar" size="60"></up-avatar>
          <view class="review-user">
            <text class="review-username">{{ review.username || '匿名用户' }}</text>
            <view class="review-rating">
              <up-rate 
                :value="review.rating || 5" 
                readonly 
                size="12" 
                active-color="#faad14"
              ></up-rate>
              <text class="review-time">{{ formatDate(review.create_time) }}</text>
            </view>
          </view>
        </view>
        <text class="review-text">{{ review.content || '用户给出了好评' }}</text>
      </view>
      
      <view class="view-more" v-if="showViewMore" @click="handleViewMore">
        <text class="view-more-text">查看全部{{ totalCount }}条评价</text>
        <SvgIcon name="arrow-right" :size="14" color="#4A90E2" />
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import SvgIcon from '@/components/SvgIcon.vue'

// 定义 props
const props = defineProps({
  // 评价列表
  reviews: {
    type: Array,
    default: () => []
  },
  // 总评价数量
  totalCount: {
    type: Number,
    default: 0
  },
  // 显示的评价数量
  displayLimit: {
    type: Number,
    default: 3
  },
  // 默认头像
  defaultAvatar: {
    type: String,
    default: '/static/images/default-avatar.png'
  },
  // 是否显示查看更多按钮
  showViewMoreBtn: {
    type: Boolean,
    default: true
  }
})

// 定义 emits
const emit = defineEmits(['viewMore'])

// 计算显示的评价列表
const displayReviews = computed(() => {
  return props.reviews.slice(0, props.displayLimit)
})

// 是否显示查看更多按钮
const showViewMore = computed(() => {
  return props.showViewMoreBtn && props.totalCount > props.displayLimit
})

// 格式化日期
const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  const year = d.getFullYear()
  const month = (d.getMonth() + 1).toString().padStart(2, '0')
  const day = d.getDate().toString().padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 查看更多处理
const handleViewMore = () => {
  emit('viewMore')
}
</script>

<style lang="scss" scoped>
.reviews-card {
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

.review-count {
  font-size: 28rpx;
  color: #999;
  margin-left: 8rpx;
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
  cursor: pointer;
}

.view-more-text {
  margin-right: 10rpx;
}
</style> 