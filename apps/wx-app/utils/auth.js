/**
 * 认证工具类
 * 用于管理 Token 和用户信息的存储、获取和清除
 */

// Token 相关的 key 常量
const TOKEN_KEY = 'mental_health_token'
const REFRESH_TOKEN_KEY = 'mental_health_refresh_token'

// 用户信息的 key 常量
const USER_INFO_KEY = 'mental_health_user_info'

/**
 * Token 相关操作
 */
export function getToken() {
  return uni.getStorageSync(TOKEN_KEY)
}

export function setToken(token) {
  return uni.setStorageSync(TOKEN_KEY, token)
}

export function removeToken() {
  return uni.removeStorageSync(TOKEN_KEY)
}

/**
 * 刷新 Token 相关操作
 */
export function getRefreshToken() {
  return uni.getStorageSync(REFRESH_TOKEN_KEY)
}

export function setRefreshToken(token) {
  return uni.setStorageSync(REFRESH_TOKEN_KEY, token)
}

export function removeRefreshToken() {
  return uni.removeStorageSync(REFRESH_TOKEN_KEY)
}

/**
 * 用户信息相关操作
 */
export function getUserInfo() {
  const userInfo = uni.getStorageSync(USER_INFO_KEY)
  return userInfo ? JSON.parse(userInfo) : null
}

export function setUserInfo(userInfo) {
  return uni.setStorageSync(USER_INFO_KEY, JSON.stringify(userInfo))
}

export function removeUserInfo() {
  return uni.removeStorageSync(USER_INFO_KEY)
}

/**
 * 判断是否已登录
 */
export function isLoggedIn() {
  return !!getToken()
}

/**
 * 获取用户特定信息的快捷方法
 */
export function getUserId() {
  const userInfo = getUserInfo()
  return userInfo ? userInfo.userId : null
}

export function getUserName() {
  const userInfo = getUserInfo()
  return userInfo ? userInfo.userName : null
}

export function getUserAvatar() {
  const userInfo = getUserInfo()
  return userInfo ? userInfo.avatar : null
}

export function getUserRole() {
  const userInfo = getUserInfo()
  return userInfo ? userInfo.role : null
}

/**
 * 清除所有认证信息
 */
export function clearAuth() {
  removeToken()
  removeRefreshToken()
  removeUserInfo()
}

/**
 * 保存完整的认证信息
 * @param {Object} authData - 认证数据对象
 * @param {string} authData.token - 访问令牌
 * @param {string} authData.refreshToken - 刷新令牌
 * @param {Object} authData.userInfo - 用户信息
 */
export function setAuth(authData) {
  const { token, refreshToken, userInfo } = authData
  
  // 保存令牌
  if (token) {
    setToken(token)
  }
  
  // 保存刷新令牌
  if (refreshToken) {
    setRefreshToken(refreshToken)
  }
  
  // 保存用户信息
  if (userInfo) {
    setUserInfo(userInfo)
  }
}

/**
 * 获取完整的认证信息
 * @returns {Object} 认证信息对象
 */
export function getAuth() {
  return {
    token: getToken(),
    refreshToken: getRefreshToken(),
    userInfo: getUserInfo()
  }
}

/**
 * 检查 Token 是否需要刷新
 * 可以根据项目需求自定义检查逻辑
 * @returns {boolean}
 */
export function isTokenNeedRefresh() {
  const token = getToken()
  if (!token) return false
  
  try {
    // 这里可以添加 Token 过期检查逻辑
    // 例如：检查 JWT 的过期时间
    // const decoded = jwt_decode(token)
    // return decoded.exp * 1000 - Date.now() < 1800000 // 小于30分钟需要刷新
    
    return false
  } catch (error) {
    return false
  }
}

/**
 * 更新用户信息中的特定字段
 * @param {Object} updateData - 要更新的字段
 */
export function updateUserInfo(updateData) {
  const userInfo = getUserInfo() || {}
  setUserInfo({ ...userInfo, ...updateData })
}

/**
 * 检查用户是否有特定权限
 * @param {string|string[]} permissions - 权限标识或权限标识数组
 * @returns {boolean}
 */
export function hasPermission(permissions) {
  const userInfo = getUserInfo()
  if (!userInfo || !userInfo.permissions) return false
  
  if (Array.isArray(permissions)) {
    return permissions.some(permission => userInfo.permissions.includes(permission))
  }
  
  return userInfo.permissions.includes(permissions)
}

/**
 * 检查用户是否是咨询师
 * @returns {boolean}
 */
export function isCounselor() {
  const userInfo = getUserInfo()
  return userInfo ? userInfo.role === 'counselor' : false
}

/**
 * 检查用户是否是普通用户
 * @returns {boolean}
 */
export function isNormalUser() {
  const userInfo = getUserInfo()
  return userInfo ? userInfo.role === 'user' : false
} 