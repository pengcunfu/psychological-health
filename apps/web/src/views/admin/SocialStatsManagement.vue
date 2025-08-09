<template>
  <div class="social-stats-management">
    <div class="page-header">
      <h2>社区统计</h2>
      <a-button @click="refreshData">
        <reload-outlined />
        刷新数据
      </a-button>
    </div>

    <!-- 话题统计 -->
    <a-card title="话题统计" class="stats-card" :loading="loading">
      <a-row :gutter="16" v-if="topicStats">
        <a-col :span="6">
          <a-statistic title="总话题数" :value="topicStats.total_topics || 0" />
        </a-col>
        <a-col :span="6">
          <a-statistic title="活跃话题" :value="topicStats.active_topics || 0" />
        </a-col>
        <a-col :span="6">
          <a-statistic title="热门话题" :value="topicStats.hot_topics || 0" />
        </a-col>
        <a-col :span="6">
          <a-statistic title="精选话题" :value="topicStats.featured_topics || 0" />
        </a-col>
      </a-row>
      <a-empty v-else-if="!loading" description="暂无话题统计数据" />
      
      <a-divider />
      
      <div v-if="topicStats && topicStats.top_topic" class="top-item">
        <h4>最热门话题</h4>
        <a-card size="small">
          <div class="topic-info">
            <div class="topic-header">
              <span class="topic-name">{{ topicStats.top_topic.name || '未知话题' }}</span>
              <div class="topic-color" :style="{ backgroundColor: topicStats.top_topic.color || '#1890ff' }"></div>
            </div>
            <p class="topic-desc">{{ topicStats.top_topic.description || '无描述' }}</p>
            <div class="topic-stats">
              <a-space>
                <span>帖子: {{ topicStats.top_topic.post_count || 0 }}</span>
                <span>参与: {{ topicStats.top_topic.participant_count || 0 }}</span>
                <span>浏览: {{ topicStats.top_topic.view_count || 0 }}</span>
              </a-space>
            </div>
          </div>
        </a-card>
      </div>
    </a-card>

    <!-- 帖子统计 -->
    <a-card title="帖子统计" class="stats-card" :loading="loading">
      <a-row :gutter="16" v-if="postStats">
        <a-col :span="4">
          <a-statistic title="总帖子数" :value="postStats.total_posts || 0" />
        </a-col>
        <a-col :span="4">
          <a-statistic title="已发布" :value="postStats.published_posts || 0" />
        </a-col>
        <a-col :span="4">
          <a-statistic title="草稿" :value="postStats.draft_posts || 0" />
        </a-col>
        <a-col :span="4">
          <a-statistic title="隐藏" :value="postStats.hidden_posts || 0" />
        </a-col>
        <a-col :span="4">
          <a-statistic title="今日新增" :value="postStats.today_posts || 0" />
        </a-col>
        <a-col :span="4">
          <a-statistic title="待审核" :value="postStats.pending_posts || 0" />
        </a-col>
      </a-row>
      <a-empty v-else-if="!loading" description="暂无帖子统计数据" />
      
      <a-divider />
      
      <div v-if="postStats && postStats.hot_post" class="top-item">
        <h4>最热门帖子</h4>
        <a-card size="small">
          <div class="post-info">
            <h5>{{ postStats.hot_post.title || '无标题' }}</h5>
            <p>{{ getContentPreview(postStats.hot_post.content) }}</p>
            <div class="post-stats">
              <a-space>
                <span>👁 {{ postStats.hot_post.view_count || 0 }}</span>
                <span>❤️ {{ postStats.hot_post.like_count || 0 }}</span>
                <span>💬 {{ postStats.hot_post.comment_count || 0 }}</span>
                <span>🔥 {{ postStats.hot_post.hot_score || 0 }}</span>
              </a-space>
            </div>
          </div>
        </a-card>
      </div>
    </a-card>

    <!-- 用户活跃度统计 -->
    <a-card title="用户活跃度" class="stats-card">
      <a-row :gutter="16">
        <a-col :span="12">
          <div class="chart-container">
            <h4>用户参与度分布</h4>
            <a-empty v-if="!userActivityData.length" description="暂无数据" />
            <div v-else class="activity-list">
              <div v-for="item in userActivityData" :key="item.level" class="activity-item">
                <span class="level">{{ item.level }}</span>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: item.percentage + '%' }"></div>
                </div>
                <span class="count">{{ item.count }}人</span>
              </div>
            </div>
          </div>
        </a-col>
        <a-col :span="12">
          <div class="chart-container">
            <h4>内容类型分布</h4>
            <a-empty v-if="!contentTypeData.length" description="暂无数据" />
            <div v-else class="content-types">
              <a-row :gutter="8">
                <a-col :span="12" v-for="item in contentTypeData" :key="item.type">
                  <a-statistic
                    :title="item.type"
                    :value="item.count"
                    :value-style="{ color: item.color }"
                  />
                </a-col>
              </a-row>
            </div>
          </div>
        </a-col>
      </a-row>
    </a-card>

    <!-- 实时数据 -->
    <a-card title="实时数据" class="stats-card">
      <a-row :gutter="16">
        <a-col :span="6">
          <a-statistic
            title="在线用户"
            :value="realtimeData.online_users"
            :value-style="{ color: '#3f8600' }"
          />
        </a-col>
        <a-col :span="6">
          <a-statistic
            title="本小时新帖"
            :value="realtimeData.hour_posts"
            :value-style="{ color: '#1890ff' }"
          />
        </a-col>
        <a-col :span="6">
          <a-statistic
            title="本小时评论"
            :value="realtimeData.hour_comments"
            :value-style="{ color: '#722ed1' }"
          />
        </a-col>
        <a-col :span="6">
          <a-statistic
            title="本小时点赞"
            :value="realtimeData.hour_likes"
            :value-style="{ color: '#eb2f96' }"
          />
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { message } from 'ant-design-vue'
import { ReloadOutlined } from '@ant-design/icons-vue'
import { socialTopicAPI, socialPostAPI } from '@/api/social'

