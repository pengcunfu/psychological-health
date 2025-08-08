<template>
  <view class="container">
    <!-- 顶部搜索栏 -->
    <Navbar 
      :showLeft="true"
      :showRight="false"
      @leftClick="goBack"
    >
      <template #center>
        <view class="search-container">
          <u-input
            v-model="searchKeyword"
            placeholder="搜索课程、测评、咨询师..."
            :border="false"
            :clearable="true"
            :focus="true"
            @change="onSearchInput"
            @confirm="performSearch"
            shape="round"
            height="64"
            backgroundColor="#f5f7fa"
            fontSize="26"
            placeholderStyle="color: #999; font-size: 26rpx;"
            :customStyle="{ padding: '0', margin: '0' }"
          >
            <template #suffix>
              <up-icon name="search" size="20" color="#999" @click="performSearch"></up-icon>
            </template>
          </u-input>
        </view>
      </template>
      
      <template #left>
        <SvgIcon name="arrow-left" :size="20" color="#333" />
      </template>
    </Navbar>

    <!-- 搜索内容区域 -->
    <view class="search-content" v-show="!showResults">
      <!-- 搜索历史 -->
      <view class="history-section" v-if="searchHistory.length > 0">
        <view class="section-title">
          <text>搜索历史</text>
          <up-icon class="clear-icon" name="trash" size="32" color="#999" @click="clearHistory"></up-icon>
        </view>
        <view class="history-list">
          <view 
            class="history-item" 
            v-for="(item, index) in searchHistory" 
            :key="index"
            @click="selectHistoryItem(item)"
          >
            <view class="history-text">
              <up-icon class="history-icon" name="clock" size="32" color="#999"></up-icon>
              <text>{{ item }}</text>
            </view>
            <up-icon 
              class="delete-icon" 
              name="close" 
              size="32" 
              color="#999" 
              @click.stop="removeHistoryItem(index)"
            ></up-icon>
                     </view>
         </view>
       </view>
      
      <!-- 热门搜索 -->
      <view class="hot-section">
        <view class="section-title">
          <text>热门搜索</text>
        </view>
        <view class="tag-list">
          <text 
            class="search-tag" 
            v-for="(tag, index) in hotSearchTags" 
            :key="index"
            @click="selectTag(tag)"
          >
            {{ tag }}
          </text>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view class="empty-state" v-show="showResults && searchResults.length === 0">
      <up-icon name="search" size="120" color="#ccc"></up-icon>
      <text class="empty-text">暂无相关内容</text>
    </view>

    <!-- 搜索结果 -->
    <view class="search-results" v-show="showResults && searchResults.length > 0">
      <!-- 结果分类选项卡 -->
      <view class="result-tabs">
        <text 
          class="result-tab"
          :class="{ active: activeTab === tab.key }"
          v-for="tab in resultTabs"
          :key="tab.key"
          @click="switchTab(tab.key)"
        >
          {{ tab.name }}
        </text>
      </view>
      
      <!-- 搜索结果列表 -->
      <view class="result-list">
        <view 
          class="result-item" 
          v-for="(item, index) in filteredResults" 
          :key="index"
          @click="goToDetail(item)"
        >
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

<script>
import Navbar from '@/components/Navbar.vue'
import SvgIcon from '@/components/SvgIcon.vue'

