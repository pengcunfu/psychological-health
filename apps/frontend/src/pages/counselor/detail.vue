<template>
  <view class="container">
    <view class="counselor-header">
      <view class="counselor-basic">
        <u-avatar :src="counselorInfo.avatar || '/static/images/default-avatar.png'" size="160"></u-avatar>
        <view class="counselor-info">
          <text class="counselor-name">{{ counselorInfo.name || '加载中...' }}</text>
          <view class="counselor-title">{{ counselorInfo.title || '' }}</view>
          <view class="counselor-rating">
            <u-icon name="star-fill" color="#faad14" size="24"></u-icon>
            <text class="rating-text">{{ counselorInfo.rating || '5.0' }}</text>
            <text class="consultation-count">{{ counselorInfo.consultation_count || 0 }}次咨询</text>
          </view>
          <view class="counselor-tags">
            <text class="tag" v-for="(tag, index) in tags" :key="index">{{ tag }}</text>
          </view>
        </view>
      </view>
      <view class="price-section">
        <text class="price">¥{{ counselorInfo.price || 0 }}/次</text>
        <button class="appointment-btn" @click="handleAppointment">立即预约</button>
      </view>
    </view>

    <view class="tab-section">
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'intro' }" 
        @click="switchTab('intro')"
      >
        简介
      </view>
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'comments' }" 
        @click="switchTab('comments')"
      >
        评价({{ commentCount }})
      </view>
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'schedule' }" 
        @click="switchTab('schedule')"
      >
        排班
      </view>
    </view>

    <view class="content-section">
      <!-- 简介 -->
      <view v-if="activeTab === 'intro'" class="intro-content">
        <view class="section-block">
          <view class="block-title">咨询师介绍</view>
          <view class="block-content">
            <text class="intro-text">{{ counselorInfo.introduction || '暂无介绍' }}</text>
          </view>
        </view>
        
        <view class="section-block">
          <view class="block-title">专业领域</view>
          <view class="block-content">
            <view class="field-item" v-for="(field, index) in fields" :key="index">
              <u-icon name="checkmark-circle" color="#4A90E2" size="30"></u-icon>
              <text class="field-text">{{ field }}</text>
            </view>
          </view>
        </view>
        
        <view class="section-block">
          <view class="block-title">教育背景</view>
          <view class="block-content">
            <view class="education-item" v-for="(edu, index) in education" :key="index">
              <text class="edu-year">{{ edu.year }}</text>
              <view class="edu-info">
                <text class="edu-school">{{ edu.school }}</text>
                <text class="edu-degree">{{ edu.degree }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 评价 -->
      <view v-if="activeTab === 'comments'" class="comments-content">
        <view v-if="comments.length > 0">
          <view class="comment-item" v-for="(comment, index) in comments" :key="index">
            <view class="comment-header">
              <u-avatar :src="comment.user_avatar || '/static/images/default-avatar.png'" size="80"></u-avatar>
              <view class="comment-user">
                <text class="comment-username">{{ comment.username }}</text>
                <view class="comment-rating">
                  <u-rate :value="comment.rating" readonly size="16" active-color="#faad14"></u-rate>
                  <text class="comment-time">{{ comment.create_time }}</text>
                </view>
              </view>
            </view>
            <view class="comment-body">
              <text class="comment-text">{{ comment.content }}</text>
            </view>
            <view class="comment-footer" v-if="comment.reply">
              <text class="reply-label">咨询师回复：</text>
              <text class="reply-text">{{ comment.reply }}</text>
            </view>
          </view>
        </view>
        <view v-else class="empty-content">
          <u-empty mode="comment" icon="chat" text="暂无评价"></u-empty>
        </view>
      </view>
      
      <!-- 排班 -->
      <view v-if="activeTab === 'schedule'" class="schedule-content">
        <view class="calendar-section">
          <view class="calendar-header">
            <u-icon name="arrow-left" size="30" @click="prevWeek"></u-icon>
            <text class="calendar-title">{{ currentWeekText }}</text>
            <u-icon name="arrow-right" size="30" @click="nextWeek"></u-icon>
          </view>
          
          <view class="calendar-days">
            <view 
              class="day-item" 
              v-for="(day, index) in weekDays" 
              :key="index"
              :class="{ 'day-active': selectedDay === day.date }"
              @click="selectDay(day.date)"
            >
              <text class="day-name">{{ day.name }}</text>
              <text class="day-date">{{ day.day }}</text>
            </view>
          </view>
        </view>
        
        <view class="time-slots">
          <view class="time-slot-title">可预约时段</view>
          <view v-if="timeSlots.length > 0" class="time-slot-list">
            <view 
              class="time-slot-item" 
              v-for="(slot, index) in timeSlots" 
              :key="index"
              :class="{ 'slot-selected': selectedSlot === slot.id, 'slot-disabled': !slot.available }"
              @click="selectTimeSlot(slot)"
            >
              {{ slot.start_time }} - {{ slot.end_time }}
            </view>
          </view>
          <view v-else class="empty-content">
            <u-empty mode="list" icon="calendar" text="暂无可预约时段"></u-empty>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { request } from '@/utils/request'
import { checkLogin } from '@/utils/auth'

export default {
  setup() {
    const counselorId = ref('')
    const counselorInfo = ref({})
    const activeTab = ref('intro')
    const tags = ref([])
    const fields = ref([])
    const education = ref([])
    const comments = ref([])
    const commentCount = ref(0)
    const weekDays = ref([])
    const currentWeek = ref(0)
    const selectedDay = ref('')
    const timeSlots = ref([])
    const selectedSlot = ref('')
    
    // 获取咨询师信息
    const fetchCounselorInfo = async () => {
      try {
        const res = await request({
          url: `/counselor/${counselorId.value}`,
          method: 'GET'
        })
        
        if (res.code === 200 && res.success) {
          counselorInfo.value = res.data || {}
          
          // 处理标签
          if (typeof counselorInfo.value.tags === 'string') {
            tags.value = counselorInfo.value.tags.split(',').filter(tag => tag.trim() !== '')
          } else if (Array.isArray(counselorInfo.value.tags)) {
            tags.value = counselorInfo.value.tags
          }
          
          // 处理专业领域
          fields.value = [
            '抑郁症', '焦虑症', '强迫症', '恐惧症',
            '人际关系', '婚恋情感', '家庭关系', '职场压力'
          ]
          
          // 处理教育背景
          education.value = [
            { year: '2015-2018', school: '北京大学', degree: '心理学博士' },
            { year: '2012-2015', school: '清华大学', degree: '心理学硕士' },
            { year: '2008-2012', school: '复旦大学', degree: '心理学学士' }
          ]
        }
      } catch (error) {
        console.error('获取咨询师信息失败:', error)
        uni.showToast({
          title: '获取咨询师信息失败',
          icon: 'none'
        })
      }
    }
    
    // 获取评价列表
    const fetchComments = async () => {
      try {
        const res = await request({
          url: `/counselor/${counselorId.value}/comments`,
          method: 'GET',
          data: {
            page: 1,
            per_page: 10
          }
        })
        
        if (res.code === 200 && res.success) {
          comments.value = res.data.list || []
          commentCount.value = res.data.total || 0
        }
      } catch (error) {
        console.error('获取评价列表失败:', error)
      }
    }
    
    // 获取排班信息
    const fetchSchedule = async (date) => {
      try {
        const res = await request({
          url: `/counselor/${counselorId.value}/schedule`,
          method: 'GET',
          data: {
            date: date
          }
        })
        
        if (res.code === 200 && res.success) {
          timeSlots.value = res.data || []
        }
      } catch (error) {
        console.error('获取排班信息失败:', error)
        timeSlots.value = []
      }
    }
    
    // 切换标签
    const switchTab = (tab) => {
      activeTab.value = tab
      
      if (tab === 'comments' && comments.value.length === 0) {
        fetchComments()
      } else if (tab === 'schedule' && weekDays.value.length === 0) {
        initCalendar()
      }
    }
    
    // 初始化日历
    const initCalendar = () => {
      const today = new Date()
      const weekStart = new Date(today)
      weekStart.setDate(today.getDate() - today.getDay())
      
      const days = []
      const weekNames = ['日', '一', '二', '三', '四', '五', '六']
      
      for (let i = 0; i < 7; i++) {
        const date = new Date(weekStart)
        date.setDate(weekStart.getDate() + i)
        
        const dateStr = formatDate(date)
        
        days.push({
          date: dateStr,
          day: date.getDate(),
          name: weekNames[i],
          isToday: formatDate(today) === dateStr
        })
      }
      
      weekDays.value = days
      selectedDay.value = formatDate(today)
      
      // 获取选中日期的排班
      fetchSchedule(selectedDay.value)
    }
    
    // 格式化日期
    const formatDate = (date) => {
      const year = date.getFullYear()
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const day = date.getDate().toString().padStart(2, '0')
      return `${year}-${month}-${day}`
    }
    
    // 上一周
    const prevWeek = () => {
      currentWeek.value--
      updateWeekDays()
    }
    
    // 下一周
    const nextWeek = () => {
      currentWeek.value++
      updateWeekDays()
    }
    
    // 更新周日期
    const updateWeekDays = () => {
      const today = new Date()
      const weekStart = new Date(today)
      weekStart.setDate(today.getDate() - today.getDay() + (currentWeek.value * 7))
      
      const days = []
      const weekNames = ['日', '一', '二', '三', '四', '五', '六']
      
      for (let i = 0; i < 7; i++) {
        const date = new Date(weekStart)
        date.setDate(weekStart.getDate() + i)
        
        const dateStr = formatDate(date)
        
        days.push({
          date: dateStr,
          day: date.getDate(),
          name: weekNames[i],
          isToday: formatDate(today) === dateStr
        })
      }
      
      weekDays.value = days
      selectedDay.value = days[0].date
      
      // 获取选中日期的排班
      fetchSchedule(selectedDay.value)
    }
    
    // 选择日期
    const selectDay = (date) => {
      selectedDay.value = date
      fetchSchedule(date)
    }
    
    // 选择时间段
    const selectTimeSlot = (slot) => {
      if (!slot.available) return
      
      selectedSlot.value = slot.id
    }
    
    // 当前周文本
    const currentWeekText = computed(() => {
      if (weekDays.value.length === 0) return ''
      
      const firstDay = weekDays.value[0].date
      const lastDay = weekDays.value[6].date
      
      return `${firstDay} 至 ${lastDay}`
    })
    
    // 预约处理
    const handleAppointment = () => {
      if (!checkLogin()) return
      
      if (activeTab.value !== 'schedule') {
        switchTab('schedule')
        uni.showToast({
          title: '请先选择预约时间',
          icon: 'none'
        })
        return
      }
      
      if (!selectedSlot.value) {
        uni.showToast({
          title: '请选择预约时间段',
          icon: 'none'
        })
        return
      }
      
      // 跳转到预约确认页
      uni.navigateTo({
        url: `/pages/appointment/confirm?counselor_id=${counselorId.value}&time_slot_id=${selectedSlot.value}`
      })
    }
    
    // 页面加载
    onLoad((options) => {
      if (options.id) {
        counselorId.value = options.id
        fetchCounselorInfo()
      } else {
        uni.showToast({
          title: '参数错误',
          icon: 'none'
        })
        
        setTimeout(() => {
          uni.navigateBack()
        }, 1500)
      }
    })
    
    return {
      counselorInfo,
      activeTab,
      tags,
      fields,
      education,
      comments,
      commentCount,
      weekDays,
      currentWeek,
      selectedDay,
      timeSlots,
      selectedSlot,
      currentWeekText,
      switchTab,
      prevWeek,
      nextWeek,
      selectDay,
      selectTimeSlot,
      handleAppointment
    }
  }
}
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 30rpx;
}

