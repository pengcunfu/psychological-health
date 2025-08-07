<template>
  <div class="appointment-management">
    <!-- 搜索栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="咨询师ID">
          <a-input v-model:value="searchForm.counselor_id" placeholder="请输入咨询师ID" style="width: 150px;" />
        </a-form-item>
        <a-form-item label="用户ID">
          <a-input v-model:value="searchForm.user_id" placeholder="请输入用户ID" style="width: 150px;" />
        </a-form-item>
        <a-form-item label="状态">
          <a-select v-model:value="searchForm.status" placeholder="请选择状态" style="width: 150px;" allow-clear>
            <a-select-option value="pending">待确认</a-select-option>
            <a-select-option value="confirmed">已确认</a-select-option>
            <a-select-option value="completed">已完成</a-select-option>
            <a-select-option value="cancelled">已取消</a-select-option>
            <a-select-option value="rescheduled">已改期</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="日期范围">
          <a-range-picker v-model:value="searchForm.date_range" style="width: 240px;" />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
          <a-button style="margin-left: 8px;" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>
    </div>

    <!-- 预约列表 -->
    <a-table :columns="columns" :data-source="appointments" :loading="loading" :pagination="pagination"
      @change="handleTableChange" row-key="id">
      <template #counselor_name="{ record }">
        <div class="counselor-info">
          <a-avatar v-if="record.counselor_avatar" :src="record.counselor_avatar" size="small" />
          <span class="counselor-name">{{ record.counselor_name }}</span>
        </div>
      </template>

      <template #user_name="{ record }">
        <div class="user-info">
          <a-avatar v-if="record.user_avatar" :src="record.user_avatar" size="small" />
          <span class="user-name">{{ record.user_name }}</span>
        </div>
      </template>

      <template #appointment_time="{ record }">
        <div class="time-info">
          <div>{{ formatDate(record.appointment_date) }}</div>
          <div class="time-range">{{ record.start_time }} - {{ record.end_time }}</div>
        </div>
      </template>

      <template #status="{ record }">
        <a-tag :color="getStatusColor(record.status)">
          {{ getStatusText(record.status) }}
        </a-tag>
      </template>

      <template #createTime="{ record }">
        {{ formatDate(record.create_time) }}
      </template>

      <template #action="{ record }">
        <a-space>
          <a-button type="link" size="small" @click="viewAppointment(record)">
            查看详情
          </a-button>
          <a-dropdown v-if="record.status === 'pending'">
            <a-button type="link" size="small">
              操作
              <DownOutlined />
            </a-button>
            <template #overlay>
              <a-menu @click="({ key }) => handleStatusChange(record.id, key)">
                <a-menu-item key="confirmed">
                  <span style="color: #52c41a;">确认预约</span>
                </a-menu-item>
                <a-menu-item key="cancelled">
                  <span style="color: #ff4d4f;">取消预约</span>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
          <a-dropdown v-else-if="record.status === 'confirmed'">
            <a-button type="link" size="small">
              操作
              <DownOutlined />
            </a-button>
            <template #overlay>
              <a-menu @click="({ key }) => handleStatusChange(record.id, key)">
                <a-menu-item key="completed">
                  <span style="color: #1890ff;">标记完成</span>
                </a-menu-item>
                <a-menu-item key="cancelled">
                  <span style="color: #ff4d4f;">取消预约</span>
                </a-menu-item>
                <a-menu-item key="rescheduled">
                  <span style="color: #faad14;">改期</span>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </a-space>
      </template>
    </a-table>

    <!-- 查看预约详情弹窗 -->
    <a-modal v-model:open="viewModalVisible" title="预约详情" :footer="null" width="700px">
      <div v-if="currentAppointment" class="appointment-detail">
        <div class="detail-header">
          <h3>预约信息</h3>
          <a-tag :color="getStatusColor(currentAppointment.status)">
            {{ getStatusText(currentAppointment.status) }}
          </a-tag>
        </div>

        <a-divider />

        <div class="detail-section">
          <h4>基本信息</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">预约编号：</span>
              <span>{{ currentAppointment.id }}</span>
            </div>
            <div class="info-item">
              <span class="label">预约类型：</span>
              <span>{{ getAppointmentType(currentAppointment.type) }}</span>
            </div>
            <div class="info-item">
              <span class="label">预约日期：</span>
              <span>{{ formatDate(currentAppointment.appointment_date) }}</span>
            </div>
            <div class="info-item">
              <span class="label">预约时间：</span>
              <span>{{ currentAppointment.start_time }} - {{ currentAppointment.end_time }}</span>
            </div>
            <div class="info-item">
              <span class="label">创建时间：</span>
              <span>{{ formatDate(currentAppointment.create_time) }}</span>
            </div>
            <div class="info-item">
              <span class="label">更新时间：</span>
              <span>{{ formatDate(currentAppointment.update_time) }}</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>咨询师信息</h4>
          <div class="person-info">
            <a-avatar v-if="currentAppointment.counselor_avatar" :src="currentAppointment.counselor_avatar"
              :size="64" />
            <div class="person-details">
              <div class="person-name">{{ currentAppointment.counselor_name }}</div>
              <div class="person-id">ID: {{ currentAppointment.counselor_id }}</div>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>用户信息</h4>
          <div class="person-info">
            <a-avatar v-if="currentAppointment.user_avatar" :src="currentAppointment.user_avatar" :size="64" />
            <div class="person-details">
              <div class="person-name">{{ currentAppointment.user_name }}</div>
              <div class="person-id">ID: {{ currentAppointment.user_id }}</div>
              <div v-if="currentAppointment.user_phone" class="person-contact">
                电话: {{ currentAppointment.user_phone }}
              </div>
            </div>
          </div>
        </div>

        <div class="detail-section" v-if="currentAppointment.description">
          <h4>预约描述</h4>
          <p class="description-text">{{ currentAppointment.description }}</p>
        </div>

        <div class="detail-section" v-if="currentAppointment.notes">
          <h4>备注</h4>
          <p class="notes-text">{{ currentAppointment.notes }}</p>
        </div>

        <div v-if="currentAppointment.status === 'pending'" class="detail-section">
          <h4>操作</h4>
          <a-space>
            <a-button type="primary" @click="handleStatusChange(currentAppointment.id, 'confirmed')">
              确认预约
            </a-button>
            <a-button danger @click="handleStatusChange(currentAppointment.id, 'cancelled')">
              取消预约
            </a-button>
          </a-space>
        </div>

        <div v-else-if="currentAppointment.status === 'confirmed'" class="detail-section">
          <h4>操作</h4>
          <a-space>
            <a-button type="primary" @click="handleStatusChange(currentAppointment.id, 'completed')">
              标记完成
            </a-button>
            <a-button danger @click="handleStatusChange(currentAppointment.id, 'cancelled')">
              取消预约
            </a-button>
            <a-button @click="showRescheduleModal(currentAppointment)">
              改期
            </a-button>
          </a-space>
        </div>
      </div>
    </a-modal>

    <!-- 改期弹窗 -->
    <a-modal v-model:open="rescheduleModalVisible" title="预约改期" @ok="handleReschedule"
      @cancel="rescheduleModalVisible = false" width="500px">
      <a-form ref="rescheduleFormRef" :model="rescheduleForm" :rules="rescheduleFormRules" layout="vertical">
        <a-form-item label="预约日期" name="appointment_date">
          <a-date-picker v-model:value="rescheduleForm.appointment_date" style="width: 100%;" />
        </a-form-item>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="开始时间" name="start_time">
              <a-time-picker v-model:value="rescheduleForm.start_time" format="HH:mm" style="width: 100%;" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="结束时间" name="end_time">
              <a-time-picker v-model:value="rescheduleForm.end_time" format="HH:mm" style="width: 100%;" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="改期原因" name="reason">
          <a-textarea v-model:value="rescheduleForm.reason" placeholder="请输入改期原因" :rows="3" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>