// 响应式数据
const loading = ref(false)
const topicStats = ref(null)
const postStats = ref(null)

// 模拟数据
const userActivityData = ref([
  { level: '新手用户', count: 1250, percentage: 60 },
  { level: '活跃用户', count: 580, percentage: 28 },
  { level: '资深用户', count: 180, percentage: 9 },
  { level: '专家用户', count: 62, percentage: 3 }
])

const contentTypeData = ref([
  { type: '图文帖子', count: 2680, color: '#1890ff' },
  { type: '纯文字', count: 1520, color: '#52c41a' },
  { type: '图片分享', count: 890, color: '#faad14' },
  { type: '视频内容', count: 320, color: '#722ed1' }
])

const realtimeData = reactive({
  online_users: 156,
  hour_posts: 23,
  hour_comments: 87,
  hour_likes: 142
})

// 工具函数
const getContentPreview = (content) => {
  if (!content || typeof content !== 'string') return '无内容'
  return content.length > 100 ? content.substring(0, 100) + '...' : content
}

// 获取话题统计
const fetchTopicStats = async () => {
  try {
    const response = await socialTopicAPI.getTopicStats()
    if (response && response.success) {
      topicStats.value = response.data
    } else {
      // 设置默认数据
      topicStats.value = {
        total_topics: 0,
        active_topics: 0,
        hot_topics: 0,
        featured_topics: 0,
        top_topic: null
      }
    }
  } catch (error) {
    console.error('获取话题统计失败:', error)
    // 设置默认数据
    topicStats.value = {
      total_topics: 0,
      active_topics: 0,
      hot_topics: 0,
      featured_topics: 0,
      top_topic: null
    }
  }
}

