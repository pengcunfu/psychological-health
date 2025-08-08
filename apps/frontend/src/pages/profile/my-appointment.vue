<template>
  <view class="container">
    <!-- 顶部导航 -->
    <!-- <Navbar 
      title="我的预约"
      :showLeft="true"
      :showRight="false"
      @leftClick="goBack"
    /> -->

    <view class="tab-section">
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'upcoming' }" 
        @click="switchTab('upcoming')"
      >
        待完成
      </view>
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'completed' }" 
        @click="switchTab('completed')"
      >
        已完成
      </view>
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'cancelled' }" 
        @click="switchTab('cancelled')"
      >
        已取消
      </view>
    </view>

    <view class="content-section">
      <view v-if="appointments.length > 0">
        <view 
          class="appointment-card" 
          v-for="(item, index) in appointments" 
          :key="index"
          @click="navigateToDetail(item.id)"
        >
          <view class="appointment-header">
            <view class="counselor-info">
              <up-avatar :src="item.counselor_avatar || '/static/images/default-avatar.png'" size="80"></up-avatar>
              <view class="counselor-detail">
                <text class="counselor-name">{{ item.counselor_name }}</text>
                <text class="counselor-title">{{ item.counselor_title }}</text>
              </view>
            </view>
            <view class="appointment-status" :class="`status-${item.status}`">
              {{ getStatusText(item.status) }}
            </view>
          </view>
          
          <view class="appointment-info">
            <view class="info-item">
              <up-icon name="calendar" size="30" color="#4A90E2"></up-icon>
              <text class="info-text">{{ item.appointment_date }}</text>
            </view>
            <view class="info-item">
              <up-icon name="clock" size="30" color="#4A90E2"></up-icon>
              <text class="info-text">{{ item.start_time }} - {{ item.end_time }}</text>
            </view>
            <view class="info-item">
              <up-icon name="map" size="30" color="#4A90E2"></up-icon>
              <text class="info-text">{{ item.type === 'online' ? '线上咨询' : '线下咨询' }}</text>
            </view>
            <view class="info-item" v-if="item.type === 'offline'">
              <up-icon name="home" size="30" color="#4A90E2"></up-icon>
              <text class="info-text">{{ item.address }}</text>
            </view>
          </view>
          
          <view class="appointment-footer">
            <text class="appointment-price">¥{{ item.price }}</text>
            <view class="action-btns">
              <button 
                class="action-btn cancel-btn" 
                v-if="item.status === 'pending' || item.status === 'confirmed'"
                @click.stop="handleCancel(item)"
              >
                取消预约
              </button>
              <button 
                class="action-btn consult-btn" 
                v-if="item.status === 'confirmed' && item.type === 'online'"
                @click.stop="handleStartConsult(item)"
              >
                开始咨询
              </button>
              <button 
                class="action-btn comment-btn" 
                v-if="item.status === 'completed' && !item.has_commented"
                @click.stop="handleComment(item)"
              >
                评价
              </button>
            </view>
          </view>
        </view>
      </view>
      <view v-else class="empty-content">
        <up-empty mode="list" icon="calendar" :text="`暂无${getTabText()}预约`"></up-empty>
      </view>
    </view>
    
    <!-- 评价弹窗 -->
    <up-popup :show="showCommentModal" mode="center" @close="showCommentModal = false" round="10">
      <view class="comment-popup">
        <view class="popup-title">评价咨询</view>
        
        <view class="rating-section">
          <text class="rating-label">服务评分</text>
          <up-rate v-model="commentForm.rating" count="5" active-color="#faad14" size="40"></up-rate>
        </view>
        
        <view class="comment-section">
          <up--textarea
            v-model="commentForm.content"
            placeholder="请输入您的评价内容"
            height="200"
            count
            maxlength="500"
          ></up--textarea>
        </view>
        
        <view class="popup-btns">
          <button class="cancel-btn" @click="showCommentModal = false">取消</button>
          <button class="confirm-btn" @click="submitComment">提交评价</button>
        </view>
      </view>
    </up-popup>
    
    <!-- 取消预约弹窗 -->
    <up-popup :show="showCancelModal" mode="center" @close="showCancelModal = false" round="10">
      <view class="cancel-popup">
        <view class="popup-title">取消预约</view>
        
        <view class="cancel-section">
          <text class="cancel-tips">取消预约后，将按照平台规则进行退款</text>
          
          <view class="reason-section">
            <text class="reason-label">取消原因</text>
            <up-radio-group v-model="cancelForm.reason">
              <up-radio 
                v-for="(item, index) in cancelReasons" 
                :key="index"
                :name="item.value"
                :label="item.label"
                :customStyle="{marginBottom: '16px'}"
              ></up-radio>
            </up-radio-group>
          </view>
          
          <view class="remark-section" v-if="cancelForm.reason === 'other'">
            <up--textarea
              v-model="cancelForm.remark"
              placeholder="请输入取消原因"
              height="150"
              count
              maxlength="200"
            ></up--textarea>
          </view>
        </view>
        
        <view class="popup-btns">
          <button class="cancel-btn" @click="showCancelModal = false">返回</button>
          <button class="confirm-btn danger" @click="submitCancel">确认取消</button>
        </view>
      </view>
    </up-popup>
  </view>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { onLoad, onPullDownRefresh, onReachBottom } from '@dcloudio/uni-app'
