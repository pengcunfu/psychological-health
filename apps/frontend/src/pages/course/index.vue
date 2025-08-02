<template>
  <view class="container tab-page">
    <view class="search-bar">
      <u-search
        v-model="searchKeyword"
        placeholder="搜索课程"
        :show-action="false"
        @search="handleSearch"
        @custom="handleSearch"
      ></u-search>
    </view>

    <view class="filter-bar">
      <view 
        class="filter-item" 
        :class="{ active: activeFilter === 'all' }" 
        @click="setFilter('all')"
      >
        全部
      </view>
      <view 
        class="filter-item" 
        :class="{ active: activeFilter === 'popular' }" 
        @click="setFilter('popular')"
      >
        最热门
      </view>
      <view 
        class="filter-item" 
        :class="{ active: activeFilter === 'newest' }" 
        @click="setFilter('newest')"
      >
        最新上架
      </view>
      <view 
        class="filter-item" 
        :class="{ active: activeFilter === 'price' }" 
        @click="setFilter('price')"
      >
        价格排序
      </view>
    </view>

    <view class="course-list">
      <view 
        class="course-card" 
        v-for="(item, index) in courseList" 
        :key="index"
        @click="navigateToDetail(item.id)"
      >
        <image class="course-image" :src="item.cover || '/static/images/default-course.png'" mode="aspectFill"></image>
        <view class="course-info">
          <text class="course-name text-ellipsis">{{ item.name }}</text>
          <view class="course-teacher">
            <u-avatar :src="item.teacher_avatar || '/static/images/default-avatar.png'" size="40"></u-avatar>
            <text class="teacher-name">{{ item.teacher_name }}</text>
          </view>
          <view class="course-stats">
            <text class="course-sales">{{ item.sales || 0 }}人已学习</text>
            <text class="course-lessons">{{ item.lesson_count || 0 }}课时</text>
          </view>
          <view class="course-footer">
            <text class="course-price">¥{{ item.price || 0 }}</text>
            <button class="buy-btn">立即购买</button>
          </view>
        </view>
      </view>
    </view>

    <u-loadmore :status="loadMoreStatus" />
  </view>
</template>

<script>
import { ref, reactive } from 'vue'
import { onLoad, onReachBottom } from '@dcloudio/uni-app'
import { request } from '@/utils/request'

export default {
  setup() {
    const searchKeyword = ref('')
    const activeFilter = ref('all')
    const courseList = ref([])
    const loadMoreStatus = ref('loading')
    
    const pagination = reactive({
      page: 1,
      per_page: 10,
      total: 0,
      total_pages: 0
    })
    
    // 获取课程列表
    const fetchCourses = async (reset = false) => {
      if (reset) {
        pagination.page = 1
        courseList.value = []
      }
      
      loadMoreStatus.value = 'loading'
      
      try {
        // 构建查询参数
        const params = {
          page: pagination.page,
          per_page: pagination.per_page,
          keyword: searchKeyword.value
        }
        
        // 根据筛选条件添加排序参数
        switch (activeFilter.value) {
          case 'popular':
            params.sort_by = 'sales'
            params.sort_order = 'desc'
            break
          case 'newest':
            params.sort_by = 'create_time'
            params.sort_order = 'desc'
            break
          case 'price':
            params.sort_by = 'price'
            params.sort_order = 'asc'
            break
        }
        
        const res = await request({
          url: '/course',
          method: 'GET',
          data: params
        })
        
        if (res.code === 200 && res.success) {
          // 解析返回的课程列表
          const newList = res.data.list || []
          
          // 更新列表和分页信息
          courseList.value = reset ? newList : [...courseList.value, ...newList]
          pagination.total = res.data.total || 0
          pagination.total_pages = res.data.pages || 0
          
          // 更新加载更多状态
          loadMoreStatus.value = pagination.page >= pagination.total_pages ? 'nomore' : 'loadmore'
        } else {
          loadMoreStatus.value = 'loadmore'
          uni.showToast({
            title: res.message || '获取课程列表失败',
            icon: 'none'
          })
        }
      } catch (error) {
        console.error('获取课程列表失败:', error)
        loadMoreStatus.value = 'loadmore'
        uni.showToast({
          title: '获取课程列表失败，请稍后重试',
          icon: 'none'
        })
      }
    }
    
    // 搜索处理
    const handleSearch = () => {
      fetchCourses(true)
    }
    
    // 筛选处理
    const setFilter = (filter) => {
      activeFilter.value = filter
      fetchCourses(true)
    }
    
    // 跳转到详情页
    const navigateToDetail = (id) => {
      uni.navigateTo({
        url: `/pages/course/detail/index?id=${id}`
      })
    }
    
    // 页面加载
    onLoad(() => {
      fetchCourses()
    })
    
    // 下拉加载更多
    onReachBottom(() => {
      if (loadMoreStatus.value === 'loadmore') {
        pagination.page++
        fetchCourses()
      }
    })
    
    return {
      searchKeyword,
      activeFilter,
      courseList,
      loadMoreStatus,
      handleSearch,
      setFilter,
      navigateToDetail
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

.search-bar {
  padding: 20rpx 30rpx;
  background-color: #fff;
}

.filter-bar {
  display: flex;
  background-color: #fff;
  padding: 0 20rpx;
  margin-bottom: 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.filter-item {
  padding: 20rpx 30rpx;
  font-size: 28rpx;
  color: #666;
  position: relative;
}

.filter-item.active {
  color: #4A90E2;
  font-weight: bold;
}

.filter-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40rpx;
  height: 4rpx;
  background-color: #4A90E2;
}

.course-list {
  padding: 0 30rpx;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.course-card {
  width: calc(50% - 15rpx);
  background-color: #fff;
  border-radius: 20rpx;
  overflow: hidden;
  margin-bottom: 30rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.course-image {
  width: 100%;
  height: 200rpx;
  background-color: #f0f0f0;
}

.course-info {
  padding: 20rpx;
}

.course-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
  display: block;
  white-space: nowrap;
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
  justify-content: space-between;
  margin-bottom: 10rpx;
}

.course-sales, .course-lessons {
  font-size: 24rpx;
  color: #999;
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

.buy-btn {
  background-color: #4A90E2;
  color: #fff;
  font-size: 24rpx;
  padding: 8rpx 20rpx;
  border-radius: 30rpx;
  border: none;
}
</style> 