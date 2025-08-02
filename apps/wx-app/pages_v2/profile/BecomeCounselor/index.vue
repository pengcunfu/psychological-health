<template>
  <view class="become-counselor">
    <!-- 内容区域 -->
    <scroll-view scroll-y class="content-area">
      <!-- 说明文本 -->
      <view class="instruction-box">
        <text class="title">加入我们的咨询师团队</text>
        <text class="desc">成为专业咨询师，帮助更多人解决心理困扰，实现自我价值。我们将对您的资质进行严格审核，确保平台服务质量。</text>
      </view>

      <!-- 表单区域 -->
      <view class="form-area">
        <!-- 个人信息 -->
        <view class="form-section">
          <view class="section-title">基本信息</view>

          <view class="form-item">
            <text class="label">真实姓名</text>
            <input class="input" type="text" v-model="formData.realName" placeholder="请输入您的真实姓名" />
          </view>

          <view class="form-item">
            <text class="label">性别</text>
            <view class="radio-group">
              <view class="radio-item" :class="{ active: formData.gender === 'male' }"
                @click="formData.gender = 'male'">
                <text class="radio-dot"></text>
                <text>男</text>
              </view>
              <view class="radio-item" :class="{ active: formData.gender === 'female' }"
                @click="formData.gender = 'female'">
                <text class="radio-dot"></text>
                <text>女</text>
              </view>
            </view>
          </view>

          <view class="form-item">
            <text class="label">联系电话</text>
            <input class="input" type="number" v-model="formData.phone" placeholder="请输入您的联系电话" />
          </view>

          <view class="form-item">
            <text class="label">邮箱</text>
            <input class="input" type="text" v-model="formData.email" placeholder="请输入您的电子邮箱" />
          </view>
        </view>

        <!-- 专业资质 -->
        <view class="form-section">
          <view class="section-title">专业资质</view>

          <view class="form-item">
            <text class="label">最高学历</text>
            <picker class="picker" mode="selector" :range="educationLevels" @change="handleEducationChange">
              <view class="picker-text">{{ formData.education || '请选择最高学历' }}</view>
              <!-- <text class="iconfont right-icon">&#xe6e1;</text> -->
            </picker>
          </view>

          <view class="form-item">
            <text class="label">毕业院校</text>
            <input class="input" type="text" v-model="formData.university" placeholder="请输入您的毕业院校" />
          </view>

          <view class="form-item">
            <text class="label">专业方向</text>
            <input class="input" type="text" v-model="formData.major" placeholder="如：心理学、精神医学等" />
          </view>

          <view class="form-item">
            <text class="label">从业年限</text>
            <picker class="picker" mode="selector" :range="experienceYears" @change="handleExperienceChange">
              <view class="picker-text">{{ formData.years || '请选择从业年限' }}</view>
              <!-- <text class="iconfont right-icon">&#xe6e1;</text> -->
            </picker>
          </view>

          <view class="form-item">
            <text class="label">擅长领域</text>
            <view class="tags-container">
              <view v-for="(tag, index) in expertiseTags" :key="index" class="tag"
                :class="{ active: formData.expertise.includes(tag) }" @click="toggleExpertise(tag)">
                {{ tag }}
              </view>
            </view>
          </view>
        </view>

        <!-- 资质证明 -->
        <view class="form-section">
          <view class="section-title">资质证明</view>

          <view class="form-item upload-item">
            <text class="label">职业资格证书</text>
            <view class="upload-area" @click="uploadCertificate">
              <view v-if="!formData.certificate" class="upload-placeholder">
                <text class="iconfont upload-icon">&#xe67c;</text>
                <text class="upload-text">点击上传证书照片</text>
              </view>
              <image v-else class="uploaded-image" :src="formData.certificate" mode="aspectFill"></image>
            </view>
          </view>

          <view class="form-item upload-item">
            <text class="label">身份证照片</text>
            <view class="upload-area" @click="uploadIdCard">
              <view v-if="!formData.idCard" class="upload-placeholder">
                <text class="iconfont upload-icon">&#xe67c;</text>
                <text class="upload-text">点击上传身份证正面照片</text>
              </view>
              <image v-else class="uploaded-image" :src="formData.idCard" mode="aspectFill"></image>
            </view>
          </view>
        </view>

        <!-- 个人简介 -->
        <view class="form-section">
          <view class="section-title">个人简介</view>

          <view class="form-item">
            <text class="label">个人简介</text>
            <textarea class="textarea" v-model="formData.introduction" placeholder="请简要描述您的工作经历、专业背景和咨询风格等（300字以内）"
              maxlength="300"></textarea>
            <text class="word-count">{{ formData.introduction.length }}/300</text>
          </view>
        </view>

        <!-- 提交按钮 -->
        <view class="submit-area">
          <button class="submit-btn" @click="submitApplication">提交申请</button>
          <text class="tip-text">提交申请后，我们将在7个工作日内完成审核</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue';

