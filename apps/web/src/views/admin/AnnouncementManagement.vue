<template>
  <div class="announcement-management">
    <!-- 搜索栏和添加按钮在同一行 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="公告标题">
          <a-input
              v-model:value="searchForm.title"
              placeholder="请输入公告标题"
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
        <a-form-item label="类型">
          <a-select
              v-model:value="searchForm.type"
              placeholder="请选择类型"
              style="width: 150px;"
              allow-clear
          >
            <a-select-option value="system">系统公告</a-select-option>
            <a-select-option value="activity">活动公告</a-select-option>
            <a-select-option value="maintenance">维护公告</a-select-option>
            <a-select-option value="notice">重要通知</a-select-option>
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
        发布公告
      </a-button>
    </div>

    <!-- 公告列表 -->
    <a-table
        :columns="columns"
        :data-source="announcements"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
    >
      <template #type="{ record }">
        <a-tag :color="getTypeColor(record?.type)">
          {{ getTypeText(record?.type) }}
        </a-tag>
      </template>

      <template #status="{ record }">
        <a-tag :color="getStatusColor(record?.status)">
          {{ getStatusText(record?.status) }}
        </a-tag>
      </template>

      <template #priority="{ record }">
        <a-tag :color="getPriorityColor(record?.priority)">
          {{ getPriorityText(record?.priority) }}
        </a-tag>
      </template>

      <template #createTime="{ record }">
        {{ formatDate(record?.create_time) }}
      </template>

      <template #action="{ record }">
        <a-space>
          <a-button type="link" size="small" @click="editAnnouncement(record)">
            编辑
          </a-button>
          <a-button type="link" size="small" @click="viewAnnouncement(record)">
            查看
          </a-button>
          <a-dropdown>
            <a-button type="link" size="small">
              更多
              <DownOutlined/>
            </a-button>
            <template #overlay>
              <a-menu @click="({ key }) => handleMenuAction(record, key)">
                <a-menu-item v-if="record?.status === 'draft'" key="publish">
                  发布公告
                </a-menu-item>
                <a-menu-item v-if="record?.status === 'published'" key="archive">
                  归档公告
                </a-menu-item>
                <a-menu-item key="delete" class="danger-item">
                  删除公告
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </a-space>
      </template>
    </a-table>

    <!-- 添加/编辑公告弹窗 -->
    <a-modal
        v-model:open="modalVisible"
        :title="modalTitle"
        @ok="handleModalOk"
        @cancel="handleModalCancel"
        width="800px"
        :body-style="{ maxHeight: '70vh', overflowY: 'auto' }"
    >
      <a-form
          ref="announcementFormRef"
          :model="announcementForm"
          :rules="announcementFormRules"
          layout="vertical"
      >
        <a-form-item label="公告标题" name="title">
          <a-input v-model:value="announcementForm.title" placeholder="请输入公告标题"/>
        </a-form-item>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="公告类型" name="type">
              <a-select v-model:value="announcementForm.type" placeholder="请选择类型">
                <a-select-option value="system">系统公告</a-select-option>
                <a-select-option value="activity">活动公告</a-select-option>
                <a-select-option value="maintenance">维护公告</a-select-option>
                <a-select-option value="notice">重要通知</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="优先级" name="priority">
              <a-select v-model:value="announcementForm.priority" placeholder="请选择优先级">
                <a-select-option value="low">低</a-select-option>
                <a-select-option value="medium">中</a-select-option>
                <a-select-option value="high">高</a-select-option>
                <a-select-option value="urgent">紧急</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="状态" name="status">
              <a-select v-model:value="announcementForm.status" placeholder="请选择状态">
                <a-select-option value="draft">草稿</a-select-option>
                <a-select-option value="published">已发布</a-select-option>
                <a-select-option value="archived">已归档</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="生效时间" name="start_time">
              <a-date-picker
                  v-model:value="announcementForm.start_time"
                  show-time
                  placeholder="请选择生效时间"
                  style="width: 100%;"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="失效时间" name="end_time">
              <a-date-picker
                  v-model:value="announcementForm.end_time"
                  show-time
                  placeholder="请选择失效时间"
                  style="width: 100%;"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="公告摘要" name="summary">
          <a-textarea
              v-model:value="announcementForm.summary"
              placeholder="请输入公告摘要（选填）"
              :rows="2"
          />
        </a-form-item>

        <a-form-item label="公告内容" name="content">
          <a-textarea
              v-model:value="announcementForm.content"
              placeholder="请输入公告详细内容"
              :rows="8"
          />
        </a-form-item>

        <a-form-item label="是否置顶" name="is_pinned">
          <a-switch
              v-model:checked="announcementForm.is_pinned"
              checked-children="是"
              un-checked-children="否"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 查看公告详情弹窗 -->
    <a-modal
        v-model:open="viewModalVisible"
        title="公告详情"
        :footer="null"
        width="700px"
    >
      <div v-if="currentAnnouncement" class="announcement-detail">
        <div class="detail-header">
          <h3>{{ currentAnnouncement?.title || '' }}</h3>
          <div class="meta-info">
            <a-tag :color="getTypeColor(currentAnnouncement?.type)">
              {{ getTypeText(currentAnnouncement?.type) }}
            </a-tag>
            <a-tag :color="getPriorityColor(currentAnnouncement?.priority)">
              {{ getPriorityText(currentAnnouncement?.priority) }}
            </a-tag>
            <a-tag :color="getStatusColor(currentAnnouncement?.status)">
              {{ getStatusText(currentAnnouncement?.status) }}
            </a-tag>
            <a-tag v-if="currentAnnouncement?.is_pinned" color="gold">
              置顶
            </a-tag>
          </div>
        </div>

        <a-divider/>

        <div v-if="currentAnnouncement?.summary" class="detail-section">
          <h4>摘要</h4>
          <p>{{ currentAnnouncement?.summary }}</p>
        </div>

        <div class="detail-section">
          <h4>公告内容</h4>
          <div class="content-text">{{ currentAnnouncement?.content || '' }}</div>
        </div>

        <div class="detail-section">
          <h4>基本信息</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">生效时间：</span>
              <span>{{ formatDate(currentAnnouncement?.start_time) || '立即生效' }}</span>
            </div>
            <div class="info-item">
              <span class="label">失效时间：</span>
              <span>{{ formatDate(currentAnnouncement?.end_time) || '永久有效' }}</span>
            </div>
            <div class="info-item">
              <span class="label">创建时间：</span>
              <span>{{ formatDate(currentAnnouncement?.create_time) || '-' }}</span>
            </div>
            <div class="info-item">
              <span class="label">更新时间：</span>
              <span>{{ formatDate(currentAnnouncement?.update_time) || '-' }}</span>
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
import {PlusOutlined, DownOutlined} from '@ant-design/icons-vue'
import {announcementAPI} from '@/api/admin'
import dayjs from 'dayjs'

