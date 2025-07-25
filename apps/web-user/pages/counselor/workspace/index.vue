<template>
  <view class="workspace-container">
    <!-- 顶部欢迎与今日概览 -->
    <view class="welcome-section" style="background-color: #F9EFD6;">
      <view class="welcome-text">
        <text class="greeting">您好，{{counselorName}}</text>
        <text class="date">{{currentDate}}</text>
      </view>
      <view class="avatar-container">
        <image class="avatar" :src="counselorAvatar" mode="aspectFill"></image>
      </view>
    </view>

    <!-- 预约数据概览 -->
    <view class="data-overview">
      <view class="overview-card" style="background-color: #FFF8EC;">
        <view class="card-value primary">{{todayAppointments.pending}}</view>
        <view class="card-label">今日待接待</view>
      </view>
      <view class="overview-card" style="background-color: #EAF7EA;">
        <view class="card-value success">{{todayAppointments.completed}}</view>
        <view class="card-label">今日已完成</view>
      </view>
      <view class="overview-card" style="background-color: #FFF3E0;">
        <view class="card-value warning">{{pendingRequests}}</view>
        <view class="card-label">待处理请求</view>
      </view>
      <view class="overview-card" style="background-color: #E3F2FD;">
        <view class="card-value info">{{unreadMessages}}</view>
        <view class="card-label">未读消息</view>
      </view>
    </view>

    <!-- 近期预约时间表 -->
    <view class="section-title">今日预约</view>
    <view class="schedule-section" style="background-color: #FFFFFF;" v-if="todaySchedule.length > 0">
      <scroll-view scroll-y class="schedule-list">
        <view 
          v-for="(item, index) in todaySchedule" 
          :key="index" 
          class="schedule-item"
          :class="{'completed': item.status === 'completed'}"
        >
          <view class="time-slot">{{item.timeSlot}}</view>
          <view class="appointment-info">
            <view class="client-name">{{item.clientName}}</view>
            <view class="service-type">{{item.serviceType}}</view>
          </view>
          <view class="appointment-status" :class="item.status">
            {{getStatusText(item.status)}}
          </view>
        </view>
      </scroll-view>
    </view>
    <view class="empty-data" style="background-color: #FFFFFF;" v-else>
      <text>今日暂无预约</text>
    </view>

    <!-- 收入统计 -->
    <view class="section-title">收入统计</view>
    <view class="income-section">
      <view class="income-card" style="background-color: #FFF8EC;">
        <view class="income-label">本周收入</view>
        <view class="income-value">¥{{income.weekly}}</view>
      </view>
      <view class="income-card" style="background-color: #FFF8EC;">
        <view class="income-label">本月收入</view>
        <view class="income-value">¥{{income.monthly}}</view>
      </view>
    </view>

    <!-- 功能入口 -->
    <view class="section-title">快捷功能</view>
    <view class="quick-actions" style="background-color: #FFFFFF;">
      <view class="action-item" @click="navigateTo('/pages/counselor/appointments/index')">
        <view class="action-icon appointment"></view>
        <text class="action-text">预约管理</text>
      </view>
      <view class="action-item" @click="navigateTo('/pages/counselor/time-slots/index')">
        <view class="action-icon time"></view>
        <text class="action-text">时间管理</text>
      </view>
      <view class="action-item" @click="navigateTo('/pages/counselor/clients/index')">
        <view class="action-icon client"></view>
        <text class="action-text">客户管理</text>
      </view>
      <view class="action-item" @click="navigateTo('/pages/counselor/profile/index')">
        <view class="action-icon profile"></view>
        <text class="action-text">个人主页</text>
      </view>
    </view>

    <!-- 最新评价 -->
    <view class="section-title">最新评价</view>
    <view class="reviews-section" style="background-color: #FFFFFF;" v-if="latestReviews.length > 0">
      <scroll-view scroll-y class="reviews-list">
        <view 
          v-for="(review, index) in latestReviews" 
          :key="index" 
          class="review-item"
        >
          <view class="review-header">
            <text class="client-name">{{review.clientName}}</text>
            <view class="rating">
              <text class="rating-value">{{review.rating}}</text>
              <text class="rating-max">/5</text>
            </view>
          </view>
          <view class="review-content">{{review.content}}</view>
          <view class="review-time">{{review.time}}</view>
        </view>
      </scroll-view>
    </view>
    <view class="empty-data" style="background-color: #FFFFFF;" v-else>
      <text>暂无评价</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      counselorName: '王医生',
      counselorAvatar: 'https://randomuser.me/api/portraits/women/68.jpg',
      currentDate: '',
      todayAppointments: {
        pending: 3,
        completed: 2
      },
      pendingRequests: 5,
      unreadMessages: 8,
      todaySchedule: [
        {
          timeSlot: '09:00-10:00',
          clientName: '张先生',
          serviceType: '个人咨询',
          status: 'pending'
        },
        {
          timeSlot: '11:00-12:00',
          clientName: '李女士',
          serviceType: '情绪管理',
          status: 'completed'
        },
        {
          timeSlot: '14:00-15:00',
          clientName: '刘先生',
          serviceType: '压力疏导',
          status: 'pending'
        },
        {
          timeSlot: '16:00-17:00',
          clientName: '陈女士',
          serviceType: '关系咨询',
          status: 'pending'
        }
      ],
      income: {
        weekly: 2800,
        monthly: 12600
      },
      latestReviews: [
        {
          clientName: '匿名用户',
          rating: 5,
          content: '非常专业的咨询，给了我很多实用的建议，感谢医生！',
          time: '2小时前'
        },
        {
          clientName: '李**',
          rating: 4.5,
          content: '咨询过程很舒适，医生很有耐心。下次还会继续预约。',
          time: '昨天'
        }
      ]
    }
  },
  onLoad() {
    this.setCurrentDate();
    // 这里应该从API获取数据
    // this.fetchDashboardData();
  },
  methods: {
    setCurrentDate() {
      const date = new Date();
      const year = date.getFullYear();
      const month = date.getMonth() + 1;
      const day = date.getDate();
      const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
      const weekday = weekdays[date.getDay()];
      this.currentDate = `${year}年${month}月${day}日 ${weekday}`;
    },
    getStatusText(status) {
      const statusMap = {
        pending: '待接待',
        completed: '已完成',
        canceled: '已取消'
      };
      return statusMap[status] || status;
    },
    navigateTo(url) {
      uni.navigateTo({
        url
      });
    },
    fetchDashboardData() {
      // 这里应该调用API获取仪表盘数据
      // 暂时使用模拟数据
    }
  }
}
</script>

