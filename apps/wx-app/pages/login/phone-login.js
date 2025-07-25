Page({
  data: {
    phone: '',
    code: '',
    codeText: '获取验证码',
    codeDisabled: false,
    timer: null,
    seconds: 60
  },
  onPhoneInput(e) {
    this.setData({ phone: e.detail.value });
  },
  onCodeInput(e) {
    this.setData({ code: e.detail.value });
  },
  getCode() {
    if (this.data.codeDisabled) return;
    if (!/^1\d{10}$/.test(this.data.phone)) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' });
      return;
    }
    // 模拟发送验证码
    wx.showToast({ title: '验证码已发送', icon: 'success' });
    this.setData({ codeDisabled: true, codeText: `${this.data.seconds}s` });
    this.startTimer();
  },
  startTimer() {
    let seconds = this.data.seconds;
    this.data.timer = setInterval(() => {
      seconds--;
      this.setData({ codeText: `${seconds}s` });
      if (seconds <= 0) {
        clearInterval(this.data.timer);
        this.setData({ codeText: '获取验证码', codeDisabled: false });
      }
    }, 1000);
  },
  phoneLogin() {
    if (!/^1\d{10}$/.test(this.data.phone)) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' });
      return;
    }
    if (!/^\d{6}$/.test(this.data.code)) {
      wx.showToast({ title: '请输入6位验证码', icon: 'none' });
      return;
    }
    // 模拟登录
    wx.showToast({ title: '登录成功', icon: 'success' });
    // 登录成功后可跳转
    // wx.redirectTo({ url: '/pages/index/index' });
  },
  openUserAgreement() {
    wx.navigateTo({ url: '/pages/login/agreement' });
  },
  openPrivacyPolicy() {
    wx.navigateTo({ url: '/pages/login/privacy' });
  },
  onUnload() {
    if (this.data.timer) clearInterval(this.data.timer);
  }
}); 