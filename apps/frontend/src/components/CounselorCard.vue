<template>
  <view 
    class="counselor-card" 
    @click="handleCardClick"
  >
    <view class="counselor-left">
      <view class="avatar-container">
        <image class="counselor-avatar" :src="counselor.avatar || '/static/images/default-avatar.png'" mode="aspectFill"></image>
        <view class="counselor-status">最早后天可约</view>
      </view>
    </view>
    <view class="counselor-right">
      <view class="counselor-header">
        <view class="counselor-name-section">
          <text class="counselor-name">{{ counselor.name }}</text>
          <view class="counselor-badge">
            <view class="badge-icon">✓</view>
            <text class="badge-text">中级咨询师</text>
          </view>
        </view>
        <view class="counselor-location">深圳·福田</view>
      </view>
      
      <view class="counselor-description">
        <text>{{ counselor.description || '国家二级心理咨询师 注册系统助理心理师 精神动力学取向' }}</text>
      </view>
      
      <view class="counselor-specialties">
        <text>擅长：{{ getSpecialtyText(counselor) }}</text>
      </view>
      
      <view class="counselor-experience">
        <text>从业{{ counselor.experience_years || '11' }}年 · 咨询经验{{ counselor.consultation_hours || '3700+' }}小时</text>
      </view>
      
      <view class="counselor-footer">
        <view class="counselor-services">
          <text class="service-tag">视频咨询</text>
        </view>
        <view class="counselor-price">
          <text class="price-symbol">¥</text>
          <text class="price-amount">{{ counselor.price || '500' }}</text>
          <text class="price-unit">/节</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { navigateTo } from '@/utils/link'

// Props
const props = defineProps({
  counselor: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

// Events
const emit = defineEmits(['click'])

// Methods
const handleCardClick = () => {
  emit('click', props.counselor)
  navigateTo(`/pages/counselor/detail?id=${props.counselor.id}`)
}

// 获取专业领域
const getSpecialties = (item) => {
  if (item.specialties && Array.isArray(item.specialties) && item.specialties.length > 0) {
    return item.specialties
  }
  if (item.tags && Array.isArray(item.tags) && item.tags.length > 0) {
    return item.tags
  }
  if (typeof item.specialties === 'string' && item.specialties.trim()) {
    return item.specialties.split('/').map(s => s.trim()).filter(s => s)
  }
  return ['心理咨询', '情感支持', '焦虑抑郁']
}

// 获取专长描述文本
const getSpecialtyText = (item) => {
  const specialties = getSpecialties(item)
  return specialties.slice(0, 3).join(' / ')
}
</script>

<style lang="scss" scoped>
.counselor-card {
  display: flex;
  padding: 20rpx;
  border-radius: 12rpx;
  background-color: #fff;
  overflow: hidden;
  margin-bottom: 12rpx;
}

.counselor-left {
  width: 180rpx;
  margin-right: 20rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.avatar-container {
  position: relative;
  width: 180rpx;
  height: 100%;
}

.counselor-avatar {
  width: 180rpx;
  height: 100%;
  border-radius: 12rpx;
  object-fit: cover;
}

.counselor-status {
  position: absolute;
  bottom: 8rpx;
  left: 50%;
  transform: translateX(-50%);
  font-size: 20rpx;
  color: #fff;
  background-color: #4A90E2;
  padding: 4rpx 12rpx;
  border-radius: 12rpx;
  text-align: center;
  white-space: nowrap;
}

.counselor-right {
  flex: 1;
  height: 240rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.counselor-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 6rpx;
}

.counselor-name-section {
  display: flex;
  align-items: center;
  flex: 1;
}

.counselor-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
}

.counselor-badge {
  display: flex;
  align-items: center;
  margin-left: 8rpx;
}

.badge-icon {
  font-size: 16rpx;
  color: #fff;
  font-weight: bold;
  background-color: #fa8c16;
  border-radius: 50%;
  width: 28rpx;
  height: 28rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 6rpx;
}

.badge-text {
  font-size: 22rpx;
  color: #fa8c16;
}

.counselor-location {
  font-size: 24rpx;
  color: #999;
  margin-top: 4rpx;
}

.counselor-description {
  font-size: 24rpx;
  color: #333;
  margin-bottom: 4rpx;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.counselor-specialties {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 4rpx;
  line-height: 1.3;
}

.counselor-experience {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 8rpx;
  line-height: 1.3;
}

.counselor-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.counselor-services {
  display: flex;
  gap: 12rpx;
}

.service-tag {
  font-size: 22rpx;
  color: #4A90E2;
  background-color: #e6f7ff;
  border-radius: 16rpx;
  padding: 6rpx 16rpx;
}

.counselor-price {
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
</style> 