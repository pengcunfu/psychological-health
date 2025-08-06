<template>
  <div class="workspace-management">
    <!-- 搜索栏和操作栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="工作室名称">
          <a-input 
            v-model:value="searchForm.name" 
            placeholder="请输入工作室名称" 
            style="width: 200px;"
            allow-clear 
          />
        </a-form-item>
        <a-form-item label="状态">
          <a-select 
            v-model:value="searchForm.status" 
            style="width: 120px;" 
            allow-clear 
            placeholder="请选择状态"
          >
            <a-select-option :value="1">营业中</a-select-option>
            <a-select-option :value="0">关闭</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
          <a-button style="margin-left: 8px;" @click="handleReset">重置</a-button>
        </a-form-item>
      </a-form>
      
      <div class="action-buttons">
        <a-button type="primary" @click="showAddModal">
          <template #icon>
            <PlusOutlined/>
          </template>
          添加工作室
        </a-button>
      </div>
    </div>

    <!-- 数据表格 -->
    <a-table
      :columns="columns"
      :data-source="workspaces"
      :loading="loading"
      :pagination="pagination"
      @change="handleTableChange"
      row-key="id"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'address'">
          <div class="address-cell">
            <span class="address-text">{{ record.address || '-' }}</span>
          </div>
        </template>
        
        <template v-if="column.key === 'business_hours'">
          {{ record.business_hours || '-' }}
        </template>
        
        <template v-if="column.key === 'distance'">
          {{ record.distance ? record.distance.toFixed(1) : '0.0' }}
        </template>
        
        <template v-if="column.key === 'status'">
          <a-tag :color="record.status === 1 ? 'green' : 'red'">
            {{ record.status === 1 ? '营业中' : '关闭' }}
          </a-tag>
        </template>
        
        <template v-if="column.key === 'action'">
          <a-space>
            <a-button type="link" size="small" @click="viewWorkspace(record)">
              查看
            </a-button>
            <a-button type="link" size="small" @click="showEditModal(record)">
              编辑
            </a-button>
            <a-popconfirm
              title="确定要删除该工作室吗？"
              @confirm="handleDelete(record.id)"
            >
              <a-button type="link" size="small" danger>
                删除
              </a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 添加/编辑工作室弹窗 -->
    <a-modal
      v-model:open="modalVisible"
      :title="modalTitle"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
      width="800px"
    >
      <a-form
        ref="workspaceFormRef"
        :model="workspaceForm"
        :rules="rules"
        layout="vertical"
      >
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="工作室名称" name="name">
              <a-input v-model:value="workspaceForm.name" placeholder="请输入工作室名称" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="状态" name="status">
              <a-radio-group v-model:value="workspaceForm.status">
                <a-radio :value="1">营业中</a-radio>
                <a-radio :value="0">关闭</a-radio>
              </a-radio-group>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="详细地址" name="address">
          <a-input v-model:value="workspaceForm.address" placeholder="请输入工作室详细地址" />
        </a-form-item>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="距离(km)" name="distance">
              <a-input-number 
                v-model:value="workspaceForm.distance" 
                :min="0" 
                :precision="1"
                style="width: 100%;" 
                placeholder="距离"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="纬度" name="latitude">
              <a-input-number 
                v-model:value="workspaceForm.latitude" 
                :min="-90" 
                :max="90"
                :precision="6"
                style="width: 100%;" 
                placeholder="纬度"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="经度" name="longitude">
              <a-input-number 
                v-model:value="workspaceForm.longitude" 
                :min="-180" 
                :max="180"
                :precision="6"
                style="width: 100%;" 
                placeholder="经度"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="营业时间" name="business_hours">
              <a-input v-model:value="workspaceForm.business_hours" placeholder="如：周一至周日 9:00-18:00" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="排序" name="sort_order">
              <a-input-number 
                v-model:value="workspaceForm.sort_order" 
                :min="0" 
                :max="9999"
                style="width: 100%;" 
                placeholder="排序值"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="封面图片" name="cover_image">
          <a-upload 
            v-model:file-list="coverFileList" 
            :before-upload="beforeUploadCover" 
            :custom-request="handleUploadCover"
            @remove="handleRemoveCover"
            list-type="picture-card" 
            :max-count="1"
            accept="image/*"
            :show-upload-list="{
              showPreviewIcon: true,
              showRemoveIcon: true,
              showDownloadIcon: false
            }"
          >
            <div v-if="coverFileList.length < 1">
              <upload-outlined />
              <div style="margin-top: 8px;">上传封面</div>
            </div>
          </a-upload>
        </a-form-item>

        <a-form-item label="环境照片" name="environment_images">
          <a-upload 
            v-model:file-list="environmentFileList" 
            :before-upload="beforeUploadEnvironment" 
            :custom-request="handleUploadEnvironment"
            @remove="handleRemoveEnvironment"
            list-type="picture-card" 
            :max-count="6"
            accept="image/*"
            multiple
            :show-upload-list="{
              showPreviewIcon: true,
              showRemoveIcon: true,
              showDownloadIcon: false
            }"
          >
            <div v-if="environmentFileList.length < 6">
              <upload-outlined />
              <div style="margin-top: 8px;">上传环境照片</div>
            </div>
          </a-upload>
        </a-form-item>

        <a-form-item label="工作室简介" name="introduction">
          <a-textarea 
            v-model:value="workspaceForm.introduction" 
            placeholder="请输入工作室简介（可选）" 
            :rows="4" 
          />
        </a-form-item>

        <a-form-item label="工作室寄语" name="slogan">
          <a-textarea 
            v-model:value="workspaceForm.slogan" 
            placeholder="请输入工作室寄语（可选）" 
            :rows="2" 
          />
        </a-form-item>
              </a-form>
    </a-modal>

    <!-- 查看工作室详情弹窗 -->
    <a-modal
      v-model:open="viewModalVisible"
      title="工作室详情"
      :footer="null"
      width="800px"
    >
      <div v-if="currentWorkspace" class="workspace-detail">
        <div class="detail-header">
          <h3>{{ currentWorkspace.name || '' }}</h3>
          <a-tag :color="currentWorkspace.status === 1 ? 'green' : 'red'">
            {{ currentWorkspace.status === 1 ? '营业中' : '关闭' }}
          </a-tag>
        </div>

        <a-divider/>

        <div class="detail-section">
          <a-descriptions bordered :column="2">
            <a-descriptions-item label="工作室名称" :span="2">{{ currentWorkspace.name || '-' }}</a-descriptions-item>
            <a-descriptions-item label="详细地址" :span="2">{{ currentWorkspace.address || '-' }}</a-descriptions-item>
            <a-descriptions-item label="距离">{{ currentWorkspace.distance ? currentWorkspace.distance.toFixed(1) + ' km' : '-' }}</a-descriptions-item>
            <a-descriptions-item label="营业时间">{{ currentWorkspace.business_hours || '-' }}</a-descriptions-item>
            <a-descriptions-item label="纬度">{{ currentWorkspace.latitude || '-' }}</a-descriptions-item>
            <a-descriptions-item label="经度">{{ currentWorkspace.longitude || '-' }}</a-descriptions-item>
            <a-descriptions-item label="排序">{{ currentWorkspace.sort_order || '-' }}</a-descriptions-item>
            <a-descriptions-item label="状态">
              <a-tag :color="currentWorkspace.status === 1 ? 'green' : 'red'">
                {{ currentWorkspace.status === 1 ? '营业中' : '关闭' }}
              </a-tag>
            </a-descriptions-item>
            <a-descriptions-item label="封面图片" :span="2">
              <img 
                v-if="currentWorkspace.cover_image" 
                :src="FileUploader.getFullImageUrl(currentWorkspace.cover_image)"
                style="max-width: 200px; max-height: 150px; object-fit: cover; border-radius: 4px;"
                alt="工作室封面"
              />
              <span v-else>-</span>
            </a-descriptions-item>
            <a-descriptions-item label="环境照片" :span="2">
              <div v-if="currentWorkspace.environment_images && currentWorkspace.environment_images.length > 0" class="environment-images">
                <img 
                  v-for="(img, index) in currentWorkspace.environment_images" 
                  :key="index"
                  :src="FileUploader.getFullImageUrl(img)"
                  style="width: 100px; height: 75px; object-fit: cover; border-radius: 4px; margin-right: 8px; margin-bottom: 8px;"
                  :alt="`环境照片${index + 1}`"
                />
              </div>
              <span v-else>-</span>
            </a-descriptions-item>
            <a-descriptions-item label="工作室简介" :span="2">
              <div class="intro-text">{{ currentWorkspace.introduction || '-' }}</div>
            </a-descriptions-item>
            <a-descriptions-item label="工作室寄语" :span="2">
              <div class="slogan-text">{{ currentWorkspace.slogan || '-' }}</div>
            </a-descriptions-item>
            <a-descriptions-item label="创建时间">{{ formatDate(currentWorkspace.create_time) }}</a-descriptions-item>
            <a-descriptions-item label="更新时间">{{ formatDate(currentWorkspace.update_time) }}</a-descriptions-item>
          </a-descriptions>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined, UploadOutlined } from '@ant-design/icons-vue'
