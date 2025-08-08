<template>
  <!-- 统一使用自定义TabBar，兼容所有平台 -->
  <view class="custom-tabbar" :style="{ paddingBottom: safeAreaBottom + 'px' }" v-if="currentIndex >= 0">
    <view class="tabbar-border"></view>
    <view class="tabbar-item" v-for="(item, index) in tabList" :key="index" :class="{
      'tabbar-item--active': currentIndex === index,
      'tabbar-item--switching': switching && switchingIndex === index
    }" @click="switchTab(index)">

      <!-- 波纹动画背景 -->
      <view class="tabbar-item__ripple" :class="{ 'ripple-active': currentIndex === index }"></view>

      <!-- 活跃指示器 -->
      <view class="tabbar-item__indicator" :class="{ 'indicator-active': currentIndex === index }"></view>

      <!-- 图标容器 -->
      <view class="tabbar-item__icon" :class="{ 'icon-bounce': switching && switchingIndex === index }">
        <SvgIcon :name="item.iconName" path="tabbar" :active="currentIndex === index" :size="22"
          :fallbackIcon="item.fallbackIcon" :activeColor="activeColor" :color="inactiveColor" />
      </view>

      <!-- 文字标签 -->
      <text class="tabbar-item__text" :class="{ 'text-slide-up': switching && switchingIndex === index }"
        :style="{ color: currentIndex === index ? activeColor : inactiveColor }">
        {{ item.text }}
      </text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SvgIcon from './SvgIcon.vue'

const currentIndex = ref(-1)  // 初始化为-1，等待获取真实索引
const switchingIndex = ref(-1)  // 跟踪正在切换的项目索引

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

// 切换标签页（使用页面跳转，保持原有架构）
const switchTab = (index) => {
  // 验证索引范围
  if (index < 0 || index > 3 || index >= tabList.length) {
    return
  }

  if (currentIndex.value === index || switching) return

  switching = true
  switchingIndex.value = index  // 设置正在切换的索引

  // 添加触觉反馈（支持的平台）
  try {
    uni.vibrateShort({
      type: 'light'
    })
  } catch (e) {
  }

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
  }
}

