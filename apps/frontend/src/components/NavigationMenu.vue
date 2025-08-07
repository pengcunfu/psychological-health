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
    url: '/pages/community/index',
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
.nav-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  padding: 40rpx 20rpx;
  background-color: #fff;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx;
  transition: transform 0.2s ease;
}

.nav-item:active {
  transform: scale(0.95);
}

.nav-icon {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16rpx;
  transition: all 0.3s ease;
}

.nav-item:active .nav-icon {
  transform: scale(0.9);
}

.nav-text {
  font-size: 24rpx;
  color: #333;
  text-align: center;
  line-height: 1.2;
}
</style> 