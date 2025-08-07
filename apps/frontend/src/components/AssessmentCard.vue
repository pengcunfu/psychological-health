<template>
  <view 
    class="assessment-card" 
    @click="handleCardClick"
  >
    <view class="assessment-left">
      <image 
        class="assessment-img" 
        :src="getAssessmentCover()" 
        mode="aspectFill"
        @error="onImageError"
      />
    </view>
    
    <view class="assessment-right">
      <view class="assessment-header">
        <text class="assessment-title">{{ assessment.name || assessment.title }}</text>
        <text class="assessment-subtitle" v-if="assessment.subtitle">
          {{ assessment.subtitle }}
        </text>
      </view>
      
      <view class="assessment-info">
        <view class="info-row">
          <text class="info-item">{{ formatParticipantCount(assessment.participant_count) }}人已测</text>
          <text class="info-item" v-if="assessment.difficulty">{{ getDifficultyText(assessment.difficulty) }}</text>
        </view>
        <text class="assessment-desc" v-if="assessment.description">{{ assessment.description }}</text>
      </view>
      
      <view class="assessment-footer">
        <view class="assessment-price">
          <text class="price-text" v-if="assessment.price > 0">¥{{ assessment.price }}</text>
          <text class="price-text free" v-else>免费</text>
        </view>
        <view class="assessment-action">
          <text class="action-btn">立即测试</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { navigateTo } from '@/utils/link'

// Props
const props = defineProps({
  assessment: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

// Events
const emit = defineEmits(['click'])

// Methods
const handleCardClick = () => {
  emit('click', props.assessment)
  const assessmentId = props.assessment.id
  if (assessmentId) {
    navigateTo(`/pages/assessment/detail?id=${assessmentId}`)
  }
}

// 格式化参与人数
const formatParticipantCount = (count) => {
  if (!count) return '201.2万'
  
  const num = parseInt(count)
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toString()
}

// 获取评估封面图片
const getAssessmentCover = () => {
  return props.assessment.cover_image || props.assessment.cover || '/static/images/default-assessment.png'
}

// 图片加载失败处理
const onImageError = () => {
  console.error('Assessment cover image failed to load')
}

// 获取难度文本
const getDifficultyText = (difficulty) => {
  switch (difficulty) {
    case 'easy':
      return '简单'
    case 'medium':
      return '中等'
    case 'hard':
      return '困难'
    default:
      return ''
  }
}
</script>

<style lang="scss" scoped>
.assessment-card {
  display: flex;
  border-radius: 12rpx;
  background-color: #fff;
  overflow: hidden;
  margin-bottom: 20rpx;
  height: 240rpx;
}

.assessment-left {
  position: relative;
  width: 180rpx;
  height: 240rpx;
  margin-right: 20rpx;
  flex-shrink: 0;
}

.assessment-img {
  width: 180rpx;
  height: calc(100% - 10rpx);
  border-radius: 12rpx;
  object-fit: cover;
}

.assessment-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 120rpx;
}

.assessment-header {
  margin-bottom: 8rpx;
}

.assessment-title {
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

.assessment-subtitle {
  font-size: 24rpx;
  color: #666;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.assessment-info {
  flex: 1;
  margin-bottom: 8rpx;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 6rpx;
}

.info-item {
  font-size: 22rpx;
  color: #999;
  margin-right: 20rpx;
}

.assessment-desc {
  font-size: 22rpx;
  color: #666;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.assessment-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.assessment-price {
  flex: 1;
}

.price-text {
  font-size: 26rpx;
  font-weight: bold;
  color: #ff6b35;
  
  &.free {
    color: #52c41a;
  }
}

.assessment-action {
  margin-left: 20rpx;
}

.action-btn {
  background-color: #52c41a;
  color: #fff;
  font-size: 22rpx;
  padding: 10rpx 20rpx;
  // border-radius: 8rpx;
  border-top-left-radius: 16rpx;
  font-weight: 500;
}
</style> 