<template>
  <view class="container">
    <view class="tab-section">
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'counselor' }" 
        @click="switchTab('counselor')"
      >
        咨询师
      </view>
      <view 
        class="tab-item" 
        :class="{ active: activeTab === 'course' }" 
        @click="switchTab('course')"
      >
        课程
      </view>
    </view>

    <view class="content-section">
      <!-- 咨询师收藏 -->
      <view v-if="activeTab === 'counselor'">
        <view v-if="counselors.length > 0">
          <view 
            class="counselor-card" 
            v-for="(item, index) in counselors" 
            :key="index"
            @click="navigateToCounselor(item.id)"
          >
            <view class="card-left">
              <up-avatar :src="item.avatar || '/static/images/default-avatar.png'" :size="120"></up-avatar>
              <view class="counselor-info">
                <view class="counselor-name-row">
                  <text class="counselor-name">{{ item.name }}</text>
                  <text class="counselor-title">{{ item.title }}</text>
                </view>
                <view class="counselor-rating">
                  <up-icon name="star-fill" color="#faad14" :size="24"></up-icon>
                  <text class="rating-text">{{ item.rating }}</text>
                  <text class="consultation-count">{{ item.consultation_count }}次咨询</text>
                </view>
                <view class="counselor-tags">
                  <text class="tag" v-for="(tag, tagIndex) in item.tags" :key="tagIndex">{{ tag }}</text>
                </view>
              </view>
            </view>
            <view class="card-right">
              <text class="price">¥{{ item.price }}/次</text>
              <view class="action-btns">
                <button class="action-btn cancel-btn" @click.stop="handleCancelFavorite('counselor', item.id)">
                  <up-icon name="close" :size="24" color="#999"></up-icon>
                </button>
              </view>
            </view>
          </view>
        </view>
        <view v-else class="empty-content">
          <up-empty mode="list" icon="star" text="暂无收藏的咨询师"></up-empty>
        </view>
      </view>

      <!-- 课程收藏 -->
      <view v-if="activeTab === 'course'">
        <view v-if="courses.length > 0">
          <view 
            class="course-card" 
            v-for="(item, index) in courses" 
            :key="index"
            @click="navigateToCourse(item.id)"
          >
            <image class="course-image" :src="item.cover || '/static/images/default-course.png'" mode="aspectFill"></image>
            <view class="course-info">
              <text class="course-name">{{ item.name }}</text>
              <view class="course-teacher">
                <up-avatar :src="item.teacher_avatar || '/static/images/default-avatar.png'" :size="40"></up-avatar>
                <text class="teacher-name">{{ item.teacher_name }}</text>
              </view>
              <view class="course-stats">
                <view class="stat-item">
                  <up-icon name="clock" :size="24" color="#999"></up-icon>
                  <text class="stat-text">{{ item.duration || '0小时' }}</text>
                </view>
                <view class="stat-item">
                  <up-icon name="account" :size="24" color="#999"></up-icon>
                  <text class="stat-text">{{ item.sales || 0 }}人学习</text>
                </view>
              </view>
              <view class="course-footer">
                <text class="course-price">¥{{ item.price }}</text>
                <button class="action-btn cancel-btn" @click.stop="handleCancelFavorite('course', item.id)">
                  <up-icon name="close" :size="24" color="#999"></up-icon>
                </button>
              </view>
            </view>
          </view>
        </view>
        <view v-else class="empty-content">
          <up-empty mode="list" icon="star" text="暂无收藏的课程"></up-empty>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { ref } from 'vue'
import { onLoad, onPullDownRefresh, onReachBottom } from '@dcloudio/uni-app'
import { request } from '@/utils/request'
import { checkLogin } from '@/utils/auth'

