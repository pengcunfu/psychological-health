<template>
  <div class="social-comment-management">
    <div class="page-header">
      <h2>评论管理</h2>
    </div>

    <!-- 搜索筛选 -->
    <div class="search-section">
      <a-card>
        <a-form layout="inline" :model="searchForm" @finish="handleSearch">
          <a-form-item label="关键词">
            <a-input v-model:value="searchForm.keyword" placeholder="搜索评论内容" allow-clear />
          </a-form-item>
          <a-form-item label="帖子ID">
            <a-input v-model:value="searchForm.post_id" placeholder="请输入帖子ID" allow-clear />
          </a-form-item>
          <a-form-item label="用户ID">
            <a-input v-model:value="searchForm.user_id" placeholder="请输入用户ID" allow-clear />
          </a-form-item>
          <a-form-item label="状态">
            <a-select v-model:value="searchForm.status" placeholder="请选择状态" allow-clear style="width: 120px">
              <a-select-option value="">全部</a-select-option>
              <a-select-option value="published">已发布</a-select-option>
              <a-select-option value="hidden">隐藏</a-select-option>
              <a-select-option value="deleted">已删除</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="审核状态">
            <a-select v-model:value="searchForm.audit_status" placeholder="请选择审核状态" allow-clear style="width: 120px">
              <a-select-option value="">全部</a-select-option>
              <a-select-option value="pending">待审核</a-select-option>
              <a-select-option value="approved">通过</a-select-option>
              <a-select-option value="rejected">拒绝</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item>
            <a-space>
              <a-button type="primary" html-type="submit">搜索</a-button>
              <a-button @click="resetSearch">重置</a-button>
            </a-space>
          </a-form-item>
        </a-form>
      </a-card>
    </div>

    <!-- 数据表格 -->
    <div class="table-section">
      <a-card>
        <a-table
          :columns="columns"
          :data-source="tableData"
          :pagination="pagination"
          :loading="loading"
          row-key="id"
          @change="handleTableChange"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'content'">
              <div class="comment-content">
                {{ getContentPreview(record.content) }}
              </div>
            </template>
            
            <template v-if="column.key === 'user_info'">
              <div v-if="record.user_info && !record.is_anonymous" class="user-info">
                <a-avatar :size="24" :src="record.user_info.avatar">
                  {{ record.user_info.username?.charAt(0).toUpperCase() }}
                </a-avatar>
                <span class="username">{{ record.user_info.username }}</span>
              </div>
              <div v-else class="anonymous-user">
                <a-avatar :size="24">匿</a-avatar>
                <span>匿名用户</span>
              </div>
            </template>
            
            <template v-if="column.key === 'status'">
              <a-tag :color="getStatusColor(record.status)">
                {{ getStatusText(record.status) }}
              </a-tag>
            </template>
            
            <template v-if="column.key === 'audit_status'">
              <a-tag :color="getAuditStatusColor(record.audit_status)">
                {{ getAuditStatusText(record.audit_status) }}
              </a-tag>
            </template>
            
            <template v-if="column.key === 'is_reply'">
              <a-tag v-if="record.parent_id" color="blue" size="small">回复</a-tag>
              <a-tag v-else color="default" size="small">评论</a-tag>
            </template>
            
            <template v-if="column.key === 'stats'">
              <div class="stats-info">
                <div>❤️ {{ record.like_count || 0 }}</div>
                <div>💬 {{ record.reply_count || 0 }}</div>
              </div>
            </template>
            
            <template v-if="column.key === 'action'">
              <a-space>
                <a-button type="link" size="small" @click="showCommentDetail(record)">查看</a-button>
                <a-popconfirm
                  title="确定要删除这条评论吗？"
                  ok-text="确定"
                  cancel-text="取消"
                  @confirm="handleDelete(record.id)"
                >
                  <a-button type="link" size="small" danger>删除</a-button>
                </a-popconfirm>
              </a-space>
            </template>
          </template>
        </a-table>
      </a-card>
    </div>

    <!-- 评论详情模态框 -->
    <a-modal
      v-model:open="detailModalVisible"
      title="评论详情"
      width="600px"
      :footer="null"
    >
      <div v-if="currentComment" class="comment-detail">
        <div class="detail-header">
          <div class="comment-meta">
            <a-space>
              <span>评论时间: {{ currentComment.create_time }}</span>
              <span>帖子ID: {{ currentComment.post_id }}</span>
              <span v-if="currentComment.parent_id">父评论ID: {{ currentComment.parent_id }}</span>
            </a-space>
          </div>
        </div>
        
        <div class="detail-content">
          <div class="content-text">{{ currentComment.content }}</div>
          
          <div v-if="currentComment.images && currentComment.images.length" class="images-section">
            <h4>图片</h4>
            <a-space wrap>
              <a-image
                v-for="(image, index) in currentComment.images"
                :key="index"
                :src="image"
                :width="100"
                :height="100"
                style="object-fit: cover; border-radius: 4px;"
              />
            </a-space>
          </div>
          
          <div v-if="currentComment.location" class="location-section">
            <h4>位置信息</h4>
            <p>{{ currentComment.location }}</p>
          </div>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { socialCommentAPI } from '@/api/social'