import { request } from '@/utils/request'
import { checkLogin } from '@/utils/auth'
import Navbar from '@/components/Navbar.vue'

// 检查登录状态
if (!checkLogin()) {
  // 如果未登录，直接返回
}
    
    const activeTab = ref('upcoming')
    const appointments = ref([])
    const pagination = reactive({
      page: 1,
      per_page: 10,
      total: 0,
      total_pages: 0
    })
    const loading = ref(false)
    
    // 评价相关
    const showCommentModal = ref(false)
    const currentAppointment = ref(null)
    const commentForm = reactive({
      rating: 5,
      content: ''
    })
    
    // 取消预约相关
    const showCancelModal = ref(false)
    const cancelForm = reactive({
      reason: 'schedule_conflict',
      remark: ''
    })
    const cancelReasons = [
      { value: 'schedule_conflict', label: '时间冲突，无法按时参加' },
      { value: 'found_other', label: '已找到其他咨询师' },
      { value: 'health_issue', label: '身体不适，无法参加' },
      { value: 'price_issue', label: '价格原因' },
      { value: 'other', label: '其他原因' }
    ]
    
    // 获取预约列表
    const fetchAppointments = async (reset = false) => {
      if (loading.value) return
      
      if (reset) {
        pagination.page = 1
        appointments.value = []
      }
      
      loading.value = true
      
      try {
        // 根据当前标签页确定状态过滤
        let status = ''
        switch (activeTab.value) {
          case 'upcoming':
            status = 'pending,confirmed'
            break
          case 'completed':
            status = 'completed'
            break
          case 'cancelled':
            status = 'cancelled'
            break
        }
        
        const res = await request({
          url: '/appointment/my',
          method: 'GET',
          data: {
            page: pagination.page,
            per_page: pagination.per_page,
            status: status
          }
        })
        
        if (res.code === 200 && res.success) {
          const newList = res.data.list || []
          appointments.value = reset ? newList : [...appointments.value, ...newList]
          
          pagination.total = res.data.total || 0
          pagination.total_pages = res.data.pages || 0
        } else {
          uni.showToast({
            title: res.message || '获取预约列表失败',
            icon: 'none'
          })
        }
      } catch (error) {
        console.error('获取预约列表失败:', error)
        uni.showToast({
          title: '获取预约列表失败，请稍后重试',
          icon: 'none'
        })
      } finally {
        loading.value = false
        
        // 停止下拉刷新
        uni.stopPullDownRefresh()
      }
    }
    
    // 切换标签页
    const switchTab = (tab) => {
      activeTab.value = tab
      fetchAppointments(true)
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'pending':
          return '待确认'
        case 'confirmed':
          return '已确认'
        case 'completed':
          return '已完成'
        case 'cancelled':
          return '已取消'
        default:
          return '未知状态'
      }
    }
    
    // 获取当前标签页文本
    const getTabText = () => {
      switch (activeTab.value) {
        case 'upcoming':
          return '待完成'
        case 'completed':
          return '已完成'
        case 'cancelled':
          return '已取消'
        default:
          return ''
      }
    }
    
    // 跳转到详情页
    const navigateToDetail = (id) => {
      uni.navigateTo({
        url: `/pages/profile/my-appointment/detail?id=${id}`
      })
    }
    
    // 开始咨询
    const handleStartConsult = (appointment) => {
      uni.navigateTo({
        url: `/pages/message/chat?type=counselor&id=${appointment.counselor_id}`
      })
    }
    
    // 评价
    const handleComment = (appointment) => {
      currentAppointment.value = appointment
      commentForm.rating = 5
      commentForm.content = ''
      showCommentModal.value = true
    }
    
    // 提交评价
    const submitComment = async () => {
      if (!currentAppointment.value) return
      
      if (!commentForm.content) {
        uni.showToast({
          title: '请输入评价内容',
          icon: 'none'
        })
        return
      }
      
      try {
        uni.showLoading({
          title: '提交中...'
        })
        
        const res = await request({
          url: `/appointment/${currentAppointment.value.id}/comment`,
          method: 'POST',
          data: {
            rating: commentForm.rating,
            content: commentForm.content
          }
        })
        
        uni.hideLoading()
        
        if (res.code === 200 && res.success) {
          uni.showToast({
            title: '评价成功',
            icon: 'success'
          })
          
          // 更新当前预约的评价状态
          const index = appointments.value.findIndex(item => item.id === currentAppointment.value.id)
          if (index !== -1) {
            appointments.value[index].has_commented = true
          }
          
          showCommentModal.value = false
        } else {
          uni.showToast({
            title: res.message || '评价失败',
            icon: 'none'
          })
        }
      } catch (error) {
        uni.hideLoading()
        console.error('提交评价失败:', error)
        uni.showToast({
          title: '评价失败，请稍后重试',
          icon: 'none'
        })
      }
    }
    
    // 取消预约
    const handleCancel = (appointment) => {
      currentAppointment.value = appointment
      cancelForm.reason = 'schedule_conflict'
      cancelForm.remark = ''
      showCancelModal.value = true
    }
    
    // 提交取消
    const submitCancel = async () => {
      if (!currentAppointment.value) return
      
      if (cancelForm.reason === 'other' && !cancelForm.remark) {
        uni.showToast({
          title: '请输入取消原因',
          icon: 'none'
        })
        return
      }
      
      try {
        uni.showLoading({
          title: '处理中...'
        })
        
        const res = await request({
          url: `/appointment/${currentAppointment.value.id}/cancel`,
          method: 'POST',
          data: {
            reason: cancelForm.reason === 'other' ? cancelForm.remark : cancelForm.reason
          }
        })
        
        uni.hideLoading()
        
        if (res.code === 200 && res.success) {
          uni.showToast({
            title: '取消成功',
            icon: 'success'
          })
          
          // 刷新列表
          fetchAppointments(true)
          
          showCancelModal.value = false
        } else {
          uni.showToast({
            title: res.message || '取消失败',
            icon: 'none'
          })
        }
      } catch (error) {
        uni.hideLoading()
        console.error('取消预约失败:', error)
        uni.showToast({
          title: '取消失败，请稍后重试',
          icon: 'none'
        })
      }
    }
    
    // 返回上一页
    const goBack = () => {
      uni.navigateBack()
    }
    
    // 页面加载
    onLoad(() => {
      fetchAppointments(true)
    })
    
    // 下拉刷新
    onPullDownRefresh(() => {
      fetchAppointments(true)
    })
    
    // 上拉加载更多
    onReachBottom(() => {
      if (loading.value) return
      
      if (pagination.page < pagination.total_pages) {
        pagination.page++
        fetchAppointments()
      }
    })
    
