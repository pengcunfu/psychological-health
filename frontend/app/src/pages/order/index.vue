<template>
  <view class="container">
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-bar">
        <up-icon name="search" size="20" color="#999"></up-icon>
        <input 
          v-model="searchKeyword" 
          placeholder="搜索订单号或商品名称" 
          class="search-input"
          @input="handleSearch"
          @confirm="handleSearch"
        />
        <view v-if="searchKeyword" class="clear-btn" @click="clearSearch">
          <up-icon name="close" size="16" color="#999"></up-icon>
        </view>
      </view>
    </view>

    <!-- 订单分类标签 -->
    <view class="tabs-section">
      <view class="tabs">
        <view 
          v-for="(tab, index) in orderTabs" 
          :key="index"
          class="tab-item"
          :class="{ active: currentTab === tab.key }"
          @click="switchTab(tab.key)"
        >
          {{ tab.label }}
        </view>
      </view>
    </view>

    <!-- 订单列表 -->
    <view class="order-list" v-if="orderList.length > 0">
      <view 
        v-for="order in orderList" 
        :key="order.id"
        class="order-item"
        @click="viewDetail(order)"
      >
        <!-- 订单头部 -->
        <view class="order-header">
          <view class="order-info">
            <text class="order-number">订单号：{{ order.order_number }}</text>
            <text class="order-time">{{ formatTime(order.created_at) }}</text>
          </view>
          <view class="order-status" :class="`status-${order.status}`">
            {{ getStatusText(order.status) }}
          </view>
        </view>

        <!-- 订单内容 -->
        <view class="order-content">
          <view class="order-main">
            <view class="service-info">
              <view class="service-title">{{ order.service_name || '心理咨询服务' }}</view>
              <view class="service-desc" v-if="order.counselor_name">
                咨询师：{{ order.counselor_name }}
              </view>
              <view class="service-desc" v-if="order.appointment_time">
                预约时间：{{ formatDateTime(order.appointment_time) }}
              </view>
            </view>
            <view class="order-amount">
              <text class="amount-symbol">¥</text>
              <text class="amount-value">{{ order.amount }}</text>
            </view>
          </view>
        </view>

        <!-- 订单操作 -->
        <view class="order-actions" v-if="getOrderActions(order).length > 0">
          <view 
            v-for="action in getOrderActions(order)" 
            :key="action.key"
            class="action-btn"
            :class="action.type"
            @click.stop="handleAction(action.key, order)"
          >
            {{ action.label }}
          </view>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view class="empty-state" v-else-if="!loading">
      <view class="empty-icon">📋</view>
      <text class="empty-text">{{ getEmptyText() }}</text>
      <view class="empty-btn" @click="goToServices" v-if="currentTab === 'all'">
        <text>去看看服务</text>
      </view>
    </view>

    <!-- 加载状态 -->
    <view class="loading-state" v-if="loading">
      <up-loading-icon mode="spinner"></up-loading-icon>
      <text class="loading-text">加载中...</text>
    </view>

    <!-- 分页加载更多 -->
    <view class="load-more" v-if="orderList.length > 0 && hasMore" @click="loadMore">
      <text class="load-more-text">{{ loadingMore ? '加载中...' : '加载更多' }}</text>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { onLoad, onShow, onPullDownRefresh, onReachBottom } from '@dcloudio/uni-app'

// 响应式数据
const searchKeyword = ref('')
const currentTab = ref('all')
const orderList = ref([])
const loading = ref(false)
const loadingMore = ref(false)
const searchTimeout = ref(null)

// 分页参数
const pagination = reactive({
  page: 1,
  per_page: 10,
  total: 0,
  pages: 1
})

// 订单标签
const orderTabs = ref([
  { key: 'all', label: '全部' },
  { key: 'pending', label: '待付款' },
  { key: 'paid', label: '已付款' },
  { key: 'completed', label: '已完成' },
  { key: 'cancelled', label: '已取消' }
])

