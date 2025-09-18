import config from './config.js'

/**
 * 图片处理工具
 */
export const imageUtils = {
  /**
   * 处理图片URL，如果是相对路径则添加服务器地址前缀
   * @param {string} imageUrl - 图片URL
   * @param {string} defaultImage - 默认图片路径（可选）
   * @returns {string} 完整的图片URL
   */
  processImageUrl(imageUrl, defaultImage = '') {
    if (!imageUrl) {
      return defaultImage || config.defaultAvatar
    }
    
    // 如果已经是完整的URL（包含http或https），直接返回
    if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
      return imageUrl
    }
    
    // 如果是相对路径，添加静态资源URL前缀
    if (imageUrl.startsWith('/')) {
      return `${config.staticUrl}${imageUrl}`
    }
    
    // 如果不是以/开头，添加/和静态资源URL前缀
    return `${config.staticUrl}/${imageUrl}`
  },

  /**
   * 处理轮播图数据，转换图片URL
   * @param {Array} banners - 轮播图数组
   * @returns {Array} 处理后的轮播图数组
   */
  processBanners(banners) {
    if (!Array.isArray(banners)) {
      return []
    }
    
    return banners.map(banner => ({
      ...banner,
      image_url: this.processImageUrl(banner.image_url)
    }))
  },

  /**
   * 处理咨询师数据，转换头像URL
   * @param {Array} counselors - 咨询师数组
   * @returns {Array} 处理后的咨询师数组
   */
  processCounselors(counselors) {
    if (!Array.isArray(counselors)) {
      return []
    }
    
    return counselors.map(counselor => ({
      ...counselor,
      avatar: this.processImageUrl(counselor.avatar, config.defaultAvatar)
    }))
  },

  /**
   * 处理课程数据，转换封面图URL
   * @param {Array} courses - 课程数组
   * @returns {Array} 处理后的课程数组
   */
  processCourses(courses) {
    if (!Array.isArray(courses)) {
      return []
    }
    
    return courses.map(course => ({
      ...course,
      cover: this.processImageUrl(course.cover, config.defaultCourseCover)
    }))
  },

  /**
   * 获取默认头像URL
   * @returns {string} 默认头像的完整URL
   */
  getDefaultAvatar() {
    return this.processImageUrl(config.defaultAvatar)
  },

  /**
   * 获取默认课程封面URL
   * @returns {string} 默认课程封面的完整URL
   */
  getDefaultCourseCover() {
    return this.processImageUrl(config.defaultCourseCover)
  },

  /**
   * 获取默认测评封面URL
   * @returns {string} 默认测评封面的完整URL
   */
  getDefaultAssessmentCover() {
    return this.processImageUrl(config.defaultAssessmentCover)
  }
} 