<template>
  <view class="container">
    <!-- <Navbar title="请完善订单信息" /> -->

    <!-- 主要内容 -->
    <view class="content">
      <!-- 咨询人信息 -->
      <view class="section">
        <view class="section-title">咨询人</view>
        
        <!-- 显示所有咨询人选项 -->
        <view v-if="consultantList.length > 0">
          <view 
            v-for="consultant in consultantList" 
            :key="consultant.id"
            class="consultant-card" 
            :class="{ selected: selectedConsultant?.id === consultant.id }"
            @click="selectConsultant(consultant)"
          >
            <view class="consultant-info">
              <view class="consultant-name">{{ consultant.name }}</view>
              <view class="consultant-details">
                <text class="detail-text">{{ getConsultantAge(consultant) }}</text>
                <text class="detail-text">{{ consultant.phone }}</text>
              </view>
            </view>
            <u-icon 
              v-if="selectedConsultant?.id === consultant.id" 
              name="checkmark" 
              size="16" 
              color="#4A90E2"
            ></u-icon>
          </view>
        </view>
        
        <!-- 添加新咨询人按钮 -->
        <view class="client-card" @click="showClientPicker">
          <view class="add-client">
            <u-icon name="plus" size="24" color="#999"></u-icon>
            <text class="add-client-text">新增咨询人</text>
          </view>
        </view>
      </view>

      <!-- 咨询类型 -->
      <view class="section">
        <view class="section-title">咨询类型</view>
        <view class="consultation-types">
          <view 
            class="type-item" 
            :class="{ active: selectedType === type.value }"
            v-for="type in consultationTypes" 
            :key="type.value"
            @click="selectType(type.value)"
          >
            <text class="type-text">{{ type.label }}</text>
          </view>
        </view>
      </view>

      <!-- 咨询方式 -->
      <view class="section">
        <view class="section-title">咨询方式</view>
        <view class="consultation-methods">
          <view 
            class="method-item" 
            :class="{ active: selectedMethod === method.value }"
            v-for="method in consultationMethods" 
            :key="method.value"
            @click="selectMethod(method.value)"
          >
            <text class="method-text">{{ method.label }}</text>
          </view>
        </view>
      </view>

      <!-- 可约时间 -->
      <view class="section">
        <view class="section-title">可约时间</view>
        <view class="time-schedule">
          <view 
            class="date-item" 
            v-for="(date, index) in availableDates" 
            :key="index"
          >
            <view class="date-info">
              <text class="date-text">{{ date.date }}</text>
              <text class="weekday-text">{{ date.weekday }}</text>
            </view>
            <view class="time-slots">
              <view 
                class="time-slot" 
                :class="{ 
                  active: selectedTimeSlot === slot.id,
                  disabled: !slot.available,
                  full: slot.status === 'full'
                }"
                v-for="slot in date.timeSlots" 
                :key="slot.id"
                @click="selectTimeSlot(slot)"
              >
                <text class="slot-text" v-if="slot.available">{{ slot.time }}</text>
                <text class="slot-text full" v-else-if="slot.status === 'full'">已满</text>
                <text class="slot-text disabled" v-else>-</text>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 固定底部 -->
    <view class="fixed-bottom">
      <view class="price-info">
        <text class="price-label">共计：</text>
        <text class="price-symbol">¥</text>
        <text class="price-amount">{{ totalPrice }}</text>
      </view>
      <button 
        class="submit-btn" 
        :disabled="!canSubmit"
        @click="submitOrder"
      >
        提交订单
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { consultantAPI } from '@/api/consultant'
import Navbar from '@/components/Navbar.vue'

// 页面参数
const counselorId = ref('')
const counselorInfo = ref({})

// 表单数据
const selectedClient = ref('')
const selectedConsultant = ref(null)
const selectedType = ref('')
const selectedMethod = ref('')
const selectedTimeSlot = ref('')

// 咨询人相关
const consultantList = ref([])

// 咨询类型选项
const consultationTypes = ref([
  { label: '个人咨询', value: 'individual' },
  { label: '情侣咨询', value: 'couple' },
  { label: '家庭咨询', value: 'family' }
])

