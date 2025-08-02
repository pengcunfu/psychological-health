<template>
  <div class="review-management">
    <div class="page-header">
      <h2>评价管理</h2>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch">
        <a-form-item label="咨询师ID">
          <a-input
              v-model:value="searchForm.counselor_id"
              placeholder="请输入咨询师ID"
              style="width: 150px;"
          />
        </a-form-item>
        <a-form-item label="订单ID">
          <a-input
              v-model:value="searchForm.order_id"
              placeholder="请输入订单ID"
              style="width: 150px;"
          />
        </a-form-item>
        <a-form-item label="评分">
          <a-select
              v-model:value="searchForm.rating"
              placeholder="请选择评分"
              style="width: 120px;"
              allow-clear
          >
            <a-select-option :value="5">5分</a-select-option>
            <a-select-option :value="4">4分</a-select-option>
            <a-select-option :value="3">3分</a-select-option>
            <a-select-option :value="2">2分</a-select-option>
            <a-select-option :value="1">1分</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="状态">
          <a-select
              v-model:value="searchForm.status"
              placeholder="请选择状态"
              style="width: 120px;"
              allow-clear
          >
            <a-select-option value="pending">待审核</a-select-option>
            <a-select-option value="approved">已通过</a-select-option>
            <a-select-option value="rejected">已拒绝</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
          <a-button style="margin-left: 8px;" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>
    </div>

    <!-- 评价列表 -->
    <a-table
        :columns="columns"
        :data-source="reviews"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
    >
      <template #rating="{ record }">
        <div class="rating-display">
          <a-rate :value="record.rating" disabled/>
          <span class="rating-text">{{ record.rating }}/5</span>
        </div>
      </template>

      <template #content="{ record }">
        <div class="review-content">
          <p class="content-text">{{ record.content }}</p>
          <div v-if="record.images && record.images.length" class="review-images">
            <a-image
                v-for="(img, index) in record.images.slice(0, 3)"
                :key="index"
                :src="img"
                width="40"
                height="40"
                style="object-fit: cover; border-radius: 4px; margin-right: 8px;"
            />
            <span v-if="record.images.length > 3" class="more-images">
              +{{ record.images.length - 3 }}
            </span>
          </div>
        </div>
      </template>

      <template #status="{ record }">
        <a-tag :color="getStatusColor(record.status)">
          {{ getStatusText(record.status) }}
        </a-tag>
      </template>

      <template #createTime="{ record }">
        {{ formatDate(record.create_time) }}
      </template>

      <template #action="{ record }">
        <a-space>
          <a-button type="link" size="small" @click="viewReview(record)">
            查看详情
          </a-button>
          <a-dropdown v-if="record.status === 'pending'">
            <a-button type="link" size="small">
              审核
              <DownOutlined/>
            </a-button>
            <template #overlay>
              <a-menu @click="({ key }) => handleAudit(record.id, key)">
                <a-menu-item key="approved">
                  <span style="color: #52c41a;">通过审核</span>
                </a-menu-item>
                <a-menu-item key="rejected">
                  <span style="color: #ff4d4f;">拒绝审核</span>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
          <a-popconfirm
              title="确定要删除这条评价吗？"
              @confirm="deleteReview(record.id)"
          >
            <a-button type="link" size="small" danger>
              删除
            </a-button>
          </a-popconfirm>
        </a-space>
      </template>
    </a-table>

    <!-- 查看评价详情弹窗 -->
    <a-modal
        v-model:open="viewModalVisible"
        title="评价详情"
        :footer="null"
        width="600px"
    >
      <div v-if="currentReview" class="review-detail">
        <div class="detail-header">
          <div class="rating-section">
            <a-rate :value="currentReview.rating" disabled/>
            <span class="rating-score">{{ currentReview.rating }}/5</span>
          </div>
          <a-tag :color="getStatusColor(currentReview.status)">
            {{ getStatusText(currentReview.status) }}
          </a-tag>
        </div>

        <a-divider/>

        <div class="detail-section">
          <h4>评价内容</h4>
          <p class="review-text">{{ currentReview.content || '用户未留下文字评价' }}</p>
        </div>

        <div v-if="currentReview.images && currentReview.images.length" class="detail-section">
          <h4>评价图片</h4>
          <div class="images-grid">
            <a-image
                v-for="(img, index) in currentReview.images"
                :key="index"
                :src="img"
                width="80"
                height="80"
                style="object-fit: cover; border-radius: 6px;"
            />
          </div>
        </div>

        <div class="detail-section">
          <h4>基本信息</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">咨询师ID：</span>
              <span>{{ currentReview.counselor_id }}</span>
            </div>
            <div class="info-item">
              <span class="label">订单ID：</span>
              <span>{{ currentReview.order_id }}</span>
            </div>
            <div class="info-item">
              <span class="label">用户ID：</span>
              <span>{{ currentReview.user_id }}</span>
            </div>
            <div class="info-item">
              <span class="label">评价时间：</span>
              <span>{{ formatDate(currentReview.create_time) }}</span>
            </div>
          </div>
        </div>

        <div v-if="currentReview.status === 'pending'" class="detail-section">
          <h4>审核操作</h4>
          <a-space>
            <a-button
                type="primary"
                @click="handleAudit(currentReview.id, 'approved')"
            >
              通过审核
            </a-button>
            <a-button
                danger
                @click="handleAudit(currentReview.id, 'rejected')"
            >
              拒绝审核
            </a-button>
          </a-space>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script>
