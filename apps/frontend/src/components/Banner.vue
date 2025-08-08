<template>
    <view class="banner">
        <swiper v-if="bannerList.length > 0" :autoplay="autoplay" :interval="interval" :duration="duration"
            :circular="circular" :indicator-dots="false" class="swiper-container" @change="handleBannerChange">
            <swiper-item v-for="(item, index) in bannerList" :key="item.id || index"
                @tap="() => handleBannerClick(index)">
                <view class="swiper-item">
                    <image :src="item.image_url" mode="aspectFill" class="swiper-image" @load="onImageLoad"
                        @error="onImageError" />
                    <view v-if="showTitle && item.title" class="swiper-title">{{ item.title }}</view>
                </view>
            </swiper-item>
        </swiper>

        <!-- 自定义指示器 -->
        <view v-if="bannerList.length > 0 && indicatorDots" class="custom-indicator">
            <view 
                v-for="(item, index) in bannerList" 
                :key="index"
                class="indicator-item"
                :class="{ active: index === currentIndex }"
            ></view>
        </view>

        <!-- 空状态 -->
        <view v-else class="banner-empty">
            <slot name="empty">
                <up-empty text="暂无轮播图" icon="https://cdn.uviewui.com/uview/empty/list.png" iconSize="80" textSize="12"
                    textColor="#999999" marginTop="50" />
            </slot>
        </view>

        <!-- 加载状态 -->
        <view v-if="loading" class="banner-loading">
            <slot name="loading">
                <up-loading-icon mode="flower" size="40"></up-loading-icon>
                <text class="loading-text">加载中...</text>
            </slot>
        </view>
    </view>
</template>

<script setup>
import { computed, ref } from 'vue'
import { preprocessUrl, handleUrlNavigation } from '@/utils/link'

// 定义 props
const props = defineProps({
    // 轮播图数据
    bannerData: {
        type: Array,
        default: () => []
    },
    // 是否自动播放
    autoplay: {
        type: Boolean,
        default: true
    },
    // 自动播放间隔时间（毫秒）
    interval: {
        type: Number,
        default: 3000
    },
    // 滑动动画时长（毫秒）
    duration: {
        type: Number,
        default: 300
    },
    // 是否循环播放
    circular: {
        type: Boolean,
        default: true
    },
    // 是否显示指示点
    indicatorDots: {
        type: Boolean,
        default: true
    },
    // 指示点激活颜色
    indicatorActiveColor: {
        type: String,
        default: '#4A90E2'
    },
    // 指示点默认颜色
    indicatorColor: {
        type: String,
        default: 'rgba(222, 222, 222, 1)'
    },
    // 加载状态
    loading: {
        type: Boolean,
        default: false
    },
    // 轮播图高度
    height: {
        type: String,
        default: '300rpx'
    },
    // 是否显示标题
    showTitle: {
        type: Boolean,
        default: false
    }
})

// 定义 emits
const emit = defineEmits(['bannerClick', 'bannerChange', 'imageLoad', 'imageError'])

// 计算轮播图数据
const bannerList = computed(() => props.bannerData)

// 当前索引
const currentIndex = ref(0)

// 轮播图点击处理
const handleBannerClick = (index) => {

    const banner = bannerList.value[index]

    // 发送点击事件给父组件
    emit('bannerClick', { banner, index })

    // 默认跳转逻辑
    if (banner && banner.link_url) {

        // 预处理链接URL
        const processedUrl = preprocessUrl(banner.link_url)

        // 判断链接类型并执行相应的跳转逻辑
        handleUrlNavigation(processedUrl, banner.title || '加载中...')
    } else {
        uni.showToast({
            title: '链接无效',
            icon: 'none'
        })
    }
}

// 轮播图变化处理
const handleBannerChange = (e) => {
    const currentIndexValue = e.detail.current

    // 更新当前索引
    currentIndex.value = currentIndexValue

    // 发送变化事件给父组件
    emit('bannerChange', {
        current: currentIndexValue,
        banner: bannerList.value[currentIndexValue]
    })
}

// 图片加载成功
const onImageLoad = (e) => {
    emit('imageLoad', e)
}

// 图片加载失败
const onImageError = (e) => {
    emit('imageError', e)
}
</script>

<style lang="scss" scoped>
.banner {
    height: v-bind(height);
    position: relative;
    padding:  20rpx;
}

.banner :deep(.uni-swiper-wrapper),
.banner :deep(.uni-swiper-slides) {
    border-radius: 16rpx !important;
    overflow: hidden !important;
}

.swiper-container {
    height: 100%;
    border-radius: 16rpx;
    overflow: hidden;
}

.swiper-item {
    width: 100%;
    height: 100%;
    position: relative;
    border-radius: 16rpx;
    overflow: hidden;
}

.swiper-image {
    width: 100%;
    height: 100%;
    object-fit: fill;
}

.swiper-title {
    position: absolute;
    bottom: 20rpx;
    left: 20rpx;
    right: 20rpx;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    padding: 10rpx 20rpx;
    border-radius: 10rpx;
    font-size: 28rpx;
    text-align: center;
}

.banner-empty {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #fafafa;
    border-radius: 12rpx;
}

.banner-loading {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: rgba(245, 245, 245, 0.9);
    z-index: 10;
}

.loading-text {
    font-size: 28rpx;
    color: #999;
    margin-top: 20rpx;
}

// 自定义指示器样式
.custom-indicator {
    position: absolute;
    bottom: 8rpx;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 5;
}

.indicator-item {
    width: 8rpx;
    height: 4rpx;
    background-color: v-bind(indicatorColor);
    border-radius: 3rpx;
    margin: 0 2rpx;
    transition: all 0.3s ease;
    
    &.active {
        background-color: v-bind(indicatorActiveColor);
        width: 10rpx;
    }
}
</style>