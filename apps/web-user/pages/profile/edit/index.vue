<template>
  <view class="edit-profile">    
    <!-- 表单内容 -->
    <view class="form-container">
      <!-- 头像选择 -->
      <view class="form-item avatar-item">
        <text class="item-label">头像</text>
        <view class="avatar-selector" @click="selectAvatar">
          <image v-if="userInfo.avatar" class="avatar-preview" :src="userInfo.avatar" mode="aspectFill"></image>
          <view v-else class="avatar-placeholder">
            <text>{{ getInitials(userInfo.nickname) }}</text>
          </view>
          <text class="change-text">更换</text>
        </view>
      </view>
      
      <!-- 昵称输入 -->
      <view class="form-item">
        <text class="item-label">昵称</text>
        <input 
          class="input-field" 
          type="text" 
          v-model="userInfo.nickname" 
          placeholder="请输入昵称"
          maxlength="20"
        />
      </view>
      
      <!-- 性别选择 -->
      <view class="form-item">
        <text class="item-label">性别</text>
        <view class="gender-selector">
          <view 
            class="gender-option" 
            :class="{ active: userInfo.gender === 'male' }"
            @click="userInfo.gender = 'male'"
          >
            <text>男</text>
          </view>
          <view 
            class="gender-option" 
            :class="{ active: userInfo.gender === 'female' }"
            @click="userInfo.gender = 'female'"
          >
            <text>女</text>
          </view>
        </view>
      </view>
      
      <!-- 手机号 -->
      <view class="form-item">
        <text class="item-label">手机号</text>
        <view class="phone-field">
          <text class="phone-number">{{ formatPhone(userInfo.phone) }}</text>
          <view class="change-phone-btn" @click="changePhone">更换手机号</view>
        </view>
      </view>
      
      <!-- 个性签名 -->
      <!-- <view class="form-item">
        <text class="item-label">个性签名</text>
        <textarea 
          class="textarea-field" 
          v-model="userInfo.bio" 
          placeholder="请输入个性签名"
          maxlength="100"
        ></textarea>
        <text class="word-count">{{ userInfo.bio.length }}/100</text>
      </view> -->
      
      <!-- 生日选择 -->
      <view class="form-item">
        <text class="item-label">生日</text>
        <picker 
          mode="date" 
          :value="userInfo.birthday" 
          @change="onBirthdayChange"
          class="date-picker"
        >
          <view class="picker-text">{{ userInfo.birthday || '请选择生日' }}</view>
        </picker>
      </view>
    </view>
    
    <!-- 保存按钮 -->
    <view class="footer">
      <view class="save-button" @click="saveProfileInfo">保存</view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue';

// 用户信息
const userInfo = reactive({
  nickname: '张三',
  avatar: '',
  gender: 'male',
  phone: '13812345678',
//   bio: '热爱生活，享受每一天',
  birthday: '1990-01-01'
});

// 获取昵称首字母
const getInitials = (name) => {
  if (!name) return 'U';
  return name.charAt(0).toUpperCase();
};

// 返回上一页
const goBack = () => {
  uni.navigateBack();
};

// 更换头像
const selectAvatar = () => {
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      userInfo.avatar = res.tempFilePaths[0];
      // 这里通常会有上传头像到服务器的逻辑
    }
  });
};

// 更换手机号
const changePhone = () => {
  uni.navigateTo({
    url: '/pages/profile/edit/phone'
  });
};

// 生日选择器变更
const onBirthdayChange = (e) => {
  userInfo.birthday = e.detail.value;
};

// 格式化手机号为 138****5678 的形式
const formatPhone = (phone) => {
  if (!phone || phone.length < 11) return phone;
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');
};

