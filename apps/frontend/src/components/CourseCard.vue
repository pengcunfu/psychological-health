<template>
  <view 
    class="course-card" 
    @click="handleCardClick"
  >
    <view class="course-left">
      <image 
        class="course-img" 
        :src="course.cover_image || course.cover || '/static/images/default-course.png'" 
        mode="aspectFill"
      />
      <view class="course-tag">精品课</view>
    </view>
    
    <view class="course-right">
      <view class="course-header">
        <text class="course-title">{{ course.title || course.name }}</text>
        <text class="course-subtitle" v-if="course.subtitle">{{ course.subtitle }}</text>
      </view>
      
      <view class="course-instructor">
        <text>{{ course.instructor || course.teacher || '武志红' }} | {{ course.lesson_count || course.chapters || '109' }}节</text>
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
.course-card {
  display: flex;
  border-radius: 12rpx;
  background-color: #fff;
  overflow: hidden;
  margin-bottom: 20rpx;
  height: 160rpx;
}

.course-left {
  position: relative;
  width: 180rpx;
  height: 100%;
  margin-right: 20rpx;
  flex-shrink: 0;
}

.course-img {
  width: 180rpx;
  height: 100%;
  border-radius: 12rpx;
  object-fit: cover;
}

.course-tag {
  position: absolute;
  bottom: 8rpx;
  left: 8rpx;
  background-color: rgba(0, 0, 0, 0.6);
  color: #fff;
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
}

.course-right {
  flex: 1;
  height: 120rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.course-header {
  margin-bottom: 0;
}

.course-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 6rpx;
}

.course-subtitle {
  font-size: 24rpx;
  color: #333;
  line-height: 1.3;
  margin-bottom: 6rpx;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.course-instructor {
  margin-bottom: 6rpx;
}

.course-instructor text {
  font-size: 24rpx;
  color: #999;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.course-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-stats {
  flex: 1;
}

.play-count {
  font-size: 24rpx;
  color: #999;
}

.course-price {
  margin-left: 20rpx;
}

.price-container {
  display: flex;
  align-items: baseline;
  color: #ff4d4f;
  font-weight: bold;
}

.price-symbol {
  font-size: 20rpx;
}

.price-amount {
  font-size: 32rpx;
  margin: 0 2rpx;
}

.price-unit {
  font-size: 20rpx;
  color: #999;
  font-weight: normal;
}

.price-free {
  color: #52c41a;
  font-size: 32rpx;
  font-weight: bold;
}
</style> 