// 计算属性
const hasMore = computed(() => pagination.page < pagination.pages)

// 订单状态映射
const statusMap = {
  'pending': '待付款',
  'paid': '已付款',
  'processing': '处理中',
  'completed': '已完成',
  'cancelled': '已取消',
  'refunded': '已退款'
}

// 模拟订单数据
const mockOrders = [
  {
    id: 1,
    order_number: 'ORD202401150001',
    status: 'completed',
    amount: 299.00,
    service_name: '心理咨询服务',
    counselor_name: '张医生',
    appointment_time: '2024-01-20 14:00:00',
    created_at: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    order_number: 'ORD202401140002',
    status: 'paid',
    amount: 199.00,
    service_name: '心理课程',
    counselor_name: '',
    appointment_time: '',
    created_at: '2024-01-14 16:20:00'
  },
  {
    id: 3,
    order_number: 'ORD202401130003',
    status: 'pending',
    amount: 399.00,
    service_name: '深度心理分析',
    counselor_name: '李咨询师',
    appointment_time: '2024-01-25 09:00:00',
    created_at: '2024-01-13 09:15:00'
  }
]

// 方法
const getStatusText = (status) => {
  return statusMap[status] || status
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return `${date.getMonth() + 1}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

const formatDateTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return `${date.getMonth() + 1}月${date.getDate()}日 ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

const getEmptyText = () => {
  const textMap = {
    'all': '您还没有下单',
    'pending': '没有待付款订单',
    'paid': '没有已付款订单',
    'completed': '没有已完成订单',
    'cancelled': '没有已取消订单'
  }
  return textMap[currentTab.value] || '暂无订单'
}

const getOrderActions = (order) => {
  const actions = []
  
  switch (order.status) {
    case 'pending':
      actions.push(
        { key: 'pay', label: '立即付款', type: 'primary' },
        { key: 'cancel', label: '取消订单', type: 'default' }
      )
      break
    case 'paid':
      actions.push(
        { key: 'contact', label: '联系咨询师', type: 'default' }
      )
      break
    case 'completed':
      actions.push(
        { key: 'evaluate', label: '评价', type: 'default' },
        { key: 'rebuy', label: '再次购买', type: 'primary' }
      )
      break
    case 'cancelled':
      actions.push(
        { key: 'rebuy', label: '再次购买', type: 'primary' }
      )
      break
  }
  
  return actions
}

// 获取订单列表
const getOrderList = async (isRefresh = false) => {
  try {
    if (isRefresh) {
      pagination.page = 1
      loading.value = true
    } else if (pagination.page > 1) {
      loadingMore.value = true
    } else {
      loading.value = true
    }

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 800))
    
    let filteredOrders = mockOrders
    
    // 按状态筛选
    if (currentTab.value !== 'all') {
      filteredOrders = mockOrders.filter(order => order.status === currentTab.value)
    }
    
    // 搜索筛选
    if (searchKeyword.value.trim()) {
      const keyword = searchKeyword.value.trim().toLowerCase()
      filteredOrders = filteredOrders.filter(order => 
        order.order_number.toLowerCase().includes(keyword) ||
        order.service_name.toLowerCase().includes(keyword)
      )
    }

    if (isRefresh || pagination.page === 1) {
      orderList.value = filteredOrders
    } else {
      orderList.value = [...orderList.value, ...filteredOrders]
    }

    pagination.total = filteredOrders.length
    pagination.pages = Math.ceil(filteredOrders.length / pagination.per_page)
  } catch (error) {
    console.error('获取订单列表失败:', error)
    uni.showToast({
      title: '获取列表失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
    loadingMore.value = false
    uni.stopPullDownRefresh()
  }
}

// 搜索处理
const handleSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  
  searchTimeout.value = setTimeout(() => {
    pagination.page = 1
    getOrderList(true)
  }, 500)
}