export default {
  setup() {
    // 检查登录状态
    if (!checkLogin()) return {}
    
    const activeTab = ref('counselor')
    const counselors = ref([])
    const courses = ref([])
    const loading = ref(false)
    
    const counselorPagination = ref({
      page: 1,
      per_page: 10,
      total: 0,
      total_pages: 0
    })
    
    const coursePagination = ref({
      page: 1,
      per_page: 10,
      total: 0,
      total_pages: 0
    })
    
    // 获取收藏的咨询师列表
    const fetchCounselors = async (reset = false) => {
      if (loading.value) return
      
      if (reset) {
        counselorPagination.value.page = 1
        counselors.value = []
      }
      
      loading.value = true
      
      try {
        const res = await request({
          url: '/user/favorite',
          method: 'GET',
          data: {
            type: 'counselor',
            page: counselorPagination.value.page,
            per_page: counselorPagination.value.per_page
          }
        })
        
        if (res.code === 200 && res.success) {
          const newList = res.data.list || []
          
          // 处理标签字段，将字符串转为数组
          newList.forEach(item => {
            if (typeof item.tags === 'string') {
              item.tags = item.tags.split(',').filter(tag => tag.trim() !== '')
            } else if (!Array.isArray(item.tags)) {
              item.tags = []
            }
          })
          
          counselors.value = reset ? newList : [...counselors.value, ...newList]
          counselorPagination.value.total = res.data.total || 0
          counselorPagination.value.total_pages = res.data.pages || 0
        } else {
          uni.showToast({
            title: res.message || '获取收藏列表失败',
            icon: 'none'
          })
        }
      } catch (error) {
        console.error('获取收藏列表失败:', error)
        uni.showToast({
          title: '获取收藏列表失败，请稍后重试',
          icon: 'none'
        })
      } finally {
        loading.value = false
        
        // 停止下拉刷新
        uni.stopPullDownRefresh()
      }
    }
    
    // 获取收藏的课程列表
    const fetchCourses = async (reset = false) => {
      if (loading.value) return
      
      if (reset) {
        coursePagination.value.page = 1
        courses.value = []
      }
      
      loading.value = true
      
      try {
        const res = await request({
          url: '/user/favorite',
          method: 'GET',
          data: {
            type: 'course',
            page: coursePagination.value.page,
            per_page: coursePagination.value.per_page
          }
        })
        
        if (res.code === 200 && res.success) {
          const newList = res.data.list || []
          courses.value = reset ? newList : [...courses.value, ...newList]
          coursePagination.value.total = res.data.total || 0
          coursePagination.value.total_pages = res.data.pages || 0
        } else {
          uni.showToast({
            title: res.message || '获取收藏列表失败',
            icon: 'none'
          })
        }
      } catch (error) {
        console.error('获取收藏列表失败:', error)
        uni.showToast({
          title: '获取收藏列表失败，请稍后重试',
          icon: 'none'
        })
      } finally {
        loading.value = false
        
        // 停止下拉刷新
        uni.stopPullDownRefresh()
      }
    }
    
    // 切换标签页
    const switchTab = (tab) => {
      activeTab.value = tab
      
      if (tab === 'counselor' && counselors.value.length === 0) {
        fetchCounselors(true)
      } else if (tab === 'course' && courses.value.length === 0) {
        fetchCourses(true)
      }
    }
    
    // 取消收藏
    const handleCancelFavorite = (type, id) => {
      uni.showModal({
        title: '提示',
        content: '确定要取消收藏吗？',
        success: async (res) => {
          if (res.confirm) {
            try {
              uni.showLoading({
                title: '处理中...'
              })
              
              const result = await request({
                url: '/user/favorite/cancel',
                method: 'POST',
                data: {
                  type: type,
                  target_id: id
                }
              })
              
              uni.hideLoading()
              
              if (result.code === 200 && result.success) {
                uni.showToast({
                  title: '已取消收藏',
                  icon: 'success'
                })
                
                // 从列表中移除
                if (type === 'counselor') {
                  counselors.value = counselors.value.filter(item => item.id !== id)
                } else if (type === 'course') {
                  courses.value = courses.value.filter(item => item.id !== id)
                }
              } else {
                uni.showToast({
                  title: result.message || '操作失败',
                  icon: 'none'
                })
              }
            } catch (error) {
              uni.hideLoading()
              console.error('取消收藏失败:', error)
              uni.showToast({
                title: '操作失败，请稍后重试',
                icon: 'none'
              })
            }
          }
        }
      })
    }
    
    // 跳转到咨询师详情
    const navigateToCounselor = (id) => {
      uni.navigateTo({
        url: `/pages/counselor/detail?id=${id}`
      })
    }
    
    // 跳转到课程详情
    const navigateToCourse = (id) => {
      uni.navigateTo({
        url: `/pages/course/detail?id=${id}`
      })
    }
    
    // 页面加载
    onLoad(() => {
      fetchCounselors(true)
    })
    
    // 下拉刷新
    onPullDownRefresh(() => {
      if (activeTab.value === 'counselor') {
        fetchCounselors(true)
      } else {
        fetchCourses(true)
      }
    })
    
    // 上拉加载更多
    onReachBottom(() => {
      if (loading.value) return
      
      if (activeTab.value === 'counselor') {
        if (counselorPagination.value.page < counselorPagination.value.total_pages) {
          counselorPagination.value.page++
          fetchCounselors()
        }
      } else {
        if (coursePagination.value.page < coursePagination.value.total_pages) {
          coursePagination.value.page++
          fetchCourses()
        }
      }
    })
    
    return {
      activeTab,
      counselors,
      courses,
      switchTab,
      handleCancelFavorite,
      navigateToCounselor,
      navigateToCourse
    }
  }
}
</script>

