import { request } from './request'
import { imageUtils } from './image'

/**
 * API工具类
 * 提供统一的API调用方法和数据处理
 */
export const apiUtils = {
  /**
   * 处理API响应数据
   * @param {Promise} apiCall - API调用Promise
   * @param {string} dataType - 数据类型 ('banners', 'counselors', 'courses')
   * @returns {Promise} 处理后的数据
   */
  async processApiResponse(apiCall, dataType = '') {
    try {
      const res = await apiCall
      
      if (res.code === 200 && res.success) {
        const data = res.data.list || res.data || []
        
        // 根据数据类型处理图片URL
        switch (dataType) {
          case 'banners':
            return imageUtils.processBanners(data)
          case 'counselors':
            return imageUtils.processCounselors(data)
          case 'courses':
            return imageUtils.processCourses(data)
          default:
            return data
        }
      }
      
      return []
    } catch (error) {
      console.warn('API调用失败:', error)
      return []
    }
  },

  /**
   * 获取分页数据
   * @param {Function} apiCall - API调用函数
   * @param {Object} params - 请求参数
   * @param {string} dataType - 数据类型
   * @returns {Promise<Object>} 包含数据和分页信息的对象
   */
  async getPaginatedData(apiCall, params = {}, dataType = '') {
    try {
      const res = await apiCall(params)
      
      if (res.code === 200 && res.success) {
        let processedData = res.data.list || []
        
        // 根据数据类型处理图片URL
        switch (dataType) {
          case 'banners':
            processedData = imageUtils.processBanners(processedData)
            break
          case 'counselors':
            processedData = imageUtils.processCounselors(processedData)
            break
          case 'courses':
            processedData = imageUtils.processCourses(processedData)
            break
        }
        
        return {
          list: processedData,
          total: res.data.total || 0,
          page: res.data.page || 1,
          per_page: res.data.per_page || 10,
          pages: res.data.pages || 1
        }
      }
      
      return {
        list: [],
        total: 0,
        page: 1,
        per_page: 10,
        pages: 1
      }
    } catch (error) {
      console.warn('API调用失败:', error)
      return {
        list: [],
        total: 0,
        page: 1,
        per_page: 10,
        pages: 1
      }
    }
  },

  /**
   * 统一的错误处理
   * @param {Error} error - 错误对象
   * @param {string} defaultMessage - 默认错误消息
   */
  handleError(error, defaultMessage = '操作失败') {
    const message = error?.message || error?.data?.message || defaultMessage
    
    uni.showToast({
      title: message,
      icon: 'none',
      duration: 2000
    })
    
    console.error('API错误:', error)
  },

  /**
   * 显示成功消息
   * @param {string} message - 成功消息
   */
  showSuccess(message) {
    uni.showToast({
      title: message,
      icon: 'success',
      duration: 2000
    })
  }
} 