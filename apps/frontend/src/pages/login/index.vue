<template>
  <view class="login-container">
    <view class="header">
      <view class="logo">
        <image src="/static/logo/3.png" mode="widthFix" style="width: 100%;"></image>
      </view>
      <text class="title">美光心理</text>
      <text class="subtitle">专业的心理健康服务，为您的心灵护航</text>
    </view>
    
    <view class="form">
      <view class="form-group">
        <text class="form-label">手机号</text>
        <u--input
          v-model="form.username"
          placeholder="请输入手机号"
          border="bottom"
          :clearable="true"
        ></u--input>
      </view>
      <view class="form-group">
        <text class="form-label">密码</text>
        <u--input
          v-model="form.password"
          type="password"
          placeholder="请输入密码"
          border="bottom"
          :clearable="true"
          :passwordIcon="true"
        ></u--input>
      </view>
      
      <button class="login-btn" @click="handleLogin">登 录</button>
      
      <view class="form-footer">
        <navigator url="/pages/register/index" class="form-link">注册账号</navigator>
        <navigator url="/pages/forgot-password/index" class="form-link">忘记密码?</navigator>
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
          <u-icon name="weixin-fill" color="#09BB07" size="60"></u-icon>
        </view>
        <view class="social-btn" @click="handleQQLogin">
          <u-icon name="qq-fill" color="#1296db" size="60"></u-icon>
        </view>
      </view>
    </view>
    
    <view class="footer">
      <text>登录即代表同意《用户协议》和《隐私政策》</text>
    </view>
  </view>
</template>

<script>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'

export default {
  setup() {
    const userStore = useUserStore()
    
    const form = ref({
      username: '',
      password: ''
    })
    
    // 重定向路径
    const redirectPath = ref('')
    
    const handleLogin = async () => {
      // 表单验证
      if (!form.value.username) {
        uni.showToast({
          title: '请输入手机号',
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
      
      try {
        uni.showLoading({
          title: '登录中...'
        })
        
        // 调用登录API
        const result = await userStore.login({
          username: form.value.username,
          password: form.value.password
        })
        
        uni.hideLoading()
        
        if (result.success) {
          uni.showToast({
            title: '登录成功',
            icon: 'success'
          })
          
          // 根据重定向路径决定跳转目标
          setTimeout(() => {
            if (redirectPath.value) {
              // 如果有重定向路径，且是tabBar页面，使用switchTab
              const tabBarPaths = [
                '/pages/index/index',
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
                url: '/pages/index/index'
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
        uni.hideLoading()
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
      
      // 检查是否已登录
      if (userStore.isLoggedIn) {
        if (redirectPath.value) {
          const tabBarPaths = [
            '/pages/index/index',
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
          uni.switchTab({
            url: '/pages/index/index'
          })
        }
      }
    })
    
    return {
      form,
      handleLogin,
      handleWechatLogin,
      handleQQLogin
    }
  }
}
</script>

<style lang="scss">
.login-container {
  min-height: 100vh;
  background-color: #fff;
  padding: 0 30rpx;
}

.header {
  text-align: center;
  padding: 80rpx 0 40rpx;
}

.logo {
  width: 160rpx;
  height: 160rpx;
  margin: 0 auto 30rpx;
  background-color: #4A90E2;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 48rpx;
  font-weight: bold;
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  margin-bottom: 20rpx;
  color: #333;
  display: block;
}

.subtitle {
  font-size: 28rpx;
  color: #999;
  margin-bottom: 60rpx;
  display: block;
}

.form {
  padding: 0 20rpx;
}

.form-group {
  margin-bottom: 40rpx;
}

.form-label {
  display: block;
  font-size: 28rpx;
  margin-bottom: 16rpx;
  color: #666;
}

.login-btn {
  width: 100%;
  height: 90rpx;
  background-color: #4A90E2;
  color: white;
  border: none;
  border-radius: 10rpx;
  font-size: 32rpx;
  font-weight: bold;
  margin-top: 40rpx;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 30rpx;
  font-size: 28rpx;
}

.form-link {
  color: #4A90E2;
  text-decoration: none;
}

.other-login {
  margin-top: 80rpx;
  text-align: center;
}

.divider {
  display: flex;
  align-items: center;
  margin: 40rpx 0;
}

.divider-line {
  flex: 1;
  height: 2rpx;
  background-color: #eee;
}

.divider-text {
  padding: 0 30rpx;
  font-size: 28rpx;
  color: #999;
}

.social-login {
  display: flex;
  justify-content: center;
  gap: 60rpx;
  margin-top: 40rpx;
}

.social-btn {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer {
  text-align: center;
  padding: 40rpx 0;
  font-size: 24rpx;
  color: #999;
  margin-top: 80rpx;
}
</style> 