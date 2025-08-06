/**
 * 测评相关API接口
 */
import { request } from '@/utils/request'

// 测评管理API
export const assessmentAPI = {
  // 获取测评列表
  getAssessments: (params) => {
    return request({
      url: '/assessment',
      method: 'get',
      params
    })
  },

  // 获取测评详情
  getAssessment: (assessmentId) => {
    return request({
      url: `/assessment/${assessmentId}`,
      method: 'get'
    })
  },

  // 创建测评
  createAssessment: (data) => {
    return request({
      url: '/assessment',
      method: 'post',
      data
    })
  },

  // 更新测评
  updateAssessment: (assessmentId, data) => {
    return request({
      url: `/assessment/${assessmentId}`,
      method: 'put',
      data
    })
  },

  // 删除测评
  deleteAssessment: (assessmentId) => {
    return request({
      url: `/assessment/${assessmentId}`,
      method: 'delete'
    })
  },

  // 创建测评题目
  createQuestion: (assessmentId, data) => {
    return request({
      url: `/assessment/${assessmentId}/questions`,
      method: 'post',
      data
    })
  },

  // 更新测评题目
  updateQuestion: (assessmentId, questionId, data) => {
    return request({
      url: `/assessment/${assessmentId}/questions/${questionId}`,
      method: 'put',
      data
    })
  },

  // 删除测评题目
  deleteQuestion: (assessmentId, questionId) => {
    return request({
      url: `/assessment/${assessmentId}/questions/${questionId}`,
      method: 'delete'
    })
  },

  // 获取题目选项列表
  getOptions: (assessmentId, questionId) => {
    return request({
      url: `/assessment/${assessmentId}/questions/${questionId}/options`,
      method: 'get'
    })
  },

  // 批量保存题目选项
  saveOptions: (assessmentId, questionId, options) => {
    return request({
      url: `/assessment/${assessmentId}/questions/${questionId}/options`,
      method: 'post',
      data: options
    })
  },

  // 删除选项
  deleteOption: (assessmentId, questionId, optionId) => {
    return request({
      url: `/assessment/${assessmentId}/questions/${questionId}/options/${optionId}`,
      method: 'delete'
    })
  },

  // 开始测评
  startAssessment: (data) => {
    return request({
      url: '/assessment/start',
      method: 'post',
      data
    })
  },

  // 提交测评
  submitAssessment: (data) => {
    return request({
      url: '/assessment/submit',
      method: 'post',
      data
    })
  },

  // 获取测评记录列表
  getRecords: (params) => {
    return request({
      url: '/assessment/records',
      method: 'get',
      params
    })
  },

  // 获取测评记录详情
  getRecord: (recordId) => {
    return request({
      url: `/assessment/records/${recordId}`,
      method: 'get'
    })
  }
}

// 测评查询参数构建器
export class AssessmentQueryBuilder {
  constructor() {
    this.params = {
      page: 1,
      per_page: 10
    }
  }

  // 设置分页
  page(page, perPage = 10) {
    this.params.page = page
    this.params.per_page = perPage
    return this
  }

  // 按名称搜索
  name(name) {
    if (name) {
      this.params.name = name
    }
    return this
  }

  // 按分类筛选
  category(category) {
    if (category) {
      this.params.category = category
    }
    return this
  }

  // 按难度筛选
  difficulty(difficulty) {
    if (difficulty) {
      this.params.difficulty = difficulty
    }
    return this
  }

  // 按状态筛选
  status(status) {
    if (status) {
      this.params.status = status
    }
    return this
  }

  // 是否免费
  free(isFree) {
    if (typeof isFree === 'boolean') {
      this.params.is_free = isFree
    }
    return this
  }

  // 关键词搜索
  keyword(keyword) {
    if (keyword) {
      this.params.keyword = keyword
    }
    return this
  }

  // 排序
  sort(sortBy, sortOrder = 'asc') {
    this.params.sort_by = sortBy
    this.params.sort_order = sortOrder
    return this
  }

  // 构建查询参数
  build() {
    return { ...this.params }
  }

  // 执行查询
  async execute() {
    return assessmentAPI.getAssessments(this.build())
  }
}

// 测评记录查询参数构建器
export class AssessmentRecordQueryBuilder {
  constructor() {
    this.params = {
      page: 1,
      per_page: 10
    }
  }

  // 设置分页
  page(page, perPage = 10) {
    this.params.page = page
    this.params.per_page = perPage
    return this
  }

  // 按用户ID筛选
  userId(userId) {
    if (userId) {
      this.params.user_id = userId
    }
    return this
  }

  // 按测评ID筛选
  assessmentId(assessmentId) {
    if (assessmentId) {
      this.params.assessment_id = assessmentId
    }
    return this
  }

  // 按状态筛选
  status(status) {
    if (status) {
      this.params.status = status
    }
    return this
  }

  // 日期范围
  dateRange(startDate, endDate) {
    if (startDate) {
      this.params.start_date = startDate
    }
    if (endDate) {
      this.params.end_date = endDate
    }
    return this
  }

  // 排序
  sort(sortBy, sortOrder = 'desc') {
    this.params.sort_by = sortBy
    this.params.sort_order = sortOrder
    return this
  }

