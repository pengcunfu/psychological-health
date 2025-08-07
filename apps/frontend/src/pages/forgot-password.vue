<template>
  <view class="forgot-password-container">
    <view class="header">
      <view class="logo">心理</view>
      <text class="title">找回密码</text>
      <text class="subtitle">请输入您的账号信息</text>
    </view>
    
    <view class="form">
      <view class="form-group">
        <text class="form-label">手机号</text>
        <u--input
          v-model="form.phone"
          placeholder="请输入手机号"
          border="bottom"
          :clearable="true"
          type="number"
        ></u--input>
      </view>
      
      <view class="form-group">
        <text class="form-label">验证码</text>
        <view class="verify-code-input">
          <u--input
            v-model="form.verifyCode"
            placeholder="请输入验证码"
            border="bottom"
            :clearable="true"
            style="flex: 1;"
          ></u--input>
          <button class="verify-code-btn" :disabled="counting" @click="handleSendCode">
            {{ counting ? `${countdown}s后重新获取` : '获取验证码' }}
          </button>
        </view>
      </view>
      
      <view class="form-group">
        <text class="form-label">新密码</text>
        <u--input
          v-model="form.password"
          type="password"
          placeholder="请输入新密码"
          border="bottom"
          :clearable="true"
          :passwordIcon="true"
        ></u--input>
      </view>
      
      <view class="form-group">
        <text class="form-label">确认密码</text>
        <u--input
          v-model="form.confirmPassword"
          type="password"
          placeholder="请再次输入新密码"
          border="bottom"
          :clearable="true"
          :passwordIcon="true"
        ></u--input>
      </view>
      
      <button class="reset-btn" @click="handleResetPassword">重置密码</button>
      
      <view class="form-footer">
        <navigator url="/pages/login" class="form-link">返回登录</navigator>
      </view>
    </view>
  </view>
</template>

<script>
import { ref } from 'vue'
import { request } from '@/utils/request'

export default {
  setup() {
    const form = ref({
      phone: '',
      verifyCode: '',
      password: '',
      confirmPassword: ''
    })
    
    const counting = ref(false)
    const countdown = ref(60)
    let timer = null
    
    const handleSendCode = async () => {
      // 验证手机号
      if (!form.value.phone) {
        uni.showToast({
          title: '请输入手机号',
          icon: 'none'
        })
        return
      }
      
      if (!/^1\d{10}$/.test(form.value.phone)) {
        uni.showToast({
          title: '手机号格式不正确',
          icon: 'none'
        })
        return
      }
      
      if (counting.value) return
      
      try {
        uni.showLoading({
          title: '发送中...'
        })
        
        const res = await request({
          url: '/auth/send-code',
          method: 'POST',
          data: {
            phone: form.value.phone,
            type: 'reset_password'
          }
        })
        
        uni.hideLoading()
        
        if (res.code === 200) {
          uni.showToast({
            title: '验证码已发送',
            icon: 'success'
          })
          
          // 开始倒计时
          counting.value = true
          countdown.value = 60
          
          timer = setInterval(() => {
            if (countdown.value > 0) {
              countdown.value--
            } else {
              clearInterval(timer)
              counting.value = false
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
        uni.showToast({
          title: '发送验证码失败，请稍后重试',
          icon: 'none'
        })
        console.error('发送验证码失败:', error)
      }
    }
    
    const handleResetPassword = async () => {
      // 表单验证
      if (!form.value.phone) {
        uni.showToast({
          title: '请输入手机号',
          icon: 'none'
        })
        return
      }
      
      if (!form.value.verifyCode) {
        uni.showToast({
          title: '请输入验证码',
          icon: 'none'
        })
        return
      }
      
      if (!form.value.password) {
        uni.showToast({
          title: '请输入新密码',
          icon: 'none'
        })
        return
      }
      
      if (form.value.password.length < 6) {
        uni.showToast({
          title: '密码长度不能少于6位',
          icon: 'none'
        })
        return
      }
      
      if (form.value.password !== form.value.confirmPassword) {
        uni.showToast({
          title: '两次输入的密码不一致',
          icon: 'none'
        })
        return
      }
      
      try {
        uni.showLoading({
          title: '重置密码中...'
        })
        
        const res = await request({
          url: '/auth/reset-password',
          method: 'POST',
          data: {
            phone: form.value.phone,
            verify_code: form.value.verifyCode,
            password: form.value.password
          }
        })
        
        uni.hideLoading()
        
        if (res.code === 200) {
          uni.showToast({
            title: '密码重置成功',
            icon: 'success'
          })
          
          // 跳转到登录页
          setTimeout(() => {
            uni.navigateTo({
              url: '/pages/login'
            })
          }, 1500)
        } else {
          uni.showToast({
            title: res.message || '密码重置失败',
            icon: 'none'
          })
        }
      } catch (error) {
        uni.hideLoading()
        uni.showToast({
          title: '密码重置失败，请稍后重试',
          icon: 'none'
        })
        console.error('密码重置失败:', error)
      }
    }
    
    // 组件销毁时清除定时器
    uni.onUnload(() => {
      if (timer) {
        clearInterval(timer)
        timer = null
      }
    })
    
    return {
      form,
      counting,
      countdown,
      handleSendCode,
      handleResetPassword
    }
  }
}
</script>

<style lang="scss" scoped>
.forgot-password-container {
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

.verify-code-input {
  display: flex;
  align-items: center;
}

.verify-code-btn {
  width: 220rpx;
  height: 70rpx;
  line-height: 70rpx;
  font-size: 24rpx;
  color: #4A90E2;
  background-color: #fff;
  border: 1rpx solid #4A90E2;
  border-radius: 10rpx;
  margin-left: 20rpx;
  padding: 0;
}

.verify-code-btn[disabled] {
  color: #999;
  border-color: #ddd;
}

.reset-btn {
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
  justify-content: center;
  margin-top: 30rpx;
  font-size: 28rpx;
}

.form-link {
  color: #4A90E2;
  text-decoration: none;
}
</style> 