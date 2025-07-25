const { getResource } = require('../../utils/util')

// 首页测试数据
const homeData = {
  // 轮播图数据
  banners: [
    {
      id: 1,
      image: getResource('images/banner1.jpg'),
      title: '专业心理咨询服务',
      subtitle: '让心灵得到专业的呵护',
      link: '/pages/activity/detail?id=1'
    },
    {
      id: 2,
      image: getResource('images/banner2.jpg'),
      title: '情感问题专家解答',
      subtitle: '重新找回内心的平静',
      link: '/pages/activity/detail?id=2'
    },
    {
      id: 3,
      image: getResource('images/banner3.jpg'),
      title: '职业规划指导',
      subtitle: '规划人生，成就未来',
      link: '/pages/activity/detail?id=3'
    }
  ],

  // 预约提醒
  notification: '您有一个预约咨询即将开始，请注意查看',

  // 咨询类型分类
  categories: [
    {
      id: 1,
      name: '个人成长',
      icon: getResource('images/op1.svg'),
      description: '自我认知与提升',
      path: '/pages/counselor/index?category=个人成长'
    },
    {
      id: 2,
      name: '情感咨询',
      icon: getResource('images/op2.svg'),
      description: '恋爱婚姻情感问题',
      path: '/pages/counselor/index?category=情感咨询'
    },
    {
      id: 3,
      name: '职业规划',
      icon: getResource('images/op3.svg'),
      description: '职场发展与规划',
      path: '/pages/counselor/index?category=职业规划'
    },
    {
      id: 4,
      name: '家庭关系',
      icon: getResource('images/op4.svg'),
      description: '亲子关系与家庭和谐',
      path: '/pages/counselor/index?category=家庭关系'
    },
    {
      id: 5,
      name: '焦虑抑郁',
      icon: getResource('images/op5.svg'),
      description: '情绪调节与心理健康',
      path: '/pages/counselor/index?category=焦虑抑郁'
    },
    {
      id: 6,
      name: '学习压力',
      icon: getResource('images/op6.svg'),
      description: '学业压力与考试焦虑',
      path: '/pages/counselor/index?category=学习压力'
    },
    {
      id: 7,
      name: '人际关系',
      icon: getResource('images/op7.svg'),
      description: '社交技巧与人际沟通',
      path: '/pages/counselor/index?category=人际关系'
    },
    {
      id: 8,
      name: '心理创伤',
      icon: getResource('images/op8.svg'),
      description: '创伤修复与心理重建',
      path: '/pages/counselor/index?category=心理创伤'
    }
  ],

  // 推荐咨询师数据
  counselors: [
    {
      id: 1,
      name: '郭万梅',
      avatar: getResource('images/counselor1.jpg'),
      title: '资深咨询师',
      specialty: '个人成长',
      experience: 10,
      consultType: '视频/语音',
      rating: 4.9,
      consultCount: 2156,
      price: 800,
      online: true,
      tags: ['认知行为疗法', '正念疗法', '情绪管理'],
      introduction: '擅长个人成长、情绪管理和认知重构，帮助来访者建立积极的人生观。',
      education: '北京师范大学心理学硕士',
      certification: ['国家二级心理咨询师', 'CBT认证咨询师']
    },
    {
      id: 2,
      name: '李静',
      avatar: getResource('images/counselor2.jpg'),
      title: '心理治疗师',
      specialty: '情感咨询',
      experience: 8,
      consultType: '视频/语音',
      rating: 4.8,
      consultCount: 1893,
      price: 600,
      online: false,
      tags: ['情感修复', '婚姻咨询', '关系重建'],
      introduction: '专注于情感问题解决，帮助来访者建立健康的亲密关系。',
      education: '华东师范大学应用心理学博士',
      certification: ['国家二级心理咨询师', 'EFT情绪取向治疗师']
    },
    {
      id: 3,
      name: '王晓华',
      avatar: getResource('images/counselor3.jpg'),
      title: '职业规划师',
      specialty: '职业规划',
      experience: 12,
      consultType: '视频/语音',
      rating: 4.9,
      consultCount: 3102,
      price: 1000,
      online: true,
      tags: ['职业发展', '生涯规划', '职场适应'],
      introduction: '资深职业规划专家，帮助来访者找到适合的职业发展道路。',
      education: '清华大学心理学硕士',
      certification: ['全球职业规划师', '国家一级心理咨询师']
    },
    {
      id: 4,
      name: '张明',
      avatar: getResource('images/counselor4.jpg'),
      title: '家庭治疗师',
      specialty: '家庭关系',
      experience: 15,
      consultType: '视频/语音',
      rating: 5.0,
      consultCount: 4230,
      price: 1200,
      online: true,
      tags: ['家庭治疗', '亲子关系', '系统式治疗'],
      introduction: '家庭系统治疗专家，致力于修复和改善家庭关系。',
      education: '中科院心理研究所博士',
      certification: ['国家一级心理咨询师', '系统式家庭治疗师']
    },
    {
      id: 5,
      name: '陈雨薇',
      avatar: getResource('images/counselor5.jpg'),
      title: '青少年心理专家',
      specialty: '学习压力',
      experience: 7,
      consultType: '视频/语音',
      rating: 4.7,
      consultCount: 1567,
      price: 500,
      online: true,
      tags: ['青少年心理', '学习焦虑', '考试压力'],
      introduction: '专注青少年心理健康，帮助学生缓解学习压力，提升学习效率。',
      education: '北京大学心理学硕士',
      certification: ['国家二级心理咨询师', '青少年心理健康指导师']
    },
    {
      id: 6,
      name: '刘建国',
      avatar: getResource('images/counselor6.jpg'),
      title: '创伤治疗师',
      specialty: '心理创伤',
      experience: 13,
      consultType: '视频/语音',
      rating: 4.8,
      consultCount: 2890,
      price: 900,
      online: false,
      tags: ['EMDR治疗', '创伤修复', 'PTSD治疗'],
      introduction: '创伤治疗专家，运用EMDR等专业技术帮助来访者走出心理阴霾。',
      education: '上海交通大学医学院精神医学博士',
      certification: ['国家一级心理咨询师', 'EMDR治疗师']
    }
  ],

  // 城市列表
  cities: ['全国', '北京', '上海', '广州', '深圳', '成都', '杭州', '武汉', '南京', '西安', '重庆', '天津'],

  // 时间选择选项
  timeOptions: [
    { label: '今天', value: 'today' },
    { label: '明天', value: 'tomorrow' },
    { label: '本周', value: 'thisWeek' },
    { label: '下周', value: 'nextWeek' },
    { label: '本月', value: 'thisMonth' }
  ],

  // 价格选择选项
  priceOptions: [
    { label: '不限', value: 'all' },
    { label: '500以下', value: 'under500' },
    { label: '500-800', value: '500to800' },
    { label: '800-1000', value: '800to1000' },
    { label: '1000以上', value: 'above1000' }
  ],

  // 排序选择选项
  sortOptions: [
    { label: '综合排序', value: 'comprehensive' },
    { label: '评分最高', value: 'highestRating' },
    { label: '咨询最多', value: 'mostConsultations' },
    { label: '价格从低到高', value: 'priceAsc' },
    { label: '价格从高到低', value: 'priceDesc' },
    { label: '经验最丰富', value: 'mostExperienced' }
  ],

  // 筛选选项
  filterOptions: [
    {
      title: '咨询类型',
      key: 'consultType',
      options: [
        { label: '个人成长', value: 'personal' },
        { label: '情感咨询', value: 'emotion' },
        { label: '婚姻家庭', value: 'marriage' },
        { label: '职业规划', value: 'career' },
        { label: '亲子教育', value: 'parenting' },
        { label: '焦虑抑郁', value: 'anxiety' },
        { label: '学习压力', value: 'study' },
        { label: '人际关系', value: 'interpersonal' },
        { label: '心理创伤', value: 'trauma' }
      ]
    },
    {
      title: '咨询方式',
      key: 'consultMethod',
      options: [
        { label: '视频咨询', value: 'video' },
        { label: '语音咨询', value: 'audio' },
        { label: '图文咨询', value: 'text' },
        { label: '面对面', value: 'offline' }
      ]
    },
    {
      title: '从业经验',
      key: 'experience',
      options: [
        { label: '3年以下', value: 'under3' },
        { label: '3-5年', value: '3to5' },
        { label: '5-10年', value: '5to10' },
        { label: '10年以上', value: 'above10' }
      ]
    },
    {
      title: '咨询师性别',
      key: 'gender',
      options: [
        { label: '男性咨询师', value: 'male' },
        { label: '女性咨询师', value: 'female' }
      ]
    }
  ],

  // 热门搜索关键词
  hotSearchKeywords: [
    '焦虑', '抑郁', '失眠', '情感问题', '职业规划', 
    '亲子关系', '婚姻咨询', '学习压力', '人际关系', '自我成长'
  ],

  // 公告通知
  announcements: [
    {
      id: 1,
      title: '春节期间咨询服务安排通知',
      content: '春节期间（2月10日-2月17日）咨询服务正常进行，部分咨询师时间有调整，请提前预约。',
      type: 'notice',
      publishTime: '2024-02-01 10:00:00'
    },
    {
      id: 2,
      title: '新用户专享优惠活动',
      content: '新注册用户首次咨询享受8折优惠，活动时间至2月29日。',
      type: 'promotion',
      publishTime: '2024-02-01 09:00:00'
    }
  ]
}