// 保存用户信息
const saveProfileInfo = () => {
  // 表单验证
  if (!userInfo.nickname.trim()) {
    uni.showToast({
      title: '昵称不能为空',
      icon: 'none'
    });
    return;
  }
  
  // 提交用户信息到服务器
  uni.showLoading({
    title: '保存中...'
  });
  
  setTimeout(() => {
    uni.hideLoading();
    uni.showToast({
      title: '保存成功',
      icon: 'success',
      duration: 2000,
      success: () => {
        setTimeout(() => {
          uni.navigateBack();
        }, 2000);
      }
    });
  }, 1500);
};
</script>

<style lang="scss" scoped>
@import '@/static/theme.scss';

.edit-profile {
  min-height: 100vh;
  background-color: $mg-bg-secondary;
  display: flex;
  flex-direction: column;
}

// 导航栏
.nav-bar {
  display: flex;
  align-items: center;
  height: 90rpx;
  padding: 0 20rpx;
  background-color: $mg-bg-primary;
  position: relative;
  
  .nav-left {
    width: 80rpx;
    display: flex;
    align-items: center;
    
    .nav-icon {
      font-size: 44rpx;
      color: $mg-text-primary;
    }
  }
  
  .nav-title {
    flex: 1;
    text-align: center;
    font-size: 36rpx;
    font-weight: 500;
    color: $mg-text-primary;
  }
  
  .nav-right {
    width: 80rpx;
  }
}

// 表单容器
.form-container {
  background-color: $mg-bg-primary;
  padding: 20rpx 30rpx;
  margin-top: 20rpx;
}

// 表单项
.form-item {
  padding: 30rpx 0;
  border-bottom: 1px solid $mg-border-light;
  position: relative;
  
  &:last-child {
    border-bottom: none;
  }
  
  .item-label {
    font-size: 30rpx;
    color: $mg-text-primary;
    margin-bottom: 20rpx;
    display: block;
  }
  
  .input-field {
    font-size: 30rpx;
    color: $mg-text-primary;
    height: 60rpx;
    width: 100%;
  }
  
  .textarea-field {
    font-size: 30rpx;
    color: $mg-text-primary;
    width: 100%;
    height: 180rpx;
    line-height: 1.5;
  }
  
  .word-count {
    position: absolute;
    right: 0;
    bottom: 30rpx;
    font-size: 24rpx;
    color: $mg-text-tertiary;
  }
  
  .picker-text {
    font-size: 30rpx;
    color: $mg-text-primary;
    height: 60rpx;
    line-height: 60rpx;
  }
}

// 头像选择
.avatar-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  
  .item-label {
    margin-bottom: 0;
  }
  
  .avatar-selector {
    position: relative;
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    overflow: hidden;
    
    .avatar-preview {
      width: 100%;
      height: 100%;
    }
    
    .avatar-placeholder {
      width: 100%;
      height: 100%;
      background-color: $mg-primary;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 48rpx;
      color: $mg-white;
      font-weight: bold;
    }
    
    .change-text {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 40rpx;
      line-height: 40rpx;
      text-align: center;
      font-size: 22rpx;
      color: $mg-white;
      background-color: rgba(0, 0, 0, 0.5);
    }
  }
}

// 性别选择
.gender-selector {
  display: flex;
  
  .gender-option {
    flex: 1;
    height: 70rpx;
    line-height: 70rpx;
    text-align: center;
    border: 1px solid $mg-border-light;
    font-size: 28rpx;
    color: $mg-text-secondary;
    margin-right: 20rpx;
    border-radius: 8rpx;
    
    &:last-child {
      margin-right: 0;
    }
    
    &.active {
      color: $mg-primary;
      border-color: $mg-primary;
      background-color: $mg-bg-gold-light;
    }
  }
}

// 手机号
.phone-field {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .phone-number {
    font-size: 30rpx;
    color: $mg-text-primary;
  }
  
  .change-phone-btn {
    font-size: 28rpx;
    color: $mg-primary;
  }
}

// 底部保存按钮
.footer {
  padding: 40rpx 30rpx;
  
  .save-button {
    height: 90rpx;
    background-color: $mg-primary;
    color: $mg-white;
    font-size: 32rpx;
    font-weight: 500;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12rpx;
  }
}
</style>
