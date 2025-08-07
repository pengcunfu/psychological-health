<template>
  <div class="order-management">
    <!-- 搜索栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="订单类型">
          <a-select
              v-model:value="searchForm.type"
              placeholder="请选择订单类型"
              style="width: 150px;"
              allow-clear
          >
            <a-select-option value="consultation">咨询订单</a-select-option>
            <a-select-option value="course">课程订单</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="状态">
          <a-select
              v-model:value="searchForm.status"
              placeholder="请选择状态"
              style="width: 120px;"
              allow-clear
          >
            <a-select-option value="pending">待支付</a-select-option>
            <a-select-option value="paid">已支付</a-select-option>
            <a-select-option value="completed">已完成</a-select-option>
            <a-select-option value="cancelled">已取消</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
          <a-button style="margin-left: 8px;" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>
    </div>

    <!-- 订单列表 -->
    <a-table
        :columns="columns"
        :data-source="orders"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
    >
      <template #type="{ record }">
        <a-tag :color="record.type === 'consultation' ? 'blue' : 'green'">
          {{ record.type === 'consultation' ? '咨询订单' : '课程订单' }}
        </a-tag>
      </template>

      <template #status="{ record }">
        <a-tag :color="getStatusColor(record.status)">
          {{ getStatusText(record.status) }}
        </a-tag>
      </template>

      <template #amount="{ record }">
        <span class="amount">¥{{ record.amount || 0 }}</span>
      </template>

      <template #createTime="{ record }">
        {{ formatDate(record.create_time) }}
      </template>

      <template #action="{ record }">
        <a-space>
          <a-button type="link" size="small" @click="viewOrder(record)">
            查看详情
          </a-button>
          <a-dropdown v-if="record.status !== 'completed' && record.status !== 'cancelled'">
            <a-button type="link" size="small">
              更新状态
              <DownOutlined/>
            </a-button>
            <template #overlay>
              <a-menu @click="({ key }) => updateOrderStatus(record.id, key)">
                <a-menu-item v-if="record.status === 'pending'" key="paid">
                  标记为已支付
                </a-menu-item>
                <a-menu-item v-if="record.status === 'paid'" key="completed">
                  标记为已完成
                </a-menu-item>
                <a-menu-item key="cancelled">
                  取消订单
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </a-space>
      </template>
    </a-table>

    <!-- 订单详情弹窗 -->
    <a-modal
        v-model:open="viewModalVisible"
        title="订单详情"
        :footer="null"
        width="600px"
    >
      <div v-if="currentOrder" class="order-detail">
        <div class="detail-item">
          <span class="label">订单号：</span>
          <span>{{ currentOrder.id }}</span>
        </div>
        <div class="detail-item">
          <span class="label">订单类型：</span>
          <a-tag :color="currentOrder.type === 'consultation' ? 'blue' : 'green'">
            {{ currentOrder.type === 'consultation' ? '咨询订单' : '课程订单' }}
          </a-tag>
        </div>
        <div class="detail-item">
          <span class="label">用户ID：</span>
          <span>{{ currentOrder.user_id }}</span>
        </div>
        <div class="detail-item">
          <span class="label">产品ID：</span>
          <span>{{ currentOrder.product_id }}</span>
        </div>
        <div class="detail-item">
          <span class="label">订单金额：</span>
          <span class="amount">¥{{ currentOrder.amount || 0 }}</span>
        </div>
        <div class="detail-item">
          <span class="label">订单状态：</span>
          <a-tag :color="getStatusColor(currentOrder.status)">
            {{ getStatusText(currentOrder.status) }}
          </a-tag>
        </div>
        <div class="detail-item">
          <span class="label">创建时间：</span>
          <span>{{ formatDate(currentOrder.create_time) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">更新时间：</span>
          <span>{{ formatDate(currentOrder.update_time) }}</span>
        </div>
        <div v-if="currentOrder.notes" class="detail-item">
          <span class="label">备注：</span>
          <p>{{ currentOrder.notes }}</p>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script>
import {ref, reactive, onMounted} from 'vue'
import {message} from 'ant-design-vue'
import {DownOutlined} from '@ant-design/icons-vue'
import {orderAPI} from '@/api'

export default {
  name: 'OrderManagement',
  components: {
    DownOutlined
  },
  setup() {
    const loading = ref(false)
    const orders = ref([])
    const viewModalVisible = ref(false)
    const currentOrder = ref(null)

    const searchForm = reactive({
      type: undefined,
      status: undefined
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
        title: '订单号',
        dataIndex: 'id',
        key: 'id',
        width: 200
      },
      {
        title: '订单类型',
        dataIndex: 'type',
        key: 'type',
        slots: {customRender: 'type'}
      },
      {
        title: '用户ID',
        dataIndex: 'user_id',
        key: 'user_id',
        width: 120
      },
      {
        title: '产品ID',
        dataIndex: 'product_id',
        key: 'product_id',
        width: 120
      },
      {
        title: '订单金额',
        dataIndex: 'amount',
        key: 'amount',
        slots: {customRender: 'amount'}
      },
      {
        title: '订单状态',
        dataIndex: 'status',
        key: 'status',
        slots: {customRender: 'status'}
      },
      {
        title: '创建时间',
        dataIndex: 'create_time',
        key: 'create_time',
        slots: {customRender: 'createTime'}
      },
      {
        title: '操作',
        key: 'action',
        slots: {customRender: 'action'},
        width: 180
      }
    ]

    // 获取订单列表
    const fetchOrders = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          type: searchForm.type,
          status: searchForm.status
        }

        const result = await orderAPI.getOrders(params)
        if (result.code === 200) {
          orders.value = result.data.list
          pagination.total = result.data.total
        }
      } catch (error) {
        message.error('获取订单列表失败')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current = 1
      fetchOrders()
    }

    // 重置搜索
    const resetSearch = () => {
      Object.assign(searchForm, {
        type: undefined,
        status: undefined
      })
      pagination.current = 1
      fetchOrders()
    }

    // 表格分页改变
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchOrders()
    }

    // 查看订单详情
    const viewOrder = (order) => {
      currentOrder.value = order
      viewModalVisible.value = true
    }

    // 更新订单状态
    const updateOrderStatus = async (orderId, status) => {
      try {
        const result = await orderAPI.updateOrderStatus(orderId, status)
        if (result.code === 200) {
          message.success('状态更新成功')
          fetchOrders()
        }
      } catch (error) {
        message.error('状态更新失败')
      }
    }

    // 获取状态颜色
    const getStatusColor = (status) => {
      const colorMap = {
        pending: 'orange',
        paid: 'blue',
        completed: 'green',
        cancelled: 'red'
      }
      return colorMap[status] || 'default'
    }

    // 获取状态文本
    const getStatusText = (status) => {
      const textMap = {
        pending: '待支付',
        paid: '已支付',
        completed: '已完成',
        cancelled: '已取消'
      }
      return textMap[status] || '未知'
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }

    onMounted(() => {
      fetchOrders()
    })

    return {
      loading,
      orders,
      searchForm,
      pagination,
      columns,
      viewModalVisible,
      currentOrder,
      fetchOrders,
      handleSearch,
      resetSearch,
      handleTableChange,
      viewOrder,
      updateOrderStatus,
      getStatusColor,
      getStatusText,
      formatDate
    }
  }
}
</script>

<style scoped>
.order-management {
  padding: 0;
}

.search-and-action-bar {
  background: white;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.search-form .ant-form-item {
  margin-bottom: 0;
}

.search-form .ant-form-item:last-child {
  margin-bottom: 0;
}

.order-detail {
  padding: 12px 0;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 12px;
}

.detail-item .label {
  font-weight: 500;
  width: 100px;
  color: #666;
  flex-shrink: 0;
}

.detail-item p {
  margin: 0;
  line-height: 1.6;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.amount {
  font-weight: 600;
  color: #f5222d;
}

@media (max-width: 768px) {
  .order-management {
    padding: 8px;
  }

  .search-and-action-bar {
    padding: 8px;
    margin-bottom: 8px;
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
}
</style> 