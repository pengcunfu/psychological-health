<template>
  <div class="category-management">
    <!-- 搜索栏和操作栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="分类名称">
          <a-input
              v-model:value="searchForm.name"
              placeholder="请输入分类名称"
              style="width: 200px;"
          />
        </a-form-item>
        <a-form-item label="类型">
          <a-select
              v-model:value="searchForm.type"
              placeholder="请选择类型"
              style="width: 150px;"
              allow-clear
          >
            <a-select-option value="course">课程分类</a-select-option>
            <a-select-option value="counselor">咨询师分类</a-select-option>
            <a-select-option value="article">文章分类</a-select-option>
          </a-select>
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
          添加分类
        </a-button>
      </div>
    </div>

    <!-- 分类列表 -->
    <a-table
        :columns="columns"
        :data-source="categories"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
    >
      <template #icon="{ record }">
        <div class="category-icon">
          <span v-if="record.icon" class="icon-preview">
            <component :is="record.icon"/>
          </span>
          <span v-else class="no-icon">-</span>
        </div>
      </template>

      <template #type="{ record }">
        <a-tag :color="getTypeColor(record.type)">
          {{ getTypeText(record.type) }}
        </a-tag>
      </template>

      <template #status="{ record }">
        <a-tag :color="record.status === 1 ? 'green' : 'default'">
          {{ record.status === 1 ? '启用' : '禁用' }}
        </a-tag>
      </template>

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
          <a-button type="link" size="small" @click="editCategory(record)">
            编辑
          </a-button>
          <a-button
              type="link"
              size="small"
              @click="toggleStatus(record)"
              :style="{ color: record.status === 1 ? '#ff4d4f' : '#52c41a' }"
          >
            {{ record.status === 1 ? '禁用' : '启用' }}
          </a-button>
          <a-popconfirm
              title="确定要删除该分类吗？"
              @confirm="deleteCategory(record.id)"
          >
            <a-button type="link" size="small" danger>
              删除
            </a-button>
          </a-popconfirm>
        </a-space>
      </template>
    </a-table>

    <!-- 添加/编辑分类弹窗 -->
    <a-modal
        v-model:open="modalVisible"
        :title="modalTitle"
        @ok="handleModalOk"
        @cancel="handleModalCancel"
        width="600px"
    >
      <a-form
          ref="categoryFormRef"
          :model="categoryForm"
          :rules="categoryFormRules"
          layout="vertical"
      >
        <a-form-item label="分类名称" name="name">
          <a-input v-model:value="categoryForm.name" placeholder="请输入分类名称"/>
        </a-form-item>

        <a-form-item label="分类类型" name="type">
          <a-select v-model:value="categoryForm.type" placeholder="请选择分类类型">
            <a-select-option value="course">课程分类</a-select-option>
            <a-select-option value="counselor">咨询师分类</a-select-option>
            <a-select-option value="article">文章分类</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="图标" name="icon">
          <a-input v-model:value="categoryForm.icon" placeholder="请输入图标名称（可选）"/>
        </a-form-item>

        <a-form-item label="排序" name="sort">
          <a-input-number
              v-model:value="categoryForm.sort"
              placeholder="请输入排序值（数字越小越靠前）"
              :min="0"
              style="width: 100%;"
          />
        </a-form-item>

        <a-form-item label="状态" name="status">
          <a-radio-group v-model:value="categoryForm.status">
            <a-radio :value="1">启用</a-radio>
            <a-radio :value="0">禁用</a-radio>
          </a-radio-group>
        </a-form-item>

        <a-form-item label="描述" name="description">
          <a-textarea
              v-model:value="categoryForm.description"
              placeholder="请输入分类描述（可选）"
              :rows="3"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
import {ref, reactive, onMounted, computed} from 'vue'
import {message} from 'ant-design-vue'
import {PlusOutlined} from '@ant-design/icons-vue'
import {categoryAPI} from '@/api/admin'

