<template>
  <!-- 微信小程序自定义TabBar -->
  <!-- #ifdef MP-WEIXIN -->
  <view class="custom-tabbar" :style="{ paddingBottom: safeAreaBottom + 'px' }">
    <view class="tabbar-border"></view>
    <view 
      class="tabbar-item"
      v-for="(item, index) in tabList"
      :key="index"
      :class="{ 'tabbar-item--active': currentIndex === index }"
      @click="switchTab(index)"
    >
      <view class="tabbar-item__icon">
        <SvgIcon 
          :name="item.iconName" 
          path="tabbar"
          :active="currentIndex === index"
          :size="22"
          :fallbackIcon="item.fallbackIcon"
          :activeColor="activeColor"
          :color="inactiveColor"
        />
      </view>
      <text class="tabbar-item__text" :style="{ color: currentIndex === index ? activeColor : inactiveColor }">
        {{ item.text }}
      </text>
    </view>
  </view>
  <!-- #endif -->
  
  <!-- 其他平台使用uView TabBar -->
  <!-- #ifndef MP-WEIXIN -->
  <u-tabbar
    :value="currentIndex"
    @change="switchTab"
    :fixed="true"
    :safeAreaInsetBottom="true"
    activeColor="#4A90E2"
    inactiveColor="#999999"
    :border="false"
  >
    <u-tabbar-item
      v-for="(item, index) in tabList"
      :key="index"
      :text="item.text"
    >
      <template #active-icon>
        <SvgIcon 
          :name="item.iconName" 
          path="tabbar"
          :active="true"
          :size="44"
          :fallbackIcon="item.fallbackIcon"
        />
      </template>
      <template #inactive-icon>
        <SvgIcon 
          :name="item.iconName" 
          path="tabbar"
          :active="false"
          :size="44"
          :fallbackIcon="item.fallbackIcon"
        />
      </template>
    </u-tabbar-item>
  </u-tabbar>
  <!-- #endif -->
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SvgIcon from './SvgIcon.vue'

const currentIndex = ref(0)

// TabBar颜色配置
const activeColor = ref('#4A90E2')
const inactiveColor = ref('#999999')

// 安全区域底部高度
const safeAreaBottom = ref(0)

const tabList = [
  {
    pagePath: '/pages/index',
    iconName: 'home',
    text: '首页',
    fallbackIcon: 'home'
  },
  {
    pagePath: '/pages/counselor/index',
    iconName: 'counselor',
    text: '咨询',
    fallbackIcon: 'account'
  },
  {
    pagePath: '/pages/course/index',
    iconName: 'course',
    text: '课程',
    fallbackIcon: 'play-circle'
  },
  {
    pagePath: '/pages/profile/index',
    iconName: 'profile',
    text: '我的',
    fallbackIcon: 'account-circle'
  }
]

// 防抖标识
let switching = false

// 切换标签页
const switchTab = (index) => {
  if (currentIndex.value === index || switching) return
  
  switching = true
  const targetPath = tabList[index].pagePath
  
  // 先更新UI状态
  currentIndex.value = index
  
  uni.switchTab({
    url: targetPath,
    success: () => {
      console.log('TabBar切换成功:', targetPath)
      setTimeout(() => {
        switching = false
      }, 300)
    },
    fail: (err) => {
      console.error('TabBar切换失败:', err)
      // 失败时恢复状态
      getCurrentIndex()
      setTimeout(() => {
        switching = false
      }, 300)
    }
  })
}

// 获取当前页面路径对应的索引
const getCurrentIndex = () => {
  const pages = getCurrentPages()
  if (pages.length > 0) {
    const currentPage = pages[pages.length - 1]
    const route = '/' + currentPage.route
    
    // 检查是否是tabBar页面（需要去掉可能的参数）
    const basePath = route.split('?')[0]
    
    // 找到对应的索引
    const index = tabList.findIndex(item => item.pagePath === basePath)
    if (index !== -1) {
      currentIndex.value = index
    }
  }
}

onMounted(() => {
  getCurrentIndex()
  
  // 获取安全区域信息
  // #ifdef MP-WEIXIN
  const systemInfo = uni.getSystemInfoSync()
  safeAreaBottom.value = systemInfo.safeAreaInsets ? systemInfo.safeAreaInsets.bottom : 0
  // #endif
})

// 监听页面显示
uni.$on('tabBarPageShow', () => {
  getCurrentIndex()
})
</script>

<style lang="scss" scoped>
// 微信小程序自定义TabBar样式
/* #ifdef MP-WEIXIN */
.custom-tabbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100rpx;
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-around;
  z-index: 1000;
  box-sizing: border-box;
  border-top: 1rpx solid #ebeef5;
}

.tabbar-border {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1rpx;
  background-color: #ebeef5;
}

.tabbar-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100rpx;
  position: relative;
  transition: all 0.2s ease;
}

.tabbar-item__icon {
  width: 44rpx;
  height: 44rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4rpx;
}

.tabbar-item__text {
  font-size: 20rpx;
  line-height: 1;
  text-align: center;
  transition: color 0.2s ease;
}

.tabbar-item--active .tabbar-item__text {
  font-weight: 500;
}

// 添加点击效果
.tabbar-item:active {
  background-color: rgba(74, 144, 226, 0.05);
  border-radius: 8rpx;
}

// 适配iPhone X等带有安全区域的设备
@supports (bottom: env(safe-area-inset-bottom)) {
  .custom-tabbar {
    padding-bottom: env(safe-area-inset-bottom);
    height: calc(100rpx + env(safe-area-inset-bottom));
  }
}
/* #endif */

// 其他平台的uView TabBar样式优化
/* #ifndef MP-WEIXIN */
:deep(.u-tabbar-item__icon) {
  margin-bottom: 4rpx !important;
}

:deep(.u-tabbar-item__text) {
  font-size: 20rpx !important;
}

:deep(.u-tabbar) {
  background-color: #ffffff !important;
  border-top: 1rpx solid #ebeef5 !important;
}
/* #endif */
</style> 