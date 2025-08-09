<template>
  <div class="assessment-record-management">
    <!-- 搜索栏和操作栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="用户ID">
          <a-input v-model:value="searchForm.user_id" placeholder="请输入用户ID" style="width: 200px;" />
        </a-form-item>
        <a-form-item label="测评名称">
          <a-input v-model:value="searchForm.assessment_name" placeholder="请输入测评名称" style="width: 200px;" />
        </a-form-item>
        <a-form-item label="状态">
          <a-select v-model:value="searchForm.status" placeholder="请选择状态" style="width: 120px;" allow-clear>
            <a-select-option value="in_progress">进行中</a-select-option>
            <a-select-option value="completed">已完成</a-select-option>
            <a-select-option value="expired">已过期</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="结果等级">
          <a-input v-model:value="searchForm.result_level" placeholder="请输入结果等级" style="width: 150px;" />
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
          添加记录
        </a-button>
        <a-button @click="exportRecords">
          <export-outlined />
          导出数据
        </a-button>
        <a-button @click="refreshStats">
          <bar-chart-outlined />
          统计信息
        </a-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards" v-if="showStats">
      <a-row :gutter="16">
        <a-col :span="6">
          <a-card size="small">
            <a-statistic title="总记录数" :value="stats.total_records" />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card size="small">
            <a-statistic title="已完成" :value="stats.completed_records" />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card size="small">
            <a-statistic title="进行中" :value="stats.in_progress_records" />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card size="small">
            <a-statistic title="平均分" :value="stats.average_score" :precision="1" />
          </a-card>
        </a-col>
      </a-row>
    </div>

    <!-- 测评记录列表 -->
    <a-table 
      :columns="columns" 
      :data-source="records" 
      :loading="loading" 
      :pagination="pagination"
      @change="handleTableChange" 
      row-key="id"
      :scroll="{ x: 1200 }"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'user_info'">
          <div v-if="record.user_info">
            <div class="user-name">{{ record.user_info.username }}</div>
            <div class="user-phone text-gray">{{ record.user_info.phone }}</div>
          </div>
          <span v-else class="text-gray">用户ID: {{ record.user_id }}</span>
        </template>

        <template v-if="column.key === 'assessment_info'">
          <div v-if="record.assessment_info">
            <div class="assessment-title">{{ record.assessment_info.name }}</div>
            <div class="assessment-category text-gray">{{ record.assessment_info.category }}</div>
          </div>
          <span v-else class="text-gray">测评ID: {{ record.assessment_id }}</span>
        </template>

        <template v-if="column.key === 'status'">
          <a-tag :color="getStatusColor(record.status)">
            {{ getStatusText(record.status) }}
          </a-tag>
        </template>

        <template v-if="column.key === 'score_info'">
          <div class="score-info">
            <div class="score-text">
              <span class="total-score">{{ record.total_score }}</span>
              <span class="max-score">/ {{ record.max_score }}</span>
            </div>
            <div class="score-percentage" v-if="record.max_score > 0">
              ({{ Math.round((record.total_score / record.max_score) * 100) }}%)
            </div>
          </div>
        </template>

        <template v-if="column.key === 'result_level'">
          <a-tag v-if="record.result_level" :color="getLevelColor(record.result_level)">
            {{ record.result_level }}
          </a-tag>
          <span v-else class="text-gray">-</span>
        </template>

        <template v-if="column.key === 'time_info'">
          <div class="time-info">
            <div class="start-time">
              开始：{{ formatDateTime(record.start_time) }}
            </div>
            <div class="complete-time" v-if="record.complete_time">
              完成：{{ formatDateTime(record.complete_time) }}
            </div>
            <div class="duration text-gray" v-if="record.start_time && record.complete_time">
              用时：{{ calculateDuration(record.start_time, record.complete_time) }}
            </div>
          </div>
        </template>

        <template v-if="column.key === 'is_anonymous'">
          <a-tag :color="record.is_anonymous ? 'orange' : 'green'">
            {{ record.is_anonymous ? '匿名' : '实名' }}
          </a-tag>
        </template>

        <template v-if="column.key === 'action'">
          <a-space>
            <a-button type="link" size="small" @click="viewDetail(record)">
              查看详情
            </a-button>
            <a-button type="link" size="small" @click="viewResults(record)" :disabled="record.status !== 'completed'">
              查看结果
            </a-button>
            <a-dropdown>
              <a-button type="link" size="small">
                更多 <down-outlined />
              </a-button>
              <template #overlay>
                <a-menu>
                  <a-menu-item @click="editRecord(record)">
                    编辑记录
                  </a-menu-item>
                  <a-menu-item @click="downloadReport(record)" :disabled="record.status !== 'completed'">
                    下载报告
                  </a-menu-item>
                  <a-menu-divider />
                  <a-menu-item danger @click="deleteRecord(record)">
                    删除记录
                  </a-menu-item>
                </a-menu>
              </template>
            </a-dropdown>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 添加/编辑记录模态框 -->
    <a-modal
      v-model:open="modalVisible"
      :title="isEditing ? '编辑测评记录' : '添加测评记录'"
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
            <a-form-item label="用户ID" name="user_id">
              <a-input v-model:value="formData.user_id" placeholder="请输入用户ID" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="测评ID" name="assessment_id">
              <a-input v-model:value="formData.assessment_id" placeholder="请输入测评ID" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="状态" name="status">
              <a-select v-model:value="formData.status" placeholder="请选择状态">
                <a-select-option value="in_progress">进行中</a-select-option>
                <a-select-option value="completed">已完成</a-select-option>
                <a-select-option value="expired">已过期</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="总分" name="total_score">
              <a-input-number 
                v-model:value="formData.total_score" 
                placeholder="总分"
                :min="0"
                :precision="1"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="满分" name="max_score">
              <a-input-number 
                v-model:value="formData.max_score" 
                placeholder="满分"
                :min="0"
                :precision="1"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="结果等级" name="result_level">
              <a-input v-model:value="formData.result_level" placeholder="结果等级" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="是否匿名" name="is_anonymous">
              <a-switch v-model:checked="formData.is_anonymous" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="结果描述" name="result_description">
          <a-textarea v-model:value="formData.result_description" placeholder="结果描述" :rows="3" />
        </a-form-item>

        <a-form-item label="建议" name="result_suggestion">
          <a-textarea v-model:value="formData.result_suggestion" placeholder="建议" :rows="3" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 详情查看模态框 -->
    <a-modal
      v-model:open="detailModalVisible"
      title="测评记录详情"
      :footer="null"
      width="900px"
    >
      <div v-if="currentRecord">
        <a-descriptions :column="2" bordered>
          <a-descriptions-item label="记录ID">{{ currentRecord.id }}</a-descriptions-item>
          <a-descriptions-item label="用户信息">
            <div v-if="currentRecord.user_info">
              {{ currentRecord.user_info.username }} ({{ currentRecord.user_info.phone }})
            </div>
            <span v-else>{{ currentRecord.user_id }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="测评信息">
            <div v-if="currentRecord.assessment_info">
              {{ currentRecord.assessment_info.name }}
            </div>
            <span v-else>{{ currentRecord.assessment_id }}</span>
          </a-descriptions-item>
          <a-descriptions-item label="状态">
            <a-tag :color="getStatusColor(currentRecord.status)">
              {{ getStatusText(currentRecord.status) }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="开始时间">{{ formatDateTime(currentRecord.start_time) }}</a-descriptions-item>
          <a-descriptions-item label="完成时间">{{ formatDateTime(currentRecord.complete_time) }}</a-descriptions-item>
          <a-descriptions-item label="得分情况">
            {{ currentRecord.total_score }} / {{ currentRecord.max_score }}
            <span v-if="currentRecord.max_score > 0">
              ({{ Math.round((currentRecord.total_score / currentRecord.max_score) * 100) }}%)
            </span>
          </a-descriptions-item>
          <a-descriptions-item label="结果等级">
            <a-tag v-if="currentRecord.result_level" :color="getLevelColor(currentRecord.result_level)">
              {{ currentRecord.result_level }}
            </a-tag>
            <span v-else>-</span>
          </a-descriptions-item>
          <a-descriptions-item label="结果描述" :span="2">
            {{ currentRecord.result_description || '-' }}
          </a-descriptions-item>
          <a-descriptions-item label="建议" :span="2">
            {{ currentRecord.result_suggestion || '-' }}
          </a-descriptions-item>
        </a-descriptions>

        <!-- 维度得分 -->
        <div v-if="currentRecord.dimension_scores && Object.keys(currentRecord.dimension_scores).length > 0" class="dimension-scores">
          <h4>维度得分</h4>
          <a-row :gutter="16">
            <a-col :span="8" v-for="(score, dimension) in currentRecord.dimension_scores" :key="dimension">
              <a-card size="small">
                <a-statistic :title="dimension" :value="score" :precision="1" />
              </a-card>
            </a-col>
          </a-row>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { assessmentRecordAPI } from '@/api/assessment'
import { 
  PlusOutlined, 
  ExportOutlined, 
  BarChartOutlined,
  DownOutlined 
} from '@ant-design/icons-vue'

// 响应式数据
const loading = ref(false)
const records = ref([])
const modalVisible = ref(false)
const detailModalVisible = ref(false)
const isEditing = ref(false)
const submitting = ref(false)
const showStats = ref(false)
const formRef = ref()
const currentRecord = ref(null)

// 搜索表单
const searchForm = reactive({
  user_id: undefined,
  assessment_name: undefined,
  status: undefined,
  result_level: undefined,
  dateRange: undefined
})

// 统计数据
const stats = reactive({
  total_records: 0,
  completed_records: 0,
  in_progress_records: 0,
  average_score: 0
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
  assessment_id: '',
  status: 'in_progress',
  total_score: 0,
  max_score: 0,
  result_level: '',
  result_description: '',
  result_suggestion: '',
  is_anonymous: false
})

// 表单验证规则
const formRules = {
  user_id: [
    { required: true, message: '请输入用户ID' }
  ],
  assessment_id: [
    { required: true, message: '请输入测评ID' }
  ],
  status: [
    { required: true, message: '请选择状态' }
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
    title: '测评信息',
    key: 'assessment_info',
    width: 180
  },
  {
    title: '状态',
    key: 'status',
    width: 100
  },
  {
    title: '得分',
    key: 'score_info',
    width: 120
  },
  {
    title: '结果等级',
    key: 'result_level',
    width: 100
  },
  {
    title: '时间信息',
    key: 'time_info',
    width: 200
  },
  {
    title: '匿名',
    key: 'is_anonymous',
    width: 80
  },
  {
    title: '操作',
    key: 'action',
    width: 180,
    fixed: 'right'
  }
]

// 方法
const fetchRecords = async () => {
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

    const response = await assessmentRecordAPI.getAssessmentRecords(params)
    if (response.data) {
      records.value = response.data.list || []
      pagination.total = response.data.total || 0
    }
  } catch (error) {
    console.error('获取测评记录失败:', error)
    message.error('获取测评记录失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.current = 1
  fetchRecords()
}

const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = undefined
  })
  pagination.current = 1
  fetchRecords()
}