<style lang="scss">
@import "@/static/theme.scss";
.workspace-container {
  padding: 30rpx;
  background-color: #f8f9fa;
  background-image: linear-gradient(to bottom, #f8f9fa 0%, #f3f5f7 100%);
  min-height: 100vh;
}

.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
  padding: 30rpx;
  background-color: white;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 8rpx;
    background: var(--mg-gradient-gold);
  }
  
  &::after {
    content: '';
    position: absolute;
    right: 0;
    top: 0;
    height: 100%;
    width: 60%;
    background-image: radial-gradient(circle at right top, rgba(226, 170, 89, 0.08) 0%, transparent 70%);
    z-index: 0;
  }
}

.welcome-text {
  display: flex;
  flex-direction: column;
  z-index: 1;
}

.greeting {
  font-size: 44rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 12rpx;
  letter-spacing: -0.5rpx;
}

.date {
  font-size: 28rpx;
  color: #666;
}

.avatar-container {
  width: 110rpx;
  height: 110rpx;
  border-radius: 50%;
  overflow: hidden;
  border: 4rpx solid white;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.avatar {
  width: 100%;
  height: 100%;
}

.data-overview {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30rpx;
}

.overview-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 24rpx 16rpx;
  width: 22%;
  text-align: center;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 4rpx;
    background: transparent;
    transition: transform 0.3s ease;
    transform: scaleX(0);
    transform-origin: left center;
  }
  
  &:hover::after {
    transform: scaleX(1);
  }
  
  &:nth-child(1)::after {
    background: var(--mg-primary);
  }
  
  &:nth-child(2)::after {
    background: var(--mg-success);
  }
  
  &:nth-child(3)::after {
    background: var(--mg-warning);
  }
  
  &:nth-child(4)::after {
    background: var(--mg-info);
  }
}

.card-value {
  font-size: 42rpx;
  font-weight: bold;
  margin-bottom: 10rpx;
  line-height: 1.2;
  
  &.primary {
    color: var(--mg-primary);
  }
  
  &.success {
    color: var(--mg-success);
  }
  
  &.warning {
    color: var(--mg-warning);
  }
  
  &.info {
    color: var(--mg-info);
  }
}

.card-label {
  font-size: 24rpx;
  color: #666;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin: 40rpx 0 20rpx;
  position: relative;
  padding-left: 20rpx;
  display: flex;
  align-items: center;
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 6rpx;
    height: 26rpx;
    background-color: var(--mg-primary);
    border-radius: 3rpx;
  }
}

.schedule-section {
  background-color: white;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
  max-height: 300rpx;
  position: relative;
  overflow: hidden;
  
  &::after {
    content: '';
    position: absolute;
    right: 0;
    bottom: 0;
    width: 100rpx;
    height: 100rpx;
    background-image: radial-gradient(circle at bottom right, rgba(226, 170, 89, 0.06) 0%, transparent 70%);
  }
}

.schedule-list {
  max-height: 300rpx;
  position: relative;
  z-index: 1;
}

.schedule-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 10rpx;
  border-bottom: 1rpx solid #f0f0f0;
  transition: background-color 0.2s ease;
  
  &:last-child {
    border-bottom: none;
  }
  
  &.completed {
    opacity: 0.7;
  }
  
  &:hover {
    background-color: #fafafa;
    border-radius: 8rpx;
  }
}

