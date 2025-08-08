<template>
  <view class="course-card" @click="handleCardClick">
    <view class="course-left">
      <image class="course-img" :src="course.cover_image || course.cover || '/static/images/default-course.png'"
        mode="aspectFill" />
      <view class="course-tag">精品课</view>
    </view>

    <view class="course-right">
      <view class="course-header">
        <text class="course-title">{{ course.title || course.name }}</text>
        <text class="course-subtitle" v-if="course.subtitle">{{ course.subtitle }}</text>
      </view>

      <view class="course-instructor">
        <text>{{ course.instructor || course.teacher || '武志红' }} | {{ course.lesson_count || course.chapters || '109'
        }}节</text>
      </view>

      <view class="course-footer">
        <view class="course-stats">
          <text class="play-count">{{ formatPlayCount(course.play_count || course.student_count) }}播放</text>
        </view>
        <view class="course-price">
          <view v-if="course.price > 0" class="price-container">
            <text class="price-symbol">¥</text>
            <text class="price-amount">{{ course.price }}</text>
            <text class="price-unit">/课</text>
          </view>
          <text class="price-free" v-else>免费</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { navigateTo } from '@/utils/link'

// Props
const props = defineProps({
  course: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

// Events
const emit = defineEmits(['click'])

// Methods
const handleCardClick = () => {
  emit('click', props.course)
  const courseId = props.course.id
  if (courseId) {
    navigateTo(`/pages/course/detail?id=${courseId}`)
  }
}

// 格式化播放次数
const formatPlayCount = (count) => {
  if (!count) return '1626.4万'

  const num = parseInt(count)
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toString()
}
</script>

<style lang="scss" scoped>
// SCSS变量
$primary-color: #4A90E2;
$danger-color: #ff4d4f;
$success-color: #52c41a;
$text-color: #333;
$text-light: #666;
$text-lighter: #999;
$text-lightest: #ccc;
$white: #fff;
$black: #000;
$bg-light: #f8f9fa;
$shadow-light: rgba(0, 0, 0, 0.08);
$shadow-medium: rgba(0, 0, 0, 0.12);
$shadow-dark: rgba(0, 0, 0, 0.7);
$shadow-hover: rgba(0, 0, 0, 0.15);
$border-radius: 16rpx;
$border-radius-small: 8rpx;

.course-card {
  display: flex;
  border-radius: $border-radius;
  background: linear-gradient(135deg, $white 0%, $bg-light 100%);
  overflow: hidden;
  margin: 0 30rpx 24rpx 30rpx;
  min-height: 180rpx;
  width: calc(100% - 60rpx);
  box-shadow: 0 4rpx 16rpx $shadow-light;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1rpx solid rgba(0, 0, 0, 0.04);
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2rpx;
    background: linear-gradient(90deg, $primary-color 0%, rgba(74, 144, 226, 0.3) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  &:hover {
    transform: translateY(-4rpx);
    box-shadow: 0 8rpx 32rpx $shadow-hover;

    &::before {
      opacity: 1;
    }
  }

  &:active {
    transform: translateY(-2rpx);
    box-shadow: 0 6rpx 24rpx $shadow-medium;
  }

  .course-left {
    position: relative;
    width: 200rpx;
    min-width: 200rpx;
    min-height: 180rpx;
    margin-right: 24rpx;
    flex-shrink: 0;
    overflow: hidden;
    border-radius: $border-radius;

    .course-img {
      width: 100%;
      height: 180rpx;
      border-radius: $border-radius;
      object-fit: cover;
      transition: transform 0.4s ease;
    }

    &:hover .course-img {
      transform: scale(1.05);
    }

    .course-tag {
      position: absolute;
      bottom: 12rpx;
      left: 12rpx;
      background: linear-gradient(135deg, $shadow-dark 0%, rgba(0, 0, 0, 0.8) 100%);
      color: $white;
      font-size: 20rpx;
      font-weight: 500;
      padding: 6rpx 16rpx;
      border-radius: 20rpx;
      backdrop-filter: blur(10rpx);
      box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
      border: 1rpx solid rgba(255, 255, 255, 0.1);
    }
  }

  .course-right {
    flex: 1;
    min-height: 180rpx;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 16rpx 0;

    .course-header {
      margin-bottom: 12rpx;

      .course-title {
        font-size: 32rpx;
        font-weight: 600;
        color: $text-color;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 12rpx;
        word-break: break-word;
        letter-spacing: 0.5rpx;
      }

      .course-subtitle {
        font-size: 26rpx;
        color: $text-light;
        line-height: 1.3;
        margin-bottom: 8rpx;
        display: -webkit-box;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
        font-weight: 400;
      }
    }

    .course-instructor {
      margin-bottom: 16rpx;
      padding: 8rpx 16rpx;
      background-color: rgba(74, 144, 226, 0.05);
      border-radius: $border-radius-small;
      border-left: 3rpx solid $primary-color;

      text {
        font-size: 24rpx;
        color: $text-light;
        display: -webkit-box;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
        font-weight: 500;
      }
    }

    .course-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 8rpx;
      border-top: 1rpx solid rgba(0, 0, 0, 0.06);

      .course-stats {
        flex: 1;

        .play-count {
          font-size: 24rpx;
          color: $text-lighter;
          position: relative;
          padding-left: 24rpx;

          &::before {
            content: '▶';
            position: absolute;
            left: 0;
            color: $primary-color;
            font-size: 20rpx;
          }
        }
      }

      .course-price {
        margin-left: 20rpx;

        .price-container {
          display: flex;
          align-items: baseline;
          color: $danger-color;
          font-weight: bold;

          .price-symbol {
            font-size: 20rpx;
          }

          .price-amount {
            font-size: 32rpx;
            margin: 0 2rpx;
          }

          .price-unit {
            font-size: 20rpx;
            color: $text-lighter;
            font-weight: normal;
          }
        }

        .price-free {
          color: $success-color;
          font-size: 32rpx;
          font-weight: bold;
        }
      }
    }
  }
}

// 响应式设计
@media screen and (max-width: 400px) {
  .course-card {
    min-height: 160rpx;
    margin: 0 20rpx 20rpx 20rpx;
    width: calc(100% - 40rpx);

    .course-left {
      width: 170rpx;
      min-width: 170rpx;
      min-height: 160rpx;
      margin-right: 20rpx;

      .course-img {
        height: 160rpx;
      }

      .course-tag {
        bottom: 8rpx;
        left: 8rpx;
        font-size: 18rpx;
        padding: 4rpx 12rpx;
      }
    }

    .course-right {
      min-height: 160rpx;
      padding: 12rpx 0;

      .course-header {
        margin-bottom: 8rpx;

        .course-title {
          font-size: 28rpx;
          margin-bottom: 8rpx;
        }

        .course-subtitle {
          font-size: 24rpx;
          margin-bottom: 6rpx;
        }
      }

      .course-instructor {
        margin-bottom: 12rpx;
        padding: 6rpx 12rpx;

        text {
          font-size: 22rpx;
        }
      }

      .course-footer {
        .course-stats {
          .play-count {
            font-size: 22rpx;
          }
        }

        .course-price {
          .price-container {
            padding: 4rpx 8rpx;

            .price-symbol {
              font-size: 20rpx;
            }

            .price-amount {
              font-size: 30rpx;
            }

            .price-unit {
              font-size: 20rpx;
            }
          }

          .price-free {
            font-size: 30rpx;
            padding: 4rpx 12rpx;
          }
        }
      }
    }
  }
}
</style>