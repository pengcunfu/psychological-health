<template>
    <view class="order-detail-page">
        <!-- 页面标题 -->
        <view class="page-header">
            <view class="title">订单详情</view>
        </view>

        <!-- 加载中 -->
        <view v-if="loading" class="loading-container">
            <u-loading-icon mode="circle" size="36"></u-loading-icon>
            <text class="loading-text">加载中...</text>
        </view>

        <!-- 订单详情卡片 -->
        <view v-else class="order-card">
            <!-- 订单状态 -->
            <view class="status-bar" :style="{ backgroundColor: theme.mgPrimary }">
                <text class="status-text">{{ getStatusText(orderDetail.status) }}</text>
            </view>

            <!-- 订单基本信息 -->
            <view class="order-info">
                <view class="order-no">
                    <text class="label">订单编号：</text>
                    <text class="value">{{ orderDetail.orderNo }}</text>
                    <text class="copy-btn" @click="copyOrderNo">复制</text>
                </view>
                <view class="order-time">
                    <text class="label">创建时间：</text>
                    <text class="value">{{ orderDetail.createTime }}</text>
                </view>
            </view>

            <!-- 分割线 -->
            <view class="divider"></view>

            <!-- 服务信息 -->
            <view class="service-info">
                <!-- 服务类型图标 -->
                <image :src="getOrderTypeIcon(orderDetail.type)" class="service-icon"></image>

                <!-- 服务详情 -->
                <view class="service-details">
                    <view class="service-title">{{ orderDetail.title }}</view>
                    <view class="provider-info">
                        <image v-if="orderDetail.providerAvatar" :src="orderDetail.providerAvatar"
                            class="provider-avatar"></image>
                        <view class="provider-text">
                            <text class="provider-name">{{ orderDetail.providerName }}</text>
                            <text v-if="orderDetail.providerTitle" class="provider-title">{{ orderDetail.providerTitle
                                }}</text>
                        </view>
                    </view>
                    <view class="service-desc">{{ orderDetail.serviceInfo }}</view>

                    <!-- 预约时间或有效期 -->
                    <view v-if="orderDetail.appointmentTime" class="appointment-time">
                        <text class="label">预约时间：</text>
                        <text class="value highlight">{{ orderDetail.appointmentTime }}</text>
                    </view>
                    <view v-if="orderDetail.expiryDate" class="expiry-date">
                        <text class="label">有效期至：</text>
                        <text class="value">{{ orderDetail.expiryDate }}</text>
                    </view>
                </view>
            </view>

            <!-- 分割线 -->
            <view class="divider"></view>

            <!-- 价格信息 -->
            <view class="price-info">
                <view class="price-row">
                    <text class="label">订单金额</text>
                    <text class="value">¥{{ orderDetail.price.toFixed(2) }}</text>
                </view>
                <view v-if="orderDetail.discount > 0" class="price-row">
                    <text class="label">优惠金额</text>
                    <text class="value">-¥{{ orderDetail.discount.toFixed(2) }}</text>
                </view>
                <view class="price-row total">
                    <text class="label">实付金额</text>
                    <text class="value" :style="{ color: theme.mgPrimary }">¥{{ orderDetail.actualPaid.toFixed(2)
                        }}</text>
                </view>
            </view>

            <!-- 分割线 -->
            <view class="divider"></view>

            <!-- 支付信息 -->
            <view class="payment-info">
                <view class="payment-method">
                    <text class="label">支付方式：</text>
                    <text class="value">{{ getPaymentMethodText(orderDetail.paymentMethod) }}</text>
                </view>
                <view v-if="orderDetail.paymentTime" class="payment-time">
                    <text class="label">支付时间：</text>
                    <text class="value">{{ orderDetail.paymentTime }}</text>
                </view>
            </view>

            <!-- 备注信息 -->
            <view v-if="orderDetail.note" class="note-section">
                <text class="note-label">备注信息</text>
                <text class="note-content">{{ orderDetail.note }}</text>
            </view>
        </view>

        <!-- 底部操作按钮 -->
        <view v-if="!loading" class="bottom-actions">
            <template v-if="orderDetail.status === 'pending'">
                <view class="action-button cancel-button" @click="cancelOrder">取消订单</view>
                <view class="action-button primary-button" :style="{ backgroundColor: theme.mgPrimary }"
                    @click="payOrder">立即支付</view>
            </template>

            <template v-else-if="orderDetail.status === 'paid' && orderDetail.type === 'course'">
                <view class="action-button full-button" :style="{ backgroundColor: theme.mgPrimary }"
                    @click="studyCourse">立即学习</view>
            </template>

            <template v-else-if="orderDetail.status === 'paid' && orderDetail.type === 'counseling'">
                <view class="action-button cancel-button" @click="contactCustomerService">联系客服</view>
                <view class="action-button primary-button" :style="{ backgroundColor: theme.mgPrimary }"
                    @click="enterCounseling">进入咨询</view>
            </template>
        </view>

        <!-- <tab-bar current="/pages/order/index" /> -->
    </view>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useTheme } from '@/hooks/useTheme';
