<template>
  <view class="container">
    <view class="form-section">

      <view class="current-info">
        <view class="info-item">
          <text class="info-label">当前邮箱</text>
          <text class="info-value">{{ maskEmail(currentEmail) }}</text>
        </view>
      </view>

      <view class="form-group">
        <view class="form-item">
          <text class="form-label">新邮箱</text>
          <u-input 
            v-model="form.email" 
            placeholder="请输入新邮箱地址" 
            border="bottom"
            type="email"
            customStyle="background: transparent; border: none;"
          />
        </view>

        <view class="form-item">
          <text class="form-label">验证码</text>
          <view class="verify-code-input">
            <u-input 
              v-model="form.verifyCode" 
              placeholder="请输入验证码" 
              border="bottom"
              style="flex: 1;"
              customStyle="background: transparent; border: none;"
            />
            <button 
              class="verify-code-btn" 
              :class="{ disabled: form.counting }"
              :disabled="form.counting || !form.email" 
              @click="sendCode"
            >
              {{ form.counting ? `${form.countdown}s后重新获取` : '获取验证码' }}
            </button>
          </view>
        </view>
      </view>

      <view class="tips">
        <text class="tip-item">• 请确保新邮箱可以正常接收邮件</text>
        <text class="tip-item">• 验证码有效期为5分钟</text>
        <text class="tip-item">• 更换后将影响登录和安全验证</text>
      </view>

    </view>

    <!-- 底部按钮 -->
    <view class="submit-section">
      <button class="submit-btn" @click="handleChangeEmail">
        确认更换
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { onLoad, onUnload } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { request } from '@/utils/request'

const userStore = useUserStore()

// 当前邮箱
const currentEmail = ref('')

// 表单数据
const form = reactive({
  email: '',
  verifyCode: '',
  counting: false,
  countdown: 60
})

// 定时器
let timer = null

// 获取用户信息
const getUserInfo = async () => {
  try {
    const res = await userStore.getUserInfo()
    if (res.success) {
      currentEmail.value = res.data.email || ''
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 发送验证码
const sendCode = async () => {
  // 验证邮箱
  if (!form.email) {
    uni.showToast({
      title: '请输入邮箱',
      icon: 'none'
    })
    return
  }

  if (!/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(form.email)) {
    uni.showToast({
      title: '邮箱格式不正确',
      icon: 'none'
    })
    return
  }

  if (form.email === currentEmail.value) {
    uni.showToast({
      title: '新邮箱不能与当前邮箱相同',
      icon: 'none'
    })
    return
  }

  if (form.counting) return

  try {
    uni.showLoading({
      title: '发送中...'
    })

    const res = await request({
      url: '/auth/send-code',
      method: 'POST',
      data: {
        email: form.email,
        type: 'bind_email'
      }
    })

    uni.hideLoading()

    if (res.code === 200 && res.success) {
      uni.showToast({
        title: '验证码已发送',
        icon: 'success'
      })

      // 开始倒计时
      form.counting = true
      form.countdown = 60

      timer = setInterval(() => {
        if (form.countdown > 0) {
          form.countdown--
        } else {
          clearInterval(timer)
          form.counting = false
        }
      }, 1000)
    } else {
      uni.showToast({
        title: res.message || '发送验证码失败',
        icon: 'none'
      })
    }
  } catch (error) {
    uni.hideLoading()
    console.error('发送验证码失败:', error)
    uni.showToast({
      title: '发送验证码失败，请稍后重试',
      icon: 'none'
    })
  }
}

// 更换邮箱
const handleChangeEmail = async () => {
  // 表单验证
  if (!form.email) {
    uni.showToast({
      title: '请输入邮箱',
      icon: 'none'
    })
    return
  }

  if (!/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(form.email)) {
    uni.showToast({
      title: '邮箱格式不正确',
      icon: 'none'
    })
    return
  }

  if (!form.verifyCode) {
    uni.showToast({
      title: '请输入验证码',
      icon: 'none'
    })
    return
  }

  try {
    uni.showLoading({
      title: '更换中...'
    })

    const res = await request({
      url: '/user/bind-email',
      method: 'POST',
      data: {
        email: form.email,
        verify_code: form.verifyCode
      }
    })

    uni.hideLoading()

    if (res.code === 200 && res.success) {
      uni.showToast({
        title: '邮箱更换成功',
        icon: 'success'
      })

      // 更新用户信息
      await userStore.getUserInfo()

      // 延迟返回上一页
      setTimeout(() => {
        uni.navigateBack()
      }, 1500)
    } else {
      uni.showToast({
        title: res.message || '更换失败',
        icon: 'none'
      })
    }
  } catch (error) {
    uni.hideLoading()
    console.error('更换邮箱失败:', error)
    uni.showToast({
      title: '更换失败，请稍后重试',
      icon: 'none'
    })
  }
}

// 邮箱脱敏
const maskEmail = (email) => {
  if (!email) return '未绑定'
  const parts = email.split('@')
  if (parts.length !== 2) return email

  const name = parts[0]
  const domain = parts[1]

  let maskedName = name
  if (name.length > 3) {
    maskedName = name.substr(0, 3) + '****'
  } else {
    maskedName = name.substr(0, 1) + '****'
  }

  return maskedName + '@' + domain
}

// 页面加载
onLoad(() => {
  uni.setNavigationBarTitle({
    title: '更换邮箱'
  })
  getUserInfo()
})

// 页面卸载时清除定时器
onUnload(() => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
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

.current-info {
  background-color: #F8F9FA;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 40rpx;

  .info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .info-label {
      font-size: 28rpx;
      color: $text-secondary;
    }

    .info-value {
      font-size: 28rpx;
      color: $text-primary;
      font-weight: 500;
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

    .verify-code-input {
      display: flex;
      align-items: center;
      gap: 20rpx;

      .verify-code-btn {
        width: 220rpx;
        height: 70rpx;
        font-size: 24rpx;
        color: $primary-color;
        background-color: $white;
        border: 1rpx solid $primary-color;
        border-radius: 35rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;

        &.disabled {
          color: $text-tertiary;
          border-color: #E5E5EA;
          background-color: #F8F9FA;
        }

        &:not(.disabled):active {
          background-color: $primary-color;
          color: $white;
        }
      }
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
