<template>
  <div class="course-outline-management">
    <!-- 搜索栏和添加按钮在同一行 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" class="search-form">
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
      
      <a-button type="primary" @click="showAddModal">
        <plus-outlined /> 添加课程大纲
      </a-button>
    </div>

    <!-- 当前课程提示 -->
    <div v-if="selectedCourseName" class="current-course-info">
      <span class="course-label">当前课程：</span>
      <span class="course-name">{{ selectedCourseName }}</span>
      <span class="outline-count">（{{ outlines.length }} 个大纲）</span>
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
        <template v-if="column.key === 'video_url'">
          <div class="video-preview">
            <a-space v-if="record.video_url" direction="vertical" size="small">
              <a :href="getFullVideoUrl(record.video_url)" target="_blank" class="video-link">
                <video-camera-outlined /> 查看视频
              </a>
              <span class="video-filename">{{ record.video_filename || record.video_url.split('/').pop() }}</span>
            </a-space>
            <span v-else class="no-video">暂无视频</span>
          </div>
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
        ref="outlineFormRef"
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
        <a-form-item label="视频">
          <div>
            <a-upload
              :file-list="videoFileList"
              :before-upload="beforeVideoUpload"
              :custom-request="handleVideoUpload"
              :show-upload-list="false"
              accept="video/*"
            >
              <a-button>
                <upload-outlined /> 选择视频文件
              </a-button>
            </a-upload>
            <div v-if="outlineForm.video_url" class="video-info">
              当前视频: <a :href="getFullVideoUrl(outlineForm.video_url)" target="_blank">{{ outlineForm.video_filename || '查看视频' }}</a>
              <a-button type="link" size="small" @click="removeVideo">删除</a-button>
            </div>
            <div v-if="videoUploading" class="upload-progress">
              <a-spin size="small" /> 视频上传中...
            </div>
          </div>
        </a-form-item>
        <a-form-item label="排序" name="sort_order">
          <a-input-number v-model:value="outlineForm.sort_order" :min="0" style="width: 100%" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined, SearchOutlined, ReloadOutlined, UploadOutlined, VideoCameraOutlined } from '@ant-design/icons-vue'
import { courseOutlineAPI } from '@/api'
import { uploadCourseVideo, FileUploader } from '@/api/upload'

