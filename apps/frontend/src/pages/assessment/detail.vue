<template>
  <view class="container">
    <!-- 加载状态 -->
    <view v-if="loading" class="loading-container">
      <up-loading-page :loading="true" loading-text="加载中..."></up-loading-page>
    </view>

    <!-- 主要内容 -->
    <view v-else-if="assessment" class="content">
      <!-- 测评封面和基本信息 -->
      <view class="assessment-header">
        <image 
          class="cover-image" 
          :src="assessment.cover_image || '/static/images/default-assessment.png'" 
          mode="aspectFill"
          @error="onImageError"
        />
        <view class="header-overlay">
          <view class="assessment-info">
            <text class="assessment-title">{{ assessment.name }}</text>
            <text v-if="assessment.subtitle" class="assessment-subtitle">{{ assessment.subtitle }}</text>
            
            <view class="assessment-meta">
              <view class="meta-item">
                <up-icon name="clock" size="14" color="#fff"></up-icon>
                <text>{{ assessment.duration || 30 }}分钟</text>
              </view>
              <view class="meta-item">
                <up-icon name="file-text" size="14" color="#fff"></up-icon>
                <text>{{ assessment.question_count || 0 }}题</text>
              </view>
              <view class="meta-item">
                <up-icon name="account" size="14" color="#fff"></up-icon>
                <text>{{ formatParticipantCount(assessment.participant_count) }}人已测</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 测评统计 -->
      <view class="stats-section">
        <view class="stats-grid">
          <view class="stat-item">
            <text class="stat-number">{{ formatParticipantCount(assessment.participant_count) }}</text>
            <text class="stat-label">参与人数</text>
          </view>
          <view class="stat-item">
            <text class="stat-number">{{ assessment.rating || 4.8 }}</text>
            <text class="stat-label">评分</text>
          </view>
          <view class="stat-item">
            <text class="stat-number">{{ getDifficultyText(assessment.difficulty) }}</text>
            <text class="stat-label">难度</text>
          </view>
          <view class="stat-item">
            <text class="stat-number">{{ formatPrice(assessment.price) }}</text>
            <text class="stat-label">价格</text>
          </view>
        </view>
      </view>

      <!-- 测评描述 -->
      <view v-if="assessment.description" class="section">
        <view class="section-title">测评介绍</view>
        <view class="description-content">
          <text class="description-text">{{ assessment.description }}</text>
        </view>
      </view>

      <!-- 测评说明 -->
      <view v-if="assessment.instructions" class="section">
        <view class="section-title">测评说明</view>
        <view class="instructions-content">
          <text class="instructions-text">{{ assessment.instructions }}</text>
        </view>
      </view>

      <!-- 题目预览 -->
      <view v-if="questions.length > 0" class="section">
        <view class="section-title">
          <text>题目预览</text>
          <text class="question-count">(共{{ questions.length }}题)</text>
        </view>
        <view class="questions-preview">
          <view 
            v-for="(question, index) in previewQuestions" 
            :key="question.id"
            class="question-preview-item"
          >
            <view class="question-header">
              <text class="question-number">{{ index + 1 }}.</text>
              <view class="question-type-tag">
                <text class="question-type-text">{{ getQuestionTypeText(question.question_type) }}</text>
              </view>
            </view>
            <text class="question-text">{{ question.question_text }}</text>
          </view>
          
          <view v-if="questions.length > 3" class="more-questions" @click="showAllQuestions">
            <text class="more-text">查看全部 {{ questions.length }} 道题目</text>
            <up-icon name="arrow-right" size="14" color="#52c41a"></up-icon>
          </view>
        </view>
      </view>

      <!-- 测评记录 -->
      <view v-if="userRecords.length > 0" class="section">
        <view class="section-title">我的测评记录</view>
        <view class="records-list">
          <view 
            v-for="record in userRecords" 
            :key="record.id"
            class="record-item"
            @click="viewRecord(record)"
          >
            <view class="record-info">
              <text class="record-date">{{ formatDate(record.create_time) }}</text>
              <text class="record-status">{{ getRecordStatusText(record.status) }}</text>
            </view>
            <view class="record-score" v-if="record.status === 'completed'">
              <text class="score-text">{{ record.total_score || 0 }}分</text>
            </view>
            <up-icon name="arrow-right" size="14" color="#999"></up-icon>
          </view>
        </view>
      </view>

      <!-- 相关推荐 -->
      <view v-if="relatedAssessments.length > 0" class="section">
        <view class="section-title">相关推荐</view>
        <view class="related-list">
          <view 
            v-for="item in relatedAssessments" 
            :key="item.id"
            class="related-item"
            @click="goToAssessment(item.id)"
          >
            <image 
              class="related-cover" 
              :src="item.cover_image || '/static/images/default-assessment.png'" 
              mode="aspectFill"
            />
            <view class="related-info">
              <text class="related-title">{{ item.name }}</text>
              <text class="related-meta">{{ formatParticipantCount(item.participant_count) }}人已测</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 错误状态 -->
    <view v-else-if="error" class="error-container">
      <up-empty 
        text="测评信息加载失败"
        icon="https://cdn.uviewui.com/uview/empty/error.png"
        iconSize="120"
        textSize="16"
        textColor="#999999"
        marginTop="100"
      >
        <template #button>
          <up-button
            text="重新加载"
            type="primary"
            size="normal"
            @click="fetchAssessmentDetail"
            :customStyle="{
              marginTop: '30rpx',
              width: '200rpx',
              borderRadius: '22rpx',
              background: '#52c41a'
            }"
          ></up-button>
        </template>
      </up-empty>
    </view>

    <!-- 底部操作栏 -->
    <view v-if="assessment && !loading" class="bottom-bar">
      <view class="price-info">
        <text v-if="assessment.price > 0" class="current-price">¥{{ assessment.price }}</text>
        <text v-else class="free-price">免费</text>
        <text v-if="assessment.original_price && assessment.original_price > assessment.price" class="original-price">¥{{ assessment.original_price }}</text>
      </view>
      <view class="action-buttons">
        <up-button
          v-if="hasInProgressRecord"
          text="继续测评"
          type="warning"
          size="normal"
          @click="continueAssessment"
          :customStyle="{
            width: '160rpx',
            borderRadius: '22rpx',
            marginRight: '20rpx'
          }"
        ></up-button>
        <up-button
          :text="assessment.price > 0 ? '立即购买' : '开始测评'"
          type="primary"
          size="normal"
          @click="startAssessment"
          :loading="startLoading"
          :customStyle="{
            width: assessment.price > 0 ? '160rpx' : '200rpx',
            borderRadius: '22rpx',
            background: '#52c41a'
          }"
        ></up-button>
      </view>
    </view>

    <!-- 全部题目弹窗 -->
    <up-popup v-model:show="questionsModalVisible" mode="bottom" :round="10">
      <view class="questions-modal">
        <view class="modal-header">
          <text class="modal-title">全部题目 ({{ questions.length }}题)</text>
          <up-icon name="close" size="20" color="#999" @click="questionsModalVisible = false"></up-icon>
        </view>
        <scroll-view class="questions-scroll" scroll-y :style="{ height: '60vh' }">
          <view 
            v-for="(question, index) in questions" 
            :key="question.id"
            class="modal-question-item"
          >
            <view class="modal-question-header">
              <text class="modal-question-number">{{ index + 1 }}.</text>
              <view class="modal-question-type-tag">
                <text class="modal-question-type-text">{{ getQuestionTypeText(question.question_type) }}</text>
              </view>
            </view>
            <text class="modal-question-text">{{ question.question_text }}</text>
          </view>
        </scroll-view>
      </view>
    </up-popup>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { assessmentAPI } from '@/api/assessment'

