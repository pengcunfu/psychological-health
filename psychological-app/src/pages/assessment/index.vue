<template>
  <view class="container tab-page">
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
        <u-icon name="arrow-down" size="12" color="#999"></u-icon>
      </view>
      <view class="filter-item" @click="showDifficultyFilter">
        <text>{{ currentDifficulty ? getDifficultyText(currentDifficulty) : '全部难度' }}</text>
        <u-icon name="arrow-down" size="12" color="#999"></u-icon>
      </view>
      <view class="filter-item" @click="showPriceFilter">
        <text>{{ currentPriceFilter || '全部价格' }}</text>
        <u-icon name="arrow-down" size="12" color="#999"></u-icon>
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
        <u-icon name="file-text" size="60" color="#ccc"></u-icon>
        <text class="empty-title">暂无相关测评</text>
        <text class="empty-subtitle">试试调整搜索条件或筛选选项</text>
        <u-button
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
        ></u-button>
      </view>
    </view>

    <!-- 加载更多 -->
    <view class="load-more-container">
      <u-loadmore :status="loadMoreStatus" @loadmore="loadMore" 
        :loading-text="'正在加载更多测评...'"
        :loadmore-text="'上拉加载更多'"
        :nomore-text="'已加载全部测评'"
        icon-size="20"
        :margin-top="20"
        :margin-bottom="20"
      />
    </view>

    <!-- 分类筛选弹窗 -->
    <u-popup v-model:show="categoryFilterVisible" mode="bottom" :round="10">
      <view class="filter-popup">
        <view class="filter-header">
          <text class="filter-title">选择分类</text>
          <u-icon name="close" size="20" color="#999" @click="categoryFilterVisible = false"></u-icon>
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
    </u-popup>

    <!-- 难度筛选弹窗 -->
    <u-popup v-model:show="difficultyFilterVisible" mode="bottom" :round="10">
      <view class="filter-popup">
        <view class="filter-header">
          <text class="filter-title">选择难度</text>
          <u-icon name="close" size="20" color="#999" @click="difficultyFilterVisible = false"></u-icon>
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
    </u-popup>

    <!-- 价格筛选弹窗 -->
    <u-popup v-model:show="priceFilterVisible" mode="bottom" :round="10">
      <view class="filter-popup">
        <view class="filter-header">
          <text class="filter-title">选择价格</text>
          <u-icon name="close" size="20" color="#999" @click="priceFilterVisible = false"></u-icon>
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
    </u-popup>

    <!-- 悬浮搜索按钮 -->
    <view class="floating-search-btn" @click="handleSearchClick">
      <SvgIcon name="search" :size="24" color="#fff" />
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { onLoad, onReachBottom } from '@dcloudio/uni-app'
import { assessmentAPI } from '@/api/assessment'
import AssessmentCard from '@/components/AssessmentCard.vue'
import SvgIcon from '@/components/SvgIcon.vue'

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

// goBack函数已移除，NavBar组件会自动处理返回功能

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


    const res = await assessmentAPI.getAssessments(params)


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

    } else {

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
  const tabIndex = typeof index === 'object' ? index.index : index
  currentTab.value = Number(tabIndex)
  fetchAssessments(true)
}

// 处理测评卡片点击
const handleAssessmentClick = (assessment) => {
  
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
// SCSS 变量定义
$primary-color: #52c41a;
$bg-color: #f5f7fa;
$white: #fff;
$gray-light: #f0f0f0;
$gray: #999;
$gray-medium: #666;
$text-color: #333;
$border-radius: 12rpx;
$shadow-light: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);

.container {
  min-height: 100vh;
  background: $bg-color;
  padding-bottom: 30rpx;
}

// 标签栏
.tabs {
  display: flex;
  background: $white;
  border-bottom: 1rpx solid $gray-light;
}

.tab {
  flex: 1;
  text-align: center;
  padding: 24rpx 0;
  font-size: 28rpx;
  color: $gray-medium;
  position: relative;

  &.active {
    color: $primary-color;
    font-weight: bold;

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 40rpx;
      height: 6rpx;
      background: $primary-color;
      border-radius: 3rpx;
    }
  }
}

// 筛选栏
.filter-bar {
  display: flex;
  padding: 20rpx 30rpx;
  background: $white;
  border-bottom: 1rpx solid $gray-light;
}

.filter-item {
  display: flex;
  align-items: center;
  margin-right: 30rpx;
  font-size: 24rpx;
  color: $gray-medium;
  padding: 10rpx 0;

  text {
    margin-right: 8rpx;
  }
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

  .empty-content {
    background: $white;
    border-radius: $border-radius;
    padding: 40rpx 30rpx;
  }

  .empty-title {
    font-size: 28rpx;
    color: $text-color;
    margin: 20rpx 0 8rpx;
    display: block;
  }

  .empty-subtitle {
    font-size: 24rpx;
    color: $gray;
    display: block;
  }
}

// 加载更多
.load-more-container {
  padding: 0 0 20rpx;
}

// 筛选弹窗
.filter-popup {
  background: $white;
  border-radius: 20rpx 20rpx 0 0;
  max-height: 60vh;

  .filter-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30rpx;
    border-bottom: 1rpx solid $gray-light;

    .filter-title {
      font-size: 32rpx;
      font-weight: bold;
      color: $text-color;
    }
  }

  .filter-options {
    padding: 20rpx 0;
    max-height: 50vh;
    overflow-y: auto;
  }

  .filter-option {
    padding: 24rpx 30rpx;
    font-size: 28rpx;
    color: $text-color;
    border-bottom: 1rpx solid #f8f8f8;

    &.active {
      color: $primary-color;
      background: #f6ffed;
    }

    &:last-child {
      border-bottom: none;
    }
  }
}

// 悬浮搜索按钮
.floating-search-btn {
  position: fixed;
  bottom: 120rpx;
  right: 30rpx;
  width: 100rpx;
  height: 100rpx;
  background: $primary-color;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: $shadow-light;
  z-index: 1000;
  transition: all 0.3s ease;

  &:active {
    transform: scale(0.95);
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.12);
  }

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 6rpx 16rpx rgba(0, 0, 0, 0.12);
  }
}
</style>
