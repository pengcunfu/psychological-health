<template>
  <view class="container">
    <!-- 隐私保护提示 -->
    <view class="privacy-notice" v-if="showPrivacyNotice">
      <text class="shield-icon">🛡️</text>
      <text class="privacy-text">平台会保证您的隐私安全，请放心如实填写</text>
      <text class="close-icon" @click="hidePrivacyNotice">×</text>
    </view>

    <!-- 主要内容 -->
    <view class="content">
      <!-- 咨询人信息 -->
      <view class="form-item">
        <view class="form-row">
          <view class="form-label">
            <text class="required-mark">*</text>
            <text>真实姓名</text>
          </view>
          <input
            v-model="formData.name"
            placeholder="请输入真实姓名"
            class="form-input"
          />
        </view>
      </view>

      <!-- 出生年月 -->
      <view class="form-item">
        <picker
          mode="date"
          fields="month"
          :value="datePickerValue"
          :start="datePickerStart"
          :end="datePickerEnd"
          @change="onDateConfirm"
        >
          <view class="form-row">
            <view class="form-label">
              <text class="required-mark">*</text>
              <text>出生年月</text>
            </view>
            <view class="form-value">
              <text class="date-display" :class="{ placeholder: !dateDisplay }">
                {{ dateDisplay || '请选择出生年月' }}
              </text>
              <text class="arrow-icon">></text>
            </view>
          </view>
        </picker>
      </view>

      <!-- 性别 -->
      <view class="form-item">
        <view class="form-row">
          <view class="form-label">
            <text class="required-mark">*</text>
            <text>性别</text>
          </view>
          <view class="gender-options">
            <view 
              class="gender-item" 
              :class="{ active: formData.gender === 'male' }"
              @click="selectGender('male')"
            >
              <view class="radio-icon" :class="{ checked: formData.gender === 'male' }">
                <view class="radio-inner" v-if="formData.gender === 'male'"></view>
              </view>
              <text class="gender-text">男</text>
            </view>
            <view 
              class="gender-item" 
              :class="{ active: formData.gender === 'female' }"
              @click="selectGender('female')"
            >
              <view class="radio-icon" :class="{ checked: formData.gender === 'female' }">
                <view class="radio-inner" v-if="formData.gender === 'female'"></view>
              </view>
              <text class="gender-text">女</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 联系方式 -->
      <view class="form-item">
        <view class="form-row">
          <view class="form-label">
            <text class="required-mark">*</text>
            <text>联系方式</text>
          </view>
          <input
            v-model="formData.phone"
            placeholder="请输入手机号码"
            type="number"
            maxlength="11"
            class="form-input"
          />
        </view>
      </view>

      <!-- 紧急联系人标题 -->
      <view class="section-title-main">紧急联系人</view>
      
      <!-- 紧急联系人姓名 -->
      <view class="form-item">
        <view class="form-row">
          <view class="form-label">
            <text class="required-mark">*</text>
            <text>真实姓名</text>
          </view>
          <input
            v-model="formData.emergencyContact.name"
            placeholder="请输入紧急联系人姓名"
            class="form-input"
          />
        </view>
      </view>

      <!-- 关系选择 -->
      <view class="form-item">
        <picker
          mode="selector"
          :range="relationshipList"
          range-key="label"
          :value="relationshipIndex"
          @change="onRelationshipConfirm"
        >
          <view class="form-row">
            <view class="form-label">
              <text class="required-mark">*</text>
              <text>TA是您的</text>
            </view>
            <view class="form-value">
              <text class="relationship-display" :class="{ placeholder: !formData.emergencyContact.relationship }">
                {{ getRelationshipText(formData.emergencyContact.relationship) || '请选择关系' }}
              </text>
              <text class="arrow-icon">></text>
            </view>
          </view>
        </picker>
      </view>

      <!-- 紧急联系人电话 -->
      <view class="form-item">
        <view class="form-row">
          <view class="form-label">
            <text class="required-mark">*</text>
            <text>联系电话</text>
          </view>
          <input
            v-model="formData.emergencyContact.phone"
            placeholder="请输入紧急联系人电话"
            type="number"
            maxlength="11"
            class="form-input"
          />
        </view>
      </view>

      <!-- 协议同意 -->
      <view class="agreement-section">
        <view class="agreement-checkbox" @click="toggleAgreement">
          <text class="agreement-text">我同意并签署</text>
          <text class="agreement-link" @click.stop="showAgreement">《咨询预约协议书》</text>
        </view>
      </view>
    </view>

    <!-- 固定底部 -->
    <view class="fixed-bottom">
      <button 
        class="save-btn" 
        :disabled="!canSave"
        @click="saveConsultant"
      >
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

