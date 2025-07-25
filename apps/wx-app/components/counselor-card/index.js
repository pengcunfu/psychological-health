Component({
  properties: {
    // 咨询师数据
    counselor: {
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
    // 是否显示在线状态
    showOnlineStatus: {
      type: Boolean,
      value: true
    },
    // 是否显示价格
    showPrice: {
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
    }
  },

  data: {
    isFavorited: false
  },

  lifetimes: {
    attached() {
      // 初始化收藏状态
      this.setData({
        isFavorited: this.data.counselor.isFavorited || false
      });
    }
  },

  observers: {
    'counselor.isFavorited': function (isFavorited) {
      this.setData({
        isFavorited: isFavorited || false
      });
    }
  },

  methods: {
    // 点击卡片
    onCardTap() {
      const counselor = this.data.counselor;
      if (counselor.id) {
        wx.navigateTo({
          url: `/pages/counselor/detail?id=${counselor.id}`,
          fail: (err) => {
            console.error('跳转咨询师详情失败:', err);
            wx.showToast({
              title: '页面跳转失败',
              icon: 'none'
            });
          }
        });
      }

      // 触发点击事件
      this.triggerEvent('cardclick', {
        counselor
      });
    },

    // 点击收藏按钮
    onFavoriteTap(e) {
      e.stopPropagation(); // 阻止事件冒泡

      const counselor = this.data.counselor;
      const newFavoriteStatus = !this.data.isFavorited;

      this.setData({
        isFavorited: newFavoriteStatus
      });

      // 触发收藏事件
      this.triggerEvent('favoritechange', {
        counselor,
        isFavorited: newFavoriteStatus
      });
    },

    // 点击咨询按钮
    onConsultTap(e) {
      e.stopPropagation(); // 阻止事件冒泡

      const counselor = this.data.counselor;

      // 检查咨询师是否在线
      if (!counselor.isOnline) {
        wx.showToast({
          title: '咨询师当前不在线',
          icon: 'none'
        });
        return;
      }

      // 跳转到预约页面
      wx.navigateTo({
        url: `/pages/appointment/book?counselorId=${counselor.id}`,
        fail: (err) => {
          console.error('跳转预约页面失败:', err);
          wx.showToast({
            title: '页面跳转失败',
            icon: 'none'
          });
        }
      });

      // 触发咨询事件
      this.triggerEvent('consultclick', {
        counselor
      });
    },

    // 格式化价格显示
    formatPrice(price) {
      if (!price) return '面议';
      return `¥${price}/次`;
    },

    // 格式化评分显示
    formatRating(rating) {
      if (!rating) return '暂无评分';
      return rating.toFixed(1);
    },

    // 格式化经验年限
    formatExperience(years) {
      if (!years) return '';
      return `从业${years}年`;
    },

    // 格式化咨询次数
    formatConsultCount(count) {
      if (!count) return '';
      if (count >= 10000) {
        return `咨询经验${Math.floor(count / 10000)}万+小时`;
      } else if (count >= 1000) {
        return `咨询经验${Math.floor(count / 1000)}千+小时`;
      } else {
        return `咨询经验${count}+小时`;
      }
    }
  }
});