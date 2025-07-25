const { getResource } = require('../../utils/util')
const { homeData, apiResponses } = require('./data')

Page({
  data: {
    // 页面状态
    isRefreshing: false,
    isLoading: false,
    
    // 首页数据
    banners: [],
    notification: '',
    categories: [],
    counselors: [],
    announcements: [],
    hotSearchKeywords: [],

    // 筛选相关数据
    activeFilter: '', // 当前激活的筛选类型
    showFilterPopup: false, // 是否显示筛选弹出层

    // 筛选选项数据
    selectedCity: '',
    selectedTime: '',
    selectedPrice: '',
    selectedSort: '',
    selectedFilters: {
      consultType: [],
      consultMethod: [],
      experience: [],
      gender: []
    },

    // 选项列表
    cities: [],
    timeOptions: [],
    priceOptions: [],
    sortOptions: [],
    filterOptions: [],

    // 滚动相关
    isFilterSticky: false,
    hideTopSection: false,
    scrollTop: 0,
    lastScrollTop: 0
  },

  onLoad() {
    // 初始化页面数据
    this.initPageData();
    // 加载首页数据
    this.loadPageData();
  },

  // 初始化页面数据
  initPageData() {
    this.setData({
      cities: homeData.cities,
      timeOptions: homeData.timeOptions,
      priceOptions: homeData.priceOptions,
      sortOptions: homeData.sortOptions,
      filterOptions: homeData.filterOptions,
      selectedCity: homeData.cities[0] // 默认选择第一个城市
    });
  },

  // 加载页面数据
  async loadPageData() {
    try {
      this.setData({ isLoading: true });
      
      // 使用模拟API获取首页数据
      const response = await apiResponses.getHomeData();
      
      if (response.code === 200) {
        const data = response.data;
        this.setData({
          banners: data.banners,
          notification: data.notification,
          categories: data.categories,
          counselors: data.counselors,
          announcements: data.announcements,
          hotSearchKeywords: data.hotSearchKeywords
        });
      } else {
        wx.showToast({
          title: '数据加载失败',
          icon: 'none'
        });
      }
    } catch (error) {
      console.error('加载首页数据失败:', error);
      wx.showToast({
        title: '网络错误',
        icon: 'none'
      });
    } finally {
      this.setData({ isLoading: false });
    }
  },

  // 下拉刷新
  onRefresh() {
    if (this.data.isRefreshing) {
      return;
    }

    this.setData({
      isRefreshing: true
    });

    // 模拟刷新
    setTimeout(() => {
      this.loadPageData();
      this.setData({
        isRefreshing: false
      });
    }, 1000);
  },

  // 标签页切换事件
  handleTabChange(e) {
    const index = e.detail.index;
    this.setData({
      activeTabIndex: index
    });
  },

  // 滑动切换事件
  handleSwiperChange(e) {
    const index = e.detail.current;
    this.setData({
      activeTabIndex: index
    });
  },

  // 搜索框输入
  onSearchInput(e) {
    const value = e.detail.value;
    console.log('搜索内容：', value);
    // 实现搜索逻辑
  },

  // 点击分类
  onCategoryTap(e) {
    const id = e.currentTarget.dataset.id;
    const category = this.data.categories.find(item => item.id === id);
    if (category) {
      wx.navigateTo({
        url: `/pages/counselor/index?category=${category.name}`
      });
    }
  },

  // 点击更多
  onMoreTap() {
    wx.navigateTo({
      url: '/pages/counselor/index'
    });
  },

  // 点击咨询师
  onCounselorTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/counselor/detail?id=${id}`
    });
  },

  goLogin() {
    wx.navigateTo({
      url: '/pages/login/login'
    });
  },
  goRegister() {
    wx.navigateTo({
      url: '/pages/login/register'
    });
  },
  goProfile() {
    wx.navigateTo({
      url: '/pages/profile/index'
    });
  },
  goCourse() {
    wx.navigateTo({
      url: '/pages/course/index'
    });
  },
  goOrder() {
    wx.navigateTo({
      url: '/pages/order/index'
    });
  },
  goCounselor() {
    wx.navigateTo({
      url: '/pages/counselor/index'
    });
  },

  // 标签页切换
  onTabChange(e) {
    const {
      index,
      tab
    } = e.detail;
    console.log('切换到标签页:', tab.text);
  },

  // 点击预约按钮
  onBookTap(e) {
    const counselorId = e.currentTarget.dataset.counselorId;
    wx.navigateTo({
      url: `/pages/appointment/index?counselorId=${counselorId}`
    });
  },

  // 点击筛选项
  onFilterTap(e) {
    const type = e.currentTarget.dataset.type;

    if (this.data.activeFilter === type) {
      this.setData({
        activeFilter: '',
        showFilterPopup: false
      });
    } else {
      this.setData({
        activeFilter: type,
        showFilterPopup: true
      });
    }
  },

  // 点击遮罩层
  onMaskTap() {
    this.setData({
      activeFilter: '',
      showFilterPopup: false
    });
  },

  // 选择城市
  onCitySelect(e) {
    const city = e.currentTarget.dataset.city;
    this.setData({
      selectedCity: city,
      activeFilter: '',
      showFilterPopup: false
    });
    this.applyFilters();
  },

  // 选择时间
  onTimeSelect(e) {
    const time = e.currentTarget.dataset.time;
    this.setData({
      selectedTime: time,
      activeFilter: '',
      showFilterPopup: false
    });
    this.applyFilters();
  },

  // 选择价格
  onPriceSelect(e) {
    const price = e.currentTarget.dataset.price;
    this.setData({
      selectedPrice: price,
      activeFilter: '',
      showFilterPopup: false
    });
    this.applyFilters();
  },

  // 选择排序方式
  onSortSelect(e) {
    const sort = e.currentTarget.dataset.sort;
    this.setData({
      selectedSort: sort,
      activeFilter: '',
      showFilterPopup: false
    });
    this.applyFilters();
  },

  // 选择筛选选项
  onFilterOptionSelect(e) {
    const {
      group,
      value
    } = e.currentTarget.dataset;
    const selectedFilters = {
      ...this.data.selectedFilters
    };
    const index = selectedFilters[group].indexOf(value);

    if (index > -1) {
      selectedFilters[group].splice(index, 1);
    } else {
      selectedFilters[group].push(value);
    }

    this.setData({
      selectedFilters
    });
  },

  // 重置筛选
  onFilterReset() {
    this.setData({
      selectedFilters: {
        consultType: [],
        consultMethod: [],
        experience: []
      }
    });
  },

  // 确认筛选
  onFilterConfirm() {
    this.setData({
      activeFilter: '',
      showFilterPopup: false
    });
    this.applyFilters();
  },

  // 应用筛选条件
  async applyFilters() {
    try {
      this.setData({ isLoading: true });
      
      const params = {
        city: this.data.selectedCity,
        time: this.data.selectedTime,
        price: this.data.selectedPrice,
        sort: this.data.selectedSort,
        filters: this.data.selectedFilters,
        page: 1,
        pageSize: 20
      };
      
      console.log('应用筛选条件：', params);
      
      // 调用模拟API获取筛选后的咨询师列表
      const response = await apiResponses.getCounselorList(params);
      
      if (response.code === 200) {
        this.setData({
          counselors: response.data.list
        });
        
        // 显示筛选结果提示
        if (response.data.list.length === 0) {
          wx.showToast({
            title: '暂无符合条件的咨询师',
            icon: 'none'
          });
        }
      } else {
        wx.showToast({
          title: '筛选失败',
          icon: 'none'
        });
      }
    } catch (error) {
      console.error('筛选咨询师失败:', error);
      wx.showToast({
        title: '网络错误',
        icon: 'none'
      });
    } finally {
      this.setData({ isLoading: false });
    }
  },

  // 跳转到搜索页面
  goSearch() {
    wx.navigateTo({
      url: '/pages/search/index'
    });
  },

  // 搜索咨询师
  async searchCounselors(keyword) {
    try {
      this.setData({ isLoading: true });
      
      const response = await apiResponses.searchCounselors(keyword);
      
      if (response.code === 200) {
        this.setData({
          counselors: response.data.list
        });
        
        if (response.data.list.length === 0) {
          wx.showToast({
            title: '未找到相关咨询师',
            icon: 'none'
          });
        }
      }
    } catch (error) {
      console.error('搜索失败:', error);
      wx.showToast({
        title: '搜索失败',
        icon: 'none'
      });
    } finally {
      this.setData({ isLoading: false });
    }
  },

  // 重置所有筛选条件
  resetAllFilters() {
    this.setData({
      selectedCity: this.data.cities[0],
      selectedTime: '',
      selectedPrice: '',
      selectedSort: '',
      selectedFilters: {
        consultType: [],
        consultMethod: [],
        experience: [],
        gender: []
      },
      activeFilter: '',
      showFilterPopup: false
    });
    
    // 重新加载数据
    this.loadPageData();
  },

  // 收藏咨询师
  onFavoriteTap(e) {
    const counselorId = e.currentTarget.dataset.counselorId;
    const counselors = this.data.counselors.map(counselor => {
      if (counselor.id === counselorId) {
        counselor.isFavorite = !counselor.isFavorite;
        wx.showToast({
          title: counselor.isFavorite ? '已收藏' : '已取消收藏',
          icon: 'success'
        });
      }
      return counselor;
    });
    
    this.setData({ counselors });
  },

  // 轮播图点击事件
  onBannerClick(e) {
    const { banner, index } = e.detail;
    console.log('点击轮播图:', banner, '索引:', index);
  },

  onScroll(e) {
    const scrollTop = e.detail.scrollTop;
    const lastScrollTop = this.data.lastScrollTop;
    const threshold = 300; // 可以根据实际内容调整这个值

    // 判断滚动方向
    if (scrollTop > lastScrollTop) {
      // 向上滚动
      if (scrollTop > threshold && !this.data.hideTopSection) {
        this.setData({
          hideTopSection: true,
          isFilterSticky: true
        });
      }
    } else {
      // 向下滚动
      if (scrollTop <= threshold && this.data.hideTopSection) {
        this.setData({
          hideTopSection: false,
          isFilterSticky: false
        });
      }
    }

    // 更新上次滚动位置
    this.setData({
      lastScrollTop: scrollTop
    });
  },
});