// 表单数据
const formData = reactive({
  realName: '',
  gender: '',
  phone: '',
  email: '',
  education: '',
  university: '',
  major: '',
  years: '',
  expertise: [],
  certificate: '',
  idCard: '',
  introduction: ''
});

// 下拉选项
const educationLevels = ['大专', '本科', '硕士', '博士'];
const experienceYears = ['1-3年', '3-5年', '5-10年', '10年以上'];

// 擅长领域标签
const expertiseTags = [
  '抑郁症', '焦虑症', '睡眠障碍', '强迫症', '恐惧症',
  '情绪管理', '人际关系', '婚姻家庭', '青少年心理', '职场压力',
  '个人成长', '生涯规划', '创伤后应激', '性心理', '性格障碍'
];

// 切换擅长领域选择
const toggleExpertise = (tag) => {
  const index = formData.expertise.indexOf(tag);
  if (index > -1) {
    formData.expertise.splice(index, 1);
  } else {
    if (formData.expertise.length < 5) {
      formData.expertise.push(tag);
    } else {
      uni.showToast({
        title: '最多选择5个擅长领域',
        icon: 'none'
      });
    }
  }
};

// 处理学历选择
const handleEducationChange = (e) => {
  formData.education = educationLevels[e.detail.value];
};

// 处理从业年限选择
const handleExperienceChange = (e) => {
  formData.years = experienceYears[e.detail.value];
};

// 上传证书
const uploadCertificate = () => {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      // 实际项目中应该调用上传API
      formData.certificate = res.tempFilePaths[0];
    }
  });
};

// 上传身份证
const uploadIdCard = () => {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      // 实际项目中应该调用上传API
      formData.idCard = res.tempFilePaths[0];
    }
  });
};

// 提交申请
const submitApplication = () => {
  // 开发阶段跳过验证
  uni.navigateTo({
    url: '/pages/counselor/workspace/index'
  })

  // 表单验证
  if (!formData.realName) {
    return uni.showToast({
      title: '请输入真实姓名',
      icon: 'none'
    });
  }

  if (!formData.gender) {
    return uni.showToast({
      title: '请选择性别',
      icon: 'none'
    });
  }

  if (!formData.phone) {
    return uni.showToast({
      title: '请输入联系电话',
      icon: 'none'
    });
  }

  if (!formData.education) {
    return uni.showToast({
      title: '请选择最高学历',
      icon: 'none'
    });
  }

  if (!formData.university) {
    return uni.showToast({
      title: '请输入毕业院校',
      icon: 'none'
    });
  }

  if (!formData.years) {
    return uni.showToast({
      title: '请选择从业年限',
      icon: 'none'
    });
  }

  if (formData.expertise.length === 0) {
    return uni.showToast({
      title: '请选择擅长领域',
      icon: 'none'
    });
  }

  if (!formData.certificate) {
    return uni.showToast({
      title: '请上传职业资格证书',
      icon: 'none'
    });
  }

  if (!formData.idCard) {
    return uni.showToast({
      title: '请上传身份证照片',
      icon: 'none'
    });
  }

  if (!formData.introduction) {
    return uni.showToast({
      title: '请填写个人简介',
      icon: 'none'
    });
  }

  // TODO: 调用申请成为咨询师API
  uni.showLoading({
    title: '提交中...'
  });

  setTimeout(() => {
    uni.hideLoading();
    uni.showModal({
      title: '申请已提交',
      content: '您的申请已成功提交，我们将在7个工作日内完成审核，请留意通知消息',
      showCancel: false,
      success: () => {
        goBack();
      }
    });
  }, 1500);
};

// 返回上一页
const goBack = () => {
  uni.navigateBack();
};
</script>

<style lang="scss" scoped>
@import '@/static/theme.scss';

.become-counselor {
  min-height: 100vh;
  background-color: $mg-bg-secondary;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-top: 20rpx;
  padding-bottom: 20rpx;
}

// 内容区域
.content-area {
  flex: 1;
  padding: 20rpx 30rpx;
  box-sizing: border-box;
  width: 100%;
  height: 100%;
}

