<template>
	<!-- #ifdef MP-WEIXIN -->
	<view class="container">
		<!-- 搜索框 -->
		<view class="search-box">
			<u-search placeholder="请输入内容" v-model="searchText" :showAction="false" @search="goToSearch"></u-search>
		</view>

		<!-- 城市选择 -->
		<view class="city-select">
			<view v-for="(city, index) in cityList" :key="index" class="city-item"
				:class="{ active: currentCity === city.value }" @click="selectCity(city.value)">
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

		<!-- 咨询师列表 -->
		<view class="counselor-list">
			<view class="counselor-card" v-for="(counselor, index) in counselorList" :key="index"
				@click="navigateToCounselor(counselor.id)">
				<view class="counselor-avatar">
					<view class="avatar-placeholder" :style="{ backgroundColor: counselor.avatarColor }">
						<text>{{ counselor.name.substr(0, 1) }}</text>
					</view>
					<view class="badge bg-primary">{{ counselor.earliestAvailable }}</view>
				</view>
				<view class="counselor-info">
					<view class="counselor-name-wrap">
						<text class="counselor-name">{{ counselor.name }}</text>
						<view class="mg-tag primary">
							<u-icon name="star-fill" color="#E2AA59" size="14"></u-icon>
							<text>{{ counselor.level }}</text>
						</view>
					</view>
					<view class="counselor-title text-ellipsis">{{ counselor.title }}</view>
					<view class="counselor-tags">
						<text>擅长：</text>
						<text>{{ counselor.expertise.join(' / ') }}</text>
					</view>
					<view class="counselor-exp">从业{{ counselor.yearsOfExperience }}年 · 咨询经验{{
						counselor.consultationHours }}+小时</view>
					<view class="counselor-actions">
						<view class="action-video">视频咨询</view>
						<view class="price">¥<text class="price-value">{{ counselor.price }}</text>/节</view>
					</view>
				</view>
			</view>
		</view>
	</view>
	<!-- #endif -->
</template>

<script setup>
	import {
		reactive,
		ref
	} from 'vue'
	import {
		onLoad
	} from '@dcloudio/uni-app'
	import api from '../../api';
	import {
		date
	} from 'uview-plus/libs/function/test';
	const searchText = ref('')
	const currentCity = ref('all')

	// 城市列表
	const cityList = ref([{
			name: '全国',
			value: 'all'
		},
		{
			name: '北京',
			value: 'beijing'
		},
		{
			name: '上海',
			value: 'shanghai'
		},
		{
			name: '广州',
			value: 'guangzhou'
		},
		{
			name: '深圳',
			value: 'shenzhen'
		},
		{
			name: '成都',
			value: 'chengdu'
		},
		{
			name: '杭州',
			value: 'hangzhou'
		},
		{
			name: '武汉',
			value: 'wuhan'
		}
	])

	// 咨询师列表数据
	const counselorList = ref([{
			id: '1',
			name: '郭丽娟',
			avatarColor: '#F1C88B',
			level: '中级咨询师',
			title: '国家二级心理咨询师 中国心理学会注册助理心理师',
			expertise: ['情绪管理', '人际关系', '个人成长'],
			yearsOfExperience: 12,
			consultationHours: '2900',
			price: 500,
			earliestAvailable: '最早明天可约'
		},
		{
			id: '2',
			name: '陈丽萍',
			avatarColor: '#F47878',
			level: '中级咨询师',
			title: '国家二级心理咨询师 中级心理治疗师 中级社会工作师',
			expertise: ['少儿发展', '情绪管理', '个人成长'],
			yearsOfExperience: 16,
			consultationHours: '5500',
			price: 600,
			earliestAvailable: '最早明天可约'
		},
		{
			id: '3',
			name: '李瑞峰',
			avatarColor: '#E2AA59',
			level: '资深咨询师',
			title: '中国心理学会注册心理师 国家二级心理咨询师 国家督导师',
			expertise: ['情绪管理', '个人成长', '人际关系'],
			yearsOfExperience: 16,
			consultationHours: '15700',
			price: 900,
			earliestAvailable: '最早明天可约'
		}
	])

	onLoad(() => {
		console.log('首页加载')
		// 获取咨询师列表
		// getCounselorList()
	})

	const getCounselorList = async () => {
		const res = await api.counselor.getCounselorList({
			page: 1,
			pageSize: 10
		})
		counselorList.value = res.list || []
		console.log('咨询师列表', res.list);
	}

	// 切换城市
	const selectCity = (city) => {
		currentCity.value = city
		// 可以根据城市筛选咨询师列表
		console.log('切换城市:', city)
	}

	// 切换筛选条件
	const toggleFilter = (filterType) => {
		console.log('切换筛选条件:', filterType)
		// 实现筛选逻辑
	}

	// 跳转到搜索页面
	const goToSearch = () => {
		console.log('搜索内容', searchText.value);

	}

	// 跳转到咨询师详情页
	const navigateToCounselor = (id) => {
		uni.navigateTo({
			url: `/pages/counselor/detail/index?id=${id}`
		})
	}
