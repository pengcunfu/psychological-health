<template>
  <view class="container tab-page">
    <!-- 顶部导航栏 -->
    <view class="header">
      <view class="back-button" @click="goBack">
        <up-icon name="arrow-left" size="20" color="#333"></up-icon>
      </view>
      <view class="header-title">心理测评</view>
      <view class="search-button" @click="handleSearchClick">
        <up-icon name="search" size="20" color="#333"></up-icon>
      </view>
    </view>

    <!-- 标签栏 -->
    <view class="tabs">
      <view 
        v-for="(tab, index) in tabList" 
        :key="index"
        class="tab"
        :class="{ active: currentTab === index }"
        @click="handleTabChange(index)"
      >
        {{ tab.name }}
      </view>
    </view>

    <!-- 筛选栏 -->
    <view class="filter-bar">
      <view class="filter-item" @click="showCategoryFilter">
        <text>{{ currentCategory || '全部分类' }}</text>
        <up-icon name="arrow-down" size="12" color="#999"></up-icon>
      </view>
      <view class="filter-item" @click="showDifficultyFilter">
        <text>{{ currentDifficulty ? getDifficultyText(currentDifficulty) : '全部难度' }}</text>
        <up-icon name="arrow-down" size="12" color="#999"></up-icon>
      </view>
      <view class="filter-item" @click="showPriceFilter">
        <text>{{ currentPriceFilter || '全部价格' }}</text>
        <up-icon name="arrow-down" size="12" color="#999"></up-icon>
      </view>
    </view>

    <!-- 测评列表 -->
    <view class="assessment-list">
      <AssessmentCard 
        v-for="(item, index) in assessmentList" 
        :key="item.id || index"
        :assessment="item"
        @click="handleAssessmentClick"
      />
    </view>

    <!-- 空状态 -->
    <view v-if="!loading && assessmentList.length === 0" class="empty-state">
      <view class="empty-content">
        <up-icon name="file-text" size="60" color="#ccc"></up-icon>
        <text class="empty-title">暂无相关测评</text>
        <text class="empty-subtitle">试试调整搜索条件或筛选选项</text>
        <up-button
            text="重新搜索"
            type="primary"
            size="normal"
            @click="fetchAssessments(true)"
            :customStyle="{
              marginTop: '30rpx',
              width: '160rpx',
              borderRadius: '22rpx',
              background: '#52c41a'
            }"
        ></up-button>
      </view>
    </view>

    <!-- 加载更多 -->
    <view class="load-more-container">
      <up-loadmore :status="loadMoreStatus" @loadmore="loadMore" 
        :loading-text="'正在加载更多测评...'"
        :loadmore-text="'上拉加载更多'"
        :nomore-text="'已加载全部测评'"
        icon-size="20"
        :margin-top="20"
        :margin-bottom="20"
      />
    </view>

    <!-- 分类筛选弹窗 -->
    <up-popup v-model:show="categoryFilterVisible" mode="bottom" :round="10">
      <view class="filter-popup">
        <view class="filter-header">
          <text class="filter-title">选择分类</text>
          <up-icon name="close" size="20" color="#999" @click="categoryFilterVisible = false"></up-icon>
        </view>
        <view class="filter-options">
          <view 
            v-for="category in categoryOptions" 
            :key="category.value"
            class="filter-option"
            :class="{ active: currentCategory === category.value }"
            @click="selectCategory(category.value)"
          >
            {{ category.label }}
          </view>
        </view>
      </view>
    </up-popup>

    <!-- 难度筛选弹窗 -->
    <up-popup v-model:show="difficultyFilterVisible" mode="bottom" :round="10">
      <view class="filter-popup">
        <view class="filter-header">
          <text class="filter-title">选择难度</text>
          <up-icon name="close" size="20" color="#999" @click="difficultyFilterVisible = false"></up-icon>
        </view>
        <view class="filter-options">
          <view 
            v-for="difficulty in difficultyOptions" 
            :key="difficulty.value"
            class="filter-option"
            :class="{ active: currentDifficulty === difficulty.value }"
            @click="selectDifficulty(difficulty.value)"
          >
            {{ difficulty.label }}
          </view>
        </view>
      </view>
    </up-popup>

    <!-- 价格筛选弹窗 -->
    <up-popup v-model:show="priceFilterVisible" mode="bottom" :round="10">
      <view class="filter-popup">
        <view class="filter-header">
          <text class="filter-title">选择价格</text>
          <up-icon name="close" size="20" color="#999" @click="priceFilterVisible = false"></up-icon>
        </view>
        <view class="filter-options">
          <view 
            v-for="price in priceOptions" 
            :key="price.value"
            class="filter-option"
            :class="{ active: currentPriceFilter === price.value }"
            @click="selectPrice(price.value)"
          >
            {{ price.label }}
          </view>
        </view>
      </view>
    </up-popup>
  </view>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { onLoad, onReachBottom } from '@dcloudio/uni-app'