// 说明文本框
.instruction-box {
  background-color: $mg-bg-gold-light;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;

  .title {
    font-size: 32rpx;
    font-weight: bold;
    color: $mg-primary-dark;
    margin-bottom: 16rpx;
    display: block;
  }

  .desc {
    font-size: 28rpx;
    color: $mg-text-secondary;
    line-height: 1.5;
  }
}

// 表单区域
.form-area {
  box-sizing: border-box;
  width: 100%;
  margin: 0 auto;

  .form-section {
    box-sizing: border-box;
    background-color: $mg-white;
    border-radius: 12rpx;
    padding: 30rpx;
    margin-bottom: 30rpx;

    .section-title {
      font-size: 32rpx;
      font-weight: 500;
      color: $mg-text-primary;
      margin-bottom: 30rpx;
      position: relative;
      padding-left: 20rpx;

      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 6rpx;
        width: 8rpx;
        height: 32rpx;
        background-color: $mg-primary;
        border-radius: 4rpx;
      }
    }

    .form-item {
      margin-bottom: 30rpx;
      box-sizing: border-box;

      .label {
        font-size: 28rpx;
        color: $mg-text-secondary;
        margin-bottom: 16rpx;
        display: block;
      }

      .input {
        box-sizing: border-box;
        width: 100%;
        height: 80rpx;
        background-color: $mg-bg-secondary;
        border-radius: 8rpx;
        padding: 0 20rpx;
        font-size: 28rpx;
        color: $mg-text-primary;
      }

      .textarea {
        box-sizing: border-box;
        width: 100%;
        height: 240rpx;
        background-color: $mg-bg-secondary;
        border-radius: 8rpx;
        padding: 20rpx;
        font-size: 28rpx;
        color: $mg-text-primary;
      }

      .word-count {
        font-size: 24rpx;
        color: $mg-text-tertiary;
        text-align: right;
        display: block;
        margin-top: 8rpx;
      }

      .radio-group {
        display: flex;

        .radio-item {
          display: flex;
          align-items: center;
          margin-right: 60rpx;

          .radio-dot {
            width: 40rpx;
            height: 40rpx;
            border-radius: 20rpx;
            border: 2rpx solid $mg-border-medium;
            margin-right: 10rpx;
            position: relative;

            &::after {
              content: '';
              position: absolute;
              width: 24rpx;
              height: 24rpx;
              background-color: $mg-primary;
              border-radius: 12rpx;
              left: 50%;
              top: 50%;
              transform: translate(-50%, -50%);
              opacity: 0;
            }
          }

          &.active {
            .radio-dot {
              border-color: $mg-primary;

              &::after {
                opacity: 1;
              }
            }
          }
        }
      }

      .picker {
        box-sizing: border-box;
        width: 100%;
        height: 80rpx;
        background-color: $mg-bg-secondary;
        border-radius: 8rpx;
        padding: 0 20rpx;
        display: flex;
        align-items: center;
        justify-content: space-between;

        .picker-text {
          font-size: 28rpx;
          color: $mg-text-primary;
        }

        .right-icon {
          font-size: 32rpx;
          color: $mg-text-tertiary;
        }
      }

      .tags-container {
        display: flex;
        flex-wrap: wrap;

        .tag {
          height: 60rpx;
          padding: 0 30rpx;
          background-color: $mg-bg-secondary;
          border-radius: 30rpx;
          margin-right: 20rpx;
          margin-bottom: 20rpx;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 26rpx;
          color: $mg-text-secondary;

          &.active {
            background-color: $mg-bg-gold-light;
            color: $mg-primary;
            border: 1rpx solid $mg-primary;
          }
        }
      }
    }

    .upload-item {
      .upload-area {
        width: 100%;
        height: 200rpx;
        background-color: $mg-bg-secondary;
        border-radius: 8rpx;
        overflow: hidden;

        .upload-placeholder {
          width: 100%;
          height: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;

          .upload-icon {
            font-size: 48rpx;
            color: $mg-text-tertiary;
            margin-bottom: 16rpx;
          }

          .upload-text {
            font-size: 26rpx;
            color: $mg-text-tertiary;
          }
        }

        .uploaded-image {
          width: 100%;
          height: 100%;
        }
      }
    }
  }
}

// 提交区域
.submit-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 40rpx 0 100rpx;
  box-sizing: border-box;

  .submit-btn {
    width: 90%;
    height: 88rpx;
    background-color: $mg-primary;
    color: $mg-white;
    font-size: 32rpx;
    border-radius: 44rpx;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .tip-text {
    font-size: 24rpx;
    color: $mg-text-tertiary;
    margin-top: 20rpx;
  }
}
</style>