.time-slot {
  width: 25%;
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

.appointment-info {
  width: 50%;
}

.client-name {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 6rpx;
  font-weight: 500;
}

.service-type {
  font-size: 24rpx;
  color: #888;
}

.appointment-status {
  width: 20%;
  font-size: 24rpx;
  text-align: center;
  padding: 6rpx 12rpx;
  border-radius: 20rpx;
  font-weight: 500;
  
  &.pending {
    color: var(--mg-warning);
    background-color: rgba(255, 152, 0, 0.1);
  }
  
  &.completed {
    color: var(--mg-success);
    background-color: rgba(76, 175, 80, 0.1);
  }
  
  &.canceled {
    color: var(--mg-error);
    background-color: rgba(244, 67, 54, 0.1);
  }
}

.empty-data {
  background-color: white;
  border-radius: 16rpx;
  padding: 40rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
  text-align: center;
  color: #888;
}

.income-section {
  display: flex;
  justify-content: space-between;
  gap: 20rpx;
}

.income-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 30rpx;
  width: 48%;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 6rpx;
    background: var(--mg-gradient-gold);
  }
  
  &::after {
    content: '';
    position: absolute;
    right: 0;
    bottom: 0;
    width: 100rpx;
    height: 100rpx;
    background-image: radial-gradient(circle at bottom right, rgba(226, 170, 89, 0.08) 0%, transparent 70%);
  }
}

.income-label {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 20rpx;
}

.income-value {
  font-size: 48rpx;
  font-weight: bold;
  color: var(--mg-primary);
  letter-spacing: -1rpx;
}

.quick-actions {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  background-color: white;
  border-radius: 16rpx;
  padding: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.action-item {
  width: 24%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24rpx 0;
  transition: transform 0.2s ease;
  border-radius: 12rpx;
  
  &:hover {
    background-color: #fafafa;
  }
}

.action-icon {
  width: 90rpx;
  height: 90rpx;
  border-radius: 16rpx;
  margin-bottom: 16rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -6rpx;
    left: 50%;
    transform: translateX(-50%);
    width: 40%;
    height: 6rpx;
    border-radius: 3rpx;
    opacity: 0.7;
  }
  
  &.appointment {
    background: var(--mg-primary);
    &::before {
      content: "\e6dd";
      font-family: "uniicons";
      font-size: 44rpx;
    }
    &::after {
      background: var(--mg-primary-dark);
    }
  }
  
  &.time {
    background: var(--mg-info);
    &::before {
      content: "\e65f";
      font-family: "uniicons";
      font-size: 44rpx;
    }
    &::after {
      background: var(--mg-info-dark);
    }
  }
  
  &.client {
    background: var(--mg-warning);
    &::before {
      content: "\e604";
      font-family: "uniicons";
      font-size: 44rpx;
    }
    &::after {
      background: var(--mg-warning-dark);
    }
  }
  
  &.profile {
    background: var(--mg-success);
    &::before {
      content: "\e70b";
      font-family: "uniicons";
      font-size: 44rpx;
    }
    &::after {
      background: var(--mg-success-dark);
    }
  }
}

.action-text {
  font-size: 26rpx;
  color: #666;
  margin-top: 6rpx;
  
  .action-item:hover & {
    color: var(--mg-primary);
  }
}

.reviews-section {
  background-color: white;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
  max-height: 300rpx;
  position: relative;
  overflow: hidden;
  
  &::after {
    content: '';
    position: absolute;
    right: 0;
    bottom: 0;
    width: 120rpx;
    height: 120rpx;
    background-image: radial-gradient(circle at bottom right, rgba(226, 170, 89, 0.06) 0%, transparent 70%);
    z-index: 0;
  }
}

.reviews-list {
  max-height: 300rpx;
  position: relative;
  z-index: 1;
}

.review-item {
  padding: 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
  transition: background-color 0.2s ease;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    background-color: #fafafa;
  }
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10rpx;
}

.rating {
  display: flex;
  align-items: baseline;
  padding: 4rpx 12rpx;
  border-radius: 20rpx;
  background-color: #FFF8EC;
}

.rating-value {
  font-size: 32rpx;
  font-weight: bold;
  color: var(--mg-primary);
}

.rating-max {
  font-size: 24rpx;
  color: #999;
}

.review-content {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 10rpx;
  line-height: 1.5;
  padding: 12rpx 16rpx;
  background-color: #FAFAFA;
  border-radius: 10rpx;
  font-style: italic;
  position: relative;
  
  &::before {
    content: '"';
    position: absolute;
    left: 6rpx;
    top: 0;
    font-size: 32rpx;
    color: #ddd;
  }
  
  &::after {
    content: '"';
    position: absolute;
    right: 6rpx;
    bottom: 0;
    font-size: 32rpx;
    color: #ddd;
  }
}

.review-time {
  font-size: 24rpx;
  color: #999;
  text-align: right;
}

// 媒体查询 - 针对小屏幕优化
@media screen and (max-width: 375px) {
  .data-overview {
    flex-wrap: wrap;
  }
  
  .overview-card {
    width: 48%;
    margin-bottom: 16rpx;
  }
  
  .quick-actions {
    padding: 20rpx 16rpx;
  }
  
  .action-item {
    width: 48%;
    margin-bottom: 20rpx;
  }
}
</style> 