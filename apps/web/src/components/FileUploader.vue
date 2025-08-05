<template>
  <div class="file-uploader">
    <a-upload
        v-model:file-list="fileList"
        :action="uploadUrl"
        :headers="uploadHeaders"
        :before-upload="beforeUpload"
        :on-change="handleChange"
        :on-remove="handleRemove"
        :list-type="listType"
        :accept="accept"
        :multiple="multiple"
        :max-count="maxCount"
        :show-upload-list="showUploadList"
    >
      <div v-if="listType === 'picture-card'" class="upload-card">
        <div v-if="fileList.length < maxCount" class="upload-button">
          <PlusOutlined />
          <div style="margin-top: 8px">Upload</div>
        </div>
      </div>
      <a-button v-else>
        <UploadOutlined />
        {{ buttonText }}
      </a-button>
    </a-upload>

    <!-- 预览模态框 -->
    <a-modal
        v-model:open="previewVisible"
        :title="previewTitle"
        :footer="null"
        centered
    >
      <img :src="previewImage" style="width: 100%" />
    </a-modal>
  </div>
</template>

<script>
import { ref, watch, computed } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined, UploadOutlined } from '@ant-design/icons-vue'

export default {
  name: 'FileUploader',
  components: {
    PlusOutlined,
    UploadOutlined
  },
  props: {
    value: {
      type: [String, Array],
      default: ''
    },
    accept: {
      type: String,
      default: '*'
    },
    maxSize: {
      type: Number,
      default: 10 // MB
    },
    maxCount: {
      type: Number,
      default: 1
    },
    multiple: {
      type: Boolean,
      default: false
    },
    listType: {
      type: String,
      default: 'text', // text, picture, picture-card
      validator: value => ['text', 'picture', 'picture-card'].includes(value)
    },
    buttonText: {
      type: String,
      default: '上传文件'
    },
    showUploadList: {
      type: Boolean,
      default: true
    }
  },
  emits: ['update:value', 'change'],
  setup(props, { emit }) {
    const fileList = ref([])
    const previewVisible = ref(false)
    const previewImage = ref('')
    const previewTitle = ref('')

    // 上传地址
    const uploadUrl = computed(() => {
      return `${import.meta.env.VITE_APP_API_URL || '/api'}/upload/image`
    })

    // 上传头部
    const uploadHeaders = computed(() => {
      const token = localStorage.getItem('token')
      return token ? { Authorization: `Bearer ${token}` } : {}
    })

    // 监听值变化
    watch(() => props.value, (newValue) => {
      if (newValue) {
        if (Array.isArray(newValue)) {
          fileList.value = newValue.map((url, index) => ({
            uid: `${index}`,
            name: `image-${index}`,
            status: 'done',
            url: getFullImageUrl(url),
            response: { data: { url } }
          }))
        } else if (typeof newValue === 'string' && newValue.trim()) {
          fileList.value = [{
            uid: '1',
            name: 'image',
            status: 'done',
            url: getFullImageUrl(newValue),
            response: { data: { url: newValue } }
          }]
        } else {
          fileList.value = []
        }
      } else {
        fileList.value = []
      }
    }, { immediate: true })

    // 获取完整图片URL
    const getFullImageUrl = (url) => {
      if (!url) return ''
      if (url.startsWith('http')) return url
      return `/static/uploads/${url}`
    }

    // 上传前检查
    const beforeUpload = (file) => {
      // 检查文件类型
      if (props.accept !== '*') {
        const acceptTypes = props.accept.split(',').map(type => type.trim())
        const fileType = file.type
        const isValidType = acceptTypes.some(type => {
          if (type.endsWith('/*')) {
            return fileType.startsWith(type.slice(0, -1))
          }
          return fileType === type || file.name.toLowerCase().endsWith(type.replace('*', ''))
        })
        
        if (!isValidType) {
          message.error(`只能上传 ${props.accept} 格式的文件！`)
          return false
        }
      }

      // 检查文件大小
      const isValidSize = file.size / 1024 / 1024 < props.maxSize
      if (!isValidSize) {
        message.error(`文件大小不能超过 ${props.maxSize}MB！`)
        return false
      }

      return true
    }

    // 处理上传状态变化
    const handleChange = ({ fileList: newFileList }) => {
      fileList.value = newFileList

      // 过滤成功上传的文件
      const successFiles = newFileList.filter(file => 
        file.status === 'done' && file.response && file.response.success
      )

      if (props.multiple) {
        const urls = successFiles.map(file => file.response.data.url)
        emit('update:value', urls)
        emit('change', urls)
      } else {
        const url = successFiles.length > 0 ? successFiles[0].response.data.url : ''
        emit('update:value', url)
        emit('change', url)
      }
    }

    // 处理文件移除
    const handleRemove = (file) => {
      const remainingFiles = fileList.value.filter(f => f.uid !== file.uid)
      const successFiles = remainingFiles.filter(f => 
        f.status === 'done' && f.response && f.response.success
      )

      if (props.multiple) {
        const urls = successFiles.map(f => f.response.data.url)
        emit('update:value', urls)
        emit('change', urls)
      } else {
        emit('update:value', '')
        emit('change', '')
      }
    }

    // 预览图片
    const handlePreview = (file) => {
      previewImage.value = file.url || file.preview
      previewVisible.value = true
      previewTitle.value = file.name || file.url.substring(file.url.lastIndexOf('/') + 1)
    }

    return {
      fileList,
      previewVisible,
      previewImage,
      previewTitle,
      uploadUrl,
      uploadHeaders,
      beforeUpload,
      handleChange,
      handleRemove,
      handlePreview,
      getFullImageUrl
    }
  }
}
</script>

<style scoped>
.file-uploader {
  width: 100%;
}

.upload-card {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-button {
  text-align: center;
  color: #999;
}

:deep(.ant-upload-select-picture-card) {
  width: 104px;
  height: 104px;
  border-radius: 6px;
}

:deep(.ant-upload-list-picture-card-container) {
  width: 104px;
  height: 104px;
}

:deep(.ant-upload-list-picture-card .ant-upload-list-item) {
  border-radius: 6px;
}

:deep(.ant-upload-list-picture-card .ant-upload-list-item-image) {
  border-radius: 6px;
}
</style> 