<template>
  <view class="container">
    <!-- 头像区域 -->
    <view class="avatar-section">
      <view class="avatar-upload" @click="chooseAvatar">
        <image class="avatar" :src="form.avatar || '/static/images/default-avatar.png'" mode="aspectFill"></image>
        <view class="upload-btn">
          <up-icon name="camera-fill" color="#fff" size="36"></up-icon>
        </view>
      </view>
    </view>

    <!-- 基本信息 -->
    <view class="form-section">
      <view class="form-item" @click="editNickname">
        <text class="form-label">昵称</text>
        <view class="form-value">
          <text class="value-text">{{ form.nickname || '请输入昵称' }}</text>
          <up-icon name="arrow-right" size="20" color="#C7C7CC"></up-icon>
        </view>
      </view>

      <view class="form-item" @click="triggerGenderPicker">
        <text class="form-label">性别</text>
        <view class="form-value">
          <picker ref="genderPicker" :range="genderOptions" range-key="label" :value="getGenderIndex()" @change="onGenderChange" style="position: absolute; opacity: 0; pointer-events: none;">
            <text></text>
          </picker>
          <text class="value-text">{{ getGenderLabel() }}</text>
          <up-icon name="arrow-right" size="20" color="#C7C7CC"></up-icon>
        </view>
      </view>

      <view class="form-item" @click="editPhone">
        <text class="form-label">手机号</text>
        <view class="form-value">
          <text class="value-text">{{ form.phone || '请输入手机号' }}</text>
          <up-icon name="arrow-right" size="20" color="#C7C7CC"></up-icon>
        </view>
      </view>

      <view class="form-item" @click="editEmail">
        <text class="form-label">邮箱</text>
        <view class="form-value">
          <text class="value-text">{{ form.email || '请输入邮箱' }}</text>
          <up-icon name="arrow-right" size="20" color="#C7C7CC"></up-icon>
        </view>
      </view>

      <view class="form-item" @click="triggerDatePicker">
        <text class="form-label">生日</text>
        <view class="form-value">
          <picker ref="datePicker" mode="date" :value="form.birthday" @change="onDateChange" style="position: absolute; opacity: 0; pointer-events: none;">
            <text></text>
          </picker>
          <text class="value-text">{{ form.birthday || '请选择生日' }}</text>
          <up-icon name="arrow-right" size="20" color="#C7C7CC"></up-icon>
        </view>
      </view>
    </view>

    <!-- 个人简介 -->
    <view class="form-section bio-section">
      <view class="form-item" @click="navigateToBioEdit">
        <text class="form-label">个人简介</text>
        <view class="form-value">
          <text class="value-text">{{ form.bio || '编辑个签' }}</text>
          <up-icon name="arrow-right" size="20" color="#C7C7CC"></up-icon>
        </view>
      </view>
    </view>

    <!-- 保存按钮 -->
    <view class="submit-section">
      <button class="submit-btn" @click="handleSubmit">保存修改</button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'


const userStore = useUserStore()



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

// 引用picker组件
const genderPicker = ref(null)
const datePicker = ref(null)

// 触发性别选择器
const triggerGenderPicker = () => {
  // 手动触发隐藏的picker
  const pickerElement = genderPicker.value
  if (pickerElement && pickerElement.$el) {
    pickerElement.$el.click()
  }
}

// 触发日期选择器
const triggerDatePicker = () => {
  // 手动触发隐藏的date picker
  const pickerElement = datePicker.value
  if (pickerElement && pickerElement.$el) {
    pickerElement.$el.click()
  }
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

// 导航到个人简介编辑页
const navigateToBioEdit = () => {
  uni.navigateTo({
    url: `/pages/profile/bio-edit?bio=${encodeURIComponent(form.bio || '')}`
  })
}

// 编辑昵称
const editNickname = () => {
  uni.showModal({
    title: '编辑昵称',
    editable: true,
    content: form.nickname,
    placeholderText: '请输入昵称',
    success: (res) => {
      if (res.confirm && res.content) {
        form.nickname = res.content
      }
    }
  })
}

// 编辑手机号
const editPhone = () => {
  uni.showModal({
    title: '编辑手机号',
    editable: true,
    content: form.phone,
    placeholderText: '请输入手机号',
    success: (res) => {
      if (res.confirm && res.content) {
        if (!/^1\d{10}$/.test(res.content)) {
          uni.showToast({
            title: '手机号格式不正确',
            icon: 'none'
          })
          return
        }
        form.phone = res.content
      }
    }
  })
}

// 编辑邮箱
const editEmail = () => {
  uni.showModal({
    title: '编辑邮箱',
    editable: true,
    content: form.email,
    placeholderText: '请输入邮箱',
    success: (res) => {
      if (res.confirm && res.content) {
        if (!/^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(res.content)) {
          uni.showToast({
            title: '邮箱格式不正确',
            icon: 'none'
          })
          return
        }
        form.email = res.content
      }
    }
  })
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

  // 头像区域
  .avatar-section {
    display: flex;
    justify-content: center;
    padding: 60rpx 0 40rpx;
    background-color: $bg-secondary;

    .avatar-upload {
      position: relative;
      cursor: pointer;

      .avatar {
        width: $avatar-size;
        height: $avatar-size;
        border-radius: $border-radius-circle;
        background-color: $gray-200;
      }

      .upload-btn {
        position: absolute;
        bottom: 8rpx;
        right: 8rpx;
        width: $upload-btn-size;
        height: $upload-btn-size;
        background: $primary-gradient;
        border-radius: $border-radius-circle;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: $shadow-md;

        &:active {
          transform: scale(0.95);
        }
      }
    }
  }

  // 表单区域
  .form-section {
    background-color: $bg-primary;
    margin: 20rpx 0;

    &.bio-section {
      margin-top: 20rpx;
    }

    .form-item {
      display: flex;
      align-items: center;
      min-height: 96rpx;
      padding: 0 30rpx;
      background-color: $bg-primary;
      border-bottom: 1rpx solid $gray-100;

      &:last-child {
        border-bottom: none;
      }

      .form-label {
        font-size: 32rpx;
        font-weight: $font-weight-normal;
        color: $text-primary;
        flex-shrink: 0;
        margin-right: 20rpx;
      }

      .form-value {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        min-height: 60rpx;

        .value-text {
          font-size: 32rpx;
          color: $text-primary;
          margin-right: 16rpx;
          text-align: right;
        }
      }
    }
  }

  // 保存按钮区域
  .submit-section {
    padding: 20rpx;
    padding-top: 0rpx;

    .submit-btn {
      width: 100%;
      height: 88rpx;
      background: $primary-gradient;
      color: $white;
      border: none;
      border-radius: 12rpx;
      font-size: 32rpx;
      font-weight: $font-weight-semibold;
      box-shadow: $shadow-md;
      transition: all 0.2s ease;
      letter-spacing: 1rpx;
      display: flex;
      align-items: center;
      justify-content: center;

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