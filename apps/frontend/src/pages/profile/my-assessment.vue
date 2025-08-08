<template>
  <view class="container">
    <Navbar
      title="我的测评"
      :showLeft="true"
      :showRight="false"
      @leftClick="goBack"
    />
    
    <!-- 标签栏 -->
    <view class="tabs">
      <view 
        v-for="(tab, index) in tabs" 
        :key="index"
        class="tab"
        :class="{ active: activeTab === index }"
        @click="switchTab(index)"
      >
        {{ tab.name }}
      </view>
    </view>
    
    <!-- 测评列表 -->
    <view class="assessment-list" v-if="filteredAssessments.length > 0">
      <view 
        v-for="(assessment, index) in filteredAssessments" 
        :key="index"
        class="assessment-card"
      >
        <!-- 状态栏 -->
        <view class="assessment-status" :class="getStatusClass(assessment.status)">
          <text>{{ getStatusText(assessment.status) }}</text>
          <text>{{ getStatusSubtext(assessment) }}</text>
        </view>
        
        <!-- 内容区域 -->
        <view class="assessment-content">
          <image 
            :src="assessment.image || '/static/images/default-assessment.png'" 
            class="assessment-image"
            mode="aspectFill"
          />
          <view class="assessment-info">
            <view class="assessment-name">{{ assessment.name }}</view>
            <view class="assessment-description">{{ assessment.description }}</view>
            <view class="assessment-time">{{ getTimeText(assessment) }}</view>
            <view class="assessment-actions">
              <view 
                class="action-button secondary-button" 
                @click="viewDetails(assessment)"
              >
                查看详情
              </view>
              <view 
                class="action-button primary-button" 
                @click="handlePrimaryAction(assessment)"
              >
                {{ getPrimaryActionText(assessment.status) }}
              </view>
            </view>
          </view>
        </view>
        
        <!-- 结果摘要（仅已完成的测评显示） -->
        <view v-if="assessment.status === 'completed' && assessment.result" class="result-summary">
          <view class="result-item">
            <text class="result-label">测评结果：</text>
            <text class="result-value" :class="getResultClass(assessment.result.level)">
              {{ assessment.result.text }}
            </text>
          </view>
          <view class="result-item">
            <text class="result-label">建议：</text>
            <text>{{ assessment.result.suggestion }}</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 空状态 -->
    <view v-else class="empty-state">
      <view class="empty-icon">
        <text style="font-size: 32px;">📋</text>
      </view>
      <view class="empty-text">{{ getEmptyText() }}</view>
      <view class="empty-button" @click="goToAssessment">
        去测评
      </view>
    </view>
    
    <!-- 底部空间 -->
    <view style="height: 40rpx;"></view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/store/user'
import SvgIcon from '@/components/SvgIcon.vue'
import Navbar from '@/components/Navbar.vue'

const userStore = useUserStore()

// 当前激活的标签
const activeTab = ref(0)

// 标签数据
const tabs = ref([
  { name: '全部', value: 'all' },
  { name: '已完成', value: 'completed' },
  { name: '进行中', value: 'inprogress' }
])

// 模拟测评数据
const assessments = ref([
  {
    id: 1,
    name: '抑郁症筛查量表（PHQ-9）',
    description: 'PHQ-9是一种常用的抑郁症筛查工具，通过9个问题评估过去两周内的抑郁症状。',
    image: '/static/images/assessment-phq9.png',
    status: 'completed',
    completedTime: '2023年6月15日',
    duration: '4分钟',
    result: {
      text: '轻度抑郁（9分）',
      level: 'medium',
      suggestion: '建议进行心理咨询，学习情绪管理技巧'
    }
  },
  {
    id: 2,
    name: '广泛性焦虑障碍量表（GAD-7）',
    description: 'GAD-7是一种简短的自评量表，用于评估广泛性焦虑障碍的症状严重程度。',
    image: '/static/images/assessment-gad7.png',
    status: 'inprogress',
    startTime: '2023年6月20日',
    progress: {
      completed: 3,
      total: 7
    }
  },
  {
    id: 3,
    name: '大五人格测试（Big Five）',
    description: '大五人格测试是一种广泛应用的人格评估工具，从五个维度评估您的性格特点。',
    image: '/static/images/assessment-bigfive.png',
    status: 'expired',
    startTime: '2023年5月8日',
    expiredTime: '2023年5月10日'
  }
])

// 过滤后的测评列表
const filteredAssessments = computed(() => {
  const currentTab = tabs.value[activeTab.value]
  if (currentTab.value === 'all') {
    return assessments.value
  }
  return assessments.value.filter(assessment => assessment.status === currentTab.value)
})

// 返回上一页
const goBack = () => {
  uni.navigateBack()
}

// 切换标签
const switchTab = (index) => {
  activeTab.value = index
}

// 获取状态样式类
const getStatusClass = (status) => {
  const statusMap = {
    'completed': 'status-completed',
    'inprogress': 'status-inprogress',
    'expired': 'status-expired'
  }
  return statusMap[status] || ''
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'completed': '已完成',
    'inprogress': '进行中',
    'expired': '已过期'
  }
  return statusMap[status] || ''
}

// 获取状态副文本
const getStatusSubtext = (assessment) => {
  switch (assessment.status) {
    case 'completed':
      return assessment.completedTime
    case 'inprogress':
      return `已完成 ${assessment.progress.completed}/${assessment.progress.total} 题`
    case 'expired':
      return assessment.expiredTime
    default:
      return ''
  }
}