const handleTableChange = (pag) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchRecords()
}

const showAddModal = () => {
  isEditing.value = false
  modalVisible.value = true
  resetFormData()
}

const editRecord = (record) => {
  isEditing.value = true
  modalVisible.value = true
  currentRecord.value = record
  Object.assign(formData, {
    user_id: record.user_id,
    assessment_id: record.assessment_id,
    status: record.status,
    total_score: record.total_score,
    max_score: record.max_score,
    result_level: record.result_level,
    result_description: record.result_description,
    result_suggestion: record.result_suggestion,
    is_anonymous: record.is_anonymous
  })
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    submitting.value = true

    if (isEditing.value) {
      await assessmentRecordAPI.updateAssessmentRecord(currentRecord.value.id, formData)
      message.success('记录更新成功')
    } else {
      await assessmentRecordAPI.createAssessmentRecord(formData)
      message.success('记录创建成功')
    }

    modalVisible.value = false
    fetchRecords()
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
    assessment_id: '',
    status: 'in_progress',
    total_score: 0,
    max_score: 0,
    result_level: '',
    result_description: '',
    result_suggestion: '',
    is_anonymous: false
  })
}

const viewDetail = (record) => {
  currentRecord.value = record
  detailModalVisible.value = true
}

const viewResults = (record) => {
  // 可以跳转到详细结果页面或显示结果详情
  message.info('查看测评结果功能待实现')
}

