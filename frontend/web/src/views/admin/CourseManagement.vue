<template>
  <div class="course-management">
    <!-- 搜索栏和添加按钮在同一行 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="课程标题">
          <a-input
              v-model:value="searchForm.title"
              placeholder="请输入课程标题"
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
            <a-select-option value="published">已发布</a-select-option>
            <a-select-option value="draft">草稿</a-select-option>
            <a-select-option value="archived">已归档</a-select-option>
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
        添加课程
      </a-button>
    </div>

    <!-- 课程列表 -->
    <a-table
        :columns="columns"
        :data-source="courses"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
    >
      <template #cover="{ record }">
        <a-image
            :src="FileUploader.getFullImageUrl(record?.cover_image)"
            :alt="record?.title || ''"
            width="60"
            height="40"
            style="object-fit: cover; border-radius: 4px;"
            :preview="false"
        />
      </template>

      <template #title="{ record }">
        <div class="course-title">
          <div class="title-text">{{ record?.title || '' }}</div>
          <div class="title-subtitle">{{ record?.subtitle || '' }}</div>
        </div>
      </template>

      <template #status="{ record }">
        <a-tag :color="getStatusColor(record?.status)">
          {{ getStatusText(record?.status) }}
        </a-tag>
      </template>

      <template #price="{ record }">
        <span class="price">
          <span v-if="record?.price > 0">¥{{ record?.price }}</span>
          <span v-else class="free">免费</span>
        </span>
      </template>

      <template #createTime="{ record }">
        {{ formatDate(record?.create_time) }}
      </template>

      <template #action="{ record }">
        <a-space>
          <a-button type="link" size="small" @click="editCourse(record)">
            编辑
          </a-button>
          <a-button type="link" size="small" @click="viewCourse(record)">
            查看
          </a-button>
          <a-dropdown>
            <a-button type="link" size="small">
              更多
              <DownOutlined/>
            </a-button>
            <template #overlay>
              <a-menu @click="({ key }) => handleMenuAction(record, key)">
                <a-menu-item v-if="record.status === 'draft'" key="publish">
                  发布课程
                </a-menu-item>
                <a-menu-item v-if="record.status === 'published'" key="archive">
                  归档课程
                </a-menu-item>
                <a-menu-item key="delete" class="danger-item">
                  删除课程
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </a-space>
      </template>
    </a-table>

    <!-- 添加/编辑课程弹窗 -->
    <a-modal
        v-model:open="modalVisible"
        :title="modalTitle"
        @ok="handleModalOk"
        @cancel="handleModalCancel"
        width="800px"
        :body-style="{ maxHeight: '70vh', overflowY: 'auto' }"
    >
      <a-form
          ref="courseFormRef"
          :model="courseForm"
          :rules="courseFormRules"
          layout="vertical"
      >
        <a-row :gutter="16">
          <a-col :span="16">
            <a-form-item label="课程标题" name="title">
              <a-input v-model:value="courseForm.title" placeholder="请输入课程标题"/>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="状态" name="status">
              <a-select v-model:value="courseForm.status" placeholder="请选择状态">
                <a-select-option value="draft">草稿</a-select-option>
                <a-select-option value="published">已发布</a-select-option>
                <a-select-option value="archived">已归档</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="课程副标题" name="subtitle">
          <a-input v-model:value="courseForm.subtitle" placeholder="请输入课程副标题"/>
        </a-form-item>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="课程价格" name="price">
              <a-input-number
                  v-model:value="courseForm.price"
                  placeholder="请输入课程价格"
                  :min="0"
                  :precision="2"
                  style="width: 100%;"
                  addon-before="¥"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="课程时长(分钟)" name="duration">
              <a-input-number
                  v-model:value="courseForm.duration"
                  placeholder="请输入课程时长"
                  :min="1"
                  style="width: 100%;"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="课程描述" name="description">
          <a-textarea
              v-model:value="courseForm.description"
              placeholder="请输入课程描述"
              :rows="4"
          />
        </a-form-item>

        <a-form-item label="课程内容" name="content">
          <a-textarea
              v-model:value="courseForm.content"
              placeholder="请输入详细的课程内容"
              :rows="6"
          />
        </a-form-item>

        <a-form-item label="课程封面" name="cover_image">
          <a-upload
              v-model:file-list="fileList"
              :before-upload="beforeUpload"
              :custom-request="uploadCover"
              :on-remove="handleRemove"
              list-type="picture-card"
              :max-count="1"
          >
            <div v-if="fileList.length < 1">
              <upload-outlined/>
              <div>上传封面</div>
            </div>
          </a-upload>
        </a-form-item>

        <a-form-item label="关键词标签">
          <a-select
              v-model:value="courseForm.tags"
              mode="tags"
              placeholder="请输入关键词标签"
              style="width: 100%;"
          >
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 查看课程详情弹窗 -->
    <a-modal
        v-model:open="viewModalVisible"
        title="课程详情"
        :footer="null"
        width="700px"
    >
      <div v-if="currentCourse" class="course-detail">
        <div class="detail-header">
          <a-image
              :src="FileUploader.getFullImageUrl(currentCourse.cover_image)"
              :alt="currentCourse.title"
              width="120"
              height="80"
              style="object-fit: cover; border-radius: 8px;"
          />
          <div class="header-info">
            <h3>{{ currentCourse.title }}</h3>
            <p class="subtitle">{{ currentCourse.subtitle }}</p>
            <div class="meta-info">
              <a-tag :color="getStatusColor(currentCourse.status)">
                {{ getStatusText(currentCourse.status) }}
              </a-tag>
              <span class="price">
                <span v-if="currentCourse.price > 0">¥{{ currentCourse.price }}</span>
                <span v-else class="free">免费</span>
              </span>
              <span class="duration">{{ currentCourse.duration }}分钟</span>
            </div>
          </div>
        </div>

        <a-divider/>

        <div class="detail-section">
          <h4>课程描述</h4>
          <p>{{ currentCourse.description || '暂无描述' }}</p>
        </div>

        <div class="detail-section">
          <h4>课程内容</h4>
          <div class="content-text">{{ currentCourse.content || '暂无详细内容' }}</div>
        </div>

        <div v-if="currentCourse.tags && currentCourse.tags.length" class="detail-section">
          <h4>标签</h4>
          <a-tag v-for="tag in currentCourse.tags" :key="tag" color="blue">
            {{ tag }}
          </a-tag>
        </div>

        <div class="detail-section">
          <h4>基本信息</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">创建时间：</span>
              <span>{{ formatDate(currentCourse.create_time) }}</span>
            </div>
            <div class="info-item">
              <span class="label">更新时间：</span>
              <span>{{ formatDate(currentCourse.update_time) }}</span>
            </div>
          </div>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script>
