<template>
  <view class="tab-bar">
    <view 
      class="tab-item" 
      v-for="(item, index) in tabList" 
      :key="index"
      @click="switchTab(item.pagePath)"
    >
      <view class="tab-icon">
        <image 
          :src="currentPath === item.pagePath ? item.selectedIconPath : item.iconPath" 
          class="tab-icon-img"
          mode="aspectFit"
        ></image>
      </view>
      <view 
        class="tab-text" 
        :class="{ active: currentPath === item.pagePath }"
      >
        {{ item.text }}
      </view>
    </view>
  </view>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'

export default {
  setup() {
    const currentPath = ref('')
    
    const tabList = reactive([
      {
        pagePath: '/pages/index/index',
        iconPath: '/static/images/tabbar/home.svg',
        selectedIconPath: '/static/images/tabbar/home-active.svg',
        text: '首页'
      },
      {
        pagePath: '/pages/counselor/index',
        iconPath: '/static/images/tabbar/counselor.svg',
        selectedIconPath: '/static/images/tabbar/counselor-active.svg',
        text: '咨询'
      },
      {
        pagePath: '/pages/course/index',
        iconPath: '/static/images/tabbar/course.svg',
        selectedIconPath: '/static/images/tabbar/course-active.svg',
        text: '课程'
      },
      {
        pagePath: '/pages/profile/index',
        iconPath: '/static/images/tabbar/profile.svg',
        selectedIconPath: '/static/images/tabbar/profile-active.svg',
        text: '我的'
      }
    ])
    
    // 切换标签页
    const switchTab = (path) => {
      if (currentPath.value === path) return
      
      uni.switchTab({
        url: path
      })
    }
    
    // 获取当前页面路径
    const getCurrentPath = () => {
      const pages = getCurrentPages()
      if (pages.length > 0) {
        const currentPage = pages[pages.length - 1]
        const route = '/' + currentPage.route
        
        // 检查是否是tabBar页面（需要去掉可能的参数）
        const basePath = route.split('?')[0]
        
        // 检查是否是tabBar页面
        const isTabBarPage = tabList.some(item => item.pagePath === basePath)
        
        if (isTabBarPage) {
          currentPath.value = basePath
        }
      }
    }
    
    onMounted(() => {
      getCurrentPath()
    })
    
    // 监听页面显示
    uni.$on('tabBarPageShow', () => {
      getCurrentPath()
    })
    
    return {
      currentPath,
      tabList,
      switchTab
    }
  }
}
</script>

<style lang="scss">
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100rpx;
  background-color: #fff;
  display: flex;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
  z-index: 100;
  padding-bottom: env(safe-area-inset-bottom);
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.tab-icon {
  margin-bottom: 6rpx;
}

.tab-icon-img {
  width: 44rpx;
  height: 44rpx;
}

.tab-text {
  font-size: 24rpx;
  color: #999;
}

.tab-text.active {
  color: #4A90E2;
  font-weight: bold;
}
</style> 