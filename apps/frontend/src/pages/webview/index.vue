<template>
  <view class="webview-container">
    <!-- #ifdef H5 -->
    <iframe 
      :src="url" 
      class="webview-iframe"
      frameborder="0"
      allowfullscreen
    ></iframe>
    <!-- #endif -->
    
    <!-- #ifndef H5 -->
    <web-view 
      :src="url" 
      @message="handleMessage"
      @error="handleError"
      @load="handleLoad"
    ></web-view>
    <!-- #endif -->
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const url = ref('')
const title = ref('')

onLoad((options) => {
  if (options.url) {
    url.value = decodeURIComponent(options.url)
  }
  if (options.title) {
    title.value = decodeURIComponent(options.title)
    uni.setNavigationBarTitle({
      title: title.value
    })
  }
  
  // 验证URL的有效性
  if (!isValidUrl(url.value)) {
    uni.showToast({
      title: '链接格式不正确',
      icon: 'none'
    })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  }
})

// URL验证函数
const isValidUrl = (string) => {
  try {
    new URL(string)
    return true
  } catch (_) {
    return false
  }
}

// 处理消息
const handleMessage = (e) => {
  console.log('WebView消息:', e.detail)
}

// 处理错误
const handleError = (e) => {
  console.error('WebView加载错误:', e.detail)
  uni.showToast({
    title: '页面加载失败',
    icon: 'none'
  })
}

// 处理加载完成
const handleLoad = (e) => {
  console.log('WebView加载完成:', e.detail)
}
</script>

<style lang="scss" scoped>
.webview-container {
  width: 100%;
  height: 100vh;
  
  /* #ifdef H5 */
  .webview-iframe {
    width: 100%;
    height: 100%;
    border: none;
  }
  /* #endif */
}

/* #ifndef H5 */
web-view {
  width: 100%;
  height: 100vh;
}
/* #endif */
</style> 