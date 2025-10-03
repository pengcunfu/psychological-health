<template>
  <view class="container">
    <!-- 隐私保护提示 -->
    <view class="privacy-notice" v-if="showPrivacyNotice">
      <text class="shield-icon">🛡️</text>
      <text class="privacy-text">平台会保证您的隐私安全，请放心如实填写</text>
      <text class="close-icon" @click="hidePrivacyNotice">×</text>
    </view>

    <!-- 咨询人信息 -->
    <view class="form-section">
      <view class="section-header">咨询人信息</view>
      
      <view class="form-item">
        <text class="form-label">
          <text class="required-mark">*</text>
          真实姓名
        </text>
        <input v-model="formData.name" placeholder="请输入真实姓名" class="form-input" />
      </view>

      <view class="form-item" @click="triggerDatePicker">
        <text class="form-label">
          <text class="required-mark">*</text>
          出生年月
        </text>
        <picker 
          ref="datePicker"
          mode="date" 
          fields="month" 
          :value="datePickerValue" 
          :start="datePickerStart" 
          :end="datePickerEnd"
          @change="onDateConfirm"
          style="position: absolute; opacity: 0; pointer-events: none;"
        >
          <text></text>
        </picker>
        <view class="form-value">
          <text class="value-text" :class="{ placeholder: !dateDisplay }">
            {{ dateDisplay || '请选择出生年月' }}
          </text>
        </view>
      </view>

      <view class="form-item gender-item">
        <text class="form-label">
          <text class="required-mark">*</text>
          性别
        </text>
        <view class="gender-options">
          <view class="gender-option" :class="{ active: formData.gender === 'male' }" @click="selectGender('male')">
            <view class="radio-icon" :class="{ checked: formData.gender === 'male' }">
              <view class="radio-inner" v-if="formData.gender === 'male'"></view>
            </view>
            <text class="gender-text">男</text>
          </view>
          <view class="gender-option" :class="{ active: formData.gender === 'female' }" @click="selectGender('female')">
            <view class="radio-icon" :class="{ checked: formData.gender === 'female' }">
              <view class="radio-inner" v-if="formData.gender === 'female'"></view>
            </view>
            <text class="gender-text">女</text>
          </view>
        </view>
      </view>

      <view class="form-item">
        <text class="form-label">
          <text class="required-mark">*</text>
          联系方式
        </text>
        <input v-model="formData.phone" placeholder="请输入手机号码" type="number" maxlength="11" class="form-input" />
      </view>
    </view>

    <!-- 监护人信息 -->
    <view class="form-section">
      <view class="section-header">监护人信息</view>

      <view class="form-item">
        <text class="form-label">
          <text class="required-mark">*</text>
          真实姓名
        </text>
        <input v-model="formData.emergencyContact.name" placeholder="请输入紧急联系人姓名" class="form-input" />
      </view>

      <view class="form-item" @click="triggerRelationshipPicker">
        <text class="form-label">
          <text class="required-mark">*</text>
          TA是您的
        </text>
        <picker 
          ref="relationshipPicker"
          mode="selector" 
          :range="relationshipList" 
          range-key="label" 
          :value="relationshipIndex"
          @change="onRelationshipConfirm"
          style="position: absolute; opacity: 0; pointer-events: none;"
        >
          <text></text>
        </picker>
        <view class="form-value">
          <text class="value-text" :class="{ placeholder: !formData.emergencyContact.relationship }">
            {{ getRelationshipText(formData.emergencyContact.relationship) || '请选择关系' }}
          </text>
        </view>
      </view>

      <view class="form-item">
        <text class="form-label">
          <text class="required-mark">*</text>
          联系电话
        </text>
        <input v-model="formData.emergencyContact.phone" placeholder="请输入紧急联系人电话" type="number" maxlength="11"
          class="form-input" />
      </view>
    </view>

    <!-- 协议同意 -->
    <view class="agreement-section">
      <view class="agreement-item" @click="toggleAgreement">
        <view class="checkbox-wrapper">
          <view class="checkbox" :class="{ checked: formData.agreeToTerms }">
            <u-icon v-if="formData.agreeToTerms" name="checkmark" size="16" color="#fff"></u-icon>
          </view>
        </view>
        <view class="agreement-content">
          <text class="agreement-text">我同意并签署</text>
          <text class="agreement-link" @click.stop="showAgreement">《咨询预约协议书》</text>
        </view>
      </view>
    </view>

    <!-- 固定底部 -->
    <view class="submit-section">
      <button class="submit-btn" :disabled="!canSave" @click="saveConsultant">
        保存
      </button>
    </view>


  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { consultantAPI } from '@/api/consultant'

