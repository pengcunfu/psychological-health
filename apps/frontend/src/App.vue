<template>
  <view class="app-container">
    <!-- 页面内容区域 -->
    <view class="page-content" :class="{ 
      'has-tabbar': showTabbar,
      'tab-page': isTabBarPage 
    }">
      <!-- uni-app 使用页面栈，这里作为内容容器 -->
      <view class="content-wrapper">
        <slot />
      </view>
    </view>

    <!-- 全局底部TabBar，只在指定的四个页面显示 -->
    <TabBar v-if="showTabbar" />
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { useUserStore } from './store/user'
import TabBar from './components/TabBar.vue'

// Store
const userStore = useUserStore()

// 页面状态
const currentRoute = ref('')

// TabBar页面列表 - 只有这四个页面显示TabBar
const tabBarPages = [
  '/pages/index',
  'pages/index',  // 兼容不同的路由格式
  '/pages/counselor/index', 
  'pages/counselor/index',
  '/pages/course/index',
  'pages/course/index',
  '/pages/profile/index',
  'pages/profile/index'
]

// 计算属性
const isTabBarPage = computed(() => {
  const result = tabBarPages.includes(currentRoute.value)
  console.log(`TabBar检查 - 当前路由: ${currentRoute.value}, 是否TabBar页面: ${result}`)
  return result
})

const showTabbar = computed(() => {
  const result = isTabBarPage.value
  console.log(`TabBar显示状态: ${result}`)
  return result
})

// Navbar由各个子页面自己控制，App.vue不再管理

// 获取当前页面路由
const getCurrentRoute = () => {
  try {
    const pageStack = getCurrentPages()
    console.log('页面栈:', pageStack)
    if (pageStack.length > 0) {
      const currentPage = pageStack[pageStack.length - 1]
      const route = '/' + currentPage.route
      currentRoute.value = route
      console.log('当前页面路由:', route)
      console.log('TabBar页面列表:', tabBarPages)
      console.log('是否包含当前路由:', tabBarPages.includes(route))
    }
  } catch (error) {
    console.error('获取当前路由失败:', error)
  }
}

// 生命周期
onLaunch(() => {
  console.log('App Launch')
  userStore.initUserInfo()
  getCurrentRoute()
})

onShow(() => {
  console.log('App Show')
  // 延迟获取路由，确保页面完全加载
  setTimeout(() => {
    getCurrentRoute()
  }, 100)
})

onHide(() => {
  console.log('App Hide')
})

onMounted(() => {
  getCurrentRoute()
  
  // 监听页面栈变化
  const originalNavigateTo = uni.navigateTo
  const originalNavigateBack = uni.navigateBack
  const originalRedirectTo = uni.redirectTo
  const originalReLaunch = uni.reLaunch
  
  uni.navigateTo = function(options) {
    return originalNavigateTo.call(this, {
      ...options,
      success: (...args) => {
        setTimeout(getCurrentRoute, 100)
        options.success && options.success(...args)
      }
    })
  }
  
  uni.navigateBack = function(options = {}) {
    return originalNavigateBack.call(this, {
      ...options,
      success: (...args) => {
        setTimeout(getCurrentRoute, 100)
        options.success && options.success(...args)
      }
    })
  }
  
  uni.redirectTo = function(options) {
    return originalRedirectTo.call(this, {
      ...options,
      success: (...args) => {
        setTimeout(getCurrentRoute, 100)
        options.success && options.success(...args)
      }
    })
  }
  
  uni.reLaunch = function(options) {
    return originalReLaunch.call(this, {
      ...options,
      success: (...args) => {
        setTimeout(getCurrentRoute, 100)
        options.success && options.success(...args)
      }
    })
  }
})

// 暴露给模板的数据和方法
defineExpose({
  currentRoute,
  getCurrentRoute
})
</script>

<style lang="scss">
/* 引入uni基础样式 */
@import "./uni.scss";

/* 引入uView基础样式 */
@import "uview-plus/index.scss";

/* 引入自定义全局样式 */
@import "./static/global.scss";

/* 引入主题样式 */
@import "./static/theme.scss";

page {
  background-color: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica,
    Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei',
    sans-serif;
  color: #333;
  font-size: 28rpx;
  line-height: 1.6;
}

.app-container {
  min-height: 100vh;
  position: relative;
  background-color: #f5f7fa;
}

.page-content {
  position: relative;
  min-height: 100vh;
  
  &.has-tabbar {
    padding-bottom: calc(100rpx + env(safe-area-inset-bottom));
  }
  
  &.tab-page {
    padding-bottom: calc(100rpx + env(safe-area-inset-bottom));
  }
}

.content-wrapper {
  width: 100%;
  min-height: 100%;
}

/* 微信小程序专用的TabBar间距 */
/* #ifdef MP-WEIXIN */
.page-content.has-tabbar,
.page-content.tab-page {
  padding-bottom: 120rpx; /* 微信小程序固定高度 */
}
/* #endif */

/* 安全区域适配 */
@supports (bottom: env(safe-area-inset-bottom)) {
  .page-content.has-tabbar,
  .page-content.tab-page {
    padding-bottom: calc(100rpx + env(safe-area-inset-bottom));
  }
}

/* 过渡动画 */
.page-content {
  transition: padding 0.3s ease;
}

/* 响应式布局 */
@media (max-width: 750rpx) {
  .page-content {
    font-size: 26rpx;
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .app-container {
    background-color: #1a1a1a;
    color: #ffffff;
  }
}
</style>
