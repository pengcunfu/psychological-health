<template>
  <view class="container">
    <view class="tab-section">
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'all' }" 
        @click="switchTab('all')"
      >
        全部
      </view>
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'pending' }" 
        @click="switchTab('pending')"
      >
        待付款
      </view>
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'paid' }" 
        @click="switchTab('paid')"
      >
        已付款
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
      <view v-if="orders.length > 0">
        <view 
          class="order-card" 
          v-for="(item, index) in orders" 
          :key="index"
          @click="navigateToDetail(item.id)"
        >
          <view class="order-header">
            <text class="order-number">订单号：{{ item.order_number }}</text>
            <view class="order-status" :class="`status-${item.status}`">
              {{ getStatusText(item.status) }}
            </view>
          </view>
          
          <view class="order-content">
            <view class="order-item">
              <image 
                class="item-image" 
                :src="item.cover || '/static/images/default-cover.png'" 
                mode="aspectFill"
              ></image>
              <view class="item-info">
                <text class="item-name">{{ item.title }}</text>
                <view class="item-type">{{ getOrderTypeText(item.type) }}</view>
                <view class="item-price-row">
                  <text class="item-price">¥{{ item.price }}</text>
                  <text class="item-quantity">x{{ item.quantity || 1 }}</text>
                </view>
              </view>
            </view>
          </view>
          
          <view class="order-footer">
            <view class="order-info">
              <text class="order-time">{{ item.create_time }}</text>
              <text class="order-total">合计：¥{{ item.total_amount }}</text>
            </view>
            <view class="order-actions">
              <button 
                class="action-btn cancel-btn" 
                v-if="item.status === 'pending'"
                @click.stop="handleCancel(item)"
              >
                取消订单
              </button>
              <button 
                class="action-btn pay-btn" 
                v-if="item.status === 'pending'"
                @click.stop="handlePay(item)"
              >
                去支付
              </button>
              <button 
                class="action-btn detail-btn" 
                v-if="item.status === 'paid' || item.status === 'completed'"
                @click.stop="handleViewDetail(item)"
              >
                查看详情
              </button>
            </view>
          </view>
        </view>
      </view>
      <view v-else class="empty-content">
        <up-empty mode="order" icon="order" :text="`暂无${getTabText()}订单`"></up-empty>
      </view>
    </view>
    
    <!-- 取消订单弹窗 -->
    <up-popup :show="showCancelModal" mode="center" @close="showCancelModal = false" round="10">
      <view class="cancel-popup">
        <view class="popup-title">取消订单</view>
        
        <view class="cancel-section">
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

<script>
import { ref, reactive } from 'vue'
import { onLoad, onPullDownRefresh, onReachBottom } from '@dcloudio/uni-app'
import { request } from '@/utils/request'
import { checkLogin } from '@/utils/auth'

