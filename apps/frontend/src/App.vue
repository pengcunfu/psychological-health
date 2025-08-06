<template>
  <view>
    <tab-bar v-if="showTabBar"></tab-bar>
  </view>
</template>

<script>
import { ref, computed } from 'vue'
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { useUserStore } from './store/user'
import TabBar from '@/components/TabBar.vue'

export default {
  components: {
    TabBar
  },
  setup() {
    const userStore = useUserStore()
    const showTabBar = ref(true)
    
    // 检查当前页面是否是tabBar页面
    const checkTabBarPage = () => {
      const pages = getCurrentPages()
      if (pages.length > 0) {
        const currentPage = pages[pages.length - 1]
        const route = '/' + currentPage.route
        
        // tabBar页面路径
        const tabBarPaths = [
          '/pages/index/index',
          '/pages/counselor/index',
          '/pages/course/index',
          '/pages/profile/index'
        ]
        
        showTabBar.value = tabBarPaths.includes(route)
        
        // 发送事件通知TabBar组件更新当前页面
        if (showTabBar.value) {
          uni.$emit('tabBarPageShow')
        }
      }
    }
    
    onLaunch(() => {
      console.log('App Launch')
      // 初始化用户信息
      userStore.initUserInfo()
    })
    
    onShow(() => {
      console.log('App Show')
      checkTabBarPage()
    })
    
    onHide(() => {
      console.log('App Hide')
    })
    
    return {
      showTabBar
    }
  }
}
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

/* 为底部TabBar预留空间 */
.page-container {
  padding-bottom: calc(100rpx + env(safe-area-inset-bottom));
}

/* TabBar页面底部预留空间 */
.tab-page {
  padding-bottom: calc(100rpx + env(safe-area-inset-bottom));
}
</style>
