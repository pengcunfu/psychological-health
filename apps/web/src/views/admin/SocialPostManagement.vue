<template>
  <div class="social-post-management">
    <div class="page-header">
      <h2>帖子管理</h2>
      <a-space>
        <a-button @click="showStatsModal">
          <bar-chart-outlined />
          统计信息
        </a-button>
      </a-space>
    </div>

    <!-- 搜索筛选 -->
    <div class="search-section">
      <a-card>
        <a-form layout="inline" :model="searchForm" @finish="handleSearch">
          <a-form-item label="关键词">
            <a-input v-model:value="searchForm.keyword" placeholder="搜索标题或内容" allow-clear />
          </a-form-item>
          <a-form-item label="用户ID">
            <a-input v-model:value="searchForm.user_id" placeholder="请输入用户ID" allow-clear />
          </a-form-item>
          <a-form-item label="分类">
            <a-input v-model:value="searchForm.category" placeholder="请输入分类" allow-clear />
          </a-form-item>
          <a-form-item label="状态">
            <a-select v-model:value="searchForm.status" placeholder="请选择状态" allow-clear style="width: 120px">
              <a-select-option value="">全部</a-select-option>
              <a-select-option value="draft">草稿</a-select-option>
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
          :scroll="{ x: 1500 }"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'title'">
              <div class="post-title">
                <div class="title-text">{{ record.title || '无标题' }}</div>
                <div class="content-preview">{{ getContentPreview(record.content) }}</div>
              </div>
            </template>
            
            <template v-if="column.key === 'user_info'">
              <div v-if="record.user_info && !record.is_anonymous" class="user-info">
                <a-avatar :size="32" :src="record.user_info.avatar">
                  {{ record.user_info.username?.charAt(0).toUpperCase() }}
                </a-avatar>
                <div class="user-details">
                  <div>{{ record.user_info.username }}</div>
                  <div class="user-id">{{ record.user_info.id }}</div>
                </div>
              </div>
              <div v-else class="anonymous-user">
                <a-avatar :size="32">匿</a-avatar>
                <span>匿名用户</span>
              </div>
            </template>
            
            <template v-if="column.key === 'topics'">
              <a-space wrap>
                <a-tag v-for="topic in record.topics" :key="topic" color="blue" size="small">
                  {{ topic }}
                </a-tag>
              </a-space>
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
            
            <template v-if="column.key === 'flags'">
              <a-space>
                <a-tag v-if="record.is_top" color="red" size="small">置顶</a-tag>
                <a-tag v-if="record.is_featured" color="purple" size="small">精选</a-tag>
                <a-tag v-if="record.is_anonymous" color="gray" size="small">匿名</a-tag>
              </a-space>
            </template>
            
            <template v-if="column.key === 'stats'">
              <div class="stats-info">
                <div>👁 {{ record.view_count || 0 }}</div>
                <div>❤️ {{ record.like_count || 0 }}</div>
                <div>💬 {{ record.comment_count || 0 }}</div>
                <div>🔥 {{ record.hot_score || 0 }}</div>
              </div>
            </template>
            
            <template v-if="column.key === 'action'">
              <a-space>
                <a-button type="link" size="small" @click="showPostDetail(record)">查看</a-button>
                <a-button type="link" size="small" @click="showEditModal(record)">编辑</a-button>
                <a-dropdown>
                  <a-button type="link" size="small">
                    更多 <down-outlined />
                  </a-button>
                  <template #overlay>
                    <a-menu>
                      <a-menu-item key="audit" @click="showAuditModal(record)">
                        审核
                      </a-menu-item>
                      <a-menu-item key="top" @click="toggleTop(record)">
                        {{ record.is_top ? '取消置顶' : '置顶' }}
                      </a-menu-item>
                      <a-menu-item key="feature" @click="toggleFeature(record)">
                        {{ record.is_featured ? '取消精选' : '精选' }}
                      </a-menu-item>
                      <a-menu-divider />
                      <a-menu-item key="delete" @click="handleDelete(record.id)" danger>
                        删除
                      </a-menu-item>
                    </a-menu>
                  </template>
                </a-dropdown>
              </a-space>
            </template>
          </template>
        </a-table>
      </a-card>
    </div>

    <!-- 帖子详情模态框 -->
    <a-modal
      v-model:open="detailModalVisible"
      title="帖子详情"
      width="800px"
      :footer="null"
    >
      <div v-if="currentPost" class="post-detail">
        <div class="detail-header">
          <h3>{{ currentPost.title || '无标题' }}</h3>
          <div class="post-meta">
            <a-space>
              <span>发布时间: {{ currentPost.create_time }}</span>
              <span>分类: {{ currentPost.category || '无分类' }}</span>
              <span>位置: {{ currentPost.location || '无位置' }}</span>
            </a-space>
          </div>
        </div>
        
        <div class="detail-content">
          <div class="content-text">{{ currentPost.content }}</div>
          
          <div v-if="currentPost.images && currentPost.images.length" class="images-section">
            <h4>图片</h4>
            <a-space wrap>
              <a-image
                v-for="(image, index) in currentPost.images"
                :key="index"
                :src="image"
                :width="100"
                :height="100"
                style="object-fit: cover; border-radius: 4px;"
              />
            </a-space>
          </div>
          
          <div v-if="currentPost.topics && currentPost.topics.length" class="topics-section">
            <h4>话题标签</h4>
            <a-space wrap>
              <a-tag v-for="topic in currentPost.topics" :key="topic" color="blue">
                {{ topic }}
              </a-tag>
            </a-space>
          </div>
        </div>
      </div>
    </a-modal>

    <!-- 编辑帖子模态框 -->
    <a-modal
      v-model:open="editModalVisible"
      title="编辑帖子"
      :confirm-loading="submitLoading"
      @ok="handleUpdate"
      @cancel="handleEditCancel"
      width="600px"
    >
      <a-form
        ref="editFormRef"
        :model="editFormData"
        layout="vertical"
      >
        <a-form-item label="标题">
          <a-input v-model:value="editFormData.title" placeholder="请输入标题" />
        </a-form-item>
        
        <a-form-item label="分类">
          <a-input v-model:value="editFormData.category" placeholder="请输入分类" />
        </a-form-item>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="状态">
              <a-select v-model:value="editFormData.status">
                <a-select-option value="draft">草稿</a-select-option>
                <a-select-option value="published">已发布</a-select-option>
                <a-select-option value="hidden">隐藏</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="审核状态">
              <a-select v-model:value="editFormData.audit_status">
                <a-select-option value="pending">待审核</a-select-option>
                <a-select-option value="approved">通过</a-select-option>
                <a-select-option value="rejected">拒绝</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="是否置顶">
              <a-switch v-model:checked="editFormData.is_top" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="是否精选">
              <a-switch v-model:checked="editFormData.is_featured" />
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
    </a-modal>

    <!-- 审核模态框 -->
    <a-modal
      v-model:open="auditModalVisible"
      title="审核帖子"
      :confirm-loading="auditLoading"
      @ok="handleAudit"
      @cancel="handleAuditCancel"
    >
      <a-form layout="vertical">
        <a-form-item label="审核结果">
          <a-radio-group v-model:value="auditForm.audit_status">
            <a-radio value="approved">通过</a-radio>
            <a-radio value="rejected">拒绝</a-radio>
          </a-radio-group>
        </a-form-item>
        
        <a-form-item label="审核原因">
          <a-textarea 
            v-model:value="auditForm.audit_reason" 
            placeholder="请输入审核原因（拒绝时必填）" 
            :rows="4" 
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 统计信息模态框 -->
    <a-modal
      v-model:open="statsModalVisible"
      title="帖子统计信息"
      :footer="null"
      width="600px"
    >
      <div v-if="statsData" class="stats-content">
        <a-row :gutter="16">
          <a-col :span="8">
            <a-statistic title="总帖子数" :value="statsData.total_posts" />
          </a-col>
          <a-col :span="8">
            <a-statistic title="已发布" :value="statsData.published_posts" />
          </a-col>
          <a-col :span="8">
            <a-statistic title="今日新增" :value="statsData.today_posts" />
          </a-col>
        </a-row>
        
        <a-divider />
        
        <a-row :gutter="16">
          <a-col :span="6">
            <a-statistic title="草稿" :value="statsData.draft_posts" />
          </a-col>
          <a-col :span="6">
            <a-statistic title="隐藏" :value="statsData.hidden_posts" />
          </a-col>
          <a-col :span="6">
            <a-statistic title="待审核" :value="statsData.pending_posts" />
          </a-col>
          <a-col :span="6">
            <a-statistic title="已拒绝" :value="statsData.rejected_posts" />
          </a-col>
        </a-row>
        
        <a-divider />
        
        <div v-if="statsData.hot_post" class="hot-post-section">
          <h4>最热门帖子</h4>
          <a-card size="small">
            <div class="hot-post-info">
              <h5>{{ statsData.hot_post.title || '无标题' }}</h5>
              <p>{{ getContentPreview(statsData.hot_post.content) }}</p>
              <div class="hot-post-stats">
                <a-space>
                  <span>👁 {{ statsData.hot_post.view_count || 0 }}</span>
                  <span>❤️ {{ statsData.hot_post.like_count || 0 }}</span>
                  <span>💬 {{ statsData.hot_post.comment_count || 0 }}</span>
                  <span>🔥 {{ statsData.hot_post.hot_score || 0 }}</span>
                </a-space>
              </div>
            </div>
          </a-card>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { BarChartOutlined, DownOutlined } from '@ant-design/icons-vue'