// 咨询方式选项
const consultationMethods = ref([
  { label: '视频咨询', value: 'video' },
  { label: '语音咨询', value: 'audio' },
  { label: '面对面咨询', value: 'offline' }
])

// 可约时间数据
const availableDates = ref([
  {
    date: '8·7',
    weekday: '周四',
    timeSlots: [
      { id: '1', time: '已满', available: false, status: 'full' }
    ]
  },
  {
    date: '8·8',
    weekday: '周五',
    timeSlots: [
      { id: '2', time: '-', available: false, status: 'unavailable' }
    ]
  },
  {
    date: '8·9',
    weekday: '周六',
    timeSlots: [
      { id: '3', time: '16:00', available: true },
      { id: '4', time: '18:00', available: true }
    ]
  },
  {
    date: '8·10',
    weekday: '周日',
    timeSlots: [
      { id: '5', time: '16:00', available: true }
    ]
  },
  {
    date: '8·11',
    weekday: '周一',
    timeSlots: [
      { id: '6', time: '19:00', available: true }
    ]
  },
  {
    date: '8·12',
    weekday: '周二',
    timeSlots: [
      { id: '7', time: '9:00', available: true },
      { id: '8', time: '15:00', available: true }
    ]
  }
])

// 计算属性
const totalPrice = computed(() => {
  return counselorInfo.value.price || 0
})

const canSubmit = computed(() => {
  return (selectedClient.value || selectedConsultant.value) && selectedType.value && selectedMethod.value && selectedTimeSlot.value
})

// 方法

const showClientPicker = () => {
  uni.showActionSheet({
    itemList: ['新增成人账户', '新增儿童账户'],
    success: (res) => {
      if (res.tapIndex === 0) {
        // 跳转到咨询人创建页面
        uni.navigateTo({
          url: '/pages/consultant/create'
        })
      } else {
        // 新增儿童账户（暂时保持原逻辑或后续实现）
        selectedClient.value = 'child'
      }
    }
  })
}

// 获取咨询人列表
const fetchConsultantList = async () => {
  try {
    const result = await consultantAPI.getConsultants({
      page: 1,
      per_page: 20
    })
    
    if (result.success && result.data) {
      consultantList.value = result.data.list || result.data.consultants || []
    }
  } catch (error) {
    console.error('获取咨询人列表失败:', error)
  }
}

// 获取咨询人年龄信息
const getConsultantAge = (consultant) => {
  if (consultant.birth_year && consultant.birth_month) {
    const currentYear = new Date().getFullYear()
    const age = currentYear - consultant.birth_year
    return `${consultant.birth_year}年${consultant.birth_month}月 (${age}岁)`
  }
  return '年龄未知'
}

// 选择咨询人
const selectConsultant = (consultant) => {
  selectedConsultant.value = consultant
}

const selectType = (type) => {
  selectedType.value = type
}

const selectMethod = (method) => {
  selectedMethod.value = method
}

const selectTimeSlot = (slot) => {
  if (!slot.available) return
  
  selectedTimeSlot.value = slot.id
}

const submitOrder = () => {
  if (!canSubmit.value) {
    uni.showToast({
      title: '请完善预约信息',
      icon: 'none'
    })
    return
  }

  // 构建订单数据
  const orderData = {
    counselor_id: counselorId.value,
    client_type: selectedClient.value,
    consultant_id: selectedConsultant.value?.id,
    consultation_type: selectedType.value,
    consultation_method: selectedMethod.value,
    time_slot_id: selectedTimeSlot.value,
    total_price: totalPrice.value
  }


  // 跳转到订单支付页面
  uni.navigateTo({
    url: `/pages/order/submit?data=${encodeURIComponent(JSON.stringify(orderData))}`
  })
}

// 页面加载
onLoad((options) => {
  if (options.counselor_id) {
    counselorId.value = options.counselor_id
    // 获取咨询师信息
    fetchCounselorInfo()
  }
})

// 页面显示时（从其他页面返回时会触发）
onShow(() => {
  // 刷新咨询人列表，以便获取新创建的咨询人
  fetchConsultantList()
})

