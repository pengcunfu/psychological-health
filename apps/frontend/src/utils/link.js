/**
 * 链接跳转工具函数
 * 处理内部页面跳转和外部链接打开
 */

/**
 * URL预处理函数
 * @param {string} url - 原始URL
 * @returns {string} - 处理后的URL
 */
export const preprocessUrl = (url) => {
  if (!url) return ''
  
  // 去除首尾空格
  url = url.trim()
  
  // 如果是相对路径，确保以 / 开头
  if (!url.startsWith('http') && !url.startsWith('/')) {
    url = '/' + url
  }
  
  return url
}

/**
 * 判断是否是外部链接
 * @param {string} url - URL地址
 * @returns {boolean} - 是否为外部链接
 */
export const isExternalUrl = (url) => {
  return url.startsWith('http://') || url.startsWith('https://')
}

/**
 * 验证内部路径是否有效
 * @param {string} url - 内部路径
 * @returns {boolean} - 路径是否有效
 */
export const isValidInternalPath = (url) => {
  // 基本的路径格式验证
  if (!url || typeof url !== 'string') return false
  
  // 移除查询参数进行路径验证
  const pathOnly = url.split('?')[0]
  
  // 定义有效的页面路径列表（基于pages.json）
  const validPaths = [
    '/pages/index',
    '/pages/login',
    '/pages/register',
    '/pages/forgot-password',
    '/pages/counselor/index',
    '/pages/counselor/detail',
    '/pages/course/index',
    '/pages/course/detail',
    '/pages/assessment/index',
    '/pages/assessment/detail',
    '/pages/social/index',
    '/pages/profile/index',
    '/pages/profile/edit',
    '/pages/profile/security',
    '/pages/profile/become-counselor',
    '/pages/profile/contact-us',
    '/pages/profile/agreement',
    '/pages/profile/privacy',
    '/pages/profile/my-course',
    '/pages/profile/my-favorite',
    '/pages/order',
    '/pages/profile/my-appointment',
    '/pages/search',
    '/pages/webview',
    '/pages/message'
  ]
  
  return validPaths.includes(pathOnly)
}

/**
 * 判断是否是tabbar页面
 * @param {string} url - 页面路径
 * @returns {boolean} - 是否为tabbar页面
 */
export const isTabBarPage = (url) => {
  const pathOnly = url.split('?')[0]
  const tabBarPaths = [
    '/pages/index',
    '/pages/counselor/index',
    '/pages/course/index',
    '/pages/profile/index'
  ]
  
  return tabBarPaths.includes(pathOnly)
}

/**
 * 处理外部链接
 * @param {string} url - 外部链接地址
 * @param {string} title - 链接标题
 */
export const handleExternalUrl = (url, title = '') => {
  
  // #ifdef H5
  // 浏览器环境下，可以直接打开新窗口
  if (typeof window !== 'undefined') {
    window.open(url, '_blank')
    return
  }
  // #endif
  
  // #ifdef MP-WEIXIN
  // 微信小程序环境下，使用webview页面
  uni.navigateTo({
    url: `/pages/webview?url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`,
    fail: (err) => {
      console.error('外部链接跳转失败:', err)
      // 微信小程序可能不支持某些外部链接，提示用户复制链接
      uni.showModal({
        title: '提示',
        content: '无法直接打开链接，是否复制到剪贴板？',
        success: (res) => {
          if (res.confirm) {
            uni.setClipboardData({
              data: url,
              success: () => {
                uni.showToast({
                  title: '链接已复制',
                  icon: 'success'
                })
              }
            })
          }
        }
      })
    }
  })
  // #endif
  
  // #ifndef H5 || MP-WEIXIN
  // 其他平台使用webview页面
  uni.navigateTo({
    url: `/pages/webview?url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`,
    fail: (err) => {
      console.error('外部链接跳转失败:', err)
      uni.showToast({
        title: '链接打开失败',
        icon: 'none'
      })
    }
  })
  // #endif
}

/**
 * 处理内部链接
 * @param {string} url - 内部页面路径
 */
export const handleInternalUrl = (url) => {
  
  // 验证内部路径是否有效
  if (!isValidInternalPath(url)) {
    console.error('无效的内部路径:', url)
    uni.showToast({
      title: '页面不存在',
      icon: 'none'
    })
    return
  }
  
  // 判断是否是tabbar页面
  if (isTabBarPage(url)) {
    uni.switchTab({
      url: url,
      success: () => {
      },
      fail: (err) => {
        console.error('TabBar页面跳转失败:', err, url)
        uni.showToast({
          title: '页面跳转失败',
          icon: 'none'
        })
      }
    })
  } else {
    uni.navigateTo({
      url: url,
      success: () => {
      },
      fail: (err) => {
        console.error('内部页面跳转失败:', err, url)
        // 如果navigateTo失败，尝试使用redirectTo
        uni.redirectTo({
          url: url,
          fail: (redirectErr) => {
            console.error('页面重定向也失败:', redirectErr, url)
            uni.showToast({
              title: '页面跳转失败',
              icon: 'none'
            })
          }
        })
      }
    })
  }
}

/**
 * 统一的URL导航处理函数
 * @param {string} url - URL地址
 * @param {string} title - 链接标题（可选）
 */
export const handleUrlNavigation = (url, title = '') => {
  // 判断是否是外部链接
  if (isExternalUrl(url)) {
    handleExternalUrl(url, title)
  } else {
    handleInternalUrl(url)
  }
}



/**
 * 智能的页面跳转函数
 * @param {string} url - 页面路径
 */
export const navigateTo = (url) => {
  // 使用智能导航，自动判断是否为tabbar页面
  handleInternalUrl(url)
}
