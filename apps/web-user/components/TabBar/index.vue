<template>
  <view class="tab-bar-container">
    <view class="tab-bar-wrapper">
      <view 
        v-for="(item, index) in tabBarList" 
        :key="index" 
        class="tab-item" 
        :class="{ active: currentTab === item.pagePath }"
        @click="switchTab(item.pagePath)"
      >
        <image :src="currentTab === item.pagePath ? item.selectedIconPath : item.iconPath" class="tab-icon"></image>
        <text class="tab-text" :class="{ 'active-text': currentTab === item.pagePath }">{{ item.text }}</text>
      </view>
    </view>
    <!-- 适配iPhone底部安全区 -->
    <view class="safe-area-inset-bottom"></view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useTheme } from '@/hooks/useTheme';

// 获取主题变量
const theme = useTheme();

// 定义Props
const props = defineProps({
  current: {
    type: String,
    default: '/pages/index/index'
  }
});

// 当前选中标签
const currentTab = ref(props.current);

// 标签列表
const tabBarList = [
  {
    pagePath: '/pages/index/index',
    text: '首页',
    iconPath: '/static/images/tabbar/home.png',
    selectedIconPath: '/static/images/tabbar/home-active.png'
  },
  {
    pagePath: '/pages/order/index',
    text: '订单',
    iconPath: '/static/images/tabbar/order.png',
    selectedIconPath: '/static/images/tabbar/order-active.png'
  },
  {
    pagePath: '/pages/message/index',
    text: '消息',
    iconPath: '/static/images/tabbar/message.png',
    selectedIconPath: '/static/images/tabbar/message-active.png'
  },
  {
    pagePath: '/pages/profile/index',
    text: '我的',
    iconPath: '/static/images/tabbar/profile.png',
    selectedIconPath: '/static/images/tabbar/profile-active.png'
  }
];

// 定义Emits
const emit = defineEmits(['change']);

// 切换标签
const switchTab = (path) => {
  if (currentTab.value === path) return;
  
  currentTab.value = path;
  emit('change', path);
  
  // 跳转到对应页面
  uni.switchTab({
    url: path
  });
};

// 根据当前路径更新选中状态
onMounted(() => {
  const pages = getCurrentPages();
  if (pages.length > 0) {
    const currentPage = pages[pages.length - 1];
    const route = `/${currentPage.route}`;
    
    // 检查是否是tabBar页面，如果是则更新选中状态
    const matchedTab = tabBarList.find(tab => tab.pagePath === route);
    if (matchedTab) {
      currentTab.value = matchedTab.pagePath;
    }
  }
});
</script>

<style lang="scss" scoped>
.tab-bar-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #ffffff;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
  z-index: 999;
}

.tab-bar-wrapper {
  display: flex;
  height: 110rpx;
  justify-content: space-between;
  align-items: center;
  padding: 0 20rpx;
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10rpx 0;
  position: relative;
  
  &.active::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 40rpx;
    height: 4rpx;
    background-color: $uni-color-primary;
    border-radius: 2rpx;
  }
}

.tab-icon {
  width: 44rpx;
  height: 44rpx;
  margin-bottom: 8rpx;
}

.tab-text {
  font-size: 24rpx;
  color: #999999;
  
  &.active-text {
    color: $uni-color-primary;
    font-weight: 500;
  }
}

.safe-area-inset-bottom {
  height: constant(safe-area-inset-bottom);
  height: env(safe-area-inset-bottom);
  background-color: #ffffff;
}
</style>