export default {
  name: 'CategoryManagement',
  components: {
    PlusOutlined
  },
  setup() {
    const loading = ref(false)
    const categories = ref([])
    const modalVisible = ref(false)
    const isEdit = ref(false)
    const categoryFormRef = ref()

    const searchForm = reactive({
      name: '',
      type: undefined
    })

    const categoryForm = reactive({
      name: '',
      type: 'course',
      icon: '',
      sort: 0,
      status: 1,
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
        title: '分类名称',
        dataIndex: 'name',
        key: 'name',
        width: 150
      },
      {
        title: '图标',
        dataIndex: 'icon',
        key: 'icon',
        slots: {customRender: 'icon'},
        width: 80
      },
      {
        title: '类型',
        dataIndex: 'type',
        key: 'type',
        slots: {customRender: 'type'},
        width: 120
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
        slots: {customRender: 'status'},
        width: 100
      },
      {
        title: '描述',
        dataIndex: 'description',
        key: 'description',
        slots: {customRender: 'description'},
        width: 200
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
        width: 180
      }
    ]

    const categoryFormRules = {
      name: [
        {required: true, message: '请输入分类名称', trigger: 'blur'}
      ],
      type: [
        {required: true, message: '请选择分类类型', trigger: 'change'}
      ],
      sort: [
        {required: true, message: '请输入排序值', trigger: 'blur'}
      ],
      status: [
        {required: true, message: '请选择状态', trigger: 'change'}
      ]
    }

    // 获取分类列表
    const fetchCategories = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          name: searchForm.name,
          type: searchForm.type
        }

        const result = await categoryAPI.getCategories(params)
        if (result.code === 200) {
          categories.value = result.data.list
          pagination.total = result.data.total
        }
      } catch (error) {
        message.error('获取分类列表失败')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current = 1
      fetchCategories()
    }

    // 重置搜索
    const resetSearch = () => {
      Object.assign(searchForm, {
        name: '',
        type: undefined
      })
      pagination.current = 1
      fetchCategories()
    }

    // 表格分页改变
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchCategories()
    }

    // 显示添加模态框
    const showAddModal = () => {
      isEdit.value = false
      modalVisible.value = true
      resetCategoryForm()
    }

    // 编辑分类
    const editCategory = (category) => {
      isEdit.value = true
      modalVisible.value = true
      Object.assign(categoryForm, {
        id: category.id,
        name: category.name,
        type: category.type,
        icon: category.icon,
        sort: category.sort_order || category.sort,
        status: category.status,
        description: category.description
      })
    }

    // 切换状态
    const toggleStatus = async (category) => {
      const newStatus = category.status === 1 ? 0 : 1
      try {
        const result = await categoryAPI.updateCategory(category.id, {status: newStatus})
        if (result.code === 200) {
          message.success(`${newStatus === 1 ? '启用' : '禁用'}成功`)
          fetchCategories()
        }
      } catch (error) {
        message.error('操作失败')
      }
    }

    // 删除分类
    const deleteCategory = async (categoryId) => {
      try {
        const result = await categoryAPI.deleteCategory(categoryId)
        if (result.code === 200) {
          message.success('删除成功')
          fetchCategories()
        }
      } catch (error) {
        message.error('删除失败')
      }
    }

    // 模态框确定
    const handleModalOk = async () => {
      try {
        await categoryFormRef.value.validate()

        const data = {...categoryForm}
        delete data.id
        
        // 将前端字段名映射为后端字段名
        if (data.sort !== undefined) {
          data.sort_order = data.sort
          delete data.sort
        }

        if (isEdit.value) {
          const result = await categoryAPI.updateCategory(categoryForm.id, data)
          if (result.code === 200) {
            message.success('更新成功')
            modalVisible.value = false
            fetchCategories()
          }
        } else {
          const result = await categoryAPI.createCategory(data)
          if (result.code === 200 || result.code === 201) {
            message.success('创建成功')
            modalVisible.value = false
            fetchCategories()
          }
        }
      } catch (error) {
        console.error('Form validation failed:', error)
      }
    }

    // 模态框取消
    const handleModalCancel = () => {
      modalVisible.value = false
      resetCategoryForm()
    }

    // 重置分类表单
    const resetCategoryForm = () => {
      Object.assign(categoryForm, {
        name: '',
        type: 'course',
        icon: '',
        sort: 0,
        status: 1,
        description: ''
      })
      categoryFormRef.value?.resetFields()
    }

    // 获取类型颜色
    const getTypeColor = (type) => {
      const colorMap = {
        course: 'blue',
        counselor: 'green',
        article: 'purple'
      }
      return colorMap[type] || 'default'
    }

    // 获取类型文本
    const getTypeText = (type) => {
      const textMap = {
        course: '课程分类',
        counselor: '咨询师分类',
        article: '文章分类'
      }
      return textMap[type] || '未知'
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }

    const modalTitle = computed(() => isEdit.value ? '编辑分类' : '添加分类')

    onMounted(() => {
      fetchCategories()
    })

    return {
      loading,
      categories,
      searchForm,
      categoryForm,
      categoryFormRef,
      categoryFormRules,
      modalVisible,
      isEdit,
      pagination,
      columns,
      modalTitle,
      fetchCategories,
      handleSearch,
      resetSearch,
      handleTableChange,
      showAddModal,
      editCategory,
      toggleStatus,
      deleteCategory,
      handleModalOk,
      handleModalCancel,
      getTypeColor,
      getTypeText,
      formatDate
    }
  }
}
</script>

<style scoped>
.category-management {
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

.category-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-preview {
  font-size: 18px;
  color: #1890ff;
}

.no-icon {
  color: #ccc;
  font-style: italic;
}

.description-cell {
  max-width: 180px;
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
  .category-management {
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
    max-width: 120px;
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
    max-width: 100px;
  }
}
</style> 