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
          <view class="form-input">
            <up--input v-model="form.username" placeholder="请输入用户名" border="none" disabled></up--input>
          </view>
        </view>

        <view class="form-item">
          <text class="form-label">昵称</text>
          <view class="form-input">
            <up--input v-model="form.nickname" placeholder="请输入昵称" border="none"></up--input>
          </view>
        </view>

        <view class="form-item">
          <text class="form-label">性别</text>
          <picker :range="genderOptions" range-key="label" :value="getGenderIndex()" @change="onGenderChange">
            <view class="form-picker">
              <text class="picker-text">{{ getGenderLabel() }}</text>
              <up-icon name="arrow-down" size="24" color="#999"></up-icon>
            </view>
          </picker>
        </view>

        <view class="form-item">
          <text class="form-label">手机号</text>
          <view class="form-input">
            <up--input v-model="form.phone" placeholder="请输入手机号" border="none" type="number"></up--input>
          </view>
        </view>

        <view class="form-item">
          <text class="form-label">邮箱</text>
          <view class="form-input">
            <up--input v-model="form.email" placeholder="请输入邮箱" border="none" type="email"></up--input>
          </view>
        </view>

        <view class="form-item">
          <text class="form-label">生日</text>
          <picker mode="date" :value="form.birthday" @change="onDateChange">
            <view class="form-picker">
              <text class="picker-text">{{ form.birthday || '请选择生日' }}</text>
              <up-icon name="calendar" size="24" color="#999"></up-icon>
            </view>
          </picker>
        </view>

        <view class="form-item">
          <text class="form-label">个人简介</text>
          <view class="form-input bio-input">
            <textarea v-model="form.bio" placeholder="请输入个人简介" class="bio-textarea" maxlength="200"></textarea>
            <view class="char-count">{{ (form.bio || '').length }}/200</view>
          </view>
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
  const index = e.detail.value
  form.gender = genderOptions[index].value
}

// 获取性别索引
const getGenderIndex = () => {
  return genderOptions.findIndex(item => item.value === form.gender)
}

