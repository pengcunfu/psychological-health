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
          <u-avatar :src="review.user_avatar || defaultAvatar" size="60"></u-avatar>
          <view class="review-user">
            <text class="review-username">{{ review.username || '匿名用户' }}</text>
            <view class="review-rating">
              <u-rate :value="review.rating || 5" readonly size="12" active-color="#faad14"></u-rate>
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
// SCSS变量
$primary-color: #4A90E2;
$white: #fff;
$text-color: #333;
$text-lighter: #999;
$border-color: #f0f0f0;
$shadow-medium: rgba(0, 0, 0, 0.1);

$padding-large: 30rpx;
$padding-medium: 25rpx;
$padding-small: 20rpx;
$padding-xs: 15rpx;
$margin-medium: 20rpx;
$margin-small: 15rpx;
$margin-xs: 10rpx;
$margin-icon: 8rpx;

$border-radius: 12rpx;
$border-radius-xs: 3rpx;
$indicator-width: 6rpx;
$indicator-height: 30rpx;

$font-size-title: 32rpx;
$font-size-base: 28rpx;
$font-size-small: 24rpx;
$font-weight-bold: bold;
$line-height-text: 1.6;

.reviews-card {
  background-color: $white;
  padding: $padding-large;
  margin-bottom: $margin-medium;
  border-radius: $border-radius;
  box-shadow: 0 2rpx 8rpx $shadow-medium;

  .card-header {
    display: flex;
    align-items: center;
    margin-bottom: $margin-medium;

    .section-indicator {
      width: $indicator-width;
      height: $indicator-height;
      background-color: $primary-color;
      margin-right: $margin-xs;
      border-radius: $border-radius-xs;
    }

    .card-title {
      font-size: $font-size-title;
      font-weight: $font-weight-bold;
      color: $text-color;
    }

    .review-count {
      font-size: $font-size-base;
      color: $text-lighter;
      margin-left: $margin-icon;
    }
  }

  .reviews-content {
    margin-top: $margin-medium;

    .review-item {
      padding: $padding-medium 0;
      border-bottom: 1rpx solid $border-color;

      &:last-child {
        border-bottom: none;
      }

      .review-header {
        display: flex;
        align-items: center;
        margin-bottom: $margin-small;

        .review-user {
          flex: 1;
          margin-left: $margin-small;

          .review-username {
            font-size: $font-size-base;
            color: $text-color;
            font-weight: $font-weight-bold;
            display: block;
            margin-bottom: $margin-icon;
          }

          .review-rating {
            display: flex;
            align-items: center;

            .review-time {
              font-size: $font-size-small;
              color: $text-lighter;
              margin-left: $margin-small;
            }
          }
        }
      }

      .review-text {
        font-size: $font-size-base;
        color: $text-color;
        line-height: $line-height-text;
      }
    }

    .view-more {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-top: $margin-medium;
      color: $primary-color;
      font-size: $font-size-base;
      cursor: pointer;

      .view-more-text {
        margin-right: $margin-xs;
      }
    }
  }
}
</style>