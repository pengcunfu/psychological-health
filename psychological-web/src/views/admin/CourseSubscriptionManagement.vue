<template>
  <div class="course-subscription-management">
    <!-- 搜索栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="订阅类型">
          <a-select
              v-model:value="searchForm.subscription_type"
              placeholder="请选择订阅类型"
              style="width: 150px;"
              allow-clear
          >
            <a-select-option value="standard">标准订阅</a-select-option>
            <a-select-option value="premium">高级订阅</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="状态">
          <a-select
              v-model:value="searchForm.status"
              placeholder="请选择状态"
              style="width: 120px;"
              allow-clear
          >
            <a-select-option value="active">有效</a-select-option>
            <a-select-option value="expired">已过期</a-select-option>
            <a-select-option value="cancelled">已取消</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="用户ID">
          <a-input
              v-model:value="searchForm.user_id"
              placeholder="请输入用户ID"
              style="width: 200px;"
              allow-clear
          />
        </a-form-item>
        <a-form-item label="课程ID">
          <a-input
              v-model:value="searchForm.course_id"
              placeholder="请输入课程ID"
              style="width: 200px;"
              allow-clear
          />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
          <a-button style="margin-left: 8px;" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>

      <div class="action-buttons">
        <a-button type="primary" @click="showCreateModal">
          <plus-outlined />
          新增订阅
        </a-button>
        <a-button @click="exportData">
          <export-outlined />
          导出数据
        </a-button>
      </div>
    </div>

    <!-- 订阅列表 -->
    <a-table
        :columns="columns"
        :data-source="subscriptions"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'subscription_type'">
          <a-tag :color="record.subscription_type === 'standard' ? 'blue' : 'purple'">
            {{ record.subscription_type === 'standard' ? '标准订阅' : '高级订阅' }}
          </a-tag>
        </template>

        <template v-if="column.key === 'status'">
          <a-tag :color="getStatusColor(record.status)">
            {{ record.status_text }}
          </a-tag>
        </template>

        <template v-if="column.key === 'progress'">
          <a-progress 
            :percent="Math.round(record.progress_percentage)" 
            size="small" 
            :status="record.progress_percentage === 100 ? 'success' : 'active'"
          />
        </template>

        <template v-if="column.key === 'paid_price'">
          ¥{{ record.paid_price?.toFixed(2) }}
        </template>

        <template v-if="column.key === 'course_info'">
          <div v-if="record.course_info">
            <div class="course-title">{{ record.course_info.title }}</div>
            <div class="course-teacher text-gray">{{ record.course_info.teacher }}</div>
          </div>
          <span v-else class="text-gray">-</span>
        </template>

        <template v-if="column.key === 'user_info'">
          <div v-if="record.user_info">
            <div>{{ record.user_info.username }}</div>
            <div class="text-gray">{{ record.user_info.phone }}</div>
          </div>
          <span v-else class="text-gray">-</span>
        </template>

        <template v-if="column.key === 'subscription_date'">
          {{ formatDate(record.subscription_date) }}
        </template>

        <template v-if="column.key === 'expiry_date'">
          {{ record.expiry_date ? formatDate(record.expiry_date) : '永久有效' }}
        </template>

        <template v-if="column.key === 'action'">
          <a-space>
            <a-button type="link" size="small" @click="viewDetail(record)">
              查看
            </a-button>
            <a-button type="link" size="small" @click="editSubscription(record)">
              编辑
            </a-button>
            <a-dropdown>
              <a-button type="link" size="small">
                更多 <down-outlined />
              </a-button>
              <template #overlay>
                <a-menu>
                  <a-menu-item v-if="record.status === 'active'" @click="extendSubscription(record)">
                    延长订阅
                  </a-menu-item>
                  <a-menu-item v-if="record.status === 'active'" @click="cancelSubscription(record)">
                    取消订阅
                  </a-menu-item>
                  <a-menu-divider />
                  <a-menu-item danger @click="deleteSubscription(record)">
                    删除记录
                  </a-menu-item>
                </a-menu>
              </template>
            </a-dropdown>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 创建/编辑订阅模态框 -->
    <a-modal
        v-model:open="modalVisible"
        :title="isEditing ? '编辑订阅' : '新增订阅'"
        @ok="handleSubmit"
        @cancel="handleCancel"
        :confirm-loading="submitting"
        width="800px"
    >
      <a-form
          :model="formData"
          :rules="formRules"
          ref="formRef"
          layout="vertical"
      >
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="课程ID" name="course_id">
              <a-input v-model:value="formData.course_id" placeholder="请输入课程ID" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="订阅类型" name="subscription_type">
              <a-select v-model:value="formData.subscription_type" placeholder="请选择订阅类型">
                <a-select-option value="standard">标准订阅</a-select-option>
                <a-select-option value="premium">高级订阅</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="支付价格" name="paid_price">
              <a-input-number 
                v-model:value="formData.paid_price" 
                placeholder="支付价格"
                :min="0"
                :precision="2"
                style="width: 100%"
                addon-before="¥"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="原价" name="original_price">
              <a-input-number 
                v-model:value="formData.original_price" 
                placeholder="原价"
                :min="0"
                :precision="2"
                style="width: 100%"
                addon-before="¥"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="折扣金额" name="discount_amount">
              <a-input-number 
                v-model:value="formData.discount_amount" 
                placeholder="折扣金额"
                :min="0"
                :precision="2"
                style="width: 100%"
                addon-before="¥"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="订单ID" name="order_id">
              <a-input v-model:value="formData.order_id" placeholder="关联订单ID" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="支付方式" name="payment_method">
              <a-input v-model:value="formData.payment_method" placeholder="支付方式" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="支付交易ID" name="payment_transaction_id">
          <a-input v-model:value="formData.payment_transaction_id" placeholder="支付交易ID" />
        </a-form-item>

        <a-form-item label="备注" name="notes">
          <a-textarea v-model:value="formData.notes" placeholder="备注信息" :rows="3" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 延长订阅模态框 -->
    <a-modal
        v-model:open="extendModalVisible"
        title="延长订阅"
        @ok="handleExtendSubmit"
        @cancel="extendModalVisible = false"
        :confirm-loading="extending"
    >
      <a-form layout="vertical">
        <a-form-item label="延长天数">
          <a-input-number 
            v-model:value="extendDays" 
            placeholder="请输入延长天数"
            :min="1"
            :max="365"
            style="width: 100%"
            addon-after="天"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 取消订阅模态框 -->
    <a-modal
        v-model:open="cancelModalVisible"
        title="取消订阅"
        @ok="handleCancelSubmit"
        @cancel="cancelModalVisible = false"
        :confirm-loading="cancelling"
    >
      <a-form layout="vertical">
        <a-form-item label="取消原因">
          <a-textarea 
            v-model:value="cancelReason" 
            placeholder="请输入取消原因"
            :rows="3"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { courseSubscriptionAPI } from '@/api/course_subscription'
