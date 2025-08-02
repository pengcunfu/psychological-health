<template>
  <view class="container tab-page">
    <view class="search-bar">
      <u-search
        v-model="searchKeyword"
        placeholder="搜索咨询师"
        :show-action="false"
        @search="handleSearch"
        @custom="handleSearch"
      ></u-search>
    </view>

    <view class="filter-bar">
      <view 
        class="filter-item" 
        :class="{ active: activeFilter === 'all' }" 
        @click="setFilter('all')"
      >
        全部
      </view>
      <view 
        class="filter-item" 
        :class="{ active: activeFilter === 'rating' }" 
        @click="setFilter('rating')"
      >
        评分最高
      </view>
      <view 
        class="filter-item" 
        :class="{ active: activeFilter === 'price-asc' }" 
        @click="setFilter('price-asc')"
      >
        价格从低到高
      </view>
      <view 
        class="filter-item" 
        :class="{ active: activeFilter === 'price-desc' }" 
        @click="setFilter('price-desc')"
      >
        价格从高到低
      </view>
    </view>

    <view class="counselor-list">
      <view 
        class="counselor-card" 
        v-for="(item, index) in counselorList" 
        :key="index"
        @click="navigateToDetail(item.id)"
      >
        <view class="counselor-header">
          <u-avatar :src="item.avatar || '/static/images/default-avatar.png'" size="120"></u-avatar>
          <view class="counselor-info">
            <view class="counselor-name-row">
              <text class="counselor-name">{{ item.name }}</text>
              <text class="counselor-title">{{ item.title }}</text>
            </view>
            <view class="counselor-rating">
              <u-icon name="star-fill" color="#faad14" size="24"></u-icon>
              <text class="rating-text">{{ item.rating }}</text>
              <text class="consultation-count">{{ item.consultation_count }}次咨询</text>
            </view>
            <view class="counselor-tags">
              <text class="tag" v-for="(tag, tagIndex) in item.tags" :key="tagIndex">{{ tag }}</text>
            </view>
          </view>
        </view>
        <view class="counselor-content">
          <text class="counselor-intro text-ellipsis-2">{{ item.introduction || '暂无简介' }}</text>
        </view>
        <view class="counselor-footer">
          <text class="price">¥{{ item.price }}/次</text>
          <button class="appointment-btn">立即预约</button>
        </view>
      </view>
    </view>

    <u-loadmore :status="loadMoreStatus" />
  </view>
</template>

<script>
import { ref, reactive } from 'vue'
import { onLoad, onReachBottom } from '@dcloudio/uni-app'
import { request } from '@/utils/request'

export default {
  setup() {
    const searchKeyword = ref('')
    const activeFilter = ref('all')
    const counselorList = ref([])
    const loadMoreStatus = ref('loading')
    
    const pagination = reactive({
      page: 1,
      per_page: 10,
      total: 0,
      total_pages: 0
    })
    
    // 获取咨询师列表
    const fetchCounselors = async (reset = false) => {
      if (reset) {
        pagination.page = 1
        counselorList.value = []
      }
      
      loadMoreStatus.value = 'loading'
      
      try {
        // 构建查询参数
        const params = {
          page: pagination.page,
          per_page: pagination.per_page,
          keyword: searchKeyword.value
        }
        
        // 根据筛选条件添加排序参数
        switch (activeFilter.value) {
          case 'rating':
            params.sort_by = 'rating'
            params.sort_order = 'desc'
            break
          case 'price-asc':
            params.sort_by = 'price'
            params.sort_order = 'asc'
            break
          case 'price-desc':
            params.sort_by = 'price'
            params.sort_order = 'desc'
            break
        }
        
        const res = await request({
          url: '/counselor',
          method: 'GET',
          data: params
        })
        
        if (res.code === 200 && res.success) {
          // 解析返回的咨询师列表
          const newList = res.data.counselors || []
          
          // 处理标签字段，将字符串转为数组
          newList.forEach(item => {
            if (typeof item.tags === 'string') {
              item.tags = item.tags.split(',').filter(tag => tag.trim() !== '')
            } else if (!Array.isArray(item.tags)) {
              item.tags = []
            }
          })
          
          // 更新列表和分页信息
          counselorList.value = reset ? newList : [...counselorList.value, ...newList]
          pagination.total = res.data.total || 0
          pagination.total_pages = res.data.pages || 0
          
          // 更新加载更多状态
          loadMoreStatus.value = pagination.page >= pagination.total_pages ? 'nomore' : 'loadmore'
        } else {
          loadMoreStatus.value = 'loadmore'
          uni.showToast({
            title: res.message || '获取咨询师列表失败',
            icon: 'none'
          })
        }
      } catch (error) {
        console.error('获取咨询师列表失败:', error)
        loadMoreStatus.value = 'loadmore'
        uni.showToast({
          title: '获取咨询师列表失败，请稍后重试',
          icon: 'none'
        })
      }
    }
    
    // 搜索处理
    const handleSearch = () => {
      fetchCounselors(true)
    }
    
    // 筛选处理
    const setFilter = (filter) => {
      activeFilter.value = filter
      fetchCounselors(true)
    }
    
    // 跳转到详情页
    const navigateToDetail = (id) => {
      uni.navigateTo({
        url: `/pages/counselor/detail/index?id=${id}`
      })
    }
    
    // 页面加载
    onLoad(() => {
      fetchCounselors()
    })
    
    // 下拉加载更多
    onReachBottom(() => {
      if (loadMoreStatus.value === 'loadmore') {
        pagination.page++
        fetchCounselors()
      }
    })
    
    return {
      searchKeyword,
      activeFilter,
      counselorList,
      loadMoreStatus,
      handleSearch,
      setFilter,
      navigateToDetail
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

.search-bar {
  padding: 20rpx 30rpx;
  background-color: #fff;
}

.filter-bar {
  display: flex;
  background-color: #fff;
  padding: 0 20rpx;
  margin-bottom: 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.filter-item {
  padding: 20rpx 30rpx;
  font-size: 28rpx;
  color: #666;
  position: relative;
}

.filter-item.active {
  color: #4A90E2;
  font-weight: bold;
}

.filter-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40rpx;
  height: 4rpx;
  background-color: #4A90E2;
}

.counselor-list {
  padding: 0 30rpx;
}

.counselor-card {
  background-color: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.counselor-header {
  display: flex;
  margin-bottom: 20rpx;
}

.counselor-info {
  flex: 1;
  margin-left: 20rpx;
}

.counselor-name-row {
  display: flex;
  align-items: center;
  margin-bottom: 10rpx;
}

.counselor-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-right: 10rpx;
}

.counselor-title {
  font-size: 24rpx;
  color: #666;
  background-color: #f5f7fa;
  padding: 4rpx 10rpx;
  border-radius: 4rpx;
}

.counselor-rating {
  display: flex;
  align-items: center;
  margin-bottom: 10rpx;
}

.rating-text {
  font-size: 24rpx;
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

.counselor-content {
  margin-bottom: 20rpx;
}

.counselor-intro {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.counselor-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  font-size: 36rpx;
  color: #f5222d;
  font-weight: bold;
}

.appointment-btn {
  background-color: #4A90E2;
  color: #fff;
  font-size: 28rpx;
  padding: 10rpx 30rpx;
  border-radius: 30rpx;
  border: none;
}
</style> 