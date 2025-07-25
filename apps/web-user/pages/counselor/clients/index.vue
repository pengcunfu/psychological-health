<template>
    <view class="clients-container">
        <!-- 搜索和筛选区 -->
        <view class="search-filter-container" style="background-color: white;">
            <view class="search-box">
                <input type="text" placeholder="搜索客户姓名/手机号" v-model="searchQuery" class="search-input" />
                <view class="search-icon">
                    <view class="icon-search"></view>
                </view>
            </view>

            <view class="filter-options">
                <view class="filter-item" 
                    :class="{ active: activeFilter === 'all' }" 
                    :style="activeFilter === 'all' ? 'background-color: rgba(226, 170, 89, 0.1); color: #E2AA59;' : ''" 
                    @click="setFilter('all')">
                    全部
                </view>
                <view class="filter-item" 
                    :class="{ active: activeFilter === 'recent' }" 
                    :style="activeFilter === 'recent' ? 'background-color: rgba(226, 170, 89, 0.1); color: #E2AA59;' : ''" 
                    @click="setFilter('recent')">
                    最近咨询
                </view>
                <view class="filter-item" 
                    :class="{ active: activeFilter === 'frequent' }" 
                    :style="activeFilter === 'frequent' ? 'background-color: rgba(226, 170, 89, 0.1); color: #E2AA59;' : ''" 
                    @click="setFilter('frequent')">
                    咨询频繁
                </view>
                <view class="filter-item" 
                    :class="{ active: activeFilter === 'followup' }" 
                    :style="activeFilter === 'followup' ? 'background-color: rgba(226, 170, 89, 0.1); color: #E2AA59;' : ''" 
                    @click="setFilter('followup')">
                    待跟进
                </view>
            </view>
        </view>

        <!-- 客户列表 -->
        <scroll-view class="client-list-scroll" scroll-y @scrolltolower="loadMore" v-if="filteredClients.length > 0">
            <view class="client-list">
                <view class="client-card" v-for="(client, index) in displayClients" :key="index"
                    @click="viewClientDetail(client.id)" style="background-color: white; border-left: 3px solid #E2AA59;">
                    <view class="client-info">
                        <view class="client-avatar" :style="{ backgroundColor: getAvatarColor(client.name) }">
                            <text>{{ client.name.charAt(0) }}</text>
                        </view>

                        <view class="client-details">
                            <view class="client-name-row">
                                <text class="client-name" style="color: #333333;">{{ client.name }}</text>
                                <text class="client-gender" style="background-color: #F9EFD6; color: #D19845;">{{ client.gender === 'male' ? '男' : '女' }}</text>
                                <text class="client-age" v-if="client.age" style="background-color: #F9EFD6; color: #D19845;">{{ client.age }}岁</text>
                            </view>

                            <view class="client-contact">
                                <text class="client-phone">{{ client.phone }}</text>
                            </view>

                            <view class="client-stats">
                                <text class="stat-item">咨询次数: <text
                                        class="stat-value" style="color: #E2AA59;">{{ client.sessionCount }}</text></text>
                                <text class="stat-item">首次咨询: <text
                                        class="stat-value">{{ formatDate(client.firstSession) }}</text></text>
                                <text class="stat-item">最近咨询: <text
                                        class="stat-value">{{ formatDate(client.lastSession) }}</text></text>
                            </view>
                        </view>
                    </view>

                    <view class="client-tags" v-if="client.tags && client.tags.length > 0">
                        <text class="tag" v-for="(tag, tagIndex) in client.tags" :key="tagIndex" style="background-color: #F9EFD6; color: #D19845;">{{ tag }}</text>
                    </view>

                    <view class="client-actions" style="border-top: 1px solid #F1F1F1;">
                        <view class="action-button call" @click.stop="callClient(client.phone)" style="color: #3498db;">
                            <view class="icon-phone action-icon"></view>
                            <text class="action-text">电话</text>
                        </view>
                        <view class="action-button message" @click.stop="messageClient(client.id)" style="color: #E2AA59;">
                            <view class="icon-message action-icon"></view>
                            <text class="action-text">消息</text>
                        </view>
                        <view class="action-button appointment" @click.stop="scheduleAppointment(client.id)" style="color: #27ae60;">
                            <view class="icon-calendar action-icon"></view>
                            <text class="action-text">预约</text>
                        </view>
                        <view class="action-button notes" @click.stop="viewNotes(client.id)" style="color: #e67e22;">
                            <view class="icon-note action-icon"></view>
                            <text class="action-text">记录</text>
                        </view>
                    </view>
                </view>

                <!-- 加载更多 -->
                <view class="load-more" v-if="hasMoreClients">
                    <view class="load-more-btn" @click="loadMore" style="background-color: #F9EFD6; color: #D19845;">加载更多</view>
                </view>
                <view class="no-more" v-else style="color: #999999;">
                    没有更多客户了
                </view>
            </view>
        </scroll-view>

        <!-- 空状态 -->
        <view class="empty-state" v-else style="background-color: white;">
            <image class="empty-icon" src="/static/images/empty-clients.png" mode="aspectFit"></image>
            <text class="empty-text">暂无客户记录</text>
            <text class="empty-description">用户咨询后将自动创建客户记录</text>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            // 定义主题色变量以确保JS中引用的颜色一致
            themeColors: {
                primary: '#E2AA59',
                primaryDark: '#D19845',
                primaryLight: '#F1C88B',
                primaryBg: '#F9EFD6',
                success: '#4CAF50',
                info: '#2196F3',
                warning: '#FF9800',
                error: '#F44336'
            },
            searchQuery: '',
            activeFilter: 'all',
            pageSize: 10,
            currentPage: 1,
            clients: [
                {
                    id: 'c001',
                    name: '张女士',
                    gender: 'female',
                    age: 28,
                    phone: '138****1234',
                    email: 'zhang@example.com',
                    sessionCount: 5,
                    firstSession: '2023-06-15',
                    lastSession: '2023-09-05',
                    nextSession: '2023-09-20',
                    tags: ['焦虑症', '工作压力', '需跟进'],
                    notes: '对工作压力很敏感，需要帮助建立应对机制'
                },
                {
                    id: 'c002',
                    name: '李先生',
                    gender: 'male',
                    age: 35,
                    phone: '139****5678',
                    email: 'li@example.com',
                    sessionCount: 3,
                    firstSession: '2023-07-20',
                    lastSession: '2023-09-01',
                    nextSession: null,
                    tags: ['抑郁症', '家庭问题'],
                    notes: '正在经历离婚，需情绪支持'
                },
                {
                    id: 'c003',
                    name: '王女士',
                    gender: 'female',
                    age: 42,
                    phone: '136****9012',
                    email: 'wang@example.com',
                    sessionCount: 8,
                    firstSession: '2023-03-10',
                    lastSession: '2023-08-28',
                    nextSession: '2023-09-18',
                    tags: ['慢性焦虑', '亲子关系'],
                    notes: '与青春期孩子存在沟通问题'
                },
                {
                    id: 'c004',
                    name: '赵先生',
                    gender: 'male',
                    age: 31,
                    phone: '135****3456',
                    email: 'zhao@example.com',
                    sessionCount: 2,
                    firstSession: '2023-08-05',
                    lastSession: '2023-08-19',
                    nextSession: '2023-09-15',
                    tags: ['职场适应', '社交压力'],
                    notes: '刚换工作，面临适应性挑战'
                },
                {
                    id: 'c005',
                    name: '陈女士',
                    gender: 'female',
                    age: 27,
                    phone: '137****7890',
                    email: 'chen@example.com',
                    sessionCount: 4,
                    firstSession: '2023-05-25',
                    lastSession: '2023-08-25',
                    nextSession: null,
                    tags: ['恋爱问题', '自我认同'],
                    notes: '走出失恋阴影，重建自我价值感'
                }
            ]
        }
    },
    computed: {
        filteredClients() {
            let result = [...this.clients];

            // 搜索过滤
            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase();
                result = result.filter(client =>
                    client.name.toLowerCase().includes(query) ||
                    client.phone.includes(query)
                );
            }

            // 标签过滤
            switch (this.activeFilter) {
                case 'recent':
                    // 最近30天内有咨询的客户
                    const thirtyDaysAgo = new Date();
                    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
                    result = result.filter(client => {
                        const lastSession = new Date(client.lastSession);
                        return lastSession >= thirtyDaysAgo;
                    });
                    break;
                case 'frequent':
                    // 咨询次数大于平均值的客户
                    const avgSessions = this.clients.reduce((sum, client) => sum + client.sessionCount, 0) / this.clients.length;
                    result = result.filter(client => client.sessionCount > avgSessions);
                    break;
                case 'followup':
                    // 标记为需要跟进的客户
                    result = result.filter(client =>
                        client.tags && client.tags.some(tag => tag.includes('跟进'))
                    );
                    break;
            }

            return result;
        },
        displayClients() {
            return this.filteredClients.slice(0, this.currentPage * this.pageSize);
        },
        hasMoreClients() {
            return this.displayClients.length < this.filteredClients.length;
        }
    },
    methods: {
        formatDate(dateString) {
            if (!dateString) return '无';

            const date = new Date(dateString);
            return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
        },
        setFilter(filter) {
            this.activeFilter = filter;
            this.currentPage = 1;
        },
        loadMore() {
            if (this.hasMoreClients) {
                this.currentPage++;
            }
        },
        getAvatarColor(name) {
            // 使用在data中定义的主题色
            const colors = [
                this.themeColors.primary,
                this.themeColors.error, 
                this.themeColors.success, 
                this.themeColors.info,
                '#9C27B0'  // 紫色
            ];

            let hash = 0;
            for (let i = 0; i < name.length; i++) {
                hash = name.charCodeAt(i) + ((hash << 5) - hash);
            }

            return colors[Math.abs(hash) % colors.length];
        },
        viewClientDetail(clientId) {
            // 导航到客户详情页
            uni.navigateTo({
                url: `/pages/counselor/clients/detail?id=${clientId}`
            });
        },
        callClient(phone) {
            // 打电话给客户
            uni.makePhoneCall({
                phoneNumber: phone.replace(/\*+/g, '0'), // 替换掉隐私保护的星号
                success: () => {
                    console.log('拨打电话成功');
                },
                fail: (err) => {
                    console.error('拨打电话失败', err);
                }
            });
        },
        messageClient(clientId) {
            // 导航到消息页面
            uni.navigateTo({
                url: `/pages/counselor/messages?clientId=${clientId}`
            });
        },
        scheduleAppointment(clientId) {
            // 导航到预约页面
            uni.navigateTo({
                url: `/pages/counselor/appointments/schedule?clientId=${clientId}`
            });
        },
        viewNotes(clientId) {
            // 导航到咨询记录页面
            uni.navigateTo({
                url: `/pages/counselor/clients/notes?clientId=${clientId}`
            });
        }
    }
}
</script>

