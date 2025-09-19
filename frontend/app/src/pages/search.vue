<template>
  <view class="container">
    <!-- 顶部搜索栏 -->
    <view class="search-header">
      <view class="search-header-content">
        <view class="search-input-wrapper">
          <view class="search-icon" @click="performSearch">
            <SvgIcon name="search" :size="20" color="#999" />
          </view>
          <u-input v-model="searchKeyword" placeholder="搜索课程、测评、咨询师..." border="none" :clearable="true" :focus="true"
            @change="onSearchInput" @confirm="performSearch" shape="round" height="64" backgroundColor="#f5f7fa"
            fontSize="26" placeholderStyle="color: #999; font-size: 26rpx;"
            :customStyle="{ padding: '0', margin: '0' }" />
        </view>
      </view>
    </view>

    <!-- 搜索内容区域 -->
    <view class="search-content" v-show="!showResults">
      <!-- 搜索历史 -->
      <view class="history-section" v-if="searchHistory.length > 0">
        <view class="section-title">
          <text>搜索历史</text>
          <u-icon class="clear-icon" name="trash" :size="32" color="#999" @click="clearHistory"></u-icon>
        </view>
        <view class="history-list">
          <view class="history-item" v-for="(item, index) in searchHistory" :key="index"
            @click="selectHistoryItem(item)">
            <view class="history-text">
              <u-icon class="history-icon" name="clock" :size="32" color="#999"></u-icon>
              <text>{{ item }}</text>
            </view>
            <u-icon class="delete-icon" name="close" :size="32" color="#999"
              @click.stop="removeHistoryItem(index)"></u-icon>
          </view>
        </view>
      </view>

      <!-- 热门搜索 -->
      <view class="hot-section">
        <view class="section-title">
          <text>热门搜索</text>
        </view>
        <view class="tag-list">
          <text class="search-tag" v-for="(tag, index) in hotSearchTags" :key="index" @click="selectTag(tag)">
            {{ tag }}
          </text>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view class="empty-state" v-show="showResults && searchResults.length === 0">
      <u-icon name="search" :size="120" color="#ccc"></u-icon>
      <text class="empty-text">暂无相关内容</text>
    </view>

    <!-- 搜索结果 -->
    <view class="search-results" v-show="showResults && searchResults.length > 0">
      <!-- 结果分类选项卡 -->
      <view class="result-tabs">
        <text class="result-tab" :class="{ active: activeTab === tab.key }" v-for="tab in resultTabs" :key="tab.key"
          @click="switchTab(tab.key)">
          {{ tab.name }}
        </text>
      </view>

      <!-- 搜索结果列表 -->
      <view class="result-list">
        <view class="result-item" v-for="(item, index) in filteredResults" :key="index" @click="goToDetail(item)">
          <image :src="item.image" class="result-image" mode="aspectFill"></image>
          <view class="result-content">
            <view class="result-title" v-html="highlightKeyword(item.title)"></view>
            <view class="result-desc" v-html="highlightKeyword(item.description)"></view>
            <view class="result-meta">
              <text class="result-tag">{{ item.type }}</text>
              <text class="result-info">{{ item.meta }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import SvgIcon from '@/components/SvgIcon.vue'

// 响应式数据
const searchKeyword = ref('')
const showResults = ref(false)
const activeTab = ref('all')
const searchHistory = ref([])
const searchResults = ref([])

// 静态数据
const hotSearchTags = [
  '焦虑自评量表',
  '情绪管理', 
  '抑郁症测试',
  '睡眠障碍',
  '压力缓解',
  '人际关系',
  '心理咨询师',
  '婚恋情感'
]

const resultTabs = [
  { key: 'all', name: '全部' },
  { key: 'course', name: '课程' },
  { key: 'assessment', name: '测评' },
  { key: 'counselor', name: '咨询师' }
]

// 计算属性
const filteredResults = computed(() => {
  if (activeTab.value === 'all') {
    return searchResults.value
  }
  return searchResults.value.filter(item => item.type === getTypeByTab(activeTab.value))
})

// 方法
const onSearchInput = (value) => {
  searchKeyword.value = value
}

const performSearch = () => {
  if (!searchKeyword.value.trim()) return
  
  addToHistory(searchKeyword.value.trim())
  showResults.value = true
  searchData()
}

const searchData = () => {
  // 模拟搜索数据
  searchResults.value = [
    {
      type: '课程',
      title: '情绪管理：如何应对日常压力与焦虑',
      description: '本课程将帮助你了解情绪的本质，识别压力和焦虑的来源，掌握实用的情绪管理技巧，建立健康的应对机制。',
      image: 'https://via.placeholder.com/80x60/4A90E2/FFFFFF/?text=课程',
      meta: '3,256人学习',
      id: 1
    },
    {
      type: '测评',
      title: '情绪管理能力测评',
      description: '评估您的情绪管理能力水平，帮助您了解自己在情绪调节方面的优势和不足，提供针对性的改进建议。',
      image: 'https://via.placeholder.com/80x60/52C41A/FFFFFF/?text=测评',
      meta: '1,892人已测',
      id: 2
    },
    {
      type: '咨询师',
      title: '李医生 - 情绪管理专家',
      description: '擅长情绪管理、压力缓解、焦虑调节等领域，拥有10年心理咨询经验，帮助过上千名来访者解决情绪问题。',
      image: 'https://via.placeholder.com/80x60/FA8C16/FFFFFF/?text=咨询师',
      meta: '4.9分 | 咨询2000+小时',
      id: 3
    }
  ]
}

const addToHistory = (keyword) => {
  if (searchHistory.value.includes(keyword)) {
    searchHistory.value = searchHistory.value.filter(item => item !== keyword)
  }
  searchHistory.value.unshift(keyword)
  if (searchHistory.value.length > 10) {
    searchHistory.value = searchHistory.value.slice(0, 10)
  }
  saveSearchHistory()
}

const loadSearchHistory = () => {
  const history = uni.getStorageSync('searchHistory')
  if (history) {
    searchHistory.value = JSON.parse(history)
  }
}

const saveSearchHistory = () => {
  uni.setStorageSync('searchHistory', JSON.stringify(searchHistory.value))
}

const clearHistory = () => {
  searchHistory.value = []
  saveSearchHistory()
}

const removeHistoryItem = (index) => {
  searchHistory.value.splice(index, 1)
  saveSearchHistory()
}

const selectHistoryItem = (item) => {
  searchKeyword.value = item
  performSearch()
}

const selectTag = (tag) => {
  searchKeyword.value = tag
  performSearch()
}

const switchTab = (tabKey) => {
  activeTab.value = tabKey
}

const getTypeByTab = (tab) => {
  const mapping = {
    course: '课程',
    assessment: '测评', 
    counselor: '咨询师'
  }
  return mapping[tab] || ''
}

const highlightKeyword = (text) => {
  if (!searchKeyword.value || !text) return text
  const keyword = searchKeyword.value.trim()
  const regex = new RegExp(`(${keyword})`, 'gi')
  return text.replace(regex, '<span class="result-highlight">$1</span>')
}

const goToDetail = (item) => {
  // 根据类型跳转到不同的详情页
  if (item.type === '课程') {
    uni.navigateTo({
      url: `/pages/course/detail?id=${item.id}`
    })
  } else if (item.type === '咨询师') {
    uni.navigateTo({
      url: `/pages/counselor/detail?id=${item.id}`
    })
  }
}

// 生命周期
onLoad(() => {
  // 获取系统信息，设置状态栏高度
  const systemInfo = uni.getSystemInfoSync()
  const statusBarHeight = systemInfo.statusBarHeight || 0
  
  // 设置CSS变量
  const style = document.documentElement.style || document.body.style
  if (style) {
    style.setProperty('--status-bar-height', statusBarHeight + 'px')
  }
  
  loadSearchHistory()
})
</script>

<style lang="scss" scoped>
// SCSS 变量定义
$primary-color: #4A90E2;
$primary-light: #f0f7ff;
$bg-color: #f5f7fa;
$white: #fff;
$gray-light: #f0f0f0;
$gray: #999;
$gray-medium: #666;
$gray-dark: #333;
$text-color: #333;
$border-radius: 8rpx;
$border-radius-large: 32rpx;
$shadow-light: 0 2rpx 8rpx rgba(0, 0, 0, 0.06);

.container {
  min-height: 100vh;
  background-color: $bg-color;
}

// 搜索头部样式
.search-header {
  background-color: $white;
  box-shadow: $shadow-light;
  position: sticky;
  top: 0;
  z-index: 1000;

  &-content {
    display: flex;
    align-items: center;
    padding: 20rpx 30rpx;
    height: 88rpx;
  }
}

.search-input-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;

  .search-icon {
    position: absolute;
    left: 24rpx;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8rpx;
    cursor: pointer;
  }

  // uview输入框样式优化
  ::v-deep .up--input {
    height: 64rpx !important;
    padding: 0 !important;
    margin: 0 !important;
    box-sizing: border-box !important;

    &__content {
      height: 64rpx !important;
      background-color: $bg-color !important;
      border-radius: $border-radius-large !important;
      padding: 0 24rpx 0 64rpx !important;
      margin: 0 !important;
      border: none !important;
      box-sizing: border-box !important;

      &__field-wrapper {
        height: 64rpx !important;
        padding: 0 !important;
        margin: 0 !important;
        box-sizing: border-box !important;

        &__field {
          height: 64rpx !important;
          line-height: 64rpx !important;
          font-size: 26rpx !important;
          padding: 0 !important;
          margin: 0 !important;
          box-sizing: border-box !important;
        }
      }
    }
  }

  // 移除可能的默认间距和边框
  ::v-deep .uni-input-wrapper {
    padding: 0 !important;
    margin: 0 !important;
  }

  ::v-deep .uni-input-placeholder,
  ::v-deep .uni-input-input {
    padding: 0 !important;
    margin: 0 !important;
  }
}

