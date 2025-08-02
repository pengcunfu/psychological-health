import { getToken } from './auth'
import config from './config'

// 请求基础URL
const baseURL = config.apiBaseUrl

/**
 * 请求拦截器
 * @param {Object} options - 请求配置
 */
const requestInterceptor = (options) => {
  // 添加token到请求头
  const token = getToken()
  if (token) {
    options.header = {
      ...options.header,
      'Authorization': `Bearer ${token}`
    }
  }
  
  // 添加内容类型
  if (options.method === 'POST' || options.method === 'PUT') {
    options.header = {
      ...options.header,
      'Content-Type': 'application/json'
    }
  }
  
  // 拼接完整URL
  if (!options.url.startsWith('http')) {
    options.url = baseURL + options.url
  }
  
  return options
}

/**
 * 响应拦截器
 * @param {Object} response - 响应数据
 * @param {Object} options - 请求配置
 */
const responseInterceptor = (response, options) => {
  const { statusCode, data } = response
  
  // 请求成功
  if (statusCode >= 200 && statusCode < 300) {
    return data
  }
  
  // 处理401未授权错误
  if (statusCode === 401) {
    // 可以在这里处理登录过期的逻辑，例如清除token并跳转到登录页
    uni.showToast({
      title: '登录已过期，请重新登录',
      icon: 'none'
    })
    
    // 延迟跳转到登录页
    setTimeout(() => {
      uni.navigateTo({
        url: '/pages/login/index'
      })
    }, 1500)
  }
  
  // 其他错误
  return Promise.reject({
    statusCode,
    message: data.message || '请求失败',
    data
  })
}

/**
 * 统一请求函数
 * @param {Object} options - 请求配置
 * @returns {Promise} - 返回Promise对象
 */
export const request = (options) => {
  // 应用请求拦截器
  options = requestInterceptor(options)
  
  return new Promise((resolve, reject) => {
    uni.request({
      ...options,
      success: (res) => {
        try {
          // 应用响应拦截器
          const result = responseInterceptor(res, options)
          resolve(result)
        } catch (error) {
          reject(error)
        }
      },
      fail: (err) => {
        uni.showToast({
          title: '网络请求失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

/**
 * GET请求
 * @param {string} url - 请求URL
 * @param {Object} params - 请求参数
 * @param {Object} options - 其他配置
 */
export const get = (url, params = {}, options = {}) => {
  return request({
    url,
    method: 'GET',
    data: params,
    ...options
  })
}

/**
 * POST请求
 * @param {string} url - 请求URL
 * @param {Object} data - 请求数据
 * @param {Object} options - 其他配置
 */
export const post = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'POST',
    data,
    ...options
  })
}

/**
 * PUT请求
 * @param {string} url - 请求URL
 * @param {Object} data - 请求数据
 * @param {Object} options - 其他配置
 */
export const put = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'PUT',
    data,
    ...options
  })
}

/**
 * DELETE请求
 * @param {string} url - 请求URL
 * @param {Object} data - 请求数据
 * @param {Object} options - 其他配置
 */
export const del = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'DELETE',
    data,
    ...options
  })
}

export default {
  request,
  get,
  post,
  put,
  del
} 