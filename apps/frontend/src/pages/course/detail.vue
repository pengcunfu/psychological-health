<template>
  <view class="container">
    <view class="course-header">
      <image class="course-cover" :src="courseInfo.cover || '/static/images/default-course.png'" mode="aspectFill"></image>
      <view class="course-info">
        <text class="course-name">{{ courseInfo.name || '加载中...' }}</text>
        <view class="course-stats">
          <text class="course-price">¥{{ courseInfo.price || 0 }}</text>
          <text class="course-sales">{{ courseInfo.sales || 0 }}人已学习</text>
        </view>
      </view>
    </view>

    <view class="tab-section">
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'intro' }" 
        @click="switchTab('intro')"
      >
        课程介绍
      </view>
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'catalog' }" 
        @click="switchTab('catalog')"
      >
        课程目录
      </view>
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'comments' }" 
        @click="switchTab('comments')"
      >
        评价({{ commentCount }})
      </view>
    </view>

    <view class="content-section">
      <!-- 课程介绍 -->
      <view v-if="activeTab === 'intro'" class="intro-content">
        <view class="section-block">
          <view class="block-title">课程简介</view>
          <view class="block-content">
            <text class="intro-text">{{ courseInfo.introduction || '暂无介绍' }}</text>
          </view>
        </view>
        
        <view class="section-block">
          <view class="block-title">适合人群</view>
          <view class="block-content">
            <view class="target-item" v-for="(target, index) in targetUsers" :key="index">
              <up-icon name="checkmark-circle" color="#4A90E2" size="30"></up-icon>
              <text class="target-text">{{ target }}</text>
            </view>
          </view>
        </view>
        
        <view class="section-block">
          <view class="block-title">课程亮点</view>
          <view class="block-content">
            <view class="highlight-item" v-for="(highlight, index) in highlights" :key="index">
              <text class="highlight-num">{{ index + 1 }}</text>
              <text class="highlight-text">{{ highlight }}</text>
            </view>
          </view>
        </view>
        
        <view class="section-block">
          <view class="block-title">讲师介绍</view>
          <view class="block-content">
            <view class="teacher-card">
              <up-avatar :src="courseInfo.teacher_avatar || '/static/images/default-avatar.png'" size="120"></up-avatar>
              <view class="teacher-info">
                <text class="teacher-name">{{ courseInfo.teacher_name || '未知讲师' }}</text>
                <text class="teacher-title">{{ courseInfo.teacher_title || '' }}</text>
                <text class="teacher-intro">{{ courseInfo.teacher_intro || '暂无介绍' }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 课程目录 -->
      <view v-if="activeTab === 'catalog'" class="catalog-content">
        <view v-if="chapters.length > 0">
          <view class="chapter-item" v-for="(chapter, chapterIndex) in chapters" :key="chapterIndex">
            <view class="chapter-header" @click="toggleChapter(chapterIndex)">
              <view class="chapter-title">
                <text class="chapter-index">{{ chapterIndex + 1 }}</text>
                <text class="chapter-name">{{ chapter.name }}</text>
              </view>
              <up-icon :name="chapter.expanded ? 'arrow-down' : 'arrow-right'" size="30" color="#999"></up-icon>
            </view>
            <view class="chapter-lessons" v-if="chapter.expanded">
              <view 
                class="lesson-item" 
                v-for="(lesson, lessonIndex) in chapter.lessons" 
                :key="lessonIndex"
                @click="playLesson(lesson)"
              >
                <view class="lesson-info">
                  <text class="lesson-index">{{ chapterIndex + 1 }}-{{ lessonIndex + 1 }}</text>
                  <text class="lesson-name">{{ lesson.name }}</text>
                </view>
                <view class="lesson-duration">
                  <up-icon name="clock" size="24" color="#999"></up-icon>
                  <text class="duration-text">{{ lesson.duration || '00:00' }}</text>
                </view>
              </view>
            </view>
          </view>
        </view>
        <view v-else class="empty-content">
          <up-empty mode="list" icon="list" text="暂无课程目录"></up-empty>
        </view>
      </view>
      
      <!-- 评价 -->
      <view v-if="activeTab === 'comments'" class="comments-content">
        <view v-if="comments.length > 0">
          <view class="comment-item" v-for="(comment, index) in comments" :key="index">
            <view class="comment-header">
              <up-avatar :src="comment.user_avatar || '/static/images/default-avatar.png'" size="80"></up-avatar>
              <view class="comment-user">
                <text class="comment-username">{{ comment.username }}</text>
                <view class="comment-rating">
                  <up-rate :value="comment.rating" readonly size="16" active-color="#faad14"></up-rate>
                  <text class="comment-time">{{ comment.create_time }}</text>
                </view>
              </view>
            </view>
            <view class="comment-body">
              <text class="comment-text">{{ comment.content }}</text>
            </view>
            <view class="comment-footer" v-if="comment.reply">
              <text class="reply-label">讲师回复：</text>
              <text class="reply-text">{{ comment.reply }}</text>
            </view>
          </view>
        </view>
        <view v-else class="empty-content">
          <up-empty mode="comment" icon="chat" text="暂无评价"></up-empty>
        </view>
      </view>
    </view>

    <view class="bottom-action">
      <view class="action-btn-group">
        <view class="action-btn" @click="handleCollect">
          <up-icon :name="isCollected ? 'star-fill' : 'star'" :color="isCollected ? '#faad14' : '#999'" size="40"></up-icon>
          <text class="btn-text">{{ isCollected ? '已收藏' : '收藏' }}</text>
        </view>
        <view class="action-btn" @click="handleShare">
          <up-icon name="share" color="#999" size="40"></up-icon>
          <text class="btn-text">分享</text>
        </view>
      </view>
      <button class="buy-btn" @click="handleBuy">立即购买</button>
    </view>
  </view>
</template>

<script>
import { ref, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { request } from '@/utils/request'
import { checkLogin } from '@/utils/auth'

export default {
  setup() {
    const courseId = ref('')
    const courseInfo = ref({})
    const activeTab = ref('intro')
    const targetUsers = ref([])
    const highlights = ref([])
    const chapters = ref([])
    const comments = ref([])
    const commentCount = ref(0)
    const isCollected = ref(false)
    
    // 获取课程信息
    const fetchCourseInfo = async () => {
      try {
        const res = await request({
          url: `/course/${courseId.value}`,
          method: 'GET'
        })
        
        if (res.code === 200 && res.success) {
          courseInfo.value = res.data || {}
          
          // 处理适合人群
          targetUsers.value = [
            '有心理困扰，需要专业指导的人群',
            '想要提升心理健康水平的人群',
            '对心理学知识感兴趣的人群',
            '希望改善人际关系的人群'
          ]
          
          // 处理课程亮点
          highlights.value = [
            '由资深心理咨询师授课，理论与实践相结合',
            '系统化的课程内容，循序渐进，易于理解',
            '提供丰富的案例分析，贴近生活实际',
            '配套练习和工具，帮助学员巩固所学知识'
          ]
          
          // 检查是否已收藏
          checkCollectionStatus()
        }
      } catch (error) {
        console.error('获取课程信息失败:', error)
        uni.showToast({
          title: '获取课程信息失败',
          icon: 'none'
        })
      }
    }
    
    // 获取课程目录
    const fetchCourseCatalog = async () => {
      try {
        const res = await request({
          url: `/course/${courseId.value}/catalog`,
          method: 'GET'
        })
        
        if (res.code === 200 && res.success) {
          const catalogData = res.data || []
          
          // 处理章节数据
          chapters.value = catalogData.map(chapter => {
            return {
              ...chapter,
              expanded: false // 默认折叠
            }
          })
        }
      } catch (error) {
        console.error('获取课程目录失败:', error)
      }
    }
    
    // 获取评价列表
    const fetchComments = async () => {
      try {
        const res = await request({
          url: `/course/${courseId.value}/comments`,
          method: 'GET',
          data: {
            page: 1,
            per_page: 10
          }
        })
        
        if (res.code === 200 && res.success) {
          comments.value = res.data.list || []
          commentCount.value = res.data.total || 0
        }
      } catch (error) {
        console.error('获取评价列表失败:', error)
      }
    }
    
    // 检查收藏状态
    const checkCollectionStatus = async () => {
      if (!checkLogin(false)) return
      
      try {
        const res = await request({
          url: `/user/favorite/check`,
          method: 'GET',
          data: {
            type: 'course',
            target_id: courseId.value
          }
        })
        
        if (res.code === 200 && res.success) {
          isCollected.value = res.data.is_favorite || false
        }
      } catch (error) {
        console.error('检查收藏状态失败:', error)
      }
    }
    
    // 切换标签
    const switchTab = (tab) => {
      activeTab.value = tab
      
      if (tab === 'catalog' && chapters.value.length === 0) {
        fetchCourseCatalog()
      } else if (tab === 'comments' && comments.value.length === 0) {
        fetchComments()
      }
    }
    
    // 展开/折叠章节
    const toggleChapter = (index) => {
      chapters.value[index].expanded = !chapters.value[index].expanded
    }
    
    // 播放课程
    const playLesson = (lesson) => {
      if (!checkLogin()) return
      
      // 检查是否已购买课程
      checkPurchaseStatus(() => {
        // 跳转到播放页面
        uni.navigateTo({
          url: `/pages/course/play/index?course_id=${courseId.value}&lesson_id=${lesson.id}`
        })
      })
    }
    
    // 检查是否已购买课程
    const checkPurchaseStatus = (callback) => {
      request({
        url: `/user/course/check`,
        method: 'GET',
        data: {
          course_id: courseId.value
        }
      }).then(res => {
        if (res.code === 200 && res.success && res.data.purchased) {
          // 已购买，执行回调
          callback && callback()
        } else {
          // 未购买，提示购买
          uni.showModal({
            title: '提示',
            content: '您尚未购买该课程，是否立即购买？',
            success: (result) => {
              if (result.confirm) {
                handleBuy()
              }
            }
          })
        }
      }).catch(error => {
        console.error('检查购买状态失败:', error)
        uni.showToast({
          title: '检查购买状态失败',
          icon: 'none'
        })
      })
    }
    
    // 收藏/取消收藏
    const handleCollect = () => {
      if (!checkLogin()) return
      
      const url = isCollected.value ? '/user/favorite/cancel' : '/user/favorite/add'
      
      request({
        url,
        method: 'POST',
        data: {
          type: 'course',
          target_id: courseId.value
        }
      }).then(res => {
        if (res.code === 200 && res.success) {
          isCollected.value = !isCollected.value
          
          uni.showToast({
            title: isCollected.value ? '收藏成功' : '已取消收藏',
            icon: 'success'
          })
        } else {
          uni.showToast({
            title: res.message || '操作失败',
            icon: 'none'
          })
        }
      }).catch(error => {
        console.error('收藏操作失败:', error)
        uni.showToast({
          title: '操作失败，请稍后重试',
          icon: 'none'
        })
      })
    }
    
    // 分享
    const handleShare = () => {
      uni.showToast({
        title: '分享功能开发中',
        icon: 'none'
      })
    }
    
    // 购买
    const handleBuy = () => {
      if (!checkLogin()) return
      
      uni.navigateTo({
        url: `/pages/order/create?type=course&id=${courseId.value}`
      })
    }
    
    // 页面加载
    onLoad((options) => {
      if (options.id) {
        courseId.value = options.id
        fetchCourseInfo()
      } else {
        uni.showToast({
          title: '参数错误',
          icon: 'none'
        })
        
        setTimeout(() => {
          uni.navigateBack()
        }, 1500)
      }
    })
    
    return {
      courseInfo,
      activeTab,
      targetUsers,
      highlights,
      chapters,
      comments,
      commentCount,
      isCollected,
      switchTab,
      toggleChapter,
      playLesson,
      handleCollect,
      handleShare,
      handleBuy
    }
  }
}
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 120rpx; /* 为底部操作栏留出空间 */
}

.course-header {
  background-color: #fff;
}

.course-cover {
  width: 100%;
  height: 400rpx;
  background-color: #f0f0f0;
}

.course-info {
  padding: 30rpx;
}

.course-name {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.course-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-price {
  font-size: 40rpx;
  color: #f5222d;
  font-weight: bold;
}

.course-sales {
  font-size: 28rpx;
  color: #999;
}

.tab-section {
  display: flex;
  background-color: #fff;
  margin-top: 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 30rpx 0;
  font-size: 28rpx;
  color: #666;
  position: relative;
}

.tab-item.active {
  color: #4A90E2;
  font-weight: bold;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60rpx;
  height: 4rpx;
  background-color: #4A90E2;
}

.content-section {
  background-color: #fff;
  min-height: 300rpx;
  padding: 30rpx;
}

.section-block {
  margin-bottom: 40rpx;
}

.block-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  position: relative;
  padding-left: 20rpx;
}

.block-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 6rpx;
  height: 30rpx;
  background-color: #4A90E2;
}