import {ref, reactive, onMounted, computed} from 'vue'
import {message} from 'ant-design-vue'
import {PlusOutlined, UploadOutlined, DownOutlined} from '@ant-design/icons-vue'
import {courseAPI} from '@/api'
import {uploadCourseCover, FileUploader} from '@/api/upload'

export default {
  name: 'CourseManagement',
  components: {
    PlusOutlined,
    UploadOutlined,
    DownOutlined
  },
  setup() {
    const loading = ref(false)
    const courses = ref([])
    const modalVisible = ref(false)
    const viewModalVisible = ref(false)
    const isEdit = ref(false)
    const currentCourse = ref(null)
    const courseFormRef = ref()
    const fileList = ref([])

    const searchForm = reactive({
      title: '',
      status: undefined
    })

    const courseForm = reactive({
      title: '',
      subtitle: '',
      description: '',
      content: '',
      price: 0,
      duration: 60,
      status: 'draft',
      cover_image: '',
      tags: []
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
        title: '封面',
        dataIndex: 'cover_image',
        key: 'cover_image',
        slots: {customRender: 'cover'},
        width: 80
      },
      {
        title: '课程信息',
        dataIndex: 'title',
        key: 'title',
        slots: {customRender: 'title'},
        width: 250
      },
      {
        title: '价格',
        dataIndex: 'price',
        key: 'price',
        slots: {customRender: 'price'},
        width: 100
      },
      {
        title: '时长',
        dataIndex: 'duration',
        key: 'duration',
        render: (text) => `${text || 0} 分钟`,
        width: 100
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        slots: {customRender: 'status'},
        width: 100
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
        width: 150
      }
    ]

    const courseFormRules = {
      title: [
        {required: true, message: '请输入课程标题', trigger: 'blur'}
      ],
      status: [
        {required: true, message: '请选择状态', trigger: 'change'}
      ],
      price: [
        {required: true, message: '请输入课程价格', trigger: 'blur'}
      ]
    }

    // 获取课程列表
    const fetchCourses = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          title: searchForm.title,
          status: searchForm.status
        }

        const result = await courseAPI.getCourses(params)
        if (result.code === 200) {
          courses.value = result.data.list
          pagination.total = result.data.total
        }
      } catch (error) {
        message.error('获取课程列表失败')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current = 1
      fetchCourses()
    }

    // 重置搜索
    const resetSearch = () => {
      Object.assign(searchForm, {
        title: '',
        status: undefined
      })
      pagination.current = 1
      fetchCourses()
    }

    // 表格分页改变
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchCourses()
    }

    // 显示添加模态框
    const showAddModal = () => {
      isEdit.value = false
      modalVisible.value = true
      resetCourseForm()
    }

    // 编辑课程
    const editCourse = (course) => {
      isEdit.value = true
      modalVisible.value = true
      Object.assign(courseForm, {
        id: course.id,
        title: course.title,
        subtitle: course.subtitle,
        description: course.description,
        content: course.content,
        price: course.price,
        duration: course.duration,
        status: course.status,
        cover_image: course.cover_image,
        tags: course.tags || []
      })
      if (course.cover_image) {
        // 获取完整的图片URL用于预览
        const imageUrl = FileUploader.getFullImageUrl(course.cover_image)
        fileList.value = [{
          uid: '-1',
          name: 'cover.png',
          status: 'done',
          url: imageUrl
        }]
      }
    }

    // 查看课程
    const viewCourse = (course) => {
      currentCourse.value = course
      viewModalVisible.value = true
    }

    // 菜单操作
    const handleMenuAction = async (course, action) => {
      if (action === 'delete') {
        try {
          const result = await courseAPI.deleteCourse(course.id)
          if (result.code === 200) {
            message.success('删除成功')
            fetchCourses()
          }
        } catch (error) {
          message.error('删除失败')
        }
      } else if (action === 'publish') {
        await updateCourseStatus(course.id, 'published')
      } else if (action === 'archive') {
        await updateCourseStatus(course.id, 'archived')
      }
    }

    // 更新课程状态
    const updateCourseStatus = async (courseId, status) => {
      try {
        const result = await courseAPI.updateCourse(courseId, {status})
        if (result.code === 200) {
          message.success('状态更新成功')
          fetchCourses()
        }
      } catch (error) {
        message.error('状态更新失败')
      }
    }

    // 模态框确定
    const handleModalOk = async () => {
      try {
        await courseFormRef.value.validate()

        const data = {...courseForm}
        delete data.id

        if (isEdit.value) {
          const result = await courseAPI.updateCourse(courseForm.id, data)
          if (result.code === 200) {
            message.success('更新成功')
            modalVisible.value = false
            fetchCourses()
          }
        } else {
          const result = await courseAPI.createCourse(data)
          if (result.code === 200 || result.code === 201) {
            message.success('创建成功')
            modalVisible.value = false
            fetchCourses()
          }
        }
      } catch (error) {
        console.error('Form validation failed:', error)
      }
    }

    // 模态框取消
    const handleModalCancel = () => {
      modalVisible.value = false
      resetCourseForm()
    }

    // 重置课程表单
    const resetCourseForm = () => {
      Object.assign(courseForm, {
        title: '',
        subtitle: '',
        description: '',
        content: '',
        price: 0,
        duration: 60,
        status: 'draft',
        cover_image: '',
        tags: []
      })
      fileList.value = []
      courseFormRef.value?.resetFields()
    }

    // 上传前验证
    const beforeUpload = (file) => {
      try {
        FileUploader.validateImage(file, 2) // 验证图片，最大2MB
        return true
      } catch (error) {
        message.error(error.message)
        return false
      }
    }

    // 移除封面
    const handleRemove = (file) => {
      courseForm.cover_image = ''
      fileList.value = []
      return true
    }

    // 上传封面
    const uploadCover = async ({file, onSuccess, onError, onProgress}) => {
      try {
        // 显示上传中状态
        fileList.value = [{
          uid: file.uid,
          name: file.name,
          status: 'uploading',
          percent: 0
        }]
        
        // 调用上传接口
        const result = await uploadCourseCover(file)
        
        if (result.success && result.code === 200) {
          // 上传成功，获取完整的图片URL
          const imageUrl = FileUploader.getFullImageUrl(result.data.url)
          
          // 更新表单数据
          courseForm.cover_image = result.data.url // 保存相对路径到数据库
          
          // 更新文件列表状态
          fileList.value = [{
            uid: file.uid,
            name: file.name,
            status: 'done',
            url: imageUrl, // 显示完整URL用于预览
            response: result
          }]
          
          // 调用成功回调
          onSuccess && onSuccess(result, file)
          message.success('封面上传成功!')
        } else {
          throw new Error(result.message || '上传失败')
        }
      } catch (error) {
        console.error('上传封面失败:', error)
        
        // 更新文件列表状态为失败
        fileList.value = [{
          uid: file.uid,
          name: file.name,
          status: 'error'
        }]
        
        // 调用失败回调
        onError && onError(error)
        message.error(error.message || '上传封面失败!')
      }
    }

    // 获取状态颜色
    const getStatusColor = (status) => {
      if (!status) return 'default'
      const colorMap = {
        published: 'green',
        draft: 'orange',
        archived: 'red'
      }
      return colorMap[status] || 'default'
    }

    // 获取状态文本
    const getStatusText = (status) => {
      if (!status) return '未知'
      const textMap = {
        published: '已发布',
        draft: '草稿',
        archived: '已归档'
      }
      return textMap[status] || '未知'
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }

    const modalTitle = computed(() => isEdit.value ? '编辑课程' : '添加课程')

    onMounted(() => {
      fetchCourses()
    })

    return {
      loading,
      courses,
      searchForm,
      courseForm,
      courseFormRef,
      courseFormRules,
      modalVisible,
      viewModalVisible,
      isEdit,
      currentCourse,
      pagination,
      columns,
      fileList,
      modalTitle,
      fetchCourses,
      handleSearch,
      resetSearch,
      handleTableChange,
      showAddModal,
      editCourse,
      viewCourse,
      handleMenuAction,
      handleModalOk,
      handleModalCancel,
      beforeUpload,
      uploadCover,
      handleRemove,
      getStatusColor,
      getStatusText,
      formatDate,
      FileUploader
    }
  }
}
</script>

<style scoped>
.course-management {
  padding: 0px;
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

.course-title .title-text {
  font-weight: 500;
  margin-bottom: 4px;
}

.course-title .title-subtitle {
  font-size: 12px;
  color: #999;
}

.price .free {
  color: #52c41a;
  font-weight: 500;
}

.price {
  font-weight: 600;
  color: #f5222d;
}

.course-detail {
  padding: 12px 0;
}

.detail-header {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.header-info h3 {
  margin: 0 0 6px 0;
  color: #1890ff;
}

.header-info .subtitle {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-section {
  margin-bottom: 16px;
}

.detail-section h4 {
  margin: 0 0 6px 0;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.content-text {
  line-height: 1.6;
  white-space: pre-wrap;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.info-item {
  display: flex;
  align-items: center;
}

.info-item .label {
  font-weight: 500;
  color: #666;
  margin-right: 8px;
}

.danger-item {
  color: #ff4d4f !important;
}

@media (max-width: 768px) {
  .course-management {
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

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style> 