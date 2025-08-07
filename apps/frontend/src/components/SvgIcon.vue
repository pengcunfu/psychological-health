<template>
  <view class="svg-icon" :style="iconStyle">
    <!-- 对于uni-app，我们使用image标签来显示SVG -->
    <image 
      v-if="!loadError && showSvg"
      :src="iconPath" 
      :style="iconStyle"
      mode="aspectFit"
      @error="onError"
      @load="onLoad"
    />
    <!-- 如果SVG加载失败，显示备用图标 -->
    <up-icon 
      v-else-if="fallbackIcon"
      :name="fallbackIcon" 
      :size="iconSize"
      :color="currentColor"
    />
    <!-- 如果没有备用图标，显示默认文字 -->
    <view v-else class="fallback-text" :style="{ color: currentColor, fontSize: fallbackTextSize }">
      {{ name.charAt(0) }}
    </view>
  </view>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  path: {
    type: String,
    default: '' // 默认路径
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
  },
  fallbackIcon: {
    type: String,
    default: '' // uview图标名称作为备用
  }
})

const emit = defineEmits(['error', 'load'])

const loadError = ref(false)
const showSvg = ref(true)

// 计算图标路径
const iconPath = computed(() => {
  const suffix = props.active ? '-active' : ''
  const path = props.path 
    ? `/static/icons/${props.path}/${props.name}${suffix}.svg`
    : `/static/icons/${props.name}${suffix}.svg`
  return path
})

// 计算图标样式
const iconStyle = computed(() => {
  const size = typeof props.size === 'number' ? `${props.size}rpx` : props.size
  return {
    width: size,
    height: size,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }
})

// 计算当前颜色
const currentColor = computed(() => {
  return props.active ? props.activeColor : props.color
})

// 计算图标大小（用于uview图标）
const iconSize = computed(() => {
  return typeof props.size === 'number' ? props.size : parseInt(props.size)
})

// 计算fallback文字大小
const fallbackTextSize = computed(() => {
  const size = typeof props.size === 'number' ? props.size : parseInt(props.size)
  return `${Math.max(12, size * 0.5)}rpx`
})

const onError = (e) => {
  loadError.value = true
  showSvg.value = false
  emit('error', e)
}

const onLoad = (e) => {
  loadError.value = false
  emit('load', e)
}

// 监听props变化，重置状态
watch([() => props.name, () => props.path, () => props.active], () => {
  loadError.value = false
  showSvg.value = true
})

onMounted(() => {
  // 组件挂载完成
})
</script>

<style lang="scss" scoped>
.svg-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.fallback-text {
  text-align: center;
  font-weight: bold;
}
</style> 