export default {
  setup() {
    // 检查登录状态
    if (!checkLogin()) return {}
    
    const activeTab = ref('all')
    const orders = ref([])
    const pagination = reactive({
      page: 1,
      per_page: 10,
      total: 0,
      total_pages: 0
    })
    const loading = ref(false)
    
    // 取消订单相关
    const showCancelModal = ref(false)
    const currentOrder = ref(null)
    const cancelForm = reactive({
      reason: 'changed_mind',
      remark: ''
    })
    const cancelReasons = [
      { value: 'changed_mind', label: '我改变了主意' },
      { value: 'duplicate_order', label: '重复下单' },
      { value: 'payment_issue', label: '支付问题' },
      { value: 'price_issue', label: '价格原因' },
      { value: 'other', label: '其他原因' }
    ]
    
    // 获取订单列表
    const fetchOrders = async (reset = false) => {
      if (loading.value) return
      
      if (reset) {
        pagination.page = 1
        orders.value = []
      }
      
      loading.value = true
      
      try {
        // 根据当前标签页确定状态过滤
        let status = ''
        switch (activeTab.value) {
          case 'all':
            status = ''
            break
          case 'pending':
            status = 'pending'
            break
          case 'paid':
            status = 'paid,completed'
            break
          case 'cancelled':
            status = 'cancelled'
            break
        }
        
        const res = await request({
          url: '/order/my',
          method: 'GET',
          data: {
            page: pagination.page,
            per_page: pagination.per_page,
            status: status
          }
        })
        
        if (res.code === 200 && res.success) {
          const newList = res.data.list || []
          orders.value = reset ? newList : [...orders.value, ...newList]
          
          pagination.total = res.data.total || 0
          pagination.total_pages = res.data.pages || 0
        } else {
          uni.showToast({
            title: res.message || '获取订单列表失败',
            icon: 'none'
          })
        }
      } catch (error) {
        console.error('获取订单列表失败:', error)
        uni.showToast({
          title: '获取订单列表失败，请稍后重试',
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
      fetchOrders(true)
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'pending':
          return '待付款'
        case 'paid':
          return '已付款'
        case 'completed':
          return '已完成'
        case 'cancelled':
          return '已取消'
        default:
          return '未知状态'
      }
    }
    
    // 获取订单类型文本
    const getOrderTypeText = (type) => {
      switch (type) {
        case 'course':
          return '课程'
        case 'appointment':
          return '咨询预约'
        case 'membership':
          return '会员'
        default:
          return '商品'
      }
    }
    
    // 获取当前标签页文本
    const getTabText = () => {
      switch (activeTab.value) {
        case 'all':
          return ''
        case 'pending':
          return '待付款'
        case 'paid':
          return '已付款'
        case 'cancelled':
          return '已取消'
        default:
          return ''
      }
    }
    
    // 跳转到详情页
    const navigateToDetail = (id) => {
      uni.navigateTo({
        url: `/pages/order/detail?id=${id}`
      })
    }
    
    // 取消订单
    const handleCancel = (order) => {
      currentOrder.value = order
      cancelForm.reason = 'changed_mind'
      cancelForm.remark = ''
      showCancelModal.value = true
    }
    
    // 提交取消
    const submitCancel = async () => {
      if (!currentOrder.value) return
      
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
          url: `/order/${currentOrder.value.id}/cancel`,
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
          fetchOrders(true)
          
          showCancelModal.value = false
        } else {
          uni.showToast({
            title: res.message || '取消失败',
            icon: 'none'
          })
        }
      } catch (error) {
        uni.hideLoading()
        console.error('取消订单失败:', error)
        uni.showToast({
          title: '取消失败，请稍后重试',
          icon: 'none'
        })
      }
    }
    
    // 去支付
    const handlePay = (order) => {
      uni.navigateTo({
        url: `/pages/order/pay?id=${order.id}`
      })
    }
    
    // 查看详情
    const handleViewDetail = (order) => {
      if (order.type === 'course') {
        uni.navigateTo({
          url: `/pages/course/detail?id=${order.target_id}`
        })
      } else if (order.type === 'appointment') {
        uni.navigateTo({
          url: `/pages/profile/my-appointment/detail?id=${order.target_id}`
        })
      } else {
        navigateToDetail(order.id)
      }
    }
    
    // 页面加载
    onLoad(() => {
      fetchOrders(true)
    })
    
    // 下拉刷新
    onPullDownRefresh(() => {
      fetchOrders(true)
    })
    
    // 上拉加载更多
    onReachBottom(() => {
      if (loading.value) return
      
      if (pagination.page < pagination.total_pages) {
        pagination.page++
        fetchOrders()
      }
    })
    
    return {
      activeTab,
      orders,
      showCancelModal,
      cancelForm,
      cancelReasons,
      switchTab,
      getStatusText,
      getOrderTypeText,
      getTabText,
      navigateToDetail,
      handleCancel,
      submitCancel,
      handlePay,
      handleViewDetail
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
  padding: 20rpx 30rpx;
}

.order-card {
  background-color: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
  padding-bottom: 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.order-number {
  font-size: 28rpx;
  color: #666;
}

.order-status {
  font-size: 28rpx;
  font-weight: bold;
}

.status-pending {
  color: #faad14;
}

.status-paid {
  color: #4A90E2;
}

.status-completed {
  color: #52c41a;
}

.status-cancelled {
  color: #999;
}

.order-content {
  margin-bottom: 20rpx;
}

.order-item {
  display: flex;
  padding-bottom: 20rpx;
}

.item-image {
  width: 160rpx;
  height: 160rpx;
  border-radius: 10rpx;
  background-color: #f0f0f0;
}

.item-info {
  flex: 1;
  margin-left: 20rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.item-name {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
  margin-bottom: 10rpx;
}

.item-type {
  font-size: 24rpx;
  color: #666;
  background-color: #f5f7fa;
  display: inline-block;
  padding: 4rpx 10rpx;
  border-radius: 4rpx;
  margin-bottom: 10rpx;
}

.item-price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-price {
  font-size: 28rpx;
  color: #f5222d;
}

.item-quantity {
  font-size: 24rpx;
  color: #999;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20rpx;
  border-top: 1rpx solid #f0f0f0;
}

.order-info {
  display: flex;
  flex-direction: column;
}

.order-time {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 10rpx;
}

.order-total {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
}

.order-actions {
  display: flex;
}

.action-btn {
  padding: 10rpx 30rpx;
  font-size: 28rpx;
  border-radius: 30rpx;
  margin-left: 20rpx;
}

.cancel-btn {
  background-color: #fff;
  color: #999;
  border: 1rpx solid #ddd;
}

.pay-btn {
  background-color: #f5222d;
  color: #fff;
  border: none;
}

.detail-btn {
  background-color: #4A90E2;
  color: #fff;
  border: none;
}

.empty-content {
  padding: 100rpx 0;
  text-align: center;
}

.cancel-popup {
  width: 650rpx;
  background-color: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
}

.popup-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin-bottom: 30rpx;
}

.cancel-section {
  margin-bottom: 30rpx;
}

.reason-section {
  margin-bottom: 30rpx;
}

.reason-label {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.remark-section {
  margin-bottom: 30rpx;
}

.popup-btns {
  display: flex;
  justify-content: space-between;
}

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
}

.danger {
  background-color: #f5222d;
}
</style> 