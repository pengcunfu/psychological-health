<template>
  <div class="counselor-management">
    <!-- 搜索栏和添加按钮在同一行 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="姓名">
          <a-input
              v-model:value="searchForm.name"
              placeholder="请输入咨询师姓名"
              style="width: 200px;"
          />
        </a-form-item>
        <a-form-item label="职称">
          <a-input
              v-model:value="searchForm.title"
              placeholder="请输入职称"
              style="width: 200px;"
          />
        </a-form-item>
        <a-form-item label="状态">
          <a-select
              v-model:value="searchForm.status"
              placeholder="请选择状态"
              style="width: 120px;"
              allow-clear
          >
            <a-select-option :value="1">在职</a-select-option>
            <a-select-option :value="0">离职</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
          <a-button style="margin-left: 8px;" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>
      
      <a-button type="primary" @click="showAddModal">
        <template #icon>
          <PlusOutlined/>
        </template>
        添加咨询师
      </a-button>
    </div>

    <!-- 咨询师列表 -->
    <a-table
        :columns="columns"
        :data-source="counselors"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'avatar'">
          <a-avatar :src="FileUploader.getFullImageUrl(record?.avatar)" :alt="record?.name || ''" size="large">
            {{ record?.name?.[0] || '' }}
          </a-avatar>
        </template>
        
        <template v-else-if="column.key === 'status'">
          <a-tag :color="record?.status === 1 ? 'green' : 'red'">
            {{ record?.status === 1 ? '在职' : '离职' }}
          </a-tag>
        </template>

        <template v-else-if="column.key === 'rating'">
          <a-rate :value="record?.rating || 0" disabled allow-half/>
          <span style="margin-left: 8px;">{{ record?.rating || 0 }}</span>
        </template>

        <template v-else-if="column.key === 'price'">
          {{ `${record?.price || 0} 元/小时` }}
        </template>

        <template v-else-if="column.key === 'create_time'">
          {{ formatDate(record?.create_time) }}
        </template>

        <template v-else-if="column.key === 'action'">
          <a-space>
            <a-button type="link" size="small" @click="editCounselor(record)">
              编辑
            </a-button>
            <a-button type="link" size="small" @click="viewCounselor(record)">
              查看
            </a-button>
            <a-popconfirm
                title="确定要删除这个咨询师吗？"
                @confirm="deleteCounselor(record.id)"
            >
              <a-button type="link" size="small" danger>
                删除
              </a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 添加/编辑咨询师弹窗 -->
    <a-modal
        v-model:open="modalVisible"
        :title="modalTitle"
        @ok="handleModalOk"
        @cancel="handleModalCancel"
        width="800px"
    >
      <a-form
          ref="counselorFormRef"
          :model="counselorForm"
          :rules="counselorFormRules"
          layout="vertical"
      >
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="姓名" name="name">
              <a-input v-model:value="counselorForm.name" placeholder="请输入咨询师姓名"/>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="职称" name="title">
              <a-input v-model:value="counselorForm.title" placeholder="请输入职称"/>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="手机号" name="phone">
              <a-input v-model:value="counselorForm.phone" placeholder="请输入手机号"/>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="邮箱" name="email">
              <a-input v-model:value="counselorForm.email" placeholder="请输入邮箱"/>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="状态" name="status">
              <a-select v-model:value="counselorForm.status" placeholder="请选择状态">
                <a-select-option :value="1">在职</a-select-option>
                <a-select-option :value="0">离职</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="咨询费用(元/小时)" name="price">
              <a-input-number
                  v-model:value="counselorForm.price"
                  placeholder="请输入咨询费用"
                  :min="0"
                  style="width: 100%;"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="专业领域" name="specialty">
          <a-textarea
              v-model:value="counselorForm.specialty"
              placeholder="请输入专业领域"
              :rows="3"
          />
        </a-form-item>

        <a-form-item label="个人简介" name="bio">
          <a-textarea
              v-model:value="counselorForm.bio"
              placeholder="请输入个人简介"
              :rows="4"
          />
        </a-form-item>

        <a-form-item label="头像" name="avatar">
          <a-upload
              v-model:file-list="fileList"
              :before-upload="beforeUpload"
              :custom-request="handleUploadAvatar"
              @remove="handleRemoveAvatar"
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
              <upload-outlined/>
              <div style="margin-top: 8px;">上传头像</div>
              <div style="color: #999; font-size: 12px; margin-top: 4px;">
                支持 JPG、PNG、GIF、WebP<br/>
                文件大小不超过 2MB
              </div>
            </div>
          </a-upload>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 查看咨询师详情弹窗 -->
    <a-modal
        v-model:open="viewModalVisible"
        title="咨询师详情"
        :footer="null"
        width="600px"
    >
      <div v-if="currentCounselor" class="counselor-detail">
        <div class="detail-header">
          <a-avatar :src="FileUploader.getFullImageUrl(currentCounselor.avatar)" size="large">
            {{ currentCounselor.name?.[0] }}
          </a-avatar>
          <div class="header-info">
            <h3>{{ currentCounselor.name }}</h3>
            <p>{{ currentCounselor.title }}</p>
            <a-rate :value="currentCounselor.rating" disabled allow-half/>
          </div>
        </div>

        <a-divider/>

        <div class="detail-item">
          <span class="label">手机号：</span>
          <span>{{ currentCounselor.phone || '未设置' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">邮箱：</span>
          <span>{{ currentCounselor.email || '未设置' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">状态：</span>
          <a-tag :color="currentCounselor.status === 1 ? 'green' : 'red'">
            {{ currentCounselor.status === 1 ? '在职' : '离职' }}
          </a-tag>
        </div>
        <div class="detail-item">
          <span class="label">咨询费用：</span>
          <span>{{ currentCounselor.price || 0 }} 元/小时</span>
        </div>
        <div class="detail-item">
          <span class="label">专业领域：</span>
          <p>{{ currentCounselor.specialty || '未设置' }}</p>
        </div>
        <div class="detail-item">
          <span class="label">个人简介：</span>
          <p>{{ currentCounselor.bio || '未设置' }}</p>
        </div>
        <div class="detail-item">
          <span class="label">创建时间：</span>
          <span>{{ formatDate(currentCounselor.create_time) }}</span>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script>
import {ref, reactive, onMounted, computed} from 'vue'
import {message} from 'ant-design-vue'
import {PlusOutlined, UploadOutlined} from '@ant-design/icons-vue'
import {counselorAPI} from '@/api'
import {uploadAvatar, FileUploader} from '@/api/upload'

export default {
  name: 'CounselorManagement',
  components: {
    PlusOutlined,
    UploadOutlined
  },
  setup() {
    const loading = ref(false)
    const counselors = ref([])
    const modalVisible = ref(false)
    const viewModalVisible = ref(false)
    const isEdit = ref(false)
    const currentCounselor = ref(null)
    const counselorFormRef = ref()
    const fileList = ref([])

    const searchForm = reactive({
      name: '',
      title: '',
      status: undefined
    })

    const counselorForm = reactive({
      name: '',
      title: '',
      phone: '',
      email: '',
      status: 1,
      price: 0,
      specialty: '',
      bio: '',
      avatar: ''
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
        title: '头像',
        dataIndex: 'avatar',
        key: 'avatar',
        width: 80
      },
      {
        title: '姓名',
        dataIndex: 'name',
        key: 'name'
      },
      {
        title: '职称',
        dataIndex: 'title',
        key: 'title'
      },
      {
        title: '手机号',
        dataIndex: 'phone',
        key: 'phone'
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status'
      },
      {
        title: '评分',
        dataIndex: 'rating',
        key: 'rating'
      },
      {
        title: '咨询费用',
        dataIndex: 'price',
        key: 'price'
      },
      {
        title: '创建时间',
        dataIndex: 'create_time',
        key: 'create_time'
      },
      {
        title: '操作',
        key: 'action',
        width: 180
      }
    ]

    const counselorFormRules = {
      name: [
        {required: true, message: '请输入咨询师姓名', trigger: 'blur'}
      ],
      title: [
        {required: true, message: '请输入职称', trigger: 'blur'}
      ],
      email: [
        {type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur'}
      ],
      status: [
        {required: true, message: '请选择状态', trigger: 'change'}
      ]
    }

    // 获取咨询师列表
    const fetchCounselors = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          name: searchForm.name,
          title: searchForm.title,
          status: searchForm.status
        }

        const result = await counselorAPI.getCounselors(params)
        if (result.code === 200) {
          counselors.value = result.data.list
          pagination.total = result.data.total
        }
      } catch (error) {
        message.error('获取咨询师列表失败')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current = 1
      fetchCounselors()
    }

    // 重置搜索
    const resetSearch = () => {
      Object.assign(searchForm, {
        name: '',
        title: '',
        status: undefined
      })
      pagination.current = 1
      fetchCounselors()
    }

    // 表格分页改变
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchCounselors()
    }

    // 显示添加模态框
    const showAddModal = () => {
      isEdit.value = false
      modalVisible.value = true
      resetCounselorForm()
    }

    // 编辑咨询师
    const editCounselor = (counselor) => {
      isEdit.value = true
      modalVisible.value = true
      Object.assign(counselorForm, {
        id: counselor.id,
        name: counselor.name,
        title: counselor.title,
        phone: counselor.phone,
        email: counselor.email,
        status: counselor.status,
        price: counselor.price,
        specialty: counselor.specialty,
        bio: counselor.bio,
        avatar: counselor.avatar
      })
      if (counselor.avatar) {
        // 使用封装的方法获取完整URL进行显示
        const fullImageUrl = FileUploader.getFullImageUrl(counselor.avatar)
        fileList.value = [{
          uid: '-1',
          name: 'avatar.png',
          status: 'done',
          url: fullImageUrl,
          thumbUrl: fullImageUrl
        }]
      } else {
        fileList.value = []
      }
    }

    // 查看咨询师
    const viewCounselor = (counselor) => {
      currentCounselor.value = counselor
      viewModalVisible.value = true
    }

    // 删除咨询师
    const deleteCounselor = async (id) => {
      try {
        const result = await counselorAPI.deleteCounselor(id)
        if (result.code === 200) {
          message.success('删除成功')
          fetchCounselors()
        }
      } catch (error) {
        message.error('删除失败')
      }
    }

    // 模态框确定
    const handleModalOk = async () => {
      try {
        await counselorFormRef.value.validate()

        const data = {...counselorForm}
        delete data.id

        if (isEdit.value) {
          const result = await counselorAPI.updateCounselor(counselorForm.id, data)
          if (result.code === 200) {
            message.success('更新成功')
            modalVisible.value = false
            fetchCounselors()
          }
        } else {
          const result = await counselorAPI.createCounselor(data)
          if (result.code === 200 || result.code === 201) {
            message.success('创建成功')
            modalVisible.value = false
            fetchCounselors()
          }
        }
      } catch (error) {
        console.error('Form validation failed:', error)
      }
    }

    // 模态框取消
    const handleModalCancel = () => {
      modalVisible.value = false
      resetCounselorForm()
    }

    // 重置咨询师表单
    const resetCounselorForm = () => {
      Object.assign(counselorForm, {
        name: '',
        title: '',
        phone: '',
        email: '',
        status: 1,
        price: 0,
        specialty: '',
        bio: '',
        avatar: ''
      })
      fileList.value = []
      counselorFormRef.value?.resetFields()
    }

    // 上传前验证
    const beforeUpload = (file) => {
      try {
        // 使用封装的验证方法
        FileUploader.validateImage(file, 2) // 头像限制2MB
        return true // 允许上传
      } catch (error) {
        message.error(error.message)
        return false
      }
    }

    // 上传头像
    const handleUploadAvatar = async ({file}) => {
      try {
        // 调用封装的头像上传接口
        const result = await uploadAvatar(file)
        
        if (result.success && result.data) {
          // 上传成功，设置头像URL
          const imageUrl = result.data.url
          // 使用封装的方法获取完整URL用于显示
          const fullImageUrl = FileUploader.getFullImageUrl(imageUrl)
          
          counselorForm.avatar = imageUrl // 保存相对路径到表单
          
          // 更新文件列表显示
          fileList.value = [{
            uid: file.uid,
            name: result.data.original_filename || file.name,
            status: 'done',
            url: fullImageUrl,
            response: result.data,
            thumbUrl: fullImageUrl
          }]
          
          message.success('头像上传成功')
        } else {
          // 上传失败
          fileList.value = [{
            uid: file.uid,
            name: file.name,
            status: 'error'
          }]
          message.error(result.message || '头像上传失败')
        }
      } catch (error) {
        console.error('头像上传失败:', error)
        fileList.value = [{
          uid: file.uid,
          name: file.name,
          status: 'error'
        }]
        message.error('头像上传失败')
      }
    }

    // 移除头像
    const handleRemoveAvatar = (file) => {
      counselorForm.avatar = '' // 清空头像URL
      fileList.value = fileList.value.filter(f => f.uid !== file.uid)
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }

    const modalTitle = computed(() => isEdit.value ? '编辑咨询师' : '添加咨询师')

    onMounted(() => {
      fetchCounselors()
    })

    return {
      loading,
      counselors,
      searchForm,
      counselorForm,
      counselorFormRef,
      counselorFormRules,
      modalVisible,
      viewModalVisible,
      isEdit,
      currentCounselor,
      pagination,
      columns,
      fileList,
      modalTitle,
      fetchCounselors,
      handleSearch,
      resetSearch,
      handleTableChange,
      showAddModal,
      editCounselor,
      viewCounselor,
      deleteCounselor,
      handleModalOk,
      handleModalCancel,
      beforeUpload,
      handleUploadAvatar,
      handleRemoveAvatar,
      formatDate,
      FileUploader
    }
  }
}
</script>

<style scoped>
.counselor-management {
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

.search-form .ant-form {
  flex: 1;
  margin-right: 12px;
}

.search-form .ant-form-item {
  margin-bottom: 0;
}

.search-form .ant-form-item:last-child {
  margin-bottom: 0;
}

.counselor-detail {
  padding: 12px 0;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-info h3 {
  margin: 0 0 3px 0;
  color: #1890ff;
}

.header-info p {
  margin: 0 0 6px 0;
  color: #666;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 12px;
}

.detail-item .label {
  font-weight: 500;
  width: 100px;
  color: #666;
  flex-shrink: 0;
}

.detail-item p {
  margin: 0;
  line-height: 1.6;
}

.detail-item:last-child {
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .counselor-management {
    padding: 8px;
  }

  .search-and-action-bar {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
    padding: 8px;
    margin-bottom: 8px;
  }

  .search-form .ant-form {
    width: 100%;
    margin-right: 0;
  }

  .detail-header {
    flex-direction: column;
    text-align: center;
  }
}
</style> 