<template>
  <view 
    class="assessment-card" 
    @click="handleCardClick"
  >
    <view class="assessment-left">
      <image 
        class="assessment-img" 
        :src="assessment.cover || assessment.cover_image || '/static/images/default-assessment.png'" 
        mode="aspectFill"
      />
    </view>
    
    <view class="assessment-right">
      <view class="assessment-header">
        <text class="assessment-title">{{ assessment.title || assessment.name }}</text>
        <text class="assessment-subtitle" v-if="assessment.subtitle || assessment.description">
          {{ assessment.subtitle || assessment.description }}
        </text>
      </view>
      
      <view class="assessment-info">
        <text>{{ formatParticipantCount(assessment.participant_count || assessment.test_count) }}已测</text>
      </view>
      
      <view class="assessment-footer">
        <view class="assessment-stats">
          <!-- 可以放置其他统计信息 -->
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
    navigateTo(`/pages/assessment/detail/index?id=${assessmentId}`)
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
</script>

<style lang="scss" scoped>
.assessment-card {
  display: flex;
  padding: 20rpx;
  border-radius: 12rpx;
  background-color: #fff;
  overflow: hidden;
  margin-bottom: 12rpx;
  height: 160rpx;
}

.assessment-left {
  position: relative;
  width: 180rpx;
  height: 100%;
  margin-right: 20rpx;
  flex-shrink: 0;
}

.assessment-img {
  width: 180rpx;
  height: 100%;
  border-radius: 12rpx;
  object-fit: cover;
}

.assessment-right {
  flex: 1;
  height: 120rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.assessment-header {
  margin-bottom: 0;
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
  color: #333;
  line-height: 1.3;
  margin-bottom: 6rpx;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.assessment-info {
  margin-bottom: 6rpx;
}

.assessment-info text {
  font-size: 24rpx;
  color: #999;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.assessment-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.assessment-stats {
  flex: 1;
}

.assessment-action {
  margin-left: 20rpx;
}

.action-btn {
  background-color: #52c41a;
  color: #fff;
  font-size: 24rpx;
  padding: 12rpx 24rpx;
  border-radius: 20rpx;
  font-weight: 500;
}
</style> 