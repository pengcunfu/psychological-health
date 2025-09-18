<template>
  <view class="login-container">
    <view class="header">
      <view class="logo-container">
        <view class="logo">
          <image :src="imageUtils.processImageUrl('/logo/3.png')" mode="aspectFit"></image>
        </view>
        <view class="logo-shadow"></view>
      </view>
      <text class="title">美光心理</text>
      <text class="subtitle">专业的心理健康服务，为您的心灵护航</text>
    </view>

    <view class="form">
      <!-- 账户登录 -->
      <view class="form-group">
        <view class="input-wrapper">
          <view class="input-icon">
            <up-icon name="account" color="#999" size="30"></up-icon>
          </view>
          <up--input v-model="form.account" placeholder="请输入用户名、手机号或邮箱" border="none" :clearable="true" 
            class="custom-input"></up--input>
        </view>
      </view>

      <view class="form-group">
        <view class="input-wrapper">
          <view class="input-icon">
            <up-icon name="lock" color="#999" size="30"></up-icon>
          </view>
          <up--input v-model="form.password" type="password" placeholder="请输入密码" border="none" :clearable="true"
            :passwordIcon="true" class="custom-input"></up--input>
        </view>
      </view>

      <!-- 隐私协议勾选 -->
      <view class="agreement-section">
        <view class="agreement-checkbox" @click="toggleAgreement">
          <view class="checkbox" :class="{ checked: form.agreePrivacy }">
            <up-icon v-if="form.agreePrivacy" name="checkmark" color="#fff" size="24"></up-icon>
          </view>
          <text class="agreement-text">
            我已阅读并同意<text class="agreement-link" @click="goToPrivacyPolicy">《隐私政策》</text>和<text class="agreement-link"
              @click="goToUserAgreement">《用户协议》</text>
          </text>
        </view>
      </view>

      <button class="login-btn" @click="handleLogin">
        <text class="btn-text">登 录</text>
        <view class="btn-loading" v-if="loading">
          <up-loading-icon mode="flower" color="#fff" size="30"></up-loading-icon>
        </view>
      </button>

      <view class="form-footer">
        <navigator url="/pages/register" class="form-link">注册账号</navigator>
        <navigator url="/pages/forgot-password" class="form-link">忘记密码?</navigator>
      </view>
    </view>

    <view class="other-login">
      <view class="divider">
        <view class="divider-line"></view>
        <text class="divider-text">其他登录方式</text>
        <view class="divider-line"></view>
      </view>

      <view class="social-login">
        <view class="social-btn" @click="handleWechatLogin">
          <up-icon name="weixin-fill" color="#09BB07" size="60"></up-icon>
        </view>
        <view class="social-btn" @click="handleQQLogin">
          <up-icon name="qq-fill" color="#1296db" size="60"></up-icon>
        </view>
      </view>
    </view>


  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { login, userLogin } from '@/api/auth'
import { imageUtils } from '@/utils/image'

const userStore = useUserStore()


const form = ref({
  account: '',
  password: '',
  agreePrivacy: false
})

// 重定向路径
const redirectPath = ref('')

// 加载状态
const loading = ref(false)

// 切换隐私协议同意状态
const toggleAgreement = () => {
  form.value.agreePrivacy = !form.value.agreePrivacy
}

// 跳转到隐私政策页面
const goToPrivacyPolicy = () => {
  uni.navigateTo({
    url: '/pages/profile/privacy-agreement'
  })
}

// 跳转到用户协议页面
const goToUserAgreement = () => {
  uni.navigateTo({
    url: '/pages/profile/agreement'
  })
}

const handleLogin = async () => {
  // 表单验证
  if (!form.value.account) {
    uni.showToast({
      title: '请输入账户',
      icon: 'none'
    })
    return
  }

  if (!form.value.password) {
    uni.showToast({
      title: '请输入密码',
      icon: 'none'
    })
    return
  }

  if (!form.value.agreePrivacy) {
    uni.showToast({
      title: '请先同意隐私政策和用户协议',
      icon: 'none'
    })
    return
  }

  try {
    loading.value = true

    // 统一使用账户登录
    const result = await userLogin({
      account: form.value.account,
      password: form.value.password
    })

    loading.value = false

    if (result.code === 200 && result.success) {
      // 保存登录信息到store
      await userStore.setLoginInfo(result.data)

      uni.showToast({
        title: '登录成功',
        icon: 'success'
      })

      // 根据重定向路径决定跳转目标
      setTimeout(() => {
        if (redirectPath.value) {
          // 如果有重定向路径，且是tabBar页面，使用switchTab
          const tabBarPaths = [
            '/pages/index',
            '/pages/counselor/index',
            '/pages/course/index',
            '/pages/profile/index'
          ]

          if (tabBarPaths.includes(redirectPath.value)) {
            uni.switchTab({
              url: redirectPath.value
            })
          } else {
            uni.navigateTo({
              url: redirectPath.value
            })
          }
        } else {
          // 默认跳转到首页
          uni.switchTab({
            url: '/pages/index'
          })
        }
      }, 1500)
    } else {
      uni.showToast({
        title: result.message || '登录失败',
        icon: 'none'
      })
    }
  } catch (error) {
    loading.value = false
    uni.showToast({
      title: '登录失败，请稍后重试',
      icon: 'none'
    })
    console.error('登录失败:', error)
  }
}

const handleWechatLogin = () => {
  uni.showToast({
    title: '微信登录功能开发中',
    icon: 'none'
  })
}

const handleQQLogin = () => {
  uni.showToast({
    title: 'QQ登录功能开发中',
    icon: 'none'
  })
}

onLoad((options) => {
  // 获取重定向参数
  if (options.redirect) {
    redirectPath.value = decodeURIComponent(options.redirect)
  }
})
</script>

