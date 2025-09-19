<template>
  <view class="container">
    <view class="form-section">

      <view class="form-group">
        <view class="form-item">
          <text class="form-label">当前密码</text>
          <u-input 
            v-model="form.oldPassword" 
            type="password" 
            placeholder="请输入当前密码" 
            border="bottom"
            :password-icon="true"
            customStyle="background: transparent; border: none;"
          />
        </view>

        <view class="form-item">
          <text class="form-label">新密码</text>
          <u-input 
            v-model="form.newPassword" 
            type="password" 
            placeholder="请输入新密码" 
            border="bottom"
            :password-icon="true"
            customStyle="background: transparent; border: none;"
          />
        </view>

        <view class="form-item">
          <text class="form-label">确认新密码</text>
          <u-input 
            v-model="form.confirmPassword" 
            type="password" 
            placeholder="请再次输入新密码" 
            border="bottom"
            :password-icon="true"
            customStyle="background: transparent; border: none;"
          />
        </view>
      </view>

      <view class="tips">
        <text class="tip-item">• 密码长度不少于6位</text>
        <text class="tip-item">• 建议包含字母、数字的组合</text>
        <text class="tip-item">• 不要使用过于简单的密码</text>
      </view>

    </view>

    <!-- 底部按钮 -->
    <view class="submit-section">
      <button class="submit-btn" @click="handleChangePassword">
        确认修改
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

// 修改密码表单
const form = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 修改密码
const handleChangePassword = async () => {
  // 表单验证
  if (!form.oldPassword) {
    uni.showToast({
      title: '请输入当前密码',
      icon: 'none'
    })
    return
  }

  if (!form.newPassword) {
    uni.showToast({
      title: '请输入新密码',
      icon: 'none'
    })
    return
  }

  if (form.newPassword.length < 6) {
    uni.showToast({
      title: '新密码长度不能少于6位',
      icon: 'none'
    })
    return
  }

  if (form.newPassword !== form.confirmPassword) {
    uni.showToast({
      title: '两次输入的新密码不一致',
      icon: 'none'
    })
    return
  }

  try {
    uni.showLoading({
      title: '修改中...'
    })

    const res = await userStore.changePassword({
      old_password: form.oldPassword,
      new_password: form.newPassword
    })

    uni.hideLoading()

    if (res.success) {
      uni.showToast({
        title: '密码修改成功',
        icon: 'success'
      })

      // 清空表单
      form.oldPassword = ''
      form.newPassword = ''
      form.confirmPassword = ''

      // 延迟返回上一页
      setTimeout(() => {
        uni.navigateBack()
      }, 1500)
    } else {
      uni.showToast({
        title: res.message || '密码修改失败',
        icon: 'none'
      })
    }
  } catch (error) {
    uni.hideLoading()
    console.error('修改密码失败:', error)
    uni.showToast({
      title: '修改密码失败，请稍后重试',
      icon: 'none'
    })
  }
}

// 页面加载
onLoad(() => {
  // 设置导航栏标题
  uni.setNavigationBarTitle({
    title: '修改密码'
  })
})
</script>

<style lang="scss" scoped>
// SCSS 变量定义
$primary-color: #4A90E2;
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
  padding-bottom: 120rpx;
}

.form-section {
  background-color: $white;
  border-radius: 20rpx;
  padding: 40rpx;
  box-shadow: 0 2rpx 20rpx rgba(0, 0, 0, 0.05);

  .form-title {
    font-size: 36rpx;
    font-weight: bold;
    color: $text-primary;
    margin-bottom: 40rpx;
    text-align: center;
    position: relative;
    padding-bottom: 20rpx;

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 60rpx;
      height: 4rpx;
      background-color: $primary-color;
      border-radius: 2rpx;
    }
  }
}

.form-group {
  margin-bottom: 40rpx;

  .form-item {
    margin-bottom: 40rpx;

    .form-label {
      font-size: 30rpx;
      color: $text-primary;
      margin-bottom: 20rpx;
      display: block;
      font-weight: 500;
    }
  }
}

.tips {
  background-color: #FFF7E6;
  border: 1rpx solid #FFD591;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 40rpx;

  .tip-item {
    display: block;
    font-size: 26rpx;
    color: #D46B08;
    line-height: 1.6;
    margin-bottom: 10rpx;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

// 保存按钮区域
.submit-section {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: $white;
  padding: 20rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  border-top: 1rpx solid #E5E5EA;
  z-index: 100;

  .submit-btn {
    width: 100%;
    height: 88rpx;
    background: linear-gradient(135deg, $primary-color 0%, #357ABD 100%);
    color: $white;
    border: none;
    border-radius: 12rpx;
    font-size: 32rpx;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
    transition: all 0.2s ease;
    letter-spacing: 1rpx;

    &:active {
      transform: scale(0.98);
      box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
    }

    &:disabled {
      background: #C7C7CC;
      color: #8E8E93;
      box-shadow: none;
      transform: none;
    }
  }
}
</style>