// 获取时间文本
const getTimeText = (assessment) => {
  switch (assessment.status) {
    case 'completed':
      return `测评用时：${assessment.duration}`
    case 'inprogress':
      return `开始时间：${assessment.startTime}`
    case 'expired':
      return `开始时间：${assessment.startTime}`
    default:
      return ''
  }
}

// 获取主要操作按钮文本
const getPrimaryActionText = (status) => {
  const actionMap = {
    'completed': '查看报告',
    'inprogress': '继续测评',
    'expired': '重新测评'
  }
  return actionMap[status] || '开始测评'
}

// 获取结果等级样式类
const getResultClass = (level) => {
  return `result-${level}`
}

// 获取空状态文本
const getEmptyText = () => {
  const currentTab = tabs.value[activeTab.value]
  const textMap = {
    'all': '您还没有测评记录',
    'completed': '您还没有已完成的测评',
    'inprogress': '您没有进行中的测评'
  }
  return textMap[currentTab.value] || '暂无数据'
}

// 查看详情
const viewDetails = (assessment) => {
  uni.navigateTo({
    url: `/pages/assessment/detail?id=${assessment.id}`
  })
}

// 处理主要操作
const handlePrimaryAction = (assessment) => {
  switch (assessment.status) {
    case 'completed':
      // 查看报告
      uni.navigateTo({
        url: `/pages/assessment/report?id=${assessment.id}`
      })
      break
    case 'inprogress':
      // 继续测评
      uni.navigateTo({
        url: `/pages/assessment/take?id=${assessment.id}`
      })
      break
    case 'expired':
      // 重新测评
      goToAssessment()
      break
    default:
      break
  }
}

// 去测评
const goToAssessment = () => {
  uni.navigateTo({
    url: '/pages/assessment/index'
  })
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  color: #333;
}

.tabs {
  display: flex;
  background-color: #fff;
  border-bottom: 1rpx solid #f0f0f0;

  .tab {
    flex: 1;
    text-align: center;
    padding: 24rpx 0;
    font-size: 28rpx;
    color: #666;
    position: relative;
    transition: color 0.3s;

    &.active {
      color: #4A90E2;
      font-weight: bold;

      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 40rpx;
        height: 6rpx;
        background-color: #4A90E2;
        border-radius: 3rpx;
      }
    }
  }
}

.assessment-list {
  padding: 30rpx;

  .assessment-card {
    margin-bottom: 30rpx;
    border-radius: 16rpx;
    background-color: #fff;
    box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.05);
    overflow: hidden;

    .assessment-status {
      padding: 16rpx 30rpx;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 24rpx;

      &.status-completed {
        background-color: #f6ffed;
        color: #52c41a;
      }

      &.status-inprogress {
        background-color: #e6f7ff;
        color: #4A90E2;
      }

      &.status-expired {
        background-color: #f5f5f5;
        color: #999;
      }
    }
  }
}

      .assessment-content {
        padding: 30rpx;
        display: flex;

        .assessment-image {
          width: 160rpx;
          height: 160rpx;
          border-radius: 8rpx;
          margin-right: 24rpx;
          background-color: #f5f5f5;
        }

        .assessment-info {
          flex: 1;

          .assessment-name {
            font-size: 32rpx;
            font-weight: bold;
            margin-bottom: 12rpx;
            color: #333;
          }

          .assessment-description {
            font-size: 24rpx;
            color: #666;
            margin-bottom: 16rpx;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
          }

          .assessment-time {
            font-size: 24rpx;
            color: #999;
            margin-bottom: 16rpx;
          }

          .assessment-actions {
            display: flex;
            justify-content: flex-end;
          }
        }
      }

            .action-button {
              padding: 12rpx 24rpx;
              font-size: 24rpx;
              border-radius: 8rpx;
              margin-left: 16rpx;
              transition: all 0.2s;

              &.primary-button {
                background-color: #4A90E2;
                color: #fff;

                &:active {
                  background-color: #357abd;
                }
              }

              &.secondary-button {
                background-color: #f5f5f5;
                color: #666;

                &:active {
                  background-color: #e8e8e8;
                }
              }
            }

      .result-summary {
        padding: 24rpx 30rpx;
        border-top: 1rpx solid #f0f0f0;
        font-size: 24rpx;
        color: #666;

        .result-item {
          display: flex;
          justify-content: space-between;
          margin-bottom: 8rpx;

          &:last-child {
            margin-bottom: 0;
          }

          .result-label {
            color: #999;
          }

          .result-value {
            font-weight: bold;

            &.result-high {
              color: #ff4d4f;
            }

            &.result-medium {
              color: #faad14;
            }

            &.result-low {
              color: #52c41a;
            }
          }
        }
      }

.empty-state {
  padding: 120rpx 40rpx;
  text-align: center;

  .empty-icon {
    width: 160rpx;
    height: 160rpx;
    margin: 0 auto 40rpx;
    background-color: #f5f5f5;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .empty-text {
    font-size: 28rpx;
    color: #999;
    margin-bottom: 40rpx;
  }

  .empty-button {
    display: inline-block;
    padding: 16rpx 40rpx;
    background-color: #4A90E2;
    color: #fff;
    border-radius: 8rpx;
    font-size: 28rpx;
    transition: background-color 0.2s;

    &:active {
      background-color: #357abd;
    }
  }
}
</style>
