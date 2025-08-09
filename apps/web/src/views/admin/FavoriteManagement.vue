<template>
  <div class="favorite-management">
    <!-- 搜索栏和操作栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="用户ID">
          <a-input v-model:value="searchForm.user_id" placeholder="请输入用户ID" style="width: 200px;" />
        </a-form-item>
        <a-form-item label="收藏类型">
          <a-select v-model:value="searchForm.item_type" placeholder="请选择收藏类型" style="width: 150px;" allow-clear>
            <a-select-option value="course">课程</a-select-option>
            <a-select-option value="counselor">咨询师</a-select-option>
            <a-select-option value="assessment">测评</a-select-option>
            <a-select-option value="article">文章</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="收藏项ID">
          <a-input v-model:value="searchForm.item_id" placeholder="请输入收藏项ID" style="width: 200px;" />
        </a-form-item>
        <a-form-item label="时间范围">
          <a-range-picker 
            v-model:value="searchForm.dateRange" 
            style="width: 240px;" 
            :placeholder="['开始时间', '结束时间']"
          />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
          <a-button style="margin-left: 8px;" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>

      <div class="action-buttons">
        <a-button type="primary" @click="showAddModal">
          <plus-outlined />
          添加收藏
        </a-button>
        <a-button @click="batchDelete" :disabled="selectedRowKeys.length === 0">
          <delete-outlined />
          批量删除
        </a-button>
        <a-button @click="exportData">
          <export-outlined />
          导出数据
        </a-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <a-row :gutter="16">
        <a-col :span="6">
          <a-card size="small">
            <a-statistic title="总收藏数" :value="stats.total_favorites" />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card size="small">
            <a-statistic title="课程收藏" :value="stats.course_favorites" />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card size="small">
            <a-statistic title="咨询师收藏" :value="stats.counselor_favorites" />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card size="small">
            <a-statistic title="今日新增" :value="stats.today_favorites" />
          </a-card>
        </a-col>
      </a-row>
    </div>

    <!-- 收藏列表 -->
    <a-table 
      :columns="columns" 
      :data-source="favorites" 
      :loading="loading" 
      :pagination="pagination"
      @change="handleTableChange" 
      row-key="id"
      :row-selection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }"
      :scroll="{ x: 1000 }"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'user_info'">
          <div v-if="record.user_info">
            <div class="user-name">{{ record.user_info.username }}</div>
            <div class="user-phone text-gray">{{ record.user_info.phone }}</div>
          </div>
          <span v-else class="text-gray">用户ID: {{ record.user_id }}</span>
        </template>

        <template v-if="column.key === 'item_type'">
          <a-tag :color="getItemTypeColor(record.item_type)">
            {{ getItemTypeText(record.item_type) }}
          </a-tag>
        </template>

        <template v-if="column.key === 'item_info'">
          <div class="item-info">
            <div class="item-title">{{ record.item_title || record.item_id }}</div>
            <div class="item-desc text-gray">{{ record.item_description || '-' }}</div>
          </div>
        </template>

        <template v-if="column.key === 'create_time'">
          {{ formatDateTime(record.create_time) }}
        </template>

        <template v-if="column.key === 'action'">
          <a-space>
            <a-button type="link" size="small" @click="viewDetail(record)">
              查看详情
            </a-button>
            <a-button type="link" size="small" @click="editFavorite(record)">
              编辑
            </a-button>
            <a-button type="link" size="small" danger @click="deleteFavorite(record)">
              删除
            </a-button>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 添加/编辑收藏模态框 -->
    <a-modal
      v-model:open="modalVisible"
      :title="isEditing ? '编辑收藏' : '添加收藏'"
      @ok="handleSubmit"
      @cancel="handleCancel"
      :confirm-loading="submitting"
      width="600px"
    >
      <a-form
        :model="formData"
        :rules="formRules"
        ref="formRef"
        layout="vertical"
      >
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="用户ID" name="user_id">
              <a-input v-model:value="formData.user_id" placeholder="请输入用户ID" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="收藏类型" name="item_type">
              <a-select v-model:value="formData.item_type" placeholder="请选择收藏类型">
                <a-select-option value="course">课程</a-select-option>
                <a-select-option value="counselor">咨询师</a-select-option>
                <a-select-option value="assessment">测评</a-select-option>
                <a-select-option value="article">文章</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="收藏项ID" name="item_id">
          <a-input v-model:value="formData.item_id" placeholder="请输入收藏项ID" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 详情查看模态框 -->
    <a-modal
      v-model:open="detailModalVisible"
      title="收藏详情"
      :footer="null"
      width="700px"
    >
      <div v-if="currentRecord">
        <a-descriptions :column="2" bordered>
          <a-descriptions-item label="收藏ID">{{ currentRecord.id }}</a-descriptions-item>
          <a-descriptions-item label="用户信息">
            <div v-if="currentRecord.user_info">
              {{ currentRecord.user_info.username }} ({{ currentRecord.user_info.phone }})
            </div>
            <span v-else>{{ currentRecord.user_id }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="收藏类型">
            <a-tag :color="getItemTypeColor(currentRecord.item_type)">
              {{ getItemTypeText(currentRecord.item_type) }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="收藏项ID">{{ currentRecord.item_id }}</a-descriptions-item>
          <a-descriptions-item label="收藏时间" :span="2">{{ formatDateTime(currentRecord.create_time) }}</a-descriptions-item>
          <a-descriptions-item label="收藏项信息" :span="2">
            <div v-if="currentRecord.item_title">
              <div><strong>{{ currentRecord.item_title }}</strong></div>
              <div class="text-gray">{{ currentRecord.item_description }}</div>
            </div>
            <span v-else class="text-gray">暂无详细信息</span>
          </a-descriptions-item>
        </a-descriptions>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { favoriteAPI } from '@/api/favorite'
import { 
  PlusOutlined, 
  DeleteOutlined,
  ExportOutlined 
} from '@ant-design/icons-vue'

// 响应式数据
const loading = ref(false)
const favorites = ref([])
const modalVisible = ref(false)
const detailModalVisible = ref(false)
const isEditing = ref(false)
const submitting = ref(false)
const formRef = ref()
const currentRecord = ref(null)
const selectedRowKeys = ref([])

// 搜索表单
const searchForm = reactive({
  user_id: undefined,
  item_type: undefined,
  item_id: undefined,
  dateRange: undefined
})

// 统计数据
const stats = reactive({
  total_favorites: 0,
  course_favorites: 0,
  counselor_favorites: 0,
  today_favorites: 0
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
  user_id: '',
  item_type: '',
  item_id: ''
})

// 表单验证规则
const formRules = {
  user_id: [
    { required: true, message: '请输入用户ID' }
  ],
  item_type: [
    { required: true, message: '请选择收藏类型' }
  ],
  item_id: [
    { required: true, message: '请输入收藏项ID' }
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
    title: '收藏类型',
    key: 'item_type',
    width: 100
  },
  {
    title: '收藏项信息',
    key: 'item_info',
    width: 200
  },
  {
    title: '收藏项ID',
    dataIndex: 'item_id',
    key: 'item_id',
    width: 150,
    ellipsis: true
  },
  {
    title: '收藏时间',
    key: 'create_time',
    width: 150
  },
  {
    title: '操作',
    key: 'action',
    width: 150,
    fixed: 'right'
  }
]

// 方法
const fetchFavorites = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.current,
      per_page: pagination.pageSize,
      ...searchForm
    }

    // 处理日期范围
    if (searchForm.dateRange && searchForm.dateRange.length === 2) {
      params.start_date = searchForm.dateRange[0].format('YYYY-MM-DD')
      params.end_date = searchForm.dateRange[1].format('YYYY-MM-DD')
    }

    const response = await favoriteAPI.getFavorites(params)
    if (response.data) {
      favorites.value = response.data.favorites || []
      pagination.total = response.data.total || 0
      
      // 更新统计数据
      updateStats()
    }
  } catch (error) {
    console.error('获取收藏列表失败:', error)
    message.error('获取收藏列表失败')
  } finally {
    loading.value = false
  }
}

