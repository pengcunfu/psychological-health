<template>
  <div class="workspace-management">
    <div class="page-header">
      <h2>工作空间管理</h2>
      <a-button type="primary" @click="showAddModal">
        <plus-outlined /> 添加工作空间
      </a-button>
    </div>

    <!-- 搜索区域 -->
    <div class="search-container">
      <a-form layout="inline">
        <a-form-item label="工作空间名称">
          <a-input v-model:value="searchForm.name" placeholder="请输入工作空间名称" allowClear />
        </a-form-item>
        <a-form-item label="状态">
          <a-select v-model:value="searchForm.status" style="width: 120px" allowClear placeholder="请选择状态">
            <a-select-option :value="1">启用</a-select-option>
            <a-select-option :value="0">禁用</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="handleSearch">
            <search-outlined /> 搜索
          </a-button>
          <a-button style="margin-left: 8px" @click="handleReset">
            <reload-outlined /> 重置
          </a-button>
        </a-form-item>
      </a-form>
    </div>

    <!-- 数据表格 -->
    <a-table
      :columns="columns"
      :data-source="workspaces"
      :loading="loading"
      :pagination="pagination"
      @change="handleTableChange"
      rowKey="id"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'status'">
          <a-tag :color="record.status === 1 ? 'green' : 'red'">
            {{ record.status === 1 ? '启用' : '禁用' }}
          </a-tag>
        </template>
        <template v-if="column.key === 'action'">
          <a-space>
            <a @click="showEditModal(record)">编辑</a>
            <a-divider type="vertical" />
            <a-popconfirm
              title="确定要删除该工作空间吗?"
              ok-text="确定"
              cancel-text="取消"
              @confirm="handleDelete(record.id)"
            >
              <a class="danger-link">删除</a>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 添加/编辑工作空间弹窗 -->
    <a-modal
      v-model:visible="modalVisible"
      :title="modalTitle"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
    >
      <a-form
        ref="workspaceForm"
        :model="workspaceForm"
        :rules="rules"
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 20 }"
      >
        <a-form-item label="名称" name="name">
          <a-input v-model:value="workspaceForm.name" placeholder="请输入工作空间名称" />
        </a-form-item>
        <a-form-item label="描述" name="description">
          <a-textarea v-model:value="workspaceForm.description" placeholder="请输入工作空间描述" :rows="4" />
        </a-form-item>
        <a-form-item label="排序" name="sort_order">
          <a-input-number v-model:value="workspaceForm.sort_order" :min="0" style="width: 100%" />
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
import { defineComponent, ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined, SearchOutlined, ReloadOutlined } from '@ant-design/icons-vue'
import { getWorkspaces, createWorkspace, updateWorkspace, deleteWorkspace } from '@/api/admin'

export default defineComponent({
  name: 'WorkspaceManagement',
  components: {
    PlusOutlined,
    SearchOutlined,
    ReloadOutlined
  },
  setup() {
    // 表格列定义
    const columns = [
      {
        title: '工作空间名称',
        dataIndex: 'name',
        key: 'name'
      },
      {
        title: '描述',
        dataIndex: 'description',
        key: 'description',
        ellipsis: true
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
        width: 180
      },
      {
        title: '操作',
        key: 'action',
        width: 150
      }
    ]

    // 数据状态
    const workspaces = ref([])
    const loading = ref(false)
    const pagination = reactive({
      current: 1,
      pageSize: 10,
      total: 0,
      showTotal: (total) => `共 ${total} 条数据`
    })

    // 搜索表单
    const searchForm = reactive({
      name: '',
      status: undefined,
      page: 1,
      per_page: 10
    })

    // 工作空间表单
    const workspaceForm = reactive({
      id: '',
      name: '',
      description: '',
      sort_order: 0,
      status: 1
    })

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

    // 弹窗控制
    const modalVisible = ref(false)
    const modalTitle = ref('添加工作空间')
    const isEdit = ref(false)
    const workspaceFormRef = ref(null)

    // 获取工作空间列表
    const fetchWorkspaces = async () => {
      loading.value = true
      try {
        const res = await getWorkspaces({
          name: searchForm.name,
          status: searchForm.status,
          page: pagination.current,
          per_page: pagination.pageSize
        })
        workspaces.value = res.data.list
        pagination.total = res.data.total
      } catch (error) {
        message.error('获取工作空间列表失败：' + error.message)
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
      searchForm.name = ''
      searchForm.status = undefined
      pagination.current = 1
      fetchWorkspaces()
    }

    // 表格变化
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchWorkspaces()
    }

    // 显示添加弹窗
    const showAddModal = () => {
      isEdit.value = false
      modalTitle.value = '添加工作空间'
      resetForm()
      modalVisible.value = true
    }

    // 显示编辑弹窗
    const showEditModal = (record) => {
      isEdit.value = true
      modalTitle.value = '编辑工作空间'
      resetForm()
      
      // 填充表单数据
      workspaceForm.id = record.id
      workspaceForm.name = record.name
      workspaceForm.description = record.description
      workspaceForm.sort_order = record.sort_order
      workspaceForm.status = record.status
      
      modalVisible.value = true
    }

    // 重置表单
    const resetForm = () => {
      workspaceForm.id = ''
      workspaceForm.name = ''
      workspaceForm.description = ''
      workspaceForm.sort_order = 0
      workspaceForm.status = 1
      
      if (workspaceFormRef.value) {
        workspaceFormRef.value.resetFields()
      }
    }

    // 提交表单
    const handleModalOk = () => {
      workspaceFormRef.value.validate().then(async () => {
        try {
          if (isEdit.value) {
            await updateWorkspace(workspaceForm.id, workspaceForm)
            message.success('工作空间更新成功')
          } else {
            await createWorkspace(workspaceForm)
            message.success('工作空间创建成功')
          }
          
          modalVisible.value = false
          fetchWorkspaces()
        } catch (error) {
          message.error('操作失败：' + error.message)
        }
      }).catch(error => {
        console.log('表单校验失败', error)
      })
    }

    // 取消弹窗
    const handleModalCancel = () => {
      modalVisible.value = false
      resetForm()
    }

    // 删除工作空间
    const handleDelete = async (id) => {
      try {
        await deleteWorkspace(id)
        message.success('工作空间删除成功')
        fetchWorkspaces()
      } catch (error) {
        message.error('删除失败：' + error.message)
      }
    }

    onMounted(() => {
      fetchWorkspaces()
    })

    return {
      columns,
      workspaces,
      loading,
      pagination,
      searchForm,
      workspaceForm,
      rules,
      modalVisible,
      modalTitle,
      workspaceFormRef,
      handleSearch,
      handleReset,
      handleTableChange,
      showAddModal,
      showEditModal,
      handleModalOk,
      handleModalCancel,
      handleDelete
    }
  }
})
</script>

<style scoped>
.workspace-management {
  padding: 20px;
  background: #fff;
  border-radius: 4px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 18px;
}

.search-container {
  margin-bottom: 20px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 4px;
}

.danger-link {
  color: #ff4d4f;
}
</style> 