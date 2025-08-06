<template>
  <view class="container tab-page">
    <!-- 顶部导航栏 -->
    <view class="header">
      <view class="back-button" @click="goBack">
        <up-icon name="arrow-left" size="20" color="#333"></up-icon>
      </view>
      <view class="header-title">咨询预约</view>
      <view class="search-button" @click="handleSearchClick">
        <up-icon name="search" size="20" color="#333"></up-icon>
      </view>
    </view>

    <!-- 标签栏 -->
    <view class="tabs">
      <view class="tab active">全部咨询师</view>
      <view class="tab">我的预约</view>
    </view>

    <!-- 筛选栏 -->
    <view class="filter-bar">
      <view class="filter-item">
        <text>专业领域</text>
        <up-icon name="arrow-down" size="12" color="#999"></up-icon>
      </view>
      <view class="filter-item">
        <text>价格区间</text>
        <up-icon name="arrow-down" size="12" color="#999"></up-icon>
      </view>
      <view class="filter-item">
        <text>综合排序</text>
        <up-icon name="arrow-down" size="12" color="#999"></up-icon>
      </view>
    </view>

    <!-- 咨询师列表 -->
    <view class="counselor-list">
      <CounselorCard 
        v-for="(item, index) in counselorList" 
        :key="item.id || index"
        :counselor="item"
        @click="handleCounselorClick"
      />
    </view>

    <!-- 空状态 -->
    <view v-if="!loading && counselorList.length === 0" class="empty-state">
      <view class="empty-content">
        <up-icon name="search" size="60" color="#ccc"></up-icon>
        <text class="empty-title">暂未找到合适的咨询师</text>
        <text class="empty-subtitle">试试调整搜索条件或筛选选项</text>
        <up-button
            text="重新搜索"
            type="primary"
            size="normal"
            @click="fetchCounselors(true)"
            :customStyle="{
              marginTop: '30rpx',
              width: '160rpx',
              borderRadius: '22rpx',
              background: '#4A90E2'
            }"
        ></up-button>
      </view>
    </view>

    <!-- 加载更多 -->
    <view class="load-more-container">
      <up-loadmore :status="loadMoreStatus" @loadmore="loadMore" 
        :loading-text="'正在加载更多咨询师...'"
        :loadmore-text="'上拉加载更多'"
        :nomore-text="'已加载全部咨询师'"
        icon-size="20"
        :margin-top="20"
        :margin-bottom="20"
      />
    </view>
  </view>
</template>

<script setup>
import {ref, reactive, computed} from 'vue'
import {onLoad, onReachBottom} from '@dcloudio/uni-app'
import {counselorAPI} from '@/api/counselor'
import CounselorCard from '@/components/CounselorCard.vue'

// 搜索关键词
const searchKeyword = ref('')

// 当前选中的标签页 - 确保是数字类型
const currentTab = ref(0)

// 标签页列表 - 确保正确的数据结构
const tabList = ref([
  {name: '全部'},
  {name: '评分最高'},
  {name: '价格最低'},
  {name: '价格最高'}
])

// 咨询师列表
const counselorList = ref([])

// 加载状态
const loading = ref(false)
const loadMoreStatus = ref('loadmore')

// 分页信息
const pagination = reactive({
  page: 1,
  per_page: 10,
  total: 0,
  total_pages: 0
})

// 当前筛选条件
const currentFilter = computed(() => {
  const filters = ['all', 'rating', 'price-asc', 'price-desc']
  const index = Math.max(0, Math.min(currentTab.value || 0, filters.length - 1))
  return filters[index] || 'all'
})

// 获取专业领域
const getSpecialties = (item) => {
  if (item.specialties && item.specialties.length > 0) {
    return item.specialties
  }
  return ['心理咨询', '情感支持', '焦虑抑郁', '人际关系']
}

// 获取专长描述文本
const getSpecialtyText = (item) => {
  const specialties = getSpecialties(item)
  return specialties.slice(0, 3).join('、')
}

// 返回上一页
const goBack = () => {
  uni.navigateBack()
}

// 搜索按钮点击
const handleSearchClick = () => {
  uni.navigateTo({
    url: '/pages/search'
  })
}