// 获取帖子统计
const fetchPostStats = async () => {
  try {
    const response = await socialPostAPI.getPostStats()
    if (response && response.success) {
      postStats.value = response.data
    } else {
      // 设置默认数据
      postStats.value = {
        total_posts: 0,
        published_posts: 0,
        draft_posts: 0,
        hidden_posts: 0,
        today_posts: 0,
        pending_posts: 0,
        approved_posts: 0,
        rejected_posts: 0,
        hot_post: null
      }
    }
  } catch (error) {
    console.error('获取帖子统计失败:', error)
    // 设置默认数据
    postStats.value = {
      total_posts: 0,
      published_posts: 0,
      draft_posts: 0,
      hidden_posts: 0,
      today_posts: 0,
      pending_posts: 0,
      approved_posts: 0,
      rejected_posts: 0,
      hot_post: null
    }
  }
}

// 刷新数据
const refreshData = async () => {
  loading.value = true
  try {
    // 并行获取统计数据，即使某个失败也不影响其他的
    await Promise.allSettled([
      fetchTopicStats(),
      fetchPostStats()
    ])
    
    // 模拟实时数据更新
    realtimeData.online_users = Math.floor(Math.random() * 200) + 100
    realtimeData.hour_posts = Math.floor(Math.random() * 50) + 10
    realtimeData.hour_comments = Math.floor(Math.random() * 150) + 50
    realtimeData.hour_likes = Math.floor(Math.random() * 200) + 80
    
    message.success('数据刷新成功')
  } catch (error) {
    console.error('数据刷新失败:', error)
    message.warning('部分数据刷新失败，但页面已加载默认数据')
  } finally {
    loading.value = false
  }
}

// 定时刷新实时数据
let refreshTimer = null

const startAutoRefresh = () => {
  refreshTimer = setInterval(() => {
    realtimeData.online_users = Math.floor(Math.random() * 200) + 100
    realtimeData.hour_posts = Math.floor(Math.random() * 50) + 10
    realtimeData.hour_comments = Math.floor(Math.random() * 150) + 50
    realtimeData.hour_likes = Math.floor(Math.random() * 200) + 80
  }, 30000) // 30秒刷新一次
}

const stopAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

// 初始化
onMounted(() => {
  refreshData()
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style lang="scss" scoped>
.social-stats-management {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    h2 {
      margin: 0;
    }
  }
  
  .stats-card {
    margin-bottom: 16px;
  }
  
  .top-item {
    margin-top: 16px;
    
    h4 {
      margin-bottom: 8px;
      font-size: 14px;
      color: #666;
    }
  }
  
  .topic-info {
    .topic-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
      
      .topic-name {
        font-weight: 500;
      }
      
      .topic-color {
        width: 16px;
        height: 16px;
        border-radius: 2px;
        border: 1px solid #d9d9d9;
      }
    }
    
    .topic-desc {
      margin-bottom: 8px;
      color: #666;
      font-size: 12px;
    }
    
    .topic-stats {
      font-size: 12px;
    }
  }
  
  .post-info {
    h5 {
      margin-bottom: 8px;
    }
    
    p {
      margin-bottom: 8px;
      color: #666;
      font-size: 12px;
    }
    
    .post-stats {
      font-size: 12px;
    }
  }
  
  .chart-container {
    h4 {
      margin-bottom: 16px;
      font-size: 14px;
      color: #666;
    }
  }
  
  .activity-list {
    .activity-item {
      display: flex;
      align-items: center;
      margin-bottom: 12px;
      
      .level {
        width: 80px;
        font-size: 12px;
      }
      
      .progress-bar {
        flex: 1;
        height: 8px;
        background: #f0f0f0;
        border-radius: 4px;
        margin: 0 12px;
        position: relative;
        
        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #1890ff, #52c41a);
          border-radius: 4px;
          transition: width 0.3s;
        }
      }
      
      .count {
        width: 50px;
        font-size: 12px;
        text-align: right;
      }
    }
  }
  
  .content-types {
    .ant-statistic {
      text-align: center;
      margin-bottom: 16px;
    }
  }
}
</style> 