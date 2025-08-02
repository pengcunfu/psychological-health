<template>
  <view class="container">
    <view class="form-section">
      <view class="form-title">修改密码</view>
      
      <view class="form-group">
        <view class="form-item">
          <text class="form-label">当前密码</text>
          <u--input
            v-model="form.oldPassword"
            type="password"
            placeholder="请输入当前密码"
            border="bottom"
            :password-icon="true"
          ></u--input>
        </view>
        
        <view class="form-item">
          <text class="form-label">新密码</text>
          <u--input
            v-model="form.newPassword"
            type="password"
            placeholder="请输入新密码"
            border="bottom"
            :password-icon="true"
          ></u--input>
        </view>
        
        <view class="form-item">
          <text class="form-label">确认新密码</text>
          <u--input
            v-model="form.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
            border="bottom"
            :password-icon="true"
          ></u--input>
        </view>
      </view>
      
      <button class="submit-btn" @click="handleChangePassword">修改密码</button>
    </view>
    
    <view class="form-section">
      <view class="form-title">绑定手机</view>
      
      <view class="form-group">
        <view class="form-item">
          <text class="form-label">当前手机号</text>
          <view class="phone-display">
            <text>{{ maskPhone(userInfo.phone) }}</text>
            <button class="change-btn" @click="showBindPhoneModal = true">更换</button>
          </view>
        </view>
      </view>
    </view>
    
    <view class="form-section">
      <view class="form-title">绑定邮箱</view>
      
      <view class="form-group">
        <view class="form-item">
          <text class="form-label">当前邮箱</text>
          <view class="phone-display">
            <text>{{ maskEmail(userInfo.email) }}</text>
            <button class="change-btn" @click="showBindEmailModal = true">更换</button>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 绑定手机弹窗 -->
    <u-popup :show="showBindPhoneModal" mode="center" @close="showBindPhoneModal = false" round="10">
      <view class="popup-content">
        <view class="popup-title">绑定手机</view>
        
        <view class="popup-form">
          <view class="form-item">
            <text class="form-label">新手机号</text>
            <u--input
              v-model="phoneForm.phone"
              placeholder="请输入新手机号"
              border="bottom"
              type="number"
            ></u--input>
          </view>
          
          <view class="form-item">
            <text class="form-label">验证码</text>
            <view class="verify-code-input">
              <u--input
                v-model="phoneForm.verifyCode"
                placeholder="请输入验证码"
                border="bottom"
                style="flex: 1;"
              ></u--input>
              <button 
                class="verify-code-btn" 
                :disabled="phoneForm.counting" 
                @click="sendPhoneCode"
              >
                {{ phoneForm.counting ? `${phoneForm.countdown}s后重新获取` : '获取验证码' }}
              </button>
            </view>
          </view>
        </view>
        
        <view class="popup-btns">
          <button class="cancel-btn" @click="showBindPhoneModal = false">取消</button>
          <button class="confirm-btn" @click="handleBindPhone">确认</button>
        </view>
      </view>
    </u-popup>
    
    <!-- 绑定邮箱弹窗 -->
    <u-popup :show="showBindEmailModal" mode="center" @close="showBindEmailModal = false" round="10">
      <view class="popup-content">
        <view class="popup-title">绑定邮箱</view>
        
        <view class="popup-form">
          <view class="form-item">
            <text class="form-label">新邮箱</text>
            <u--input
              v-model="emailForm.email"
              placeholder="请输入新邮箱"
              border="bottom"
              type="email"
            ></u--input>
          </view>
          
          <view class="form-item">
            <text class="form-label">验证码</text>
            <view class="verify-code-input">
              <u--input
                v-model="emailForm.verifyCode"
                placeholder="请输入验证码"
                border="bottom"
                style="flex: 1;"
              ></u--input>
              <button 
                class="verify-code-btn" 
                :disabled="emailForm.counting" 
                @click="sendEmailCode"
              >
                {{ emailForm.counting ? `${emailForm.countdown}s后重新获取` : '获取验证码' }}
              </button>
            </view>
          </view>
        </view>
        
        <view class="popup-btns">
          <button class="cancel-btn" @click="showBindEmailModal = false">取消</button>
          <button class="confirm-btn" @click="handleBindEmail">确认</button>
        </view>
      </view>
    </u-popup>
  </view>