// 获取性别标签
const getGenderLabel = () => {
  const option = genderOptions.find(item => item.value === form.gender)
  return option ? option.label : '请选择性别'
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
// SCSS变量 - 现代化设计系统
$primary-color: #007AFF;
$primary-gradient: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
$primary-light: rgba(0, 122, 255, 0.1);
$primary-alpha: rgba(0, 122, 255, 0.8);

$white: #FFFFFF;
$gray-50: #FAFAFA;
$gray-100: #F5F5F7;
$gray-200: #E5E5EA;
$gray-300: #D1D1D6;
$gray-400: #C7C7CC;
$gray-500: #8E8E93;
$gray-600: #636366;
$gray-700: #48484A;
$gray-800: #2C2C2E;
$gray-900: #1C1C1E;

$text-primary: #1C1C1E;
$text-secondary: #48484A;
$text-tertiary: #8E8E93;
$text-placeholder: #C7C7CC;

$bg-primary: #FFFFFF;
$bg-secondary: #F2F2F7;
$bg-tertiary: #FAFAFA;

$shadow-sm: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
$shadow-md: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
$shadow-lg: 0 8rpx 24rpx rgba(0, 0, 0, 0.12);

$padding-xs: 8rpx;
$padding-sm: 12rpx;
$padding-md: 16rpx;
$padding-lg: 20rpx;
$padding-xl: 24rpx;
$padding-2xl: 32rpx;

$margin-xs: 8rpx;
$margin-sm: 12rpx;
$margin-md: 16rpx;
$margin-lg: 20rpx;
$margin-xl: 24rpx;
$margin-2xl: 32rpx;

$avatar-size: 180rpx;
$upload-btn-size: 64rpx;
$form-item-height: 96rpx;
$submit-btn-height: 96rpx;

$border-radius-xs: 4rpx;
$border-radius-sm: 8rpx;
$border-radius-md: 12rpx;
$border-radius-lg: 16rpx;
$border-radius-xl: 20rpx;
$border-radius-circle: 50%;

$font-size-xs: 22rpx;
$font-size-sm: 24rpx;
$font-size-md: 28rpx;
$font-size-lg: 32rpx;
$font-size-xl: 36rpx;

$font-weight-normal: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;

.container {
  min-height: 100vh;
  background-color: $bg-secondary;
  padding-bottom: 120rpx;

  .form-section {
    background-color: $bg-primary;
    margin: $margin-xl;
    border-radius: $border-radius-lg;
    box-shadow: $shadow-sm;
    overflow: hidden;

    .avatar-upload {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: $padding-2xl $padding-xl;
      background: $primary-light;
      position: relative;

      .avatar {
        width: $avatar-size;
        height: $avatar-size;
        border-radius: $border-radius-circle;
        background-color: $gray-200;
        box-shadow: $shadow-md;
        border: 4rpx solid $white;
      }

      .upload-btn {
        position: absolute;
        bottom: $padding-xl;
        right: 50%;
        transform: translateX(calc(50% + 30rpx));
        width: $upload-btn-size;
        height: $upload-btn-size;
        background: $primary-gradient;
        border-radius: $border-radius-circle;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: $shadow-md;
        border: 3rpx solid $white;

        &:active {
          transform: translateX(calc(50% + 30rpx)) scale(0.95);
        }
      }
    }

    .form-group {
      padding: 0 $padding-xl $padding-lg;

      .form-item {
        display: flex;
        align-items: center;
        min-height: $form-item-height;
        padding: $padding-lg 0;
        background-color: $bg-primary;
        transition: all 0.2s ease;

        &:not(:last-child) {
          border-bottom: 1rpx solid $gray-100;
        }

        &:hover {
          background-color: $bg-tertiary;
        }

        .form-label {
          font-size: $font-size-md;
          font-weight: $font-weight-medium;
          color: $text-secondary;
          width: 140rpx;
          flex-shrink: 0;
          line-height: 1.4;
        }

        .form-input {
          flex: 1;
          margin-left: $margin-lg;

          &.bio-input {
            display: flex;
            flex-direction: column;

            .bio-textarea {
              width: 100%;
              min-height: 80rpx;
              padding: $padding-sm;
              border: none;
              border-radius: $border-radius-sm;
              font-size: $font-size-md;
              color: $text-primary;
              background-color: $bg-tertiary;
              resize: none;
              line-height: 1.5;
              font-family: inherit;

              &:focus {
                background-color: $primary-light;
                outline: none;
              }
            }

            .char-count {
              text-align: right;
              font-size: $font-size-xs;
              color: $text-tertiary;
              margin-top: $margin-xs;
              font-weight: $font-weight-normal;
            }
          }
        }

        .form-picker {
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex: 1;
          margin-left: $margin-lg;
          padding: $padding-sm $padding-md;
          background-color: $bg-tertiary;
          border-radius: $border-radius-sm;
          transition: all 0.2s ease;

          &:active {
            background-color: $primary-light;
            transform: scale(0.98);
          }

          .picker-text {
            font-size: $font-size-md;
            color: $text-primary;
            font-weight: $font-weight-normal;
          }
        }
      }
    }

    .submit-btn {
      width: calc(100% - #{$padding-xl * 2});
      height: $submit-btn-height;
      background: $primary-gradient;
      color: $white;
      border: none;
      border-radius: $border-radius-lg;
      font-size: $font-size-lg;
      font-weight: $font-weight-semibold;
      margin: $margin-2xl $padding-xl;
      box-shadow: $shadow-md;
      transition: all 0.2s ease;
      letter-spacing: 1rpx;

      &:active {
        transform: scale(0.98);
        box-shadow: $shadow-sm;
      }

      &:disabled {
        background: $gray-300;
        color: $gray-500;
        box-shadow: none;
        transform: none;
      }
    }
  }
}
</style>