  // 构建查询参数
  build() {
    return { ...this.params }
  }

  // 执行查询
  async execute() {
    return assessmentAPI.getRecords(this.build())
  }
}

// 测评表单数据构建器
export class AssessmentFormBuilder {
  constructor() {
    this.data = {
      name: '',
      subtitle: '',
      description: '',
      cover_image: '',
      price: 0,
      original_price: 0,
      duration: 30,
      difficulty: 'medium',
      category: '',
      status: 'draft',
      tags: '',
      instructions: '',
      is_free: true,
      sort_order: 0
    }
  }

  // 基本信息
  basicInfo(name, subtitle = '', description = '') {
    this.data.name = name
    this.data.subtitle = subtitle
    this.data.description = description
    return this
  }

  // 封面图片
  cover(coverImage) {
    this.data.cover_image = coverImage
    return this
  }

  // 价格信息
  pricing(price, originalPrice = null) {
    this.data.price = price
    this.data.original_price = originalPrice || price
    this.data.is_free = price === 0
    return this
  }

  // 测评设置
  settings(duration, difficulty = 'medium', category = '') {
    this.data.duration = duration
    this.data.difficulty = difficulty
    this.data.category = category
    return this
  }

  // 状态
  status(status) {
    this.data.status = status
    return this
  }

  // 标签
  tags(tags) {
    if (Array.isArray(tags)) {
      this.data.tags = tags.join(',')
    } else {
      this.data.tags = tags
    }
    return this
  }

  // 说明
  instructions(instructions) {
    this.data.instructions = instructions
    return this
  }

  // 排序
  sortOrder(order) {
    this.data.sort_order = order
    return this
  }

  // 构建表单数据
  build() {
    return { ...this.data }
  }
}

// 题目表单数据构建器
export class QuestionFormBuilder {
  constructor() {
    this.data = {
      question_text: '',
      question_type: 'single',
      question_order: 0,
      is_required: true,
      score_weight: 1.0,
      dimension: '',
      description: ''
    }
  }

  // 题目内容
  text(questionText) {
    this.data.question_text = questionText
    return this
  }

  // 题目类型
  type(questionType) {
    this.data.question_type = questionType
    return this
  }

  // 题目序号
  order(order) {
    this.data.question_order = order
    return this
  }

  // 是否必答
  required(isRequired = true) {
    this.data.is_required = isRequired
    return this
  }

  // 分值权重
  weight(weight) {
    this.data.score_weight = weight
    return this
  }

  // 维度标识
  dimension(dimension) {
    this.data.dimension = dimension
    return this
  }

  // 题目说明
  description(description) {
    this.data.description = description
    return this
  }

  // 构建表单数据
  build() {
    return { ...this.data }
  }
}

// 常量定义
export const ASSESSMENT_STATUS = {
  DRAFT: 'draft',
  PUBLISHED: 'published',
  ARCHIVED: 'archived'
}

export const ASSESSMENT_DIFFICULTY = {
  EASY: 'easy',
  MEDIUM: 'medium',
  HARD: 'hard'
}

export const QUESTION_TYPE = {
  SINGLE: 'single',
  MULTIPLE: 'multiple',
  TEXT: 'text',
  SCALE: 'scale'
}

export const RECORD_STATUS = {
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  EXPIRED: 'expired'
}

// 工具函数
export const assessmentUtils = {
  // 获取状态文本
  getStatusText(status) {
    const statusMap = {
      [ASSESSMENT_STATUS.DRAFT]: '草稿',
      [ASSESSMENT_STATUS.PUBLISHED]: '已发布',
      [ASSESSMENT_STATUS.ARCHIVED]: '已归档'
    }
    return statusMap[status] || status
  },

  // 获取难度文本
  getDifficultyText(difficulty) {
    const difficultyMap = {
      [ASSESSMENT_DIFFICULTY.EASY]: '简单',
      [ASSESSMENT_DIFFICULTY.MEDIUM]: '中等',
      [ASSESSMENT_DIFFICULTY.HARD]: '困难'
    }
    return difficultyMap[difficulty] || difficulty
  },

  // 获取题目类型文本
  getQuestionTypeText(type) {
    const typeMap = {
      [QUESTION_TYPE.SINGLE]: '单选',
      [QUESTION_TYPE.MULTIPLE]: '多选',
      [QUESTION_TYPE.TEXT]: '文本',
      [QUESTION_TYPE.SCALE]: '量表'
    }
    return typeMap[type] || type
  },

  // 获取记录状态文本
  getRecordStatusText(status) {
    const statusMap = {
      [RECORD_STATUS.IN_PROGRESS]: '进行中',
      [RECORD_STATUS.COMPLETED]: '已完成',
      [RECORD_STATUS.EXPIRED]: '已过期'
    }
    return statusMap[status] || status
  },

  // 格式化价格
  formatPrice(price) {
    if (price === 0 || price === null || price === undefined) {
      return '免费'
    }
    return `¥${price.toFixed(2)}`
  },

  // 格式化时长
  formatDuration(duration) {
    if (!duration) return '未设置'
    return `${duration}分钟`
  }
}

export default assessmentAPI
