<template>
  <view class="register-container">
    <view class="header">
      <view class="logo">心理</view>
      <text class="title">注册账号</text>
      <text class="subtitle">欢迎加入心理健康平台</text>
    </view>
    
    <view class="form">
      <view class="form-group">
        <text class="form-label">用户名</text>
        <u--input
          v-model="form.username"
          placeholder="请输入用户名"
          border="bottom"
          :clearable="true"
        ></u--input>
      </view>
      
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
      
      <view class="form-group">
        <text class="form-label">确认密码</text>
        <u--input
          v-model="form.confirmPassword"
          type="password"
          placeholder="请再次输入密码"
          border="bottom"
          :clearable="true"
          :passwordIcon="true"
        ></u--input>
      </view>
      
      <button class="register-btn" @click="handleRegister">注 册</button>
      
      <view class="form-footer">
        <text>已有账号？</text>
        <navigator url="/pages/login" class="form-link">立即登录</navigator>
      </view>
    </view>
    
    <view class="footer">
      <text>注册即代表同意《用户协议》和《隐私政策》</text>
    </view>
  </view>
</template>

<script>
import { ref } from 'vue'
import { request } from '@/utils/request'

export default {
  setup() {
    const form = ref({
      username: '',
      phone: '',
      password: '',
      confirmPassword: ''
    })
    
    const handleRegister = async () => {
      // 表单验证
      if (!form.value.username) {
        uni.showToast({
          title: '请输入用户名',
          icon: 'none'
        })
        return
      }
      
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
      
      if (!form.value.password) {
        uni.showToast({
          title: '请输入密码',
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
          title: '注册中...'
        })
        
        const res = await request({
          url: '/auth/register',
          method: 'POST',
          data: {
            username: form.value.username,
            phone: form.value.phone,
            password: form.value.password
          }
        })
        
        uni.hideLoading()
        
        if (res.code === 200 || res.code === 201) {
          uni.showToast({
            title: '注册成功',
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
            title: res.message || '注册失败',
            icon: 'none'
          })
        }
      } catch (error) {
        uni.hideLoading()
        uni.showToast({
          title: error.message || '注册失败，请稍后重试',
          icon: 'none'
        })
        console.error('注册失败:', error)
      }
    }
    
    return {
      form,
      handleRegister
    }
  }
}
</script>

<style lang="scss">
.register-container {
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

.register-btn {
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
  color: #666;
}

.form-link {
  color: #4A90E2;
  text-decoration: none;
  margin-left: 10rpx;
}

.footer {
  text-align: center;
  padding: 40rpx 0;
  font-size: 24rpx;
  color: #999;
  margin-top: 80rpx;
}
</style> 