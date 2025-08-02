<template>
  <view class="appointments-container">
    <!-- 页面标题 -->
    <view class="page-header">
      <text class="page-title">预约管理</text>
    </view>
    
    <!-- 状态筛选选项卡 -->
    <view class="status-tabs">
      <view 
        v-for="(tab, index) in statusTabs" 
        :key="index"
        class="tab-item"
        :class="{ active: currentTab === index }"
        @click="switchTab(index)"
      >
        <text class="tab-text">{{tab.text}}</text>
        <text class="tab-count" v-if="tab.count > 0">{{tab.count}}</text>
      </view>
    </view>
    
    <!-- 日历视图切换 -->
    <view class="view-toggle">
      <view 
        class="toggle-item" 
        :class="{ active: viewMode === 'list' }"
        @click="switchView('list')"
      >
        <text class="toggle-icon list"></text>
        <text class="toggle-text">列表视图</text>
      </view>
      <view 
        class="toggle-item" 
        :class="{ active: viewMode === 'calendar' }"
        @click="switchView('calendar')"
      >
        <text class="toggle-icon calendar"></text>
        <text class="toggle-text">日历视图</text>
      </view>
    </view>
    
    <!-- 列表视图 -->
    <view class="list-view" v-if="viewMode === 'list' && currentAppointments.length > 0">
      <view 
        v-for="(appointment, index) in currentAppointments" 
        :key="index"
        class="appointment-card"
        :class="appointment.status"
      >
        <view class="appointment-header">
          <view class="appointment-time">
            <text class="day">{{formatDate(appointment.date).day}}</text>
            <text class="date">{{formatDate(appointment.date).date}}</text>
            <text class="time">{{appointment.timeSlot}}</text>
          </view>
          <view class="appointment-status-tag" :class="appointment.status">
            {{getStatusText(appointment.status)}}
          </view>
        </view>
        
        <view class="appointment-body">
          <view class="client-info">
            <view class="client-name">{{appointment.clientName}}</view>
            <view class="service-type">{{appointment.serviceType}}</view>
          </view>
          
          <view class="appointment-note" v-if="appointment.note">
            <text class="note-label">备注：</text>
            <text class="note-content">{{appointment.note}}</text>
          </view>
        </view>
        
        <view class="appointment-actions">
          <view class="action-button" v-if="appointment.status === 'pending'" @click="confirmAppointment(appointment.id)">
            确认
          </view>
          <view class="action-button" v-if="appointment.status === 'pending'" @click="rejectAppointment(appointment.id)">
            婉拒
          </view>
          <view class="action-button" v-if="appointment.status === 'confirmed'" @click="completeAppointment(appointment.id)">
            完成
          </view>
          <view class="action-button" v-if="['pending', 'confirmed'].includes(appointment.status)" @click="rescheduleAppointment(appointment.id)">
            改期
          </view>
          <view class="action-button view" @click="viewAppointmentDetail(appointment.id)">
            详情
          </view>
        </view>
      </view>
    </view>
    
    <!-- 日历视图 -->
    <view class="calendar-view" v-if="viewMode === 'calendar'">
      <view class="calendar-header">
        <view class="calendar-nav prev" @click="changeMonth(-1)">
          <text class="nav-icon">《</text>
        </view>
        <view class="current-month">{{currentYear}}年{{currentMonth}}月</view>
        <view class="calendar-nav next" @click="changeMonth(1)">
          <text class="nav-icon">》</text>
        </view>
      </view>
      
      <view class="weekdays">
        <view class="weekday" v-for="(day, index) in weekDays" :key="index">
          {{day}}
        </view>
      </view>
      
      <view class="calendar-days">
        <view 
          v-for="(day, index) in calendarDays" 
          :key="index"
          class="calendar-day"
          :class="{
            'other-month': !day.isCurrentMonth,
            'has-appointments': day.appointments.length > 0,
            'today': day.isToday
          }"
          @click="selectDay(day)"
        >
          <text class="day-number">{{day.day}}</text>
          <view class="day-indicator" v-if="day.appointments.length > 0">
            <text class="indicator-text">{{day.appointments.length}}</text>
          </view>
        </view>
      </view>
      
      <view class="day-appointments" v-if="selectedDay && selectedDay.appointments.length > 0">
        <view class="selected-day-header">
          <text class="selected-day-text">{{formatSelectedDay(selectedDay)}}</text>
          <text class="appointment-count">{{selectedDay.appointments.length}}个预约</text>
        </view>
        
        <view 
          v-for="(appointment, index) in selectedDay.appointments" 
          :key="index"
          class="day-appointment-item"
          :class="appointment.status"
          @click="viewAppointmentDetail(appointment.id)"
        >
          <text class="appointment-time">{{appointment.timeSlot}}</text>
          <text class="appointment-client">{{appointment.clientName}}</text>
          <text class="appointment-status" :class="appointment.status">
            {{getStatusText(appointment.status)}}
          </text>
        </view>
      </view>
      
      <view class="empty-day-message" v-else-if="selectedDay">
        <text>{{formatSelectedDay(selectedDay)}} 没有预约</text>
      </view>
    </view>
    
    <!-- 空状态提示 -->
    <view class="empty-state" v-if="viewMode === 'list' && currentAppointments.length === 0">
      <image class="empty-icon" src="/static/images/empty-appointments.png" mode="aspectFit"></image>
      <text class="empty-text">暂无{{getStatusText(statusTabs[currentTab].status)}}的预约</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 状态选项卡
      statusTabs: [
        { text: '全部', status: 'all', count: 12 },
        { text: '待确认', status: 'pending', count: 3 },
        { text: '已确认', status: 'confirmed', count: 4 },
        { text: '已完成', status: 'completed', count: 5 },
        { text: '已取消', status: 'canceled', count: 0 }
      ],
      currentTab: 0,
      viewMode: 'list',
      
      // 日历数据
      currentYear: new Date().getFullYear(),
      currentMonth: new Date().getMonth() + 1,
      weekDays: ['日', '一', '二', '三', '四', '五', '六'],
      calendarDays: [],
      selectedDay: null,
      
      // 预约数据
      allAppointments: [
        {
          id: 'a001',
          date: '2023-09-15',
          timeSlot: '09:00-10:00',
          clientName: '张女士',
          serviceType: '个人咨询',
          status: 'pending',
          note: '第一次咨询，有些紧张'
        },
        {
          id: 'a002',
          date: '2023-09-15',
          timeSlot: '11:00-12:00',
          clientName: '李先生',
          serviceType: '焦虑管理',
          status: 'confirmed',
          note: ''
        },
        {
          id: 'a003',
          date: '2023-09-16',
          timeSlot: '14:00-15:00',
          clientName: '王先生',
          serviceType: '抑郁症治疗',
          status: 'completed',
          note: '继续上次的治疗方案'
        },
        {
          id: 'a004',
          date: '2023-09-18',
          timeSlot: '16:00-17:00',
          clientName: '赵女士',
          serviceType: '人际关系',
          status: 'canceled',
          note: ''
        },
        {
          id: 'a005',
          date: '2023-09-20',
          timeSlot: '10:00-11:00',
          clientName: '陈先生',
          serviceType: '职场压力',
          status: 'pending',
          note: '希望找到缓解工作压力的方法'
        }
      ]
    }
  },
  computed: {
    currentAppointments() {
      const status = this.statusTabs[this.currentTab].status;
      if (status === 'all') {
        return this.allAppointments;
      } else {
        return this.allAppointments.filter(app => app.status === status);
      }
    }
  },
  created() {
    this.initCalendar();
  },
  methods: {
    switchTab(index) {
      this.currentTab = index;
    },
    switchView(mode) {
      this.viewMode = mode;
      if (mode === 'calendar') {
        this.initCalendar();
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
      
      return {
        day: weekDays[date.getDay()],
        date: `${date.getMonth() + 1}月${date.getDate()}日`,
        time: `${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
      };
    },
    getStatusText(status) {
      const statusMap = {
        all: '所有',
        pending: '待确认',
        confirmed: '已确认',
        completed: '已完成',
        canceled: '已取消'
      };
      return statusMap[status] || status;
    },
    confirmAppointment(id) {
      // 调用确认预约API
      uni.showToast({
        title: '已确认预约',
        icon: 'success'
      });
    },
    rejectAppointment(id) {
      // 调用拒绝预约API
      uni.showModal({
        title: '婉拒预约',
        content: '确定要婉拒此预约吗？',
        success: (res) => {
          if (res.confirm) {
            uni.showToast({
              title: '已婉拒预约',
              icon: 'success'
            });
          }
        }
      });
    },
    completeAppointment(id) {
      // 调用完成预约API
      uni.showToast({
        title: '预约已完成',
        icon: 'success'
      });
    },
    rescheduleAppointment(id) {
      // 导航到改期页面
      uni.navigateTo({
        url: `/pages/counselor/appointments/reschedule?id=${id}`
      });
    },
    viewAppointmentDetail(id) {
      // 导航到预约详情页面
      uni.navigateTo({
        url: `/pages/counselor/appointments/detail?id=${id}`
      });
    },
    initCalendar() {
      const today = new Date();
      const year = this.currentYear;
      const month = this.currentMonth - 1; // JavaScript月份从0开始
      
      // 获取月份的第一天和最后一天
      const firstDay = new Date(year, month, 1);
      const lastDay = new Date(year, month + 1, 0);
      
      // 当月天数
      const daysInMonth = lastDay.getDate();
      
      // 第一天是星期几（0是星期日）
      const firstDayOfWeek = firstDay.getDay();
      
      // 日历中可能显示上个月的最后几天
      const daysFromPrevMonth = firstDayOfWeek;
      
      // 获取上个月的最后几天
      const prevMonth = new Date(year, month, 0);
      const prevMonthDays = prevMonth.getDate();
      
      // 生成日历数组
      const calendarDays = [];
      
      // 添加上个月的天数
      for (let i = prevMonthDays - daysFromPrevMonth + 1; i <= prevMonthDays; i++) {
        const dayDate = new Date(year, month - 1, i);
        calendarDays.push({
          day: i,
          date: dayDate,
          isCurrentMonth: false,
          isToday: false,
          appointments: this.getAppointmentsForDate(dayDate)
        });
      }
      
      // 添加当月的天数
      for (let i = 1; i <= daysInMonth; i++) {
        const dayDate = new Date(year, month, i);
        const isToday = 
          dayDate.getDate() === today.getDate() && 
          dayDate.getMonth() === today.getMonth() && 
          dayDate.getFullYear() === today.getFullYear();
        
        calendarDays.push({
          day: i,
          date: dayDate,
          isCurrentMonth: true,
          isToday: isToday,
          appointments: this.getAppointmentsForDate(dayDate)
        });
        
        // 如果是今天，默认选中
        if (isToday) {
          this.selectedDay = calendarDays[calendarDays.length - 1];
        }
      }
      
      // 添加下个月的开始几天，使日历填满6行
      const totalDaysNeeded = 42; // 6行 x 7天
      const nextMonthDays = totalDaysNeeded - calendarDays.length;
      
      for (let i = 1; i <= nextMonthDays; i++) {
        const dayDate = new Date(year, month + 1, i);
        calendarDays.push({
          day: i,
          date: dayDate,
          isCurrentMonth: false,
          isToday: false,
          appointments: this.getAppointmentsForDate(dayDate)
        });
      }
      
      this.calendarDays = calendarDays;
    },
    getAppointmentsForDate(date) {
      // 根据日期筛选预约
      const dateString = date.toISOString().split('T')[0]; // 转为YYYY-MM-DD格式
      return this.allAppointments.filter(app => app.date === dateString);
    },
    selectDay(day) {
      this.selectedDay = day;
    },
    formatSelectedDay(day) {
      const date = day.date;
      const month = date.getMonth() + 1;
      const dayNum = date.getDate();
      const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
      const weekDay = weekDays[date.getDay()];
      
      return `${month}月${dayNum}日 ${weekDay}`;
    },
    changeMonth(offset) {
      // 切换月份
      let year = this.currentYear;
      let month = this.currentMonth + offset;
      
      if (month > 12) {
        month = 1;
        year++;
      } else if (month < 1) {
        month = 12;
        year--;
      }
      
      this.currentYear = year;
      this.currentMonth = month;
      this.initCalendar();
    }
  }
}
</script>

<style lang="scss">
@import "@/static/theme.scss";
.appointments-container {
  padding: 30rpx;
  background-color: var(--mg-bg-secondary);
  background-image: linear-gradient(to bottom, var(--mg-bg-secondary) 0%, var(--mg-white) 100%);
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30rpx;
  position: relative;
  padding-left: 20rpx;
}

.page-title {
  font-size: 40rpx;
  font-weight: bold;
  color: var(--mg-primary);
  position: relative;
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
  
  &::before {
    content: '';
    position: absolute;
    left: -20rpx;
    top: 50%;
    transform: translateY(-50%);
    width: 8rpx;
    height: 32rpx;
    background: var(--mg-gradient-gold);
    border-radius: 4rpx;
    box-shadow: 0 2px 4px rgba(226, 170, 89, 0.3);
  }
}

.status-tabs {
  display: flex;
  background: white;
  border-radius: 12rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 16rpx var(--mg-shadow-color-strong);
  overflow: hidden;
  position: relative;
  border: 1px solid var(--mg-border-medium);
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(to right, transparent, var(--mg-primary), transparent);
  }
}

.tab-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24rpx 0;
  position: relative;
  transition: all 0.3s ease;
  color: var(--mg-text-secondary);
  
  &.active {
    color: var(--mg-primary);
    font-weight: bold;
    background-color: rgba(226, 170, 89, 0.15);
    
    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 25%;
      width: 50%;
      height: 4rpx;
      background: var(--mg-primary);
      border-radius: 4rpx;
      animation: tabIndicator 0.3s ease;
    }
  }
  
  &:hover:not(.active) {
    background-color: rgba(226, 170, 89, 0.08);
    color: var(--mg-primary-dark);
  }
}

@keyframes tabIndicator {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

.tab-text {
  font-size: 28rpx;
}

.tab-count {
  font-size: 20rpx;
  background-color: var(--mg-accent);
  color: var(--mg-white);
  border-radius: 20rpx;
  padding: 2rpx 10rpx;
  margin-left: 8rpx;
  line-height: 1;
  transform: scale(0.9);
  box-shadow: 0 2px 4px rgba(232, 76, 76, 0.2);
}

.view-toggle {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20rpx;
}

.toggle-item {
  display: flex;
  align-items: center;
  padding: 12rpx 24rpx;
  font-size: 24rpx;
  color: var(--mg-text-secondary);
  background-color: var(--mg-white);
  border-radius: 30rpx;
  margin-left: 10rpx;
  box-shadow: 0 2rpx 8rpx var(--mg-shadow-color);
  transition: all 0.2s ease;
  border: 1px solid var(--mg-border-medium);
  
  &.active {
    background: rgba(226, 170, 89, 0.2);
    color: var(--mg-primary);
    box-shadow: 0 2rpx 12rpx rgba(226, 170, 89, 0.3);
    border-color: var(--mg-primary);
  }
  
  &:hover:not(.active) {
    transform: translateY(-2rpx);
    box-shadow: 0 4rpx 12rpx var(--mg-shadow-color-strong);
  }
}

.toggle-icon {
  margin-right: 6rpx;
  font-family: 'uniicons';
  
  &.list::before {
    content: '\e682';
  }
  
  &.calendar::before {
    content: '\e6a0';
  }
}

.appointment-card {
  background: linear-gradient(to bottom, var(--mg-white) 0%, var(--mg-gray-100) 100%);
  border-radius: 12rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 16rpx var(--mg-shadow-color-strong);
  overflow: hidden;
  transition: all 0.2s ease;
  position: relative;
  border: 1px solid var(--mg-border-medium);
  
  &:hover {
    transform: translateY(-2rpx);
    box-shadow: 0 8rpx 24rpx var(--mg-shadow-color-strong);
    border-color: var(--mg-primary);
  }
  
  &.pending {
    border-left: 8rpx solid var(--mg-warning);
  }
  
  &.confirmed {
    border-left: 8rpx solid var(--mg-primary);
  }
  
  &.completed {
    border-left: 8rpx solid var(--mg-success);
  }
  
  &.canceled {
    border-left: 8rpx solid var(--mg-gray-600);
    opacity: 0.8;
  }
  
  &::after {
    content: '';
    position: absolute;
    right: 0;
    bottom: 0;
    width: 120rpx;
    height: 120rpx;
    background-image: radial-gradient(circle at bottom right, rgba(226, 170, 89, 0.15) 0%, transparent 70%);
    z-index: 0;
    pointer-events: none;
  }
}

.appointment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 30rpx;
  border-bottom: 1px solid var(--mg-border-medium);
  position: relative;
  background: linear-gradient(to right, rgba(226, 170, 89, 0.1), rgba(226, 170, 89, 0.05), rgba(226, 170, 89, 0.1));
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 20%;
    width: 60%;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--mg-primary-light), transparent);
  }
}

.appointment-time {
  display: flex;
  align-items: center;
  white-space: nowrap;
  flex-wrap: nowrap;
}

.day {
  font-size: 28rpx;
  color: var(--mg-primary-dark);
  margin-right: 10rpx;
  font-weight: 500;
  white-space: nowrap;
}

.date {
  font-size: 28rpx;
  color: var(--mg-text-primary);
  margin-right: 10rpx;
  font-weight: 500;
  white-space: nowrap;
}

.time {
  font-size: 28rpx;
  color: var(--mg-primary-dark);
  font-weight: bold;
  position: relative;
  white-space: nowrap;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -4rpx;
    left: 0;
    width: 100%;
    height: 2rpx;
    background: var(--mg-primary);
    border-radius: 1rpx;
  }
}

.appointment-status-tag {
  font-size: 24rpx;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  transition: all 0.2s ease;
  font-weight: 500;
  
  &.pending {
    background-color: rgba(255, 152, 0, 0.15);
    color: var(--mg-warning);
    border: 1px solid var(--mg-warning);
  }
  
  &.confirmed {
    background-color: rgba(226, 170, 89, 0.15);
    color: var(--mg-primary-dark);
    border: 1px solid var(--mg-primary);
  }
  
  &.completed {
    background-color: rgba(76, 175, 80, 0.15);
    color: var(--mg-success);
    border: 1px solid var(--mg-success);
  }
  
  &.canceled {
    background-color: rgba(136, 136, 136, 0.15);
    color: var(--mg-gray-700);
    border: 1px solid var(--mg-gray-600);
  }
}

.appointment-body {
  padding: 24rpx 30rpx;
  position: relative;
  z-index: 1;
  background-color: var(--mg-white);
}

.client-info {
  margin-bottom: 16rpx;
}

.client-name {
  font-size: 32rpx;
  color: var(--mg-primary-dark);
  font-weight: bold;
  margin-bottom: 8rpx;
}

.service-type {
  font-size: 28rpx;
  color: var(--mg-accent-dark);
  position: relative;
  display: inline-block;
  font-weight: 500;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -4rpx;
    left: 0;
    width: 40rpx;
    height: 2rpx;
    background-color: var(--mg-accent);
  }
}

.appointment-note {
  font-size: 26rpx;
  color: var(--mg-text-secondary);
  background-color: rgba(247, 247, 247, 0.8);
  padding: 20rpx;
  border-radius: 8rpx;
  margin-top: 20rpx;
  border-left: 4rpx solid var(--mg-primary);
}

.note-label {
  color: var(--mg-primary-dark);
  font-weight: 500;
}

.note-content {
  color: var(--mg-text-secondary);
}

.appointment-actions {
  display: flex;
  padding: 20rpx 30rpx;
  border-top: 1px solid var(--mg-border-light);
  position: relative;
  background: linear-gradient(to right, rgba(226, 170, 89, 0.05), transparent, rgba(226, 170, 89, 0.05));
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 20%;
    width: 60%;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--mg-border-medium), transparent);
  }
}

.action-button {
  padding: 12rpx 30rpx;
  font-size: 28rpx;
  color: var(--mg-white);
  background: var(--mg-gradient-gold);
  border-radius: 30rpx;
  margin-right: 20rpx;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(226, 170, 89, 0.3);
  
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.2);
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  &:hover::after {
    transform: translateX(0);
  }
  
  &:hover {
    transform: translateY(-2rpx);
    box-shadow: 0 4px 8px rgba(226, 170, 89, 0.4);
  }
  
  &.view {
    background: linear-gradient(to right, var(--mg-gray-300), var(--mg-gray-400));
    color: var(--mg-white);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    
    &:hover {
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
  }
}

.calendar-view {
  background: linear-gradient(to bottom, var(--mg-white) 0%, var(--mg-gray-100) 100%);
  border-radius: 12rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 16rpx var(--mg-shadow-color-strong);
  position: relative;
  overflow: hidden;
  border: 1px solid var(--mg-border-medium);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
  position: relative;
  z-index: 1;
}

.calendar-nav {
  width: 70rpx;
  height: 70rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  background-color: var(--mg-gray-200);
  transition: all 0.2s ease;
  border: 1px solid var(--mg-border-medium);
  color: var(--mg-text-secondary);
  
  &:hover {
    background-color: rgba(226, 170, 89, 0.15);
    color: var(--mg-primary);
    transform: scale(1.05);
    border-color: var(--mg-primary);
  }
}

.current-month {
  font-size: 36rpx;
  font-weight: bold;
  color: var(--mg-primary-dark);
  position: relative;
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
  
  &::after {
    content: '';
    position: absolute;
    bottom: -8rpx;
    left: 20%;
    width: 60%;
    height: 3rpx;
    background: var(--mg-primary);
    border-radius: 2rpx;
    box-shadow: 0 1px 2px rgba(226, 170, 89, 0.3);
  }
}

.weekdays {
  display: flex;
  border-bottom: 1px solid var(--mg-border-light);
  padding-bottom: 16rpx;
  margin-bottom: 16rpx;
  position: relative;
  z-index: 1;
}

.weekday {
  flex: 1;
  text-align: center;
  font-size: 28rpx;
  color: var(--mg-primary-dark);
  font-weight: bold;
}

.calendar-days {
  display: flex;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.calendar-day {
  width: 14.28%;
  height: 80rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  margin-bottom: 10rpx;
  transition: all 0.2s ease;
  
  &.other-month {
    opacity: 0.4;
  }
  
  &.has-appointments {
    font-weight: bold;
    
    &::after {
      content: '';
      position: absolute;
      bottom: 6rpx;
      left: 35%;
      width: 30%;
      height: 3rpx;
      background: var(--mg-gradient-gold);
      border-radius: 2rpx;
    }
  }
  
  &.today {
    background-color: rgba(226, 170, 89, 0.2);
    border-radius: 8rpx;
    box-shadow: inset 0 0 0 1px var(--mg-primary);
    
    .day-number {
      color: var(--mg-primary-dark);
      font-weight: bold;
    }
  }
  
  &:hover:not(.other-month) {
    background-color: rgba(226, 170, 89, 0.1);
    border-radius: 8rpx;
    transform: translateY(-2rpx);
  }
}

.day-number {
  font-size: 28rpx;
  color: var(--mg-text-primary);
  
  .today & {
    color: var(--mg-primary-dark);
    font-weight: bold;
  }
  
  .has-appointments & {
    color: var(--mg-accent-dark);
  }
}

.day-indicator {
  position: absolute;
  bottom: 5rpx;
  width: 30rpx;
  height: 30rpx;
  border-radius: 50%;
  background: var(--mg-primary);
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2rpx 8rpx rgba(226, 170, 89, 0.5);
}

.indicator-text {
  font-size: 20rpx;
  color: var(--mg-white);
}

.day-appointments {
  margin-top: 30rpx;
  border-top: 1px solid var(--mg-border-light);
  padding-top: 20rpx;
  position: relative;
  z-index: 1;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 20%;
    width: 60%;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--mg-border-medium), transparent);
  }
}

.selected-day-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
  padding-bottom: 10rpx;
  border-bottom: 1px dashed var(--mg-border-light);
}

.selected-day-text {
  font-size: 32rpx;
  font-weight: bold;
  color: var(--mg-primary-dark);
  position: relative;
  padding-left: 16rpx;
  text-shadow: 0 1px 1px rgba(0,0,0,0.05);
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 6rpx;
    height: 24rpx;
    background: var(--mg-primary);
    border-radius: 3rpx;
    box-shadow: 0 1px 3px rgba(226, 170, 89, 0.3);
  }
}

.appointment-count {
  font-size: 28rpx;
  color: var(--mg-white);
  background: var(--mg-primary);
  border-radius: 30rpx;
  padding: 4rpx 16rpx;
  box-shadow: 0 2px 4px rgba(226, 170, 89, 0.3);
  font-weight: bold;
}

.day-appointment-item {
  display: flex;
  align-items: center;
  padding: 20rpx;
  border-bottom: 1px solid var(--mg-border-light);
  transition: all 0.2s ease;
  position: relative;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    background-color: rgba(226, 170, 89, 0.08);
    border-radius: 8rpx;
  }
  
  &.pending {
    border-left: 4rpx solid var(--mg-warning);
  }
  
  &.confirmed {
    border-left: 4rpx solid var(--mg-primary);
  }
  
  &.completed {
    border-left: 4rpx solid var(--mg-success);
  }
  
  &.canceled {
    border-left: 4rpx solid var(--mg-gray-600);
    opacity: 0.7;
  }
  
  &::after {
    content: '>';
    position: absolute;
    right: 20rpx;
    color: var(--mg-gray-400);
    font-family: 'uniicons';
    transition: all 0.2s ease;
  }
  
  &:hover::after {
    right: 16rpx;
    color: var(--mg-primary);
  }
}

.appointment-time {
  font-size: 28rpx;
  color: var(--mg-info);
  font-weight: bold;
  width: 30%;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -4rpx;
    left: 0;
    width: 40rpx;
    height: 2rpx;
    background-color: var(--mg-info);
  }
}

.appointment-client {
  font-size: 28rpx;
  color: var(--mg-primary-dark);
  flex: 1;
  font-weight: 500;
}

.appointment-status {
  font-size: 24rpx;
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  font-weight: 500;
  
  &.pending {
    background-color: rgba(255, 152, 0, 0.15);
    color: var(--mg-warning);
    border: 1px solid var(--mg-warning);
  }
  
  &.confirmed {
    background-color: rgba(226, 170, 89, 0.15);
    color: var(--mg-primary-dark);
    border: 1px solid var(--mg-primary);
  }
  
  &.completed {
    background-color: rgba(76, 175, 80, 0.15);
    color: var(--mg-success);
    border: 1px solid var(--mg-success);
  }
  
  &.canceled {
    background-color: rgba(136, 136, 136, 0.15);
    color: var(--mg-gray-700);
    border: 1px solid var(--mg-gray-600);
  }
}

.empty-day-message {
  padding: 40rpx 0;
  text-align: center;
  color: var(--mg-text-tertiary);
  font-size: 28rpx;
  background-color: var(--mg-gray-100);
  border-radius: 8rpx;
  border: 1px dashed var(--mg-border-light);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
  background: linear-gradient(to bottom, var(--mg-white) 0%, var(--mg-gray-100) 100%);
  border-radius: 12rpx;
  box-shadow: 0 4rpx 16rpx var(--mg-shadow-color);
  border: 1px solid var(--mg-border-light);
}

.empty-icon {
  width: 200rpx;
  height: 200rpx;
  margin-bottom: 30rpx;
  opacity: 0.7;
}

.empty-text {
  font-size: 28rpx;
  color: var(--mg-primary-dark);
  position: relative;
  font-weight: 500;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -8rpx;
    left: 20%;
    width: 60%;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--mg-primary), transparent);
  }
}

// 动画
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

// 媒体查询 - 针对小屏幕优化
@media screen and (max-width: 375px) {
  .status-tabs {
    flex-wrap: wrap;
  }
  
  .tab-item {
    min-width: 33.33%;
  }
  
  .appointment-actions {
    flex-wrap: wrap;
  }
  
  .action-button {
    margin-bottom: 10rpx;
  }
}
</style> 