// 响应式数据
const loading = ref(false)
const detailModalVisible = ref(false)

// 搜索表单
const searchForm = reactive({
  keyword: '',
  post_id: '',
  user_id: '',
  status: '',
  audit_status: ''
})

// 表格数据
const tableData = ref([])
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total) => `共 ${total} 条记录`
})

// 当前评论
const currentComment = ref(null)

// 表格列定义
const columns = [
  {
    title: '评论内容',
    key: 'content',
    width: 300
  },
  {
    title: '评论者',
    key: 'user_info',
    width: 120
  },
  {
    title: '帖子ID',
    dataIndex: 'post_id',
    key: 'post_id',
    width: 120
  },
  {
    title: '类型',
    key: 'is_reply',
    width: 80
  },
  {
    title: '状态',
    key: 'status',
    width: 80
  },
  {
    title: '审核状态',
    key: 'audit_status',
    width: 100
  },
  {
    title: '统计',
    key: 'stats',
    width: 80
  },
  {
    title: '评论时间',
    dataIndex: 'create_time',
    key: 'create_time',
    width: 150,
    sorter: true
  },
  {
    title: '操作',
    key: 'action',
    width: 120,
    fixed: 'right'
  }
]

// 工具函数
const getContentPreview = (content) => {
  if (!content) return '无内容'
  return content.length > 50 ? content.substring(0, 50) + '...' : content
}

const getStatusColor = (status) => {
  const colors = {
    published: 'green',
    hidden: 'orange',
    deleted: 'red'
  }
  return colors[status] || 'default'
}

const getStatusText = (status) => {
  const texts = {
    published: '已发布',
    hidden: '隐藏',
    deleted: '已删除'
  }
  return texts[status] || status
}

const getAuditStatusColor = (auditStatus) => {
  const colors = {
    pending: 'orange',
    approved: 'green',
    rejected: 'red'
  }
  return colors[auditStatus] || 'default'
}

const getAuditStatusText = (auditStatus) => {
  const texts = {
    pending: '待审核',
    approved: '通过',
    rejected: '拒绝'
  }
  return texts[auditStatus] || auditStatus
}

// 获取数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.current,
      per_page: pagination.pageSize,
      ...searchForm
    }
    
    const response = await socialCommentAPI.getSocialComments(params)
    
    if (response.success) {
      tableData.value = response.data.list
      pagination.total = response.data.total
    } else {
      message.error(response.message || '获取数据失败')
    }
  } catch (error) {
    console.error('获取评论列表失败:', error)
    message.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  fetchData()
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  pagination.current = 1
  fetchData()
}

// 表格变化处理
const handleTableChange = (pag, filters, sorter) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchData()
}

// 显示评论详情
const showCommentDetail = (record) => {
  currentComment.value = record
  detailModalVisible.value = true
}

// 删除评论
const handleDelete = async (id) => {
  try {
    await socialCommentAPI.deleteSocialComment(id)
    message.success('删除成功')
    fetchData()
  } catch (error) {
    console.error('删除失败:', error)
    if (error.response?.data?.message) {
      message.error(error.response.data.message)
    } else {
      message.error('删除失败')
    }
  }
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style lang="scss" scoped>
.social-comment-management {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    h2 {
      margin: 0;
    }
  }
  
  .search-section {
    margin-bottom: 16px;
  }
  
  .comment-content {
    line-height: 1.4;
    word-break: break-word;
  }
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .username {
      font-size: 12px;
    }
  }
  
  .anonymous-user {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #999;
    font-size: 12px;
  }
  
  .stats-info {
    font-size: 12px;
    line-height: 1.5;
  }
}

.comment-detail {
  .detail-header {
    margin-bottom: 16px;
    
    .comment-meta {
      font-size: 12px;
      color: #666;
    }
  }
  
  .detail-content {
    .content-text {
      margin-bottom: 16px;
      line-height: 1.6;
    }
    
    .images-section,
    .location-section {
      margin-bottom: 16px;
      
      h4 {
        margin-bottom: 8px;
        font-size: 14px;
      }
    }
  }
}
</style> 