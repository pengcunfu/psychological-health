<template>
  <div class="assessment-management">
    <!-- 搜索栏和操作栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="测评名称">
          <a-input v-model:value="searchForm.name" placeholder="请输入测评名称" style="width: 200px;" />
        </a-form-item>
        <a-form-item label="分类">
          <a-input v-model:value="searchForm.category" placeholder="请输入分类" style="width: 150px;" />
        </a-form-item>
        <a-form-item label="难度">
          <a-select v-model:value="searchForm.difficulty" placeholder="请选择难度" style="width: 120px;" allow-clear>
            <a-select-option value="easy">简单</a-select-option>
            <a-select-option value="medium">中等</a-select-option>
            <a-select-option value="hard">困难</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="状态">
          <a-select v-model:value="searchForm.status" placeholder="请选择状态" style="width: 120px;" allow-clear>
            <a-select-option value="published">已发布</a-select-option>
            <a-select-option value="draft">草稿</a-select-option>
            <a-select-option value="archived">已归档</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
          <a-button style="margin-left: 8px;" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>

      <a-button type="primary" @click="showAddModal">
        <template #icon>
          <PlusOutlined />
        </template>
        添加测评
      </a-button>
    </div>

    <!-- 测评列表 -->
    <a-table :columns="columns" :data-source="assessments" :loading="loading" :pagination="pagination"
      @change="handleTableChange" row-key="id">
      <template #cover="{ record }">
        <a-image :src="FileUploader.getFullImageUrl(record?.cover_image)" :alt="record?.name || ''" width="60"
          height="40" style="object-fit: cover; border-radius: 4px;" :preview="false" />
      </template>

      <template #name="{ record }">
        <div class="assessment-name">
          <div class="name-text">{{ record?.name || '' }}</div>
          <div class="name-subtitle">{{ record?.subtitle || '' }}</div>
        </div>
      </template>

      <template #difficulty="{ record }">
        <a-tag :color="getDifficultyColor(record?.difficulty)">
          {{ getDifficultyText(record?.difficulty) }}
        </a-tag>
      </template>

      <template #status="{ record }">
        <a-tag :color="getStatusColor(record?.status)">
          {{ getStatusText(record?.status) }}
        </a-tag>
      </template>

      <template #price="{ record }">
        <span class="price">
          <span v-if="record?.price > 0">¥{{ record?.price }}</span>
          <span v-else class="free">免费</span>
        </span>
      </template>

      <template #stats="{ record }">
        <div class="stats">
          <div>题目: {{ record?.question_count || 0 }}</div>
          <div>参与: {{ record?.participant_count || 0 }}</div>
        </div>
      </template>

      <template #createTime="{ record }">
        {{ formatDate(record?.create_time) }}
      </template>

      <template #action="{ record }">
        <a-space>
          <a-button type="link" size="small" @click="editAssessment(record)">
            编辑
          </a-button>
          <a-button type="link" size="small" @click="manageQuestions(record)">
            题目管理
          </a-button>
          <a-dropdown>
            <a-button type="link" size="small">
              更多
              <DownOutlined />
            </a-button>
            <template #overlay>
              <a-menu @click="({ key }) => handleMenuAction(record, key)">
                <a-menu-item v-if="record.status === 'draft'" key="publish">
                  发布测评
                </a-menu-item>
                <a-menu-item v-if="record.status === 'published'" key="archive">
                  归档测评
                </a-menu-item>
                <a-menu-item key="view-records">
                  查看记录
                </a-menu-item>
                <a-menu-item key="stats">
                  统计分析
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item key="delete" class="danger-item">
                  删除测评
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </a-space>
      </template>
    </a-table>

    <!-- 添加/编辑测评模态框 -->
    <a-modal v-model:open="modalVisible" :title="modalTitle" :width="800" @ok="handleModalOk"
      @cancel="handleModalCancel" :confirm-loading="modalLoading">
      <a-form ref="formRef" :model="form" :rules="rules" layout="vertical">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="测评ID" name="id" v-if="!isEdit">
              <a-input v-model:value="form.id" placeholder="请输入测评ID" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="测评名称" name="name">
              <a-input v-model:value="form.name" placeholder="请输入测评名称" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="副标题" name="subtitle">
          <a-input v-model:value="form.subtitle" placeholder="请输入副标题" />
        </a-form-item>

        <a-form-item label="测评描述" name="description">
          <a-textarea v-model:value="form.description" placeholder="请输入测评描述" :rows="3" />
        </a-form-item>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="分类" name="category">
              <a-input v-model:value="form.category" placeholder="测评分类" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="难度" name="difficulty">
              <a-select v-model:value="form.difficulty" placeholder="请选择难度">
                <a-select-option value="easy">简单</a-select-option>
                <a-select-option value="medium">中等</a-select-option>
                <a-select-option value="hard">困难</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="状态" name="status">
              <a-select v-model:value="form.status" placeholder="请选择状态">
                <a-select-option value="draft">草稿</a-select-option>
                <a-select-option value="published">已发布</a-select-option>
                <a-select-option value="archived">已归档</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="预计时长(分钟)" name="duration">
              <a-input-number v-model:value="form.duration" :min="1" :max="1440" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="价格" name="price">
              <a-input-number v-model:value="form.price" :min="0" :precision="2" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="原价" name="original_price">
              <a-input-number v-model:value="form.original_price" :min="0" :precision="2" style="width: 100%" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="标签" name="tags">
          <a-input v-model:value="form.tags" placeholder="请输入标签，用逗号分隔" />
        </a-form-item>

        <a-form-item label="测评说明" name="instructions">
          <a-textarea v-model:value="form.instructions" placeholder="请输入测评说明" :rows="4" />
        </a-form-item>

        <a-form-item label="封面图片" name="cover_image">
          <FileUploaderComponent v-model:value="form.cover_image" accept="image/*" :max-size="5"
            list-type="picture-card" :max-count="1" />
        </a-form-item>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item name="is_free">
              <a-checkbox v-model:checked="form.is_free">免费测评</a-checkbox>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="排序" name="sort_order">
              <a-input-number v-model:value="form.sort_order" style="width: 100%" />
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
    </a-modal>

    <!-- 题目管理模态框 -->
    <a-modal v-model:open="questionModalVisible" title="题目管理" :width="1200" @cancel="handleQuestionModalCancel"
      :footer="null">
      <QuestionManager v-if="questionModalVisible" :assessment-id="currentAssessmentId"
        @close="handleQuestionModalCancel" />
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { message, Modal } from 'ant-design-vue'
import { PlusOutlined, DownOutlined } from '@ant-design/icons-vue'
import { assessmentAPI } from '@/api/admin'
import { FileUploader } from '@/api/upload'
import FileUploaderComponent from '@/components/FileUploader.vue'
import QuestionManager from './components/QuestionManager.vue'

