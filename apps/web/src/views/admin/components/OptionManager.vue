<template>
  <div class="option-manager">
    <div class="header">
      <div class="title">
        <h4>选项管理</h4>
        <span class="subtitle">题目ID: {{ questionId }}</span>
      </div>
      <a-button type="primary" size="small" @click="addOption">
        <template #icon>
          <PlusOutlined/>
        </template>
        添加选项
      </a-button>
    </div>

    <!-- 选项列表 -->
    <div class="option-list">
      <a-list
          :data-source="options"
          :loading="loading"
          size="small"
      >
        <template #renderItem="{ item, index }">
          <a-list-item>
            <template #actions>
              <a @click="editOption(item, index)">编辑</a>
              <a-popconfirm
                  title="确定删除这个选项吗？"
                  @confirm="deleteOption(index)"
                  ok-text="确定"
                  cancel-text="取消"
              >
                <a style="color: #ff4d4f">删除</a>
              </a-popconfirm>
            </template>

            <a-list-item-meta>
              <template #title>
                <div class="option-title">
                  <span class="order">选项 {{ String.fromCharCode(65 + index) }}</span>
                  <span class="score">分值: {{ item.score || 0 }}</span>
                </div>
              </template>
              <template #description>
                <div class="option-content">{{ item.option_text }}</div>
              </template>
            </a-list-item-meta>
          </a-list-item>
        </template>
      </a-list>

      <!-- 空状态 -->
      <a-empty v-if="options.length === 0" description="暂无选项" />
    </div>

    <!-- 选项编辑表单 -->
    <div class="option-form" v-if="editingIndex !== -1">
      <a-divider orientation="left">
        {{ editingIndex === options.length ? '添加选项' : '编辑选项' }}
      </a-divider>
      
      <a-form layout="vertical">
        <a-form-item label="选项内容">
          <a-textarea
              v-model:value="currentOption.option_text"
              placeholder="请输入选项内容"
              :rows="2"
          />
        </a-form-item>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="选项值">
              <a-input
                  v-model:value="currentOption.option_value"
                  placeholder="选项值（可选）"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="分值">
              <a-input-number
                  v-model:value="currentOption.score"
                  :precision="2"
                  style="width: 100%"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item>
          <a-space>
            <a-button type="primary" @click="saveOption">保存</a-button>
            <a-button @click="cancelEdit">取消</a-button>
          </a-space>
        </a-form-item>
      </a-form>
    </div>

    <!-- 底部操作 -->
    <div class="footer">
      <a-space>
        <a-button @click="$emit('close')">关闭</a-button>
        <a-button type="primary" @click="saveAllOptions" :loading="saving">
          保存所有选项
        </a-button>
      </a-space>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { assessmentAPI } from '@/api/admin'

const props = defineProps({
  assessmentId: {
    type: String,
    required: true
  },
  questionId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close', 'updated'])

const options = ref([])
const editingIndex = ref(-1)
const saving = ref(false)
const loading = ref(false)

const currentOption = reactive({
  option_text: '',
  option_value: '',
  score: 0,
  option_order: 0
})

// 初始化选项数据
const initOptions = async () => {
  loading.value = true
  try {
    const response = await assessmentAPI.getOptions(props.assessmentId, props.questionId)
    if (response.success) {
      options.value = response.data || []
    }
  } catch (error) {
    message.error('获取选项列表失败')
    options.value = []
  } finally {
    loading.value = false
  }
}

// 添加选项
const addOption = () => {
  resetCurrentOption()
  currentOption.option_order = options.value.length
  editingIndex.value = options.value.length
}

// 编辑选项
const editOption = (item, index) => {
  Object.assign(currentOption, item)
  editingIndex.value = index
}

// 重置当前选项
const resetCurrentOption = () => {
  Object.assign(currentOption, {
    option_text: '',
    option_value: '',
    score: 0,
    option_order: 0
  })
}

// 保存选项
const saveOption = () => {
  if (!currentOption.option_text.trim()) {
    message.error('请输入选项内容')
    return
  }

  const option = { ...currentOption }
  
  if (editingIndex.value === options.value.length) {
    // 添加新选项
    options.value.push(option)
  } else {
    // 更新现有选项
    options.value[editingIndex.value] = option
  }

  cancelEdit()
  message.success('选项保存成功')
}

// 取消编辑
const cancelEdit = () => {
  editingIndex.value = -1
  resetCurrentOption()
}

// 删除选项
const deleteOption = (index) => {
  options.value.splice(index, 1)
  // 重新排序
  options.value.forEach((option, idx) => {
    option.option_order = idx
  })
  message.success('选项删除成功')
}

// 保存所有选项
const saveAllOptions = async () => {
  if (options.value.length === 0) {
    message.error('请至少添加一个选项')
    return
  }

  saving.value = true
  try {
    await assessmentAPI.saveOptions(props.assessmentId, props.questionId, options.value)
    message.success('所有选项保存成功')
    emit('updated')
    emit('close')
  } catch (error) {
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  initOptions()
})
</script>

<style lang="scss" scoped>
.option-manager {
  min-height: 300px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;

  .title {
    h4 {
      margin: 0;
      font-size: 16px;
    }
  }

  .subtitle {
    color: #8c8c8c;
    font-size: 12px;
    margin-left: 8px;
  }
}

.option-list {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 16px;
}

.option-title {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .order {
    font-weight: 600;
    color: #262626;
  }

  .score {
    color: #1890ff;
    font-size: 12px;
  }
}

.option-content {
  color: #595959;
  line-height: 1.4;
}

.option-form {
  background: #fafafa;
  padding: 16px;
  border-radius: 6px;
  margin-bottom: 16px;
}

.footer {
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  text-align: right;
}

:deep(.ant-list-item) {
  padding: 8px 0;
}

:deep(.ant-list-item-meta-title) {
  margin-bottom: 4px;
}

:deep(.ant-divider-inner-text) {
  font-size: 14px;
  font-weight: 500;
}
</style> 