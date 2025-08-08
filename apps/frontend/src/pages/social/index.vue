<template>
  <view class="container tab-page">
    <!-- 导航栏 -->
    <Navbar 
      title="互动社区" 
      :show-left="true"
      :show-right="true" 
      right-icon="plus" 
      @leftClick="handleHomeClick"
      @rightClick="handlePublishClick" 
    >
      <template #left>
        <SvgIcon name="home" :size="44" color="#333" />
      </template>
    </Navbar>
    
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

    <!-- 热门话题 -->
    <view class="hot-topics-section" v-if="currentTab === 0">
      <view class="section-header">
        <view class="section-title">
          <text class="title-icon">🔥</text>
          <text class="title-text">热门话题</text>
        </view>
      </view>
      <scroll-view class="topics-scroll" scroll-x="true" show-scrollbar="false">
        <view class="topics-list">
          <view 
            v-for="(topic, index) in hotTopics" 
            :key="index"
            class="topic-tag"
            @click="handleTopicClick(topic)"
          >
            <text class="topic-name"># {{ topic.name }}</text>
            <text class="topic-count">{{ topic.count }}人参与</text>
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- 帖子列表 -->
    <view class="posts-list">
      <SocialCard 
        v-for="(post, index) in postList" 
        :key="post.id || index"
        :post="post"
        @click="handlePostClick"
        @like="handleLike"
        @comment="handleComment"
        @share="handleShare"
        @topicClick="handleTopicClick"
      />
    </view>

    <!-- 空状态 -->
    <view v-if="!loading && postList.length === 0" class="empty-state">
      <view class="empty-content">
        <text class="empty-icon">💬</text>
        <text class="empty-title">暂无帖子</text>
        <text class="empty-subtitle">快来分享你的心情和想法吧</text>
        <button class="empty-button" @click="handlePublishClick">
          发布动态
        </button>
      </view>
    </view>

    <!-- 加载更多 -->
    <view class="load-more-container">
      <up-loadmore 
        :status="loadMoreStatus" 
        @loadmore="loadMore" 
        loading-text="正在加载更多..."
        loadmore-text="上拉加载更多"
        nomore-text="已加载全部内容"
        icon-size="20"
        :margin-top="20"
        :margin-bottom="20"
      />
    </view>

    <!-- 发布按钮（浮动） -->
    <view class="floating-publish-btn" @click="handlePublishClick">
      <SvgIcon name="plus" :size="24" color="#fff" />
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { onLoad, onReachBottom, onPullDownRefresh } from '@dcloudio/uni-app'
import Navbar from '@/components/Navbar.vue'
import SvgIcon from '@/components/SvgIcon.vue'
import SocialCard from '@/components/SocialCard.vue'

// 当前选中的标签页
const currentTab = ref(0)

// 标签页列表
const tabList = ref([
  { name: '推荐', type: 'recommend' },
  { name: '关注', type: 'following' },
  { name: '最新', type: 'latest' },
  { name: '热门', type: 'hot' }
])

// 帖子列表
const postList = ref([])

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

// 热门话题
const hotTopics = ref([
  { name: '心理健康', count: 1234 },
  { name: '情感困扰', count: 856 },
  { name: '职场压力', count: 642 },
  { name: '人际关系', count: 523 },
  { name: '自我成长', count: 478 },
  { name: '焦虑症', count: 389 },
  { name: '抑郁情绪', count: 267 }
])

// 模拟数据
const mockPosts = [
  {
    id: 1,
    username: '小雨点',
    user_avatar: '',
    title: '如何克服社交恐惧症？',
    content: '最近在工作中总是感到紧张，不敢和同事主动交流，想请教大家有什么好的方法可以改善这种情况...',
    category: '心理健康',
    topics: ['社交恐惧', '职场心理'],
    images: [],
    like_count: 23,
    comment_count: 8,
    is_liked: false,
    create_time: '2024-01-20 14:30:00'
  },
  {
    id: 2,
    username: '阳光少年',
    user_avatar: '',
    title: '分享一些缓解焦虑的小技巧',
    content: '作为一个曾经深受焦虑困扰的人，想和大家分享一些我觉得很有效的方法：\n1. 深呼吸练习\n2. 正念冥想\n3. 运动锻炼\n希望对大家有帮助！',
    category: '经验分享',
    topics: ['焦虑症', '自我调节'],
    images: ['/static/images/post1.jpg', '/static/images/post2.jpg'],
    like_count: 45,
    comment_count: 12,
    is_liked: true,
    create_time: '2024-01-20 10:15:00'
  },
  {
    id: 3,
    username: '心理小助手',
    user_avatar: '',
    title: '',
    content: '今天心情不太好，感觉压力很大。有没有人愿意聊聊天？',
    category: '情感倾诉',
    topics: ['心情日记'],
    images: [],
    like_count: 12,
    comment_count: 15,
    is_liked: false,
    create_time: '2024-01-19 22:45:00'
  }
]

