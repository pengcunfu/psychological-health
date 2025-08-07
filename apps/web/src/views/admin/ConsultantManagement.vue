<template>
  <div class="consultant-management">
    <div class="page-header">
      <h2>咨询人管理</h2>
      <a-space>
        <a-button @click="fetchStats">
          <reload-outlined />
          刷新统计
        </a-button>
        <a-button type="primary" @click="showCreateModal">
          <plus-outlined />
          新增咨询人
        </a-button>
      </a-space>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <a-row :gutter="16">
        <a-col :span="6">
          <a-card>
            <a-statistic title="总数" :value="stats.total_count || 0" />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <a-statistic title="启用" :value="stats.active_count || 0" />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <a-statistic title="男性" :value="stats.male_count || 0" />
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <a-statistic title="女性" :value="stats.female_count || 0" />
          </a-card>
        </a-col>
      </a-row>
    </div>

    <!-- 搜索筛选区 -->
    <div class="search-section">
      <a-card>
        <a-form layout="inline" :model="searchForm" @finish="handleSearch">
          <a-form-item label="关键词">
            <a-input 
              v-model:value="searchForm.keyword" 
              placeholder="姓名、手机号、用户名" 
              style="width: 200px"
              allow-clear
            />
          </a-form-item>
          <a-form-item label="性别">
            <a-select 
              v-model:value="searchForm.gender" 
              placeholder="请选择性别" 
              style="width: 120px"
              allow-clear
            >
              <a-select-option value="">全部</a-select-option>
              <a-select-option value="male">男</a-select-option>
              <a-select-option value="female">女</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="状态">
            <a-select 
              v-model:value="searchForm.status" 
              placeholder="请选择状态" 
              style="width: 120px"
              allow-clear
            >
              <a-select-option :value="1">启用</a-select-option>
              <a-select-option :value="0">禁用</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item>
            <a-button type="primary" html-type="submit">
              <search-outlined />
              搜索
            </a-button>
            <a-button @click="resetSearch" style="margin-left: 8px">
              重置
            </a-button>
          </a-form-item>
        </a-form>
      </a-card>
    </div>

    <!-- 表格区域 -->
    <div class="table-section">
      <a-card>
        <a-table 
          :columns="columns" 
          :data-source="consultants" 
          :loading="loading" 
          :pagination="pagination"
          @change="handleTableChange"
          row-key="id"
          :scroll="{ x: 1500 }"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'user_info'">
              <div v-if="record.user_info">
                <div><strong>{{ record.user_info.username }}</strong></div>
                <div style="color: #999; font-size: 12px;">{{ record.user_info.phone }}</div>
              </div>
              <span v-else style="color: #ccc;">-</span>
            </template>
            
            <template v-else-if="column.key === 'gender'">
              <a-tag :color="record.gender === 'male' ? 'blue' : 'pink'">
                {{ record.gender_text }}
              </a-tag>
            </template>
            
            <template v-else-if="column.key === 'birth_date'">
              {{ record.birth_date || '-' }}
            </template>
            
            <template v-else-if="column.key === 'emergency_info'">
              <div>
                <div>{{ record.emergency_name }}</div>
                <div style="color: #999; font-size: 12px;">
                  {{ record.emergency_relationship_text }} - {{ record.emergency_phone }}
                </div>
              </div>
            </template>
            
            <template v-else-if="column.key === 'is_default'">
              <a-tag v-if="record.is_default" color="gold">
                <star-filled />
                默认
              </a-tag>
              <span v-else>-</span>
            </template>
            
            <template v-else-if="column.key === 'status'">
              <a-switch 
                :checked="record.status === 1" 
                @change="(checked) => handleStatusChange(record, checked)"
                :loading="record.statusLoading"
              />
            </template>
            
            <template v-else-if="column.key === 'action'">
              <a-space>
                <a-button type="link" size="small" @click="viewConsultant(record)">
                  查看
                </a-button>
                <a-button type="link" size="small" @click="editConsultant(record)">
                  编辑
                </a-button>
                <a-button 
                  type="link" 
                  size="small" 
                  @click="setDefault(record)"
                  :disabled="record.is_default || !record.user_info"
                >
                  设为默认
                </a-button>
                <a-popconfirm
                  title="确定删除这个咨询人吗？"
                  @confirm="deleteConsultant(record)"
                >
                  <a-button type="link" size="small" danger>
                    删除
                  </a-button>
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
      :title="isEdit ? '编辑咨询人' : '新增咨询人'"
      width="800px"
      @ok="handleSubmit"
      @cancel="handleCancel"
      :confirm-loading="submitLoading"
    >
      <a-form
        ref="formRef"
        :model="form"
        :rules="rules"
        layout="vertical"
      >
        <a-form-item label="关联用户" name="user_id">
          <a-select 
            v-model:value="form.user_id" 
            placeholder="请选择用户（可选）"
            show-search
            option-filter-prop="children"
            allow-clear
            @change="handleUserChange"
          >
            <a-select-option 
              v-for="user in userOptions" 
              :key="user.id" 
              :value="user.id"
            >
              {{ user.username }} ({{ user.phone }})
            </a-select-option>
          </a-select>
        </a-form-item>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="真实姓名" name="real_name">
              <a-input v-model:value="form.real_name" placeholder="请输入真实姓名" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="性别" name="gender">
              <a-select v-model:value="form.gender" placeholder="请选择性别">
                <a-select-option value="male">男</a-select-option>
                <a-select-option value="female">女</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="出生年份" name="birth_year">
              <a-input-number 
                v-model:value="form.birth_year" 
                placeholder="请输入出生年份"
                :min="1900"
                :max="2024"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="出生月份" name="birth_month">
              <a-input-number 
                v-model:value="form.birth_month" 
                placeholder="请输入出生月份"
                :min="1"
                :max="12"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="联系方式" name="phone">
          <a-input v-model:value="form.phone" placeholder="请输入手机号码" />
        </a-form-item>

        <a-divider>紧急联系人信息</a-divider>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="紧急联系人姓名" name="emergency_name">
              <a-input v-model:value="form.emergency_name" placeholder="请输入紧急联系人姓名" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="关系" name="emergency_relationship">
              <a-select v-model:value="form.emergency_relationship" placeholder="请选择关系">
                <a-select-option value="self">本人</a-select-option>
                <a-select-option value="spouse">配偶</a-select-option>
                <a-select-option value="child">子女</a-select-option>
                <a-select-option value="parent">父母</a-select-option>
                <a-select-option value="sibling">兄弟姐妹</a-select-option>
                <a-select-option value="friend">朋友</a-select-option>
                <a-select-option value="other">其他</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="紧急联系人电话" name="emergency_phone">
          <a-input v-model:value="form.emergency_phone" placeholder="请输入紧急联系人电话" />
        </a-form-item>

        <a-form-item label="备注信息" name="notes">
          <a-textarea 
            v-model:value="form.notes" 
            placeholder="请输入备注信息" 
            :rows="3"
          />
        </a-form-item>

        <a-form-item name="is_default">
          <a-checkbox v-model:checked="form.is_default" :disabled="!form.user_id">
            设为默认咨询人
          </a-checkbox>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 详情模态框 -->
    <a-modal
      v-model:open="detailVisible"
      title="咨询人详情"
      width="600px"
      :footer="null"
    >
      <a-descriptions :column="2" bordered v-if="currentConsultant">
        <a-descriptions-item label="关联用户" :span="2" v-if="currentConsultant.user_info">
          {{ currentConsultant.user_info.username }} ({{ currentConsultant.user_info.phone }})
        </a-descriptions-item>
        <a-descriptions-item label="真实姓名">
          {{ currentConsultant.real_name }}
        </a-descriptions-item>
        <a-descriptions-item label="性别">
          {{ currentConsultant.gender_text }}
        </a-descriptions-item>
        <a-descriptions-item label="出生日期">
          {{ currentConsultant.birth_date || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="联系方式">
          {{ currentConsultant.phone }}
        </a-descriptions-item>
        <a-descriptions-item label="紧急联系人">
          {{ currentConsultant.emergency_name }}
        </a-descriptions-item>
        <a-descriptions-item label="关系">
          {{ currentConsultant.emergency_relationship_text }}
        </a-descriptions-item>
        <a-descriptions-item label="紧急联系人电话">
          {{ currentConsultant.emergency_phone }}
        </a-descriptions-item>
        <a-descriptions-item label="是否默认">
          <a-tag v-if="currentConsultant.is_default" color="gold">
            <star-filled />
            默认咨询人
          </a-tag>
          <span v-else>否</span>
        </a-descriptions-item>
        <a-descriptions-item label="状态">
          <a-tag :color="currentConsultant.status === 1 ? 'success' : 'default'">
            {{ currentConsultant.status_text }}
          </a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="创建时间">
          {{ currentConsultant.create_time }}
        </a-descriptions-item>
        <a-descriptions-item label="备注信息" :span="2">
          {{ currentConsultant.notes || '-' }}
        </a-descriptions-item>
      </a-descriptions>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { 
  PlusOutlined, 
  SearchOutlined, 
  StarFilled,
  ReloadOutlined
} from '@ant-design/icons-vue'
import { consultantAPI } from '@/api/consultant'
import { userAPI } from '@/api/admin'

// 数据状态
const loading = ref(false)
const consultants = ref([])
const modalVisible = ref(false)
const detailVisible = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)
const currentConsultant = ref(null)
const formRef = ref()
const userOptions = ref([])
const stats = ref({})

// 搜索表单
const searchForm = reactive({
  keyword: '',
  gender: '',
  status: null,
  page: 1,
  per_page: 10
})

// 分页
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total) => `共 ${total} 条记录`
})