// 页面参数
const isEdit = ref(false)
const consultantId = ref('')

// Picker组件引用
const datePicker = ref(null)
const relationshipPicker = ref(null)

// 表单数据
const formData = reactive({
  name: '',
  birth_year: null,
  birth_month: null,
  gender: '',
  phone: '',
  emergencyContact: {
    name: '',
    relationship: '',
    phone: ''
  },
  agreeToTerms: false
})

// 日期相关
const datePickerShow = ref(false)
const datePickerValue = ref('')
const datePickerStart = ref('1940-01')
const datePickerEnd = ref(new Date().toISOString().substr(0, 7))

// 关系选择器
const relationshipPickerShow = ref(false)
const relationshipList = ref([
  { label: '本人', value: 'self' },
  { label: '配偶', value: 'spouse' },
  { label: '子女', value: 'child' },
  { label: '父母', value: 'parent' },
  { label: '兄弟姐妹', value: 'sibling' },
  { label: '朋友', value: 'friend' },
  { label: '其他', value: 'other' }
])
const relationshipIndex = ref(0)

// 隐私提示显示状态
const showPrivacyNotice = ref(true)

// 计算属性
const dateDisplay = computed(() => {
  if (formData.birth_year && formData.birth_month) {
    return `${formData.birth_year}年${formData.birth_month}月`
  }
  return ''
})

const canSave = computed(() => {
  return formData.name &&
    formData.birth_year &&
    formData.birth_month &&
    formData.gender &&
    formData.phone &&
    formData.emergencyContact.name &&
    formData.emergencyContact.relationship &&
    formData.emergencyContact.phone &&
    formData.agreeToTerms
})

// 方法
const hidePrivacyNotice = () => {
  showPrivacyNotice.value = false
}

const showDatePicker = () => {
  // 原生picker通过点击触发，不需要显示状态控制
}

const onDateConfirm = (e) => {
  const dateValue = e.detail.value
  datePickerValue.value = dateValue
  const [year, month] = dateValue.split('-')
  formData.birth_year = parseInt(year)
  formData.birth_month = parseInt(month)
  datePickerShow.value = false
}

const selectGender = (gender) => {
  formData.gender = gender
}

// 手动触发日期选择器
const triggerDatePicker = () => {
  const pickerElement = datePicker.value
  if (pickerElement && pickerElement.$el) {
    pickerElement.$el.click()
  }
}

// 手动触发关系选择器
const triggerRelationshipPicker = () => {
  const pickerElement = relationshipPicker.value
  if (pickerElement && pickerElement.$el) {
    pickerElement.$el.click()
  }
}

const onRelationshipConfirm = (e) => {
  const index = e.detail.value
  relationshipIndex.value = index
  formData.emergencyContact.relationship = relationshipList.value[index].value
  relationshipPickerShow.value = false
}

const getRelationshipText = (value) => {
  const option = relationshipList.value.find(item => item.value === value)
  return option ? option.label : ''
}

const toggleAgreement = () => {
  formData.agreeToTerms = !formData.agreeToTerms
}

const showAgreement = () => {
  uni.navigateTo({
    url: '/pages/consultant/agreement'
  })
}

const validatePhone = (phone) => {
  const phoneReg = /^1[3-9]\d{9}$/
  return phoneReg.test(phone)
}