// 所有变量和函数已在 setup 语法糖中定义，无需返回
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 30rpx;
}

.tab-section {
  display: flex;
  background-color: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 30rpx 0;
  font-size: 28rpx;
  color: #666;
  position: relative;

  &.active {
    color: #4A90E2;
    font-weight: bold;

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 60rpx;
      height: 4rpx;
      background-color: #4A90E2;
    }
  }
}

.content-section {
  padding: 20rpx 30rpx;
}

.appointment-card {
  background-color: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.appointment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
  padding-bottom: 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.counselor-info {
  display: flex;
  align-items: center;
}

.counselor-detail {
  margin-left: 20rpx;

  .counselor-name {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
  }

  .counselor-title {
    font-size: 24rpx;
    color: #666;
  }
}

.appointment-status {
  font-size: 28rpx;
  font-weight: bold;

  &.status-pending {
    color: #faad14;
  }

  &.status-confirmed {
    color: #4A90E2;
  }

  &.status-completed {
    color: #52c41a;
  }

  &.status-cancelled {
    color: #999;
  }
}

.appointment-info {
  margin-bottom: 20rpx;

  .info-item {
    display: flex;
    align-items: center;
    margin-bottom: 10rpx;

    .info-text {
      font-size: 28rpx;
      color: #333;
      margin-left: 10rpx;
    }
  }
}

.appointment-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20rpx;
  border-top: 1rpx solid #f0f0f0;

  .appointment-price {
    font-size: 36rpx;
    color: #f5222d;
    font-weight: bold;
  }

  .action-btns {
    display: flex;

    .action-btn {
      padding: 10rpx 30rpx;
      font-size: 28rpx;
      border-radius: 30rpx;
      margin-left: 20rpx;

      &.cancel-btn {
        background-color: #fff;
        color: #999;
        border: 1rpx solid #ddd;
      }

      &.consult-btn {
        background-color: #4A90E2;
        color: #fff;
        border: none;
      }

      &.comment-btn {
        background-color: #faad14;
        color: #fff;
        border: none;
      }
    }
  }
}

