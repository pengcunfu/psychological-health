<template>
  <div class="banner-management">
    <!-- 搜索栏和添加按钮在同一行 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="标题">
          <a-input
              v-model:value="searchForm.title"
              placeholder="请输入轮播图标题"
              style="width: 200px;"
          />
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
        添加轮播图
      </a-button>
    </div>

    <!-- 轮播图列表 -->
    <a-table
        :columns="columns"
        :data-source="banners"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'image_url'">
          <a-image
              :src="FileUploader.getFullImageUrl(record?.image_url)"
              :alt="record?.title || ''"
              width="120"
              height="60"
              style="object-fit: cover; border-radius: 4px;"
              :preview="true"
          />
        </template>
        
        <template v-else-if="column.key === 'create_time'">
          {{ formatDate(record.create_time) }}
        </template>
        
        <template v-else-if="column.key === 'action'">
          <a-space>
            <a-button type="link" size="small" @click="editBanner(record)">
              编辑
            </a-button>
            <a-button type="link" size="small" @click="viewBanner(record)">
              查看
            </a-button>
            <a-popconfirm
                title="确定要删除这个轮播图吗？"
                @confirm="deleteBanner(record.id)"
            >
              <a-button type="link" size="small" danger>
                删除
              </a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 添加/编辑轮播图弹窗 -->
    <a-modal
        v-model:open="modalVisible"
        :title="modalTitle"
        @ok="handleModalOk"
        @cancel="handleModalCancel"
        width="700px"
    >
      <a-form
          ref="bannerFormRef"
          :model="bannerForm"
          :rules="bannerFormRules"
          layout="vertical"
      >
        <a-form-item label="标题" name="title">
          <a-input v-model:value="bannerForm.title" placeholder="请输入轮播图标题"/>
        </a-form-item>

        <a-form-item label="链接地址" name="link_url">
          <a-input v-model:value="bannerForm.link_url" placeholder="请输入链接地址"/>
        </a-form-item>

        <a-form-item label="排序" name="sort_order">
          <a-input-number
              v-model:value="bannerForm.sort_order"
              placeholder="请输入排序值"
              style="width: 100%;"
              :min="0"
          />
        </a-form-item>

        <a-form-item label="轮播图" name="image_url">
          <a-upload
              v-model:file-list="fileList"
              :before-upload="beforeUpload"
              :custom-request="uploadImage"
              @remove="handleRemoveImage"
              list-type="picture-card"
              :max-count="1"
              accept="image/*"
              :show-upload-list="{
                showPreviewIcon: true,
                showRemoveIcon: true,
                showDownloadIcon: false
              }"
          >
            <div v-if="fileList.length < 1">
              <upload-outlined/>
              <div style="margin-top: 8px;">上传图片</div>
              <div style="color: #999; font-size: 12px; margin-top: 4px;">
                支持 JPG、PNG、GIF、WebP<br/>
                文件大小不超过 5MB
              </div>
            </div>
          </a-upload>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 查看轮播图详情弹窗 -->
    <a-modal
        v-model:open="viewModalVisible"
        title="轮播图详情"
        :footer="null"
        width="600px"
    >
      <div v-if="currentBanner" class="banner-detail">
        <div class="detail-header">
          <h3>{{ currentBanner?.title || '' }}</h3>
        </div>

        <a-divider/>

        <div class="detail-image">
          <a-image
              :src="FileUploader.getFullImageUrl(currentBanner?.image_url)"
              :alt="currentBanner?.title || ''"
              width="100%"
              style="max-height: 300px; object-fit: contain;"
              :preview="true"
          />
        </div>

        <a-divider/>

        <div class="detail-section">
          <a-descriptions bordered :column="1">
            <a-descriptions-item label="标题">{{ currentBanner?.title || '-' }}</a-descriptions-item>
            <a-descriptions-item label="链接地址">
              <a :href="currentBanner?.link_url" target="_blank">{{ currentBanner?.link_url || '-' }}</a>
            </a-descriptions-item>
            <a-descriptions-item label="排序">{{ currentBanner?.sort_order || '0' }}</a-descriptions-item>
            <a-descriptions-item label="创建时间">{{ formatDate(currentBanner?.create_time) }}</a-descriptions-item>
            <a-descriptions-item label="更新时间">{{ formatDate(currentBanner?.update_time) }}</a-descriptions-item>
          </a-descriptions>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script>
