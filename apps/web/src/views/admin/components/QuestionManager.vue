<template>
  <div class="question-manager">
    <div class="header">
      <div class="title">
        <h3>题目管理</h3>
        <span class="subtitle">测评ID: {{ assessmentId }}</span>
      </div>
      <a-button type="primary" @click="showAddModal">
        <template #icon>
          <PlusOutlined/>
        </template>
        添加题目
      </a-button>
    </div>

    <!-- 题目列表 -->
    <div class="question-list">
      <a-list
          :data-source="questions"
          :loading="loading"
      >
        <template #renderItem="{ item, index }">
          <a-list-item>
            <template #actions>
              <a @click="editQuestion(item)">编辑</a>
              <a @click="manageOptions(item)">选项管理</a>
              <a-popconfirm
                  title="确定删除这个题目吗？"
                  @confirm="deleteQuestion(item.id)"
                  ok-text="确定"
                  cancel-text="取消"
              >
                <a style="color: #ff4d4f">删除</a>
              </a-popconfirm>
            </template>

            <a-list-item-meta>
              <template #title>
                <div class="question-title">
                  <span class="order">题目 {{ index + 1 }}</span>
                  <a-tag :color="getQuestionTypeColor(item.question_type)">
                    {{ getQuestionTypeText(item.question_type) }}
                  </a-tag>
                  <a-tag v-if="item.dimension" color="blue">{{ item.dimension }}</a-tag>
                  <a-tag v-if="item.is_required" color="red">必答</a-tag>
                </div>
              </template>
              <template #description>
                <div class="question-content">
                  <div class="question-text">{{ item.question_text }}</div>
                  <div class="question-meta">
                    <span>权重: {{ item.score_weight }}</span>
                    <span>选项数: {{ item.options?.length || 0 }}</span>
                  </div>
                </div>
              </template>
            </a-list-item-meta>
          </a-list-item>
        </template>
      </a-list>
    </div>

    <!-- 添加/编辑题目模态框 -->
    <a-modal
        v-model:open="modalVisible"
        :title="modalTitle"
        :width="800"
        @ok="handleModalOk"
        @cancel="handleModalCancel"
        :confirm-loading="modalLoading"
    >
      <a-form
          ref="formRef"
          :model="form"
          :rules="rules"
          layout="vertical"
      >
        <a-form-item label="题目ID" name="id" v-if="!isEdit">
          <a-input v-model:value="form.id" placeholder="请输入题目ID" />
        </a-form-item>

        <a-form-item label="题目内容" name="question_text">
          <a-textarea v-model:value="form.question_text" placeholder="请输入题目内容" :rows="3" />
        </a-form-item>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="题目类型" name="question_type">
              <a-select v-model:value="form.question_type" placeholder="请选择题目类型">
                <a-select-option value="single">单选</a-select-option>
                <a-select-option value="multiple">多选</a-select-option>
                <a-select-option value="text">文本</a-select-option>
                <a-select-option value="scale">量表</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="题目序号" name="question_order">
              <a-input-number v-model:value="form.question_order" :min="0" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="分值权重" name="score_weight">
              <a-input-number v-model:value="form.score_weight" :min="0" :precision="2" style="width: 100%" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="维度标识" name="dimension">
              <a-input v-model:value="form.dimension" placeholder="如：焦虑、抑郁等" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item name="is_required">
              <a-checkbox v-model:checked="form.is_required">必答题</a-checkbox>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="题目说明" name="description">
          <a-textarea v-model:value="form.description" placeholder="请输入题目说明（可选）" :rows="2" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 选项管理模态框 -->
    <a-modal
        v-model:open="optionModalVisible"
        title="选项管理"
        :width="800"
        @cancel="handleOptionModalCancel"
        :footer="null"
    >
      <OptionManager
          v-if="optionModalVisible"
          :question-id="currentQuestionId"
          @close="handleOptionModalCancel"
          @updated="refreshQuestions"
      />
    </a-modal>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { assessmentAPI } from '@/api/admin'
import OptionManager from './OptionManager.vue'

