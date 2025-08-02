<template>
  <view class="time-slots-container">
    <!-- 页面标题 -->
    <view class="page-header">
      <text class="page-title">时间管理</text>
    </view>
    
    <!-- 日历控制 -->
    <view class="calendar-controls">
      <view class="calendar-header">
        <view class="calendar-nav prev" @click="changeWeek(-1)">
          <text class="nav-icon">《</text>
        </view>
        <view class="current-week">
          {{startWeekDate}} - {{endWeekDate}}
        </view>
        <view class="calendar-nav next" @click="changeWeek(1)">
          <text class="nav-icon">》</text>
        </view>
      </view>
      
      <view class="view-actions">
        <view class="action-button" @click="goToToday">
          <text class="action-text">今天</text>
        </view>
        <view class="action-button" @click="showBatchEdit = true">
          <text class="action-text">批量设置</text>
        </view>
      </view>
    </view>
    
    <!-- 周视图日历 -->
    <view class="week-calendar">
      <!-- 星期表头 -->
      <view class="week-header">
        <view class="day-header" v-for="(day, index) in weekDays" :key="index">
          <text class="weekday">{{day.weekday}}</text>
          <text class="date" :class="{'today': day.isToday}">{{day.date}}</text>
        </view>
      </view>
      
      <!-- 时间段网格 -->
      <scroll-view scroll-y class="time-grid-scroll">
        <view class="time-grid">
          <!-- 时间轴标记 -->
          <view class="time-axis">
            <view 
              class="time-marker" 
              v-for="hour in workHours" 
              :key="hour"
              :style="{top: (hour - startHour) * 100 + 'rpx'}"
            >
              <text class="time-text">{{formatHour(hour)}}</text>
            </view>
          </view>
          
          <!-- 每天的时间格子 -->
          <view class="day-column" v-for="(day, dayIndex) in weekDays" :key="dayIndex">
            <view class="hour-grid-container">
              <!-- 时间段背景 -->
              <view 
                class="hour-cell" 
                v-for="hour in workHours" 
                :key="hour"
                @click="toggleTimeSlot(dayIndex, hour)"
              ></view>
              
              <!-- 可预约时间段 -->
              <view 
                v-for="(slot, slotIndex) in getTimeSlots(day.date)" 
                :key="slotIndex"
                class="time-slot"
                :class="{
                  'available': slot.status === 'available',
                  'booked': slot.status === 'booked',
                  'unavailable': slot.status === 'unavailable'
                }"
                :style="{
                  top: calculateSlotPosition(slot.startHour),
                  height: calculateSlotHeight(slot.startHour, slot.endHour)
                }"
                @click.stop="editTimeSlot(slot)"
              >
                <view class="slot-time">{{formatTimeSlot(slot)}}</view>
                <view class="slot-status" v-if="slot.status === 'booked'">已预约</view>
              </view>
            </view>
          </view>
        </view>
      </scroll-view>
    </view>
    
    <!-- 批量设置弹窗 -->
    <view class="modal" v-if="showBatchEdit">
      <view class="modal-mask" @click="showBatchEdit = false"></view>
      <view class="modal-content">
        <view class="modal-header">
          <text class="modal-title">批量设置可预约时间</text>
          <text class="modal-close" @click="showBatchEdit = false">✕</text>
        </view>
        
        <view class="batch-edit-form">
          <view class="form-section">
            <text class="section-title">选择日期范围</text>
            <view class="date-range-picker">
              <view class="date-picker" @click="showStartDatePicker = true">
                <text class="date-label">开始日期：</text>
                <text class="date-value">{{batchSettings.startDate || '请选择'}}</text>
              </view>
              <view class="date-picker" @click="showEndDatePicker = true">
                <text class="date-label">结束日期：</text>
                <text class="date-value">{{batchSettings.endDate || '请选择'}}</text>
              </view>
            </view>
          </view>
          
          <view class="form-section">
            <text class="section-title">选择生效星期</text>
            <view class="weekday-selector">
              <view 
                v-for="(day, index) in ['周一', '周二', '周三', '周四', '周五', '周六', '周日']" 
                :key="index"
                class="weekday-item"
                :class="{'selected': batchSettings.weekdays.includes(index + 1)}"
                @click="toggleWeekday(index + 1)"
              >
                {{day}}
              </view>
            </view>
          </view>
          
          <view class="form-section">
            <text class="section-title">选择时间段</text>
            <view class="time-range-picker">
              <view class="time-picker" @click="showStartTimePicker = true">
                <text class="time-label">开始时间：</text>
                <text class="time-value">{{batchSettings.startTime || '请选择'}}</text>
              </view>
              <view class="time-picker" @click="showEndTimePicker = true">
                <text class="time-label">结束时间：</text>
                <text class="time-value">{{batchSettings.endTime || '请选择'}}</text>
              </view>
            </view>
          </view>
          
          <view class="form-section">
            <text class="section-title">选择重复方式</text>
            <view class="repeat-selector">
              <view 
                v-for="(type, index) in repeatTypes" 
                :key="index"
                class="repeat-item"
                :class="{'selected': batchSettings.repeatType === type.value}"
                @click="setBatchRepeatType(type.value)"
              >
                {{type.text}}
              </view>
            </view>
          </view>
          
          <view class="form-actions">
            <view class="action-button cancel" @click="showBatchEdit = false">
              取消
            </view>
            <view class="action-button confirm" @click="applyBatchSettings">
              应用设置
            </view>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 时间段编辑弹窗 -->
    <view class="modal" v-if="currentEditingSlot">
      <view class="modal-mask" @click="currentEditingSlot = null"></view>
      <view class="modal-content">
        <view class="modal-header">
          <text class="modal-title">编辑时间段</text>
          <text class="modal-close" @click="currentEditingSlot = null">✕</text>
        </view>
        
        <view class="slot-edit-form">
          <view class="slot-info">
            <text class="slot-date">{{formatDate(currentEditingSlot?.date)}}</text>
            <text class="slot-time">{{formatTimeSlot(currentEditingSlot)}}</text>
          </view>
          
          <view class="status-selector">
            <view 
              class="status-item"
              :class="{'selected': currentEditingSlot?.status === 'available'}"
              @click="updateSlotStatus('available')"
            >
              <text class="status-text">可预约</text>
            </view>
            <view 
              class="status-item"
              :class="{'selected': currentEditingSlot?.status === 'unavailable'}"
              @click="updateSlotStatus('unavailable')"
            >
              <text class="status-text">不可预约</text>
            </view>
          </view>
          
          <view class="form-actions">
            <view 
              class="action-button delete" 
              v-if="currentEditingSlot?.status !== 'booked'"
              @click="deleteTimeSlot"
            >
              删除
            </view>
            <view class="action-button cancel" @click="currentEditingSlot = null">
              取消
            </view>
            <view class="action-button confirm" @click="saveTimeSlot">
              保存
            </view>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 时间选择器 -->
    <!-- 这里应该引入uni-app的日期时间选择器组件 -->
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 工作时间设置
      startHour: 8, // 工作日开始时间（小时）
      endHour: 21, // 工作日结束时间（小时）
      workHours: [], // 工作小时数组
      
      // 日历相关
      currentWeekStart: null, // 当前周的开始日期
      weekDays: [], // 当前显示的一周七天
      timeSlots: [], // 所有时间段
      
      // 弹窗控制
      showBatchEdit: false,
      showStartDatePicker: false,
      showEndDatePicker: false,
      showStartTimePicker: false,
      showEndTimePicker: false,
      currentEditingSlot: null,
      
      // 批量设置表单
      batchSettings: {
        startDate: '',
        endDate: '',
        weekdays: [1, 2, 3, 4, 5], // 默认周一至周五
        startTime: '',
        endTime: '',
        repeatType: 'weekly'
      },
      
      // 重复类型选项
      repeatTypes: [
        { text: '每周', value: 'weekly' },
        { text: '每两周', value: 'biweekly' },
        { text: '每月', value: 'monthly' },
        { text: '单次', value: 'once' }
      ]
    }
  },
  computed: {
    startWeekDate() {
      if (!this.weekDays.length) return '';
      const date = this.weekDays[0].fullDate;
      return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
    },
    endWeekDate() {
      if (!this.weekDays.length) return '';
      const date = this.weekDays[6].fullDate;
      return `${date.getMonth() + 1}月${date.getDate()}日`;
    }
  },
  created() {
    this.initWorkHours();
    this.initCurrentWeek();
    this.fetchTimeSlots(); // 假设这是从API获取预约时间的方法
  },
  methods: {
    initWorkHours() {
      // 生成工作时间数组
      this.workHours = [];
      for (let i = this.startHour; i <= this.endHour; i++) {
        this.workHours.push(i);
      }
    },
    initCurrentWeek() {
      // 初始化为当前周
      const today = new Date();
      const currentDay = today.getDay(); // 0是周日，1是周一
      
      // 计算本周的周日
      const sundayOffset = currentDay === 0 ? 0 : -currentDay;
      const sunday = new Date(today);
      sunday.setDate(today.getDate() + sundayOffset);
      
      this.currentWeekStart = sunday;
      this.generateWeekDays();
    },
    generateWeekDays() {
      // 生成当前显示的一周七天
      const startDate = new Date(this.currentWeekStart);
      const today = new Date();
      today.setHours(0, 0, 0, 0); // 将今天的时间部分设为0
      
      this.weekDays = [];
      
      for (let i = 0; i < 7; i++) {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        
        // 检查是否是今天
        const isToday = date.getTime() === today.getTime();
        
        this.weekDays.push({
          weekday: ['日', '一', '二', '三', '四', '五', '六'][date.getDay()],
          date: `${date.getMonth() + 1}/${date.getDate()}`,
          fullDate: date,
          isToday: isToday
        });
      }
    },
    changeWeek(offset) {
      // 切换周
      const newStart = new Date(this.currentWeekStart);
      newStart.setDate(newStart.getDate() + offset * 7);
      this.currentWeekStart = newStart;
      this.generateWeekDays();
      this.fetchTimeSlots();
    },
    goToToday() {
      // 回到本周
      this.initCurrentWeek();
      this.fetchTimeSlots();
    },
    formatHour(hour) {
      // 格式化小时为时间字符串
      return `${hour}:00`;
    },
    formatTimeSlot(slot) {
      if (!slot) return '';
      // 格式化时间段
      const startHour = Math.floor(slot.startHour);
      const startMinute = (slot.startHour - startHour) * 60;
      const endHour = Math.floor(slot.endHour);
      const endMinute = (slot.endHour - endHour) * 60;
      
      return `${startHour.toString().padStart(2, '0')}:${startMinute.toString().padStart(2, '0')} - ${endHour.toString().padStart(2, '0')}:${endMinute.toString().padStart(2, '0')}`;
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 星期${'日一二三四五六'[date.getDay()]}`;
    },
    calculateSlotPosition(startHour) {
      // 计算时间段在网格中的位置
      return ((startHour - this.startHour) * 100) + 'rpx';
    },
    calculateSlotHeight(startHour, endHour) {
      // 计算时间段的高度
      return ((endHour - startHour) * 100) + 'rpx';
    },
    getTimeSlots(dateStr) {
      // 获取某一天的所有时间段
      const date = new Date(dateStr);
      const dateString = date.toISOString().split('T')[0]; // 转为YYYY-MM-DD格式
      
      return this.timeSlots.filter(slot => slot.date === dateString);
    },
    fetchTimeSlots() {
      // 模拟从API获取数据
      // 实际应该调用API
      setTimeout(() => {
        this.timeSlots = this.generateMockTimeSlots();
      }, 100);
    },
    generateMockTimeSlots() {
      // 生成模拟数据
      const slots = [];
      
      // 为每一天生成一些时间段
      this.weekDays.forEach(day => {
        const date = day.fullDate.toISOString().split('T')[0]; // 转为YYYY-MM-DD格式
        
        // 上午时间段
        slots.push({
          id: `slot-${date}-1`,
          date: date,
          startHour: 9,
          endHour: 10.5,
          status: 'available'
        });
        
        // 下午时间段
        slots.push({
          id: `slot-${date}-2`,
          date: date,
          startHour: 14,
          endHour: 15.5,
          status: 'available'
        });
        
        // 一些已预约的时间段
        if (day.weekday === '二' || day.weekday === '四') {
          slots.push({
            id: `slot-${date}-3`,
            date: date,
            startHour: 16,
            endHour: 17.5,
            status: 'booked',
            clientName: '张先生'
          });
        }
        
        // 不可用时间段
        if (day.weekday === '三') {
          slots.push({
            id: `slot-${date}-4`,
            date: date,
            startHour: 11,
            endHour: 12.5,
            status: 'unavailable'
          });
        }
      });
      
      return slots;
    },
    toggleTimeSlot(dayIndex, hour) {
      // 点击空白区域创建新的时间段
      const day = this.weekDays[dayIndex];
      const date = day.fullDate.toISOString().split('T')[0];
      
      // 查看是否有重叠的时间段
      const hasOverlap = this.timeSlots.some(slot => {
        return slot.date === date && 
               ((hour >= slot.startHour && hour < slot.endHour) || 
                (hour + 1 > slot.startHour && hour + 1 <= slot.endHour));
      });
      
      if (hasOverlap) {
        uni.showToast({
          title: '时间段重叠，请先删除已有时间段',
          icon: 'none'
        });
        return;
      }
      
      // 创建新的时间段
      this.currentEditingSlot = {
        id: `new-slot-${date}-${hour}`,
        date: date,
        startHour: hour,
        endHour: hour + 1.5,
        status: 'available'
      };
    },
    editTimeSlot(slot) {
      // 编辑已有时间段
      this.currentEditingSlot = { ...slot };
    },
    updateSlotStatus(status) {
      // 更新当前编辑时间段的状态
      if (this.currentEditingSlot) {
        this.currentEditingSlot.status = status;
      }
    },
    saveTimeSlot() {
      // 保存时间段
      const slot = this.currentEditingSlot;
      
      // 检查是否是新时间段
      const existingIndex = this.timeSlots.findIndex(s => s.id === slot.id);
      
      if (existingIndex >= 0) {
        // 更新现有时间段
        this.timeSlots.splice(existingIndex, 1, slot);
      } else {
        // 添加新时间段
        this.timeSlots.push(slot);
      }
      
      // 关闭编辑弹窗
      this.currentEditingSlot = null;
      
      // 显示成功提示
      uni.showToast({
        title: '时间段已保存',
        icon: 'success'
      });
    },
    deleteTimeSlot() {
      // 删除时间段
      if (!this.currentEditingSlot) return;
      
      const index = this.timeSlots.findIndex(s => s.id === this.currentEditingSlot.id);
      
      if (index >= 0) {
        this.timeSlots.splice(index, 1);
      }
      
      // 关闭编辑弹窗
      this.currentEditingSlot = null;
      
      // 显示成功提示
      uni.showToast({
        title: '时间段已删除',
        icon: 'success'
      });
    },
    toggleWeekday(day) {
      // 切换批量设置中的星期
      const index = this.batchSettings.weekdays.indexOf(day);
      
      if (index >= 0) {
        // 已选中，则取消
        this.batchSettings.weekdays.splice(index, 1);
      } else {
        // 未选中，则添加
        this.batchSettings.weekdays.push(day);
        // 确保顺序
        this.batchSettings.weekdays.sort();
      }
    },
    setBatchRepeatType(type) {
      // 设置重复类型
      this.batchSettings.repeatType = type;
    },
    applyBatchSettings() {
      // 应用批量设置
      // 这里应该调用API保存批量设置
      
      // 显示成功提示
      uni.showToast({
        title: '设置已应用',
        icon: 'success'
      });
      
      // 关闭弹窗
      this.showBatchEdit = false;
      
      // 重新获取时间段
      this.fetchTimeSlots();
    }
  }
}
</script>

<style lang="scss">
@import "@/static/theme.scss";
.time-slots-container {
  padding: 30rpx;
  background-color: var(--mg-bg-secondary);
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30rpx;
}

.page-title {
  font-size: 40rpx;
  font-weight: bold;
  color: var(--mg-text-primary);
}

.calendar-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.calendar-header {
  display: flex;
  align-items: center;
}

.calendar-nav {
  width: 60rpx;
  height: 60rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  background-color: var(--mg-gray-100);
}

.current-week {
  font-size: 32rpx;
  font-weight: bold;
  color: var(--mg-text-primary);
  margin: 0 20rpx;
}

.view-actions {
  display: flex;
}

.action-button {
  padding: 12rpx 30rpx;
  font-size: 28rpx;
  color: var(--mg-primary);
  background-color: var(--mg-primary-light);
  border-radius: 30rpx;
  margin-left: 20rpx;
}

.week-calendar {
  background-color: var(--mg-bg-primary);
  border-radius: 12rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 10rpx var(--mg-shadow-color);
}

.week-header {
  display: flex;
  border-bottom: 2rpx solid var(--mg-border-light);
}

.day-header {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx 0;
  border-right: 2rpx solid var(--mg-border-light);
  
  &:last-child {
    border-right: none;
  }
}

.weekday {
  font-size: 28rpx;
  color: var(--mg-text-secondary);
  margin-bottom: 10rpx;
}

.date {
  font-size: 32rpx;
  color: var(--mg-text-primary);
  
  &.today {
    color: var(--mg-primary);
    font-weight: bold;
  }
}

.time-grid-scroll {
  height: 800rpx;
}

.time-grid {
  display: flex;
  position: relative;
  min-height: 100%;
}

.time-axis {
  width: 100rpx;
  position: relative;
  border-right: 2rpx solid var(--mg-border-light);
}

.time-marker {
  position: absolute;
  width: 100%;
  height: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: translateY(-20rpx);
}

.time-text {
  font-size: 24rpx;
  color: var(--mg-text-tertiary);
}

.day-column {
  flex: 1;
  position: relative;
  border-right: 2rpx solid var(--mg-border-light);
  
  &:last-child {
    border-right: none;
  }
}

.hour-grid-container {
  position: relative;
  height: 100%;
}

.hour-cell {
  height: 100rpx;
  border-bottom: 2rpx solid var(--mg-border-light);
  
  &:last-child {
    border-bottom: none;
  }
}

.time-slot {
  position: absolute;
  left: 10rpx;
  right: 10rpx;
  border-radius: 8rpx;
  padding: 10rpx;
  font-size: 24rpx;
  overflow: hidden;
  
  &.available {
    background-color: var(--mg-primary-light);
    border: 2rpx solid var(--mg-primary);
    color: var(--mg-primary);
  }
  
  &.booked {
    background-color: var(--mg-success-light);
    border: 2rpx solid var(--mg-success);
    color: var(--mg-success);
  }
  
  &.unavailable {
    background-color: var(--mg-gray-200);
    border: 2rpx solid var(--mg-gray-400);
    color: var(--mg-gray-600);
  }
}

.slot-time {
  font-size: 24rpx;
  font-weight: bold;
  margin-bottom: 6rpx;
}

.slot-status {
  font-size: 22rpx;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 100;
}

.modal-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--mg-bg-primary);
  border-radius: 24rpx 24rpx 0 0;
  padding: 30rpx;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
}

.modal-title {
  font-size: 32rpx;
  font-weight: bold;
  color: var(--mg-text-primary);
}

.modal-close {
  font-size: 32rpx;
  color: var(--mg-text-tertiary);
}

.batch-edit-form, .slot-edit-form {
  padding-bottom: 30rpx;
}

.form-section {
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 28rpx;
  color: var(--mg-text-secondary);
  margin-bottom: 20rpx;
}

.date-range-picker, .time-range-picker {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.date-picker, .time-picker {
  display: flex;
  align-items: center;
  padding: 20rpx;
  background-color: var(--mg-gray-100);
  border-radius: 8rpx;
}

.date-label, .time-label {
  font-size: 28rpx;
  color: var(--mg-text-secondary);
  width: 180rpx;
}

.date-value, .time-value {
  font-size: 28rpx;
  color: var(--mg-text-primary);
  flex: 1;
}

.weekday-selector, .repeat-selector, .status-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.weekday-item, .repeat-item, .status-item {
  padding: 15rpx 30rpx;
  font-size: 28rpx;
  color: var(--mg-text-secondary);
  background-color: var(--mg-gray-100);
  border-radius: 8rpx;
  
  &.selected {
    color: var(--mg-primary);
    background-color: var(--mg-primary-light);
    font-weight: bold;
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 40rpx;
  gap: 20rpx;
}

.action-button {
  padding: 20rpx 40rpx;
  font-size: 28rpx;
  border-radius: 8rpx;
  
  &.cancel {
    color: var(--mg-text-secondary);
    background-color: var(--mg-gray-200);
  }
  
  &.confirm {
    color: white;
    background-color: var(--mg-primary);
  }
  
  &.delete {
    color: white;
    background-color: var(--mg-error);
  }
}

.slot-info {
  background-color: var(--mg-gray-100);
  padding: 20rpx;
  border-radius: 8rpx;
  margin-bottom: 30rpx;
}

.slot-date {
  font-size: 28rpx;
  color: var(--mg-text-secondary);
  margin-bottom: 10rpx;
  display: block;
}

.slot-time {
  font-size: 32rpx;
  color: var(--mg-text-primary);
  font-weight: bold;
  display: block;
}
</style> 