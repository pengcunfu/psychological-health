<template>
  <div class="role-management">
    <!-- 搜索栏和添加按钮在同一行 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" class="search-form">
        <a-form-item label="关键词">
          <a-input v-model:value="searchForm.keyword" placeholder="角色名称/代码" allowClear />
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

      <a-button type="primary" @click="showAddModal">
        <plus-outlined /> 添加角色
      </a-button>
    </div>

    <!-- 数据表格 -->
    <a-table :columns="columns" :data-source="roles" :loading="loading" :pagination="pagination"
      @change="handleTableChange" rowKey="id">
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'status'">
          <a-tag :color="record.status === 1 ? 'green' : 'red'">
            {{ record.status === 1 ? '启用' : '禁用' }}
          </a-tag>
        </template>
        <template v-if="column.key === 'is_default'">
          <a-tag :color="record.is_default ? 'blue' : 'default'">
            {{ record.is_default ? '是' : '否' }}
          </a-tag>
        </template>
        <template v-if="column.key === 'action'">
          <a-space>
            <a @click="showEditModal(record)">编辑</a>
            <a-divider type="vertical" />
            <a-popconfirm title="确定要删除该角色吗?" ok-text="确定" cancel-text="取消" @confirm="handleDelete(record.id)">
              <a class="danger-link">删除</a>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 添加/编辑角色弹窗 -->
    <a-modal v-model:visible="modalVisible" :title="modalTitle" @ok="handleModalOk" @cancel="handleModalCancel"
      width="700px">
      <a-form ref="roleFormRef" :model="roleForm" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
        <a-form-item label="角色名称" name="name">
          <a-input v-model:value="roleForm.name" placeholder="请输入角色名称" />
        </a-form-item>
        <a-form-item label="角色代码" name="code">
          <a-input v-model:value="roleForm.code" placeholder="请输入角色代码" />
        </a-form-item>
        <a-form-item label="描述" name="description">
          <a-textarea v-model:value="roleForm.description" placeholder="请输入角色描述" :rows="3" />
        </a-form-item>
        <a-form-item label="排序" name="sort_order">
          <a-input-number v-model:value="roleForm.sort_order" :min="0" style="width: 100%" />
        </a-form-item>
        <a-form-item label="数据范围" name="data_scope">
          <a-select v-model:value="roleForm.data_scope">
            <a-select-option :value="1">全部数据</a-select-option>
            <a-select-option :value="2">部门数据</a-select-option>
            <a-select-option :value="3">个人数据</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="菜单权限" name="menu_ids">
          <a-tree v-model:checkedKeys="roleForm.menu_ids" :tree-data="menuTree" checkable :check-strictly="false"
            :default-expand-all="true" />
        </a-form-item>
        <a-form-item label="状态" name="status">
          <a-radio-group v-model:value="roleForm.status">
            <a-radio :value="1">启用</a-radio>
            <a-radio :value="0">禁用</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item label="是否默认" name="is_default">
          <a-switch v-model:checked="roleForm.is_default" />
        </a-form-item>
        <a-form-item label="备注" name="remark">
          <a-textarea v-model:value="roleForm.remark" placeholder="请输入备注" :rows="2" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined, SearchOutlined, ReloadOutlined } from '@ant-design/icons-vue'
import { getRoles, createRole, updateRole, deleteRole, menuAPI } from '@/api/admin'

defineOptions({
  name: 'RoleManagement'
})

// 表格列定义
const columns = [
  {
    title: '角色名称',
    dataIndex: 'name',
    key: 'name'
  },
  {
    title: '角色代码',
    dataIndex: 'code',
    key: 'code'
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
    title: '数据范围',
    dataIndex: 'data_scope_name',
    key: 'data_scope_name',
    width: 100
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 80
  },
  {
    title: '默认角色',
    dataIndex: 'is_default',
    key: 'is_default',
    width: 90
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
    width: 120
  }
]

// 数据状态
const roles = ref([])
const loading = ref(false)
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showTotal: (total) => `共 ${total} 条数据`
})

