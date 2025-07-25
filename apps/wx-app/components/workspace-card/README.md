# 工作室组件使用文档

本文档介绍了心理健康应用中的工作室卡片组件（`workspace-card`）和工作室列表组件（`workspace-list`）的使用方法。

## 组件概述

### workspace-card（工作室卡片组件）
工作室卡片组件用于展示单个工作室的详细信息，支持列表和网格两种显示模式。

### workspace-list（工作室列表组件）
工作室列表组件用于展示多个工作室卡片，提供完整的列表管理功能。

## 功能特性

### 🎨 多种显示模式
- **列表模式**：适合详细信息展示
- **网格模式**：适合紧凑布局展示

### 📍 位置服务
- 显示工作室距离用户的实际距离
- 支持导航功能，可跳转到地图应用
- 自动获取用户位置进行距离计算

### ⭐ 交互功能
- 收藏/取消收藏工作室
- 在线预约功能
- 工作室详情查看
- 营业状态实时显示

### 🏷️ 信息展示
- 工作室基本信息（名称、地址、图片）
- 营业时间和营业状态
- 服务标签和特色
- 用户评分和评价
- 距离和导航信息

## workspace-card 属性配置

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| workspace | Object | {} | 工作室数据对象 |
| mode | String | 'list' | 显示模式：'list' 或 'grid' |
| showFavorite | Boolean | true | 是否显示收藏按钮 |
| showBusinessStatus | Boolean | true | 是否显示营业状态 |
| showDistance | Boolean | true | 是否显示距离信息 |
| showRating | Boolean | true | 是否显示评分 |
| showTags | Boolean | true | 是否显示服务标签 |
| showBusinessHours | Boolean | true | 是否显示营业时间 |

## workspace-list 属性配置

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| workspaces | Array | [] | 工作室数据数组 |
| mode | String | 'list' | 显示模式：'list' 或 'grid' |
| columns | Number | 2 | 网格模式下的列数 |
| showLoadMore | Boolean | true | 是否显示加载更多 |
| loading | Boolean | false | 是否正在加载 |
| finished | Boolean | false | 是否已加载完毕 |
| emptyText | String | '暂无工作室' | 空状态提示文字 |
| showFavorite | Boolean | true | 是否显示收藏功能 |
| showBusinessStatus | Boolean | true | 是否显示营业状态 |
| showDistance | Boolean | true | 是否显示距离 |
| showRating | Boolean | true | 是否显示评分 |
| showTags | Boolean | true | 是否显示标签 |
| showBusinessHours | Boolean | true | 是否显示营业时间 |

## 事件回调

### workspace-card 事件

| 事件名 | 参数 | 说明 |
|--------|------|------|
| cardclick | {workspace} | 卡片点击事件 |
| favoritechange | {workspace, isFavorite} | 收藏状态改变 |
| bookclick | {workspace} | 预约按钮点击 |
| navigateclick | {workspace} | 导航按钮点击 |

### workspace-list 事件

| 事件名 | 参数 | 说明 |
|--------|------|------|
| workspacecardclick | {workspace} | 工作室卡片点击 |
| favoritechange | {workspace, isFavorite} | 收藏状态改变 |
| bookclick | {workspace} | 预约按钮点击 |
| navigateclick | {workspace} | 导航按钮点击 |
| loadmore | {} | 加载更多事件 |
| refresh | {} | 下拉刷新事件 |
| filter | {filters} | 筛选事件 |
| sort | {sortType} | 排序事件 |

## 数据格式

### 工作室数据结构

```javascript
{
  id: 1,
  name: '武汉心理工作室',
  address: '武汉市武昌区徐东大街水岸国际',
  image: '/images/workspace1.jpg',
  distance: 5.4, // 距离（公里）
  rating: 4.8, // 评分
  reviewCount: 128, // 评价数量
  isOpen: true, // 是否营业
  businessHours: '周一至周日 9:00-18:00',
  tags: ['个人咨询', '家庭治疗', '青少年心理'],
  isFavorite: false, // 是否已收藏
  latitude: 30.5728, // 纬度
  longitude: 114.3048, // 经度
  phone: '027-88888888',
  description: '专业的心理健康服务机构',
  services: [
    {
      name: '个人心理咨询',
      price: 200,
      duration: 50
    }
  ]
}
```

## 使用示例

### 1. 基础使用

```json
// page.json
{
  "usingComponents": {
    "workspace-card": "/components/workspace-card/index",
    "workspace-list": "/components/workspace-list/index"
  }
}
```