onMounted(() => {

  // 获取安全区域信息（适用于所有平台）
  try {
    const systemInfo = uni.getSystemInfoSync()
    safeAreaBottom.value = systemInfo.safeAreaInsets ? systemInfo.safeAreaInsets.bottom : 0
  } catch (error) {
    safeAreaBottom.value = 0
  }

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
$shadow-light: rgba(0, 0, 0, 0.08);
$shadow-medium: rgba(0, 0, 0, 0.1);
$shadow-strong: rgba(0, 0, 0, 0.12);
$ripple-color: rgba(74, 144, 226, 0.1);
$tabbar-height: 100rpx;
$icon-size: 44rpx;
$text-size: 20rpx;
$z-index-tabbar: 9999;

// 动画缓动函数
$ease-out-cubic: cubic-bezier(0.4, 0, 0.2, 1);
$ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);

// 统一自定义TabBar样式，兼容所有平台
.custom-tabbar {
  position: fixed !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  width: 100% !important;
  height: $tabbar-height !important;
  background-color: $white !important;
  display: flex !important;
  align-items: center;
  justify-content: space-around;
  z-index: $z-index-tabbar !important;
  box-sizing: border-box;
  border-top: 1rpx solid $border-color;
  will-change: transform;
  /* 优化渲染性能 */
  transform: translateZ(0);
  /* 开启硬件加速 */
  /* 调试样式 - 确保可见 */
  min-height: $tabbar-height !important;
  visibility: visible !important;
  opacity: 1 !important;

  .tabbar-border {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1rpx;
    background-color: $border-color;
  }

  .tabbar-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: $tabbar-height;
    position: relative;
    overflow: hidden;
    transition: all 0.3s $ease-out-cubic;

    // 波纹动画背景
    &__ripple {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 0;
      height: 0;
      background: radial-gradient(circle, $ripple-color 0%, rgba(74, 144, 226, 0) 70%);
      border-radius: 50%;
      transform: translate(-50%, -50%);
      transition: all 0.3s $ease-out-cubic;
      pointer-events: none;

      &.ripple-active {
        width: 120rpx;
        height: 120rpx;
      }
    }

    // 活跃指示器
    &__indicator {
      position: absolute;
      top: 8rpx;
      left: 50%;
      width: 0;
      height: 6rpx;
      background: linear-gradient(90deg, $primary-color, $primary-light);
      border-radius: 3rpx;
      transform: translateX(-50%);
      transition: all 0.3s $ease-out-cubic;

      &.indicator-active {
        width: 40rpx;
      }
    }

    // 图标容器
    &__icon {
      width: $icon-size;
      height: $icon-size;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 4rpx;
      position: relative;
      z-index: 2;
      transition: all 0.3s $ease-out-cubic;

      // 图标弹跳动画
      &.icon-bounce {
        animation: iconBounce 0.4s $ease-bounce;
      }
    }

    // 文字标签
    &__text {
      font-size: $text-size;
      line-height: 1;
      text-align: center;
      position: relative;
      z-index: 2;
      transition: all 0.3s $ease-out-cubic;

      // 文字滑动动画
      &.text-slide-up {
        animation: textSlideUp 0.3s $ease-out-cubic;
      }
    }

    // 激活状态
    &--active {
      .tabbar-item__text {
        font-weight: 500;
        transform: scale(1.05);
      }

      .tabbar-item__icon {
        transform: scale(1.1);
        animation: activePulse 2s ease-in-out infinite;
      }
    }

    // 切换中的状态
    &--switching {
      .tabbar-item__icon {
        transform: scale(0.9);
      }
    }

    // 点击效果
    &:active {
      .tabbar-item__icon {
        transform: scale(0.95);
      }

      .tabbar-item__ripple {
        animation: rippleEffect 0.6s $ease-out-cubic;
      }
    }

    // 悬停效果
    &:hover {
      .tabbar-item__ripple {
        width: 60rpx;
        height: 60rpx;
        opacity: 0.3;
      }
    }
  }
}

// 关键帧动画定义
@keyframes iconBounce {
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(0.8);
  }

  70% {
    transform: scale(1.2);
  }

  100% {
    transform: scale(1.1);
  }
}

@keyframes textSlideUp {
  0% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }

  50% {
    transform: translateY(-4rpx) scale(0.95);
    opacity: 0.7;
  }

  100% {
    transform: translateY(0) scale(1.05);
    opacity: 1;
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

@keyframes activePulse {

  0%,
  100% {
    transform: scale(1.1);
  }

  50% {
    transform: scale(1.15);
  }
}



// 适配iPhone X等带有安全区域的设备
@supports (bottom: env(safe-area-inset-bottom)) {
  .custom-tabbar {
    padding-bottom: env(safe-area-inset-bottom);
    height: calc(#{$tabbar-height} + env(safe-area-inset-bottom));
  }
}

// 平台特定优化
/* #ifdef MP-WEIXIN */
.custom-tabbar {
  box-shadow: 0 -2rpx 8rpx $shadow-medium;
}

.tabbar-item {

  // 微信小程序点击反馈优化
  &:hover {
    .tabbar-item__ripple {
      width: 70rpx;
      height: 70rpx;
      opacity: 0.15;
    }

    .tabbar-item__icon {
      transform: scale(1.03);
    }
  }
}

/* #endif */

/* #ifdef H5 */
.custom-tabbar {
  box-shadow: 0 -2rpx 12rpx $shadow-light;
}

.tabbar-item {
  cursor: pointer;

  &:hover {
    .tabbar-item__ripple {
      width: 80rpx;
      height: 80rpx;
      opacity: 0.2;
    }

    .tabbar-item__icon {
      transform: scale(1.05);
    }

    .tabbar-item__text {
      transform: scale(1.02);
    }
  }
}

/* #endif */

/* #ifdef APP-PLUS */
.custom-tabbar {
  backdrop-filter: blur(20rpx);
  -webkit-backdrop-filter: blur(20rpx);
}

/* #endif */
</style>