import { assessmentAPI } from '@/api/assessment'
import AssessmentCard from '@/components/AssessmentCard.vue'

// 搜索关键词
const searchKeyword = ref('')

// 当前选中的标签页
const currentTab = ref(0)

// 标签页列表
const tabList = ref([
  { name: '全部测评' },
  { name: '最新发布' },
  { name: '最受欢迎' },
  { name: '免费测评' }
])

// 测评列表
const assessmentList = ref([])

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

// 筛选条件
const currentCategory = ref('')
const currentDifficulty = ref('')
const currentPriceFilter = ref('')

// 筛选弹窗显示状态
const categoryFilterVisible = ref(false)
const difficultyFilterVisible = ref(false)
const priceFilterVisible = ref(false)

// 分类选项
const categoryOptions = ref([
  { label: '全部分类', value: '' },
  { label: '性格测试', value: '性格测试' },
  { label: '情感测评', value: '情感测评' },
  { label: '职业规划', value: '职业规划' },
  { label: '心理健康', value: '心理健康' },
  { label: '人际关系', value: '人际关系' },
  { label: '学习能力', value: '学习能力' }
])

// 难度选项
const difficultyOptions = ref([
  { label: '全部难度', value: '' },
  { label: '简单', value: 'easy' },
  { label: '中等', value: 'medium' },
  { label: '困难', value: 'hard' }
])

// 价格选项
const priceOptions = ref([
  { label: '全部价格', value: '' },
  { label: '免费', value: 'free' },
  { label: '0-50元', value: '0-50' },
  { label: '50-100元', value: '50-100' },
  { label: '100元以上', value: '100+' }
])

// 当前筛选条件
const currentFilter = computed(() => {
  const filters = ['all', 'latest', 'popular', 'free']
  const index = Math.max(0, Math.min(currentTab.value || 0, filters.length - 1))
  return filters[index] || 'all'
})