const saveConsultant = async () => {
  try {
    // 表单验证
    if (!formData.name.trim()) {
      uni.showToast({
        title: '请输入真实姓名',
        icon: 'none'
      })
      return
    }

    if (!validatePhone(formData.phone)) {
      uni.showToast({
        title: '请输入正确的手机号码',
        icon: 'none'
      })
      return
    }

    if (!validatePhone(formData.emergencyContact.phone)) {
      uni.showToast({
        title: '请输入正确的紧急联系人电话',
        icon: 'none'
      })
      return
    }

    if (!formData.agreeToTerms) {
      uni.showToast({
        title: '请同意咨询预约协议书',
        icon: 'none'
      })
      return
    }

    uni.showLoading({
      title: isEdit.value ? '保存中...' : '创建中...'
    })

    // 构建提交数据
    const submitData = {
      real_name: formData.name.trim(),
      birth_year: formData.birth_year,
      birth_month: formData.birth_month,
      gender: formData.gender,
      phone: formData.phone,
      emergency_name: formData.emergencyContact.name.trim(),
      emergency_relationship: formData.emergencyContact.relationship,
      emergency_phone: formData.emergencyContact.phone,
      notes: `性别：${formData.gender === 'male' ? '男' : '女'}，紧急联系人：${formData.emergencyContact.name}（${getRelationshipText(formData.emergencyContact.relationship)}）`
    }

    let result
    if (isEdit.value) {
      result = await consultantAPI.updateConsultant(consultantId.value, submitData)
    } else {
      result = await consultantAPI.createConsultant(submitData)
    }

    uni.hideLoading()

    if (result.success) {
      uni.showToast({
        title: isEdit.value ? '保存成功' : '创建成功',
        icon: 'success'
      })

      setTimeout(() => {
        uni.navigateBack()
      }, 1500)
    } else {
      uni.showToast({
        title: result.message || '操作失败',
        icon: 'none'
      })
    }
  } catch (error) {
    uni.hideLoading()
    console.error('保存咨询人失败:', error)
    uni.showToast({
      title: '网络异常，请重试',
      icon: 'none'
    })
  }
}

const loadConsultantData = async () => {
  try {
    uni.showLoading({
      title: '加载中...'
    })

    const result = await consultantAPI.getConsultantDetail(consultantId.value)

    if (result.success && result.data) {
      const data = result.data
      
      // 基本信息 - 使用正确的字段名
      formData.name = data.real_name || ''
      formData.birth_year = data.birth_year
      formData.birth_month = data.birth_month
      formData.gender = data.gender || ''
      formData.phone = data.phone || ''
      
      // 紧急联系人信息
      formData.emergencyContact.name = data.emergency_name || ''
      formData.emergencyContact.relationship = data.emergency_relationship || ''
      formData.emergencyContact.phone = data.emergency_phone || ''
      
      // 设置日期选择器的值
      if (data.birth_year && data.birth_month) {
        const year = data.birth_year.toString().padStart(4, '0')
        const month = data.birth_month.toString().padStart(2, '0')
        datePickerValue.value = `${year}-${month}`
      }
      
      // 设置关系选择器的值
      if (data.emergency_relationship) {
        const relationshipIdx = relationshipList.value.findIndex(item => item.value === data.emergency_relationship)
        if (relationshipIdx !== -1) {
          relationshipIndex.value = relationshipIdx
        }
      }
      
      // 默认同意协议（编辑模式下认为已经同意过）
      formData.agreeToTerms = true
      
      console.log('数据加载成功:', data)
      console.log('表单数据:', formData)
    }

    uni.hideLoading()
  } catch (error) {
    uni.hideLoading()
    console.error('加载咨询人数据失败:', error)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  }
}

// 页面加载
onLoad((options) => {
  // 获取系统信息，设置状态栏高度
  const systemInfo = uni.getSystemInfoSync()
  const statusBarHeight = systemInfo.statusBarHeight || 0

  // 设置CSS变量
  const style = document.documentElement.style || document.body.style
  if (style) {
    style.setProperty('--status-bar-height', statusBarHeight + 'px')
  }

  if (options.id) {
    isEdit.value = true
    consultantId.value = options.id
    loadConsultantData()
  }
})

