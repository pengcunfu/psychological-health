<template>
  <view class="container">
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-bar">
        <u-icon name="search" size="20" color="#999"></u-icon>
        <input 
          v-model="searchKeyword" 
          placeholder="搜索咨询人姓名或电话" 
          class="search-input"
          @input="handleSearch"
          @confirm="handleSearch"
        />
        <view v-if="searchKeyword" class="clear-btn" @click="clearSearch">
          <u-icon name="close" size="16" color="#999"></u-icon>
        </view>
      </view>
    </view>

    <!-- 添加咨询人按钮 -->
    <view class="add-section">
      <view class="add-btn" @click="addConsultant">
        <u-icon name="plus" size="20" color="#007AFF"></u-icon>
        <text class="add-text">添加咨询人</text>
      </view>
    </view>

    <!-- 咨询人列表 -->
    <view class="consultant-list" v-if="consultantList.length > 0">
      <view 
        v-for="consultant in consultantList" 
        :key="consultant.id"
        class="consultant-item"
        @click="viewDetail(consultant)"
      >
        <view class="consultant-info">
          <view class="consultant-header">
            <text class="consultant-name">{{ consultant.real_name }}</text>
            <view v-if="consultant.is_default" class="default-tag">默认</view>
          </view>
          
          <view class="consultant-details">
            <text class="detail-item">{{ formatGender(consultant.gender) }}</text>
            <text class="detail-item" v-if="consultant.birth_year && consultant.birth_month">
              {{ consultant.birth_year }}年{{ consultant.birth_month }}月
            </text>
            <text class="detail-item">{{ formatPhone(consultant.phone) }}</text>
          </view>
          
          <view class="consultant-emergency" v-if="consultant.emergency_name">
            <text class="emergency-label">紧急联系人：</text>
            <text class="emergency-info">
              {{ consultant.emergency_name }}
              ({{ formatRelationship(consultant.emergency_relationship) }})
            </text>
          </view>
        </view>

        <view class="consultant-actions" @click.stop="">
          <view class="action-btn" @click="editConsultant(consultant)">
            <u-icon name="edit-pen" size="16" color="#007AFF"></u-icon>
          </view>
          <view 
            class="action-btn" 
            @click="setDefault(consultant)"
            v-if="!consultant.is_default"
          >
            <u-icon name="star" size="16" color="#FA8C16"></u-icon>
          </view>
          <view class="action-btn danger" @click="deleteConsultant(consultant)">
            <u-icon name="trash" size="16" color="#FF3B30"></u-icon>
          </view>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view class="empty-state" v-else-if="!loading">
      <view class="empty-icon">👤</view>
      <text class="empty-text">{{ searchKeyword ? '没有找到相关咨询人' : '还没有添加咨询人' }}</text>
      <view class="empty-btn" @click="addConsultant" v-if="!searchKeyword">
        <text>立即添加</text>
      </view>
    </view>

    <!-- 加载状态 -->
    <view class="loading-state" v-if="loading">
      <u-loading-icon mode="spinner"></u-loading-icon>
      <text class="loading-text">加载中...</text>
    </view>

    <!-- 分页加载更多 -->
    <view class="load-more" v-if="consultantList.length > 0 && hasMore" @click="loadMore">
      <text class="load-more-text">{{ loadingMore ? '加载中...' : '加载更多' }}</text>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { onLoad, onShow, onPullDownRefresh, onReachBottom } from '@dcloudio/uni-app'
import { consultantAPI } from '@/api/consultant'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

// 响应式数据
const searchKeyword = ref('')
const consultantList = ref([])
const loading = ref(false)
const loadingMore = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const searchTimeout = ref(null)

// 分页参数
const pagination = reactive({
  page: 1,
  per_page: 10,
  total: 0
})

// 计算属性
const hasMore = computed(() => pagination.page < totalPages.value)

// 关系映射
const relationshipMap = {
  'self': '本人',
  'spouse': '配偶',
  'child': '子女',
  'parent': '父母',
  'sibling': '兄弟姐妹',
  'friend': '朋友',
  'other': '其他'
}

// 方法
const formatGender = (gender) => {
  return gender === 'male' ? '男' : gender === 'female' ? '女' : ''
}

const formatPhone = (phone) => {
  if (!phone) return ''
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

const formatRelationship = (relationship) => {
  return relationshipMap[relationship] || relationship
}

// 获取咨询人列表
const getConsultantList = async (isRefresh = false) => {
  try {
    if (isRefresh) {
      pagination.page = 1
      loading.value = true
    } else if (pagination.page > 1) {
      loadingMore.value = true
    } else {
      loading.value = true
    }

    const params = {
      page: pagination.page,
      per_page: pagination.per_page
    }

    if (searchKeyword.value.trim()) {
      params.keyword = searchKeyword.value.trim()
    }

    const result = await consultantAPI.getConsultants(params)

    if (result.success && result.data) {
      const newData = result.data.list || []
      
      if (isRefresh || pagination.page === 1) {
        consultantList.value = newData
      } else {
        consultantList.value = [...consultantList.value, ...newData]
      }

      pagination.total = result.data.total || 0
      totalPages.value = result.data.pages || 1
    }
  } catch (error) {
    console.error('获取咨询人列表失败:', error)
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
    getConsultantList(true)
  }, 500)
}

