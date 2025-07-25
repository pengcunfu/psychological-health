const {
  getResource
} = require('../../utils/util');

Component({
  properties: {
    // 标签页配置
    tabs: {
      type: Array,
      value: []
    },
    showBorder: {
      type: Boolean,
      value: true
    },
    safeArea: {
      type: Boolean,
      value: true
    }
  },

  data: {
    // 内部处理后的标签页配置
    tabList: [],
    // 当前激活的索引
    activeIndex: 0
  },

  observers: {
    'tabs': function (tabs) {
      this._processTabList(tabs);
    }
  },

  lifetimes: {
    attached() {
      this.updateActiveTab();
    }
  },

  pageLifetimes: {
    show() {
      // 页面显示时更新激活状态
      this.updateActiveTab();
    }
  },

  methods: {
    // 处理标签页配置，添加激活态图标
    _processTabList(tabs) {
      const tabList = tabs.map((tab, index) => {
        const icon = tab.icon || getResource(`images/tabbar/${tab.key || index}.png`);
        return {
          ...tab,
          icon,
          // 如果外部没有提供 activeIcon，则自动生成
          activeIcon: tab.activeIcon || icon.replace('.png', '-active.png'),
          isActive: index === this.data.activeIndex
        };
      });

      this.setData({
        tabList
      });
    },

    // 更新当前激活的标签
    updateActiveTab() {
      const currentPath = '/' + getCurrentPages().pop().route;
      const index = this.properties.tabs.findIndex(tab => tab.path === currentPath);
      if (index !== -1) {
        this.setData({
          activeIndex: index
        });
      }
    },

    // 处理标签点击
    handleTabClick(e) {
      const index = e.currentTarget.dataset.index;
      const tab = this.properties.tabs[index];

      // 更新激活状态
      this.setData({
        activeIndex: index
      });

      // 页面跳转
      wx.switchTab({
        url: tab.path,
        fail: (error) => {
          console.error('页面跳转失败:', error);
          wx.showToast({
            title: '页面跳转失败',
            icon: 'none'
          });
        }
      });
    }
  }
});