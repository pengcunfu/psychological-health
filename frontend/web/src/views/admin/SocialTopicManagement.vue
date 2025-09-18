<template>
  <div class="social-topic-management">
    <div class="page-header">
      <h2>话题管理</h2>
      <a-button type="primary" @click="showCreateModal">
        <plus-outlined />
        新增话题
      </a-button>
    </div>

    <!-- 搜索筛选 -->
    <div class="search-section">
      <a-card>
        <a-form layout="inline" :model="searchForm" @finish="handleSearch">
          <a-form-item label="话题名称">
            <a-input v-model:value="searchForm.name" placeholder="请输入话题名称" allow-clear />
          </a-form-item>
          <a-form-item label="状态">
            <a-select v-model:value="searchForm.status" placeholder="请选择状态" allow-clear style="width: 120px">
              <a-select-option value="">全部</a-select-option>
              <a-select-option value="active">启用</a-select-option>
              <a-select-option value="inactive">禁用</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="是否热门">
            <a-select v-model:value="searchForm.is_hot" placeholder="请选择" allow-clear style="width: 120px">
              <a-select-option :value="true">是</a-select-option>
              <a-select-option :value="false">否</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="是否精选">
            <a-select v-model:value="searchForm.is_featured" placeholder="请选择" allow-clear style="width: 120px">
              <a-select-option :value="true">是</a-select-option>
              <a-select-option :value="false">否</a-select-option>
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
            <template v-if="column.key === 'cover_image'">
              <a-image
                v-if="record.cover_image"
                :src="record.cover_image"
                :width="60"
                :height="40"
                style="object-fit: cover; border-radius: 4px;"
              />
              <span v-else class="text-gray-400">无封面</span>
            </template>
            
            <template v-if="column.key === 'color'">
              <div class="flex items-center">
                <div
                  class="w-4 h-4 rounded border mr-2"
                  :style="{ backgroundColor: record.color }"
                ></div>
                <span>{{ record.color }}</span>
              </div>
            </template>
            
            <template v-if="column.key === 'status'">
              <a-tag :color="record.status === 'active' ? 'green' : 'red'">
                {{ record.status === 'active' ? '启用' : '禁用' }}
              </a-tag>
            </template>
            
            <template v-if="column.key === 'is_hot'">
              <a-tag :color="record.is_hot ? 'orange' : 'default'">
                {{ record.is_hot ? '热门' : '普通' }}
              </a-tag>
            </template>
            
            <template v-if="column.key === 'is_featured'">
              <a-tag :color="record.is_featured ? 'purple' : 'default'">
                {{ record.is_featured ? '精选' : '普通' }}
              </a-tag>
            </template>
            
            <template v-if="column.key === 'stats'">
              <div class="text-sm">
                <div>帖子: {{ record.post_count || 0 }}</div>
                <div>参与: {{ record.participant_count || 0 }}</div>
                <div>浏览: {{ record.view_count || 0 }}</div>
              </div>
            </template>
            
            <template v-if="column.key === 'action'">
              <a-space>
                <a-button type="link" size="small" @click="showEditModal(record)">编辑</a-button>
                <a-popconfirm
                  title="确定要删除这个话题吗？"
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

    <!-- 创建/编辑模态框 -->
    <a-modal
      v-model:open="modalVisible"
      :title="isEdit ? '编辑话题' : '新增话题'"
      :confirm-loading="submitLoading"
      @ok="handleSubmit"
      @cancel="handleCancel"
      width="600px"
    >
      <a-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        layout="vertical"
      >
        <a-form-item label="话题名称" name="name">
          <a-input v-model:value="formData.name" placeholder="请输入话题名称" />
        </a-form-item>
        
        <a-form-item label="话题描述" name="description">
          <a-textarea v-model:value="formData.description" placeholder="请输入话题描述" :rows="4" />
        </a-form-item>
        
        <a-form-item label="封面图片" name="cover_image">
          <a-input v-model:value="formData.cover_image" placeholder="请输入封面图片URL" />
        </a-form-item>
        
        <a-form-item label="话题颜色" name="color">
          <a-input v-model:value="formData.color" placeholder="请输入颜色值 (如: #1890ff)" />
        </a-form-item>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="排序权重" name="sort_order">
              <a-input-number v-model:value="formData.sort_order" :min="0" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="状态" name="status">
              <a-select v-model:value="formData.status" style="width: 100%">
                <a-select-option value="active">启用</a-select-option>
                <a-select-option value="inactive">禁用</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="是否热门" name="is_hot">
              <a-switch v-model:checked="formData.is_hot" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="是否精选" name="is_featured">
              <a-switch v-model:checked="formData.is_featured" />
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { socialTopicAPI } from '@/api/social'

