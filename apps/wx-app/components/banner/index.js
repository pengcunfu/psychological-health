Component({
  properties: {
    // 轮播图数据
    banners: {
      type: Array,
      value: []
    },
    // 是否自动播放
    autoplay: {
      type: Boolean,
      value: true
    },
    // 是否显示面板指示点
    indicatorDots: {
      type: Boolean,
      value: true
    },
    // 是否循环播放
    circular: {
      type: Boolean,
      value: true
    },
    // 自动切换时间间隔
    interval: {
      type: Number,
      value: 3000
    },
    // 滑动动画时长
    duration: {
      type: Number,
      value: 500
    }
  },

  methods: {
    // 点击轮播图
    onBannerTap(e) {
      const index = e.currentTarget.dataset.index;
      const banner = this.data.banners[index];
      if (banner.link) {
        wx.navigateTo({
          url: banner.link
        });
      }
      // 触发点击事件，让父组件也能处理点击
      this.triggerEvent('click', {
        banner,
        index
      });
    }
  }
});