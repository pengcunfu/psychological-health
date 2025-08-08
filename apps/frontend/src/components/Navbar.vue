<template>
  <view>
    <!-- 自定义导航栏 -->
    <view class="custom-navbar">
      <!-- 状态栏占位 -->
      <view class="status-bar" :style="{ height: statusBarHeight + 'px' }"></view>
      
      <!-- 导航栏内容 -->
      <view class="navbar-content">
        <!-- 左侧 -->
        <view class="navbar-left" @click="handleLeftClick" v-if="showLeft">
          <view class="navbar-left-icon" v-if="leftIcon">
            <up-icon :name="leftIcon" size="20" color="#333"></up-icon>
          </view>
          <text class="navbar-left-text" v-if="leftText">{{ leftText }}</text>
        </view>
        
        <!-- 标题 -->
        <view class="navbar-center">
          <slot name="center" v-if="$slots.center"></slot>
          <text class="navbar-title" v-else>{{ title }}</text>
        </view>
        
        <!-- 右侧 -->
        <view class="navbar-right" @click="handleRightClick" v-if="showRight">
          <slot name="right" v-if="$slots.right"></slot>
          <view v-else>
            <view class="navbar-right-icon" v-if="rightIcon">
              <up-icon :name="rightIcon" size="20" color="#333"></up-icon>
            </view>
            <text class="navbar-right-text" v-if="rightText">{{ rightText }}</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 占位元素，防止内容被导航栏遮挡 -->
    <view class="navbar-placeholder" v-if="placeholder" :style="{ height: (statusBarHeight + 44) + 'px' }"></view>
  </view>
</template>

<script setup>
import { defineProps, defineEmits, ref, onMounted } from 'vue'

// 状态栏高度
const statusBarHeight = ref(0)

// 获取状态栏高度
onMounted(() => {
  const systemInfo = uni.getSystemInfoSync()
  statusBarHeight.value = systemInfo.statusBarHeight || 0
})

// 定义props
const props = defineProps({
  // 标题文本
  title: {
    type: String,
    default: ''
  },
  // 左侧图标
  leftIcon: {
    type: String,
    default: 'arrow-left'
  },
  // 右侧图标
  rightIcon: {
    type: String,
    default: ''
  },
  // 左侧文本
  leftText: {
    type: String,
    default: ''
  },
  // 右侧文本
  rightText: {
    type: String,
    default: ''
  },
  // 背景样式
  background: {
    type: Object,
    default: () => ({
      backgroundColor: '#ffffff'
    })
  },
  // 标题样式
  titleStyle: {
    type: Object,
    default: () => ({
      fontSize: '32rpx',
      fontWeight: 'bold',
      color: '#333333'
    })
  },
  // 导航栏高度
  height: {
    type: [String, Number],
    default: '44px'
  },
  // 是否开启顶部安全区适配
  safeAreaInsetTop: {
    type: Boolean,
    default: true
  },
  // 是否显示占位元素
  placeholder: {
    type: Boolean,
    default: true
  },
  // 是否显示下边框
  border: {
    type: Boolean,
    default: true
  },
  // z-index层级
  zIndex: {
    type: [String, Number],
    default: 980
  },
  // 是否显示左侧返回按钮
  showLeft: {
    type: Boolean,
    default: true
  },
  // 是否显示右侧按钮
  showRight: {
    type: Boolean,
    default: false
  }
})

// 定义事件
const emit = defineEmits(['leftClick', 'rightClick'])

// 左侧点击处理
const handleLeftClick = () => {
  if (props.showLeft) {
    // 默认返回上一页
    const pages = getCurrentPages()
    if (pages.length > 1) {
      uni.navigateBack()
    } else {
      // 如果只有一个页面，跳转到首页
      uni.reLaunch({
        url: '/pages/index'
      })
    }
  }
  emit('leftClick')
}

// 右侧点击处理
const handleRightClick = () => {
  emit('rightClick')
}
</script>

<style lang="scss" scoped>
.custom-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: #ffffff;
  border-bottom: 1rpx solid #ebeef5;
}

.status-bar {
  width: 100%;
  background-color: #ffffff;
}

.navbar-content {
  position: relative;
  display: flex;
  align-items: center;
  height: 88rpx;
  padding: 0 30rpx;
  background-color: #ffffff;
}

.navbar-left,
.navbar-right {
  position: absolute;
  display: flex;
  align-items: center;
  height: 88rpx;
  z-index: 2;
}

.navbar-left {
  left: 30rpx;
  justify-content: flex-start;
}

.navbar-right {
  right: 30rpx;
  justify-content: flex-end;
}

.navbar-left-icon,
.navbar-right-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48rpx;
  height: 48rpx;
}

.navbar-left-text,
.navbar-right-text {
  font-size: 28rpx;
  color: #333333;
  margin-left: 8rpx;
}

.navbar-center {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 88rpx;
  z-index: 1;
  pointer-events: none;
}

.navbar-center .navbar-title,
.navbar-center view,
.navbar-center text,
.navbar-center .header-center,
.navbar-center .search-bar,
.navbar-center .logo,
.navbar-center .logo-icon,
.navbar-center .logo-text,
.navbar-center .search-text {
  pointer-events: auto;
}

.navbar-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333333;
  text-align: center;
}

// 占位元素样式
.navbar-placeholder {
  width: 100%;
  background-color: transparent;
}

// 微信小程序安全区域适配
/* #ifdef MP-WEIXIN */
.custom-navbar {
  /* 适配微信小程序 */
}
/* #endif */
</style>
