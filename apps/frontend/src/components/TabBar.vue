<template>
  <!-- 统一使用自定义TabBar，兼容所有平台 -->
  <view class="custom-tabbar" :style="{ paddingBottom: safeAreaBottom + 'px' }">
    <view class="tabbar-border"></view>
    <view class="tabbar-item" v-for="(item, index) in tabList" :key="index"
      :class="{ 'tabbar-item--active': currentIndex === index }" @click="switchTab(index)">
      <view class="tabbar-item__icon">
        <SvgIcon :name="item.iconName" path="tabbar" :active="currentIndex === index" :size="22"
          :fallbackIcon="item.fallbackIcon" :activeColor="activeColor" :color="inactiveColor" />
      </view>
      <text class="tabbar-item__text" :style="{ color: currentIndex === index ? activeColor : inactiveColor }">
        {{ item.text }}
      </text>
    </view>
  </view>
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

// 切换标签页（使用自定义TabBar，不使用原生switchTab）
const switchTab = (index) => {
  if (currentIndex.value === index || switching) return

  switching = true

  // 添加触觉反馈（支持的平台）
  try {
    uni.vibrateShort({
      type: 'light'
    })
  } catch (e) {
    console.log('震动反馈不支持')
  }

  const targetPath = tabList[index].pagePath

  // 先更新UI状态
  currentIndex.value = index

  // 使用navigateTo实现TabBar页面切换，保持页面状态不刷新
  uni.navigateTo({
    url: targetPath,
    success: () => {
      console.log('TabBar页面切换成功:', targetPath)
      setTimeout(() => {
        switching = false
      }, 300)
    },
    fail: (err) => {
      console.error('TabBar页面切换失败:', err)
      // 如果navigateTo失败（如页面已存在），尝试使用redirectTo
      uni.redirectTo({
        url: targetPath,
        success: () => {
          console.log('TabBar页面redirectTo成功:', targetPath)
          setTimeout(() => {
            switching = false
          }, 300)
        },
        fail: (redirectErr) => {
          console.error('TabBar页面redirectTo也失败:', redirectErr)
          // 失败时恢复状态
          getCurrentIndex()
          setTimeout(() => {
            switching = false
          }, 300)
        }
      })
    }
  })
}

// 获取当前页面路径对应的索引
const getCurrentIndex = () => {
  try {
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
        console.log('TabBar当前索引已更新:', index, basePath)
      } else {
        console.log('当前页面不是TabBar页面:', basePath)
      }
    }
  } catch (error) {
    console.error('获取TabBar当前索引失败:', error)
    // 错误时默认设置为首页
    currentIndex.value = 0
  }
}

onMounted(() => {
  getCurrentIndex()

  // 获取安全区域信息（适用于所有平台）
  try {
    const systemInfo = uni.getSystemInfoSync()
    safeAreaBottom.value = systemInfo.safeAreaInsets ? systemInfo.safeAreaInsets.bottom : 0
    console.log('TabBar安全区域底部高度:', safeAreaBottom.value)
  } catch (error) {
    console.log('获取安全区域信息失败:', error)
    safeAreaBottom.value = 0
  }
})

// 添加页面显示监听，确保TabBar状态与页面同步
uni.$on('onShow', () => {
  setTimeout(() => {
    getCurrentIndex()
  }, 100)
})
</script>

<style lang="scss" scoped>
// 统一自定义TabBar样式，兼容所有平台
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
  z-index: 9999;
  box-sizing: border-box;
  border-top: 1rpx solid #ebeef5;
  will-change: transform;
  /* 优化渲染性能 */
  transform: translateZ(0);
  /* 开启硬件加速 */
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
  transform: scale(0.98);
}

// 添加点击动画
.tabbar-item {
  &:active {
    .tabbar-item__icon {
      transform: scale(0.9);
      transition: transform 0.1s ease;
    }

    .tabbar-item__text {
      opacity: 0.8;
      transition: opacity 0.1s ease;
    }
  }
}

// 适配iPhone X等带有安全区域的设备
@supports (bottom: env(safe-area-inset-bottom)) {
  .custom-tabbar {
    padding-bottom: env(safe-area-inset-bottom);
    height: calc(100rpx + env(safe-area-inset-bottom));
  }
}

// 微信小程序特殊优化
/* #ifdef MP-WEIXIN */
.custom-tabbar {
  box-shadow: 0 -2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.tabbar-item {

  // 微信小程序点击反馈优化
  &:hover {
    background-color: rgba(74, 144, 226, 0.03);
  }
}

/* #endif */

// H5平台优化
/* #ifdef H5 */
.custom-tabbar {
  box-shadow: 0 -2rpx 12rpx rgba(0, 0, 0, 0.08);
}

.tabbar-item {
  cursor: pointer;

  &:hover {
    background-color: rgba(74, 144, 226, 0.03);

    .tabbar-item__icon {
      transform: scale(1.05);
    }
  }
}

/* #endif */

// APP平台优化
/* #ifdef APP-PLUS */
.custom-tabbar {
  backdrop-filter: blur(20rpx);
  -webkit-backdrop-filter: blur(20rpx);
}

/* #endif */
</style>