// 搜索表单
const searchForm = reactive({
  keyword: '',
  page: 1,
  per_page: 10
})

// 角色表单
const roleForm = reactive({
  id: '',
  name: '',
  code: '',
  description: '',
  sort_order: 0,
  data_scope: 1,
  menu_ids: [],
  status: 1,
  is_default: false,
  remark: ''
})

// 表单校验规则
const rules = {
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { max: 50, message: '角色名称不能超过50个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入角色代码', trigger: 'blur' },
    { max: 50, message: '角色代码不能超过50个字符', trigger: 'blur' }
  ],
  sort_order: [
    { required: true, message: '请输入排序值', trigger: 'blur' }
  ]
}

// 弹窗控制
const modalVisible = ref(false)
const modalTitle = ref('添加角色')
const isEdit = ref(false)
const roleFormRef = ref(null)

// 菜单树
const menuTree = ref([])

// 获取角色列表
const fetchRoles = async () => {
  loading.value = true
  try {
    const res = await getRoles({
      keyword: searchForm.keyword,
      page: pagination.current,
      per_page: pagination.pageSize
    })
    roles.value = res.data.roles
    pagination.total = res.data.total
  } catch (error) {
    message.error('获取角色列表失败：' + error.message)
  } finally {
    loading.value = false
  }
}

// 获取菜单树
const fetchMenuTree = async () => {
  try {
    const res = await menuAPI.getMenuTree()
    if (res.code === 200) {
      menuTree.value = res.data
    }
  } catch (error) {
    message.error('获取菜单树失败：' + error.message)
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  fetchRoles()
}

// 重置搜索
const handleReset = () => {
  searchForm.keyword = ''
  pagination.current = 1
  fetchRoles()
}

// 表格变化
const handleTableChange = (pag) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchRoles()
}

// 显示添加弹窗
const showAddModal = () => {
  isEdit.value = false
  modalTitle.value = '添加角色'
  resetForm()
  modalVisible.value = true
}

// 显示编辑弹窗
const showEditModal = (record) => {
  isEdit.value = true
  modalTitle.value = '编辑角色'
  resetForm()

  // 填充表单数据
  Object.keys(roleForm).forEach(key => {
    if (key in record) {
      roleForm[key] = record[key]
    }
  })

  // 处理菜单ID
  if (record.menu_ids) {
    if (Array.isArray(record.menu_ids)) {
      roleForm.menu_ids = record.menu_ids
    } else if (typeof record.menu_ids === 'string') {
      roleForm.menu_ids = record.menu_ids.split(',').filter(id => id)
    }
  }

  modalVisible.value = true
}

// 重置表单
const resetForm = () => {
  roleForm.id = ''
  roleForm.name = ''
  roleForm.code = ''
  roleForm.description = ''
  roleForm.sort_order = 0
  roleForm.data_scope = 1
  roleForm.menu_ids = []
  roleForm.status = 1
  roleForm.is_default = false
  roleForm.remark = ''

  if (roleFormRef.value) {
    roleFormRef.value.resetFields()
  }
}

// 提交表单
const handleModalOk = () => {
  roleFormRef.value.validate().then(async () => {
    try {
      // 准备表单数据（保持菜单ID为数组格式）
      const formData = { ...roleForm }

      if (isEdit.value) {
        await updateRole(formData.id, formData)
        message.success('角色更新成功')
      } else {
        await createRole(formData)
        message.success('角色创建成功')
      }

      modalVisible.value = false
      fetchRoles()
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

// 删除角色
const handleDelete = async (id) => {
  try {
    await deleteRole(id)
    message.success('角色删除成功')
    fetchRoles()
  } catch (error) {
    message.error('删除失败：' + error.message)
  }
}

onMounted(() => {
  fetchRoles()
  fetchMenuTree()
})
</script>

<style scoped>
.role-management {
  padding: 0;
  background: #fff;
  border-radius: 4px;
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

.danger-link {
  color: #ff4d4f;
}

@media (max-width: 768px) {
  .role-management {
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