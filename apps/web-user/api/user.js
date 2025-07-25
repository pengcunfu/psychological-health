import request from '../utils/request';

/**
 * 微信登录
 * @param {Object} data - 登录参数 {code}
 * @returns {Promise} - 登录结果
 */
export function wechatLogin(data) {
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
export function phoneLogin(data) {
  return request({
    url: '/phone_login',
    method: 'POST',
    data
  });
}

/**
 * 获取用户资料
 * @param {String} userId - 用户ID
 * @returns {Promise} - 用户资料
 */
export function getUserProfile(userId) {
  return request({
    url: `/user/${userId}`,
    method: 'GET'
  });
}

/**
 * 修改用户资料
 * @param {String} userId - 用户ID
 * @param {Object} data - 用户资料 {nickname, avatar, gender, age, bio}
 * @returns {Promise} - 修改结果
 */
export function updateUserProfile(userId, data) {
  return request({
    url: `/user/${userId}`,
    method: 'PUT',
    data
  });
}

/**
 * 获取用户统计数据
 * @param {String} userId - 用户ID
 * @returns {Promise} - 统计数据
 */
export function getUserStatistics(userId) {
  return request({
    url: `/user/statistics?userId=${userId}`,
    method: 'GET'
  });
}

/**
 * 发送验证码
 * @param {String} phone - 手机号
 * @returns {Promise} - 发送结果
 */
export function sendVerifyCode(phone) {
  return request({
    url: '/user/send-code',
    method: 'POST',
    data: { phone }
  });
}

export default {
  wechatLogin,
  phoneLogin,
  getUserProfile,
  updateUserProfile,
  getUserStatistics,
  sendVerifyCode
}; 