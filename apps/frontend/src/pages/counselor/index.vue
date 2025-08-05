<template>
  <view class="container tab-page">
    <view class="search-bar">
      <up-search
          v-model="searchKeyword"
          placeholder="搜索咨询师"
          :show-action="false"
          @search="handleSearch"
          @custom="handleSearch"
      ></up-search>
    </view>

    <!-- 使用uViewPlus Tabs组件 -->
    <up-tabs
        :list="tabList"
        :current="currentTab"
        @change="handleTabChange"
        :activeStyle="{
        color: '#4A90E2',
        fontWeight: 'bold',
        transform: 'scale(1.05)'
      }"
        :inactiveStyle="{
        color: '#666666'
      }"
        lineWidth="30"
        lineColor="#4A90E2"
        lineHeight="4"
        itemStyle="padding-left: 15px; padding-right: 15px; height: 50px;"
    />

    <!-- 咨询师列表 -->
    <up-list v-if="!loading && counselorList.length > 0">
      <up-list-item
          v-for="(item, index) in counselorList"
          :key="item.id || index"
          @click="navigateToDetail(item.id)"
      >
        <view class="counselor-card">
          <view class="counselor-header">
            <up-avatar :src="item.avatar || '/static/images/default-avatar.png'" size="120"></up-avatar>
            <view class="counselor-info">
              <view class="counselor-name-row">
                <text class="counselor-name">{{ item.name || '未知咨询师' }}</text>
                <text class="counselor-title">{{ item.title || item.professional_title || '心理咨询师' }}</text>
              </view>
              <view class="counselor-rating">
                <up-icon name="star-fill" color="#faad14" size="24"></up-icon>
                <text class="rating-text">{{ item.rating || '4.8' }}</text>
                <text class="consultation-count">{{ item.consultation_count || 0 }}次咨询</text>
              </view>
              <view class="counselor-tags" v-if="item.specialties && item.specialties.length > 0">
                <text class="tag" v-for="(tag, tagIndex) in item.specialties.slice(0, 3)" :key="tagIndex">{{
                    tag
                  }}
                </text>
              </view>
              <view class="counselor-tags" v-else>
                <text class="tag">心理咨询</text>
                <text class="tag">情感支持</text>
              </view>
            </view>
          </view>
          <view class="counselor-content">
            <text class="counselor-intro text-ellipsis-2">
              {{ item.introduction || item.description || '专业心理咨询师，致力于为您提供优质的心理健康服务' }}
            </text>
          </view>
          <view class="counselor-footer">
            <text class="price">¥{{ item.price || item.consultation_fee || 300 }}/次</text>
            <up-button
                text="立即预约"
                type="primary"
                size="small"
                @click.stop="handleAppointment(item)"
                :customStyle="{
                backgroundColor: '#4A90E2',
                borderColor: '#4A90E2',
                borderRadius: '30rpx',
                height: '60rpx',
                fontSize: '28rpx'
              }"
            ></up-button>
          </view>
        </view>
      </up-list-item>
    </up-list>

    <!-- 空状态 -->
    <view v-if="!loading && counselorList.length === 0" class="empty-state">
      <up-empty
          text="暂无咨询师数据"
          icon="https://cdn.uviewui.com/uview/empty/list.png"
          iconSize="120"
          textSize="14"
          textColor="#999999"
          marginTop="80"
      >
        <template v-slot:bottom>
          <up-button
              text="刷新重试"
              type="primary"
              size="small"
              @click="fetchCounselors(true)"
              :customStyle="{
              marginTop: '20rpx',
              width: '200rpx'
            }"
          ></up-button>
        </template>
      </up-empty>
    </view>

    <!-- 加载更多 -->
    <up-loadmore :status="loadMoreStatus" @loadmore="loadMore"/>
  </view>
</template>

<script setup>
import {ref, reactive, computed} from 'vue'
import {onLoad, onReachBottom} from '@dcloudio/uni-app'
import {counselorAPI} from '@/api/counselor'

// 搜索关键词
const searchKeyword = ref('')

// 当前选中的标签页
const currentTab = ref(0)

// 标签页列表
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
  return filters[currentTab.value] || 'all'
})

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
          rating: item.rating || 4.8,
          consultation_count: item.consultation_count || 0,
          price: item.price || 300,
          consultation_fee: item.price || 300,
          introduction: item.introduction || '专业心理咨询师，致力于为您提供优质的心理健康服务',
          description: item.introduction || '专业心理咨询师，致力于为您提供优质的心理健康服务',
          // 处理专业领域 - 将tags字段映射为specialties
          specialties: processSpecialties(item.tags || []),
          tags: item.tags || [],
          expertise: item.tags || []
        }
        return processedItem
      })

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
  currentTab.value = index
  fetchCounselors(true)
}

// 搜索处理
const handleSearch = () => {
  fetchCounselors(true)
}

// 跳转到详情页
const navigateToDetail = (id) => {
  uni.navigateTo({
    url: `/pages/counselor/detail/index?id=${id}`
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
  fetchCounselors()
})

// 下拉加载更多
onReachBottom(() => {
  loadMore()
})
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
  margin-bottom: 20rpx;
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
  transition: transform 0.2s ease;
}

.counselor-card:active {
  transform: scale(0.98);
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
  gap: 8rpx;
}

.tag {
  font-size: 22rpx;
  color: #4A90E2;
  background-color: rgba(74, 144, 226, 0.1);
  padding: 4rpx 8rpx;
  border-radius: 4rpx;
}

.counselor-content {
  margin-bottom: 20rpx;
}

.counselor-intro {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.text-ellipsis-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 50rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
  margin-top: 20rpx;
}
</style> 