// 页面参数
const assessmentId = ref('')

// 数据状态
const loading = ref(true)
const error = ref(false)
const startLoading = ref(false)
const assessment = ref(null)
const questions = ref([])
const userRecords = ref([])
const relatedAssessments = ref([])

// UI状态
const questionsModalVisible = ref(false)

// 计算属性
const previewQuestions = computed(() => {
  return questions.value.slice(0, 3)
})

const hasInProgressRecord = computed(() => {
  return userRecords.value.some(record => record.status === 'in_progress')
})

// 获取测评详情
const fetchAssessmentDetail = async () => {
  if (!assessmentId.value) {
    error.value = true
    loading.value = false
    return
  }

  loading.value = true
  error.value = false

  try {
    const res = await assessmentAPI.getAssessment(assessmentId.value)
    console.log('测评详情API响应:', res)

    if (res.success && res.data) {
      assessment.value = {
        ...res.data,
        participant_count: parseInt(res.data.participant_count) || 0,
        price: parseFloat(res.data.price) || 0,
        original_price: parseFloat(res.data.original_price) || 0,
        duration: parseInt(res.data.duration) || 30,
        question_count: parseInt(res.data.question_count) || 0,
        rating: parseFloat(res.data.rating) || 4.8
      }
      
      questions.value = res.data.questions || []
      
      // 获取用户测评记录
      await fetchUserRecords()
      
      // 获取相关推荐
      await fetchRelatedAssessments()
    } else {
      error.value = true
    }
  } catch (err) {
    console.error('获取测评详情失败:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

// 获取用户测评记录
const fetchUserRecords = async () => {
  try {
    const res = await assessmentAPI.getRecords({
      assessment_id: assessmentId.value,
      page: 1,
      per_page: 5
    })
    
    if (res.success && res.data) {
      userRecords.value = res.data.list || []
    }
  } catch (err) {
    console.error('获取用户记录失败:', err)
  }
}

// 获取相关推荐
const fetchRelatedAssessments = async () => {
  try {
    const res = await assessmentAPI.getAssessments({
      category: assessment.value?.category,
      status: 'published',
      page: 1,
      per_page: 4
    })
    
    if (res.success && res.data) {
      // 过滤掉当前测评
      relatedAssessments.value = (res.data.list || [])
        .filter(item => item.id !== assessmentId.value)
        .slice(0, 3)
    }
  } catch (err) {
    console.error('获取相关推荐失败:', err)
  }
}

// 开始测评
const startAssessment = async () => {
  if (!assessment.value) return

  // 如果是付费测评，跳转到支付页面
  if (assessment.value.price > 0) {
    uni.showModal({
      title: '付费测评',
      content: `此测评需要支付 ¥${assessment.value.price} 元，是否继续？`,
      success: (res) => {
        if (res.confirm) {
          // TODO: 跳转到支付页面
          uni.showToast({
            title: '跳转支付页面',
            icon: 'none'
          })
        }
      }
    })
    return
  }

  startLoading.value = true

  try {
    const res = await assessmentAPI.startAssessment({
      assessment_id: assessmentId.value,
      is_anonymous: false
    })

    if (res.success && res.data) {
      // 跳转到测评答题页面
      uni.navigateTo({
        url: `/pages/assessment/test?recordId=${res.data.id}&assessmentId=${assessmentId.value}`
      })
    } else {
      uni.showToast({
        title: res.message || '开始测评失败',
        icon: 'none'
      })
    }
  } catch (err) {
    console.error('开始测评失败:', err)
    uni.showToast({
      title: '开始测评失败，请稍后重试',
      icon: 'none'
    })
  } finally {
    startLoading.value = false
  }
}

// 继续测评
const continueAssessment = () => {
  const inProgressRecord = userRecords.value.find(record => record.status === 'in_progress')
  if (inProgressRecord) {
    uni.navigateTo({
      url: `/pages/assessment/test?recordId=${inProgressRecord.id}&assessmentId=${assessmentId.value}`
    })
  }
}

// 查看测评记录
const viewRecord = (record) => {
  uni.navigateTo({
    url: `/pages/assessment/result?recordId=${record.id}`
  })
}

// 跳转到其他测评
const goToAssessment = (id) => {
  uni.navigateTo({
    url: `/pages/assessment/detail?id=${id}`
  })
}

// 显示全部题目
const showAllQuestions = () => {
  questionsModalVisible.value = true
}

// 工具函数
const formatParticipantCount = (count) => {
  if (!count) return '0'
  const num = parseInt(count)
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toString()
}

const formatPrice = (price) => {
  if (price === 0 || price === null || price === undefined) {
    return '免费'
  }
  return `¥${price}`
}

const getDifficultyText = (difficulty) => {
  switch (difficulty) {
    case 'easy': return '简单'
    case 'medium': return '中等'
    case 'hard': return '困难'
    default: return '中等'
  }
}

const getQuestionTypeText = (type) => {
  switch (type) {
    case 'single': return '单选'
    case 'multiple': return '多选'
    case 'text': return '文本'
    case 'scale': return '量表'
    default: return '单选'
  }
}

const getRecordStatusText = (status) => {
  switch (status) {
    case 'in_progress': return '进行中'
    case 'completed': return '已完成'
    case 'expired': return '已过期'
    default: return '未知'
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const onImageError = () => {
  console.error('Assessment cover image failed to load')
}

// 页面加载
onLoad((options) => {
  if (options.id) {
    assessmentId.value = options.id
    fetchAssessmentDetail()
  } else {
    error.value = true
    loading.value = false
  }
})
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 120rpx; // 为底部操作栏留出空间
}

.loading-container, .error-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

// 测评头部
.assessment-header {
  position: relative;
  height: 400rpx;
  overflow: hidden;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.header-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  padding: 40rpx 30rpx 30rpx;
}

.assessment-info {
  color: white;
}

.assessment-title {
  font-size: 36rpx;
  font-weight: bold;
  line-height: 1.4;
  margin-bottom: 10rpx;
  display: block;
}

.assessment-subtitle {
  font-size: 28rpx;
  opacity: 0.9;
  line-height: 1.4;
  margin-bottom: 20rpx;
  display: block;
}

.assessment-meta {
  display: flex;
  gap: 30rpx;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  font-size: 24rpx;
  opacity: 0.9;
}

// 统计数据
.stats-section {
  background: white;
  margin: 20rpx;
  border-radius: 12rpx;
  padding: 30rpx;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20rpx;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 32rpx;
  font-weight: bold;
  color: #52c41a;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #999;
}

// 通用区块
.section {
  background: white;
  margin: 20rpx;
  border-radius: 12rpx;
  padding: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.question-count {
  font-size: 24rpx;
  color: #999;
  font-weight: normal;
}

// 描述内容
.description-content, .instructions-content {
  line-height: 1.6;
}

.description-text, .instructions-text {
  font-size: 28rpx;
  color: #666;
}

// 题目预览
.questions-preview {
  .question-preview-item {
    padding: 20rpx 0;
    border-bottom: 1rpx solid #f0f0f0;
    
    &:last-child {
      border-bottom: none;
    }
  }
}

.question-header {
  display: flex;
  align-items: center;
  gap: 15rpx;
  margin-bottom: 10rpx;
}

.question-number {
  font-size: 28rpx;
  font-weight: bold;
  color: #52c41a;
  min-width: 40rpx;
}

.question-type-tag {
  background: #f6ffed;
  border: 1rpx solid #b7eb8f;
  border-radius: 6rpx;
  padding: 4rpx 12rpx;
}

.question-type-text {
  font-size: 20rpx;
  color: #52c41a;
}

.question-text {
  font-size: 28rpx;
  color: #333;
  line-height: 1.5;
}

.more-questions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  padding: 30rpx 0 10rpx;
  color: #52c41a;
}

.more-text {
  font-size: 28rpx;
}

// 测评记录
.records-list {
  .record-item {
    display: flex;
    align-items: center;
    padding: 24rpx 0;
    border-bottom: 1rpx solid #f0f0f0;
    
    &:last-child {
      border-bottom: none;
    }
  }
}

.record-info {
  flex: 1;
}

.record-date {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 6rpx;
  display: block;
}

.record-status {
  font-size: 24rpx;
  color: #999;
}

.record-score {
  margin-right: 20rpx;
}

.score-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #52c41a;
}

// 相关推荐
.related-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.related-item {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.related-cover {
  width: 120rpx;
  height: 80rpx;
  border-radius: 8rpx;
  object-fit: cover;
}

.related-info {
  flex: 1;
}

.related-title {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 6rpx;
  display: block;
}

.related-meta {
  font-size: 24rpx;
  color: #999;
}

// 底部操作栏
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 20rpx 30rpx;
  border-top: 1rpx solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 100;
}

.price-info {
  display: flex;
  align-items: baseline;
  gap: 10rpx;
}

.current-price, .free-price {
  font-size: 36rpx;
  font-weight: bold;
  color: #ff6b35;
}

.free-price {
  color: #52c41a;
}

.original-price {
  font-size: 24rpx;
  color: #999;
  text-decoration: line-through;
}

.action-buttons {
  display: flex;
  align-items: center;
}

// 题目弹窗
.questions-modal {
  background: white;
  border-radius: 20rpx 20rpx 0 0;
  max-height: 80vh;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.modal-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.questions-scroll {
  padding: 20rpx 30rpx;
}

.modal-question-item {
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f8f8f8;
  
  &:last-child {
    border-bottom: none;
  }
}

.modal-question-header {
  display: flex;
  align-items: center;
  gap: 15rpx;
  margin-bottom: 10rpx;
}

.modal-question-number {
  font-size: 28rpx;
  font-weight: bold;
  color: #52c41a;
  min-width: 40rpx;
}

.modal-question-type-tag {
  background: #f6ffed;
  border: 1rpx solid #b7eb8f;
  border-radius: 6rpx;
  padding: 4rpx 12rpx;
}

.modal-question-type-text {
  font-size: 20rpx;
  color: #52c41a;
}

.modal-question-text {
  font-size: 28rpx;
  color: #333;
  line-height: 1.5;
}
</style>