// 获取咨询师列表
const fetchCounselors = async (reset = false) => {
  if (reset) {
    pagination.page = 1
    counselorList.value = []
  }

  loading.value = true
  loadMoreStatus.value = 'loading'

  try {
    // 构建查询参数
    const params = {
      page: pagination.page,
      per_page: pagination.per_page
    }

    // 添加搜索关键词
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }

    // 根据筛选条件添加排序参数
    switch (currentFilter.value) {
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
      default:
        // 默认按创建时间排序
        params.sort_by = 'created_at'
        params.sort_order = 'desc'
        break
    }

    console.log('获取咨询师列表参数:', params)

    const res = await counselorAPI.getCounselors(params)

    console.log('咨询师API响应:', res)

    if (res.code === 200 && res.success && res.data) {
      // 处理咨询师数据
      let newList = res.data.list || []

      // 数据处理和字段映射
      newList = newList.map(item => {
        const processedItem = {
          ...item,
          // 字段映射和默认值处理
          id: item.id,
          name: item.name || '未知咨询师',
          avatar: item.avatar || '/static/images/default-avatar.png',
          title: item.title || '心理咨询师',
          professional_title: item.title || '心理咨询师',
          rating: parseFloat(item.rating) || 4.8,
          consultation_count: parseInt(item.consultation_count) || 0,
          price: parseFloat(item.price) || 300,
          consultation_fee: parseFloat(item.price) || 300,
          introduction: item.introduction || '专业心理咨询师，致力于为您提供优质的心理健康服务',
          description: item.introduction || '专业心理咨询师，致力于为您提供优质的心理健康服务',
          // 处理专业领域 - 将tags字段映射为specialties
          specialties: processSpecialties(item.tags || []),
          tags: item.tags || [],
          expertise: item.tags || []
        }
        return processedItem
      })

      // 如果后端不支持排序，前端进行排序
      if (currentFilter.value !== 'all') {
        newList = sortCounselors(newList, currentFilter.value)
      }

      // 更新列表
      counselorList.value = reset ? newList : [...counselorList.value, ...newList]

      // 更新分页信息
      pagination.total = res.data.total || 0
      pagination.total_pages = res.data.pages || Math.ceil((res.data.total || 0) / pagination.per_page)

      // 更新加载更多状态
      loadMoreStatus.value = pagination.page >= pagination.total_pages ? 'nomore' : 'loadmore'

      console.log('咨询师列表加载成功，共', newList.length, '条数据')
    } else {
      console.log('API返回数据格式异常:', res)

      // 设置为空数组，显示空状态
      if (reset) {
        counselorList.value = []
      }
      loadMoreStatus.value = 'nomore'
    }
  } catch (error) {
    console.error('获取咨询师列表失败:', error)

    // 设置为空数组，显示空状态
    if (reset) {
      counselorList.value = []
    }

    loadMoreStatus.value = 'loadmore'
    uni.showToast({
      title: '获取咨询师列表失败，请稍后重试',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 前端排序函数（作为后端排序的备选方案）
const sortCounselors = (list, sortType) => {
  const sortedList = [...list]
  
  switch (sortType) {
    case 'rating':
      return sortedList.sort((a, b) => {
        const ratingA = parseFloat(a.rating) || 0
        const ratingB = parseFloat(b.rating) || 0
        return ratingB - ratingA // 降序：评分高的在前
      })
    case 'price-asc':
      return sortedList.sort((a, b) => {
        const priceA = parseFloat(a.price) || 0
        const priceB = parseFloat(b.price) || 0
        return priceA - priceB // 升序：价格低的在前
      })
    case 'price-desc':
      return sortedList.sort((a, b) => {
        const priceA = parseFloat(a.price) || 0
        const priceB = parseFloat(b.price) || 0
        return priceB - priceA // 降序：价格高的在前
      })
    default:
      return sortedList
  }
}

// 处理专业领域数据
const processSpecialties = (tags) => {
  if (Array.isArray(tags) && tags.length > 0) {
    return tags
  }
  if (typeof tags === 'string' && tags.trim()) {
    return tags.split(',').map(s => s.trim()).filter(s => s)
  }
  // 如果没有标签，返回默认标签
  return ['心理咨询', '情感支持']
}

// 标签页切换处理
const handleTabChange = (index) => {
  console.log('切换到标签页:', index, tabList.value[index]?.name)
  // 确保index是数字类型
  const tabIndex = typeof index === 'object' ? index.index : index
  currentTab.value = Number(tabIndex)
  console.log('当前筛选条件:', currentFilter.value)
  fetchCounselors(true)
}

// 搜索处理
const handleSearch = () => {
  fetchCounselors(true)
}

// 处理咨询师卡片点击
const handleCounselorClick = (counselor) => {
  uni.navigateTo({
    url: `/pages/counselor/detail?id=${counselor.id}`
  })
}

// 跳转到详情页
const navigateToDetail = (id) => {
  uni.navigateTo({
    url: `/pages/counselor/detail?id=${id}`
  })
}

// 预约处理
const handleAppointment = (counselor) => {
  uni.showToast({
    title: `预约${counselor.name}`,
    icon: 'none'
  })
  // TODO: 实现预约逻辑
}

// 加载更多
const loadMore = () => {
  if (loadMoreStatus.value === 'loadmore') {
    pagination.page++
    fetchCounselors()
  }
}

// 页面加载
onLoad(() => {
  console.log('页面加载，初始化咨询师列表')
  // 确保初始状态正确
  currentTab.value = 0
  fetchCounselors(true)
})

// 下拉加载更多
onReachBottom(() => {
  loadMore()
})
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 30rpx;
}

// 顶部导航栏
.header {
  padding: 30rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1rpx solid #f0f0f0;
}

.header-title {
  font-size: 36rpx;
  font-weight: bold;
  flex: 1;
  text-align: center;
  color: #333;
}

.back-button, .search-button {
  width: 48rpx;
  height: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

// 标签栏
.tabs {
  display: flex;
  background: #fff;
  border-bottom: 1rpx solid #f0f0f0;
}

.tab {
  flex: 1;
  text-align: center;
  padding: 24rpx 0;
  font-size: 28rpx;
  color: #666;
  position: relative;
}

.tab.active {
  color: #4A90E2;
  font-weight: bold;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40rpx;
  height: 6rpx;
  background: #4A90E2;
  border-radius: 3rpx;
}

// 筛选栏
.filter-bar {
  display: flex;
  padding: 20rpx 30rpx;
  background: #fff;
  border-bottom: 1rpx solid #f0f0f0;
}

.filter-item {
  display: flex;
  align-items: center;
  margin-right: 30rpx;
  font-size: 24rpx;
  color: #666;
}

.filter-item text {
  margin-right: 8rpx;
}

// 咨询师列表
.counselor-list {
  padding: 0;
}

// 空状态
.empty-state {
  padding: 80rpx 40rpx;
  text-align: center;
}

.empty-content {
  background: #fff;
  border-radius: 12rpx;
  padding: 40rpx 30rpx;
}

.empty-title {
  font-size: 28rpx;
  color: #333;
  margin: 20rpx 0 8rpx;
  display: block;
}

.empty-subtitle {
  font-size: 24rpx;
  color: #999;
  display: block;
}

// 加载更多
.load-more-container {
  padding: 0 0 20rpx;
}
</style> 