export default {
  name: 'QuestionManager',
  components: {
    PlusOutlined,
    OptionManager
  },
  props: {
    assessmentId: {
      type: String,
      required: true
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const loading = ref(false)
    const questions = ref([])
    const modalVisible = ref(false)
    const modalLoading = ref(false)
    const optionModalVisible = ref(false)
    const currentQuestionId = ref('')
    const isEdit = ref(false)
    const formRef = ref()

    const form = reactive({
      id: '',
      question_text: '',
      question_type: 'single',
      question_order: 0,
      score_weight: 1.0,
      dimension: '',
      is_required: true,
      description: ''
    })

    const rules = {
      id: [
        { required: true, message: '请输入题目ID', trigger: 'blur' }
      ],
      question_text: [
        { required: true, message: '请输入题目内容', trigger: 'blur' }
      ],
      question_type: [
        { required: true, message: '请选择题目类型', trigger: 'change' }
      ]
    }

    const modalTitle = computed(() => {
      return isEdit.value ? '编辑题目' : '添加题目'
    })

    // 获取题目列表
    const fetchQuestions = async () => {
      loading.value = true
      try {
        const response = await assessmentAPI.getAssessment(props.assessmentId)
        if (response.success) {
          questions.value = response.data.questions || []
        }
      } catch (error) {
        message.error('获取题目列表失败')
      } finally {
        loading.value = false
      }
    }

    // 刷新题目列表
    const refreshQuestions = () => {
      fetchQuestions()
    }

    // 显示添加模态框
    const showAddModal = () => {
      isEdit.value = false
      resetForm()
      modalVisible.value = true
    }

    // 编辑题目
    const editQuestion = (record) => {
      isEdit.value = true
      Object.assign(form, record)
      modalVisible.value = true
    }

    // 管理选项
    const manageOptions = (record) => {
      currentQuestionId.value = record.id
      optionModalVisible.value = true
    }

    // 重置表单
    const resetForm = () => {
      Object.assign(form, {
        id: '',
        question_text: '',
        question_type: 'single',
        question_order: questions.value.length,
        score_weight: 1.0,
        dimension: '',
        is_required: true,
        description: ''
      })
      if (formRef.value) {
        formRef.value.resetFields()
      }
    }

    // 模态框确定
    const handleModalOk = async () => {
      try {
        await formRef.value.validateFields()
        modalLoading.value = true

        const data = {
          ...form,
          assessment_id: props.assessmentId
        }

        if (isEdit.value) {
          await assessmentAPI.updateQuestion(props.assessmentId, form.id, data)
          message.success('更新成功')
        } else {
          await assessmentAPI.createQuestion(props.assessmentId, data)
          message.success('创建成功')
        }

        modalVisible.value = false
        fetchQuestions()
      } catch (error) {
        message.error(isEdit.value ? '更新失败' : '创建失败')
      } finally {
        modalLoading.value = false
      }
    }

    // 模态框取消
    const handleModalCancel = () => {
      modalVisible.value = false
      resetForm()
    }

    // 选项管理模态框取消
    const handleOptionModalCancel = () => {
      optionModalVisible.value = false
      currentQuestionId.value = ''
    }

    // 删除题目
    const deleteQuestion = async (questionId) => {
      try {
        await assessmentAPI.deleteQuestion(props.assessmentId, questionId)
        message.success('删除成功')
        fetchQuestions()
      } catch (error) {
        message.error('删除失败')
      }
    }

    // 获取题目类型颜色
    const getQuestionTypeColor = (type) => {
      const colors = {
        single: 'blue',
        multiple: 'green',
        text: 'orange',
        scale: 'purple'
      }
      return colors[type] || 'default'
    }

    // 获取题目类型文本
    const getQuestionTypeText = (type) => {
      const texts = {
        single: '单选',
        multiple: '多选',
        text: '文本',
        scale: '量表'
      }
      return texts[type] || type
    }

    onMounted(() => {
      fetchQuestions()
    })

    return {
      loading,
      questions,
      modalVisible,
      modalLoading,
      optionModalVisible,
      currentQuestionId,
      isEdit,
      formRef,
      form,
      rules,
      modalTitle,
      
      fetchQuestions,
      refreshQuestions,
      showAddModal,
      editQuestion,
      manageOptions,
      resetForm,
      handleModalOk,
      handleModalCancel,
      handleOptionModalCancel,
      deleteQuestion,
      getQuestionTypeColor,
      getQuestionTypeText
    }
  }
}
</script>

<style scoped>
.question-manager {
  min-height: 400px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.title h3 {
  margin: 0;
  font-size: 18px;
}

.subtitle {
  color: #8c8c8c;
  font-size: 14px;
  margin-left: 12px;
}

.question-list {
  max-height: 500px;
  overflow-y: auto;
}

.question-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.order {
  font-weight: 600;
  color: #262626;
}

.question-content {
  line-height: 1.5;
}

.question-text {
  color: #595959;
  margin-bottom: 8px;
}

.question-meta {
  display: flex;
  gap: 16px;
  color: #8c8c8c;
  font-size: 12px;
}

:deep(.ant-list-item-meta-title) {
  margin-bottom: 8px;
}

:deep(.ant-list-item-action) {
  margin-left: 16px;
}
</style> 