// 清除搜索
const clearSearch = () => {
  searchKeyword.value = ''
  pagination.page = 1
  getOrderList(true)
}

// 切换标签
const switchTab = (tabKey) => {
  if (currentTab.value === tabKey) return
  
  currentTab.value = tabKey
  pagination.page = 1
  getOrderList(true)
}

// 查看订单详情
const viewDetail = (order) => {
  uni.navigateTo({
    url: `/pages/order/detail?id=${order.id}`
  })
}

// 处理订单操作
const handleAction = (actionKey, order) => {
  switch (actionKey) {
    case 'pay':
      // 跳转到支付页面
      uni.navigateTo({
        url: `/pages/order/pay?id=${order.id}`
      })
      break
    case 'cancel':
      uni.showModal({
        title: '取消订单',
        content: '确定要取消这个订单吗？',
        success: (res) => {
          if (res.confirm) {
            // 处理取消订单逻辑
            uni.showToast({
              title: '订单已取消',
              icon: 'success'
            })
            getOrderList(true)
          }
        }
      })
      break
    case 'contact':
      // 联系咨询师
      uni.showToast({
        title: '联系功能开发中',
        icon: 'none'
      })
      break
    case 'evaluate':
      // 跳转到评价页面
      uni.showToast({
        title: '评价功能开发中',
        icon: 'none'
      })
      break
    case 'rebuy':
      // 再次购买
      uni.showToast({
        title: '跳转到服务页面',
        icon: 'none'
      })
      break
  }
}

// 跳转到服务页面
const goToServices = () => {
  uni.switchTab({
    url: '/pages/counselor/index'
  })
}

// 加载更多
const loadMore = () => {
  if (loadingMore.value || !hasMore.value) return
  
  pagination.page++
  getOrderList()
}

// 生命周期
onLoad(() => {
  getOrderList()
})

onShow(() => {
  // 页面显示时刷新数据
  getOrderList(true)
})

onPullDownRefresh(() => {
  getOrderList(true)
})

onReachBottom(() => {
  if (hasMore.value) {
    loadMore()
  }
})
</script>

<style lang="scss" scoped>
// SCSS 变量
$primary-color: #007AFF;
$success-color: #52C41A;
$warning-color: #FA8C16;
$danger-color: #FF3B30;
$text-primary: #1C1C1E;
$text-secondary: #48484A;
$text-tertiary: #8E8E93;
$bg-primary: #FFFFFF;
$bg-secondary: #F2F2F7;
$border-color: #E5E5EA;

.container {
  min-height: 100vh;
  background-color: $bg-secondary;
  padding-bottom: 40rpx;
}

// 搜索区域
.search-section {
  background-color: $bg-primary;
  padding: 20rpx;
  border-bottom: 1rpx solid $border-color;

  .search-bar {
    display: flex;
    align-items: center;
    background-color: $bg-secondary;
    border-radius: 20rpx;
    padding: 20rpx 30rpx;

    .search-input {
      flex: 1;
      font-size: 28rpx;
      color: $text-primary;
      margin: 0 20rpx;
      border: none;
      outline: none;
      background: transparent;

      &::placeholder {
        color: $text-tertiary;
      }
    }

    .clear-btn {
      padding: 8rpx;
      border-radius: 50%;
      background-color: rgba(0, 0, 0, 0.1);
    }
  }
}

// 标签区域
.tabs-section {
  background-color: $bg-primary;
  padding: 0 20rpx;
  border-bottom: 1rpx solid $border-color;

  .tabs {
    display: flex;
    align-items: center;

    .tab-item {
      flex: 1;
      text-align: center;
      padding: 24rpx 0;
      font-size: 28rpx;
      color: $text-secondary;
      position: relative;
      transition: all 0.2s ease;

      &.active {
        color: $primary-color;
        font-weight: 600;

        &::after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 50%;
          transform: translateX(-50%);
          width: 60rpx;
          height: 4rpx;
          background-color: $primary-color;
          border-radius: 2rpx;
        }
      }
    }
  }
}