</script>

<style scoped lang="scss">
	@import '@/static/theme.scss';

	.container {
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
			color: $mg-text-secondary;

			&.active {
				font-weight: bold;
				color: $mg-text-primary;
				position: relative;

				&::after {
					content: '';
					position: absolute;
					bottom: -6rpx;
					left: 50%;
					transform: translateX(-50%);
					width: 40rpx;
					height: 4rpx;
					background-color: $mg-primary;
					border-radius: 2rpx;
				}
			}
		}
	}

	.filter-bar {
		display: flex;
		justify-content: space-between;
		padding: 20rpx 30rpx;
		border-bottom: 1rpx solid $mg-border-light;

		.filter-item {
			display: flex;
			align-items: center;
			font-size: 26rpx;
			color: $mg-text-secondary;
			padding: 10rpx 16rpx;
			background-color: $mg-bg-secondary;
			border-radius: 30rpx;

			text {
				margin-right: 6rpx;
			}
		}
	}

	.counselor-list {
		padding: 0 30rpx;
	}

	.counselor-card {
		display: flex;
		padding: 30rpx 0;
		border-bottom: 1rpx solid $mg-border-light;
	}

	.counselor-avatar {
		position: relative;
		width: 180rpx;
		height: 180rpx;
		margin-right: 20rpx;
		flex-shrink: 0;

		.avatar-placeholder {
			width: 100%;
			height: 100%;
			border-radius: 8rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			font-size: 56rpx;
			font-weight: bold;
			color: $mg-white;
		}

		.badge {
			position: absolute;
			bottom: 0;
			left: 0;
			width: 100%;
			color: $mg-white;
			font-size: 20rpx;
			text-align: center;
			padding: 4rpx 0;
			border-bottom-left-radius: 8rpx;
			border-bottom-right-radius: 8rpx;

			&.bg-primary {
				background-color: $mg-primary;
			}
		}
	}

	.counselor-info {
		flex: 1;
		min-width: 0;
	}

	.counselor-name-wrap {
		display: flex;
		align-items: center;
		margin-bottom: 8rpx;
	}

	.counselor-name {
		font-size: 32rpx;
		font-weight: bold;
		margin-right: 16rpx;
		color: $mg-text-primary;
	}

	.mg-tag {
		display: inline-flex;
		align-items: center;
		padding: 2rpx 10rpx;
		border-radius: 4rpx;
		font-size: 22rpx;

		&.primary {
			background-color: $mg-bg-gold-light;
			color: $mg-primary;
			border: 1rpx solid rgba($mg-primary, 0.2);
		}
	}

	.counselor-title {
		font-size: 24rpx;
		color: $mg-text-secondary;
		margin-bottom: 10rpx;
	}

	.counselor-tags,
	.counselor-exp {
		font-size: 24rpx;
		color: $mg-text-tertiary;
		margin-bottom: 8rpx;
	}

	.counselor-actions {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-top: 16rpx;
	}

	.action-video {
		font-size: 24rpx;
		color: $mg-text-tertiary;
	}

	.price {
		font-size: 24rpx;
		color: $mg-accent;

		.price-value {
			font-size: 36rpx;
			font-weight: bold;
		}
	}

	.text-ellipsis {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
</style>