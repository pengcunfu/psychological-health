<template>
  <div class="group-management">
    <!-- 搜索栏和操作栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="群组标题">
          <a-input
              v-model:value="searchForm.title"
              placeholder="请输入群组标题"
              style="width: 200px;"
          />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
          <a-button style="margin-left: 8px;" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>
      
      <div class="action-buttons">
        <a-button type="primary" @click="showAddModal">
          <template #icon>
            <PlusOutlined/>
          </template>
          添加群组
        </a-button>
      </div>
    </div>

    <!-- 群组列表 -->
    <a-table
        :columns="columns"
        :data-source="groups"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'type'">
          <a-tag :color="record.type === 'online' ? 'blue' : 'green'">
            {{ record.type === 'online' ? '线上' : '线下' }}
          </a-tag>
        </template>
        
        <template v-if="column.key === 'price'">
          ¥{{ record.price || 0 }}
        </template>
        
        <template v-if="column.key === 'capacity'">
          {{ record.capacity || 0 }}
        </template>
        
        <template v-if="column.key === 'enrolled'">
          {{ record.enrolled || 0 }}
        </template>
        
        <template v-if="column.key === 'status'">
          <a-tag :color="getStatusColor(record.status)">
            {{ getStatusText(record.status) }}
          </a-tag>
        </template>
        
        <template v-if="column.key === 'action'">
          <a-space>
            <a-button type="link" size="small" @click="editGroup(record)">
              编辑
            </a-button>
            <a-button type="link" size="small" @click="viewGroup(record)">
              查看
            </a-button>
            <a-popconfirm
                title="确定要删除这个群组吗？"
                @confirm="deleteGroup(record.id)"
            >
              <a-button type="link" size="small" danger>
                删除
              </a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 添加/编辑群组弹窗 -->
    <a-modal
        v-model:open="modalVisible"
        :title="modalTitle"
        @ok="handleModalOk"
        @cancel="handleModalCancel"
        width="600px"
    >
      <a-form
          ref="groupFormRef"
          :model="groupForm"
          :rules="groupFormRules"
          layout="vertical"
      >
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="群组标题" name="title">
              <a-input v-model:value="groupForm.title" placeholder="请输入群组标题"/>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="类型" name="type">
              <a-select v-model:value="groupForm.type" placeholder="请选择类型">
                <a-select-option value="online">线上</a-select-option>
                <a-select-option value="offline">线下</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="导师" name="counselor_id">
              <a-select 
                v-model:value="groupForm.counselor_id" 
                placeholder="请选择导师"
                @change="handleCounselorChange"
                show-search
                :filter-option="(input, option) => 
                  option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                "
              >
                <a-select-option 
                  v-for="counselor in counselors" 
                  :key="counselor.id" 
                  :value="counselor.id"
                >
                  {{ counselor.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="导师姓名" name="counselor_name">
              <a-input v-model:value="groupForm.counselor_name" placeholder="导师姓名"/>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="价格（元）" name="price">
              <a-input-number 
                v-model:value="groupForm.price" 
                :min="0" 
                :precision="2"
                style="width: 100%"
                placeholder="请输入价格"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="人数容量" name="capacity">
              <a-input-number 
                v-model:value="groupForm.capacity" 
                :min="1" 
                style="width: 100%"
                placeholder="请输入容量"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="状态" name="status">
              <a-select v-model:value="groupForm.status" placeholder="请选择状态">
                <a-select-option :value="0">未开始</a-select-option>
                <a-select-option :value="1">报名中</a-select-option>
                <a-select-option :value="2">已结束</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="地点" name="location">
              <a-input v-model:value="groupForm.location" placeholder="请输入地点"/>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="城市" name="city">
              <a-input v-model:value="groupForm.city" placeholder="请输入城市"/>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="开始日期" name="start_date">
              <a-input v-model:value="groupForm.start_date" placeholder="请输入开始日期"/>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="持续时间" name="duration">
              <a-input v-model:value="groupForm.duration" placeholder="如：共20次"/>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="时间安排" name="schedule">
              <a-input v-model:value="groupForm.schedule" placeholder="如：每周一19:00-20:30"/>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="封面图片" name="cover_image">
          <a-upload 
            v-model:file-list="fileList" 
            :before-upload="beforeUpload" 
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
            <div v-if="fileList.length < 1">
              <upload-outlined />
              <div style="margin-top: 8px;">上传封面</div>
            </div>
          </a-upload>
        </a-form-item>

        <a-form-item label="群组描述" name="description">
          <a-textarea
              v-model:value="groupForm.description"
              placeholder="请输入群组描述（可选）"
              :rows="4"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 查看群组详情弹窗 -->
    <a-modal
        v-model:open="viewModalVisible"
        title="群组详情"
        :footer="null"
        width="600px"
    >
      <div v-if="currentGroup" class="group-detail">
        <div class="detail-header">
          <h3>{{ currentGroup.title || '' }}</h3>
        </div>

        <a-divider/>

        <div class="detail-section">
          <a-descriptions bordered :column="2">
            <a-descriptions-item label="群组标题" :span="2">{{ currentGroup.title || '-' }}</a-descriptions-item>
            <a-descriptions-item label="导师">{{ currentGroup.counselor_name || '-' }}</a-descriptions-item>
            <a-descriptions-item label="类型">
              <a-tag :color="currentGroup.type === 'online' ? 'blue' : 'green'">
                {{ currentGroup.type === 'online' ? '线上' : '线下' }}
              </a-tag>
            </a-descriptions-item>
            <a-descriptions-item label="价格">¥{{ currentGroup.price || 0 }}</a-descriptions-item>
            <a-descriptions-item label="状态">
              <a-tag :color="getStatusColor(currentGroup.status)">
                {{ getStatusText(currentGroup.status) }}
              </a-tag>
            </a-descriptions-item>
            <a-descriptions-item label="人数容量">{{ currentGroup.capacity || 0 }}</a-descriptions-item>
            <a-descriptions-item label="已报名">{{ currentGroup.enrolled || 0 }}</a-descriptions-item>
            <a-descriptions-item label="地点">{{ currentGroup.location || '-' }}</a-descriptions-item>
            <a-descriptions-item label="城市">{{ currentGroup.city || '-' }}</a-descriptions-item>
            <a-descriptions-item label="开始日期">{{ currentGroup.start_date || '-' }}</a-descriptions-item>
            <a-descriptions-item label="持续时间">{{ currentGroup.duration || '-' }}</a-descriptions-item>
            <a-descriptions-item label="时间安排" :span="2">{{ currentGroup.schedule || '-' }}</a-descriptions-item>
            <a-descriptions-item label="封面图片" :span="2">
              <img 
                v-if="currentGroup.cover_image" 
                :src="FileUploader.getFullImageUrl(currentGroup.cover_image)"
                style="max-width: 200px; max-height: 150px; object-fit: cover;"
                alt="封面图片"
              />
              <span v-else>-</span>
            </a-descriptions-item>
            <a-descriptions-item label="群组描述" :span="2">{{ currentGroup.description || '-' }}</a-descriptions-item>
            <a-descriptions-item label="创建时间">{{ formatDate(currentGroup.create_time) }}</a-descriptions-item>
            <a-descriptions-item label="更新时间">{{ formatDate(currentGroup.update_time) }}</a-descriptions-item>
          </a-descriptions>
        </div>

        <!-- 这里可以添加群组成员列表等更多信息 -->
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import {ref, reactive, onMounted, computed} from 'vue'
import {message} from 'ant-design-vue'
import {PlusOutlined, UploadOutlined} from '@ant-design/icons-vue'
import {groupAPI, counselorAPI} from '@/api'
import {FileUploader} from '@/api/upload'
    const loading = ref(false)
    const groups = ref([])
    const modalVisible = ref(false)
    const viewModalVisible = ref(false)
    const isEdit = ref(false)
const currentGroup = ref(null)
const groupFormRef = ref()
const counselors = ref([])
const fileList = ref([])

    const searchForm = reactive({
      title: ''
    })

    const groupForm = reactive({
  title: '',
  cover_image: '',
  counselor_id: '',
  counselor_name: '',
  price: 0,
  capacity: 10,
  location: '',
  city: '',
  type: 'online',
  start_date: '',
  duration: '',
  schedule: '',
  description: '',
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

    const columns = [
  {
    title: '群组标题',
    dataIndex: 'title',
    key: 'title',
    width: 180
  },
  {
    title: '导师',
    dataIndex: 'counselor_name',
    key: 'counselor_name',
    width: 120
  },
  {
    title: '类型',
    dataIndex: 'type',
    key: 'type',
    width: 80
  },
  {
    title: '价格',
    dataIndex: 'price',
    key: 'price',
    width: 100
  },
  {
    title: '容量',
    dataIndex: 'capacity',
    key: 'capacity',
    width: 80
  },
  {
    title: '已报名',
    dataIndex: 'enrolled',
    key: 'enrolled',
    width: 80
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 100
  },
  {
    title: '操作',
    key: 'action',
    width: 150
  }
]

    const groupFormRules = {
  title: [
    {required: true, message: '请输入群组标题', trigger: 'blur'},
    {max: 200, message: '群组标题不能超过200个字符', trigger: 'blur'}
  ],
  counselor_id: [
    {required: true, message: '请选择导师', trigger: 'change'}
  ],
  counselor_name: [
    {required: true, message: '请输入导师姓名', trigger: 'blur'}
  ],
  price: [
    {type: 'number', min: 0, message: '价格必须大于等于0', trigger: 'blur'}
  ],
  capacity: [
    {type: 'number', min: 1, message: '人数容量必须大于等于1', trigger: 'blur'}
  ],
  type: [
    {required: true, message: '请选择类型', trigger: 'change'}
  ]
}

    // 获取咨询师列表
const fetchCounselors = async () => {
  try {
    const result = await counselorAPI.getCounselors({ page: 1, per_page: 100 })
    if (result.code === 200) {
      counselors.value = result.data.list || []
    }
  } catch (error) {
    console.error('获取咨询师列表失败:', error)
    message.error('获取咨询师列表失败')
  }
}

// 获取群组列表
const fetchGroups = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          title: searchForm.title
        }

        const result = await groupAPI.getGroups(params)
        if (result.code === 200) {
          groups.value = result.data.groups || result.data.list || []
          pagination.total = result.data.total || 0
        }
      } catch (error) {
        console.error('获取群组列表失败:', error)
        message.error('获取群组列表失败')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current = 1
      fetchGroups()
    }

    // 重置搜索
    const resetSearch = () => {
      Object.assign(searchForm, {
        title: ''
      })
      pagination.current = 1
      fetchGroups()
    }

    // 表格分页改变
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchGroups()
    }

    // 显示添加模态框
    const showAddModal = () => {
      isEdit.value = false
      modalVisible.value = true
      resetGroupForm()
    }

    // 编辑群组
const editGroup = (group) => {
  isEdit.value = true
  modalVisible.value = true

  // 填充表单数据
  Object.assign(groupForm, {
    id: group.id,
    title: group.title,
    cover_image: group.cover_image || '',
    counselor_id: group.counselor_id || '',
    counselor_name: group.counselor_name || '',
    price: group.price || 0,
    capacity: group.capacity || 10,
    location: group.location || '',
    city: group.city || '',
    type: group.type || 'online',
    start_date: group.start_date || '',
    duration: group.duration || '',
    schedule: group.schedule || '',
    description: group.description || '',
    status: group.status !== undefined ? group.status : 1
  })
  
  // 设置封面图片
  if (group.cover_image) {
    const fullImageUrl = FileUploader.getFullImageUrl(group.cover_image)
    fileList.value = [{
      uid: '-1',
      name: 'cover.png',
      status: 'done',
      url: fullImageUrl,
      thumbUrl: fullImageUrl
    }]
  } else {
    fileList.value = []
  }
}

    // 查看群组
    const viewGroup = (group) => {
      currentGroup.value = group
      viewModalVisible.value = true
    }

    // 删除群组
    const deleteGroup = async (id) => {
      try {
        const result = await groupAPI.deleteGroup(id)
        if (result.code === 200) {
          message.success('删除成功')
          fetchGroups()
        } else {
          message.error(result.message || '删除失败')
        }
      } catch (error) {
        console.error('删除群组失败:', error)
        message.error('删除群组失败')
      }
    }

    // 模态框确定
    const handleModalOk = async () => {
      try {
        await groupFormRef.value.validate()

        const data = { ...groupForm }
        delete data.id

        if (isEdit.value) {
          // 编辑群组
          const result = await groupAPI.updateGroup(groupForm.id, data)
          if (result.code === 200) {
            message.success('更新成功')
            modalVisible.value = false
            fetchGroups()
          } else {
            message.error(result.message || '更新失败')
          }
        } else {
          // 创建群组
          const result = await groupAPI.createGroup(data)
          if (result.code === 200 || result.code === 201) {
            message.success('创建成功')
            modalVisible.value = false
            fetchGroups()
          } else {
            message.error(result.message || '创建失败')
          }
        }
      } catch (error) {
        console.error('表单验证失败:', error)
      }
    }

    // 模态框取消
    const handleModalCancel = () => {
      modalVisible.value = false
      resetGroupForm()
    }

    // 重置群组表单
const resetGroupForm = () => {
  Object.assign(groupForm, {
    title: '',
    cover_image: '',
    counselor_id: '',
    counselor_name: '',
    price: 0,
    capacity: 10,
    location: '',
    city: '',
    type: 'online',
    start_date: '',
    duration: '',
    schedule: '',
    description: '',
    status: 1
  })
  fileList.value = []
  groupFormRef.value?.resetFields()
}

    // 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 获取状态颜色
const getStatusColor = (status) => {
  switch (status) {
    case 0: return 'default'
    case 1: return 'processing'
    case 2: return 'success'
    default: return 'default'
  }
}

// 获取状态文本
const getStatusText = (status) => {
  switch (status) {
    case 0: return '未开始'
    case 1: return '报名中'
    case 2: return '已结束'
    default: return '未知'
  }
}

    // 处理导师选择
const handleCounselorChange = (counselorId) => {
  const selectedCounselor = counselors.value.find(c => c.id === counselorId)
  if (selectedCounselor) {
    groupForm.counselor_name = selectedCounselor.name
  }
}

// 上传前验证
const beforeUpload = (file) => {
  try {
    FileUploader.validateImage(file, 2) // 封面限制2MB
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
      
      groupForm.cover_image = imageUrl
      
      fileList.value = [{
        uid: file.uid,
        name: result.data.original_filename || file.name,
        status: 'done',
        url: fullImageUrl,
        response: result.data,
        thumbUrl: fullImageUrl
      }]
      
      message.success('封面上传成功')
    } else {
      fileList.value = [{
        uid: file.uid,
        name: file.name,
        status: 'error'
      }]
      message.error(result.message || '封面上传失败')
    }
  } catch (error) {
    console.error('封面上传失败:', error)
    fileList.value = [{
      uid: file.uid,
      name: file.name,
      status: 'error'
    }]
    message.error('封面上传失败')
  }
}

// 移除封面
const handleRemoveCover = () => {
  groupForm.cover_image = ''
  fileList.value = []
  message.success('封面已移除')
}

const modalTitle = computed(() => isEdit.value ? '编辑群组' : '添加群组')

onMounted(() => {
  fetchGroups()
  fetchCounselors()
})
</script>

<style lang="scss" scoped>
.group-management {
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

.description-cell {
  max-width: 280px;
}

.description-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-size: 14px;
  line-height: 1.4;
  color: #666;
}

.group-detail {
  padding: 12px 0;
}

.detail-header {
  margin-bottom: 16px;
}

.detail-header {
  h3 {
    margin: 0 0 12px 0;
    color: #1890ff;
    font-size: 18px;
  }
}

.detail-section {
  margin-bottom: 16px;
}

@media (max-width: 768px) {
  .group-management {
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

  .description-cell {
    max-width: 200px;
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

    .ant-input {
      font-size: 13px;
    }
  }

  .description-cell {
    max-width: 150px;
  }
}
</style> 