import { getWorkspaces, createWorkspace, updateWorkspace, deleteWorkspace } from '@/api/admin'
import { FileUploader } from '@/api/upload'
    const loading = ref(false)
    const workspaces = ref([])
    const modalVisible = ref(false)
    const isEdit = ref(false)
const workspaceFormRef = ref()
const coverFileList = ref([])
const environmentFileList = ref([])
const viewModalVisible = ref(false)
const currentWorkspace = ref(null)

    const searchForm = reactive({
      name: '',
      status: undefined
    })

    const workspaceForm = reactive({
  name: '',
  cover_image: '',
  address: '',
  distance: 0,
  business_hours: '',
  environment_images: [],
  introduction: '',
  slogan: '',
  latitude: 0,
  longitude: 0,
  sort_order: 100,
  status: 1
})

    const pagination = reactive({
      current: 1,
      pageSize: 10,
      total: 0,
      showSizeChanger: true,
      showQuickJumper: true,
      showTotal: (total) => `共 ${total} 条记录`
    })

// 表格列定义
const columns = [
  {
    title: '工作室名称',
    dataIndex: 'name',
    key: 'name',
    width: 180
  },
  {
    title: '地址',
    dataIndex: 'address',
    key: 'address',
    width: 200
  },
  {
    title: '营业时间',
    dataIndex: 'business_hours',
    key: 'business_hours',
    width: 150
  },
  {
    title: '距离(km)',
    dataIndex: 'distance',
    key: 'distance',
    width: 100
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 80
  },
  {
    title: '排序',
    dataIndex: 'sort_order',
    key: 'sort_order',
    width: 80
  },
  {
    title: '操作',
    key: 'action',
    width: 150
  }
]

    // 表单校验规则
