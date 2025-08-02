<template>
  <div class="course-outline-management">
    <div class="page-header">
      <h2>课程大纲管理</h2>
      <a-button type="primary" @click="showAddModal">
        <plus-outlined /> 添加课程大纲
      </a-button>
    </div>

    <!-- 搜索区域 -->
    <div class="search-container">
      <a-form layout="inline">
        <a-form-item label="课程">
          <a-select
            v-model:value="searchForm.course_id"
            style="width: 200px"
            placeholder="请选择课程"
            allowClear
            :options="courseOptions"
          />
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
      :data-source="outlines"
      :loading="loading"
      :pagination="false"
      rowKey="id"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'content'">
          <div class="content-preview">{{ record.content }}</div>
        </template>
        <template v-if="column.key === 'action'">
          <a-space>
            <a @click="showEditModal(record)">编辑</a>
            <a-divider type="vertical" />
            <a-popconfirm
              title="确定要删除该课程大纲吗?"
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

    <!-- 添加/编辑课程大纲弹窗 -->
    <a-modal
      v-model:visible="modalVisible"
      :title="modalTitle"
      width="700px"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
    >
      <a-form
        ref="outlineForm"
        :model="outlineForm"
        :rules="rules"
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 20 }"
      >
        <a-form-item label="课程" name="course_id">
          <a-select
            v-model:value="outlineForm.course_id"
            placeholder="请选择课程"
            :options="courseOptions"
          />
        </a-form-item>
        <a-form-item label="标题" name="title">
          <a-input v-model:value="outlineForm.title" placeholder="请输入大纲标题" />
        </a-form-item>
        <a-form-item label="内容" name="content">
          <a-textarea v-model:value="outlineForm.content" placeholder="请输入大纲内容" :rows="6" />
        </a-form-item>
        <a-form-item label="排序" name="sort_order">
          <a-input-number v-model:value="outlineForm.sort_order" :min="0" style="width: 100%" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted, watch } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined, SearchOutlined, ReloadOutlined } from '@ant-design/icons-vue'
import { getCourseOutlines, createCourseOutline, updateCourseOutline, deleteCourseOutline, getCourses } from '@/api/admin'

export default defineComponent({
  name: 'CourseOutlineManagement',
  components: {
    PlusOutlined,
    SearchOutlined,
    ReloadOutlined
  },
  setup() {
    // 表格列定义
    const columns = [
      {
        title: '标题',
        dataIndex: 'title',
        key: 'title',
        width: '25%'
      },
      {
        title: '内容',
        dataIndex: 'content',
        key: 'content',
        ellipsis: true
      },
      {
        title: '排序',
        dataIndex: 'sort_order',
        key: 'sort_order',
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
    const outlines = ref([])
    const loading = ref(false)
    const courseOptions = ref([])

    // 搜索表单
    const searchForm = reactive({
      course_id: undefined
    })

    // 大纲表单
    const outlineForm = reactive({
      id: '',
      course_id: undefined,
      title: '',
      content: '',
      sort_order: 0
    })

    // 表单校验规则
    const rules = {
      course_id: [
        { required: true, message: '请选择课程', trigger: 'change' }
      ],
      title: [
        { required: true, message: '请输入标题', trigger: 'blur' },
        { max: 100, message: '标题不能超过100个字符', trigger: 'blur' }
      ],
      content: [
        { required: true, message: '请输入内容', trigger: 'blur' }
      ],
      sort_order: [
        { required: true, message: '请输入排序值', trigger: 'blur' }
      ]
    }

    // 弹窗控制
    const modalVisible = ref(false)
    const modalTitle = ref('添加课程大纲')
    const isEdit = ref(false)
    const outlineFormRef = ref(null)

    // 获取课程列表
    const fetchCourses = async () => {
      try {
        const res = await getCourses({ page: 1, per_page: 1000 })
        courseOptions.value = res.data.courses.map(course => ({
          value: course.id,
          label: course.title
        }))
      } catch (error) {
        message.error('获取课程列表失败：' + error.message)
      }
    }

    // 获取课程大纲列表
    const fetchOutlines = async () => {
      if (!searchForm.course_id) {
        outlines.value = []
        return
      }
      
      loading.value = true
      try {
        const res = await getCourseOutlines({
          course_id: searchForm.course_id
        })
        outlines.value = res.data
      } catch (error) {
        message.error('获取课程大纲列表失败：' + error.message)
      } finally {
        loading.value = false
      }
    }

    // 监听课程选择变化
    watch(() => searchForm.course_id, (newVal) => {
      if (newVal) {
        fetchOutlines()
      } else {
        outlines.value = []
      }
    })

    // 搜索
    const handleSearch = () => {
      fetchOutlines()
    }

    // 重置搜索
    const handleReset = () => {
      searchForm.course_id = undefined
      outlines.value = []
    }

    // 显示添加弹窗
    const showAddModal = () => {
      isEdit.value = false
      modalTitle.value = '添加课程大纲'
      resetForm()
      outlineForm.course_id = searchForm.course_id
      modalVisible.value = true
    }

    // 显示编辑弹窗
    const showEditModal = (record) => {
      isEdit.value = true
      modalTitle.value = '编辑课程大纲'
      resetForm()
      
      // 填充表单数据
      outlineForm.id = record.id
      outlineForm.course_id = record.course_id
      outlineForm.title = record.title
      outlineForm.content = record.content
      outlineForm.sort_order = record.sort_order
      
      modalVisible.value = true
    }

    // 重置表单
    const resetForm = () => {
      outlineForm.id = ''
      outlineForm.course_id = undefined
      outlineForm.title = ''
      outlineForm.content = ''
      outlineForm.sort_order = 0
      
      if (outlineFormRef.value) {
        outlineFormRef.value.resetFields()
      }
    }

    // 提交表单
    const handleModalOk = () => {
      outlineFormRef.value.validate().then(async () => {
        try {
          if (isEdit.value) {
            await updateCourseOutline(outlineForm.id, outlineForm)
            message.success('课程大纲更新成功')
          } else {
            await createCourseOutline(outlineForm)
            message.success('课程大纲创建成功')
          }
          
          modalVisible.value = false
          fetchOutlines()
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

    // 删除课程大纲
    const handleDelete = async (id) => {
      try {
        await deleteCourseOutline(id)
        message.success('课程大纲删除成功')
        fetchOutlines()
      } catch (error) {
        message.error('删除失败：' + error.message)
      }
    }

    onMounted(() => {
      fetchCourses()
    })

    return {
      columns,
      outlines,
      loading,
      courseOptions,
      searchForm,
      outlineForm,
      rules,
      modalVisible,
      modalTitle,
      outlineFormRef,
      handleSearch,
      handleReset,
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
.course-outline-management {
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

.content-preview {
  max-height: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.danger-link {
  color: #ff4d4f;
}
</style> 