// 表单数据
const form = reactive({
  user_id: '',
  real_name: '',
  birth_year: null,
  birth_month: null,
  gender: '',
  phone: '',
  emergency_name: '',
  emergency_relationship: '',
  emergency_phone: '',
  notes: '',
  is_default: false
})

// 表单验证规则
const rules = {
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 50, message: '姓名长度应在2-50个字符之间', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  phone: [
    { required: true, message: '请输入联系方式', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  emergency_name: [
    { required: true, message: '请输入紧急联系人姓名', trigger: 'blur' },
    { min: 2, max: 50, message: '姓名长度应在2-50个字符之间', trigger: 'blur' }
  ],
  emergency_relationship: [
    { required: true, message: '请选择关系', trigger: 'change' }
  ],
  emergency_phone: [
    { required: true, message: '请输入紧急联系人电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

// 表格列定义
const columns = [
  {
    title: '关联用户',
    dataIndex: 'user_info',
    key: 'user_info',
    width: 150
  },
  {
    title: '姓名',
    dataIndex: 'real_name',
    key: 'real_name',
    width: 100
  },
  {
    title: '性别',
    dataIndex: 'gender',
    key: 'gender',
    width: 80
  },
  {
    title: '出生日期',
    dataIndex: 'birth_date',
    key: 'birth_date',
    width: 120
  },
  {
    title: '联系方式',
    dataIndex: 'phone',
    key: 'phone',
    width: 120
  },
  {
    title: '紧急联系人',
    dataIndex: 'emergency_info',
    key: 'emergency_info',
    width: 200
  },
  {
    title: '默认',
    dataIndex: 'is_default',
    key: 'is_default',
    width: 80
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 80
  },
  {
    title: '创建时间',
    dataIndex: 'create_time',
    key: 'create_time',
    width: 160
  },
  {
    title: '操作',
    key: 'action',
    fixed: 'right',
    width: 220
  }
]

// 获取咨询人列表
const fetchConsultants = async () => {
  loading.value = true
  try {
    const params = {
      ...searchForm,
      page: pagination.current,
      per_page: pagination.pageSize
    }
    
    const response = await consultantAPI.getConsultants(params)
    if (response.success) {
      consultants.value = response.data.list
      pagination.total = response.data.total
    }
  } catch (error) {
    message.error('获取咨询人列表失败')
  } finally {
    loading.value = false
  }
}

// 获取统计信息
const fetchStats = async () => {
  try {
    const response = await consultantAPI.getConsultantStats()
    if (response.success) {
      stats.value = response.data
    }
  } catch (error) {
    console.error('获取统计信息失败', error)
  }
}

// 获取用户列表
const fetchUsers = async () => {
  try {
    const response = await userAPI.getUsers({ page: 1, per_page: 1000 })
    if (response.success) {
      userOptions.value = response.data.list
    }
  } catch (error) {
    console.error('获取用户列表失败', error)
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  fetchConsultants()
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    keyword: '',
    gender: '',
    status: null
  })
  pagination.current = 1
  fetchConsultants()
}

// 表格变化处理
const handleTableChange = (pag) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchConsultants()
}

// 显示创建模态框
const showCreateModal = () => {
  isEdit.value = false
  modalVisible.value = true
  resetForm()
}

// 编辑咨询人
const editConsultant = (record) => {
  isEdit.value = true
  modalVisible.value = true
  currentConsultant.value = record
  
  // 填充表单数据
  Object.assign(form, {
    user_id: record.user_id || '',
    real_name: record.real_name,
    birth_year: record.birth_year,
    birth_month: record.birth_month,
    gender: record.gender,
    phone: record.phone,
    emergency_name: record.emergency_name,
    emergency_relationship: record.emergency_relationship,
    emergency_phone: record.emergency_phone,
    notes: record.notes,
    is_default: record.is_default === 1
  })
}

// 查看咨询人详情
const viewConsultant = (record) => {
  currentConsultant.value = record
  detailVisible.value = true
}

// 用户变更处理
const handleUserChange = (userId) => {
  if (!userId) {
    form.is_default = false
  }
}

// 状态变更
const handleStatusChange = async (record, checked) => {
  record.statusLoading = true
  try {
    const data = { status: checked ? 1 : 0 }
    await consultantAPI.updateConsultant(record.id, data)
    record.status = checked ? 1 : 0
    record.status_text = checked ? '启用' : '禁用'
    message.success('状态更新成功')
  } catch (error) {
    message.error('状态更新失败')
  } finally {
    record.statusLoading = false
  }
}

// 设为默认
const setDefault = async (record) => {
  if (!record.user_info) {
    message.warning('该咨询人未关联用户，无法设为默认')
    return
  }
  
  try {
    await consultantAPI.setDefaultConsultant(record.id)
    message.success('设置默认咨询人成功')
    fetchConsultants()
  } catch (error) {
    message.error('设置默认咨询人失败')
  }
}

// 删除咨询人
const deleteConsultant = async (record) => {
  try {
    await consultantAPI.deleteConsultant(record.id)
    message.success('删除成功')
    fetchConsultants()
    fetchStats()
  } catch (error) {
    message.error('删除失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    submitLoading.value = true
    
    const formData = {
      ...form,
      is_default: form.is_default ? 1 : 0
    }
    
    if (isEdit.value) {
      await consultantAPI.updateConsultant(currentConsultant.value.id, formData)
      message.success('更新成功')
    } else {
      await consultantAPI.createConsultant(formData)
      message.success('创建成功')
    }
    
    modalVisible.value = false
    fetchConsultants()
    fetchStats()
  } catch (error) {
    if (error.errorFields) {
      // 表单验证错误
      return
    }
    message.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitLoading.value = false
  }
}

// 取消操作
const handleCancel = () => {
  modalVisible.value = false
  resetForm()
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    user_id: '',
    real_name: '',
    birth_year: null,
    birth_month: null,
    gender: '',
    phone: '',
    emergency_name: '',
    emergency_relationship: '',
    emergency_phone: '',
    notes: '',
    is_default: false
  })
  
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchConsultants()
  fetchStats()
  fetchUsers()
})
</script>

<style scoped>
.consultant-management {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 0 4px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.stats-section {
  margin-bottom: 16px;
}

.search-section {
  margin-bottom: 16px;
}

.table-section {
  background: white;
}

.ant-descriptions-item-label {
  font-weight: 600;
}
</style> 