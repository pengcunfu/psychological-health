import { request } from '@/utils/request'

/**
 * 用户名登录
 * @param {Object} data 登录数据
 * @param {string} data.username 用户名
 * @param {string} data.password 密码
 * @param {string} data.verify_code 验证码（可选）
 * @returns {Promise}
 */
export function login(data) {
  return request({
    url: '/auth/login',
    method: 'POST',
    data
  })
}

/**
 * 手机号登录
 * @param {Object} data 登录数据
 * @param {string} data.phone 手机号
 * @param {string} data.password 密码
 * @param {string} data.verify_code 验证码（可选）
 * @returns {Promise}
 */
export function phoneLogin(data) {
  return request({
    url: '/auth/phone-login',
    method: 'POST',
    data
  })
}

/**
 * 用户注册
 * @param {Object} data 注册数据
 * @param {string} data.username 用户名
 * @param {string} data.password 密码
 * @param {string} data.phone 手机号（可选）
 * @param {string} data.email 邮箱（可选）
 * @param {string} data.avatar 头像（可选）
 * @returns {Promise}
 */
export function register(data) {
  return request({
    url: '/auth/register',
    method: 'POST',
    data
  })
}

/**
 * 用户登出
 * @returns {Promise}
 */
export function logout() {
  return request({
    url: '/auth/logout',
    method: 'POST'
  })
}

/**
 * 获取当前用户信息
 * @returns {Promise}
 */
export function getUserProfile() {
  return request({
    url: '/auth/profile',
    method: 'GET'
  })
}

/**
 * 更新用户信息
 * @param {Object} data 用户信息
 * @param {string} data.avatar 头像（可选）
 * @param {string} data.phone 手机号（可选）
 * @param {string} data.email 邮箱（可选）
 * @returns {Promise}
 */
export function updateProfile(data) {
  return request({
    url: '/auth/profile',
    method: 'PUT',
    data
  })
}

/**
 * 修改密码
 * @param {Object} data 密码数据
 * @param {string} data.old_password 旧密码
 * @param {string} data.new_password 新密码
 * @returns {Promise}
 */
export function changePassword(data) {
  return request({
    url: '/auth/change-password',
    method: 'PUT',
    data
  })
}

/**
 * 刷新访问令牌
 * @returns {Promise}
 */
export function refreshToken() {
  return request({
    url: '/auth/refresh-token',
    method: 'POST'
  })
}

/**
 * 获取验证码
 * @returns {Promise}
 */
export function getVerifyCode() {
  return request({
    url: '/auth/verify-code',
    method: 'GET',
    responseType: 'blob' // 图片数据
  })
}

/**
 * 发送短信验证码
 * @param {Object} data 
 * @param {string} data.phone 手机号
 * @param {string} data.type 验证码类型（register/login/reset）
 * @returns {Promise}
 */
export function sendSmsCode(data) {
  return request({
    url: '/auth/send-sms-code',
    method: 'POST',
    data
  })
}

/**
 * 验证短信验证码
 * @param {Object} data
 * @param {string} data.phone 手机号
 * @param {string} data.code 验证码
 * @param {string} data.type 验证码类型
 * @returns {Promise}
 */
export function verifySmsCode(data) {
  return request({
    url: '/auth/verify-sms-code',
    method: 'POST',
    data
  })
}

/**
 * 重置密码（通过手机验证码）
 * @param {Object} data
 * @param {string} data.phone 手机号
 * @param {string} data.code 短信验证码
 * @param {string} data.new_password 新密码
 * @returns {Promise}
 */
export function resetPasswordByPhone(data) {
  return request({
    url: '/auth/reset-password-by-phone',
    method: 'POST',
    data
  })
}

/**
 * 重置密码（通过邮箱）
 * @param {Object} data
 * @param {string} data.email 邮箱
 * @param {string} data.code 邮箱验证码
 * @param {string} data.new_password 新密码
 * @returns {Promise}
 */
export function resetPasswordByEmail(data) {
  return request({
    url: '/auth/reset-password-by-email',
    method: 'POST',
    data
  })
}