.empty-content {
  padding: 100rpx 0;
  text-align: center;
}

.comment-popup, .cancel-popup {
  width: 650rpx;
  background-color: #fff;
  border-radius: 20rpx;
  padding: 30rpx;

  .popup-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    text-align: center;
    margin-bottom: 30rpx;
  }
}

.rating-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30rpx;

  .rating-label {
    font-size: 28rpx;
    color: #333;
    margin-bottom: 20rpx;
  }
}

.comment-section {
  margin-bottom: 30rpx;
}

.cancel-tips {
  font-size: 28rpx;
  color: #f5222d;
  margin-bottom: 30rpx;
  display: block;
}

.reason-section {
  margin-bottom: 30rpx;

  .reason-label {
    font-size: 28rpx;
    color: #333;
    margin-bottom: 20rpx;
    display: block;
  }
}

.remark-section {
  margin-bottom: 30rpx;
}

.popup-btns {
  display: flex;
  justify-content: space-between;

  .cancel-btn, .confirm-btn {
    width: 280rpx;
    height: 80rpx;
    line-height: 80rpx;
    font-size: 28rpx;
    border-radius: 10rpx;
    border: none;
  }

  .cancel-btn {
    background-color: #f5f5f5;
    color: #666;
  }

  .confirm-btn {
    background-color: #4A90E2;
    color: #fff;

    &.danger {
      background-color: #f5222d;
    }
  }
}
</style> 