<style lang="scss">
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 30rpx;
}

.tab-section {
  display: flex;
  background-color: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
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
  padding: 20rpx 30rpx;
}

.counselor-card {
  display: flex;
  justify-content: space-between;
  background-color: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.card-left {
  display: flex;
  flex: 1;
}

.counselor-info {
  flex: 1;
  margin-left: 20rpx;
}

.counselor-name-row {
  margin-bottom: 10rpx;
}

.counselor-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-right: 10rpx;
}

.counselor-title {
  font-size: 24rpx;
  color: #666;
  background-color: #f5f7fa;
  padding: 4rpx 10rpx;
  border-radius: 4rpx;
}

.counselor-rating {
  display: flex;
  align-items: center;
  margin-bottom: 10rpx;
}

.rating-text {
  font-size: 24rpx;
  color: #faad14;
  margin: 0 10rpx;
}

.consultation-count {
  font-size: 24rpx;
  color: #999;
}

.counselor-tags {
  display: flex;
  flex-wrap: wrap;
}

.tag {
  font-size: 24rpx;
  color: #4A90E2;
  background-color: rgba(74, 144, 226, 0.1);
  padding: 4rpx 10rpx;
  border-radius: 4rpx;
  margin-right: 10rpx;
  margin-bottom: 10rpx;
}

.card-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-between;
  margin-left: 20rpx;
}

.price {
  font-size: 32rpx;
  color: #f5222d;
  font-weight: bold;
}

.action-btns {
  display: flex;
}

.action-btn {
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
  background-color: transparent;
}

.cancel-btn {
  color: #999;
}

.course-card {
  display: flex;
  background-color: #fff;
  border-radius: 20rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.course-image {
  width: 200rpx;
  height: 200rpx;
  border-radius: 10rpx;
  background-color: #f0f0f0;
}

.course-info {
  flex: 1;
  margin-left: 20rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.course-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.course-teacher {
  display: flex;
  align-items: center;
  margin-bottom: 10rpx;
}

.teacher-name {
  font-size: 24rpx;
  color: #666;
  margin-left: 10rpx;
}

.course-stats {
  display: flex;
  margin-bottom: 10rpx;
}

.stat-item {
  display: flex;
  align-items: center;
  margin-right: 30rpx;
}

.stat-text {
  font-size: 24rpx;
  color: #999;
  margin-left: 10rpx;
}

.course-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-price {
  font-size: 32rpx;
  color: #f5222d;
  font-weight: bold;
}

.empty-content {
  padding: 100rpx 0;
  text-align: center;
}
</style> 