import { 
  PlusOutlined, 
  ExportOutlined, 
  DownOutlined 
} from '@ant-design/icons-vue'

// 响应式数据
const loading = ref(false)
const subscriptions = ref([])
const modalVisible = ref(false)
const extendModalVisible = ref(false)
const cancelModalVisible = ref(false)
const isEditing = ref(false)
const submitting = ref(false)
const extending = ref(false)
const cancelling = ref(false)
const formRef = ref()

// 搜索表单
const searchForm = reactive({
  subscription_type: undefined,
  status: undefined,
  user_id: undefined,
  course_id: undefined
})

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total) => `共 ${total} 条记录`
})

// 表单数据
const formData = reactive({
  course_id: '',
  subscription_type: 'standard',
  paid_price: 0,
  original_price: 0,
  discount_amount: 0,
  order_id: '',
  payment_method: '',
  payment_transaction_id: '',
  notes: ''
})

// 延长和取消相关
const currentRecord = ref(null)
const extendDays = ref(30)
const cancelReason = ref('')

// 表单验证规则
const formRules = {
  course_id: [
    { required: true, message: '请输入课程ID' }
  ],
  paid_price: [
    { required: true, message: '请输入支付价格' }
  ],
  original_price: [
    { required: true, message: '请输入原价' }
  ]
}

// 表格列配置
const columns = [
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
    width: 100,
    ellipsis: true
  },
  {
    title: '用户信息',
    key: 'user_info',
    width: 150
  },
  {
    title: '课程信息',
    key: 'course_info',
    width: 200
  },
  {
    title: '订阅类型',
    key: 'subscription_type',
    width: 100
  },
  {
    title: '状态',
    key: 'status',
    width: 80
  },
  {
    title: '学习进度',
    key: 'progress',
    width: 120
  },
  {
    title: '支付金额',
    key: 'paid_price',
    width: 100
  },
  {
    title: '订阅时间',
    key: 'subscription_date',
    width: 120
  },
  {
    title: '过期时间',
    key: 'expiry_date',
    width: 120
  },
  {
    title: '操作',
    key: 'action',
    width: 150,
    fixed: 'right'
  }
]

