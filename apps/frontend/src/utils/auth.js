const TOKEN_KEY = 'psychological_health_token'

/**
 * 获取token
 */
export const getToken = () => {
  return uni.getStorageSync(TOKEN_KEY)
}

/**
 * 设置token
 * @param {string} token
 */
export const setToken = (token) => {
  uni.setStorageSync(TOKEN_KEY, token)
}

/**
 * 移除token
 */
export const removeToken = () => {
  uni.removeStorageSync(TOKEN_KEY)
}

/**
 * 检查是否已登录
 */
export const isLoggedIn = () => {
  return !!getToken()
}

/**
 * 跳转到登录页
 * @param {string} redirect 登录后跳转的页面路径
 */
export const redirectToLogin = (redirect) => {
  const currentPage = getCurrentPages().pop()
  const currentPath = currentPage ? currentPage.route : ''
  
  // 如果当前不是登录页，则跳转到登录页
  if (currentPath !== 'pages/login/index') {
    uni.navigateTo({
      url: `/pages/login/index${redirect ? '?redirect=' + encodeURIComponent(redirect) : ''}`
    })
  }
}

/**
 * 检查登录状态，未登录则跳转到登录页
 * @param {boolean} showToast 是否显示提示
 * @returns {boolean} 是否已登录
 */
export const checkLogin = (showToast = true) => {
  const logged = isLoggedIn()
  
  if (!logged && showToast) {
    uni.showToast({
      title: '请先登录',
      icon: 'none'
    })
    
    setTimeout(() => {
      redirectToLogin()
    }, 1500)
  }
  
  return logged
} 