export default {
  name: 'AnnouncementManagement',
  components: {
    PlusOutlined,
    DownOutlined
  },
  setup() {
    const loading = ref(false)
    const announcements = ref([])
    const modalVisible = ref(false)
    const viewModalVisible = ref(false)
    const isEdit = ref(false)
    const currentAnnouncement = ref(null)
    const announcementFormRef = ref()

    const searchForm = reactive({
      title: '',
      status: undefined,
      type: undefined
    })

    const announcementForm = reactive({
      title: '',
      type: 'system',
      priority: 'medium',
      status: 'draft',
      summary: '',
      content: '',
      start_time: null,
      end_time: null,
      is_pinned: false
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
        title: '公告标题',
        dataIndex: 'title',
        key: 'title',
        width: 200
      },
      {
        title: '类型',
        dataIndex: 'type',
        key: 'type',
        slots: {customRender: 'type'},
        width: 100
      },
      {
        title: '优先级',
        dataIndex: 'priority',
        key: 'priority',
        slots: {customRender: 'priority'},
        width: 80
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        slots: {customRender: 'status'},
        width: 80
      },
      {
        title: '置顶',
        dataIndex: 'is_pinned',
        key: 'is_pinned',
        render: (text) => text ? '是' : '否',
        width: 60
      },
      {
        title: '生效时间',
        dataIndex: 'start_time',
        key: 'start_time',
        render: (text) => formatDate(text) || '立即生效',
        width: 150
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

    const announcementFormRules = {
      title: [
        {required: true, message: '请输入公告标题', trigger: 'blur'}
      ],
      type: [
        {required: true, message: '请选择公告类型', trigger: 'change'}
      ],
      priority: [
        {required: true, message: '请选择优先级', trigger: 'change'}
      ],
      status: [
        {required: true, message: '请选择状态', trigger: 'change'}
      ],
      content: [
        {required: true, message: '请输入公告内容', trigger: 'blur'}
      ]
    }

    // 获取公告列表
    const fetchAnnouncements = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          title: searchForm.title,
          status: searchForm.status,
          type: searchForm.type
        }

        const result = await announcementAPI.getAnnouncements(params)
        if (result.code === 200) {
          announcements.value = result.data.list
          pagination.total = result.data.total
        }
      } catch (error) {
        message.error('获取公告列表失败')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current = 1
      fetchAnnouncements()
    }

    // 重置搜索
    const resetSearch = () => {
      Object.assign(searchForm, {
        title: '',
        status: undefined,
        type: undefined
      })
      pagination.current = 1
      fetchAnnouncements()
    }

    // 表格分页改变
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchAnnouncements()
    }

    // 显示添加模态框
    const showAddModal = () => {
      isEdit.value = false
      modalVisible.value = true
      resetAnnouncementForm()
    }

    // 编辑公告
    const editAnnouncement = (announcement) => {
      isEdit.value = true
      modalVisible.value = true
      Object.assign(announcementForm, {
        id: announcement.id,
        title: announcement.title,
        type: announcement.type,
        priority: announcement.priority,
        status: announcement.status,
        summary: announcement.summary,
        content: announcement.content,
        start_time: announcement.start_time ? dayjs(announcement.start_time) : null,
        end_time: announcement.end_time ? dayjs(announcement.end_time) : null,
        is_pinned: announcement.is_pinned
      })
    }

    // 查看公告
    const viewAnnouncement = (announcement) => {
      currentAnnouncement.value = announcement
      viewModalVisible.value = true
    }

    // 菜单操作
    const handleMenuAction = async (announcement, action) => {
      if (action === 'delete') {
        try {
          const result = await announcementAPI.deleteAnnouncement(announcement.id)
          if (result.code === 200) {
            message.success('删除成功')
            fetchAnnouncements()
          }
        } catch (error) {
          message.error('删除失败')
        }
      } else if (action === 'publish') {
        await updateAnnouncementStatus(announcement.id, 'published')
      } else if (action === 'archive') {
        await updateAnnouncementStatus(announcement.id, 'archived')
      }
    }

    // 更新公告状态
    const updateAnnouncementStatus = async (announcementId, status) => {
      try {
        const result = await announcementAPI.updateAnnouncement(announcementId, {status})
        if (result.code === 200) {
          message.success('状态更新成功')
          fetchAnnouncements()
        }
      } catch (error) {
        message.error('状态更新失败')
      }
    }

    // 模态框确定
    const handleModalOk = async () => {
      try {
        await announcementFormRef.value.validate()

        const data = {...announcementForm}
        delete data.id

        // 转换时间格式
        if (data.start_time) {
          data.start_time = data.start_time.format('YYYY-MM-DD HH:mm:ss')
        }
        if (data.end_time) {
          data.end_time = data.end_time.format('YYYY-MM-DD HH:mm:ss')
        }

        if (isEdit.value) {
          const result = await announcementAPI.updateAnnouncement(announcementForm.id, data)
          if (result.code === 200) {
            message.success('更新成功')
            modalVisible.value = false
            fetchAnnouncements()
          }
        } else {
          const result = await announcementAPI.createAnnouncement(data)
          if (result.code === 200 || result.code === 201) {
            message.success('创建成功')
            modalVisible.value = false
            fetchAnnouncements()
          }
        }
      } catch (error) {
        console.error('Form validation failed:', error)
      }
    }

    // 模态框取消
    const handleModalCancel = () => {
      modalVisible.value = false
      resetAnnouncementForm()
    }

    // 重置公告表单
    const resetAnnouncementForm = () => {
      Object.assign(announcementForm, {
        title: '',
        type: 'system',
        priority: 'medium',
        status: 'draft',
        summary: '',
        content: '',
        start_time: null,
        end_time: null,
        is_pinned: false
      })
      announcementFormRef.value?.resetFields()
    }

    // 获取类型颜色
    const getTypeColor = (type) => {
      if (!type) return 'default'
      const colorMap = {
        system: 'blue',
        activity: 'green',
        maintenance: 'orange',
        notice: 'red'
      }
      return colorMap[type] || 'default'
    }

    // 获取类型文本
    const getTypeText = (type) => {
      if (!type) return '未知'
      const textMap = {
        system: '系统公告',
        activity: '活动公告',
        maintenance: '维护公告',
        notice: '重要通知'
      }
      return textMap[type] || '未知'
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

    // 获取优先级颜色
    const getPriorityColor = (priority) => {
      if (!priority) return 'default'
      const colorMap = {
        low: 'default',
        medium: 'blue',
        high: 'orange',
        urgent: 'red'
      }
      return colorMap[priority] || 'default'
    }

    // 获取优先级文本
    const getPriorityText = (priority) => {
      if (!priority) return '未知'
      const textMap = {
        low: '低',
        medium: '中',
        high: '高',
        urgent: '紧急'
      }
      return textMap[priority] || '未知'
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return dayjs(dateString).format('YYYY-MM-DD HH:mm')
    }

    const modalTitle = computed(() => isEdit.value ? '编辑公告' : '发布公告')

    onMounted(() => {
      fetchAnnouncements()
    })

    return {
      loading,
      announcements,
      searchForm,
      announcementForm,
      announcementFormRef,
      announcementFormRules,
      modalVisible,
      viewModalVisible,
      isEdit,
      currentAnnouncement,
      pagination,
      columns,
      modalTitle,
      fetchAnnouncements,
      handleSearch,
      resetSearch,
      handleTableChange,
      showAddModal,
      editAnnouncement,
      viewAnnouncement,
      handleMenuAction,
      handleModalOk,
      handleModalCancel,
      getTypeColor,
      getTypeText,
      getStatusColor,
      getStatusText,
      getPriorityColor,
      getPriorityText,
      formatDate
    }
  }
}
</script>

<style scoped>
.announcement-management {
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

.announcement-detail {
  padding: 12px 0;
}

.detail-header h3 {
  margin: 0 0 8px 0;
  color: #1890ff;
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
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
  min-width: 80px;
}

.danger-item {
  color: #ff4d4f !important;
}

@media (max-width: 768px) {
  .announcement-management {
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

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style> 