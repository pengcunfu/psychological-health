<template>
  <u-tabbar
    :value="currentIndex"
    @change="handleChange"
    :fixed="true"
    :placeholder="true"
    :safeAreaInsetBottom="true"
    :activeColor="activeColor"
    :inactiveColor="inactiveColor"
    :border="true"
    :zIndex="9999"
    v-if="currentIndex >= 0"
  >
    <u-tabbar-item 
      v-for="(item, index) in tabList" 
      :key="index"
      :text="item.text" 
      :icon="getIcon(item, index)"
      @click="switchTab(index)"
    ></u-tabbar-item>
  </u-tabbar>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const currentIndex = ref(-1)  // 初始化为-1，等待获取真实索引
const switchingIndex = ref(-1)  // 跟踪正在切换的项目索引

// TabBar颜色配置
const activeColor = ref('#4A90E2')
const inactiveColor = ref('#999999')

const tabList = [
  {
    pagePath: '/pages/index',
    iconName: 'home-fill',
    iconInactive: 'home',
    text: '首页',
    fallbackIcon: 'home'
  },
  {
    pagePath: '/pages/counselor/index',
    iconName: 'chat-fill',
    iconInactive: 'chat',
    text: '咨询',
    fallbackIcon: 'message'
  },
  {
    pagePath: '/pages/course/index',
    iconName: 'play-circle-fill',
    iconInactive: 'play-circle',
    text: '课程',
    fallbackIcon: 'play-circle'
  },
  {
    pagePath: '/pages/profile/index',
    iconName: 'account-fill',
    iconInactive: 'account',
    text: '我的',
    fallbackIcon: 'account'
  }
]

// 防抖标识
let switching = false

// 根据激活状态获取图标
const getIcon = (item, index) => {
  return currentIndex.value === index ? item.iconName : item.iconInactive
}

// 处理 up-tabbar 的 change 事件
const handleChange = (index) => {
  if (currentIndex.value !== index && !switching) {
    switchTab(index)
  }
}

// 切换标签页（使用页面跳转，保持原有架构）
const switchTab = (index) => {
  // 验证索引范围
  if (index < 0 || index > 3 || index >= tabList.length) {
    return
  }

  if (currentIndex.value === index || switching) return

  switching = true
  switchingIndex.value = index  // 设置正在切换的索引

  const targetPath = tabList[index].pagePath

  // 延迟更新索引，先播放动画
  setTimeout(() => {
    currentIndex.value = index
  }, 100)

  // 检查当前页面是否为TabBar页面，决定使用何种跳转方式
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  const currentRoute = '/' + currentPage.route
  const isCurrentTabPage = tabList.some(item => item.pagePath === currentRoute)

  if (isCurrentTabPage) {
    // 如果当前在TabBar页面，使用redirectTo直接替换
    uni.redirectTo({
      url: targetPath,
      success: () => {
        setTimeout(() => {
          switching = false
          switchingIndex.value = -1  // 重置切换索引
        }, 300)
      },
      fail: (err) => {
        // 如果redirectTo失败，尝试reLaunch
        uni.reLaunch({
          url: targetPath,
          success: () => {
            setTimeout(() => {
              switching = false
              switchingIndex.value = -1  // 重置切换索引
            }, 300)
          },
          fail: (reLaunchErr) => {
            // 失败时恢复状态
            getCurrentIndex()
            setTimeout(() => {
              switching = false
              switchingIndex.value = -1  // 重置切换索引
            }, 300)
          }
        })
      }
    })
  } else {
    // 如果不在TabBar页面，使用navigateTo
    uni.navigateTo({
      url: targetPath,
      success: () => {
        setTimeout(() => {
          switching = false
          switchingIndex.value = -1  // 重置切换索引
        }, 300)
      },
      fail: (err) => {
        // 失败时使用reLaunch
        uni.reLaunch({
          url: targetPath,
          success: () => {
            setTimeout(() => {
              switching = false
              switchingIndex.value = -1  // 重置切换索引
            }, 300)
          },
          fail: (reLaunchErr) => {
            // 失败时恢复状态
            getCurrentIndex()
            setTimeout(() => {
              switching = false
              switchingIndex.value = -1  // 重置切换索引
            }, 300)
          }
        })
      }
    })
  }
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
      if (index !== -1 && index >= 0 && index <= 3) {
        // 确保索引在有效范围内
        currentIndex.value = index
      } else {
        // 不改变当前索引，保持TabBar状态
      }
    }
  } catch (error) {
    // 错误时不改变当前索引，避免跳转到错误页面
    console.error('获取当前页面索引失败:', error)
  }
}

onMounted(() => {
  // 立即获取当前索引，不设置默认值
  getCurrentIndex()

  // 如果获取失败或不是TabBar页面，则设置为首页
  setTimeout(() => {
    if (currentIndex.value < 0 || currentIndex.value > 3) {
      currentIndex.value = 0
    }
  }, 100)
})

// 添加页面显示监听，确保TabBar状态与页面同步
uni.$on('onShow', () => {
  setTimeout(() => {
    getCurrentIndex()
  }, 100)
})
</script>

<style lang="scss" scoped>
// SCSS变量
$primary-color: #4A90E2;
$primary-light: #74B3F7;
$white: #ffffff;
$border-color: #ebeef5;
$text-color: #333;
$text-lighter: #999999;

// 自定义up-tabbar样式覆盖
::v-deep .u-tabbar {
  border-top: 1rpx solid $border-color;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(20rpx);
  -webkit-backdrop-filter: blur(20rpx);
}

::v-deep .u-tabbar-item {
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

::v-deep .u-tabbar-item__icon {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

::v-deep .u-tabbar-item__text {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

// 激活状态样式增强
::v-deep .u-tabbar-item--active .u-tabbar-item__icon {
  transform: scale(1.1);
  animation: activePulse 2s ease-in-out infinite;
}

::v-deep .u-tabbar-item--active .u-tabbar-item__text {
  font-weight: 500;
  transform: scale(1.05);
}

// 添加活跃指示器
::v-deep .u-tabbar-item--active::before {
  content: '';
  position: absolute;
  top: 8rpx;
  left: 50%;
  width: 40rpx;
  height: 6rpx;
  background: linear-gradient(90deg, $primary-color, $primary-light);
  border-radius: 3rpx;
  transform: translateX(-50%);
  opacity: 1;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

// 波纹效果
::v-deep .u-tabbar-item::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(74, 144, 226, 0.1) 0%, rgba(74, 144, 226, 0) 70%);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
}

// 悬停效果
::v-deep .u-tabbar-item:hover::after {
  width: 75rpx;
  height: 75rpx;
  opacity: 0.18;
}

::v-deep .u-tabbar-item:hover .u-tabbar-item__icon {
  transform: scale(1.04);
}

::v-deep .u-tabbar-item:hover .u-tabbar-item__text {
  transform: scale(1.02);
}

// 点击效果
::v-deep .u-tabbar-item:active .u-tabbar-item__icon {
  transform: scale(0.95);
}

::v-deep .u-tabbar-item:active::after {
  animation: rippleEffect 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

// 关键帧动画定义
@keyframes activePulse {
  0%, 100% {
    transform: scale(1.1);
  }
  50% {
    transform: scale(1.15);
  }
}

@keyframes rippleEffect {
  0% {
    width: 0;
    height: 0;
    opacity: 0.8;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    width: 120rpx;
    height: 120rpx;
    opacity: 0;
  }
}
</style>
