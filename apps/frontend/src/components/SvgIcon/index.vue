<template>
  <view class="svg-icon" :style="iconStyle">
    <!-- 对于uni-app，我们使用image标签来显示SVG -->
    <image 
      :src="iconPath" 
      :style="iconStyle"
      mode="aspectFit"
      @error="onError"
      @load="onLoad"
    />
  </view>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  size: {
    type: [String, Number],
    default: 24
  },
  color: {
    type: String,
    default: '#999'
  },
  active: {
    type: Boolean,
    default: false
  },
  activeColor: {
    type: String,
    default: '#4A90E2'
  }
})

const emit = defineEmits(['error', 'load'])

// 计算图标路径
const iconPath = computed(() => {
  const suffix = props.active ? '-active' : ''
  return `/static/icons/tabbar/${props.name}${suffix}.svg`
})

// 计算图标样式
const iconStyle = computed(() => {
  const size = typeof props.size === 'number' ? `${props.size}rpx` : props.size
  return {
    width: size,
    height: size,
    display: 'block'
  }
})

const onError = (e) => {
  console.error('SVG图标加载失败:', iconPath.value, e)
  emit('error', e)
}

const onLoad = (e) => {
  emit('load', e)
}
</script>

<style lang="scss" scoped>
.svg-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
</style> 