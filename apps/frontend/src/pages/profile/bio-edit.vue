<template>
  <view class="container">
    <!-- 编辑区域 -->
    <view class="edit-section">
      <view class="textarea-container">
        <textarea 
          v-model="bioText" 
          placeholder="介绍一下你自己吧..." 
          class="bio-textarea" 
          maxlength="200"
          :focus="autoFocus"
          @input="onInput"
        ></textarea>
        <view class="char-count">{{ bioText.length }}/200</view>
      </view>
      
      <!-- 提示文字 -->
      <view class="hint-text">
        个人简介将在你的资料页面展示，让更多人了解你
      </view>
    </view>


  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad, onUnload } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

// 个人简介文本
const bioText = ref('')
// 是否自动聚焦
const autoFocus = ref(true)



// 输入处理
const onInput = (e) => {
  bioText.value = e.detail.value
}

// 保存个人简介
const handleSave = async () => {
  try {
    const res = await userStore.updateUserInfo({
      bio: bioText.value
    })

    if (res.success) {
      // 更新原始数据
      uni.setStorageSync('originalBio', bioText.value)
    } else {
      console.error('保存个人简介失败:', res.message)
    }
  } catch (error) {
    console.error('保存个人简介失败:', error)
  }
}

// 页面加载
onLoad((options) => {
  // 获取传递的bio参数
  if (options.bio) {
    bioText.value = decodeURIComponent(options.bio)
  }
  
  // 保存原始数据用于比较
  uni.setStorageSync('originalBio', bioText.value)
})

// 页面卸载时自动保存
onUnload(() => {
  // 检查是否有修改
  if (bioText.value !== (uni.getStorageSync('originalBio') || '')) {
    // 自动保存
    handleSave()
  }
})
</script>

<style lang="scss" scoped>
// SCSS 变量定义
$primary-color: #007AFF;
$white: #FFFFFF;
$gray-light: #f5f7fa;
$gray: #999;
$gray-medium: #666;
$gray-dark: #333;
$text-primary: #1C1C1E;
$text-secondary: #48484A;
$text-tertiary: #8E8E93;
$bg-primary: #FFFFFF;
$bg-secondary: #F2F2F7;

.container {
  min-height: 100vh;
  background-color: $bg-secondary;
  display: flex;
  flex-direction: column;
}

// 编辑区域
.edit-section {
  flex: 1;
  padding: 30rpx;

  .textarea-container {
    background-color: $bg-primary;
    border-radius: 16rpx;
    padding: 30rpx;
    position: relative;

    .bio-textarea {
      width: 100%;
      min-height: 300rpx;
      font-size: 32rpx;
      color: $text-primary;
      line-height: 1.6;
      background-color: transparent;
      border: none;
      outline: none;
      resize: none;
      font-family: inherit;

      &::placeholder {
        color: $text-tertiary;
      }
    }

    .char-count {
      position: absolute;
      bottom: 20rpx;
      right: 30rpx;
      font-size: 24rpx;
      color: $text-tertiary;
    }
  }

  .hint-text {
    margin-top: 30rpx;
    font-size: 26rpx;
    color: $text-tertiary;
    line-height: 1.5;
    text-align: center;
  }
}


</style> 