const loading = ref(false)
const assessments = ref([])
const modalVisible = ref(false)
const modalLoading = ref(false)
const questionModalVisible = ref(false)
const currentAssessmentId = ref('')
const isEdit = ref(false)
const formRef = ref()

const searchForm = reactive({
  name: '',
  category: '',
  difficulty: '',
  status: ''
})

const form = reactive({
  id: '',
  name: '',
  subtitle: '',
  description: '',
  category: '',
  difficulty: 'medium',
  status: 'draft',
  duration: 30,
  price: 0,
  original_price: 0,
  tags: '',
  instructions: '',
  cover_image: '',
  is_free: true,
  sort_order: 0
})

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`
})

const columns = [
  {
    title: '封面',
    dataIndex: 'cover_image',
    key: 'cover',
    width: 80,
    slots: { customRender: 'cover' }
  },
  {
    title: '测评名称',
    dataIndex: 'name',
    key: 'name',
    width: 200,
    slots: { customRender: 'name' }
  },
  {
    title: '分类',
    dataIndex: 'category',
    key: 'category',
    width: 100
  },
  {
    title: '难度',
    dataIndex: 'difficulty',
    key: 'difficulty',
    width: 80,
    slots: { customRender: 'difficulty' }
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 80,
    slots: { customRender: 'status' }
  },
  {
    title: '价格',
    dataIndex: 'price',
    key: 'price',
    width: 80,
    slots: { customRender: 'price' }
  },
  {
    title: '统计',
    key: 'stats',
    width: 100,
    slots: { customRender: 'stats' }
  },
  {
    title: '创建时间',
    dataIndex: 'create_time',
    key: 'createTime',
    width: 140,
    slots: { customRender: 'createTime' }
  },
  {
    title: '操作',
    key: 'action',
    fixed: 'right',
    width: 180,
    slots: { customRender: 'action' }
  }
]

const rules = {
  id: [
    { required: true, message: '请输入测评ID', trigger: 'blur' },
    { min: 1, max: 50, message: 'ID长度应在1-50个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入测评名称', trigger: 'blur' },
    { min: 1, max: 200, message: '名称长度应在1-200个字符', trigger: 'blur' }
  ],
  difficulty: [
    { required: true, message: '请选择难度', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

const modalTitle = computed(() => {
  return isEdit.value ? '编辑测评' : '添加测评'
})

// 获取测评列表
const fetchAssessments = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.current,
      per_page: pagination.pageSize,
      ...searchForm
    }

    const response = await assessmentAPI.getAssessments(params)
    if (response.success) {
      assessments.value = response.data.list || []
      pagination.total = response.data.total || 0
    }
  } catch (error) {
    message.error('获取测评列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  fetchAssessments()
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    name: '',
    category: '',
    difficulty: '',
    status: ''
  })
  pagination.current = 1
  fetchAssessments()
}

// 表格变化处理
const handleTableChange = (paginationData) => {
  pagination.current = paginationData.current
  pagination.pageSize = paginationData.pageSize
  fetchAssessments()
}

// 显示添加模态框
const showAddModal = () => {
  isEdit.value = false
  resetForm()
  modalVisible.value = true
}

// 编辑测评
const editAssessment = (record) => {
  isEdit.value = true
  Object.assign(form, {
    ...record,
    tags: Array.isArray(record.tags) ? record.tags.join(',') : (record.tags || '')
  })
  modalVisible.value = true
}

// 题目管理
const manageQuestions = (record) => {
  currentAssessmentId.value = record.id
  questionModalVisible.value = true
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    id: '',
    name: '',
    subtitle: '',
    description: '',
    category: '',
    difficulty: 'medium',
    status: 'draft',
    duration: 30,
    price: 0,
    original_price: 0,
    tags: '',
    instructions: '',
    cover_image: '',
    is_free: true,
    sort_order: 0
  })
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 模态框确定
const handleModalOk = async () => {
  try {
    await formRef.value.validateFields()
    modalLoading.value = true

    const data = {
      ...form,
      tags: form.tags ? form.tags.split(',').map(tag => tag.trim()).filter(tag => tag) : []
    }

    if (isEdit.value) {
      await assessmentAPI.updateAssessment(form.id, data)
      message.success('更新成功')
    } else {
      await assessmentAPI.createAssessment(data)
      message.success('创建成功')
    }

    modalVisible.value = false
    fetchAssessments()
  } catch (error) {
    message.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    modalLoading.value = false
  }
}

// 模态框取消
const handleModalCancel = () => {
  modalVisible.value = false
  resetForm()
}

// 题目管理模态框取消
const handleQuestionModalCancel = () => {
  questionModalVisible.value = false
  currentAssessmentId.value = ''
}

// 菜单操作
const handleMenuAction = async (record, key) => {
  switch (key) {
    case 'publish':
      await updateAssessmentStatus(record.id, 'published')
      break
    case 'archive':
      await updateAssessmentStatus(record.id, 'archived')
      break
    case 'view-records':
      // TODO: 跳转到测评记录页面
      message.info('功能开发中')
      break
    case 'stats':
      // TODO: 显示统计分析
      message.info('功能开发中')
      break
    case 'delete':
      showDeleteConfirm(record)
      break
  }
}

// 更新测评状态
const updateAssessmentStatus = async (id, status) => {
  try {
    await assessmentAPI.updateAssessment(id, { status })
    message.success('状态更新成功')
    fetchAssessments()
  } catch (error) {
    message.error('状态更新失败')
  }
}

// 显示删除确认
const showDeleteConfirm = (record) => {
  Modal.confirm({
    title: '确认删除',
    content: `确定要删除测评"${record.name}"吗？此操作不可恢复。`,
    okText: '确定',
    okType: 'danger',
    cancelText: '取消',
    onOk: () => deleteAssessment(record.id)
  })
}

// 删除测评
const deleteAssessment = async (id) => {
  try {
    await assessmentAPI.deleteAssessment(id)
    message.success('删除成功')
    fetchAssessments()
  } catch (error) {
    message.error('删除失败')
  }
}

// 获取难度颜色
const getDifficultyColor = (difficulty) => {
  const colors = {
    easy: 'green',
    medium: 'orange',
    hard: 'red'
  }
  return colors[difficulty] || 'default'
}

// 获取难度文本
const getDifficultyText = (difficulty) => {
  const texts = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return texts[difficulty] || difficulty
}

// 获取状态颜色
const getStatusColor = (status) => {
  const colors = {
    published: 'green',
    draft: 'orange',
    archived: 'default'
  }
  return colors[status] || 'default'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    published: '已发布',
    draft: '草稿',
    archived: '已归档'
  }
  return texts[status] || status
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchAssessments()
})
</script>

<style lang="scss" scoped>
.assessment-management {
  padding: 0;
}

.search-and-action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  background: white;
  padding: 12px;
  border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.search-form {
  .ant-form-item {
    margin-bottom: 0;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.assessment-name {
  line-height: 1.4;

  .name-text {
    font-weight: 500;
    color: #262626;
  }

  .name-subtitle {
    font-size: 12px;
    color: #8c8c8c;
    margin-top: 2px;
  }
}

.price {
  font-weight: 500;

  .free {
    color: #52c41a;
  }
}

.stats {
  line-height: 1.4;

  >div {
    font-size: 12px;
    color: #666;
  }
}

.danger-item {
  color: #ff4d4f !important;
}

// 模态框样式
.detail-section {
  margin-bottom: 16px;

  h4 {
    margin: 0 0 8px 0;
    color: #333;
    font-size: 14px;
    font-weight: 600;
  }
}

:deep(.ant-table-thead > tr > th) {
  background: #fafafa;
  font-weight: 600;
}

:deep(.ant-modal-body) {
  max-height: 600px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .assessment-management {
    padding: 8px;
  }

  .search-and-action-bar {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
    padding: 8px;
    margin-bottom: 8px;
  }

  .search-form {
    .ant-form {
      flex-direction: column;
    }

    .ant-form-item {
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}
</style>