const updateStats = () => {
  const total = favorites.value.length
  const courseCount = favorites.value.filter(f => f.item_type === 'course').length
  const counselorCount = favorites.value.filter(f => f.item_type === 'counselor').length
  
  // 计算今日新增
  const today = new Date().toDateString()
  const todayCount = favorites.value.filter(f => {
    const createDate = new Date(f.create_time).toDateString()
    return createDate === today
  }).length

  Object.assign(stats, {
    total_favorites: total,
    course_favorites: courseCount,
    counselor_favorites: counselorCount,
    today_favorites: todayCount
  })
}

const handleSearch = () => {
  pagination.current = 1
  fetchFavorites()
}

const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = undefined
  })
  pagination.current = 1
  fetchFavorites()
}

const handleTableChange = (pag) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchFavorites()
}

const showAddModal = () => {
  isEditing.value = false
  modalVisible.value = true
  resetFormData()
}

const editFavorite = (record) => {
  isEditing.value = true
  modalVisible.value = true
  currentRecord.value = record
  Object.assign(formData, {
    user_id: record.user_id,
    item_type: record.item_type,
    item_id: record.item_id
  })
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    submitting.value = true

    if (isEditing.value) {
      // 编辑收藏（实际上是删除旧的，创建新的）
      await favoriteAPI.deleteFavorite(currentRecord.value.id)
      await favoriteAPI.createFavorite(formData)
      message.success('收藏更新成功')
    } else {
      await favoriteAPI.createFavorite(formData)
      message.success('收藏创建成功')
    }

    modalVisible.value = false
    fetchFavorites()
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
    user_id: '',
    item_type: '',
    item_id: ''
  })
}

