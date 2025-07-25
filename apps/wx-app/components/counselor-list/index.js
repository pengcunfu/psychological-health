const {
  getResource
} = require('../../utils/util')

Component({
  properties: {
    // 咨询师列表数据
    counselors: {
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
      value: '暂无咨询师'
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
    // 默认咨询师数据（用于演示）
    defaultCounselors: [{
        id: 1,
        name: '陈丽萍',
        title: '中级咨询师',
        avatar: getResource('images/counselors/counselor1.jpg'),
        qualification: '国家二级心理咨询师 中级心理治疗师 中级社会工作师',
        specialties: ['少儿发展', '情绪管理', '个人成长'],
        experienceYears: 17,
        consultCount: 5600,
        rating: 4.8,
        price: 600,
        isOnline: true,
        isFavorited: false
      },
      {
        id: 2,
        name: '岳平',
        title: '资深咨询师',
        avatar: getResource('images/counselors/counselor2.jpg'),
        qualification: '中国心理学会注册系统助理心理师（ZX-24-186）',
        specialties: ['情绪管理', '人际关系', '个人成长'],
        experienceYears: 12,
        consultCount: 4400,
        rating: 4.7,
        price: 700,
        isOnline: false,
        isFavorited: true
      },
      {
        id: 3,
        name: '魏丽分',
        title: '中级咨询师',
        avatar: getResource('images/counselors/counselor3.jpg'),
        qualification: '国家二级心理咨询师 中国心理学会临床与咨询心理学专业委员会会员',
        specialties: ['婚姻家庭', '情绪管理', '个人成长'],
        experienceYears: 14,
        consultCount: 4300,
        rating: 4.9,
        price: 650,
        isOnline: true,
        isFavorited: false
      },
      {
        id: 4,
        name: '李兵莉',
        title: '高级咨询师',
        avatar: getResource('images/counselors/counselor4.jpg'),
        qualification: '国家一级心理咨询师 中国心理学会注册助理心理师',
        specialties: ['情绪障碍', '亲子关系'],
        experienceYears: 13,
        consultCount: 2200,
        rating: 4.6,
        price: 800,
        isOnline: true,
        isFavorited: false
      }
    ]
  },

  lifetimes: {
    attached() {
      // 如果没有传入咨询师数据，使用默认数据
      if (!this.data.counselors || this.data.counselors.length === 0) {
        this.setData({
          counselors: this.data.defaultCounselors
        });
      }
    }
  },

  methods: {
    // 咨询师卡片点击事件
    onCounselorCardClick(e) {
      const {
        counselor
      } = e.detail;
      this.triggerEvent('counselorclick', {
        counselor
      });
    },

    // 收藏状态改变事件
    onFavoriteChange(e) {
      const {
        counselor,
        isFavorited
      } = e.detail;

      // 更新本地数据
      const counselors = this.data.counselors.map(item => {
        if (item.id === counselor.id) {
          return {
            ...item,
            isFavorited
          };
        }
        return item;
      });

      this.setData({
        counselors
      });

      // 触发收藏事件
      this.triggerEvent('favoritechange', {
        counselor: {
          ...counselor,
          isFavorited
        },
        isFavorited
      });
    },

    // 咨询按钮点击事件
    onConsultClick(e) {
      const {
        counselor
      } = e.detail;
      this.triggerEvent('consultclick', {
        counselor
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

    // 筛选咨询师
    filterCounselors(filters) {
      let filteredCounselors = [...this.data.counselors];

      // 按在线状态筛选
      if (filters.onlineOnly) {
        filteredCounselors = filteredCounselors.filter(counselor => counselor.isOnline);
      }

      // 按专长筛选
      if (filters.specialty) {
        filteredCounselors = filteredCounselors.filter(counselor =>
          counselor.specialties && counselor.specialties.includes(filters.specialty)
        );
      }

      // 按价格范围筛选
      if (filters.priceRange) {
        const [minPrice, maxPrice] = filters.priceRange;
        filteredCounselors = filteredCounselors.filter(counselor =>
          counselor.price >= minPrice && counselor.price <= maxPrice
        );
      }

      // 按评分筛选
      if (filters.minRating) {
        filteredCounselors = filteredCounselors.filter(counselor =>
          counselor.rating >= filters.minRating
        );
      }

      return filteredCounselors;
    },

    // 排序咨询师
    sortCounselors(sortBy) {
      const counselors = [...this.data.counselors];

      switch (sortBy) {
        case 'rating':
          counselors.sort((a, b) => (b.rating || 0) - (a.rating || 0));
          break;
        case 'price-asc':
          counselors.sort((a, b) => (a.price || 0) - (b.price || 0));
          break;
        case 'price-desc':
          counselors.sort((a, b) => (b.price || 0) - (a.price || 0));
          break;
        case 'experience':
          counselors.sort((a, b) => (b.experienceYears || 0) - (a.experienceYears || 0));
          break;
        case 'consult-count':
          counselors.sort((a, b) => (b.consultCount || 0) - (a.consultCount || 0));
          break;
        default:
          // 默认排序：在线优先，然后按评分
          counselors.sort((a, b) => {
            if (a.isOnline !== b.isOnline) {
              return b.isOnline - a.isOnline;
            }
            return (b.rating || 0) - (a.rating || 0);
          });
      }

      this.setData({
        counselors
      });
    }
  }
});