.counselor-header {
  background-color: #fff;
  padding: 40rpx 30rpx;
}

.counselor-basic {
  display: flex;
  margin-bottom: 30rpx;
}

.counselor-info {
  flex: 1;
  margin-left: 30rpx;
}

.counselor-name {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
  display: block;
}

.counselor-title {
  font-size: 28rpx;
  color: #666;
  background-color: #f5f7fa;
  padding: 4rpx 10rpx;
  border-radius: 4rpx;
  display: inline-block;
  margin-bottom: 10rpx;
}

.counselor-rating {
  display: flex;
  align-items: center;
  margin-bottom: 10rpx;
}

.rating-text {
  font-size: 28rpx;
  color: #faad14;
  margin: 0 10rpx;
}

.consultation-count {
  font-size: 24rpx;
  color: #999;
}

.counselor-tags {
  display: flex;
  flex-wrap: wrap;
}

.tag {
  font-size: 24rpx;
  color: #4A90E2;
  background-color: rgba(74, 144, 226, 0.1);
  padding: 4rpx 10rpx;
  border-radius: 4rpx;
  margin-right: 10rpx;
  margin-bottom: 10rpx;
}

.price-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1rpx solid #f0f0f0;
  padding-top: 30rpx;
}

.price {
  font-size: 40rpx;
  color: #f5222d;
  font-weight: bold;
}

