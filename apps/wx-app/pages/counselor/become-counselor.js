Page({
  data: {
    // 性别选择
    gender: '',

    // 学历选择
    educationLevels: ['专科', '本科', '硕士', '博士'],
    educationIndex: -1,

    // 从业年限
    experienceYears: ['1年以下', '1-3年', '3-5年', '5-10年', '10年以上'],
    experienceIndex: -1,

    // 擅长领域
    specialties: [
      { label: '抑郁症', value: 'depression', selected: false },
      { label: '焦虑症', value: 'anxiety', selected: false },
      { label: '睡眠障碍', value: 'sleep', selected: false },
      { label: '强迫症', value: 'ocd', selected: false },
      { label: '恐慌症', value: 'panic', selected: false },
      { label: '情绪管理', value: 'emotion', selected: false },
      { label: '人际关系', value: 'relationship', selected: false },
      { label: '婚姻家庭', value: 'marriage', selected: false },
      { label: '青少年心理', value: 'youth', selected: false },
      { label: '职场压力', value: 'work', selected: false },
      { label: '个人成长', value: 'growth', selected: false },
      { label: '生涯规划', value: 'career', selected: false }
    ],

    // 图片上传
    certificateImage: '',
    idCardImage: '',

    // 个人简介字数
    introLength: 0
  },

  // 选择性别
  onGenderSelect(e) {
    const gender = e.currentTarget.dataset.gender;
    this.setData({ gender });
  },

  // 选择学历
  onEducationChange(e) {
    this.setData({
      educationIndex: e.detail.value
    });
  },

  // 选择从业年限
  onExperienceChange(e) {
    this.setData({
      experienceIndex: e.detail.value
    });
  },

  // 选择擅长领域
  onSpecialtySelect(e) {
    const index = e.currentTarget.dataset.index;
    const specialties = this.data.specialties;
    specialties[index].selected = !specialties[index].selected;
    this.setData({ specialties });
  },

  // 上传资格证照片
  onUploadCertificate() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFilePath = res.tempFiles[0].tempFilePath;
        this.setData({
          certificateImage: tempFilePath
        });
      }
    });
  },

  // 删除资格证照片
  onDeleteCertificate() {
    this.setData({
      certificateImage: ''
    });
  },

  // 上传身份证照片
  onUploadIdCard() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFilePath = res.tempFiles[0].tempFilePath;
        this.setData({
          idCardImage: tempFilePath
        });
      }
    });
  },

  // 删除身份证照片
  onDeleteIdCard() {
    this.setData({
      idCardImage: ''
    });
  },

  // 监听简介输入
  onIntroInput(e) {
    const value = e.detail.value;
    this.setData({
      introLength: value.length
    });
  },

  // 表单提交
  onSubmit(e) {
    const formData = e.detail.value;
    
    // 获取选中的擅长领域
    const selectedSpecialties = this.data.specialties
      .filter(item => item.selected)
      .map(item => item.value);

    // 表单验证
    if (!formData.realName) {
      this.showToast('请输入真实姓名');
      return;
    }
    if (!this.data.gender) {
      this.showToast('请选择性别');
      return;
    }
    if (!formData.phone) {
      this.showToast('请输入联系电话');
      return;
    }
    if (!formData.email) {
      this.showToast('请输入邮箱');
      return;
    }
    if (this.data.educationIndex === -1) {
      this.showToast('请选择最高学历');
      return;
    }
    if (!formData.school) {
      this.showToast('请输入毕业院校');
      return;
    }
    if (!formData.major) {
      this.showToast('请输入专业方向');
      return;
    }
    if (this.data.experienceIndex === -1) {
      this.showToast('请选择从业年限');
      return;
    }
    if (selectedSpecialties.length === 0) {
      this.showToast('请选择擅长领域');
      return;
    }
    if (!this.data.certificateImage) {
      this.showToast('请上传职业资格证书');
      return;
    }
    if (!this.data.idCardImage) {
      this.showToast('请上传身份证照片');
      return;
    }
    if (!formData.introduction) {
      this.showToast('请填写个人简介');
      return;
    }

    // 构建提交数据
    const submitData = {
      ...formData,
      gender: this.data.gender,
      education: this.data.educationLevels[this.data.educationIndex],
      experience: this.data.experienceYears[this.data.experienceIndex],
      specialties: selectedSpecialties,
      certificateImage: this.data.certificateImage,
      idCardImage: this.data.idCardImage
    };

    console.log('提交数据：', submitData);

    // TODO: 调用后端API提交数据
    wx.showLoading({
      title: '提交中...',
      mask: true
    });

    // 模拟提交
    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '提交成功',
        icon: 'success',
        duration: 2000,
        success: () => {
          // 延迟返回上一页
          setTimeout(() => {
            wx.navigateBack();
          }, 2000);
        }
      });
    }, 1500);
  },

  // 显示提示
  showToast(title) {
    wx.showToast({
      title,
      icon: 'none',
      duration: 2000
    });
  }
}); 