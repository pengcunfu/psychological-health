<template>
  <view class="intro-card">
    <view class="card-header">
      <view class="section-indicator"></view>
      <text class="card-title">个人简介</text>
    </view>
    
    <view class="intro-content">
      <!-- 个人头衔 -->
      <view class="intro-section" v-if="titles.length > 0">
        <text class="intro-subtitle">个人头衔：</text>
        <view class="intro-tags">
          <text class="intro-tag" v-for="(title, index) in titles" :key="index">
            {{ title }}
          </text>
        </view>
      </view>

      <!-- 咨询师介绍 -->
      <view class="intro-section" v-if="profile.introduction">
        <text class="intro-text">{{ profile.introduction }}</text>
      </view>

      <!-- 个人简介 -->
      <view class="intro-section" v-if="profile.bio">
        <text class="intro-text">{{ profile.bio }}</text>
      </view>

      <!-- 专业领域 -->
      <view class="intro-section" v-if="specialties.length > 0">
        <text class="intro-subtitle">专业领域：</text>
        <view class="specialty-tags">
          <text class="specialty-tag" v-for="(tag, index) in specialties" :key="index">
            {{ tag }}
          </text>
        </view>
      </view>

      <!-- 教育背景 -->
      <view class="intro-section" v-if="education.length > 0">
        <text class="intro-subtitle">教育背景：</text>
        <view class="education-list">
          <view class="education-item" v-for="(edu, index) in education" :key="index">
            <text class="edu-period">{{ edu.year }}</text>
            <text class="edu-detail">{{ edu.school }} {{ edu.degree }}</text>
          </view>
        </view>
      </view>

      <!-- 联系信息 -->
      <view class="intro-section" v-if="hasContactInfo">
        <text class="intro-subtitle">联系方式：</text>
        <view class="contact-info">
          <view class="contact-item" v-if="profile.phone">
            <SvgIcon name="phone" :size="16" color="#666" />
            <text class="contact-text">{{ profile.phone }}</text>
          </view>
          <view class="contact-item" v-if="profile.email">
            <SvgIcon name="email" :size="16" color="#666" />
            <text class="contact-text">{{ profile.email }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import SvgIcon from '@/components/SvgIcon.vue'

// 定义 props
const props = defineProps({
  // 个人资料信息
  profile: {
    type: Object,
    default: () => ({})
  },
  // 专业标签
  tags: {
    type: [Array, String],
    default: () => []
  },
  // 教育背景
  education: {
    type: Array,
    default: () => []
  },
  // 默认头衔
  defaultTitles: {
    type: Array,
    default: () => ['国家二级心理咨询师', '初级心理治疗师', '中国艾利克森注册催眠治疗师']
  },
  // 默认专业领域
  defaultSpecialties: {
    type: Array,
    default: () => ['抑郁症咨询', '焦虑症治疗', '人际关系指导', '情感咨询']
  }
})

// 计算个人头衔
const titles = computed(() => {
  const result = []
  
  // 添加主要头衔
  if (props.profile.title) {
    result.push(props.profile.title)
  }
  
  // 添加默认头衔（去重）
  props.defaultTitles.forEach(title => {
    if (!result.includes(title)) {
      result.push(title)
    }
  })
  
  return result
})

// 计算专业领域标签
const specialties = computed(() => {
  if (Array.isArray(props.tags)) {
    const filtered = props.tags.filter(tag => tag && tag.trim())
    return filtered.length > 0 ? filtered : props.defaultSpecialties
  } else if (typeof props.tags === 'string' && props.tags) {
    const parsed = props.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
    return parsed.length > 0 ? parsed : props.defaultSpecialties
  }
  return props.defaultSpecialties
})

// 是否有联系信息
const hasContactInfo = computed(() => {
  return !!(props.profile.phone || props.profile.email)
})
</script>

<style lang="scss" scoped>
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
</style> 