const viewDetail = (record) => {
  currentRecord.value = record
  detailModalVisible.value = true
}

const deleteFavorite = (record) => {
  const modal = message.loading('删除中...', 0)
  favoriteAPI.deleteFavorite(record.id)
    .then(() => {
      modal()
      message.success('删除成功')
      fetchFavorites()
    })
    .catch(error => {
      modal()
      console.error('删除失败:', error)
      message.error('删除失败')
    })
}

const onSelectChange = (newSelectedRowKeys) => {
  selectedRowKeys.value = newSelectedRowKeys
}

const batchDelete = () => {
  if (selectedRowKeys.value.length === 0) {
    message.warning('请选择要删除的记录')
    return
  }
  
  message.confirm({
    title: '确认删除',
    content: `确定要删除选中的 ${selectedRowKeys.value.length} 条记录吗？`,
    onOk: async () => {
      const modal = message.loading('批量删除中...', 0)
      try {
        await Promise.all(
          selectedRowKeys.value.map(id => favoriteAPI.deleteFavorite(id))
        )
        modal()
        message.success('批量删除成功')
        selectedRowKeys.value = []
        fetchFavorites()
      } catch (error) {
        modal()
        console.error('批量删除失败:', error)
        message.error('批量删除失败')
      }
    }
  })
}

const exportData = () => {
  message.info('导出功能待实现')
}

// 辅助方法
const getItemTypeColor = (type) => {
  const colorMap = {
    course: 'blue',
    counselor: 'green',
    assessment: 'orange',
    article: 'purple'
  }
  return colorMap[type] || 'default'
}

const getItemTypeText = (type) => {
  const textMap = {
    course: '课程',
    counselor: '咨询师',
    assessment: '测评',
    article: '文章'
  }
  return textMap[type] || type
}

const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '-'
  try {
    return new Date(dateTimeStr).toLocaleString('zh-CN')
  } catch {
    return dateTimeStr
  }
}

// 生命周期
onMounted(() => {
  fetchFavorites()
})
</script>

<style lang="scss" scoped>
.favorite-management {
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

.stats-cards {
  margin-bottom: 24px;
}

.user-name {
  font-weight: 500;
  color: #1890ff;
}

.user-phone {
  font-size: 12px;
  margin-top: 2px;
}

.item-info {
  max-width: 200px;
}

.item-title {
  font-weight: 500;
  color: #1890ff;
  margin-bottom: 4px;
}

.item-desc {
  font-size: 12px;
  line-height: 1.4;
}

.text-gray {
  color: #666;
}

:deep(.ant-table) {
  .ant-table-tbody > tr > td {
    padding: 12px 8px;
  }
}

:deep(.ant-descriptions) {
  .ant-descriptions-item-label {
    font-weight: 500;
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