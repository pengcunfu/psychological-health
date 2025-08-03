<template>
  <div class="user-management">
    <!-- 搜索栏和添加按钮在同一行 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="用户名">
          <a-input v-model:value="searchForm.username" placeholder="请输入用户名" style="width: 200px;" />
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
        添加用户
      </a-button>
    </div>

    <!-- 用户列表 -->
    <a-table :columns="columns" :data-source="users" :loading="loading" :pagination="pagination"
      @change="handleTableChange" row-key="id">
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'avatar'">
          <a-avatar :src="record.avatar" :alt="record.username">
            {{ record.username?.[0]?.toUpperCase() }}
          </a-avatar>
        </template>
        
        <template v-if="column.key === 'roles'">
          <a-tag v-for="role in record.roles" :key="role.id" color="blue">
            {{ role.name }}
          </a-tag>
        </template>
        
        <template v-if="column.key === 'create_time'">
          {{ formatDate(record.create_time) }}
        </template>
        
        <template v-if="column.key === 'action'">
          <a-space>
            <a-button type="link" size="small" @click="editUser(record)">
              编辑
            </a-button>
            <a-button type="link" size="small" @click="viewUser(record)">
              查看
            </a-button>
            <a-popconfirm title="确定要删除这个用户吗？" @confirm="deleteUser(record.id)">
              <a-button type="link" size="small" danger>
                删除
              </a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 添加/编辑用户弹窗 -->
    <a-modal v-model:open="modalVisible" :title="modalTitle" @ok="handleModalOk" @cancel="handleModalCancel"
      width="600px">
      <a-form ref="userFormRef" :model="userForm" :rules="userFormRules" layout="vertical">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="用户名" name="username">
              <a-input v-model:value="userForm.username" placeholder="请输入用户名" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="手机号" name="phone">
              <a-input v-model:value="userForm.phone" placeholder="请输入手机号" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="邮箱" name="email">
          <a-input v-model:value="userForm.email" placeholder="请输入邮箱" />
        </a-form-item>

        <a-form-item v-if="!isEdit" label="密码" name="password">
          <a-input-password v-model:value="userForm.password" placeholder="请输入密码" />
        </a-form-item>

        <a-form-item label="头像" name="avatar">
          <a-upload 
            v-model:file-list="fileList" 
            :before-upload="beforeUpload" 
            :custom-request="uploadAvatar"
            list-type="picture-card" 
            :max-count="1"
            :show-upload-list="{ showPreviewIcon: false, showRemoveIcon: true }"
            @remove="handleRemoveAvatar"
          >
            <div v-if="fileList.length < 1">
              <upload-outlined />
              <div>上传头像</div>
            </div>
          </a-upload>
          <div class="upload-tips">支持 jpg、png 格式，文件大小不超过 2MB</div>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 查看用户详情弹窗 -->
    <a-modal v-model:open="viewModalVisible" title="用户详情" :footer="null" width="500px">
      <div v-if="currentUser" class="user-detail">
        <div class="detail-item">
          <span class="label">头像：</span>
          <a-avatar :src="currentUser.avatar" size="large">
            {{ currentUser.username?.[0]?.toUpperCase() }}
          </a-avatar>
        </div>
        <div class="detail-item">
          <span class="label">用户名：</span>
          <span>{{ currentUser.username }}</span>
        </div>
        <div class="detail-item">
          <span class="label">手机号：</span>
          <span>{{ currentUser.phone || '未设置' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">邮箱：</span>
          <span>{{ currentUser.email || '未设置' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">角色：</span>
          <a-tag v-for="role in currentUser.roles" :key="role.id" color="blue">
            {{ role.name }}
          </a-tag>
        </div>
        <div class="detail-item">
          <span class="label">创建时间：</span>
          <span>{{ formatDate(currentUser.create_time) }}</span>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined, UploadOutlined } from '@ant-design/icons-vue'
import { userAPI } from '@/api/admin'

export default {
  name: 'UserManagement',
  components: {
    PlusOutlined,
    UploadOutlined
  },
  setup() {
    const loading = ref(false)
    const users = ref([])
    const modalVisible = ref(false)
    const viewModalVisible = ref(false)
    const isEdit = ref(false)
    const currentUser = ref(null)
    const userFormRef = ref()
    const fileList = ref([])

    const searchForm = reactive({
      username: ''
    })

    const userForm = reactive({
      username: '',
      phone: '',
      email: '',
      password: '',
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
        title: '用户名',
        dataIndex: 'username',
        key: 'username'
      },
      {
        title: '手机号',
        dataIndex: 'phone',
        key: 'phone'
      },
      {
        title: '邮箱',
        dataIndex: 'email',
        key: 'email'
      },
      {
        title: '角色',
        dataIndex: 'roles',
        key: 'roles'
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

    const userFormRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度为3-20个字符', trigger: 'blur' }
      ],
      email: [
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 3, message: '密码长度至少6个字符', trigger: 'blur' }
      ]
    }

    // 获取用户列表
    const fetchUsers = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          username: searchForm.username
        }

        const result = await userAPI.getUsers(params)
        if (result.code === 200) {
          users.value = result.data.list
          pagination.total = result.data.total
        }
      } catch (error) {
        message.error('获取用户列表失败')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current = 1
      fetchUsers()
    }

    // 重置搜索
    const resetSearch = () => {
      Object.assign(searchForm, {
        username: ''
      })
      pagination.current = 1
      fetchUsers()
    }

    // 表格分页改变
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchUsers()
    }

    // 显示添加模态框
    const showAddModal = () => {
      isEdit.value = false
      modalVisible.value = true
      resetUserForm()
    }

    // 编辑用户
    const editUser = (user) => {
      isEdit.value = true
      modalVisible.value = true
      Object.assign(userForm, {
        id: user.id,
        username: user.username,
        phone: user.phone,
        email: user.email,
        avatar: user.avatar
      })
      if (user.avatar) {
        fileList.value = [{
          uid: '-1',
          name: 'avatar.png',
          status: 'done',
          url: user.avatar
        }]
      }
    }

    // 查看用户
    const viewUser = (user) => {
      currentUser.value = user
      viewModalVisible.value = true
    }

    // 删除用户
    const deleteUser = async (id) => {
      try {
        const result = await userAPI.deleteUser(id)
        if (result.code === 200) {
          message.success('删除成功')
          fetchUsers()
        }
      } catch (error) {
        message.error('删除失败')
      }
    }

    // 模态框确定
    const handleModalOk = async () => {
      try {
        await userFormRef.value.validate()

        const data = { ...userForm }
        delete data.id

        if (isEdit.value) {
          const result = await userAPI.updateUser(userForm.id, data)
          if (result.code === 200) {
            message.success('更新成功')
            modalVisible.value = false
            fetchUsers()
          }
        } else {
          const result = await userAPI.createUser(data)
          if (result.code === 200 || result.code === 201) {
            message.success('创建成功')
            modalVisible.value = false
            fetchUsers()
          }
        }
      } catch (error) {
        console.error('Form validation failed:', error)
      }
    }

    // 模态框取消
    const handleModalCancel = () => {
      modalVisible.value = false
      resetUserForm()
    }

    // 重置用户表单
    const resetUserForm = () => {
      Object.assign(userForm, {
        username: '',
        phone: '',
        email: '',
        password: '',
        avatar: ''
      })
      fileList.value = []
      userFormRef.value?.resetFields()
    }

    // 上传前验证
    const beforeUpload = (file) => {
      const isImage = file.type.startsWith('image/')
      if (!isImage) {
        message.error('只能上传图片文件!')
        return false
      }
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        message.error('图片大小不能超过 2MB!')
        return false
      }
      return false // 阻止自动上传
    }

    // 上传头像
    const uploadAvatar = async ({ file }) => {
      try {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('subfolder', 'avatars')
        formData.append('use_unique_name', 'true')

        // 调用文件上传接口
        const response = await fetch('/api/file/upload-to-static', {
          method: 'POST',
          body: formData,
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })

        const result = await response.json()
        
        if (result.success) {
          // 获取上传成功后的URL
          userForm.avatar = result.data.url
          fileList.value = [{
            uid: file.uid,
            name: file.name,
            status: 'done',
            url: result.data.url
          }]
          message.success('头像上传成功')
        } else {
          message.error(result.message || '头像上传失败')
          fileList.value = []
        }
      } catch (error) {
        console.error('头像上传失败:', error)
        message.error('头像上传失败')
        fileList.value = []
      }
    }

    // 移除头像
    const handleRemoveAvatar = () => {
      userForm.avatar = ''
      fileList.value = []
      message.success('头像已移除')
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }

    const modalTitle = computed(() => isEdit.value ? '编辑用户' : '添加用户')

    onMounted(() => {
      fetchUsers()
    })

    return {
      loading,
      users,
      searchForm,
      userForm,
      userFormRef,
      userFormRules,
      modalVisible,
      viewModalVisible,
      isEdit,
      currentUser,
      pagination,
      columns,
      fileList,
      modalTitle,
      fetchUsers,
      handleSearch,
      resetSearch,
      handleTableChange,
      showAddModal,
      editUser,
      viewUser,
      deleteUser,
      handleModalOk,
      handleModalCancel,
      beforeUpload,
      uploadAvatar,
      handleRemoveAvatar,
      formatDate
    }
  }
}
</script>

<style scoped>
.user-management {
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

.user-detail {
  padding: 12px 0;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.detail-item .label {
  font-weight: 500;
  width: 80px;
  color: #666;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.upload-tips {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
}

@media (max-width: 768px) {
  .user-management {
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
}
</style>