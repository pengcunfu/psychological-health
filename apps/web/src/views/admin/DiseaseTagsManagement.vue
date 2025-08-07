<template>
  <div class="disease-tags-management">
    <!-- 搜索栏和操作栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="标签名称">
          <a-input 
            v-model:value="searchForm.name" 
            placeholder="请输入标签名称" 
            style="width: 200px;"
            allow-clear 
          />
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
          添加标签
        </a-button>
      </div>
    </div>

    <!-- 数据表格 -->
    <a-table
      :columns="columns"
      :data-source="tags"
      :loading="loading"
      :pagination="pagination"
      @change="handleTableChange"
      row-key="id"
    >
      <template #description="{ record }">
        <div class="description-cell">
          <span class="description-text">{{ record.description || '-' }}</span>
        </div>
      </template>

      <template #createTime="{ record }">
        {{ formatDate(record.create_time) }}
      </template>

      <template #action="{ record }">
        <a-space>
          <a-button type="link" size="small" @click="showEditModal(record)">
            编辑
          </a-button>
          <a-popconfirm
            title="确定要删除该标签吗？"
            @confirm="handleDelete(record.id)"
          >
            <a-button type="link" size="small" danger>
              删除
            </a-button>
          </a-popconfirm>
        </a-space>
      </template>
    </a-table>

    <!-- 添加/编辑标签弹窗 -->
    <a-modal
      v-model:open="modalVisible"
      :title="modalTitle"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
      width="600px"
    >
      <a-form
        ref="tagFormRef"
        :model="tagForm"
        :rules="rules"
        layout="vertical"
      >
        <a-form-item label="标签名称" name="name">
          <a-input v-model:value="tagForm.name" placeholder="请输入标签名称" />
        </a-form-item>
        <a-form-item label="描述" name="description">
          <a-textarea 
            v-model:value="tagForm.description" 
            placeholder="请输入标签描述（可选）" 
            :rows="4" 
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { getDiseaseTags, createDiseaseTag, updateDiseaseTag, deleteDiseaseTag } from '@/api'

export default {
  name: 'DiseaseTagsManagement',
  components: {
    PlusOutlined
  },
  setup() {
    const loading = ref(false)
    const tags = ref([])
    const modalVisible = ref(false)
    const isEdit = ref(false)
    const tagFormRef = ref()

    const searchForm = reactive({
      name: ''
    })

    const tagForm = reactive({
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

    // 表格列定义
    const columns = [
      {
        title: '标签名称',
        dataIndex: 'name',
        key: 'name',
        width: 200
      },
      {
        title: '描述',
        dataIndex: 'description',
        key: 'description',
        slots: { customRender: 'description' },
        width: 300
      },
      {
        title: '创建时间',
        dataIndex: 'create_time',
        key: 'create_time',
        slots: { customRender: 'createTime' },
        width: 150
      },
      {
        title: '操作',
        key: 'action',
        slots: { customRender: 'action' },
        width: 150
      }
    ]

    // 表单校验规则
    const rules = {
      name: [
        { required: true, message: '请输入标签名称', trigger: 'blur' },
        { max: 50, message: '标签名称不能超过50个字符', trigger: 'blur' }
      ]
    }

    // 获取标签列表
    const fetchTags = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          name: searchForm.name
        }

        const result = await getDiseaseTags(params)
        if (result.code === 200) {
          tags.value = result.data.list || result.data.tags || []
          pagination.total = result.data.total
        }
      } catch (error) {
        message.error('获取标签列表失败')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current = 1
      fetchTags()
    }

    // 重置搜索
    const handleReset = () => {
      Object.assign(searchForm, {
        name: ''
      })
      pagination.current = 1
      fetchTags()
    }

    // 表格分页改变
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchTags()
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
      Object.assign(tagForm, {
        id: record.id,
        name: record.name,
        description: record.description
      })
    }

    // 重置表单
    const resetForm = () => {
      Object.assign(tagForm, {
        name: '',
        description: ''
      })
      tagFormRef.value?.resetFields()
    }

    // 模态框确定
    const handleModalOk = async () => {
      try {
        await tagFormRef.value.validate()

        const data = { ...tagForm }
        delete data.id

        if (isEdit.value) {
          const result = await updateDiseaseTag(tagForm.id, data)
          if (result.code === 200) {
            message.success('更新成功')
            modalVisible.value = false
            fetchTags()
          }
        } else {
          const result = await createDiseaseTag(data)
          if (result.code === 200 || result.code === 201) {
            message.success('创建成功')
            modalVisible.value = false
            fetchTags()
          }
        }
      } catch (error) {
        console.error('Form validation failed:', error)
      }
    }

    // 模态框取消
    const handleModalCancel = () => {
      modalVisible.value = false
      resetForm()
    }

    // 删除标签
    const handleDelete = async (id) => {
      try {
        const result = await deleteDiseaseTag(id)
        if (result.code === 200) {
          message.success('删除成功')
          fetchTags()
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

    const modalTitle = computed(() => isEdit.value ? '编辑标签' : '添加标签')

    onMounted(() => {
      fetchTags()
    })

    return {
      loading,
      tags,
      searchForm,
      tagForm,
      tagFormRef,
      rules,
      modalVisible,
      isEdit,
      pagination,
      columns,
      modalTitle,
      fetchTags,
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
.disease-tags-management {
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
  .disease-tags-management {
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

  .search-form .ant-input {
    font-size: 13px;
  }

     .description-cell {
     max-width: 150px;
   }
 }
 </style> 