const rules = {
  name: [
    { required: true, message: '请输入工作室名称', trigger: 'blur' },
    { max: 200, message: '工作室名称不能超过200个字符', trigger: 'blur' }
  ],
  address: [
    { max: 500, message: '地址不能超过500个字符', trigger: 'blur' }
  ],
  business_hours: [
    { max: 200, message: '营业时间不能超过200个字符', trigger: 'blur' }
  ],
  introduction: [
    { max: 2000, message: '简介不能超过2000个字符', trigger: 'blur' }
  ],
  slogan: [
    { max: 500, message: '寄语不能超过500个字符', trigger: 'blur' }
  ],
  latitude: [
    { type: 'number', min: -90, max: 90, message: '纬度必须在-90到90之间', trigger: 'blur' }
  ],
  longitude: [
    { type: 'number', min: -180, max: 180, message: '经度必须在-180到180之间', trigger: 'blur' }
  ],
  distance: [
    { type: 'number', min: 0, message: '距离必须大于等于0', trigger: 'blur' }
  ],
  sort_order: [
    { required: true, message: '请输入排序值', trigger: 'blur' },
    { type: 'number', min: 0, max: 9999, message: '排序值必须在0-9999之间', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

    // 获取工作空间列表
    const fetchWorkspaces = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          name: searchForm.name,
          status: searchForm.status
        }

        const result = await getWorkspaces(params)
        if (result.code === 200) {
          workspaces.value = result.data.list || result.data.workspaces || []
          pagination.total = result.data.total
        }
      } catch (error) {
        message.error('获取工作空间列表失败')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current = 1
      fetchWorkspaces()
    }

    // 重置搜索
    const handleReset = () => {
      Object.assign(searchForm, {
        name: '',
        status: undefined
      })
      pagination.current = 1
      fetchWorkspaces()
    }

    // 表格分页改变
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchWorkspaces()
    }

    // 显示添加弹窗
    const showAddModal = () => {
      isEdit.value = false
      modalVisible.value = true
      resetForm()
    }