const fetchCounselorInfo = async () => {
  try {
    // 这里应该调用API获取咨询师信息
    counselorInfo.value = {
      id: counselorId.value,
      name: '咨询师姓名',
      price: 600
    }
  } catch (error) {
    console.error('获取咨询师信息失败:', error)
  }
}

onMounted(() => {
  // 页面初始化
  fetchConsultantList()
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-top: 88rpx; /* 为Navbar留出空间 */
  padding-bottom: 120rpx;
}

.content {
  padding: 20rpx;
}

.section {
  margin-bottom: 40rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 20rpx;
}

.client-card {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.add-client {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40rpx 0;
  border: 2rpx dashed #ddd;
  border-radius: 8rpx;
}

.add-client-text {
  font-size: 28rpx;
  color: #999;
  margin-top: 15rpx;
}

.consultant-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 30rpx;
  background-color: #fff;
  border: 1rpx solid #f0f0f0;
  border-radius: 12rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.consultant-card.selected {
  background-color: #e6f7ff;
  border: 1rpx solid #4a90e2;
  box-shadow: 0 4rpx 12rpx rgba(74, 144, 226, 0.2);
}

.consultant-info {
  flex: 1;
  margin-right: 20rpx;
}

.consultant-name {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 5rpx;
}

.consultant-details {
  display: flex;
  gap: 10rpx;
}

.detail-text {
  font-size: 24rpx;
  color: #666;
}

.consultation-types,
.consultation-methods {
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
}

.type-item,
.method-item {
  background-color: #fff;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  padding: 20rpx 30rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.type-item.active,
.method-item.active {
  border-color: #4A90E2;
  background-color: #e6f7ff;
}

.type-text,
.method-text {
  font-size: 28rpx;
  color: #333;
}

.type-item.active .type-text,
.method-item.active .method-text {
  color: #4A90E2;
  font-weight: 600;
}

.time-schedule {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.date-item {
  display: flex;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f5f5f5;
}

.date-item:last-child {
  border-bottom: none;
}

.date-info {
  width: 120rpx;
  flex-shrink: 0;
  margin-right: 30rpx;
}

.date-text {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  display: block;
  margin-bottom: 5rpx;
}

.weekday-text {
  font-size: 24rpx;
  color: #666;
}

.time-slots {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
}

.time-slot {
  background-color: #f5f5f5;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  padding: 12rpx 20rpx;
  min-width: 100rpx;
  text-align: center;
}

.time-slot.active {
  background-color: #4A90E2;
  border-color: #4A90E2;
}

.time-slot.disabled {
  background-color: #f9f9f9;
  border-color: #f0f0f0;
}

.time-slot.full {
  background-color: #fff2f0;
  border-color: #ffccc7;
}

.slot-text {
  font-size: 24rpx;
  color: #333;
}

.time-slot.active .slot-text {
  color: #fff;
  font-weight: 600;
}

.slot-text.disabled {
  color: #ccc;
}

.slot-text.full {
  color: #ff4d4f;
}

.fixed-bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #fff;
  padding: 25rpx 30rpx;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
  z-index: 100;
  border-top: 1rpx solid #f0f0f0;
}

.price-info {
  display: flex;
  align-items: baseline;
}

.price-label {
  font-size: 28rpx;
  color: #333;
  margin-right: 10rpx;
}

.price-symbol {
  font-size: 28rpx;
  color: #ff4d4f;
  font-weight: bold;
  margin-right: 2rpx;
}

.price-amount {
  font-size: 36rpx;
  font-weight: bold;
  color: #ff4d4f;
}

.submit-btn {
  background: linear-gradient(135deg, #4A90E2, #1890ff);
  color: #fff;
  font-size: 30rpx;
  font-weight: 600;
  padding: 0;
  border-radius: 40rpx;
  border: none;
  width: 200rpx;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 16rpx rgba(74, 144, 226, 0.4);
}

.submit-btn:disabled {
  background: linear-gradient(135deg, #d9d9d9, #f0f0f0);
  color: #999;
  box-shadow: none;
}
</style>