<style lang="scss">
/* 直接定义主题色变量，不依赖于外部导入 */
:root {
  --mg-primary: #E2AA59;
  --mg-primary-dark: #D19845;
  --mg-primary-light: #F1C88B;
  --mg-primary-bg: #F9EFD6;
  
  --mg-accent: #E84C4C;
  --mg-accent-dark: #CC3939;
  --mg-accent-light: #F47878;
  
  --mg-black: #000000;
  --mg-white: #FFFFFF;
  
  --mg-success: #4CAF50;
  --mg-info: #2196F3;
  --mg-warning: #FF9800;
  --mg-error: #F44336;
}

.clients-container {
    padding: 30rpx;
    background-color: #f9f9f9;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.page-header {
    margin-bottom: 30rpx;
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-left: 20rpx;
}

.page-title {
    font-size: 40rpx;
    font-weight: bold;
    color: var(--mg-primary);
    position: relative;

    &::before {
        content: '';
        position: absolute;
        left: -20rpx;
        top: 50%;
        transform: translateY(-50%);
        width: 6rpx;
        height: 32rpx;
        background: var(--mg-primary);
        border-radius: 3rpx;
    }
}

.add-client-btn {
    background: var(--mg-primary);
    color: var(--mg-white);
    font-size: 28rpx;
    padding: 12rpx 30rpx;
    border-radius: 8rpx;
    border: none;
    transition: all 0.2s ease;

    &:hover {
        opacity: 0.9;
        transform: translateY(-2rpx);
    }
}