import { useCounterStore } from '@/store';
import { onLoad } from '@dcloudio/uni-app';
// import TabBar from '@/components/TabBar/index.vue';

// 获取主题变量
const theme = useTheme();

// 加载状态
const loading = ref(true);

// 订单详情数据
const orderDetail = ref({
    id: '',
    orderNo: '',
    type: '', // counseling 或 course
    title: '',
    providerName: '',
    providerTitle: '',
    providerAvatar: '',
    serviceInfo: '',
    appointmentTime: '',
    expiryDate: '',
    price: 0,
    discount: 0,
    actualPaid: 0,
    paymentMethod: '',
    paymentTime: '',
    status: '',
    createTime: '',
    note: ''
});

// 加载订单详情
const loadOrderDetail = async (id) => {
    if (!id) {
        uni.showToast({
            title: '订单ID不存在',
            icon: 'none'
        });
        return;
    }

    loading.value = true;
    try {
        // 这里应该调用API获取订单详情
        // const res = await api.order.getOrderDetail(id);
        // orderDetail.value = res.data;
        
        // 模拟数据
        setTimeout(() => {
            orderDetail.value = {
                id: id,
                orderNo: '2023060112345',
                type: 'counseling',
                title: '心理咨询服务',
                providerName: '张医生',
                providerTitle: '心理咨询师',
                providerAvatar: '/static/images/avatar/doctor.png',
                serviceInfo: '个人咨询 (50分钟)',
                appointmentTime: '2023-06-01 10:00-11:00',
                expiryDate: null,
                price: 300,
                discount: 0,
                actualPaid: 300,
                paymentMethod: 'wechat',
                paymentTime: '2023-05-28 14:35:10',
                status: 'paid',
                createTime: '2023-05-28 14:30:25',
                note: '第一次咨询，希望能得到专业帮助'
            };
            loading.value = false;
        }, 500);
    } catch (error) {
        uni.showToast({
            title: '获取订单详情失败',
            icon: 'none'
        });
        loading.value = false;
    }
};

// 获取订单状态文本
const getStatusText = (status) => {
    const statusMap = {
        'pending': '待支付',
        'paid': '已支付',
        'completed': '已完成',
        'cancelled': '已取消',
        'refunded': '已退款'
    };
    return statusMap[status] || '未知状态';
};

// 获取支付方式文本
const getPaymentMethodText = (method) => {
    const methodMap = {
        'wechat': '微信支付',
        'alipay': '支付宝',
        'balance': '余额支付',
        'card': '银行卡支付'
    };
    return methodMap[method] || '未知方式';
};

// 获取订单类型图标
const getOrderTypeIcon = (type) => {
    if (type === 'counseling') {
        return '/static/images/icons/counseling.png';
    } else if (type === 'course') {
        return '/static/images/icons/course.png';
    } else {
        return '/static/images/icons/default.png';
    }
};

// 复制订单号
const copyOrderNo = () => {
    uni.setClipboardData({
        data: orderDetail.value.orderNo,
        success: () => {
            uni.showToast({
                title: '订单号已复制',
                icon: 'none'
            });
        }
    });
};

// 取消订单
const cancelOrder = () => {
    uni.showModal({
        title: '取消订单',
        content: '确定要取消该订单吗？',
        success: async (res) => {
            if (res.confirm) {
                try {
                    // 调用取消订单接口
                    // await api.order.cancelOrder(orderDetail.value.id);
                    
                    uni.showToast({
                        title: '订单已取消',
                        icon: 'success'
                    });
                    
                    // 刷新订单状态
                    loadOrderDetail(orderDetail.value.id);
                } catch (error) {
                    uni.showToast({
                        title: '取消订单失败',
                        icon: 'none'
                    });
                }
            }
        }
    });
};

// 支付订单
const payOrder = () => {
    uni.navigateTo({
        url: '/pages/order/PayPedding/index?id=' + orderDetail.value.id
    });
};

// 立即学习课程
const studyCourse = () => {
    uni.navigateTo({
        url: '/pages/course/detail/index?id=' + orderDetail.value.id
    });
};

// 进入咨询
const enterCounseling = () => {
    // 进入咨询页面
    uni.navigateTo({
        url: '/pages/counselor/session/index?id=' + orderDetail.value.id
    });
};