const deleteRecord = (record) => {
  const modal = message.loading('删除中...', 0)
  assessmentRecordAPI.deleteAssessmentRecord(record.id)
    .then(() => {
      modal()
      message.success('删除成功')
      fetchRecords()
    })
    .catch(error => {
      modal()
      console.error('删除失败:', error)
      message.error('删除失败')
    })
}

const exportRecords = async () => {
  try {
    const response = await assessmentRecordAPI.exportAssessmentRecords(searchForm)
    // 处理文件下载
    const url = window.URL.createObjectURL(new Blob([response]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `assessment_records_${new Date().getTime()}.xlsx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    message.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    message.error('导出失败')
  }
}

const refreshStats = async () => {
  try {
    const response = await assessmentRecordAPI.getAssessmentRecordStats()
    if (response.data) {
      Object.assign(stats, response.data)
      showStats.value = true
      message.success('统计信息已更新')
    }
  } catch (error) {
    console.error('获取统计信息失败:', error)
    message.error('获取统计信息失败')
  }
}

const downloadReport = (record) => {
  message.info('下载报告功能待实现')
}

// 辅助方法
const getStatusColor = (status) => {
  const colorMap = {
    in_progress: 'processing',
    completed: 'success',
    expired: 'error'
  }
  return colorMap[status] || 'default'
}

const getStatusText = (status) => {
  const textMap = {
    in_progress: '进行中',
    completed: '已完成',
    expired: '已过期'
  }
  return textMap[status] || status
}

const getLevelColor = (level) => {
  // 可以根据等级设置不同颜色
  const colorMap = {
    '优秀': 'green',
    '良好': 'blue',
    '一般': 'orange',
    '较差': 'red'
  }
  return colorMap[level] || 'default'
}

const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '-'
  try {
    return new Date(dateTimeStr).toLocaleString('zh-CN')
  } catch {
    return dateTimeStr
  }
}

const calculateDuration = (startTime, endTime) => {
  if (!startTime || !endTime) return '-'
  try {
    const start = new Date(startTime)
    const end = new Date(endTime)
    const diffMinutes = Math.round((end - start) / (1000 * 60))
    
    if (diffMinutes < 60) {
      return `${diffMinutes}分钟`
    } else {
      const hours = Math.floor(diffMinutes / 60)
      const minutes = diffMinutes % 60
      return `${hours}小时${minutes}分钟`
    }
  } catch {
    return '-'
  }
}

// 生命周期
onMounted(() => {
  fetchRecords()
  refreshStats()
})
</script>

<style lang="scss" scoped>
.assessment-record-management {
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

.user-name, .assessment-title {
  font-weight: 500;
  color: #1890ff;
}

.user-phone, .assessment-category {
  font-size: 12px;
  margin-top: 2px;
}

.score-info {
  text-align: center;
}

.total-score {
  font-weight: 600;
  font-size: 16px;
  color: #1890ff;
}

.max-score {
  color: #666;
  margin-left: 2px;
}

.score-percentage {
  font-size: 12px;
  color: #999;
  margin-top: 2px;
}

.time-info {
  font-size: 12px;
  line-height: 1.4;
}

.start-time, .complete-time {
  margin-bottom: 2px;
}

.duration {
  font-style: italic;
}

.text-gray {
  color: #666;
}

.dimension-scores {
  margin-top: 24px;
}

.dimension-scores h4 {
  margin-bottom: 16px;
  color: #1890ff;
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