// 表格列定义
const columns = [
  {
    title: '标题',
    dataIndex: 'title',
    key: 'title',
    width: '20%'
  },
  {
    title: '内容',
    dataIndex: 'content',
    key: 'content',
    ellipsis: true,
    width: '35%'
  },
  {
    title: '视频',
    dataIndex: 'video_url',
    key: 'video_url',
    width: '15%'
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
const videoFileList = ref([])
const videoUploading = ref(false)

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
  video_url: '',
  video_filename: '',
  sort_order: 1
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

// 计算当前选择的课程名称
const selectedCourseName = computed(() => {
  if (!searchForm.course_id || !courseOptions.value.length) {
    return ''
  }
  const selected = courseOptions.value.find(option => option.value === searchForm.course_id)
  return selected ? selected.label : ''
})

// 获取完整的视频URL
const getFullVideoUrl = (videoUrl) => {
  return FileUploader.getFullVideoUrl(videoUrl)
}

// 获取课程列表
const fetchCourses = async () => {
  try {
    const res = await courseOutlineAPI.getCourses({ page: 1, per_page: 1000 })
    
    if (res.success !== false) {
      courseOptions.value = res.data.courses.map(course => ({
        value: course.id,
        label: course.title
      }))
      
      // 默认选择第一个课程
      if (courseOptions.value.length > 0) {
        const firstCourse = courseOptions.value[0]
        searchForm.course_id = firstCourse.value
        console.log('Auto-selected first course:', firstCourse.label)
        // 立即获取第一个课程的大纲
        fetchOutlines()
      }
    } else {
      message.error('获取课程列表失败：' + res.message)
    }
  } catch (error) {
    console.error('Failed to fetch courses:', error)
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
    const res = await courseOutlineAPI.getCourseOutlines({
      course_id: searchForm.course_id
    })
    
    // 确保正确解析数据
    if (res && res.data) {
      outlines.value = res.data
    } else if (res && Array.isArray(res)) {
      // 如果直接返回数组
      outlines.value = res
    } else {
      outlines.value = []
    }
    
    console.log(`Loaded ${outlines.value.length} outlines for course`)
  } catch (error) {
    console.error('Failed to fetch course outlines:', error)
    message.error('获取课程大纲列表失败：' + error.message)
    outlines.value = []
  } finally {
    loading.value = false
  }
}

// 监听课程选择变化
watch(() => searchForm.course_id, (newVal, oldVal) => {
  if (newVal && newVal !== oldVal) {
    // 只有在真正改变时才调用，避免初始化时重复调用
    fetchOutlines()
  } else if (!newVal) {
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
  // 如果已选择课程，则预填充
  if (searchForm.course_id) {
    outlineForm.course_id = searchForm.course_id
  }
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
  outlineForm.video_url = record.video_url || ''
  outlineForm.video_filename = record.video_filename || ''
  outlineForm.sort_order = record.sort_order
  
  modalVisible.value = true
}

// 重置表单
const resetForm = () => {
  outlineForm.id = ''
  outlineForm.course_id = undefined
  outlineForm.title = ''
  outlineForm.content = ''
  outlineForm.video_url = ''
  outlineForm.video_filename = ''
  outlineForm.sort_order = 1  // 默认排序为1，确保是有效数字
  videoFileList.value = []
  
  // 延迟重置表单字段，确保响应式数据已更新
  if (outlineFormRef.value) {
    setTimeout(() => {
      outlineFormRef.value.resetFields()
    }, 50)
  }
}

// 视频上传前校验
const beforeVideoUpload = (file) => {
  try {
    FileUploader.validateVideo(file, 50)
    return true
  } catch (error) {
    message.error(error.message)
    return false
  }
}

// 处理视频上传
const handleVideoUpload = async (options) => {
  const { file } = options
  videoUploading.value = true
  
  try {
    const result = await uploadCourseVideo(file)
    
    if (result.code === 200) {
      outlineForm.video_url = result.data.url
      outlineForm.video_filename = result.data.original_filename
      message.success('视频上传成功')
    } else {
      message.error('视频上传失败：' + result.message)
    }
  } catch (error) {
    message.error('视频上传失败：' + error.message)
  } finally {
    videoUploading.value = false
  }
}

// 删除视频
const removeVideo = () => {
  outlineForm.video_url = ''
  outlineForm.video_filename = ''
  videoFileList.value = []
}

// 提交表单
const handleModalOk = () => {
  outlineFormRef.value.validate().then(async () => {
    try {
      if (isEdit.value) {
        await courseOutlineAPI.updateCourseOutline(outlineForm.id, outlineForm)
        message.success('课程大纲更新成功')
      } else {
        await courseOutlineAPI.createCourseOutline(outlineForm)
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
    await courseOutlineAPI.deleteCourseOutline(id)
    message.success('课程大纲删除成功')
    fetchOutlines()
  } catch (error) {
    message.error('删除失败：' + error.message)
  }
}

// 组件挂载时获取课程列表
onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
.course-outline-management {
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

.current-course-info {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 4px;
  padding: 12px 16px;
  margin-bottom: 16px;
  font-size: 14px;
}

.course-label {
  color: #64748b;
  margin-right: 8px;
}

.course-name {
  color: #0f172a;
  font-weight: 500;
  margin-right: 8px;
}

.outline-count {
  color: #64748b;
  font-size: 13px;
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

.video-preview {
  max-height: 80px;
  overflow: hidden;
}

.video-link {
  color: #1890ff;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 4px;
}

.video-link:hover {
  color: #40a9ff;
  text-decoration: underline;
}

.video-filename {
  font-size: 12px;
  color: #999;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.no-video {
  color: #ccc;
  font-style: italic;
}

.video-info {
  margin-top: 8px;
  font-size: 0.9em;
  color: #555;
}

.video-info a {
  color: #1890ff;
  text-decoration: none;
}

.video-info a:hover {
  text-decoration: underline;
}

.upload-progress {
  margin-top: 8px;
  font-size: 0.9em;
  color: #555;
}

@media (max-width: 768px) {
  .course-outline-management {
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