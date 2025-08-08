<template>
  <view class="container">
    <Navbar title="编辑资料" :showLeft="true" :showRight="false" @leftClick="goBack" />

    <view class="form-section">
      <view class="avatar-upload">
        <image class="avatar" :src="form.avatar || '/static/images/default-avatar.png'" mode="aspectFill"></image>
        <view class="upload-btn" @click="chooseAvatar">
          <up-icon name="camera-fill" color="#fff" size="40"></up-icon>
        </view>
      </view>

      <view class="form-group">
        <view class="form-item">
          <text class="form-label">用户名</text>
          <up--input v-model="form.username" placeholder="请输入用户名" border="bottom" disabled></up--input>
        </view>

        <view class="form-item">
          <text class="form-label">昵称</text>
          <up--input v-model="form.nickname" placeholder="请输入昵称" border="bottom"></up--input>
        </view>

        <view class="form-item">
          <text class="form-label">性别</text>
          <radio-group @change="onGenderChange">
            <label class="radio-item" v-for="(item, index) in genderOptions" :key="index">
              <radio :value="item.value" :checked="form.gender === item.value" />
              <text>{{ item.label }}</text>
            </label>
          </radio-group>
        </view>

        <view class="form-item">
          <text class="form-label">手机号</text>
          <up--input v-model="form.phone" placeholder="请输入手机号" border="bottom" type="number"></up--input>
        </view>

        <view class="form-item">
          <text class="form-label">邮箱</text>
          <up--input v-model="form.email" placeholder="请输入邮箱" border="bottom" type="email"></up--input>
        </view>

        <view class="form-item">
          <text class="form-label">生日</text>
          <picker mode="date" :value="form.birthday" @change="onDateChange">
            <view class="date-picker">
              <text class="date-text">{{ form.birthday || '请选择生日' }}</text>
              <up-icon name="calendar" size="30" color="#999"></up-icon>
            </view>
          </picker>
        </view>

        <view class="form-item">
          <text class="form-label">个人简介</text>
          <textarea v-model="form.bio" placeholder="请输入个人简介" class="bio-textarea" maxlength="200"></textarea>
          <view class="char-count">{{ (form.bio || '').length }}/200</view>
        </view>
      </view>

      <button class="submit-btn" @click="handleSubmit">保存修改</button>
    </view>


  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'
import Navbar from '@/components/Navbar.vue'

const userStore = useUserStore()

// 返回上一页
const goBack = () => {
  uni.navigateBack()
}

const form = reactive({
  avatar: '',
  username: '',
  nickname: '',
  gender: 0,
  phone: '',
  email: '',
  birthday: '',
  bio: ''
})

const genderOptions = [
  { value: 1, label: '男' },
  { value: 2, label: '女' },
  { value: 0, label: '保密' }
]



// 获取用户信息
const getUserInfo = async () => {
  try {
    const res = await userStore.getUserInfo()

    if (res.success) {
      // 填充表单数据
      const userInfo = res.data
      form.avatar = userInfo.avatar || ''
      form.username = userInfo.username || ''
      form.nickname = userInfo.nickname || ''
      form.gender = userInfo.gender || 0
      form.phone = userInfo.phone || ''
      form.email = userInfo.email || ''
      form.birthday = userInfo.birthday || ''
      form.bio = userInfo.bio || ''
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    uni.showToast({
      title: '获取用户信息失败',
      icon: 'none'
    })
  }
}

// 日期选择处理
const onDateChange = (e) => {
  form.birthday = e.detail.value
}

// 性别选择处理
const onGenderChange = (e) => {
  form.gender = parseInt(e.detail.value)
}

// 选择头像
const chooseAvatar = () => {
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      const tempFilePath = res.tempFilePaths[0]

      // 上传头像
      uploadAvatar(tempFilePath)
    }
  })
}