onMounted(() => {
  // 页面初始化
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background-color: #F2F2F7;
  padding-bottom: 120rpx;
}

.privacy-notice {
  background-color: #e6f7ff;
  padding: 20rpx 30rpx;
  padding-top: calc(20rpx + var(--status-bar-height, 0px));
  display: flex;
  align-items: center;
  border-bottom: 1rpx solid #91d5ff;
}

.privacy-text {
  flex: 1;
  font-size: 24rpx;
  color: #4A90E2;
  margin-left: 10rpx;
  margin-right: 15rpx;
}

// 表单区域
.form-section {
  background-color: #FFFFFF;
  margin: 20rpx 0;
  border-radius: 12rpx;
  overflow: hidden;

  .section-header {
    padding: 30rpx 30rpx 20rpx;
    font-size: 32rpx;
    font-weight: 600;
    color: #1C1C1E;
    background-color: #F8F9FA;
    border-bottom: 1rpx solid #E5E5EA;
  }

  .form-item {
    display: flex;
    align-items: center;
    min-height: 96rpx;
    padding: 0 30rpx;
    border-bottom: 1rpx solid #E5E5EA;

    &:last-child {
      border-bottom: none;
    }

    &.gender-item {
      align-items: center;
      justify-content: space-between;
    }

    .form-label {
      font-size: 32rpx;
      color: #1C1C1E;
      flex-shrink: 0;
      margin-right: 20rpx;
      display: flex;
      align-items: center;

      .required-mark {
        color: #FF3B30;
        margin-right: 8rpx;
        font-size: 32rpx;
      }
    }

    .form-input {
      flex: 1;
      text-align: right;
      font-size: 32rpx;
      color: #1C1C1E;
      border: none;
      outline: none;
      background: transparent;
      padding: 0;

      &::placeholder {
        color: #8E8E93;
      }
    }

    .form-value {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: flex-end;

      .value-text {
        font-size: 32rpx;
        color: #1C1C1E;

        text-align: right;

        &.placeholder {
          color: #8E8E93;
        }
      }
    }
  }
}

// 性别选择
.gender-options {
  display: flex;
  align-items: center;
  gap: 40rpx;

  .gender-option {
    display: flex;
    align-items: center;
    gap: 12rpx;
    cursor: pointer;

    .radio-icon {
      width: 40rpx;
      height: 40rpx;
      border-radius: 50%;
      border: 2rpx solid #C7C7CC;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;

      &.checked {
        border-color: #007AFF;
      }

      .radio-inner {
        width: 20rpx;
        height: 20rpx;
        border-radius: 50%;
        background-color: #007AFF;
      }
    }

    .gender-text {
      font-size: 32rpx;
      color: #1C1C1E;
    }
  }
}

// 协议同意区域
.agreement-section {
  margin: 40rpx 20rpx;

  .agreement-item {
    display: flex;
    align-items: flex-start;
    gap: 20rpx;
    padding: 30rpx;
    background-color: #FFFFFF;
    border-radius: 12rpx;
    cursor: pointer;

    .checkbox-wrapper {
      flex-shrink: 0;
      padding-top: 4rpx;

      .checkbox {
        width: 40rpx;
        height: 40rpx;
        border-radius: 8rpx;
        border: 2rpx solid #C7C7CC;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;

        &.checked {
          background-color: #007AFF;
          border-color: #007AFF;
        }
      }
    }

    .agreement-content {
      flex: 1;
      display: flex;
      flex-wrap: wrap;
      align-items: center;

      .agreement-text {
        font-size: 28rpx;
        color: #48484A;
        margin-right: 8rpx;
      }

      .agreement-link {
        font-size: 28rpx;
        color: #007AFF;
        text-decoration: underline;
      }
    }
  }
}

// 提交按钮区域
.submit-section {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #FFFFFF;
  padding: 20rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  border-top: 1rpx solid #E5E5EA;
  z-index: 100;

  .submit-btn {
    width: 100%;
    height: 88rpx;
    background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
    color: #FFFFFF;
    border: none;
    border-radius: 12rpx;
    font-size: 32rpx;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
    transition: all 0.2s ease;
    letter-spacing: 1rpx;

    &:active {
      transform: scale(0.98);
      box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
    }

    &:disabled {
      background: #C7C7CC;
      color: #8E8E93;
      box-shadow: none;
      transform: none;
    }
  }
}

// 隐私提示样式
.shield-icon {
  font-size: 32rpx;
  margin-right: 10rpx;
}

.close-icon {
  font-size: 32rpx;
  color: #8E8E93;
  font-weight: bold;
  cursor: pointer;
  padding: 8rpx;
}
</style>