import { socialPostAPI } from '@/api/social'

// 响应式数据
const loading = ref(false)
const submitLoading = ref(false)
const auditLoading = ref(false)
const detailModalVisible = ref(false)
const editModalVisible = ref(false)
const auditModalVisible = ref(false)
const statsModalVisible = ref(false)
const editFormRef = ref()

// 搜索表单
const searchForm = reactive({
  keyword: '',
  user_id: '',
  category: '',
  status: '',
  audit_status: ''
})

// 表格数据
const tableData = ref([])
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total) => `共 ${total} 条记录`
})

// 当前帖子
const currentPost = ref(null)
const editFormData = reactive({
  id: '',
  title: '',
  category: '',
  status: '',
  audit_status: '',
  is_top: false,
  is_featured: false
})

// 审核表单
const auditForm = reactive({
  audit_status: 'approved',
  audit_reason: ''
})

// 统计数据
const statsData = ref(null)

// 表格列定义
const columns = [
  {
    title: '标题内容',
    key: 'title',
    width: 300,
    fixed: 'left'
  },
  {
    title: '发布者',
    key: 'user_info',
    width: 120
  },
  {
    title: '分类',
    dataIndex: 'category',
    key: 'category',
    width: 100
  },
  {
    title: '话题标签',
    key: 'topics',
    width: 150
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
    title: '标记',
    key: 'flags',
    width: 120
  },
  {
    title: '统计信息',
    key: 'stats',
    width: 120
  },
  {
    title: '发布时间',
    dataIndex: 'create_time',
    key: 'create_time',
    width: 150,
    sorter: true
  },
  {
    title: '操作',
    key: 'action',
    width: 150,
    fixed: 'right'
  }
]

