<template>
  <div class="workspace-management">
    <!-- 搜索栏和操作栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="工作空间名称">
          <a-input 
            v-model:value="searchForm.name" 
            placeholder="请输入工作空间名称" 
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
            <a-select-option :value="1">启用</a-select-option>
            <a-select-option :value="0">禁用</a-select-option>
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
          添加工作空间
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
        <template v-if="column.key === 'description'">
          <div class="description-cell">
            <span class="description-text">{{ record.description || '-' }}</span>
          </div>
        </template>
        
        <template v-if="column.key === 'status'">
          <a-tag :color="record.status === 1 ? 'green' : 'red'">
            {{ record.status === 1 ? '启用' : '禁用' }}
          </a-tag>
        </template>
        
        <template v-if="column.key === 'create_time'">
          {{ formatDate(record.create_time) }}
        </template>
        
        <template v-if="column.key === 'action'">
          <a-space>
            <a-button type="link" size="small" @click="showEditModal(record)">
              编辑
            </a-button>
            <a-popconfirm
              title="确定要删除该工作空间吗？"
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

    <!-- 添加/编辑工作空间弹窗 -->
    <a-modal
      v-model:open="modalVisible"
      :title="modalTitle"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
      width="600px"
    >
      <a-form
        ref="workspaceFormRef"
        :model="workspaceForm"
        :rules="rules"
        layout="vertical"
      >
        <a-form-item label="工作空间名称" name="name">
          <a-input v-model:value="workspaceForm.name" placeholder="请输入工作空间名称" />
        </a-form-item>
        <a-form-item label="工作空间描述" name="description">
          <a-textarea 
            v-model:value="workspaceForm.description" 
            placeholder="请输入工作空间描述（可选）" 
            :rows="4" 
          />
        </a-form-item>
        <a-form-item label="排序" name="sort_order">
          <a-input-number 
            v-model:value="workspaceForm.sort_order" 
            :min="0" 
            style="width: 100%;" 
            placeholder="请输入排序值（数字越小越靠前）"
          />
        </a-form-item>
        <a-form-item label="状态" name="status">
          <a-radio-group v-model:value="workspaceForm.status">
            <a-radio :value="1">启用</a-radio>
            <a-radio :value="0">禁用</a-radio>
          </a-radio-group>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { getWorkspaces, createWorkspace, updateWorkspace, deleteWorkspace } from '@/api/admin'

export default {
  name: 'WorkspaceManagement',
  components: {
    PlusOutlined
  },
  setup() {
    const loading = ref(false)
    const workspaces = ref([])
    const modalVisible = ref(false)
    const isEdit = ref(false)
    const workspaceFormRef = ref()

    const searchForm = reactive({
      name: '',
      status: undefined
    })

    const workspaceForm = reactive({
      name: '',
      description: '',
      sort_order: 0,
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
        title: '工作空间名称',
        dataIndex: 'name',
        key: 'name',
        width: 200
      },
      {
        title: '描述',
        dataIndex: 'description',
        key: 'description',
        width: 300
      },
      {
        title: '排序',
        dataIndex: 'sort_order',
        key: 'sort_order',
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
        width: 150
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
        { required: true, message: '请输入工作空间名称', trigger: 'blur' },
        { max: 50, message: '工作空间名称不能超过50个字符', trigger: 'blur' }
      ],
      sort_order: [
        { required: true, message: '请输入排序值', trigger: 'blur' }
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
        description: record.description,
        sort_order: record.sort_order,
        status: record.status
      })
    }

    // 重置表单
    const resetForm = () => {
      Object.assign(workspaceForm, {
        name: '',
        description: '',
        sort_order: 0,
        status: 1
      })
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

    const modalTitle = computed(() => isEdit.value ? '编辑工作空间' : '添加工作空间')

    onMounted(() => {
      fetchWorkspaces()
    })

    return {
      loading,
      workspaces,
      searchForm,
      workspaceForm,
      workspaceFormRef,
      rules,
      modalVisible,
      isEdit,
      pagination,
      columns,
      modalTitle,
      fetchWorkspaces,
      handleSearch,
      handleReset,
      handleTableChange,
      showAddModal,
      showEditModal,
      handleModalOk,
      handleModalCancel,
      handleDelete,
      formatDate
    }
  }
}
</script>

<style scoped>
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

.search-form .ant-form-item {
  margin-bottom: 0;
}

.search-form .ant-form-item:last-child {
  margin-bottom: 0;
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

  .search-form .ant-form {
    flex-direction: column;
  }

  .search-form .ant-form-item {
    margin-bottom: 8px;
  }

  .search-form .ant-form-item:last-child {
    margin-bottom: 0;
  }

  .action-buttons {
    width: 100%;
  }

  .action-buttons .ant-btn {
    width: 100%;
  }

  .description-cell {
    max-width: 200px;
  }
}

@media (max-width: 576px) {
  .search-and-action-bar {
    padding: 6px;
  }

  .search-form .ant-form-item label {
    font-size: 13px;
  }

  .search-form .ant-input,
  .search-form .ant-select {
    font-size: 13px;
  }

     .description-cell {
     max-width: 150px;
   }
 }
 </style> 