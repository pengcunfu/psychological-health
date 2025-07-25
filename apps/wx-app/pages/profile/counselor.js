Page({
  data: {
    counselorInfo: {
      name: '王晓华',
      title: '心理咨询师 / 高级婚姻家庭咨询师',
      avatar: 'https://randomuser.me/api/portraits/women/68.jpg',
      isVerified: true,
      specialties: ['抑郁症', '焦虑障碍', '婚姻家庭', '青少年心理'],
      sessionsCount: 286,
      clientCount: 78,
      rating: 4.8,
      bio: '从业8年，毕业于北京师范大学心理学专业，拥有国家二级心理咨询师资格证书和美国婚姻家庭治疗协会（AAMFT）认证资格。擅长抑郁症、焦虑障碍的认知行为治疗，以及婚姻关系、亲子关系的系统式家庭治疗。我相信每个人都有自愈的能力，作为咨询师，我的职责是陪伴并激发来访者内在的力量，共同面对困境，找到成长的方向。',
      qualifications: [
        {
          type: 'degree',
          title: '心理学硕士',
          organization: '北京师范大学',
          date: '2015年',
          verified: true
        },
        {
          type: 'certificate',
          title: '国家二级心理咨询师',
          organization: '中国心理卫生协会',
          date: '2016年',
          verified: true
        },
        {
          type: 'certificate',
          title: '婚姻家庭治疗师认证',
          organization: 'AAMFT',
          date: '2018年',
          verified: true
        },
        {
          type: 'certificate',
          title: 'CBT认知行为治疗培训',
          organization: '中国认知行为治疗联盟',
          date: '2017年',
          verified: false
        }
      ],
      pricing: [
        {
          serviceType: '个人咨询',
          duration: 50,
          price: 500
        },
        {
          serviceType: '婚姻咨询',
          duration: 80,
          price: 800
        },
        {
          serviceType: '家庭咨询',
          duration: 90,
          price: 1000
        },
        {
          serviceType: '短时干预',
          duration: 30,
          price: 300
        }
      ]
    }
  },

  onLoad() {
    this.loadCounselorProfile();
  },

  // 加载咨询师个人资料
  loadCounselorProfile() {
    // TODO: 从服务器获取咨询师资料
    console.log('加载咨询师资料');
  },

  // 更换头像
  changeAvatar() {
    wx.showActionSheet({
      itemList: ['拍照', '从相册选择'],
      success: (res) => {
        if (res.tapIndex === 0) {
          this.takePhoto();
        } else if (res.tapIndex === 1) {
          this.chooseFromAlbum();
        }
      }
    });
  },

  // 拍照
  takePhoto() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['camera'],
      camera: 'back',
      success: (res) => {
        this.uploadAvatar(res.tempFiles[0].tempFilePath);
      }
    });
  },

  // 从相册选择
  chooseFromAlbum() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album'],
      success: (res) => {
        this.uploadAvatar(res.tempFiles[0].tempFilePath);
      }
    });
  },

  // 上传头像
  uploadAvatar(tempFilePath) {
    wx.showLoading({
      title: '上传中...',
      mask: true
    });

    // TODO: 实现头像上传到服务器的逻辑
    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '上传成功',
        icon: 'success'
      });
    }, 2000);
  },

  // 编辑各个部分
  editSection(e) {
    const section = e.currentTarget.dataset.section;
    const routes = {
      bio: '/pages/counselor/edit/bio',
      qualifications: '/pages/counselor/edit/qualifications',
      pricing: '/pages/counselor/edit/pricing'
    };

    wx.navigateTo({
      url: routes[section]
    });
  },

  // 获取资质图标类名
  getQualificationIcon(type) {
    const iconMap = {
      'degree': 'icon-degree',
      'certificate': 'icon-certificate',
      'license': 'icon-license',
      'training': 'icon-training'
    };
    return iconMap[type] || 'icon-certificate';
  },

  // 页面导航
  navigateTo(e) {
    const url = e.currentTarget.dataset.url;
    wx.navigateTo({ url });
  },

  // 预览公开主页
  previewPublicProfile() {
    wx.navigateTo({
      url: '/pages/counselor/detail/detail?id=self&preview=true'
    });
  },

  // 退出登录
  logout() {
    wx.showModal({
      title: '确认退出',
      content: '您确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          // 清除本地存储
          wx.clearStorageSync();
          // 跳转到登录页
          wx.reLaunch({
            url: '/pages/login/login'
          });
        }
      }
    });
  }
}); 