.appointment-btn {
  background-color: #4A90E2;
  color: #fff;
  font-size: 32rpx;
  padding: 15rpx 40rpx;
  border-radius: 40rpx;
  border: none;
}

.tab-section {
  display: flex;
  background-color: #fff;
  margin-top: 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 30rpx 0;
  font-size: 28rpx;
  color: #666;
  position: relative;
}

.tab-item.active {
  color: #4A90E2;
  font-weight: bold;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60rpx;
  height: 4rpx;
  background-color: #4A90E2;
}

.content-section {
  background-color: #fff;
  min-height: 300rpx;
  padding: 30rpx;
}

.section-block {
  margin-bottom: 40rpx;
}

.block-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  position: relative;
  padding-left: 20rpx;
}

.block-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 6rpx;
  height: 30rpx;
  background-color: #4A90E2;
}

.block-content {
  padding: 0 10rpx;
}

.intro-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.8;
}

.field-item {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.field-text {
  font-size: 28rpx;
  color: #666;
  margin-left: 10rpx;
}

.education-item {
  display: flex;
  margin-bottom: 20rpx;
}

.edu-year {
  font-size: 28rpx;
  color: #999;
  width: 180rpx;
}

.edu-info {
  flex: 1;
}

.edu-school {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
  display: block;
}

.edu-degree {
  font-size: 24rpx;
  color: #666;
}

.comment-item {
  padding: 30rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  margin-bottom: 20rpx;
}

.comment-user {
  flex: 1;
  margin-left: 20rpx;
}

.comment-username {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
  display: block;
  margin-bottom: 10rpx;
}

.comment-rating {
  display: flex;
  align-items: center;
}

.comment-time {
  font-size: 24rpx;
  color: #999;
  margin-left: 20rpx;
}

.comment-body {
  margin-bottom: 20rpx;
}

.comment-text {
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
}

.comment-footer {
  background-color: #f5f7fa;
  padding: 20rpx;
  border-radius: 10rpx;
}

.reply-label {
  font-size: 24rpx;
  color: #999;
  margin-right: 10rpx;
}

.reply-text {
  font-size: 28rpx;
  color: #333;
}

.calendar-section {
  margin-bottom: 30rpx;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.calendar-title {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
}

.calendar-days {
  display: flex;
  justify-content: space-between;
}

.day-item {
  flex: 1;
  text-align: center;
  padding: 20rpx 0;
  border-radius: 10rpx;
}

.day-item.day-active {
  background-color: #4A90E2;
}

.day-name {
  font-size: 24rpx;
  color: #666;
  display: block;
  margin-bottom: 10rpx;
}

.day-item.day-active .day-name,
.day-item.day-active .day-date {
  color: #fff;
}

.day-date {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
}

.time-slots {
  margin-top: 30rpx;
}

.time-slot-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.time-slot-list {
  display: flex;
  flex-wrap: wrap;
}

.time-slot-item {
  width: calc(33.33% - 20rpx);
  margin: 10rpx;
  padding: 20rpx 0;
  text-align: center;
  border: 1rpx solid #ddd;
  border-radius: 10rpx;
  font-size: 28rpx;
  color: #333;
}

.slot-selected {
  border-color: #4A90E2;
  background-color: rgba(74, 144, 226, 0.1);
  color: #4A90E2;
}

.slot-disabled {
  border-color: #f0f0f0;
  background-color: #f5f7fa;
  color: #ccc;
}

.empty-content {
  padding: 60rpx 0;
  text-align: center;
}
</style> 