// 订单列表
.order-list {
  padding: 0 20rpx;

  .order-item {
    background-color: $bg-primary;
    border-radius: 12rpx;
    margin-bottom: 20rpx;
    overflow: hidden;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
    transition: all 0.2s ease;

    &:active {
      transform: scale(0.98);
    }

    .order-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 30rpx 30rpx 20rpx;
      border-bottom: 1rpx solid $border-color;

      .order-info {
        flex: 1;

        .order-number {
          display: block;
          font-size: 28rpx;
          color: $text-primary;
          font-weight: 500;
          margin-bottom: 8rpx;
        }

        .order-time {
          font-size: 24rpx;
          color: $text-tertiary;
        }
      }

      .order-status {
        font-size: 26rpx;
        padding: 8rpx 16rpx;
        border-radius: 20rpx;
        font-weight: 500;

        &.status-pending {
          color: $warning-color;
          background-color: rgba(250, 140, 22, 0.1);
        }

        &.status-paid {
          color: $primary-color;
          background-color: rgba(0, 122, 255, 0.1);
        }

        &.status-completed {
          color: $success-color;
          background-color: rgba(82, 196, 26, 0.1);
        }

        &.status-cancelled {
          color: $text-tertiary;
          background-color: rgba(142, 142, 147, 0.1);
        }
      }
    }

    .order-content {
      padding: 20rpx 30rpx;

      .order-main {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;

        .service-info {
          flex: 1;
          margin-right: 20rpx;

          .service-title {
            font-size: 30rpx;
            font-weight: 600;
            color: $text-primary;
            margin-bottom: 12rpx;
          }

          .service-desc {
            font-size: 24rpx;
            color: $text-secondary;
            margin-bottom: 8rpx;

            &:last-child {
              margin-bottom: 0;
            }
          }
        }

        .order-amount {
          display: flex;
          align-items: baseline;

          .amount-symbol {
            font-size: 24rpx;
            color: $danger-color;
            margin-right: 4rpx;
          }

          .amount-value {
            font-size: 32rpx;
            font-weight: 600;
            color: $danger-color;
          }
        }
      }
    }

    .order-actions {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 20rpx;
      padding: 20rpx 30rpx 30rpx;

      .action-btn {
        padding: 16rpx 32rpx;
        border-radius: 24rpx;
        font-size: 26rpx;
        border: 1rpx solid $border-color;
        transition: all 0.2s ease;

        &.default {
          color: $text-secondary;
          background-color: $bg-primary;

          &:active {
            background-color: $bg-secondary;
          }
        }

        &.primary {
          color: $bg-primary;
          background-color: $primary-color;
          border-color: $primary-color;

          &:active {
            background-color: rgba(0, 122, 255, 0.8);
          }
        }
      }
    }
  }
}

// 空状态
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120rpx 40rpx;

  .empty-icon {
    font-size: 120rpx;
    margin-bottom: 40rpx;
    opacity: 0.3;
  }

  .empty-text {
    font-size: 28rpx;
    color: $text-tertiary;
    margin-bottom: 40rpx;
    text-align: center;
  }

  .empty-btn {
    background: linear-gradient(135deg, $primary-color 0%, #5856D6 100%);
    color: #FFFFFF;
    padding: 20rpx 40rpx;
    border-radius: 25rpx;
    font-size: 28rpx;
    font-weight: 500;

    &:active {
      transform: scale(0.95);
    }
  }
}

// 加载状态
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80rpx 40rpx;

  .loading-text {
    font-size: 28rpx;
    color: $text-tertiary;
    margin-top: 20rpx;
  }
}

// 加载更多
.load-more {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40rpx;

  .load-more-text {
    font-size: 28rpx;
    color: $text-tertiary;
  }
}
</style>