// 模拟API响应数据
const apiResponses = {
  // 获取首页数据
  getHomeData: () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          code: 200,
          message: 'success',
          data: homeData
        })
      }, 500) // 模拟网络延迟
    })
  },

  // 获取咨询师列表
  getCounselorList: (params = {}) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        let counselors = [...homeData.counselors]
        
        // 模拟筛选逻辑
        if (params.city && params.city !== '全国') {
          // 这里可以根据城市筛选，暂时返回所有数据
        }
        
        if (params.price) {
          switch (params.price) {
            case 'under500':
              counselors = counselors.filter(c => c.price < 500)
              break
            case '500to800':
              counselors = counselors.filter(c => c.price >= 500 && c.price <= 800)
              break
            case '800to1000':
              counselors = counselors.filter(c => c.price > 800 && c.price <= 1000)
              break
            case 'above1000':
              counselors = counselors.filter(c => c.price > 1000)
              break
          }
        }
        
        // 模拟排序逻辑
        if (params.sort) {
          switch (params.sort) {
            case 'highestRating':
              counselors.sort((a, b) => b.rating - a.rating)
              break
            case 'mostConsultations':
              counselors.sort((a, b) => b.consultCount - a.consultCount)
              break
            case 'priceAsc':
              counselors.sort((a, b) => a.price - b.price)
              break
            case 'priceDesc':
              counselors.sort((a, b) => b.price - a.price)
              break
            case 'mostExperienced':
              counselors.sort((a, b) => b.experience - a.experience)
              break
          }
        }
        
        resolve({
          code: 200,
          message: 'success',
          data: {
            list: counselors,
            total: counselors.length,
            page: params.page || 1,
            pageSize: params.pageSize || 10
          }
        })
      }, 300)
    })
  },

  // 搜索咨询师
  searchCounselors: (keyword) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const counselors = homeData.counselors.filter(c => 
          c.name.includes(keyword) || 
          c.specialty.includes(keyword) ||
          c.tags.some(tag => tag.includes(keyword))
        )
        
        resolve({
          code: 200,
          message: 'success',
          data: {
            list: counselors,
            total: counselors.length,
            keyword
          }
        })
      }, 200)
    })
  }
}

module.exports = {
  homeData,
  apiResponses
}