</template>

<script>
import { ref, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import { request } from '@/utils/request'

export default {
  setup() {
    const userStore = useUserStore()
    const userInfo = ref({})
    
    // 修改密码表单
    const form = reactive({
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    })
    
    // 绑定手机表单
    const phoneForm = reactive({
      phone: '',
      verifyCode: '',
      counting: false,
      countdown: 60
    })
    
    // 绑定邮箱表单
    const emailForm = reactive({
      email: '',
      verifyCode: '',
      counting: false,
      countdown: 60
    })
    
    // 弹窗控制
    const showBindPhoneModal = ref(false)
    const showBindEmailModal = ref(false)
    
    // 定时器
    let phoneTimer = null
    let emailTimer = null
    
    // 获取用户信息
    const getUserInfo = async () => {
      try {
        const res = await userStore.getUserInfo()
        
        if (res.success) {
          userInfo.value = res.data
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        uni.showToast({
          title: '获取用户信息失败',
          icon: 'none'
        })
      }
    }
    
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
    
    // 发送手机验证码
    const sendPhoneCode = async () => {
      // 验证手机号
      if (!phoneForm.phone) {
        uni.showToast({
          title: '请输入手机号',
          icon: 'none'
        })
        return
      }
      
      if (!/^1\d{10}$/.test(phoneForm.phone)) {
        uni.showToast({
          title: '手机号格式不正确',
          icon: 'none'
        })
        return
      }
      
      if (phoneForm.counting) return
      
      try {
        uni.showLoading({
          title: '发送中...'
        })
        
        const res = await request({
          url: '/auth/send-code',
          method: 'POST',
          data: {
            phone: phoneForm.phone,
            type: 'bind_phone'
          }
        })
        
        uni.hideLoading()
        
        if (res.code === 200 && res.success) {
          uni.showToast({
            title: '验证码已发送',
            icon: 'success'
          })
          
          // 开始倒计时
          phoneForm.counting = true
          phoneForm.countdown = 60
          
          phoneTimer = setInterval(() => {
            if (phoneForm.countdown > 0) {
              phoneForm.countdown--
            } else {
              clearInterval(phoneTimer)
              phoneForm.counting = false
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
    
    // 发送邮箱验证码
    const sendEmailCode = async () => {
      // 验证邮箱
      if (!emailForm.email) {
        uni.showToast({
          title: '请输入邮箱',
          icon: 'none'
        })
        return
      }
      
      if (!/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(emailForm.email)) {
        uni.showToast({
          title: '邮箱格式不正确',
          icon: 'none'
        })
        return
      }
      
      if (emailForm.counting) return
      
      try {
        uni.showLoading({
          title: '发送中...'
        })
        
        const res = await request({
          url: '/auth/send-code',
          method: 'POST',
          data: {
            email: emailForm.email,
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
          emailForm.counting = true
          emailForm.countdown = 60
          
          emailTimer = setInterval(() => {
            if (emailForm.countdown > 0) {
              emailForm.countdown--
            } else {
              clearInterval(emailTimer)
              emailForm.counting = false
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
    
    // 绑定手机
    const handleBindPhone = async () => {
      // 表单验证
      if (!phoneForm.phone) {
        uni.showToast({
          title: '请输入手机号',
          icon: 'none'
        })
        return
      }
      
      if (!/^1\d{10}$/.test(phoneForm.phone)) {
        uni.showToast({
          title: '手机号格式不正确',
          icon: 'none'
        })
        return
      }
      
      if (!phoneForm.verifyCode) {
        uni.showToast({
          title: '请输入验证码',
          icon: 'none'
        })
        return
      }
      
      try {
        uni.showLoading({
          title: '绑定中...'
        })
        
        const res = await request({
          url: '/user/bind-phone',
          method: 'POST',
          data: {
            phone: phoneForm.phone,
            verify_code: phoneForm.verifyCode
          }
        })
        
        uni.hideLoading()
        
        if (res.code === 200 && res.success) {
          uni.showToast({
            title: '绑定成功',
            icon: 'success'
          })
          
          // 更新用户信息
          userInfo.value.phone = phoneForm.phone
          
          // 清空表单并关闭弹窗
          phoneForm.phone = ''
          phoneForm.verifyCode = ''
          showBindPhoneModal.value = false
        } else {
          uni.showToast({
            title: res.message || '绑定失败',
            icon: 'none'
          })
        }
      } catch (error) {
        uni.hideLoading()
        console.error('绑定手机失败:', error)
        uni.showToast({
          title: '绑定失败，请稍后重试',
          icon: 'none'
        })
      }
    }
    
    // 绑定邮箱
    const handleBindEmail = async () => {
      // 表单验证
      if (!emailForm.email) {
        uni.showToast({
          title: '请输入邮箱',
          icon: 'none'
        })
        return
      }
      
      if (!/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(emailForm.email)) {
        uni.showToast({
          title: '邮箱格式不正确',
          icon: 'none'
        })
        return
      }
      
      if (!emailForm.verifyCode) {
        uni.showToast({
          title: '请输入验证码',
          icon: 'none'
        })
        return
      }
      
      try {
        uni.showLoading({
          title: '绑定中...'
        })
        
        const res = await request({
          url: '/user/bind-email',
          method: 'POST',
          data: {
            email: emailForm.email,
            verify_code: emailForm.verifyCode
          }
        })
        
        uni.hideLoading()
        
        if (res.code === 200 && res.success) {
          uni.showToast({
            title: '绑定成功',
            icon: 'success'
          })
          
          // 更新用户信息
          userInfo.value.email = emailForm.email
          
          // 清空表单并关闭弹窗
          emailForm.email = ''
          emailForm.verifyCode = ''
          showBindEmailModal.value = false
        } else {
          uni.showToast({
            title: res.message || '绑定失败',
            icon: 'none'
          })
        }
      } catch (error) {
        uni.hideLoading()
        console.error('绑定邮箱失败:', error)
        uni.showToast({
          title: '绑定失败，请稍后重试',
          icon: 'none'
        })
      }
    }
    
    // 手机号脱敏
    const maskPhone = (phone) => {
      if (!phone) return '未绑定'
      return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
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
      getUserInfo()
    })
    
    // 页面卸载时清除定时器
    uni.onUnload(() => {
      if (phoneTimer) {
        clearInterval(phoneTimer)
        phoneTimer = null
      }
      
      if (emailTimer) {
        clearInterval(emailTimer)
        emailTimer = null
      }
    })
    
    return {
      userInfo,
      form,
      phoneForm,
      emailForm,
      showBindPhoneModal,
      showBindEmailModal,
      handleChangePassword,
      sendPhoneCode,
      sendEmailCode,
      handleBindPhone,
      handleBindEmail,
      maskPhone,
      maskEmail
    }
  }
}
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20rpx 0 30rpx;
}

.form-section {
  background-color: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.form-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
  position: relative;
  padding-left: 20rpx;
}

.form-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 6rpx;
  height: 30rpx;
  background-color: #4A90E2;
}

.form-group {
  margin-bottom: 20rpx;
}

.form-item {
  margin-bottom: 30rpx;
}

.form-label {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.phone-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #eee;
}

.change-btn {
  background-color: #4A90E2;
  color: #fff;
  font-size: 24rpx;
  padding: 6rpx 20rpx;
  border-radius: 30rpx;
  border: none;
}

.submit-btn {
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

.popup-content {
  width: 600rpx;
  background-color: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
}

.popup-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin-bottom: 30rpx;
}

.popup-form {
  margin-bottom: 30rpx;
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

.popup-btns {
  display: flex;
  justify-content: space-between;
}

.cancel-btn, .confirm-btn {
  width: 260rpx;
  height: 80rpx;
  line-height: 80rpx;
  font-size: 28rpx;
  border-radius: 10rpx;
  border: none;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #666;
}

.confirm-btn {
  background-color: #4A90E2;
  color: #fff;
}
</style> 