// 获取帖子列表
const fetchPosts = async (reset = false) => {
  if (reset) {
    pagination.page = 1
    postList.value = []
  }

  loading.value = true
  loadMoreStatus.value = 'loading'

  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 使用模拟数据
    const newPosts = mockPosts.map(post => ({
      ...post,
      id: post.id + (pagination.page - 1) * pagination.per_page
    }))

    postList.value = reset ? newPosts : [...postList.value, ...newPosts]
    
    // 模拟分页
    pagination.total = 20
    pagination.total_pages = Math.ceil(pagination.total / pagination.per_page)
    
    loadMoreStatus.value = pagination.page >= pagination.total_pages ? 'nomore' : 'loadmore'
    
  } catch (error) {
    console.error('获取帖子列表失败:', error)
    uni.showToast({
      title: '获取内容失败',
      icon: 'none'
    })
    loadMoreStatus.value = 'loadmore'
  } finally {
    loading.value = false
  }
}

// 标签页切换
const handleTabChange = (index) => {
  currentTab.value = index
  fetchPosts(true)
}

// 话题点击
const handleTopicClick = (topic) => {
  const topicName = typeof topic === 'string' ? topic : topic.name
  uni.showToast({
    title: `查看话题: ${topicName}`,
    icon: 'none'
  })
}

// 帖子点击
const handlePostClick = (post) => {
  uni.navigateTo({
    url: `/pages/social/detail?id=${post.id}`
  })
}

// Home按钮点击
const handleHomeClick = () => {
  uni.switchTab({
    url: '/pages/index'
  })
}

// 发布点击
const handlePublishClick = () => {
  uni.navigateTo({
    url: '/pages/social/publish'
  })
}

// 点赞
const handleLike = (post) => {
  post.is_liked = !post.is_liked
  post.like_count += post.is_liked ? 1 : -1
  
  uni.showToast({
    title: post.is_liked ? '已点赞' : '已取消点赞',
    icon: 'none'
  })
}

// 评论
const handleComment = (post) => {
  uni.navigateTo({
    url: `/pages/social/detail?id=${post.id}&focus=comment`
  })
}

// 分享
const handleShare = (post) => {
  uni.showActionSheet({
    itemList: ['分享到微信', '分享到朋友圈', '复制链接'],
    success: (res) => {
      uni.showToast({
        title: '分享功能开发中',
        icon: 'none'
      })
    }
  })
}

// previewImage和formatTime函数已移至SocialCard组件

// 加载更多
const loadMore = () => {
  if (loadMoreStatus.value === 'loadmore') {
    pagination.page++
    fetchPosts()
  }
}

// 页面加载
onLoad(() => {
  fetchPosts(true)
})

// 下拉刷新
onPullDownRefresh(() => {
  fetchPosts(true).finally(() => {
    uni.stopPullDownRefresh()
  })
})

// 触底加载更多
onReachBottom(() => {
  loadMore()
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 30rpx;
}

// 标签栏
.tabs {
  display: flex;
  background: #fff;
  border-bottom: 1rpx solid #f0f0f0;
  position: sticky;
  top: 0;
  z-index: 10;
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
  color: #fa8c16;
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
  background: #fa8c16;
  border-radius: 3rpx;
}

// 热门话题区域
.hot-topics-section {
  background: #fff;
  padding: 30rpx 0 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.section-header {
  padding: 0 30rpx 20rpx;
}

.section-title {
  display: flex;
  align-items: center;
}

.title-icon {
  font-size: 32rpx;
  margin-right: 10rpx;
}

.title-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.topics-scroll {
  white-space: nowrap;
}

.topics-list {
  display: flex;
  padding: 0 30rpx;
  gap: 20rpx;
}

.topic-tag {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx 30rpx;
  background: linear-gradient(135deg, #fff7e6, #fff2e8);
  border-radius: 16rpx;
  border: 1rpx solid #ffe7ba;
  min-width: 160rpx;
  box-shadow: 0 2rpx 8rpx rgba(250, 140, 22, 0.1);
}

.topic-name {
  font-size: 28rpx;
  color: #fa8c16;
  font-weight: bold;
  margin-bottom: 8rpx;
}

.topic-count {
  font-size: 22rpx;
  color: #999;
}

// 帖子列表
.posts-list {
  padding: 20rpx;
}

// 帖子相关样式已移至SocialCard组件

// 空状态
.empty-state {
  padding: 100rpx 40rpx;
  text-align: center;
}

.empty-content {
  background: #fff;
  border-radius: 16rpx;
  padding: 60rpx 40rpx;
}

.empty-icon {
  font-size: 100rpx;
  display: block;
  margin-bottom: 20rpx;
}

.empty-title {
  font-size: 32rpx;
  color: #333;
  margin-bottom: 12rpx;
  display: block;
}

.empty-subtitle {
  font-size: 28rpx;
  color: #999;
  margin-bottom: 40rpx;
  display: block;
}

.empty-button {
  background: #fa8c16;
  color: #fff;
  border: none;
  border-radius: 25rpx;
  padding: 0 40rpx;
  height: 70rpx;
  font-size: 28rpx;
}

// 加载更多
.load-more-container {
  padding: 0 0 20rpx;
}

// 浮动发布按钮
.floating-publish-btn {
  position: fixed;
  bottom: 120rpx;
  right: 40rpx;
  width: 100rpx;
  height: 100rpx;
  background: linear-gradient(135deg, #fa8c16, #ffa940);
  border-radius: 50rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 16rpx rgba(250, 140, 22, 0.4);
  z-index: 100;
}

.floating-publish-btn:active {
  transform: scale(0.95);
}
</style>