// 获取难度文本
const getDifficultyText = (difficulty) => {
  switch (difficulty) {
    case 'easy':
      return '简单'
    case 'medium':
      return '中等'
    case 'hard':
      return '困难'
    default:
      return '全部难度'
  }
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

// 获取测评列表
const fetchAssessments = async (reset = false) => {
  if (reset) {
    pagination.page = 1
    assessmentList.value = []
  }

  loading.value = true
  loadMoreStatus.value = 'loading'

  try {
    // 构建查询参数
    const params = {
      page: pagination.page,
      per_page: pagination.per_page,
      status: 'published' // 只获取已发布的测评
    }

    // 添加搜索关键词
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }

    // 添加分类筛选
    if (currentCategory.value) {
      params.category = currentCategory.value
    }

    // 添加难度筛选
    if (currentDifficulty.value) {
      params.difficulty = currentDifficulty.value
    }

    // 添加价格筛选
    if (currentPriceFilter.value) {
      if (currentPriceFilter.value === 'free') {
        params.is_free = true
      } else if (currentPriceFilter.value !== '') {
        // 处理价格区间
        const [min, max] = currentPriceFilter.value.split('-')
        if (min !== undefined) params.min_price = parseFloat(min)
        if (max && max !== '+') params.max_price = parseFloat(max)
      }
    }

    // 根据筛选条件添加排序参数
    switch (currentFilter.value) {
      case 'latest':
        params.sort_by = 'create_time'
        params.sort_order = 'desc'
        break
      case 'popular':
        params.sort_by = 'participant_count'
        params.sort_order = 'desc'
        break
      case 'free':
        params.is_free = true
        params.sort_by = 'create_time'
        params.sort_order = 'desc'
        break
      default:
        // 默认按排序字段排序
        params.sort_by = 'sort_order'
        params.sort_order = 'asc'
        break
    }

    console.log('获取测评列表参数:', params)

    const res = await assessmentAPI.getAssessments(params)

    console.log('测评API响应:', res)

    if (res.success && res.data) {
      // 处理测评数据
      let newList = res.data.list || []

      // 数据处理和字段映射
      newList = newList.map(item => ({
        ...item,
        // 字段映射和默认值处理
        id: item.id,
        name: item.name || '未知测评',
        title: item.name || '未知测评',
        subtitle: item.subtitle || '',
        description: item.description || '专业心理测评，帮助您更好地了解自己',
        cover_image: item.cover_image || '/static/images/default-assessment.png',
        cover: item.cover_image || '/static/images/default-assessment.png',
        participant_count: parseInt(item.participant_count) || 0,
        test_count: parseInt(item.participant_count) || 0,
        price: parseFloat(item.price) || 0,
        difficulty: item.difficulty || 'medium',
        category: item.category || '',
        duration: parseInt(item.duration) || 30,
        question_count: parseInt(item.question_count) || 0,
        rating: parseFloat(item.rating) || 4.8
      }))

      // 更新列表
      assessmentList.value = reset ? newList : [...assessmentList.value, ...newList]

      // 更新分页信息
      pagination.total = res.data.total || 0
      pagination.total_pages = res.data.pages || Math.ceil((res.data.total || 0) / pagination.per_page)

      // 更新加载更多状态
      loadMoreStatus.value = pagination.page >= pagination.total_pages ? 'nomore' : 'loadmore'

      console.log('测评列表加载成功，共', newList.length, '条数据')
    } else {
      console.log('API返回数据格式异常:', res)

      // 设置为空数组，显示空状态
      if (reset) {
        assessmentList.value = []
      }
      loadMoreStatus.value = 'nomore'
    }
  } catch (error) {
    console.error('获取测评列表失败:', error)

    // 设置为空数组，显示空状态
    if (reset) {
      assessmentList.value = []
    }

    loadMoreStatus.value = 'loadmore'
    uni.showToast({
      title: '获取测评列表失败，请稍后重试',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 标签页切换处理
const handleTabChange = (index) => {
  console.log('切换到标签页:', index, tabList.value[index]?.name)
  const tabIndex = typeof index === 'object' ? index.index : index
  currentTab.value = Number(tabIndex)
  console.log('当前筛选条件:', currentFilter.value)
  fetchAssessments(true)
}

// 处理测评卡片点击
const handleAssessmentClick = (assessment) => {
  console.log('测评卡片点击:', assessment)
  
  if (assessment && assessment.id) {
    uni.navigateTo({
      url: `/pages/assessment/detail?id=${assessment.id}`
    })
  } else {
    uni.showToast({
      title: '测评数据异常',
      icon: 'none'
    })
  }
}

// 显示分类筛选
const showCategoryFilter = () => {
  categoryFilterVisible.value = true
}

// 显示难度筛选
const showDifficultyFilter = () => {
  difficultyFilterVisible.value = true
}

// 显示价格筛选
const showPriceFilter = () => {
  priceFilterVisible.value = true
}

// 选择分类
const selectCategory = (category) => {
  currentCategory.value = category
  categoryFilterVisible.value = false
  fetchAssessments(true)
}

// 选择难度
const selectDifficulty = (difficulty) => {
  currentDifficulty.value = difficulty
  difficultyFilterVisible.value = false
  fetchAssessments(true)
}

// 选择价格
const selectPrice = (price) => {
  currentPriceFilter.value = price
  priceFilterVisible.value = false
  fetchAssessments(true)
}

// 加载更多
const loadMore = () => {
  if (loadMoreStatus.value === 'loadmore') {
    pagination.page++
    fetchAssessments()
  }
}

// 页面加载
onLoad(() => {
  console.log('页面加载，初始化测评列表')
  // 确保初始状态正确
  currentTab.value = 0
  fetchAssessments(true)
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
  color: #52c41a;
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
  background: #52c41a;
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
  padding: 10rpx 0;
}

.filter-item text {
  margin-right: 8rpx;
}

// 测评列表
.assessment-list {
  padding: 0 20rpx;
  margin-top: 20rpx;
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

// 筛选弹窗
.filter-popup {
  background: #fff;
  border-radius: 20rpx 20rpx 0 0;
  max-height: 60vh;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.filter-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.filter-options {
  padding: 20rpx 0;
  max-height: 50vh;
  overflow-y: auto;
}

.filter-option {
  padding: 24rpx 30rpx;
  font-size: 28rpx;
  color: #333;
  border-bottom: 1rpx solid #f8f8f8;
}

.filter-option.active {
  color: #52c41a;
  background: #f6ffed;
}

.filter-option:last-child {
  border-bottom: none;
}
</style>
