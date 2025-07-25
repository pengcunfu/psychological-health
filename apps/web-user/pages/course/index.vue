<template>
    <view class="course-container">
        <!-- 搜索框 -->
        <view class="search-box">
            <u-search placeholder="请输入内容" v-model="searchText" :showAction="false" @search="goToSearch"></u-search>
        </view>
        
        <!-- 城市选择 -->
        <view class="city-select">
            <view 
                v-for="(city, index) in cityList" 
                :key="index" 
                class="city-item" 
                :class="{ active: currentCity === city.value }"
                @click="selectCity(city.value)"
            >
                {{ city.name }}
            </view>
        </view>

        <!-- 筛选条件 -->
        <view class="filter-bar">
            <view class="filter-item" @click="toggleFilter('trouble')">
                <text>困扰</text>
                <u-icon name="arrow-down" size="14"></u-icon>
            </view>
            <view class="filter-item" @click="toggleFilter('time')">
                <text>时间</text>
                <u-icon name="arrow-down" size="14"></u-icon>
            </view>
            <view class="filter-item" @click="toggleFilter('price')">
                <text>价格</text>
                <u-icon name="arrow-down" size="14"></u-icon>
            </view>
            <view class="filter-item" @click="toggleFilter('filter')">
                <text>筛选</text>
                <u-icon name="arrow-down" size="14"></u-icon>
            </view>
            <view class="filter-item" @click="toggleFilter('sort')">
                <text>排序</text>
                <u-icon name="arrow-down" size="14"></u-icon>
            </view>
        </view>
        
        <!-- 课程列表 -->
        <view class="course-list">
            <view 
                class="course-card" 
                v-for="(course, index) in courseList" 
                :key="index"
                @click="navigateToCourseDetail(course.id)"
            >
                <view class="course-image">
                    <view class="image-placeholder" :style="{ backgroundColor: course.imageColor }">
                        <text>课程图片</text>
                    </view>
                </view>
                <view class="course-info">
                    <view class="course-title">{{ course.title }}</view>
                    
                    <view class="course-tags">
                        <view 
                            class="course-tag" 
                            v-for="(tag, tagIndex) in course.tags" 
                            :key="tagIndex"
                        >
                            {{ tag }}
                        </view>
                    </view>
                    
                    <view class="course-detail">
                        <text class="course-hours">{{ course.lessons }}课时 | 共{{ course.duration }}小时</text>
                        <text class="course-price">¥{{ course.price }}</text>
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const searchText = ref('')
const currentCity = ref('all')

// 城市列表
const cityList = ref([
    { name: '全国', value: 'all' },
    { name: '北京', value: 'beijing' },
    { name: '上海', value: 'shanghai' },
    { name: '广州', value: 'guangzhou' },
    { name: '深圳', value: 'shenzhen' },
    { name: '成都', value: 'chengdu' }
])

// 课程列表数据
const courseList = ref([
    {
        id: '1',
        title: '情绪管理与心理健康',
        imageColor: '#F1C88B', // 浅金色
        tags: ['认知行为疗法', '情绪管理'],
        lessons: 12,
        duration: 3,
        price: 299
    },
    {
        id: '2',
        title: '人际关系修复与提升',
        imageColor: '#F47878', // 浅红色
        tags: ['人际关系', '沟通技巧'],
        lessons: 8,
        duration: 2,
        price: 199
    },
    {
        id: '3',
        title: '压力管理与减压技巧',
        imageColor: '#E2AA59', // 金色
        tags: ['减压', '职场压力'],
        lessons: 10,
        duration: 2.5,
        price: 259
    },
    {
        id: '4',
        title: '青少年心理健康教育',
        imageColor: '#D19845', // 深金色
        tags: ['青少年', '亲子关系'],
        lessons: 15,
        duration: 4,
        price: 399
    }
])

onLoad(() => {
    console.log('课程页面加载')
})

// 切换城市
const selectCity = (city) => {
    currentCity.value = city
    // 可以根据城市筛选课程列表
    console.log('切换城市:', city)
}

// 切换筛选条件
const toggleFilter = (filterType) => {
    console.log('切换筛选条件:', filterType)
    // 实现筛选逻辑
}

// 搜索功能
const goToSearch = () => {
    console.log('搜索内容:', searchText.value)
    // 实现搜索逻辑
}

// 跳转到课程详情页
const navigateToCourseDetail = (id) => {
    uni.navigateTo({
        url: `/pages/course/detail/index?id=${id}`
    })
}
</script>

<style lang="scss" scoped>
.course-container {
    padding-bottom: 30rpx;
}

.search-box {
    padding: 20rpx 30rpx;
}

.city-select {
    display: flex;
    padding: 10rpx 30rpx;
    overflow-x: auto;
    white-space: nowrap;
    
    .city-item {
        padding: 6rpx 20rpx;
        margin-right: 30rpx;
        font-size: 28rpx;
        color: var(--mg-text-secondary, #666666);
        
        &.active {
            font-weight: bold;
            color: white;
            background-color: var(--mg-primary, #E2AA59);
            border-radius: 100rpx;
            padding: 6rpx 30rpx;
        }
    }
}

.filter-bar {
    display: flex;
    justify-content: space-between;
    padding: 20rpx 30rpx;
    border-bottom: 1rpx solid var(--mg-border-light, #E9E9E9);
    
    .filter-item {
        display: flex;
        align-items: center;
        font-size: 26rpx;
        color: var(--mg-text-secondary, #666666);
        
        text {
            margin-right: 6rpx;
        }
    }
}

.course-list {
    padding: 0 30rpx;
}

.course-card {
    display: flex;
    flex-direction: column;
    margin-bottom: 30rpx;
    background-color: white;
    border-radius: 12rpx;
    overflow: hidden;
    box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.course-image {
    width: 100%;
    height: 200rpx;
    
    .image-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28rpx;
        color: var(--mg-text-secondary, #666666);
    }
}

.course-info {
    padding: 20rpx;
}

.course-title {
    font-size: 34rpx;
    font-weight: bold;
    margin-bottom: 16rpx;
    color: var(--mg-text-primary, #222222);
}

.course-tags {
    display: flex;
    margin-bottom: 16rpx;
    flex-wrap: wrap;
    
    .course-tag {
        font-size: 24rpx;
        color: var(--mg-primary, #E2AA59);
        background-color: rgba(226, 170, 89, 0.1);
        padding: 4rpx 20rpx;
        border-radius: 100rpx;
        margin-right: 16rpx;
        margin-bottom: 10rpx;
        border: 1rpx solid var(--mg-primary, #E2AA59);
    }
}

.course-detail {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .course-hours {
        font-size: 24rpx;
        color: var(--mg-text-tertiary, #ADADAD);
    }
    
    .course-price {
        font-size: 36rpx;
        font-weight: bold;
        color: #FF5252;
    }
}
</style>