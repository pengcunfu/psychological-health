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
// SCSS变量
$primary-color: #4A90E2;
$primary-light: #e6f7ff;
$primary-border: #91d5ff;
$white: #fff;
$text-color: #333;
$text-light: #666;
$text-lighter: #999;
$border-color: #f0f0f0;
$shadow-medium: rgba(0, 0, 0, 0.1);

$padding-large: 30rpx;
$padding-medium: 20rpx;
$padding-small: 15rpx;
$padding-xs: 10rpx;
$padding-tag: 8rpx 12rpx;
$margin-large: 30rpx;
$margin-medium: 20rpx;
$margin-small: 15rpx;
$margin-xs: 10rpx;
$margin-icon: 8rpx;
$margin-text: 5rpx;

$border-radius: 12rpx;
$border-radius-small: 8rpx;
$border-radius-xs: 3rpx;
$indicator-width: 6rpx;
$edu-period-width: 180rpx;

$font-size-title: 32rpx;
$font-size-base: 28rpx;
$font-size-tag: 26rpx;
$font-weight-bold: bold;
$line-height-content: 1.8;

.intro-card {
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
      height: $padding-large;
      background-color: $primary-color;
      margin-right: $margin-xs;
      border-radius: $border-radius-xs;
    }

    .card-title {
      font-size: $font-size-title;
      font-weight: $font-weight-bold;
      color: $text-color;
    }
  }

  .intro-content {
    font-size: $font-size-base;
    color: $text-light;
    line-height: $line-height-content;

    .intro-section {
      margin-bottom: $margin-large;

      &:last-child {
        margin-bottom: 0;
      }

      .intro-subtitle {
        font-size: $font-size-base;
        color: $text-lighter;
        margin-bottom: $margin-small;
        display: block;
      }

      .intro-tags {
        display: flex;
        flex-wrap: wrap;
        gap: $margin-xs;

        .intro-tag {
          font-size: $font-size-tag;
          color: $primary-color;
          background-color: $primary-light;
          padding: $padding-tag;
          border-radius: $border-radius-small;
          border: 1rpx solid $primary-border;
        }
      }

      .intro-text {
        margin-top: $margin-xs;
      }

      .specialty-tags {
        display: flex;
        flex-wrap: wrap;
        gap: $margin-xs;

        .specialty-tag {
          font-size: $font-size-tag;
          color: $primary-color;
          background-color: $primary-light;
          padding: $padding-tag;
          border-radius: $border-radius-small;
          border: 1rpx solid $primary-border;
        }
      }

      .education-list {
        margin-top: $margin-xs;

        .education-item {
          display: flex;
          margin-bottom: $margin-small;
          padding-bottom: $margin-small;
          border-bottom: 1rpx solid $border-color;

          &:last-child {
            border-bottom: none;
            margin-bottom: 0;
          }

          .edu-period {
            font-size: $font-size-tag;
            color: $text-lighter;
            width: $edu-period-width;
            flex-shrink: 0;
          }

          .edu-detail {
            font-size: $font-size-base;
            color: $text-color;
            font-weight: $font-weight-bold;
            display: block;
            margin-bottom: $margin-text;
          }
        }
      }

      .contact-info {
        margin-top: $margin-small;

        .contact-item {
          display: flex;
          align-items: center;
          margin-bottom: $margin-xs;

          &:last-child {
            margin-bottom: 0;
          }

          .contact-text {
            font-size: $font-size-base;
            color: $text-light;
            margin-left: $margin-icon;
          }
        }
      }
    }
  }
}
</style>