import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { DownOutlined } from '@ant-design/icons-vue'
import { appointmentAPI } from '@/api'
import dayjs from 'dayjs'

const loading = ref(false)
const appointments = ref([])
const viewModalVisible = ref(false)
const rescheduleModalVisible = ref(false)
const currentAppointment = ref(null)
const rescheduleFormRef = ref()

const searchForm = reactive({
  counselor_id: '',
  user_id: '',
  status: undefined,
  date_range: []
})

const rescheduleForm = reactive({
  appointment_id: null,
  appointment_date: null,
  start_time: null,
  end_time: null,
  reason: ''
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
    title: '预约编号',
    dataIndex: 'id',
    key: 'id',
    width: 100
  },
  {
    title: '咨询师',
    dataIndex: 'counselor_name',
    key: 'counselor_name',
    slots: { customRender: 'counselor_name' },
    width: 150
  },
  {
    title: '用户',
    dataIndex: 'user_name',
    key: 'user_name',
    slots: { customRender: 'user_name' },
    width: 150
  },
  {
    title: '预约时间',
    dataIndex: 'appointment_date',
    key: 'appointment_date',
    slots: { customRender: 'appointment_time' },
    width: 200
  },
  {
    title: '类型',
    dataIndex: 'type',
    key: 'type',
    render: (text) => getAppointmentType(text),
    width: 100
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    slots: { customRender: 'status' },
    width: 100
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
    width: 180
  }
]

const rescheduleFormRules = {
  appointment_date: [
    { required: true, message: '请选择预约日期', trigger: 'change' }
  ],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ]
}