<style lang="scss" scoped>
// SCSS 变量定义
$primary-color: #4A90E2;
$white: #fff;
$gray-light: #f5f7fa;
$gray: #999;
$gray-medium: #666;
$gray-dark: #333;
$gray-border: #eee;
$gray-bg: #f5f5f5;
$border-radius: 10rpx;
$border-radius-small: 8rpx;
$transition: all 0.3s;

.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 50%, #f1f3f4 100%);
  padding: 0 30rpx;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 15% 20%, rgba(74, 144, 226, 0.08) 0%, transparent 50%),
      radial-gradient(circle at 85% 80%, rgba(147, 51, 234, 0.06) 0%, transparent 50%),
      radial-gradient(circle at 50% 50%, rgba(34, 197, 94, 0.04) 0%, transparent 50%);
    pointer-events: none;
  }

  &::after {
    content: '';
    position: absolute;
    top: 10%;
    left: 20%;
    width: 6rpx;
    height: 6rpx;
    background: rgba(74, 144, 226, 0.3);
    border-radius: 50%;
    box-shadow: 
      100rpx 50rpx 0 rgba(147, 51, 234, 0.2),
      -80rpx 120rpx 0 rgba(34, 197, 94, 0.25),
      200rpx 200rpx 0 rgba(245, 158, 11, 0.2),
      -50rpx 300rpx 0 rgba(239, 68, 68, 0.15),
      300rpx 100rpx 0 rgba(168, 85, 247, 0.18);
    pointer-events: none;
  }
}

// 头部区域
.header {
  text-align: center;
  padding: 80rpx 0 60rpx;
  position: relative;
  z-index: 1;

  .logo-container {
    position: relative;
    display: inline-block;
    margin-bottom: 40rpx;

    .logo {
      width: 120rpx;
      height: 120rpx;
      background: $white;
      border-radius: 30rpx;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1rpx solid rgba(0, 0, 0, 0.06);

      image {
        width: 80rpx;
        height: 80rpx;
      }
    }

    .logo-shadow {
      display: none;
    }
  }

  .title {
    font-size: 56rpx;
    font-weight: 700;
    margin-bottom: 16rpx;
    color: $gray-dark;
    display: block;
  }

  .subtitle {
    font-size: 28rpx;
    color: $gray-medium;
    margin-bottom: 20rpx;
    display: block;
    font-weight: 400;
  }
}



// 表单区域
.form {
  margin: 0 20rpx;
  position: relative;
  z-index: 1;

  &-group {
    margin-bottom: 32rpx;
  }

  .input-wrapper {
    position: relative;
    background: $white;
    border-radius: 12rpx;
    display: flex;
    align-items: center;
    padding: 24rpx 20rpx;
    transition: all 0.3s ease;
    border: 1rpx solid rgba(0, 0, 0, 0.08);

    &:focus-within {
      border-color: $primary-color;
    }

    .input-icon {
      margin-right: 20rpx;
      display: flex;
      align-items: center;
    }

    .custom-input {
      flex: 1;
      background: transparent;
      
      :deep(.up-input__content__field-wrapper) {
        background: transparent !important;
        border: none !important;
      }
    }
  }

  &-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 30rpx;
    font-size: 28rpx;
  }

  &-link {
    color: $primary-color;
    text-decoration: none;
  }
}

// 隐私协议勾选
.agreement-section {
  margin-top: 40rpx;

  .agreement-checkbox {
    display: flex;
    align-items: flex-start;
    gap: 20rpx;
    cursor: pointer;
    padding: 16rpx;
    border-radius: 12rpx;
    transition: all 0.3s ease;

    &:active {
      background: rgba(74, 144, 226, 0.05);
    }

    .checkbox {
      width: 40rpx;
      height: 40rpx;
      border: 1rpx solid #ddd;
      border-radius: 6rpx;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      margin-top: 2rpx;
      transition: all 0.3s ease;
      position: relative;

      &.checked {
        background: $primary-color;
        border-color: $primary-color;
      }
    }

    .agreement-text {
      font-size: 26rpx;
      color: #666;
      line-height: 1.4;
      flex: 1;

      .agreement-link {
        color: $primary-color;
        font-size: 26rpx;
        text-decoration: none;
        font-weight: 500;
        border-bottom: 1px solid transparent;
        transition: border-color 0.3s ease;

        &:active {
          border-bottom-color: $primary-color;
        }
      }
    }
  }
}

.login-btn {
  width: 100%;
  height: 100rpx;
  background: $primary-color;
  color: $white;
  border: none;
  border-radius: 12rpx;
  font-size: 32rpx;
  font-weight: 600;
  margin-top: 40rpx;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;

  &:active {
    background: #3b7dd8;
    transform: translateY(1rpx);
  }

  .btn-text {
    font-size: 32rpx;
    font-weight: 600;
  }

  .btn-loading {
    margin-left: 20rpx;
  }
}

// 其他登录方式
.other-login {
  margin-top: 60rpx;
  text-align: center;
  position: relative;
  z-index: 1;

  .divider {
    display: flex;
    align-items: center;
    margin: 40rpx 20rpx;

    &-line {
      flex: 1;
      height: 1rpx;
      background: linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.1), transparent);
    }

    &-text {
      padding: 0 30rpx;
      font-size: 26rpx;
      color: $gray;
      font-weight: 400;
    }
  }

  .social-login {
    display: flex;
    justify-content: center;
    gap: 60rpx;
    margin: 60rpx;
    padding-bottom: 120rpx;

    .social-btn {
      width: 88rpx;
      height: 88rpx;
      border-radius: 16rpx;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;

      &:active {
        transform: scale(0.96);
        background: #f8f9fa;
      }
    }
  }
}
</style>