// 清除搜索
const clearSearch = () => {
  searchKeyword.value = ''
  pagination.page = 1
  getConsultantList(true)
}

// 添加咨询人
const addConsultant = () => {
  uni.navigateTo({
    url: '/pages/consultant/create'
  })
}

// 编辑咨询人
const editConsultant = (consultant) => {
  uni.navigateTo({
    url: `/pages/consultant/create?id=${consultant.id}`
  })
}

// 查看详情
const viewDetail = (consultant) => {
  // 可以实现查看详情页面，这里先用编辑代替
  editConsultant(consultant)
}

// 设置为默认咨询人
const setDefault = async (consultant) => {
  try {
    uni.showModal({
      title: '提示',
      content: `确定将"${consultant.real_name}"设置为默认咨询人吗？`,
      success: async (res) => {
        if (res.confirm) {
          uni.showLoading({ title: '设置中...' })
          
          const result = await consultantAPI.setDefaultConsultant(consultant.id)
          
          if (result.success) {
            uni.showToast({
              title: '设置成功',
              icon: 'success'
            })
            // 刷新列表
            getConsultantList(true)
          } else {
            uni.showToast({
              title: result.message || '设置失败',
              icon: 'none'
            })
          }
          uni.hideLoading()
        }
      }
    })
  } catch (error) {
    uni.hideLoading()
    console.error('设置默认咨询人失败:', error)
    uni.showToast({
      title: '设置失败',
      icon: 'none'
    })
  }
}

// 删除咨询人
const deleteConsultant = (consultant) => {
  uni.showModal({
    title: '删除确认',
    content: `确定要删除咨询人"${consultant.real_name}"吗？此操作不可恢复。`,
    confirmColor: '#FF3B30',
    success: async (res) => {
      if (res.confirm) {
        try {
          uni.showLoading({ title: '删除中...' })
          
          const result = await consultantAPI.deleteConsultant(consultant.id)
          
          if (result.success) {
            uni.showToast({
              title: '删除成功',
              icon: 'success'
            })
            // 刷新列表
            getConsultantList(true)
          } else {
            uni.showToast({
              title: result.message || '删除失败',
              icon: 'none'
            })
          }
        } catch (error) {
          console.error('删除咨询人失败:', error)
          uni.showToast({
            title: '删除失败',
            icon: 'none'
          })
        } finally {
          uni.hideLoading()
        }
      }
    }
  })
}

// 加载更多
const loadMore = () => {
  if (loadingMore.value || !hasMore.value) return
  
  pagination.page++
  getConsultantList()
}

// 生命周期
onLoad(() => {
  getConsultantList()
})

onShow(() => {
  // 页面显示时刷新数据
  getConsultantList(true)
})

onPullDownRefresh(() => {
  getConsultantList(true)
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
$danger-color: #FF3B30;
$warning-color: #FA8C16;
$success-color: #52C41A;
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

// 添加按钮区域
.add-section {
  padding: 20rpx;

  .add-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: $bg-primary;
    border: 2rpx dashed $primary-color;
    border-radius: 12rpx;
    padding: 30rpx;
    gap: 12rpx;

    .add-text {
      font-size: 28rpx;
      color: $primary-color;
      font-weight: 500;
    }

    &:active {
      background-color: rgba(0, 122, 255, 0.05);
    }
  }
}

// 咨询人列表
.consultant-list {
  padding: 0 20rpx;

  .consultant-item {
    background-color: $bg-primary;
    border-radius: 12rpx;
    margin-bottom: 20rpx;
    padding: 30rpx;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
    transition: all 0.2s ease;

    &:active {
      background-color: #F8F9FA;
      transform: scale(0.98);
    }

    .consultant-info {
      flex: 1;
      margin-right: 20rpx;

      .consultant-header {
        display: flex;
        align-items: center;
        margin-bottom: 12rpx;

        .consultant-name {
          font-size: 32rpx;
          font-weight: 600;
          color: $text-primary;
          margin-right: 16rpx;
        }

        .default-tag {
          background: linear-gradient(135deg, $warning-color 0%, #FFD666 100%);
          color: #FFFFFF;
          font-size: 20rpx;
          padding: 4rpx 12rpx;
          border-radius: 12rpx;
          font-weight: 500;
        }
      }

      .consultant-details {
        display: flex;
        align-items: center;
        margin-bottom: 8rpx;
        gap: 20rpx;

        .detail-item {
          font-size: 26rpx;
          color: $text-secondary;
        }
      }

      .consultant-emergency {
        display: flex;
        align-items: center;

        .emergency-label {
          font-size: 24rpx;
          color: $text-tertiary;
        }

        .emergency-info {
          font-size: 24rpx;
          color: $text-secondary;
        }
      }
    }

    .consultant-actions {
      display: flex;
      align-items: center;
      gap: 20rpx;

      .action-btn {
        width: 60rpx;
        height: 60rpx;
        border-radius: 50%;
        background-color: $bg-secondary;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;

        &:active {
          transform: scale(0.9);
        }

        &.danger {
          background-color: rgba(255, 59, 48, 0.1);
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