// 上传头像
const uploadAvatar = (filePath) => {
  uni.showLoading({
    title: '上传中...'
  })

  uni.uploadFile({
    url: '/api/upload/avatar',
    filePath: filePath,
    name: 'file',
    header: {
      Authorization: `Bearer ${userStore.token}`
    },
    success: (uploadRes) => {
      try {
        const data = JSON.parse(uploadRes.data)

        if (data.code === 200 && data.success) {
          form.avatar = data.data.url

          uni.showToast({
            title: '上传成功',
            icon: 'success'
          })
        } else {
          uni.showToast({
            title: data.message || '上传失败',
            icon: 'none'
          })
        }
      } catch (error) {
        console.error('解析上传结果失败:', error)
        uni.showToast({
          title: '上传失败',
          icon: 'none'
        })
      }
    },
    fail: () => {
      uni.showToast({
        title: '上传失败',
        icon: 'none'
      })
    },
    complete: () => {
      uni.hideLoading()
    }
  })
}

// 提交表单
const handleSubmit = async () => {
  // 表单验证
  if (!form.nickname) {
    uni.showToast({
      title: '请输入昵称',
      icon: 'none'
    })
    return
  }

  if (form.phone && !/^1\d{10}$/.test(form.phone)) {
    uni.showToast({
      title: '手机号格式不正确',
      icon: 'none'
    })
    return
  }

  if (form.email && !/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(form.email)) {
    uni.showToast({
      title: '邮箱格式不正确',
      icon: 'none'
    })
    return
  }

  try {
    uni.showLoading({
      title: '保存中...'
    })

    const res = await userStore.updateUserInfo({
      avatar: form.avatar,
      nickname: form.nickname,
      gender: form.gender,
      phone: form.phone,
      email: form.email,
      birthday: form.birthday,
      bio: form.bio
    })

    uni.hideLoading()

    if (res.success) {
      uni.showToast({
        title: '保存成功',
        icon: 'success'
      })

      // 返回上一页
      setTimeout(() => {
        uni.navigateBack()
      }, 1500)
    } else {
      uni.showToast({
        title: res.message || '保存失败',
        icon: 'none'
      })
    }
  } catch (error) {
    uni.hideLoading()
    console.error('更新用户信息失败:', error)
    uni.showToast({
      title: '保存失败，请稍后重试',
      icon: 'none'
    })
  }
}

// 页面加载
onLoad(() => {
  getUserInfo()
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 30rpx;
}

.form-section {
  background-color: #fff;
  padding: 30rpx;

  .avatar-upload {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 40rpx;
    position: relative;

    .avatar {
      width: 160rpx;
      height: 160rpx;
      border-radius: 50%;
      background-color: #f0f0f0;
    }

    .upload-btn {
      position: absolute;
      bottom: 0;
      right: 50%;
      transform: translateX(50rpx);
      width: 60rpx;
      height: 60rpx;
      background-color: rgba(74, 144, 226, 0.8);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
}

.form-group {
  margin-bottom: 40rpx;

  .form-item {
    margin-bottom: 30rpx;

    .form-label {
      font-size: 28rpx;
      color: #333;
      margin-bottom: 20rpx;
      display: block;
    }
  }
}

.date-picker {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 80rpx;
  border-bottom: 1rpx solid #eee;

  .date-text {
    font-size: 28rpx;
    color: #333;
  }
}

.radio-item {
  display: inline-flex;
  align-items: center;
  margin-right: 32rpx;
  margin-bottom: 16rpx;

  radio {
    margin-right: 8rpx;
  }

  text {
    font-size: 28rpx;
    color: #333;
  }
}

.bio-textarea {
  width: 100%;
  height: 150rpx;
  padding: 20rpx;
  border: 1rpx solid #eee;
  border-radius: 8rpx;
  font-size: 28rpx;
  color: #333;
  background-color: #fff;
  resize: none;
}

.char-count {
  text-align: right;
  font-size: 24rpx;
  color: #999;
  margin-top: 8rpx;
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
</style>