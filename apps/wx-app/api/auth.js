/**
 * 认证API类
 */
class AuthApi {
  /**
   * 微信登录
   * @param {Object} data - 登录参数 {code}
   * @returns {Promise} - 登录结果
   */
  static wechatLogin(data) {
    return request({
      url: '/wechat_login',
      method: 'POST',
      data
    });
  }

  /**
   * 手机号登录
   * @param {Object} data - 登录参数 {phone, code}
   * @returns {Promise} - 登录结果
   */
  static phoneLogin(data) {
    return request({
      url: '/phone_login',
      method: 'POST',
      data
    });
  }

  /**
   * 发送验证码
   * @param {String} phone - 手机号
   * @returns {Promise} - 发送结果
   */
  static sendVerifyCode(phone) {
    return request({
      url: '/user/send-code',
      method: 'POST',
      data: {
        phone
      }
    });
  }
}

// 导出类
export default {
  AuthApi
};