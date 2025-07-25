<template>
    <view class="order-page">
        <!-- 顶部标签栏 -->
        <view class="tabs">
            <view v-for="(tab, index) in tabs" :key="index" class="tab-item" :class="{ active: currentTab === index }"
                @click="switchTab(index)">
                {{ tab.name }}
            </view>
        </view>

        <!-- 订单列表 -->
        <scroll-view scroll-y class="order-list" @scrolltolower="loadMore" :refresher-enabled="true"
            :refresher-triggered="refreshing" @refresherrefresh="onRefresh">
            <view v-if="orderList.length === 0" class="empty-list">
                <u-empty mode="order" text="暂无订单"></u-empty>
            </view>
            <view v-else>
                <view v-for="(order, index) in orderList" :key="index" class="order-item" @click="viewOrderDetails(order)">
                    <!-- 订单头部：订单号和状态 -->
                    <view class="order-header">
                        <text class="order-no">订单号：{{ order.orderNo }}</text>
                        <text class="order-status" :class="getStatusClass(order.status)">{{ getStatusText(order.status)
                        }}</text>
                    </view>

                    <!-- 订单内容 -->
                    <view class="order-content">
                        <!-- 订单类型图标 -->
                        <image :src="getOrderTypeIcon(order.type)" class="order-type-icon"></image>

                        <!-- 订单信息 -->
                        <view class="order-info">
                            <!-- 订单标题 -->
                            <view class="order-title">{{ order.title }}</view>

                            <!-- 咨询师信息或课程信息 -->
                            <view class="order-subtitle">
                                <text>{{ order.providerName || '' }}</text>
                                <text v-if="order.providerTitle">| {{ order.providerTitle }}</text>
                            </view>

                            <!-- 预约时间或购买时间 -->
                            <view class="order-time">
                                <text>{{ order.type === 'counseling' ? '预约时间：' : '购买时间：' }}</text>
                                <text>{{ order.appointmentTime || order.purchaseTime }}</text>
                            </view>
                        </view>
                    </view>

                    <!-- 订单底部：金额和操作按钮 -->
                    <view class="order-footer">
                        <view class="order-price">
                            <text>订单金额：</text>
                            <text class="price">¥{{ order.price.toFixed(2) }}</text>
                        </view>

                        <view class="order-actions">
                            <template v-if="order.status === 'pending'">
                                <view class="custom-button cancel-button" @click="cancelOrder(order)">取消订单</view>
                                <view class="custom-button primary-button" @click="payOrder(order)">立即支付</view>
                            </template>

                            <template v-else-if="order.status === 'paid' && order.type === 'course'">
                                <view class="custom-button outline-button" @click="viewOrderDetails(order)">查看详情</view>
                                <view class="custom-button primary-button" @click="studyCourse(order)">立即学习</view>
                            </template>

                            <template v-else-if="order.status === 'completed'">
                                <view class="custom-button outline-button" @click="viewOrderDetails(order)">查看详情</view>
                            </template>
                        </view>
                    </view>
                </view>
            </view>
            <!-- 加载更多 -->
            <view v-if="orderList.length > 0 && hasMore" class="loading-more">
                <u-loadmore :status="loadMoreStatus" />
            </view>
        </scroll-view>
    </view>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useCounterStore } from '@/store';
// 标签页定义
const tabs = [
    { name: '全部', status: '' },
    { name: '待付款', status: 'pending' },
    { name: '已完成', status: 'completed' },
    { name: '已取消', status: 'cancelled' }
];

// 响应式数据
const currentTab = ref(0);
const orderList = ref([]);
const page = ref(1);
const pageSize = ref(10);
const hasMore = ref(true);
const loadMoreStatus = ref('loadmore');
const refreshing = ref(false);

// 切换标签页
const switchTab = (index) => {
    if (currentTab.value === index) return;
    currentTab.value = index;
    resetList();
    loadOrders();
    orderList.value = mockOrders;
};

// 重置列表
const resetList = () => {
    orderList.value = [];
    page.value = 1;
    hasMore.value = true;
    loadMoreStatus.value = 'loadmore';
};

// store

const CounterStore = useCounterStore()

// 加载订单列表
const loadOrders = async () => {
};

// 上拉加载更多
const loadMore = () => {

};

// 下拉刷新
const onRefresh = () => {

};

// 获取订单状态文本
const getStatusText = (status) => {

};

// 获取状态样式类
const getStatusClass = (status) => {

};

// 获取订单类型图标
const getOrderTypeIcon = (type) => {

};

// 支付订单
const payOrder = (order) => {
    uni.navigateTo({
        url: '/pages/order/PayPedding/index'
    });
};