// 显示编辑弹窗
const showEditModal = (record) => {
  isEdit.value = true
  modalVisible.value = true
  
  Object.assign(workspaceForm, {
    id: record.id,
    name: record.name,
    cover_image: record.cover_image || '',
    address: record.address || '',
    distance: record.distance || 0,
    business_hours: record.business_hours || '',
    environment_images: record.environment_images || [],
    introduction: record.introduction || '',
    slogan: record.slogan || '',
    latitude: record.latitude || 0,
    longitude: record.longitude || 0,
    sort_order: record.sort_order || 100,
    status: record.status
  })
  
  // 设置封面图片
  if (record.cover_image) {
    const fullImageUrl = FileUploader.getFullImageUrl(record.cover_image)
    coverFileList.value = [{
      uid: '-1',
      name: 'cover.png',
      status: 'done',
      url: fullImageUrl,
      thumbUrl: fullImageUrl
    }]
  } else {
    coverFileList.value = []
  }
  
  // 设置环境照片
  if (record.environment_images && record.environment_images.length > 0) {
    environmentFileList.value = record.environment_images.map((img, index) => ({
      uid: `-${index + 2}`,
      name: `environment-${index + 1}.png`,
      status: 'done',
      url: FileUploader.getFullImageUrl(img),
      thumbUrl: FileUploader.getFullImageUrl(img)
    }))
  } else {
    environmentFileList.value = []
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(workspaceForm, {
    name: '',
    cover_image: '',
    address: '',
    distance: 0,
    business_hours: '',
    environment_images: [],
    introduction: '',
    slogan: '',
    latitude: 0,
    longitude: 0,
    sort_order: 100,
    status: 1
  })
  coverFileList.value = []
  environmentFileList.value = []
  workspaceFormRef.value?.resetFields()
}

    // 模态框确定
    const handleModalOk = async () => {
      try {
        await workspaceFormRef.value.validate()

        const data = { ...workspaceForm }
        delete data.id

        if (isEdit.value) {
          const result = await updateWorkspace(workspaceForm.id, data)
          if (result.code === 200) {
            message.success('更新成功')
            modalVisible.value = false
            fetchWorkspaces()
          }
        } else {
          const result = await createWorkspace(data)
          if (result.code === 200 || result.code === 201) {
            message.success('创建成功')
            modalVisible.value = false
            fetchWorkspaces()
          }
        }
      } catch (error) {
        console.error('表单验证失败:', error)
      }
    }

    // 模态框取消
    const handleModalCancel = () => {
      modalVisible.value = false
      resetForm()
    }

    // 删除工作空间
    const handleDelete = async (id) => {
      try {
        const result = await deleteWorkspace(id)
        if (result.code === 200) {
          message.success('删除成功')
          fetchWorkspaces()
        }
      } catch (error) {
        message.error('删除失败')
      }
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }

// 查看工作室
const viewWorkspace = (record) => {
  currentWorkspace.value = record
  viewModalVisible.value = true
}

// 上传前验证（封面）
const beforeUploadCover = (file) => {
  try {
    FileUploader.validateImage(file, 2) // 封面限制2MB
    return true
  } catch (error) {
    message.error(error.message)
    return false
  }
}

// 上传前验证（环境照片）
const beforeUploadEnvironment = (file) => {
  try {
    FileUploader.validateImage(file, 5) // 环境照片限制5MB
    return true
  } catch (error) {
    message.error(error.message)
    return false
  }
}

// 上传封面
const handleUploadCover = async ({ file }) => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('/api/upload/image', {
      method: 'POST',
      body: formData
    })

    const result = await response.json()
    
    if (result.success && result.data) {
      const imageUrl = result.data.url
      const fullImageUrl = FileUploader.getFullImageUrl(imageUrl)
      
      workspaceForm.cover_image = imageUrl
      
      coverFileList.value = [{
        uid: file.uid,
        name: result.data.original_filename || file.name,
        status: 'done',
        url: fullImageUrl,
        thumbUrl: fullImageUrl
      }]
      
      message.success('封面上传成功')
    } else {
      message.error(result.message || '封面上传失败')
    }
  } catch (error) {
    console.error('封面上传失败:', error)
    message.error('封面上传失败')
  }
}