// 方法
const fetchSubscriptions = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.current,
      per_page: pagination.pageSize,
      ...searchForm
    }

    const response = await courseSubscriptionAPI.getCourseSubscriptions(params)
    if (response.data) {
      subscriptions.value = response.data.list || []
      pagination.total = response.data.total || 0
    }
  } catch (error) {
    console.error('获取订阅列表失败:', error)
    message.error('获取订阅列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.current = 1
  fetchSubscriptions()
}

const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = undefined
  })
  pagination.current = 1
  fetchSubscriptions()
}

const handleTableChange = (pag) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchSubscriptions()
}

const showCreateModal = () => {
  isEditing.value = false
  modalVisible.value = true
  resetFormData()
}

const editSubscription = (record) => {
  isEditing.value = true
  modalVisible.value = true
  currentRecord.value = record
  Object.assign(formData, {
    course_id: record.course_id,
    subscription_type: record.subscription_type,
    paid_price: record.paid_price,
    original_price: record.original_price,
    discount_amount: record.discount_amount,
    order_id: record.order_id,
    payment_method: record.payment_method,
    payment_transaction_id: record.payment_transaction_id,
    notes: record.notes
  })
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    submitting.value = true

    if (isEditing.value) {
      await courseSubscriptionAPI.updateCourseSubscription(currentRecord.value.id, formData)
      message.success('订阅更新成功')
    } else {
      await courseSubscriptionAPI.createCourseSubscription(formData)
      message.success('订阅创建成功')
    }

    modalVisible.value = false
    fetchSubscriptions()
  } catch (error) {
    console.error('提交失败:', error)
    message.error('操作失败')
  } finally {
    submitting.value = false
  }
}

const handleCancel = () => {
  modalVisible.value = false
  resetFormData()
}

const resetFormData = () => {
  Object.assign(formData, {
    course_id: '',
    subscription_type: 'standard',
    paid_price: 0,
    original_price: 0,
    discount_amount: 0,
    order_id: '',
    payment_method: '',
    payment_transaction_id: '',
    notes: ''
  })
}

const viewDetail = (record) => {
  // 可以实现详情查看功能
  message.info('查看详情功能待实现')
}

const extendSubscription = (record) => {
  currentRecord.value = record
  extendDays.value = 30
  extendModalVisible.value = true
}

const handleExtendSubmit = async () => {
  try {
    extending.value = true
    await courseSubscriptionAPI.extendSubscription(currentRecord.value.id, {
      days: extendDays.value
    })
    message.success('订阅延长成功')
    extendModalVisible.value = false
    fetchSubscriptions()
  } catch (error) {
    console.error('延长订阅失败:', error)
    message.error('延长订阅失败')
  } finally {
    extending.value = false
  }
}

const cancelSubscription = (record) => {
  currentRecord.value = record
  cancelReason.value = ''
  cancelModalVisible.value = true
}

const handleCancelSubmit = async () => {
  try {
    cancelling.value = true
    await courseSubscriptionAPI.cancelSubscription(currentRecord.value.id, {
      reason: cancelReason.value
    })
    message.success('订阅取消成功')
    cancelModalVisible.value = false
    fetchSubscriptions()
  } catch (error) {
    console.error('取消订阅失败:', error)
    message.error('取消订阅失败')
  } finally {
    cancelling.value = false
  }
}

const deleteSubscription = (record) => {
  const modal = message.loading('删除中...', 0)
  courseSubscriptionAPI.deleteCourseSubscription(record.id)
    .then(() => {
      modal()
      message.success('删除成功')
      fetchSubscriptions()
    })
    .catch(error => {
      modal()
      console.error('删除失败:', error)
      message.error('删除失败')
    })
}

const exportData = () => {
  message.info('导出功能待实现')
}

const getStatusColor = (status) => {
  const colorMap = {
    active: 'green',
    expired: 'red',
    cancelled: 'gray'
  }
  return colorMap[status] || 'default'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  try {
    return new Date(dateStr).toLocaleDateString('zh-CN')
  } catch {
    return dateStr
  }
}

// 生命周期
onMounted(() => {
  fetchSubscriptions()
})
</script>

<style lang="scss" scoped>
.course-subscription-management {
  background: white;
  padding: 24px;
  border-radius: 8px;
}

.search-and-action-bar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.search-form {
  flex: 1;
  min-width: 300px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.course-title {
  font-weight: 500;
  color: #1890ff;
}

.course-teacher {
  font-size: 12px;
  margin-top: 2px;
}

.text-gray {
  color: #666;
}

:deep(.ant-table) {
  .ant-table-tbody > tr > td {
    padding: 12px 8px;
  }
}

:deep(.ant-progress) {
  .ant-progress-text {
    font-size: 12px;
  }
}

@media (max-width: 768px) {
  .search-and-action-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .action-buttons {
    justify-content: flex-start;
  }
}
</style> 