const showRelationshipPicker = () => {
  // 原生picker通过点击触发，不需要显示状态控制
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
    url: '/pages/webview?url=agreement'
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
      formData.name = data.name || ''
      formData.birth_year = data.birth_year
      formData.birth_month = data.birth_month
      formData.gender = data.gender || ''
      formData.phone = data.phone || ''
      
      // 解析备注中的紧急联系人信息（如果有的话）
      if (data.notes) {
        // 这里可以根据实际的数据结构来解析
        // 暂时使用默认值
      }
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
  background-color: #ffffff;
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

.content {
  padding: 40rpx 30rpx;
}

.section-title-main {
  font-size: 36rpx;
  font-weight: 600;
  color: #333;
  margin: 60rpx 0 40rpx 0;
}

.form-item {
  border-bottom: 1rpx solid #f0f0f0;
  padding: 30rpx 0;
}

.form-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.form-label {
  display: flex;
  align-items: center;
  font-size: 32rpx;
  color: #333;
  min-width: 160rpx;
}

.form-input {
  flex: 1;
  text-align: right;
  font-size: 32rpx;
  color: #333;
  border: none;
  outline: none;
  background: transparent;
  padding: 0;
  margin-left: 20rpx;
}

.form-input::placeholder {
  color: #999;
}

.form-value {
  display: flex;
  align-items: center;
  flex: 1;
  justify-content: flex-end;
}

.required-mark {
  color: #ff4d4f;
  margin-right: 8rpx;
  font-size: 32rpx;
}



.date-display {
  font-size: 32rpx;
  color: #333;
  margin-right: 10rpx;
}

.date-display.placeholder {
  color: #999;
}

.gender-options {
  display: flex;
  align-items: center;
  gap: 60rpx;
}

.gender-item {
  display: flex;
  align-items: center;
  gap: 15rpx;
  cursor: pointer;
}

.gender-text {
  font-size: 32rpx;
  color: #333;
}

.radio-icon {
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  border: 2rpx solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.radio-icon.checked {
  border-color: #333;
}

.radio-inner {
  width: 20rpx;
  height: 20rpx;
  border-radius: 50%;
  background-color: #333;
}



.relationship-display {
  font-size: 32rpx;
  color: #333;
  margin-right: 10rpx;
}

.relationship-display.placeholder {
  color: #999;
}

.agreement-section {
  margin-top: 60rpx;
  margin-bottom: 40rpx;
  text-align: center;
}

.agreement-checkbox {
  display: flex;
  align-items: center;
  justify-content: center;
}

.agreement-text {
  font-size: 28rpx;
  color: #666;
  margin-right: 5rpx;
}

.agreement-link {
  font-size: 28rpx;
  color: #4A90E2;
  text-decoration: underline;
}

.fixed-bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #fff;
  padding: 25rpx 30rpx;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  z-index: 100;
  border-top: 1rpx solid #f0f0f0;
}

.save-btn {
  background-color: #333;
  color: #fff;
  font-size: 32rpx;
  font-weight: 500;
  padding: 0;
  border-radius: 8rpx;
  border: none;
  width: 100%;
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.save-btn:disabled {
  background-color: #ccc;
  color: #999;
}

/* 原生组件样式 */
.shield-icon {
  font-size: 32rpx;
  margin-right: 10rpx;
}

.close-icon {
  font-size: 32rpx;
  color: #999;
  font-weight: bold;
  cursor: pointer;
}

.arrow-icon {
  font-size: 28rpx;
  color: #999;
}
</style>
