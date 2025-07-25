Component({
  properties: {
    // 工作室数据
    workspace: {
      type: Object,
      value: {}
    },
    // 卡片模式：list(列表模式) | grid(网格模式)
    mode: {
      type: String,
      value: 'list'
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
    isFavorited: false
  },

  lifetimes: {
    attached() {
      // 初始化收藏状态
      this.setData({
        isFavorited: this.data.workspace.isFavorited || false
      });
    }
  },

  observers: {
    'workspace.isFavorited': function (isFavorited) {
      this.setData({
        isFavorited: isFavorited || false
      });
    }
  },

  methods: {
    // 点击卡片
    onCardTap() {
      const workspace = this.data.workspace;
      if (workspace.id) {
        wx.navigateTo({
          url: `/pages/workspace/detail?id=${workspace.id}`,
          fail: (err) => {
            console.error('跳转工作室详情失败:', err);
            wx.showToast({
              title: '页面跳转失败',
              icon: 'none'
            });
          }
        });
      }

      // 触发点击事件
      this.triggerEvent('cardclick', {
        workspace
      });
    },

    // 点击收藏按钮
    onFavoriteTap(e) {
      e.stopPropagation(); // 阻止事件冒泡

      const workspace = this.data.workspace;
      const newFavoriteStatus = !this.data.isFavorited;

      this.setData({
        isFavorited: newFavoriteStatus
      });

      // 触发收藏事件
      this.triggerEvent('favoritechange', {
        workspace,
        isFavorited: newFavoriteStatus
      });
    },

    // 点击预约按钮
    onBookTap(e) {
      e.stopPropagation(); // 阻止事件冒泡

      const workspace = this.data.workspace;

      // 检查工作室是否营业
      if (!workspace.isOpen) {
        wx.showToast({
          title: '工作室当前未营业',
          icon: 'none'
        });
        return;
      }

      // 跳转到预约页面
      wx.navigateTo({
        url: `/pages/appointment/workspace?workspaceId=${workspace.id}`,
        fail: (err) => {
          console.error('跳转预约页面失败:', err);
          wx.showToast({
            title: '页面跳转失败',
            icon: 'none'
          });
        }
      });

      // 触发预约事件
      this.triggerEvent('bookclick', {
        workspace
      });
    },

    // 点击导航按钮
    onNavigateTap(e) {
      e.stopPropagation(); // 阻止事件冒泡

      const workspace = this.data.workspace;

      if (!workspace.address) {
        wx.showToast({
          title: '地址信息不完整',
          icon: 'none'
        });
        return;
      }

      // 打开地图导航
      wx.openLocation({
        latitude: workspace.latitude || 0,
        longitude: workspace.longitude || 0,
        name: workspace.name,
        address: workspace.address,
        fail: (err) => {
          console.error('打开地图失败:', err);
          wx.showToast({
            title: '打开地图失败',
            icon: 'none'
          });
        }
      });

      // 触发导航事件
      this.triggerEvent('navigateclick', {
        workspace
      });
    },

    // 格式化距离显示
    formatDistance(distance) {
      if (!distance) return '';
      if (distance < 1000) {
        return `距你${distance}m`;
      } else {
        return `距你${(distance / 1000).toFixed(1)}km`;
      }
    },

    // 格式化评分显示
    formatRating(rating) {
      if (!rating) return '暂无评分';
      return rating.toFixed(1);
    },

    // 格式化营业时间
    formatBusinessHours(businessHours) {
      if (!businessHours) return '';
      return businessHours;
    },

    // 获取营业状态文本
    getBusinessStatusText(isOpen, businessHours) {
      if (isOpen) {
        return businessHours ? `营业中 ${businessHours}` : '营业中';
      } else {
        return businessHours ? `休息中 ${businessHours}` : '休息中';
      }
    },

    // 获取营业状态样式类
    getBusinessStatusClass(isOpen) {
      return isOpen ? 'workspace-card__status--open' : 'workspace-card__status--closed';
    }
  }
});