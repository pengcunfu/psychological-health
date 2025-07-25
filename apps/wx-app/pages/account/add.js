Page({
  data: {
    showPrivacyTip: true,
    canSave: false,
    relationships: ['父母', '配偶', '子女', '兄弟姐妹', '朋友', '其他'],
    formData: {
      name: '',
      birthday: '',
      gender: null,
      phone: '',
      emergencyName: '',
      relationship: null,
      emergencyPhone: '',
      agreed: false
    }
  },

  onLoad(options) {
    // 如果有传入的预约ID，保存下来
    if (options.appointmentId) {
      this.setData({
        appointmentId: options.appointmentId
      });
    }
  },

  // 关闭隐私提示
  closeTip() {
    this.setData({
      showPrivacyTip: false
    });
  },

  // 输入姓名
  onInputName(e) {
    this.setData({
      'formData.name': e.detail.value
    });
    this.checkFormValid();
  },

  // 选择出生年月
  onPickerChange(e) {
    this.setData({
      'formData.birthday': e.detail.value
    });
    this.checkFormValid();
  },

  // 选择性别
  onSelectGender(e) {
    const gender = parseInt(e.currentTarget.dataset.gender);
    this.setData({
      'formData.gender': gender
    });
    this.checkFormValid();
  },

  // 输入手机号
  onInputPhone(e) {
    this.setData({
      'formData.phone': e.detail.value
    });
    this.checkFormValid();
  },

  // 输入紧急联系人姓名
  onInputEmergencyName(e) {
    this.setData({
      'formData.emergencyName': e.detail.value
    });
    this.checkFormValid();
  },

  // 选择关系
  onRelationshipChange(e) {
    this.setData({
      'formData.relationship': parseInt(e.detail.value)
    });
    this.checkFormValid();
  },

  // 输入紧急联系人电话
  onInputEmergencyPhone(e) {
    this.setData({
      'formData.emergencyPhone': e.detail.value
    });
    this.checkFormValid();
  },

  // 切换协议同意状态
  toggleAgreement() {
    this.setData({
      'formData.agreed': !this.data.formData.agreed
    });
    this.checkFormValid();
  },

  // 检查表单是否有效
  checkFormValid() {
    const {
      formData
    } = this.data;
    const isValid =
      formData.name &&
      formData.birthday &&
      formData.gender &&
      formData.phone &&
      formData.emergencyName &&
      formData.relationship !== null &&
      formData.emergencyPhone &&
      formData.agreed;

    this.setData({
      canSave: isValid
    });
  },

  // 保存账户信息
  onSave() {
    if (!this.data.canSave) {
      return;
    }

    const {
      formData
    } = this.data;

    // 表单验证
    if (!this.validateForm(formData)) {
      return;
    }

    wx.showLoading({
      title: '保存中...'
    });

    // TODO: 调用保存账户接口
    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '保存成功',
        icon: 'success',
        duration: 2000,
        success: () => {
          // 如果是从预约页面来的，返回预约页面
          if (this.data.appointmentId) {
            const pages = getCurrentPages();
            const prevPage = pages[pages.length - 2];

            // 更新上一页的数据
            if (prevPage) {
              prevPage.setData({
                'accountInfo': {
                  id: new Date().getTime(), // 模拟ID
                  name: formData.name,
                  phone: formData.phone
                }
              });
            }
          }

          setTimeout(() => {
            wx.navigateBack();
          }, 1500);
        }
      });
    }, 1500);
  },

  // 表单验证
  validateForm(formData) {
    // 验证手机号格式
    const phoneReg = /^1[3-9]\d{9}$/;
    if (!phoneReg.test(formData.phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      });
      return false;
    }

    if (!phoneReg.test(formData.emergencyPhone)) {
      wx.showToast({
        title: '请输入正确的紧急联系人手机号',
        icon: 'none'
      });
      return false;
    }

    // 验证姓名
    if (formData.name.length < 2) {
      wx.showToast({
        title: '请输入正确的姓名',
        icon: 'none'
      });
      return false;
    }

    if (formData.emergencyName.length < 2) {
      wx.showToast({
        title: '请输入正确的紧急联系人姓名',
        icon: 'none'
      });
      return false;
    }

    return true;
  }
});