// 上传环境照片
const handleUploadEnvironment = async ({ file }) => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('/api/upload/image', {
      method: 'POST',
      body: formData
    })

    const result = await response.json()
    
    if (result.success && result.data) {
      const imageUrl = result.data.url
      const fullImageUrl = FileUploader.getFullImageUrl(imageUrl)
      
      // 添加到环境照片数组
      workspaceForm.environment_images.push(imageUrl)
      
      // 更新环境照片文件列表
      const newFile = {
        uid: file.uid,
        name: result.data.original_filename || file.name,
        status: 'done',
        url: fullImageUrl,
        thumbUrl: fullImageUrl
      }
      environmentFileList.value.push(newFile)
      
      message.success('环境照片上传成功')
    } else {
      message.error(result.message || '环境照片上传失败')
    }
  } catch (error) {
    console.error('环境照片上传失败:', error)
    message.error('环境照片上传失败')
  }
}

// 移除封面
const handleRemoveCover = () => {
  workspaceForm.cover_image = ''
  coverFileList.value = []
  message.success('封面已移除')
}

// 移除环境照片
const handleRemoveEnvironment = (file) => {
  const index = environmentFileList.value.findIndex(item => item.uid === file.uid)
  if (index > -1) {
    environmentFileList.value.splice(index, 1)
    workspaceForm.environment_images.splice(index, 1)
    message.success('环境照片已移除')
  }
}

const modalTitle = computed(() => isEdit.value ? '编辑工作室' : '添加工作室')

onMounted(() => {
  fetchWorkspaces()
})
</script>

<style lang="scss" scoped>
.workspace-management {
  padding: 0;
}

.search-and-action-bar {
  background: white;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 12px;
}

.search-form {
  flex: 1;
  min-width: 0;
}

.search-form {
  .ant-form-item {
    margin-bottom: 0;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.action-buttons {
  flex-shrink: 0;
}

.address-cell {
  max-width: 180px;
}

.address-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-size: 14px;
  line-height: 1.4;
  color: #666;
}

.workspace-detail {
  padding: 12px 0;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  h3 {
    margin: 0;
    color: #1890ff;
    font-size: 18px;
  }
}

.detail-section {
  margin-bottom: 16px;
}

.environment-images {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.intro-text, .slogan-text {
  line-height: 1.6;
  white-space: pre-wrap;
}

@media (max-width: 768px) {
  .workspace-management {
    padding: 8px;
  }

  .search-and-action-bar {
    padding: 8px;
    margin-bottom: 8px;
    flex-direction: column;
    align-items: stretch;
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

  .action-buttons {
    width: 100%;
  }

  .action-buttons {
    .ant-btn {
      width: 100%;
    }
  }

  .address-cell {
    max-width: 150px;
  }
}

@media (max-width: 576px) {
  .search-and-action-bar {
    padding: 6px;
  }

  .search-form {
    .ant-form-item label {
      font-size: 13px;
    }

    .ant-input,
    .ant-select {
      font-size: 13px;
    }
  }

     .address-cell {
     max-width: 120px;
   }
 }
 </style> 