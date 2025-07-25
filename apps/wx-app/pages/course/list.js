Page({
  data: {
    searchText: '',
    currentCity: 'all',
    cityList: [
      { name: '全国', value: 'all' },
      { name: '北京', value: 'beijing' },
      { name: '上海', value: 'shanghai' },
      { name: '广州', value: 'guangzhou' },
      { name: '深圳', value: 'shenzhen' },
      { name: '成都', value: 'chengdu' }
    ],
    courseList: [
      {
        id: '1',
        title: '情绪管理与心理健康',
        imageColor: '#F1C88B',
        tags: ['认知行为疗法', '情绪管理'],
        lessons: 12,
        duration: 3,
        price: 299
      },
      {
        id: '2',
        title: '人际关系修复与提升',
        imageColor: '#F47878',
        tags: ['人际关系', '沟通技巧'],
        lessons: 8,
        duration: 2,
        price: 199
      },
      {
        id: '3',
        title: '压力管理与减压技巧',
        imageColor: '#E2AA59',
        tags: ['减压', '职场压力'],
        lessons: 10,
        duration: 2.5,
        price: 259
      },
      {
        id: '4',
        title: '青少年心理健康教育',
        imageColor: '#D19845',
        tags: ['青少年', '亲子关系'],
        lessons: 15,
        duration: 4,
        price: 399
      }
    ]
  },

  onLoad() {
    console.log('课程页面加载');
    this.loadCourseList();
  },

  // 切换城市
  selectCity(e) {
    const city = e.currentTarget.dataset.city;
    this.setData({
      currentCity: city
    });
    this.loadCourseList();
  },

  // 切换筛选条件
  toggleFilter(e) {
    const filterType = e.currentTarget.dataset.type;
    console.log('切换筛选条件:', filterType);
    // TODO: 实现筛选逻辑
  },

  // 搜索功能
  goToSearch(e) {
    const searchText = e.detail.value;
    console.log('搜索内容:', searchText);
    // TODO: 实现搜索逻辑
  },

  // 跳转到课程详情页
  navigateToCourseDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/course/detail/detail?id=${id}`
    });
  },

  // 加载课程列表
  async loadCourseList() {
    try {
      const { currentCity } = this.data;
      // TODO: Replace with actual API call
      const res = await wx.cloud.callFunction({
        name: 'getCourseList',
        data: { city: currentCity }
      });

      if (res.result && res.result.data) {
        this.setData({
          courseList: res.result.data
        });
      }
    } catch (error) {
      console.error('加载课程列表失败:', error);
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    }
  },

  // 加载更多
  loadMore() {
    console.log('加载更多课程');
    // TODO: 实现加载更多逻辑
  }
}); 