// 联系客服
const contactCustomerService = () => {
    // 联系客服逻辑
    uni.showToast({
        title: '联系客服功能开发中',
        icon: 'none'
    });
};

// 在页面加载时获取订单详情
onLoad((options) => {
    loadOrderDetail(options.id);
});
</script>

<style lang="scss">
.order-detail-page {
    min-height: 100vh;
    background-color: #f5f5f5;
    padding-bottom: 120rpx;
    // padding-bottom: 180rpx; // 调整为更大的值以适应TabBar
}

.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 100rpx 0;
    
    .loading-text {
        margin-top: 20rpx;
        font-size: 28rpx;
        color: #999;
    }
}

.page-header {
    padding: 30rpx;
    background-color: #fff;
    
    .title {
        font-size: 36rpx;
        font-weight: bold;
        color: #333;
    }
}

.order-card {
    margin: 30rpx;
    background-color: #fff;
    border-radius: 12rpx;
    box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
    overflow: hidden;
    
    .status-bar {
        padding: 20rpx 30rpx;
        
        .status-text {
            color: #fff;
            font-size: 32rpx;
            font-weight: 500;
        }
    }
    
    .order-info {
        padding: 30rpx;
        
        .order-no,
        .order-time {
            display: flex;
            align-items: center;
            margin-bottom: 10rpx;
            font-size: 28rpx;
            
            .label {
                color: #666;
                min-width: 140rpx;
            }
            
            .value {
                color: #333;
                flex: 1;
            }
            
            .copy-btn {
                color: $uni-color-primary;
                padding: 0 10rpx;
            }
        }
    }
    
    .divider {
        height: 1rpx;
        background-color: #f0f0f0;
        margin: 0 30rpx;
    }
    
    .service-info {
        padding: 30rpx;
        display: flex;
        
        .service-icon {
            width: 80rpx;
            height: 80rpx;
            margin-right: 20rpx;
        }
        
        .service-details {
            flex: 1;
            
            .service-title {
                font-size: 32rpx;
                font-weight: 500;
                color: #333;
                margin-bottom: 10rpx;
            }
            
            .provider-info {
                display: flex;
                align-items: center;
                margin-bottom: 10rpx;
                
                .provider-avatar {
                    width: 50rpx;
                    height: 50rpx;
                    border-radius: 50%;
                    margin-right: 10rpx;
                }
                
                .provider-text {
                    display: flex;
                    align-items: center;
                    
                    .provider-name {
                        font-size: 28rpx;
                        color: #333;
                    }
                    
                    .provider-title {
                        font-size: 24rpx;
                        color: #999;
                        margin-left: 10rpx;
                    }
                }
            }
            
            .service-desc {
                font-size: 28rpx;
                color: #666;
                margin-bottom: 10rpx;
            }
            
            .appointment-time,
            .expiry-date {
                font-size: 28rpx;
                margin-top: 10rpx;
                
                .label {
                    color: #666;
                }
                
                .value {
                    color: #333;
                    
                    &.highlight {
                        color: $uni-color-primary;
                        font-weight: 500;
                    }
                }
            }
        }
    }
    
    .price-info {
        padding: 30rpx;
        
        .price-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10rpx;
            font-size: 28rpx;
            
            .label {
                color: #666;
            }
            
            .value {
                color: #333;
            }
            
            &.total {
                margin-top: 20rpx;
                
                .label {
                    font-weight: 500;
                }
                
                .value {
                    font-weight: bold;
                    font-size: 32rpx;
                }
            }
        }
    }
    
    .payment-info {
        padding: 30rpx;
        
        .payment-method,
        .payment-time {
            display: flex;
            margin-bottom: 10rpx;
            font-size: 28rpx;
            
            .label {
                color: #666;
                min-width: 140rpx;
            }
            
            .value {
                color: #333;
            }
        }
    }
    
    .note-section {
        padding: 30rpx;
        
        .note-label {
            font-size: 28rpx;
            color: #666;
            margin-bottom: 10rpx;
            display: block;
        }
        
        .note-content {
            font-size: 28rpx;
            color: #333;
            background-color: #f9f9f9;
            padding: 20rpx;
            border-radius: 8rpx;
            display: block;
        }
    }
}

.bottom-actions {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    padding: 20rpx 30rpx;
    background-color: #fff;
    box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
    
    .action-button {
        flex: 1;
        height: 80rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30rpx;
        border-radius: 8rpx;
        
        &.cancel-button {
            background-color: #f5f5f5;
            color: #666;
            margin-right: 20rpx;
        }
        
        &.primary-button {
            color: #fff;
        }
        
        &.full-button {
            color: #fff;
        }
    }
}
</style>