import {ref, reactive, onMounted, computed} from 'vue'
import {message} from 'ant-design-vue'
import {PlusOutlined, UploadOutlined} from '@ant-design/icons-vue'
import {bannerAPI} from '@/api/admin'
import {uploadBanner, FileUploader} from '@/api/upload'

export default {
  name: 'BannerManagement',
  components: {
    PlusOutlined,
    UploadOutlined
  },
  setup() {
    const loading = ref(false)
    const banners = ref([])
    const modalVisible = ref(false)
    const viewModalVisible = ref(false)
    const isEdit = ref(false)
    const currentBanner = ref(null)
    const bannerFormRef = ref()
    const fileList = ref([])

    const searchForm = reactive({
      title: ''
    })

    const bannerForm = reactive({
      title: '',
      image_url: '',
      link_url: '',
      sort_order: 0
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
        title: '图片',
        dataIndex: 'image_url',
        key: 'image_url',
        width: 150
      },
      {
        title: '标题',
        dataIndex: 'title',
        key: 'title',
        width: 200
      },
      {
        title: '链接地址',
        dataIndex: 'link_url',
        key: 'link_url',
        ellipsis: true,
        width: 250
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
        width: 150
      },
      {
        title: '操作',
        key: 'action',
        width: 150,
        fixed: 'right'
      }
    ]

    const bannerFormRules = {
      title: [
        {required: true, message: '请输入轮播图标题', trigger: 'blur'}
      ],
      image_url: [
        {required: true, message: '请上传轮播图图片', trigger: 'change'}
      ]
    }

    // 获取轮播图列表
    const fetchBanners = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.current,
          per_page: pagination.pageSize,
          title: searchForm.title
        }

        const result = await bannerAPI.getBanners(params)
        if (result.code === 200) {
          banners.value = result.data.list || []
          pagination.total = result.data.total || 0
        }
      } catch (error) {
        console.error('获取轮播图列表失败:', error)
        message.error('获取轮播图列表失败')
      } finally {
        loading.value = false
      }
    }

    // 搜索
    const handleSearch = () => {
      pagination.current = 1
      fetchBanners()
    }

    // 重置搜索
    const resetSearch = () => {
      searchForm.title = ''
      pagination.current = 1
      fetchBanners()
    }

    // 表格分页改变
    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchBanners()
    }

    // 显示添加模态框
    const showAddModal = () => {
      isEdit.value = false
      modalVisible.value = true
      resetBannerForm()
    }

    // 编辑轮播图
    const editBanner = (banner) => {
      isEdit.value = true
      modalVisible.value = true

      // 填充表单数据
      Object.assign(bannerForm, {
        id: banner.id,
        title: banner.title,
        image_url: banner.image_url,
        link_url: banner.link_url,
        sort_order: banner.sort_order
      })

      // 设置图片预览
      if (banner.image_url) {
        // 使用封装的方法获取完整URL
        const fullImageUrl = FileUploader.getFullImageUrl(banner.image_url)
        
        fileList.value = [{
          uid: '-1',
          name: 'banner.jpg',
          status: 'done',
          url: fullImageUrl,
          thumbUrl: fullImageUrl
        }]
      } else {
        fileList.value = []
      }
    }

    // 查看轮播图
    const viewBanner = (banner) => {
      currentBanner.value = banner
      viewModalVisible.value = true
    }

    // 删除轮播图
    const deleteBanner = async (id) => {
      try {
        const result = await bannerAPI.deleteBanner(id)
        if (result.code === 200) {
          message.success('删除成功')
          fetchBanners()
        } else {
          message.error(result.message || '删除失败')
        }
      } catch (error) {
        console.error('删除轮播图失败:', error)
        message.error('删除轮播图失败')
      }
    }

    // 模态框确定
    const handleModalOk = async () => {
      try {
        await bannerFormRef.value.validate()

        if (isEdit.value) {
          // 编辑轮播图
          const result = await bannerAPI.updateBanner(bannerForm.id, bannerForm)
          if (result.code === 200) {
            message.success('更新成功')
            modalVisible.value = false
            fetchBanners()
          } else {
            message.error(result.message || '更新失败')
          }
        } else {
          // 创建轮播图
          const result = await bannerAPI.createBanner(bannerForm)
          if (result.code === 200 || result.code === 201) {
            message.success('创建成功')
            modalVisible.value = false
            fetchBanners()
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
      resetBannerForm()
    }

    // 重置轮播图表单
    const resetBannerForm = () => {
      Object.assign(bannerForm, {
        title: '',
        image_url: '',
        link_url: '',
        sort_order: 0
      })
      fileList.value = []
      bannerFormRef.value?.resetFields()
    }

    // 上传前验证
    const beforeUpload = (file) => {
      try {
        // 使用封装的验证方法
        FileUploader.validateImage(file, 5)
        return true // 允许上传
      } catch (error) {
        message.error(error.message)
        return false
      }
    }

    // 上传图片
    const uploadImage = async ({file}) => {
      try {
        // 调用横幅图上传接口
        const result = await uploadBanner(file)
        
        if (result.success && result.data) {
          // 上传成功，设置图片URL
          const imageUrl = result.data.url
          // 使用封装的方法获取完整URL
          const fullImageUrl = FileUploader.getFullImageUrl(imageUrl)
          
          bannerForm.image_url = imageUrl // 保存相对路径到表单
          
          // 更新文件列表显示，使用完整URL进行预览
          fileList.value = [{
            uid: file.uid,
            name: result.data.original_filename || file.name,
            status: 'done',
            url: fullImageUrl, // 使用完整URL进行预览
            response: result.data,
            thumbUrl: fullImageUrl // 添加缩略图URL
          }]
          
          message.success('图片上传成功')
        } else {
          // 上传失败
          fileList.value = [{
            uid: file.uid,
            name: file.name,
            status: 'error'
          }]
          message.error(result.message || '图片上传失败')
        }
      } catch (error) {
        console.error('上传图片失败:', error)
        fileList.value = [{
          uid: file.uid,
          name: file.name,
          status: 'error'
        }]
        message.error('图片上传失败')
      }
    }

    // 删除图片
    const handleRemoveImage = () => {
      bannerForm.image_url = ''
      fileList.value = []
      return true
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }

    const modalTitle = computed(() => isEdit.value ? '编辑轮播图' : '添加轮播图')

    onMounted(() => {
      fetchBanners()
    })

    return {
      loading,
      banners,
      searchForm,
      bannerForm,
      bannerFormRef,
      bannerFormRules,
      modalVisible,
      viewModalVisible,
      isEdit,
      currentBanner,
      pagination,
      columns,
      fileList,
      modalTitle,
      fetchBanners,
      handleSearch,
      resetSearch,
      handleTableChange,
      showAddModal,
      editBanner,
      viewBanner,
      deleteBanner,
      handleModalOk,
      handleModalCancel,
      beforeUpload,
      uploadImage,
      formatDate,
      handleRemoveImage,
      FileUploader
    }
  }
}
</script>

<style scoped>
.banner-management {
  padding: 0;
  margin: 0;
}

.banner-detail {
  padding: 12px 0;
}

.detail-header {
  margin-bottom: 16px;
}

.detail-header h3 {
  margin: 0;
  color: #1890ff;
}

.detail-image {
  margin-bottom: 16px;
  text-align: center;
}

.detail-section {
  margin-bottom: 16px;
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
  flex: 1; /* Allow form to grow and shrink */
  margin-right: 12px; /* Space between form and button */
}

.search-form .ant-form-item {
  margin-bottom: 0; /* Remove bottom margin for inline form items */
}

.search-form .ant-form-item:last-child {
  margin-bottom: 0; /* Remove bottom margin for the last item */
}

@media (max-width: 768px) {
  .banner-management {
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