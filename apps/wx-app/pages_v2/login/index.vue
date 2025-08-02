<template>
    <view class="login-container">
        <!-- Logo -->
        <view class="logo-area">
            <view class="logo">
                <text class="logo-text">Y</text>
            </view>
        </view>
        
        <!-- Title Area -->
        <view class="title-area">
            <text class="main-title">心理咨询预约</text>
            <text class="sub-title">关注心理健康，放松身心</text>
        </view>
        
        <!-- Welcome Message -->
        <view class="welcome-area">
            <text class="welcome-text">欢迎使用心理咨询预约小程序</text>
            <text class="auth-text">请使用微信授权登录</text>
        </view>
        
        <!-- Login Buttons -->
        <view class="buttons-area">
            <button class="wechat-btn" @click="wechatLogin">
                <text class="wechat-icon">&#xe6b3;</text>
                <text>微信一键登录</text>
            </button>
            
            <view class="divider">
                <text class="divider-text">其他登录方式</text>
            </view>
            
            <button class="phone-btn" @click="phoneLogin">
                <text class="phone-icon">&#xe725;</text>
                <text>手机号登录</text>
            </button>
        </view>
        
        <!-- Agreement Text -->
        <view class="agreement-area">
            <text class="agreement-text">
                登录即表示您已阅读并同意 
                <text class="agreement-link" @click="openUserAgreement">《用户协议》</text> 
                和 
                <text class="agreement-link" @click="openPrivacyPolicy">《隐私政策》</text>
            </text>
        </view>
    </view>
</template>

<script setup>
import { ref } from 'vue';

// 登录方法
const wechatLogin = () => {
    uni.login({
        provider: 'weixin',
        success: (res) => {
            console.log('微信登录成功', res);
            // 处理微信登录逻辑
        },
        fail: (err) => {
            console.error('微信登录失败', err);
            uni.showToast({
                title: '登录失败，请重试',
                icon: 'none'
            });
        }
    });
};

const phoneLogin = () => {
    uni.navigateTo({
        url: '/pages/login/phone'
    });
};

// 打开协议
const openUserAgreement = () => {
    uni.navigateTo({
        url: '/pages/agreement/user'
    });
};

const openPrivacyPolicy = () => {
    uni.navigateTo({
        url: '/pages/agreement/privacy'
    });
};
</script>

<style lang="scss" scoped>
.login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40rpx;
    min-height: 100vh;
    background-color: #fff;
}

.logo-area {
    margin-top: 60rpx;
    width: 180rpx;
    height: 180rpx;
    
    .logo {
        width: 100%;
        height: 100%;
        border-radius: 28rpx;
        background-color: #eac993;
        display: flex;
        align-items: center;
        justify-content: center;
        
        .logo-text {
            color: #fff;
            font-size: 80rpx;
            font-weight: bold;
        }
    }
}

.title-area {
    margin-top: 30rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .main-title {
        font-size: 36rpx;
        font-weight: bold;
        color: #333;
    }
    
    .sub-title {
        margin-top: 20rpx;
        font-size: 28rpx;
        color: #999;
    }
}

.welcome-area {
    margin-top: 120rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .welcome-text {
        font-size: 32rpx;
        color: #666;
    }
    
    .auth-text {
        margin-top: 20rpx;
        font-size: 28rpx;
        color: #999;
    }
}

.buttons-area {
    margin-top: 60rpx;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .wechat-btn {
        width: 90%;
        height: 90rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #07C160;
        border-radius: 45rpx;
        color: #fff;
        font-size: 30rpx;
        
        .wechat-icon {
            margin-right: 10rpx;
            font-size: 36rpx;
        }
    }
    
    .divider {
        position: relative;
        margin: 60rpx 0;
        width: 90%;
        display: flex;
        align-items: center;
        justify-content: center;
        
        &::before, &::after {
            content: "";
            width: 35%;
            height: 1px;
            background-color: #eee;
        }
        
        .divider-text {
            padding: 0 20rpx;
            font-size: 24rpx;
            color: #999;
        }
    }
    
    .phone-btn {
        width: 90%;
        height: 90rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 45rpx;
        color: #666;
        font-size: 30rpx;
        
        .phone-icon {
            margin-right: 10rpx;
            font-size: 32rpx;
        }
    }
}

.agreement-area {
    position: fixed;
    bottom: 60rpx;
    left: 0;
    right: 0;
    text-align: center;
    
    .agreement-text {
        font-size: 24rpx;
        color: #999;
        
        .agreement-link {
            color: #5271FF;
        }
    }
}
</style>