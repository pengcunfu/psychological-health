<template>
  <!-- uni-app的App.vue模板通常不渲染，页面内容由各个page组件渲染 -->
</template>

<script setup>
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { useUserStore } from './store/user'

// Store
const userStore = useUserStore()

// 生命周期
onLaunch(() => {
  console.log('App Launch')
  userStore.initUserInfo()
})

onShow(() => {
  console.log('App Show')
})

onHide(() => {
  console.log('App Hide')
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