// 获取预约列表
const fetchAppointments = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.current,
      per_page: pagination.pageSize,
      counselor_id: searchForm.counselor_id,
      user_id: searchForm.user_id,
      status: searchForm.status
    }

    if (searchForm.date_range && searchForm.date_range.length === 2) {
      params.start_date = searchForm.date_range[0].format('YYYY-MM-DD')
      params.end_date = searchForm.date_range[1].format('YYYY-MM-DD')
    }

    const result = await appointmentAPI.getAppointments(params)
    if (result.code === 200) {
      appointments.value = result.data.list
      pagination.total = result.data.total
    }
  } catch (error) {
    message.error('获取预约列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  fetchAppointments()
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    counselor_id: '',
    user_id: '',
    status: undefined,
    date_range: []
  })
  pagination.current = 1
  fetchAppointments()
}

// 表格分页改变
const handleTableChange = (pag) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchAppointments()
}

// 查看预约详情
const viewAppointment = (appointment) => {
  currentAppointment.value = appointment
  viewModalVisible.value = true
}

// 处理状态变更
const handleStatusChange = async (appointmentId, status) => {
  try {
    const result = await appointmentAPI.updateAppointmentStatus(appointmentId, status)
    if (result.code === 200) {
      message.success('状态更新成功')
      fetchAppointments()
      if (viewModalVisible.value) {
        viewModalVisible.value = false
      }
    }
  } catch (error) {
    message.error('状态更新失败')
  }
}

// 显示改期弹窗
const showRescheduleModal = (appointment) => {
  rescheduleForm.appointment_id = appointment.id
  rescheduleForm.appointment_date = dayjs(appointment.appointment_date)
  rescheduleForm.start_time = dayjs(appointment.start_time, 'HH:mm')
  rescheduleForm.end_time = dayjs(appointment.end_time, 'HH:mm')
  rescheduleForm.reason = ''

  rescheduleModalVisible.value = true
}

// 处理改期
const handleReschedule = async () => {
  try {
    await rescheduleFormRef.value.validate()

    const data = {
      appointment_date: rescheduleForm.appointment_date.format('YYYY-MM-DD'),
      start_time: rescheduleForm.start_time.format('HH:mm'),
      end_time: rescheduleForm.end_time.format('HH:mm'),
      reason: rescheduleForm.reason,
      status: 'rescheduled'
    }

    const result = await appointmentAPI.updateAppointment(rescheduleForm.appointment_id, data)
    if (result.code === 200) {
      message.success('预约改期成功')
      rescheduleModalVisible.value = false
      fetchAppointments()
      if (viewModalVisible.value) {
        viewModalVisible.value = false
      }
    }
  } catch (error) {
    console.error('Form validation failed:', error)
  }
}

// 获取状态颜色
const getStatusColor = (status) => {
  const colorMap = {
    pending: 'orange',
    confirmed: 'blue',
    completed: 'green',
    cancelled: 'red',
    rescheduled: 'gold'
  }
  return colorMap[status] || 'default'
}

// 获取状态文本
const getStatusText = (status) => {
  const textMap = {
    pending: '待确认',
    confirmed: '已确认',
    completed: '已完成',
    cancelled: '已取消',
    rescheduled: '已改期'
  }
  return textMap[status] || '未知'
}

// 获取预约类型
const getAppointmentType = (type) => {
  const typeMap = {
    online: '线上咨询',
    offline: '线下咨询',
    phone: '电话咨询',
    video: '视频咨询'
  }
  return typeMap[type] || '未知'
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return dayjs(dateString).format('YYYY-MM-DD')
}

onMounted(() => {
  fetchAppointments()
})
</script>

<style lang="scss" scoped>
.appointment-management {
  padding: 0;
}

.search-and-action-bar {
  background: white;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.search-form {
  .ant-form-item {
    margin-bottom: 0;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.counselor-info,
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.counselor-name,
.user-name {
  font-weight: 500;
}

.time-info {
  display: flex;
  flex-direction: column;

  .time-range {
    font-size: 12px;
    color: #666;
    margin-top: 4px;
  }
}

.appointment-detail {
  padding: 12px 0;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;

  h3 {
    margin: 0;
    color: #1890ff;
  }
}

.detail-section {
  margin-bottom: 16px;

  h4 {
    margin: 0 0 8px 0;
    color: #333;
    font-size: 14px;
    font-weight: 600;
  }
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.info-item {
  display: flex;
  align-items: center;

  .label {
    font-weight: 500;
    color: #666;
    margin-right: 8px;
    min-width: 80px;
  }
}

.person-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.person-details {
  display: flex;
  flex-direction: column;

  .person-name {
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 4px;
  }

  .person-id {
    font-size: 13px;
    color: #666;
    margin-bottom: 4px;
  }

  .person-contact {
    font-size: 13px;
    color: #666;
  }
}

.description-text,
.notes-text {
  line-height: 1.6;
  margin: 0;
  white-space: pre-wrap;
}

@media (max-width: 768px) {
  .appointment-management {
    padding: 8px;
  }

  .search-and-action-bar {
    padding: 8px;
    margin-bottom: 8px;
  }

  .search-form {
    .ant-form {
      flex-direction: column;
    }

    .ant-form-item {
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }

  .detail-header {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .person-info {
    flex-direction: column;
    text-align: center;
  }
}
</style>