.block-content {
  padding: 0 10rpx;
}

.intro-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.8;
}

.target-item, .highlight-item {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.target-text, .highlight-text {
  font-size: 28rpx;
  color: #666;
  margin-left: 10rpx;
  flex: 1;
}

.highlight-num {
  width: 40rpx;
  height: 40rpx;
  background-color: #4A90E2;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: bold;
}

.teacher-card {
  display: flex;
  background-color: #f5f7fa;
  padding: 20rpx;
  border-radius: 10rpx;
}

.teacher-info {
  flex: 1;
  margin-left: 20rpx;
}

.teacher-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 10rpx;
}

.teacher-title {
  font-size: 24rpx;
  color: #666;
  display: block;
  margin-bottom: 10rpx;
}

.teacher-intro {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.chapter-item {
  margin-bottom: 20rpx;
  border-radius: 10rpx;
  overflow: hidden;
  background-color: #f5f7fa;
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx;
  background-color: #f0f0f0;
}

.chapter-title {
  display: flex;
  align-items: center;
}

.chapter-index {
  width: 40rpx;
  height: 40rpx;
  background-color: #4A90E2;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: bold;
  margin-right: 10rpx;
}

.chapter-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.lesson-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.lesson-item:last-child {
  border-bottom: none;
}

.lesson-info {
  display: flex;
  align-items: center;
}

.lesson-index {
  font-size: 24rpx;
  color: #999;
  margin-right: 10rpx;
}

.lesson-name {
  font-size: 28rpx;
  color: #333;
}

.lesson-duration {
  display: flex;
  align-items: center;
}

.duration-text {
  font-size: 24rpx;
  color: #999;
  margin-left: 5rpx;
}

.comment-item {
  padding: 30rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  margin-bottom: 20rpx;
}

.comment-user {
  flex: 1;
  margin-left: 20rpx;
}

.comment-username {
  font-size: 28rpx;
  color: #333;
  font-weight: bold;
  display: block;
  margin-bottom: 10rpx;
}

.comment-rating {
  display: flex;
  align-items: center;
}

.comment-time {
  font-size: 24rpx;
  color: #999;
  margin-left: 20rpx;
}

.comment-body {
  margin-bottom: 20rpx;
}

.comment-text {
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
}

.comment-footer {
  background-color: #f5f7fa;
  padding: 20rpx;
  border-radius: 10rpx;
}

.reply-label {
  font-size: 24rpx;
  color: #999;
  margin-right: 10rpx;
}

.reply-text {
  font-size: 28rpx;
  color: #333;
}

.empty-content {
  padding: 60rpx 0;
  text-align: center;
}

.bottom-action {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 100rpx;
  background-color: #fff;
  display: flex;
  align-items: center;
  padding: 0 30rpx;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.action-btn-group {
  display: flex;
  flex: 1;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 40rpx;
}

.btn-text {
  font-size: 24rpx;
  color: #999;
  margin-top: 5rpx;
}

.buy-btn {
  width: 240rpx;
  height: 80rpx;
  line-height: 80rpx;
  background-color: #4A90E2;
  color: #fff;
  font-size: 32rpx;
  text-align: center;
  border-radius: 40rpx;
  border: none;
}
</style> 