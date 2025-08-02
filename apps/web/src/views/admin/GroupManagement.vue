<template>
  <div class="group-management">
    <div class="page-header">
      <h2>群组管理</h2>
      <a-button type="primary" @click="showAddModal">
        <template #icon>
          <PlusOutlined/>
        </template>
        添加群组
      </a-button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch">
        <a-form-item label="群组名称">
          <a-input
              v-model:value="searchForm.name"
              placeholder="请输入群组名称"
              style="width: 200px;"
          />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
          <a-button style="margin-left: 8px;" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>
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
      <template #description="{ record }">
        <div class="description-cell">
          <a-tooltip :title="record?.description || '-'">
            <div class="ellipsis">{{ record?.description || '-' }}</div>
          </a-tooltip>
        </div>
      </template>

      <template #createTime="{ record }">
        {{ formatDate(record?.create_time) }}
      </template>

      <template #action="{ record }">
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
        <a-form-item label="群组名称" name="name">
          <a-input v-model:value="groupForm.name" placeholder="请输入群组名称"/>
        </a-form-item>

        <a-form-item label="群组描述" name="description">
          <a-textarea
              v-model:value="groupForm.description"
              placeholder="请输入群组描述"
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
          <h3>{{ currentGroup?.name || '' }}</h3>
        </div>

        <a-divider/>

        <div class="detail-section">
          <a-descriptions bordered :column="1">
            <a-descriptions-item label="群组名称">{{ currentGroup?.name || '-' }}</a-descriptions-item>
            <a-descriptions-item label="群组描述">{{ currentGroup?.description || '-' }}</a-descriptions-item>
            <a-descriptions-item label="创建时间">{{ formatDate(currentGroup?.create_time) }}</a-descriptions-item>
            <a-descriptions-item label="更新时间">{{ formatDate(currentGroup?.update_time) }}</a-descriptions-item>
          </a-descriptions>
        </div>

        <!-- 这里可以添加群组成员列表等更多信息 -->
      </div>
    </a-modal>
  </div>
</template>

<script>
import {ref, reactive, onMounted, computed} from 'vue'
import {message} from 'ant-design-vue'
import {PlusOutlined} from '@ant-design/icons-vue'
import {groupAPI} from '@/api/admin'

export default {
  name: 'GroupManagement',
  components: {
    PlusOutlined
  },
  setup() {
    const loading = ref(false)
    const groups = ref([])
    const modalVisible = ref(false)
    const viewModalVisible = ref(false)
    const isEdit = ref(false)
    const currentGroup = ref(null)
    const groupFormRef = ref()

    const searchForm = reactive({
      name: ''
    })

    const groupForm = reactive({
      name: '',
      description: ''
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
        title: '群组名称',
        dataIndex: 'name',
        key: 'name',
        width: 200
      },
      {
        title: '描述',
        dataIndex: 'description',
        key: 'description',
        slots: {customRender: 'description'},
        width: 300
      },
      {
        title: '创建时间',
        dataIndex: 'create_time',
        key: 'create_time',
        slots: {customRender: 'createTime'},
        width: 150
      },
      {
        title: '操作',
        key: 'action',
        slots: {customRender: 'action'},
        width: 150,
        fixed: 'right'
      }
    ]

    const groupFormRules = {
      name: [
        {required: true, message: '请输入群组名称', trigger: 'blur'}
      ]
    }

    // 获取群组列表
    const fetchGroups = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          name: searchForm.name
        }

        const result = await groupAPI.getGroups(params)
        if (result.code === 200) {
          groups.value = result.data.groups || []
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
      searchForm.name = ''
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
        name: group.name,
        description: group.description
      })
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

        if (isEdit.value) {
          // 编辑群组
          const result = await groupAPI.updateGroup(groupForm.id, groupForm)
          if (result.code === 200) {
            message.success('更新成功')
            modalVisible.value = false
            fetchGroups()
          } else {
            message.error(result.message || '更新失败')
          }
        } else {
          // 创建群组
          const result = await groupAPI.createGroup(groupForm)
          if (result.code === 200) {
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
        name: '',
        description: ''
      })
      groupFormRef.value?.resetFields()
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }

    const modalTitle = computed(() => isEdit.value ? '编辑群组' : '添加群组')

    onMounted(() => {
      fetchGroups()
    })

    return {
      loading,
      groups,
      searchForm,
      groupForm,
      groupFormRef,
      groupFormRules,
      modalVisible,
      viewModalVisible,
      isEdit,
      currentGroup,
      pagination,
      columns,
      modalTitle,
      fetchGroups,
      handleSearch,
      resetSearch,
      handleTableChange,
      showAddModal,
      editGroup,
      viewGroup,
      deleteGroup,
      handleModalOk,
      handleModalCancel,
      formatDate
    }
  }
}
</script>

<style scoped>
.group-management {
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
  color: #1890ff;
}

.search-bar {
  background: white;
  padding: 16px;
  border-radius: 6px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.group-detail {
  padding: 16px 0;
}

.detail-header {
  margin-bottom: 20px;
}

.detail-header h3 {
  margin: 0;
  color: #1890ff;
}

.detail-section {
  margin-bottom: 20px;
}

.description-cell {
  max-width: 300px;
}

.ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 768px) {
  .group-management {
    padding: 12px;
  }

  .page-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .search-bar .ant-form {
    flex-direction: column;
  }

  .search-bar .ant-form-item {
    margin-bottom: 8px;
  }
}
</style> 