import {ref, reactive, onMounted} from 'vue'
import {message} from 'ant-design-vue'
import {DownOutlined} from '@ant-design/icons-vue'
import {reviewAPI} from '@/api/admin'

export default {
  name: 'ReviewManagement',
  components: {
    DownOutlined
  },
  setup() {
    const loading = ref(false)
    const reviews = ref([])
    const viewModalVisible = ref(false)
    const currentReview = ref(null)

    const searchForm = reactive({
      counselor_id: '',
      order_id: '',
      rating: undefined,
      status: undefined
    })

    const pagination = reactive({
      current: 1,
      pageSize: 10,
      total: 0,
      showSizeChanger: true,
      showQuickJumper: true,
      showTotal: (total) => `共 ${total} 条记录`
    })

    const columns = [
      {
        title: '咨询师ID',
        dataIndex: 'counselor_id',
        key: 'counselor_id',
        width: 120
      },
      {
        title: '订单ID',
        dataIndex: 'order_id',
        key: 'order_id',
        width: 120
      },
      {
        title: '评分',
        dataIndex: 'rating',
        key: 'rating',
        slots: {customRender: 'rating'},
        width: 150
      },
      {
        title: '评价内容',
        dataIndex: 'content',
        key: 'content',
        slots: {customRender: 'content'},
        width: 300
      },
      {
        title: '审核状态',
        dataIndex: 'status',
        key: 'status',
        slots: {customRender: 'status'},
        width: 100
      },
      {
        title: '评价时间',
        dataIndex: 'create_time',
        key: 'create_time',
        slots: {customRender: 'createTime'},
        width: 150
      },
      {
        title: '操作',
        key: 'action',
        slots: {customRender: 'action'},
        width: 180
      }
    ]

    // 获取评价列表
    const fetchReviews = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          counselor_id: searchForm.counselor_id,
          order_id: searchForm.order_id,
          rating: searchForm.rating,
          status: searchForm.status
        }

        const result = await reviewAPI.getReviews(params)
        if (result.code === 200) {
          reviews.value = result.data.list
          pagination.total = result.data.total
        }
      } catch (error) {
        message.error('获取评价列表失败')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current = 1
      fetchReviews()
    }

    // 重置搜索
    const resetSearch = () => {
      Object.assign(searchForm, {
        counselor_id: '',
        order_id: '',
        rating: undefined,
        status: undefined
      })
      pagination.current = 1
      fetchReviews()
    }

    // 表格分页改变
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchReviews()
    }

    // 查看评价详情
    const viewReview = (review) => {
      currentReview.value = review
      viewModalVisible.value = true
    }

    // 审核评价
    const handleAudit = async (reviewId, status) => {
      try {
        const result = await reviewAPI.auditReview(reviewId, status)
        if (result.code === 200) {
          message.success(status === 'approved' ? '审核通过' : '审核拒绝')
          fetchReviews()
          if (viewModalVisible.value) {
            viewModalVisible.value = false
          }
        }
      } catch (error) {
        message.error('审核操作失败')
      }
    }

    // 删除评价
    const deleteReview = async (reviewId) => {
      try {
        const result = await reviewAPI.deleteReview(reviewId)
        if (result.code === 200) {
          message.success('删除成功')
          fetchReviews()
        }
      } catch (error) {
        message.error('删除失败')
      }
    }

    // 获取状态颜色
    const getStatusColor = (status) => {
      const colorMap = {
        pending: 'orange',
        approved: 'green',
        rejected: 'red'
      }
      return colorMap[status] || 'default'
    }

    // 获取状态文本
    const getStatusText = (status) => {
      const textMap = {
        pending: '待审核',
        approved: '已通过',
        rejected: '已拒绝'
      }
      return textMap[status] || '未知'
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }

    onMounted(() => {
      fetchReviews()
    })

    return {
      loading,
      reviews,
      searchForm,
      pagination,
      columns,
      viewModalVisible,
      currentReview,
      fetchReviews,
      handleSearch,
      resetSearch,
      handleTableChange,
      viewReview,
      handleAudit,
      deleteReview,
      getStatusColor,
      getStatusText,
      formatDate
    }
  }
}
</script>

<style scoped>
.review-management {
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
  color: #1890ff;
}

.search-bar {
  background: white;
  padding: 16px;
  border-radius: 6px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-text {
  font-weight: 500;
  color: #666;
}

.review-content {
  max-width: 280px;
}

.content-text {
  margin: 0 0 8px 0;
  font-size: 14px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.review-images {
  display: flex;
  align-items: center;
}

.more-images {
  font-size: 12px;
  color: #999;
}

.review-detail {
  padding: 16px 0;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.rating-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rating-score {
  font-size: 16px;
  font-weight: 600;
  color: #fa8c16;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section h4 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.review-text {
  line-height: 1.6;
  margin: 0;
}

.images-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.info-item {
  display: flex;
  align-items: center;
}

.info-item .label {
  font-weight: 500;
  color: #666;
  margin-right: 8px;
  min-width: 80px;
}

@media (max-width: 768px) {
  .review-management {
    padding: 12px;
  }

  .page-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .search-bar .ant-form {
    flex-direction: column;
  }

  .search-bar .ant-form-item {
    margin-bottom: 8px;
  }

  .detail-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .review-content {
    max-width: 200px;
  }
}
</style> 