.search-filter-container {
    background-color: var(--mg-white);
    border-radius: 8rpx;
    padding: 20rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.search-box {
    height: 80rpx;
    position: relative;
    margin-bottom: 20rpx;
}

.search-input {
    background-color: #f5f5f5;
    border: 1px solid #eaeaea;
    height: 80rpx;
    border-radius: 6rpx;
    padding: 24rpx 70rpx 24rpx 24rpx;
    font-size: 28rpx;
    width: 100%;
    box-sizing: border-box;

    &:focus {
        border-color: var(--mg-primary);
        box-shadow: 0 0 0 2px rgba(226, 170, 89, 0.08);
    }
}

.search-icon {
    position: absolute;
    right: 24rpx;
    top: 50%;
    transform: translateY(-50%);
    color: #666666;
    font-size: 32rpx;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* 自定义图标 */
.icon-search {
    width: 36rpx;
    height: 36rpx;
    position: relative;

    &::before {
        content: '';
        position: absolute;
        width: 20rpx;
        height: 20rpx;
        border: 2rpx solid #666;
        border-radius: 50%;
        left: 4rpx;
        top: 4rpx;
    }

    &::after {
        content: '';
        position: absolute;
        width: 2rpx;
        height: 10rpx;
        background-color: #666;
        transform: rotate(-45deg);
        right: 8rpx;
        bottom: 8rpx;
        border-radius: 1rpx;
    }
}

.icon-phone {
    width: 30rpx;
    height: 30rpx;
    position: relative;

    &::before {
        content: '';
        position: absolute;
        width: 20rpx;
        height: 20rpx;
        border: 2rpx solid currentColor;
        border-radius: 4rpx;
        left: 4rpx;
        top: 5rpx;
        transform: rotate(45deg);
    }
}

.icon-message {
    width: 30rpx;
    height: 30rpx;
    position: relative;

    &::before {
        content: '';
        position: absolute;
        width: 24rpx;
        height: 16rpx;
        border: 2rpx solid currentColor;
        border-radius: 4rpx;
        left: 2rpx;
        top: 6rpx;
    }

    &::after {
        content: '';
        position: absolute;
        width: 0;
        height: 0;
        border-left: 6rpx solid transparent;
        border-right: 6rpx solid transparent;
        border-top: 6rpx solid currentColor;
        right: 6rpx;
        bottom: 4rpx;
    }
}

.icon-calendar {
    width: 30rpx;
    height: 30rpx;
    position: relative;

    &::before {
        content: '';
        position: absolute;
        width: 22rpx;
        height: 18rpx;
        border: 2rpx solid currentColor;
        border-radius: 2rpx;
        left: 3rpx;
        top: 7rpx;
    }

    &::after {
        content: '';
        position: absolute;
        width: 16rpx;
        height: 2rpx;
        background-color: currentColor;
        left: 7rpx;
        top: 12rpx;
    }
}

.icon-note {
    width: 30rpx;
    height: 30rpx;
    position: relative;

    &::before {
        content: '';
        position: absolute;
        width: 20rpx;
        height: 22rpx;
        border: 2rpx solid currentColor;
        border-radius: 2rpx;
        left: 4rpx;
        top: 4rpx;
    }

    &::after {
        content: '';
        position: absolute;
        width: 12rpx;
        height: 2rpx;
        background-color: currentColor;
        left: 8rpx;
        top: 10rpx;
        box-shadow: 0 5rpx 0 currentColor, 0 10rpx 0 currentColor;
    }
}

.filter-options {
    display: flex;
    flex-wrap: wrap;
    border-top: 1px solid #f0f0f0;
    padding-top: 20rpx;
}

.filter-item {
    padding: 8rpx 20rpx;
    margin-right: 15rpx;
    margin-bottom: 10rpx;
    font-size: 26rpx;
    color: #666666;
    background-color: #f5f5f5;
    border-radius: 4rpx;
    transition: all 0.2s ease;

    &.active {
        background-color: rgba(226, 170, 89, 0.1);
        color: var(--mg-primary);
        font-weight: 500;
    }

    &:hover:not(.active) {
        background-color: #eeeeee;
    }
}

.client-list-scroll {
    flex: 1;
}

.client-list {
    margin-bottom: 20rpx;
}

.client-card {
    background: var(--mg-white);
    border-radius: 8rpx;
    margin-bottom: 16rpx;
    padding: 24rpx;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    transition: all 0.2s ease;
    position: relative;
    border-left: 3px solid transparent;

    &:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left-color: var(--mg-primary);
    }

    &::after {
        content: "";
        position: absolute;
        top: 24rpx;
        right: 24rpx;
        width: 16rpx;
        height: 16rpx;
        border-top: 2px solid #ddd;
        border-right: 2px solid #ddd;
        transform: rotate(45deg);
    }
}

.client-info {
    display: flex;
    margin-bottom: 20rpx;
}

.client-avatar {
    width: 80rpx;
    height: 80rpx;
    border-radius: 8rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 20rpx;
    font-size: 32rpx;
    color: var(--mg-white);
    font-weight: bold;
    background: var(--mg-primary);
    flex-shrink: 0;
}

.client-details {
    flex: 1;
    padding-right: 30rpx;
}

.client-name-row {
    display: flex;
    align-items: center;
    margin-bottom: 10rpx;
    flex-wrap: wrap;
}

.client-name {
    font-size: 32rpx;
    font-weight: 600;
    color: #333333;
    margin-right: 12rpx;
}

.client-gender,
.client-age {
    font-size: 24rpx;
    padding: 2rpx 10rpx;
    border-radius: 4rpx;
    margin-right: 10rpx;
    background-color: #f5f5f5;
    color: #777777;
}

.client-contact {
    font-size: 26rpx;
    color: #777777;
    margin-bottom: 10rpx;
}

.client-stats {
    display: flex;
    flex-wrap: wrap;
}

.stat-item {
    font-size: 24rpx;
    color: #888888;
    margin-right: 20rpx;
    margin-bottom: 5rpx;
}

.stat-value {
    color: #555555;
    font-weight: 500;
}

.client-tags {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 20rpx;
}

.tag {
    font-size: 22rpx;
    padding: 4rpx 12rpx;
    margin-right: 10rpx;
    margin-bottom: 8rpx;
    border-radius: 4rpx;
    background-color: #f5f5f5;
    color: #666666;
}

.client-actions {
    display: flex;
    margin-top: 16rpx;
    border-top: 1px solid #f0f0f0;
    padding-top: 16rpx;
}

.action-button {
    display: flex;
    align-items: center;
    padding: 8rpx 16rpx;
    margin-right: 20rpx;
    border-radius: 4rpx;
    transition: all 0.2s ease;

    &:hover {
        background-color: #f5f5f5;
    }

    &.call {
        color: #3498db;
    }

    &.message {
        color: var(--mg-primary);
    }

    &.appointment {
        color: #27ae60;
    }

    &.notes {
        color: #e67e22;
    }
}

.action-icon {
    margin-right: 8rpx;
}

.action-text {
    font-size: 24rpx;
}

.load-more {
    padding: 30rpx 0;
    display: flex;
    justify-content: center;
}

.load-more-btn {
    padding: 12rpx 40rpx;
    background-color: #f5f5f5;
    color: #666666;
    border-radius: 4rpx;
    font-size: 26rpx;
    transition: all 0.2s ease;

    &:hover {
        background-color: #eeeeee;
        color: var(--mg-primary);
    }
}

.no-more {
    padding: 30rpx 0;
    text-align: center;
    color: #999999;
    font-size: 26rpx;
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80rpx 0;
    background: var(--mg-white);
    border-radius: 8rpx;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.empty-icon {
    width: 180rpx;
    height: 180rpx;
    margin-bottom: 30rpx;
    opacity: 0.6;
}

.empty-text {
    font-size: 28rpx;
    color: #888888;
    margin-bottom: 30rpx;
}

.empty-description {
    font-size: 24rpx;
    color: #999999;
}

// 媒体查询 - 针对小屏幕优化
@media screen and (max-width: 375px) {
    .filter-options {
        justify-content: space-between;
    }

    .filter-item {
        flex: 1;
        text-align: center;
        margin-right: 8rpx;
    }

    .client-stats {
        flex-direction: column;
    }

    .client-actions {
        flex-wrap: wrap;
    }

    .action-button {
        width: 50%;
        margin-bottom: 10rpx;
    }
}
</style>