// 响应式数据
const loading = ref(false)
const submitLoading = ref(false)
const modalVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()

// 搜索表单
const searchForm = reactive({
  name: '',
  status: '',
  is_hot: undefined,
  is_featured: undefined,
  keyword: ''
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

// 表格列定义
const columns = [
  {
    title: '话题名称',
    dataIndex: 'name',
    key: 'name',
    width: 150
  },
  {
    title: '封面图片',
    dataIndex: 'cover_image',
    key: 'cover_image',
    width: 100
  },
  {
    title: '颜色',
    dataIndex: 'color',
    key: 'color',
    width: 120
  },
  {
    title: '描述',
    dataIndex: 'description',
    key: 'description',
    ellipsis: true,
    width: 200
  },
  {
    title: '排序',
    dataIndex: 'sort_order',
    key: 'sort_order',
    width: 80,
    sorter: true
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 80
  },
  {
    title: '热门',
    dataIndex: 'is_hot',
    key: 'is_hot',
    width: 80
  },
  {
    title: '精选',
    dataIndex: 'is_featured',
    key: 'is_featured',
    width: 80
  },
  {
    title: '统计信息',
    key: 'stats',
    width: 120
  },
  {
    title: '创建时间',
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

// 表单数据
const formData = reactive({
  id: '',
  name: '',
  description: '',
  cover_image: '',
  color: '#1890ff',
  sort_order: 0,
  status: 'active',
  is_hot: false,
  is_featured: false
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入话题名称', trigger: 'blur' },
    { max: 100, message: '话题名称不能超过100个字符', trigger: 'blur' }
  ],
  color: [
    { pattern: /^#[0-9A-Fa-f]{6}$/, message: '请输入有效的颜色值', trigger: 'blur' }
  ]
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
    
    const response = await socialTopicAPI.getSocialTopics(params)
    console.log(response)
    
    if (response.success) {
      tableData.value = response.data.list
      pagination.total = response.data.total
    } else {
      message.error(response.message || '获取数据失败')
    }
  } catch (error) {
    console.error('获取话题列表失败:', error)
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
    if (typeof searchForm[key] === 'boolean') {
      searchForm[key] = undefined
    } else {
      searchForm[key] = ''
    }
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

// 显示创建模态框
const showCreateModal = () => {
  isEdit.value = false
  resetFormData()
  modalVisible.value = true
}

// 显示编辑模态框
const showEditModal = (record) => {
  isEdit.value = true
  Object.keys(formData).forEach(key => {
    formData[key] = record[key] || formData[key]
  })
  modalVisible.value = true
}

// 重置表单数据
const resetFormData = () => {
  formData.id = ''
  formData.name = ''
  formData.description = ''
  formData.cover_image = ''
  formData.color = '#1890ff'
  formData.sort_order = 0
  formData.status = 'active'
  formData.is_hot = false
  formData.is_featured = false
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    submitLoading.value = true
    
    const submitData = { ...formData }
    delete submitData.id
    
    if (isEdit.value) {
      await socialTopicAPI.updateSocialTopic(formData.id, submitData)
      message.success('话题更新成功')
    } else {
      await socialTopicAPI.createSocialTopic(submitData)
      message.success('话题创建成功')
    }
    
    modalVisible.value = false
    fetchData()
  } catch (error) {
    console.error('提交失败:', error)
    if (error.response?.data?.message) {
      message.error(error.response.data.message)
    } else {
      message.error('操作失败')
    }
  } finally {
    submitLoading.value = false
  }
}

// 取消模态框
const handleCancel = () => {
  modalVisible.value = false
  resetFormData()
}

// 删除话题
const handleDelete = async (id) => {
  try {
    await socialTopicAPI.deleteSocialTopic(id)
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
.social-topic-management {
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
  
  .table-section {
    .ant-table {
      .text-gray-400 {
        color: #9ca3af;
      }
    }
  }
}

.flex {
  display: flex;
}

.items-center {
  align-items: center;
}

.w-4 {
  width: 1rem;
}

.h-4 {
  height: 1rem;
}

.rounded {
  border-radius: 0.25rem;
}

.border {
  border: 1px solid #d1d5db;
}

.mr-2 {
  margin-right: 0.5rem;
}
</style> 