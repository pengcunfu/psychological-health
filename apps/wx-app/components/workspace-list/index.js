const {
  getResource
} = require('../../utils/util')

Component({
  properties: {
    // 工作室列表数据
    workspaces: {
      type: Array,
      value: []
    },
    // 显示模式：list(列表) | grid(网格)
    mode: {
      type: String,
      value: 'list'
    },
    // 网格模式下每行显示的列数
    columns: {
      type: Number,
      value: 2
    },
    // 是否显示加载更多
    showLoadMore: {
      type: Boolean,
      value: false
    },
    // 是否正在加载
    loading: {
      type: Boolean,
      value: false
    },
    // 是否已加载完毕
    finished: {
      type: Boolean,
      value: false
    },
    // 空状态文案
    emptyText: {
      type: String,
      value: '暂无工作室'
    },
    // 是否显示收藏按钮
    showFavorite: {
      type: Boolean,
      value: true
    },
    // 是否显示营业状态
    showBusinessStatus: {
      type: Boolean,
      value: true
    },
    // 是否显示距离
    showDistance: {
      type: Boolean,
      value: true
    },
    // 是否显示评分
    showRating: {
      type: Boolean,
      value: true
    },
    // 是否显示标签
    showTags: {
      type: Boolean,
      value: true
    },
    // 是否显示营业时间
    showBusinessHours: {
      type: Boolean,
      value: true
    }
  },

  data: {
    // 默认工作室数据（用于演示）
    defaultWorkspaces: [{
        id: 1,
        name: '武汉心理工作室',
        image: getResource('images/workspaces/workspace1.jpg'),
        address: '武汉市武昌区黄鹤楼街道某某国际',
        businessHours: '周三至周日 9:00-18:00',
        todayHours: '9:00-18:00',
        services: ['个人咨询', '团体咨询', '心理测评'],
        rating: 4.8,
        distance: 3400,
        isOpen: true,
        isFavorited: false,
        latitude: 30.5728,
        longitude: 114.3055
      },
      {
        id: 2,
        name: '南京心理工作室',
        image: getResource('images/workspaces/workspace2.jpg'),
        address: '南京市鼓楼区云南路20-1号',
        businessHours: '周一至周日 9:00-12:30, 13:00-17:00',
        todayHours: '9:00-12:30, 13:00-17:00',
        services: ['情绪管理', '人际关系', '职场心理'],
        rating: 4.7,
        distance: 79100,
        isOpen: false,
        isFavorited: true,
        latitude: 32.0603,
        longitude: 118.7969
      },
      {
        id: 3,
        name: '杭州心理工作室',
        image: getResource('images/workspaces/workspace3.jpg'),
        address: '杭州市西湖区文三路508号天苑大厦',
        businessHours: '周一至周日 9:30-17:30',
        todayHours: '9:30-17:30',
        services: ['婚姻家庭', '青少年心理', '焦虑抑郁'],
        rating: 4.9,
        distance: 599200,
        isOpen: true,
        isFavorited: false,
        latitude: 30.2741,
        longitude: 120.1551
      },
      {
        id: 4,
        name: '上海中山公园心理工作室',
        image: getResource('images/workspaces/workspace4.jpg'),
        address: '上海市长宁区长宁路1027号兆丰广场',
        businessHours: '周一至周日 9:00-18:00; 18点后线上可正常预约',
        todayHours: '9:00-18:00',
        services: ['认知行为治疗', '精神分析', '家庭治疗'],
        rating: 4.6,
        distance: 716500,
        isOpen: true,
        isFavorited: false,
        latitude: 31.2304,
        longitude: 121.4737
      },
      {
        id: 5,
        name: '上海浦东心理工作室',
        image: getResource('images/workspaces/workspace5.jpg'),
        address: '上海市浦东新区南山路538号中港汇',
        businessHours: '周一至周日 9:00-18:00; 18点后线上可正常预约',
        todayHours: '9:00-18:00',
        services: ['儿童心理', '学习障碍', '注意力训练'],
        rating: 4.5,
        distance: 729800,
        isOpen: true,
        isFavorited: false,
        latitude: 31.2304,
        longitude: 121.4737
      },
      {
        id: 6,
        name: '厦门心理工作室',
        image: getResource('images/workspaces/workspace6.jpg'),
        address: '厦门市思明区湖滨南路连兴大厦',
        businessHours: '周一至周日 9:00 - 18:00',
        todayHours: '9:00-18:00',
        services: ['沙盘游戏', '艺术治疗', '音乐治疗'],
        rating: 4.8,
        distance: 818000,
        isOpen: false,
        isFavorited: false,
        latitude: 24.4798,
        longitude: 118.0819
      }
    ]
  },

  lifetimes: {
    attached() {
      // 如果没有传入工作室数据，使用默认数据
      if (!this.data.workspaces || this.data.workspaces.length === 0) {
        this.setData({
          workspaces: this.data.defaultWorkspaces
        });
      }
    }
  },

  methods: {
    // 工作室卡片点击事件
    onWorkspaceCardClick(e) {
      const {
        workspace
      } = e.detail;
      this.triggerEvent('workspaceclick', {
        workspace
      });
    },

    // 收藏状态改变事件
    onFavoriteChange(e) {
      const {
        workspace,
        isFavorited
      } = e.detail;

      // 更新本地数据
      const workspaces = this.data.workspaces.map(item => {
        if (item.id === workspace.id) {
          return {
            ...item,
            isFavorited
          };
        }
        return item;
      });

      this.setData({
        workspaces
      });

      // 触发收藏事件
      this.triggerEvent('favoritechange', {
        workspace: {
          ...workspace,
          isFavorited
        },
        isFavorited
      });
    },

    // 预约按钮点击事件
    onBookClick(e) {
      const {
        workspace
      } = e.detail;
      this.triggerEvent('bookclick', {
        workspace
      });
    },

    // 导航按钮点击事件
    onNavigateClick(e) {
      const {
        workspace
      } = e.detail;
      this.triggerEvent('navigateclick', {
        workspace
      });
    },

    // 加载更多
    onLoadMore() {
      if (this.data.loading || this.data.finished) {
        return;
      }

      this.triggerEvent('loadmore');
    },

    // 下拉刷新
    onRefresh() {
      this.triggerEvent('refresh');
    },

    // 筛选工作室
    filterWorkspaces(filters) {
      let filteredWorkspaces = [...this.data.workspaces];

      // 按营业状态筛选
      if (filters.openOnly) {
        filteredWorkspaces = filteredWorkspaces.filter(workspace => workspace.isOpen);
      }

      // 按服务类型筛选
      if (filters.service) {
        filteredWorkspaces = filteredWorkspaces.filter(workspace =>
          workspace.services && workspace.services.includes(filters.service)
        );
      }

      // 按距离筛选
      if (filters.maxDistance) {
        filteredWorkspaces = filteredWorkspaces.filter(workspace =>
          workspace.distance <= filters.maxDistance
        );
      }

      // 按评分筛选
      if (filters.minRating) {
        filteredWorkspaces = filteredWorkspaces.filter(workspace =>
          workspace.rating >= filters.minRating
        );
      }

      return filteredWorkspaces;
    },

    // 排序工作室
    sortWorkspaces(sortBy) {
      const workspaces = [...this.data.workspaces];

      switch (sortBy) {
        case 'distance':
          workspaces.sort((a, b) => (a.distance || 0) - (b.distance || 0));
          break;
        case 'rating':
          workspaces.sort((a, b) => (b.rating || 0) - (a.rating || 0));
          break;
        case 'name':
          workspaces.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
          break;
        default:
          // 默认排序：营业中优先，然后按距离
          workspaces.sort((a, b) => {
            if (a.isOpen !== b.isOpen) {
              return b.isOpen - a.isOpen;
            }
            return (a.distance || 0) - (b.distance || 0);
          });
      }

      this.setData({
        workspaces
      });
    },

    // 获取附近工作室
    getNearbyWorkspaces(latitude, longitude, radius = 5000) {
      const workspaces = this.data.workspaces.filter(workspace => {
        if (!workspace.latitude || !workspace.longitude) return false;

        // 简单的距离计算（实际项目中应使用更精确的地理距离计算）
        const distance = this.calculateDistance(
          latitude, longitude,
          workspace.latitude, workspace.longitude
        );

        return distance <= radius;
      });

      return workspaces;
    },

    // 计算两点间距离（简化版本）
    calculateDistance(lat1, lon1, lat2, lon2) {
      const R = 6371000; // 地球半径（米）
      const dLat = (lat2 - lat1) * Math.PI / 180;
      const dLon = (lon2 - lon1) * Math.PI / 180;
      const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      return R * c;
    }
  }
});