// 工具函数
const getContentPreview = (content) => {
  if (!content) return '无内容'
  return content.length > 100 ? content.substring(0, 100) + '...' : content
}

const getStatusColor = (status) => {
  const colors = {
    draft: 'default',
    published: 'green',
    hidden: 'orange',
    deleted: 'red'
  }
  return colors[status] || 'default'
}

const getStatusText = (status) => {
  const texts = {
    draft: '草稿',
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
    
    const response = await socialPostAPI.getSocialPosts(params)
    
    if (response.success) {
      tableData.value = response.data.list
      pagination.total = response.data.total
    } else {
      message.error(response.message || '获取数据失败')
    }
  } catch (error) {
    console.error('获取帖子列表失败:', error)
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

// 显示帖子详情
const showPostDetail = async (record) => {
  try {
    const response = await socialPostAPI.getSocialPost(record.id)
    if (response.success) {
      currentPost.value = response.data
      detailModalVisible.value = true
    }
  } catch (error) {
    message.error('获取帖子详情失败')
  }
}

// 显示编辑模态框
const showEditModal = (record) => {
  Object.keys(editFormData).forEach(key => {
    editFormData[key] = record[key] || editFormData[key]
  })
  editModalVisible.value = true
}

// 处理更新
const handleUpdate = async () => {
  try {
    submitLoading.value = true
    const updateData = { ...editFormData }
    delete updateData.id
    
    await socialPostAPI.updateSocialPost(editFormData.id, updateData)
    message.success('更新成功')
    editModalVisible.value = false
    fetchData()
  } catch (error) {
    message.error('更新失败')
  } finally {
    submitLoading.value = false
  }
}

// 取消编辑
const handleEditCancel = () => {
  editModalVisible.value = false
}

// 显示审核模态框
const showAuditModal = (record) => {
  currentPost.value = record
  auditForm.audit_status = record.audit_status || 'approved'
  auditForm.audit_reason = record.audit_reason || ''
  auditModalVisible.value = true
}

// 处理审核
const handleAudit = async () => {
  if (auditForm.audit_status === 'rejected' && !auditForm.audit_reason.trim()) {
    message.error('拒绝时必须填写审核原因')
    return
  }
  
  try {
    auditLoading.value = true
    await socialPostAPI.updateSocialPost(currentPost.value.id, auditForm)
    message.success('审核完成')
    auditModalVisible.value = false
    fetchData()
  } catch (error) {
    message.error('审核失败')
  } finally {
    auditLoading.value = false
  }
}

// 取消审核
const handleAuditCancel = () => {
  auditModalVisible.value = false
}

// 切换置顶状态
const toggleTop = async (record) => {
  try {
    await socialPostAPI.updateSocialPost(record.id, { is_top: !record.is_top })
    message.success(record.is_top ? '取消置顶成功' : '置顶成功')
    fetchData()
  } catch (error) {
    message.error('操作失败')
  }
}

// 切换精选状态
const toggleFeature = async (record) => {
  try {
    await socialPostAPI.updateSocialPost(record.id, { is_featured: !record.is_featured })
    message.success(record.is_featured ? '取消精选成功' : '精选成功')
    fetchData()
  } catch (error) {
    message.error('操作失败')
  }
}

// 删除帖子
const handleDelete = async (id) => {
  try {
    await socialPostAPI.deleteSocialPost(id)
    message.success('删除成功')
    fetchData()
  } catch (error) {
    message.error('删除失败')
  }
}

// 显示统计信息
const showStatsModal = async () => {
  try {
    const response = await socialPostAPI.getPostStats()
    if (response.success) {
      statsData.value = response.data
      statsModalVisible.value = true
    }
  } catch (error) {
    message.error('获取统计信息失败')
  }
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style lang="scss" scoped>
.social-post-management {
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
  
  .post-title {
    .title-text {
      font-weight: 500;
      margin-bottom: 4px;
    }
    
    .content-preview {
      font-size: 12px;
      color: #666;
      line-height: 1.4;
    }
  }
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .user-details {
      .user-id {
        font-size: 11px;
        color: #999;
      }
    }
  }
  
  .anonymous-user {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #999;
  }
  
  .stats-info {
    font-size: 12px;
    line-height: 1.5;
    
    div {
      margin-bottom: 2px;
    }
  }
}

.post-detail {
  .detail-header {
    margin-bottom: 16px;
    
    h3 {
      margin-bottom: 8px;
    }
    
    .post-meta {
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
    .topics-section {
      margin-bottom: 16px;
      
      h4 {
        margin-bottom: 8px;
        font-size: 14px;
      }
    }
  }
}

.stats-content {
  .hot-post-section {
    margin-top: 16px;
    
    .hot-post-info {
      h5 {
        margin-bottom: 8px;
      }
      
      p {
        margin-bottom: 8px;
        color: #666;
        font-size: 12px;
      }
      
      .hot-post-stats {
        font-size: 12px;
      }
    }
  }
}
</style> 