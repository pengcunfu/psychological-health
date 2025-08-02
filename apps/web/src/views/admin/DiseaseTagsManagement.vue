<template>
  <div class="disease-tags-management">
    <div class="page-header">
      <h2>疾病标签管理</h2>
      <a-button type="primary" @click="showAddModal">
        <plus-outlined /> 添加标签
      </a-button>
    </div>

    <!-- 搜索区域 -->
    <div class="search-container">
      <a-form layout="inline">
        <a-form-item label="标签名称">
          <a-input v-model:value="searchForm.name" placeholder="请输入标签名称" allowClear />
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
      :data-source="tags"
      :loading="loading"
      :pagination="pagination"
      @change="handleTableChange"
      rowKey="id"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'action'">
          <a-space>
            <a @click="showEditModal(record)">编辑</a>
            <a-divider type="vertical" />
            <a-popconfirm
              title="确定要删除该标签吗?"
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

    <!-- 添加/编辑标签弹窗 -->
    <a-modal
      v-model:visible="modalVisible"
      :title="modalTitle"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
    >
      <a-form
        ref="tagForm"
        :model="tagForm"
        :rules="rules"
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 20 }"
      >
        <a-form-item label="标签名称" name="name">
          <a-input v-model:value="tagForm.name" placeholder="请输入标签名称" />
        </a-form-item>
        <a-form-item label="描述" name="description">
          <a-textarea v-model:value="tagForm.description" placeholder="请输入标签描述" :rows="4" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined, SearchOutlined, ReloadOutlined } from '@ant-design/icons-vue'
import { getDiseaseTags, createDiseaseTag, updateDiseaseTag, deleteDiseaseTag } from '@/api/admin'

export default defineComponent({
  name: 'DiseaseTagsManagement',
  components: {
    PlusOutlined,
    SearchOutlined,
    ReloadOutlined
  },
  setup() {
    // 表格列定义
    const columns = [
      {
        title: '标签名称',
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
    const tags = ref([])
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
      page: 1,
      per_page: 10
    })

    // 标签表单
    const tagForm = reactive({
      id: '',
      name: '',
      description: ''
    })

    // 表单校验规则
    const rules = {
      name: [
        { required: true, message: '请输入标签名称', trigger: 'blur' },
        { max: 50, message: '标签名称不能超过50个字符', trigger: 'blur' }
      ]
    }

    // 弹窗控制
    const modalVisible = ref(false)
    const modalTitle = ref('添加标签')
    const isEdit = ref(false)
    const tagFormRef = ref(null)

    // 获取标签列表
    const fetchTags = async () => {
      loading.value = true
      try {
        const res = await getDiseaseTags({
          name: searchForm.name,
          page: pagination.current,
          per_page: pagination.pageSize
        })
        tags.value = res.data.tags
        pagination.total = res.data.total
      } catch (error) {
        message.error('获取标签列表失败：' + error.message)
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
      searchForm.name = ''
      pagination.current = 1
      fetchTags()
    }

    // 表格变化
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchTags()
    }

    // 显示添加弹窗
    const showAddModal = () => {
      isEdit.value = false
      modalTitle.value = '添加标签'
      resetForm()
      modalVisible.value = true
    }

    // 显示编辑弹窗
    const showEditModal = (record) => {
      isEdit.value = true
      modalTitle.value = '编辑标签'
      resetForm()
      
      // 填充表单数据
      tagForm.id = record.id
      tagForm.name = record.name
      tagForm.description = record.description
      
      modalVisible.value = true
    }

    // 重置表单
    const resetForm = () => {
      tagForm.id = ''
      tagForm.name = ''
      tagForm.description = ''
      
      if (tagFormRef.value) {
        tagFormRef.value.resetFields()
      }
    }

    // 提交表单
    const handleModalOk = () => {
      tagFormRef.value.validate().then(async () => {
        try {
          if (isEdit.value) {
            await updateDiseaseTag(tagForm.id, tagForm)
            message.success('标签更新成功')
          } else {
            await createDiseaseTag(tagForm)
            message.success('标签创建成功')
          }
          
          modalVisible.value = false
          fetchTags()
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

    // 删除标签
    const handleDelete = async (id) => {
      try {
        await deleteDiseaseTag(id)
        message.success('标签删除成功')
        fetchTags()
      } catch (error) {
        message.error('删除失败：' + error.message)
      }
    }

    onMounted(() => {
      fetchTags()
    })

    return {
      columns,
      tags,
      loading,
      pagination,
      searchForm,
      tagForm,
      rules,
      modalVisible,
      modalTitle,
      tagFormRef,
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
.disease-tags-management {
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