.search-content {
  padding: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: $text-color;
  margin-bottom: 30rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

// 搜索历史
.history-section {
  margin-bottom: 40rpx;

  .history-list {
    margin-bottom: 40rpx;
  }
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 0;
  border-bottom: 1px solid $gray-light;

  &:last-child {
    border-bottom: none;
  }
}

.history-text {
  display: flex;
  align-items: center;
  font-size: 28rpx;
  color: $gray-medium;

  .history-icon {
    margin-right: 20rpx;
  }
}

// 热门标签
.tag-list {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 40rpx;
}

.search-tag {
  display: inline-block;
  padding: 12rpx 24rpx;
  background-color: $white;
  color: $gray-medium;
  border-radius: $border-radius-large;
  font-size: 28rpx;
  margin-right: 20rpx;
  margin-bottom: 20rpx;
}

// 空状态
.empty-state {
  padding: 80rpx 0;
  text-align: center;

  .empty-text {
    font-size: 28rpx;
    color: $gray;
    margin-top: 30rpx;
  }
}

// 搜索结果
.search-results {
  background-color: $white;
}

.result-tabs {
  display: flex;
  background-color: $white;
  border-bottom: 1px solid $gray-light;
  margin-bottom: 20rpx;
}

.result-tab {
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
      background-color: $primary-color;
      border-radius: 3rpx;
    }
  }
}

.result-list {
  padding: 0 30rpx;
}

.result-item {
  display: flex;
  padding: 30rpx 0;
  border-bottom: 1px solid $gray-light;
}

.result-image {
  width: 160rpx;
  height: 120rpx;
  border-radius: $border-radius;
  margin-right: 24rpx;
  flex-shrink: 0;
}

.result-content {
  flex: 1;
  overflow: hidden;
}

.result-title {
  font-size: 30rpx;
  font-weight: bold;
  color: $text-color;
  margin-bottom: 8rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.result-desc {
  font-size: 24rpx;
  color: $gray;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.5;
  margin-bottom: 12rpx;
}

.result-meta {
  display: flex;
  align-items: center;
}

.result-tag {
  font-size: 24rpx;
  color: $primary-color;
  background-color: $primary-light;
  padding: 4rpx 12rpx;
  border-radius: 4rpx;
  margin-right: 16rpx;
}

.result-info {
  font-size: 24rpx;
  color: $gray;
}

// 高亮样式
::v-deep .result-highlight {
  color: $primary-color;
  background-color: $primary-light;
  padding: 2rpx 4rpx;
  border-radius: 2rpx;
}
</style>