export default {
  components: {
    Navbar,
    SvgIcon
  },
  
  data() {
    return {
      searchKeyword: '',
      showResults: false,
      activeTab: 'all',
      searchHistory: [],
      hotSearchTags: [
        '焦虑自评量表',
        '情绪管理', 
        '抑郁症测试',
        '睡眠障碍',
        '压力缓解',
        '人际关系',
        '心理咨询师',
        '婚恋情感'
      ],
      resultTabs: [
        { key: 'all', name: '全部' },
        { key: 'course', name: '课程' },
        { key: 'assessment', name: '测评' },
        { key: 'counselor', name: '咨询师' }
      ],
      searchResults: []
    }
  },
  
  computed: {
    filteredResults() {
      if (this.activeTab === 'all') {
        return this.searchResults
      }
      return this.searchResults.filter(item => item.type === this.getTypeByTab(this.activeTab))
    }
  },
  
  onLoad() {
    this.loadSearchHistory()
  },
  
  methods: {
    goBack() {
      uni.navigateBack()
    },
    
    onSearchInput(value) {
      this.searchKeyword = value
    },
    
    performSearch() {
      if (!this.searchKeyword.trim()) return
      
      this.addToHistory(this.searchKeyword.trim())
      this.showResults = true
      this.searchData()
    },
    
    searchData() {
      // 模拟搜索数据
      this.searchResults = [
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
    },
    
    addToHistory(keyword) {
      if (this.searchHistory.includes(keyword)) {
        this.searchHistory = this.searchHistory.filter(item => item !== keyword)
      }
      this.searchHistory.unshift(keyword)
      if (this.searchHistory.length > 10) {
        this.searchHistory = this.searchHistory.slice(0, 10)
      }
      this.saveSearchHistory()
    },
    
    loadSearchHistory() {
      const history = uni.getStorageSync('searchHistory')
      if (history) {
        this.searchHistory = JSON.parse(history)
      }
    },
    
    saveSearchHistory() {
      uni.setStorageSync('searchHistory', JSON.stringify(this.searchHistory))
    },
    
    clearHistory() {
      this.searchHistory = []
      this.saveSearchHistory()
    },
    
    removeHistoryItem(index) {
      this.searchHistory.splice(index, 1)
      this.saveSearchHistory()
    },
    
    selectHistoryItem(item) {
      this.searchKeyword = item
      this.performSearch()
    },
    
    selectTag(tag) {
      this.searchKeyword = tag
      this.performSearch()
    },
    
    switchTab(tabKey) {
      this.activeTab = tabKey
    },
    
    getTypeByTab(tab) {
      const mapping = {
        course: '课程',
        assessment: '测评', 
        counselor: '咨询师'
      }
      return mapping[tab] || ''
    },
    
    highlightKeyword(text) {
      if (!this.searchKeyword || !text) return text
      const keyword = this.searchKeyword.trim()
      const regex = new RegExp(`(${keyword})`, 'gi')
      return text.replace(regex, '<span class="result-highlight">$1</span>')
    },
    
    goToDetail(item) {
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
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

/* 顶部导航样式已由Navbar组件提供 */

.search-content {
  padding: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.history-section {
  margin-bottom: 40rpx;
}

.history-list {
  margin-bottom: 40rpx;
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 0;
  border-bottom: 1px solid #f0f0f0;
}

.history-item:last-child {
  border-bottom: none;
}

.history-text {
  display: flex;
  align-items: center;
  font-size: 28rpx;
  color: #666;
}

.history-icon {
  margin-right: 20rpx;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 40rpx;
}

.search-tag {
  display: inline-block;
  padding: 12rpx 24rpx;
  background-color: #fff;
  color: #666;
  border-radius: 32rpx;
  font-size: 28rpx;
  margin-right: 20rpx;
  margin-bottom: 20rpx;
}

.empty-state {
  padding: 80rpx 0;
  text-align: center;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
  margin-top: 30rpx;
}

.search-results {
  background-color: #fff;
}

.result-tabs {
  display: flex;
  background-color: #fff;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 20rpx;
}

.result-tab {
  flex: 1;
  text-align: center;
  padding: 24rpx 0;
  font-size: 28rpx;
  color: #666;
  position: relative;
}

.result-tab.active {
  color: #4A90E2;
  font-weight: bold;
}

.result-tab.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40rpx;
  height: 6rpx;
  background-color: #4A90E2;
  border-radius: 3rpx;
}

.result-list {
  padding: 0 30rpx;
}

.result-item {
  display: flex;
  padding: 30rpx 0;
  border-bottom: 1px solid #f0f0f0;
}

.result-image {
  width: 160rpx;
  height: 120rpx;
  border-radius: 8rpx;
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
  color: #333;
  margin-bottom: 8rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.result-desc {
  font-size: 24rpx;
  color: #999;
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
  color: #4A90E2;
  background-color: #f0f7ff;
  padding: 4rpx 12rpx;
  border-radius: 4rpx;
  margin-right: 16rpx;
}

.result-info {
  font-size: 24rpx;
  color: #999;
}

/* 高亮样式 */
::v-deep .result-highlight {
  color: #4A90E2;
  background-color: #f0f7ff;
  padding: 2rpx 4rpx;
  border-radius: 2rpx;
}

/* uview输入框样式优化 - 彻底移除边距 */
.search-container {
  flex: 1;
  max-width: 500rpx;
}

.search-container ::v-deep .u-input {
  height: 64rpx !important;
  padding: 0 !important;
  margin: 0 !important;
  box-sizing: border-box !important;
}

.search-container ::v-deep .u-input__content {
  height: 64rpx !important;
  background-color: #f5f7fa !important;
  border-radius: 32rpx !important;
  padding: 0 24rpx !important;
  margin: 0 !important;
  border: none !important;
  box-sizing: border-box !important;
}

.search-container ::v-deep .u-input__content__field-wrapper {
  height: 64rpx !important;
  padding: 0 !important;
  margin: 0 !important;
  box-sizing: border-box !important;
}

.search-container ::v-deep .u-input__content__field-wrapper__field {
  height: 64rpx !important;
  line-height: 64rpx !important;
  font-size: 26rpx !important;
  padding: 0 !important;
  margin: 0 !important;
  box-sizing: border-box !important;
}

/* 移除可能的默认间距和边框 */
.search-container ::v-deep .uni-input-wrapper {
  padding: 0 !important;
  margin: 0 !important;
}

.search-container ::v-deep .uni-input-placeholder,
.search-container ::v-deep .uni-input-input {
  padding: 0 !important;
  margin: 0 !important;
}
</style> 