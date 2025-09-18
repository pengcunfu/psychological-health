<template>
  <view class="nav-grid">
    <view 
      class="nav-item" 
      v-for="(item, index) in menuItems" 
      :key="index" 
      @click="handleMenuClick(item)"
    >
      <view class="nav-icon" :style="{ backgroundColor: item.bgColor }">
        <SvgIcon 
          :name="item.iconName" 
          path="index"
          :size="48"
          :color="item.color"
          :fallbackIcon="item.fallbackIcon"
        />
      </view>
      <text class="nav-text">{{ item.name }}</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import SvgIcon from '@/components/SvgIcon.vue'
import { navigateTo } from '@/utils/link'

// 定义 props
const props = defineProps({
  // 菜单数据，允许外部传入自定义菜单
  menuData: {
    type: Array,
    default: () => []
  }
})

// 定义 emits
const emit = defineEmits(['menuClick'])

// 默认菜单数据
const defaultMenuItems = [
  { 
    name: '咨询预约', 
    color: '#1890ff', 
    bgColor: '#e6f7ff',
    url: '/pages/counselor/index',
    iconName: 'counselor',
    fallbackIcon: 'calendar-fill'
  },
  { 
    name: '课程学习', 
    color: '#eb2f96', 
    bgColor: '#fff0f6',
    url: '/pages/course/index',
    iconName: 'course',
    fallbackIcon: 'play-circle-fill'
  },
  { 
    name: '心理测评', 
    color: '#52c41a', 
    bgColor: '#f6ffed',
    url: '/pages/assessment/index',
    iconName: 'evaluate',
    fallbackIcon: 'checkmark-circle-fill'
  },
  { 
    name: '互动社区', 
    color: '#fa8c16', 
    bgColor: '#fff7e6',
    url: '/pages/social/index',
    iconName: 'community',
    fallbackIcon: 'account-fill'
  }
]

// 计算使用的菜单数据
const menuItems = ref(props.menuData.length > 0 ? props.menuData : defaultMenuItems)

// 菜单点击处理
const handleMenuClick = (item) => {
  // 发送点击事件给父组件
  emit('menuClick', item)
  
  // 默认行为：导航到对应页面
  if (item.url) {
    navigateTo(item.url)
  }
}
</script>

<style lang="scss" scoped>
// SCSS变量
$grid-columns: 4;
$margin-base: 20rpx;
$margin-icon: 16rpx;
$padding-base: 20rpx;
$white: #fff;
$text-color: #333;
$border-radius: 16rpx;
$icon-size: 100rpx;
$font-size-text: 24rpx;
$line-height-text: 1.2;
$transition-fast: 0.2s ease;
$transition-medium: 0.3s ease;
$scale-active: 0.95;
$scale-icon-active: 0.9;

.nav-grid {
  display: grid;
  grid-template-columns: repeat($grid-columns, 1fr);
  margin: $margin-base;
  margin-top: 0;
  padding: $padding-base;
  background-color: $white;
  border-radius: $border-radius;
  overflow: hidden;

  .nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: $padding-base;
    transition: transform $transition-fast;

    &:active {
      transform: scale($scale-active);

      .nav-icon {
        transform: scale($scale-icon-active);
      }
    }

    .nav-icon {
      width: $icon-size;
      height: $icon-size;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: $margin-icon;
      transition: all $transition-medium;
    }

    .nav-text {
      font-size: $font-size-text;
      color: $text-color;
      text-align: center;
      line-height: $line-height-text;
    }
  }
}
</style> 