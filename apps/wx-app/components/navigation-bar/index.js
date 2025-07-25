Component({
  properties: {
    // 标题
    title: {
      type: String,
      value: ''
    },
    // 是否显示返回按钮
    showBack: {
      type: Boolean,
      value: true
    },
    // 背景色
    background: {
      type: String,
      value: '#ffffff'
    },
    // 字体颜色
    color: {
      type: String,
      value: '#000000'
    },
    // 是否固定在顶部
    fixed: {
      type: Boolean,
      value: true
    },
    // 自定义返回按钮图标
    backIcon: {
      type: String,
      value: ''
    },
    // 标题对齐方式
    titleAlign: {
      type: String,
      value: 'center'
    },
    // 自定义导航栏高度
    navHeight: {
      type: Number,
      value: 44
    },
    // 右侧按钮配置
    rightButtons: {
      type: Array,
      value: []
    },
    // 是否显示底部边框
    showBorder: {
      type: Boolean,
      value: true
    }
  },

  data: {
    statusBarHeight: 0,
    navBarHeight: 44,
    menuButtonInfo: null,
    systemInfo: null,
    ios: false
  },

  lifetimes: {
    attached() {
      this._initNavBar();
    },

    detached() {
      // 清理工作
      this.setData({
        menuButtonInfo: null,
        systemInfo: null
      });
    }
  },

  methods: {
    // 初始化导航栏
    _initNavBar() {
      try {
        // 获取系统信息
        const systemInfo = wx.getSystemInfoSync();
        const ios = !!(systemInfo.system.toLowerCase().search('ios') + 1);

        // 获取胶囊按钮位置信息
        const menuButtonInfo = wx.getMenuButtonBoundingClientRect();

        // 计算导航栏高度
        const navHeight = this.properties.navHeight ||
          (menuButtonInfo.height + (menuButtonInfo.top - systemInfo.statusBarHeight) * 2);

        this.setData({
          statusBarHeight: systemInfo.statusBarHeight,
          navBarHeight: navHeight,
          menuButtonInfo,
          systemInfo,
          ios
        });
      } catch (error) {
        console.error('导航栏初始化失败:', error);
        // 使用默认值
        this.setData({
          statusBarHeight: 20,
          navBarHeight: this.properties.navHeight || 44
        });
      }
    },

    // 返回上一页
    handleBack() {
      if (!this.data.showBack) return;

      const pages = getCurrentPages();
      if (pages.length > 1) {
        wx.navigateBack({
          delta: 1,
          fail: (err) => {
            console.error('返回上一页失败:', err);
            this.triggerEvent('backfail', err);
          }
        });
      } else {
        // 没有上一页时触发事件，由页面决定如何处理
        this.triggerEvent('backhome');
      }
    },

    // 点击标题
    handleTitleClick() {
      this.triggerEvent('titleclick');
    },

    // 点击右侧按钮
    handleRightButtonClick(e) {
      const index = e.currentTarget.dataset.index;
      const button = this.data.rightButtons[index];
      this.triggerEvent('rightbuttonclick', {
        index,
        button
      });
    }
  }
});