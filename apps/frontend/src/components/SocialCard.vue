<template>
    <view class="social-card" @click="handleCardClick">
        <!-- 用户信息 -->
        <view class="post-header">
            <view class="user-info">
                <image class="user-avatar" :src="post.user_avatar || '/static/icons/default-avatar.svg'"
                    mode="aspectFill" />
                <view class="user-details">
                    <text class="username">{{ post.username || '匿名用户' }}</text>
                    <text class="post-time">{{ formatTime(post.create_time) }}</text>
                </view>
            </view>
            <view class="post-category" v-if="post.category">
                <text class="category-text">{{ post.category }}</text>
            </view>
        </view>

        <!-- 帖子内容 -->
        <view class="post-content">
            <text class="post-title" v-if="post.title">{{ post.title }}</text>
            <text class="post-text">{{ post.content }}</text>

            <!-- 图片 -->
            <view class="post-images" v-if="post.images && post.images.length > 0">
                <image v-for="(img, imgIndex) in post.images.slice(0, 3)" :key="imgIndex" class="post-image" :src="img"
                    mode="aspectFill" @click.stop="previewImage(post.images, imgIndex)" />
                <view v-if="post.images.length > 3" class="more-images">
                    <text>+{{ post.images.length - 3 }}</text>
                </view>
            </view>

            <!-- 话题标签 -->
            <view class="post-topics" v-if="post.topics && post.topics.length > 0">
                <text v-for="(topic, topicIndex) in post.topics" :key="topicIndex" class="topic-tag-small"
                    @click.stop="handleTopicClick(topic)">
                    # {{ topic }}
                </text>
            </view>
        </view>

        <!-- 互动区域 -->
        <view class="post-actions">
            <view class="action-item" @click.stop="handleLike">
                <SvgIcon :name="post.is_liked ? 'star-filled' : 'star'" :size="20"
                    :color="post.is_liked ? '#ff6b6b' : '#666'" />
                <text class="action-text" :class="{ liked: post.is_liked }">
                    {{ post.like_count || 0 }}
                </text>
            </view>

            <view class="action-item" @click.stop="handleComment">
                <SvgIcon name="message" :size="20" color="#666" />
                <text class="action-text">{{ post.comment_count || 0 }}</text>
            </view>

            <view class="action-item" @click.stop="handleShare">
                <SvgIcon name="share" :size="20" color="#666" />
                <text class="action-text">分享</text>
            </view>
        </view>
    </view>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import SvgIcon from '@/components/SvgIcon.vue'

const props = defineProps({
    post: {
        type: Object,
        required: true,
        default: () => ({})
    }
})

const emit = defineEmits(['click', 'like', 'comment', 'share', 'topicClick'])

// 卡片点击
const handleCardClick = () => {
    emit('click', props.post)
}

// 点赞
const handleLike = () => {
    emit('like', props.post)
}

// 评论
const handleComment = () => {
    emit('comment', props.post)
}

// 分享
const handleShare = () => {
    emit('share', props.post)
}

// 话题点击
const handleTopicClick = (topic) => {
    emit('topicClick', topic)
}

// 预览图片
const previewImage = (images, current) => {
    uni.previewImage({
        urls: images,
        current: current
    })
}

// 格式化时间
const formatTime = (timeStr) => {
    if (!timeStr) return ''

    const time = new Date(timeStr)
    const now = new Date()
    const diff = now - time

    const minute = 1000 * 60
    const hour = minute * 60
    const day = hour * 24

    if (diff < minute) {
        return '刚刚'
    } else if (diff < hour) {
        return Math.floor(diff / minute) + '分钟前'
    } else if (diff < day) {
        return Math.floor(diff / hour) + '小时前'
    } else if (diff < day * 7) {
        return Math.floor(diff / day) + '天前'
    } else {
        return time.toLocaleDateString()
    }
}
</script>

<style lang="scss" scoped>
// SCSS变量
$primary-color: #4A90E2;
$success-color: #52c41a;
$success-light: #f6ffed;
$success-border: #b7eb8f;
$warning-color: #fa8c16;
$warning-light: #fff7e6;
$warning-border: #ffe7ba;
$danger-color: #ff6b6b;
$text-color: #333;
$text-light: #666;
$text-lighter: #999;
$white: #fff;
$bg-light: #f0f0f0;
$bg-hover: #f8f8f8;
$border-color: #f0f0f0;
$shadow-light: rgba(0, 0, 0, 0.05);
$border-radius: 16rpx;
$border-radius-small: 12rpx;
$border-radius-xs: 8rpx;

.social-card {
    background: $white;
    border-radius: $border-radius;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 2rpx 8rpx $shadow-light;

    // 帖子头部
    .post-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 20rpx;

        .user-info {
            display: flex;
            align-items: center;
            flex: 1;

            .user-avatar {
                width: 80rpx;
                height: 80rpx;
                border-radius: 40rpx;
                margin-right: 20rpx;
                background: $bg-light;
            }

            .user-details {
                flex: 1;

                .username {
                    font-size: 28rpx;
                    color: $text-color;
                    font-weight: bold;
                    display: block;
                    margin-bottom: 8rpx;
                }

                .post-time {
                    font-size: 24rpx;
                    color: $text-lighter;
                }
            }
        }

        .post-category {
            background: $success-light;
            color: $success-color;
            font-size: 22rpx;
            padding: 8rpx 16rpx;
            border-radius: $border-radius-small;
            border: 1rpx solid $success-border;

            .category-text {
                font-size: 22rpx;
            }
        }
    }

    // 帖子内容
    .post-content {
        margin-bottom: 20rpx;

        .post-title {
            font-size: 32rpx;
            color: $text-color;
            font-weight: bold;
            line-height: 1.4;
            margin-bottom: 12rpx;
            display: block;
        }

        .post-text {
            font-size: 28rpx;
            color: $text-light;
            line-height: 1.6;
            display: block;
            margin-bottom: 20rpx;
        }

        // 帖子图片
        .post-images {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10rpx;
            margin-bottom: 20rpx;

            .post-image {
                width: 100%;
                height: 200rpx;
                border-radius: $border-radius-small;
                object-fit: cover;
            }

            .more-images {
                width: 100%;
                height: 200rpx;
                border-radius: $border-radius-small;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                color: $white;
                font-size: 28rpx;
            }
        }

        // 话题标签
        .post-topics {
            display: flex;
            flex-wrap: wrap;
            gap: 10rpx;

            .topic-tag-small {
                font-size: 24rpx;
                color: $warning-color;
                background: $warning-light;
                padding: 6rpx 12rpx;
                border-radius: $border-radius-xs;
                border: 1rpx solid $warning-border;
            }
        }
    }

    // 互动区域
    .post-actions {
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding-top: 20rpx;
        border-top: 1rpx solid $border-color;

        .action-item {
            display: flex;
            align-items: center;
            gap: 8rpx;
            padding: 10rpx 20rpx;
            border-radius: 20rpx;
            transition: background-color 0.2s;

            &:active {
                background-color: $bg-hover;
            }

            .action-text {
                font-size: 24rpx;
                color: $text-light;

                &.liked {
                    color: $danger-color;
                }
            }
        }
    }
}
</style>