```xml
<!-- page.wxml -->
<!-- 单个工作室卡片 -->
<workspace-card
  workspace="{{workspaceData}}"
  mode="list"
  bind:cardclick="onWorkspaceClick"
  bind:favoritechange="onFavoriteChange"
  bind:bookclick="onBookClick"
  bind:navigateclick="onNavigateClick"
/>

<!-- 工作室列表 -->
<workspace-list
  workspaces="{{workspaceList}}"
  mode="grid"
  columns="2"
  show-load-more="{{true}}"
  loading="{{loading}}"
  finished="{{finished}}"
  bind:workspacecardclick="onWorkspaceClick"
  bind:favoritechange="onFavoriteChange"
  bind:loadmore="onLoadMore"
  bind:refresh="onRefresh"
/>
```

### 2. 页面集成示例

```javascript
// page.js
Page({
  data: {
    workspaceList: [],
    loading: false,
    finished: false,
    page: 1
  },

  onLoad() {
    this.loadWorkspaces();
  },

  // 加载工作室列表
  async loadWorkspaces() {
    this.setData({ loading: true });
    
    try {
      const res = await api.getWorkspaces({
        page: this.data.page,
        limit: 10
      });
      
      const newList = this.data.page === 1 ? res.data : [...this.data.workspaceList, ...res.data];
      
      this.setData({
        workspaceList: newList,
        loading: false,
        finished: res.data.length < 10
      });
    } catch (error) {
      this.setData({ loading: false });
      wx.showToast({ title: '加载失败', icon: 'none' });
    }
  },

  // 工作室卡片点击
  onWorkspaceClick(e) {
    const { workspace } = e.detail;
    wx.navigateTo({
      url: `/pages/workspace-detail/index?id=${workspace.id}`
    });
  },

  // 收藏状态改变
  async onFavoriteChange(e) {
    const { workspace, isFavorite } = e.detail;
    
    try {
      if (isFavorite) {
        await api.favoriteWorkspace(workspace.id);
      } else {
        await api.unfavoriteWorkspace(workspace.id);
      }
      
      // 更新本地数据
      const workspaceList = this.data.workspaceList.map(item => {
        if (item.id === workspace.id) {
          return { ...item, isFavorite };
        }
        return item;
      });
      
      this.setData({ workspaceList });
      
      wx.showToast({
        title: isFavorite ? '收藏成功' : '取消收藏',
        icon: 'success'
      });
    } catch (error) {
      wx.showToast({ title: '操作失败', icon: 'none' });
    }
  },

  // 预约点击
  onBookClick(e) {
    const { workspace } = e.detail;
    wx.navigateTo({
      url: `/pages/booking/index?workspaceId=${workspace.id}`
    });
  },

  // 导航点击
  onNavigateClick(e) {
    const { workspace } = e.detail;
    wx.openLocation({
      latitude: workspace.latitude,
      longitude: workspace.longitude,
      name: workspace.name,
      address: workspace.address
    });
  },

  // 加载更多
  onLoadMore() {
    if (!this.data.loading && !this.data.finished) {
      this.setData({ page: this.data.page + 1 });
      this.loadWorkspaces();
    }
  },

  // 下拉刷新
  onRefresh() {
    this.setData({ page: 1 });
    this.loadWorkspaces();
  }
});
```

## 样式定制

### 自定义主题色

```css
/* 在页面样式中覆盖组件样式 */
.workspace-card {
  --primary-color: #your-color;
  --border-radius: 16rpx;
  --shadow-color: rgba(0, 0, 0, 0.1);
}
```

### 响应式布局

组件已内置响应式设计，会根据屏幕尺寸自动调整：
- 小屏设备：减少内边距，调整字体大小
- 网格模式：自动适配列数和间距
- 深色模式：自动适配颜色主题

## 注意事项

1. **位置权限**：使用距离功能需要获取用户位置权限
2. **图片资源**：确保工作室图片资源可访问
3. **数据格式**：严格按照文档中的数据格式传入
4. **性能优化**：大列表建议使用虚拟滚动或分页加载
5. **错误处理**：建议在事件回调中添加错误处理逻辑
6. **网络状态**：考虑网络异常情况的用户体验

## 更新日志

### v1.0.0
- 初始版本发布
- 支持列表和网格两种显示模式
- 完整的工作室信息展示
- 收藏、预约、导航等交互功能
- 响应式设计和深色模式支持