// 取消订单
const cancelOrder = (order) => {

};

// 查看订单详情
const viewOrderDetails = (order) => {    
    uni.navigateTo({
        url: '/pages/order/detail/index?id=' + order.id
    });
};

// 学习课程
const studyCourse = (order) => {

};

// 页面加载时获取订单列表
onMounted(() => {
    loadOrders();
});


const mockOrders = [
    {
        id: '1',
        orderNo: '042410621773',
        status: 'pending',
        type: 'counseling',
        title: '心理咨询服务（线上）',
        providerName: '李瑞峰',
        providerTitle: '高级心理咨询师',
        appointmentTime: '2023-10-10 14:00-14:50',
        price: 900
    },
    {
        id: '2',
        orderNo: '042410620981',
        status: 'paid',
        type: 'course',
        title: '情绪管理与心理健康',
        content: '12课时 | 共3小时',
        purchaseTime: '2023-09-25 18:30',
        price: 299,
        courseId: '101'
    },
    {
        id: '3',
        orderNo: '042410618765',
        status: 'completed',
        type: 'counseling',
        title: '心理咨询服务（线上）',
        providerName: '陈丽萍',
        providerTitle: '中级心理咨询师',
        appointmentTime: '2023-09-15 10:00-10:50',
        price: 600
    }
];

orderList.value = mockOrders;
</script>

<style lang="scss" scoped>
@import '@/static/theme.scss';

.order-page {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: $mg-bg-secondary;
}

.tabs {
    display: flex;
    background-color: $mg-bg-primary;
    border-bottom: 1px solid $mg-border-light;
    height: 88rpx;

    .tab-item {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 28rpx;
        color: $mg-text-secondary;
        position: relative;
        // background-color: red;
        height: 88rpx;

        &.active {
            color: $mg-primary;
            font-weight: 500;

            &::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 40rpx;
                height: 4rpx;
                background-color: $mg-primary;
            }
        }
    }
}

.order-list {
    flex: 1;
    padding: 20rpx;
    box-sizing: border-box;
    width: 100%;
}

.empty-list {
    padding: 60rpx 0;
}

.order-item {
    background-color: $mg-bg-primary;
    border-radius: 12rpx;
    margin-bottom: 24rpx;
    padding: 24rpx;
    box-shadow: 0 2rpx 12rpx $mg-shadow-color;
    width: 100%;
    box-sizing: border-box;
}

.order-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 20rpx;
    border-bottom: 1px solid $mg-border-light;

    .order-no {
        font-size: 24rpx;
        color: $mg-text-tertiary;
    }

    .order-status {
        font-size: 28rpx;
        font-weight: 500;

        &.status-pending {
            color: $mg-warning;
        }

        &.status-paid {
            color: $mg-primary;
        }

        &.status-completed {
            color: $mg-success;
        }

        &.status-cancelled {
            color: $mg-text-tertiary;
        }
    }
}

.order-content {
    display: flex;
    padding: 20rpx 0;

    .order-type-icon {
        width: 100rpx;
        height: 100rpx;
        border-radius: 8rpx;
        margin-right: 20rpx;
        background-color: $mg-bg-gold-light;
    }

    .order-info {
        flex: 1;

        .order-title {
            font-size: 32rpx;
            font-weight: 500;
            margin-bottom: 10rpx;
            color: $mg-text-primary;
        }

        .order-subtitle {
            font-size: 28rpx;
            color: $mg-text-secondary;
            margin-bottom: 10rpx;
        }

        .order-time {
            font-size: 24rpx;
            color: $mg-text-tertiary;
        }
    }
}

.order-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20rpx;
    border-top: 1px solid $mg-border-light;

    .order-price {
        font-size: 26rpx;
        color: $mg-text-secondary;

        .price {
            font-size: 32rpx;
            color: $mg-accent;
            font-weight: 500;
        }
    }

    .order-actions {
        display: flex;

        .custom-button {
            margin-left: 16rpx;
            height: 60rpx;
            min-width: 140rpx;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 30rpx;
            font-size: 26rpx;
            padding: 0 24rpx;
        }

        .primary-button {
            background-color: $mg-primary;
            color: $mg-white;
            border: 1px solid $mg-primary;
        }

        .outline-button {
            background-color: transparent;
            color: $mg-primary;
            border: 1px solid $mg-primary;
        }

        .cancel-button {
            background-color: transparent;
            color: $mg-text-secondary;
            border: 1px solid $mg-gray-400;
        }
    }
}

.loading-more {
    padding: 20rpx 0;
    text-align: center;
}
</style>