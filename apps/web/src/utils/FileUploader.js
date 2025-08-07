/**
 * 文件上传工具类
 */
export class FileUploader {
  // 验证文件类型
  static validateFileType(file, allowedTypes) {
    return allowedTypes.includes(file.type)
  }

  // 验证文件大小
  static validateFileSize(file, maxSizeMB) {
    const maxSizeBytes = maxSizeMB * 1024 * 1024
    return file.size <= maxSizeBytes
  }

  // 获取完整的图片URL
  static getFullImageUrl(imageUrl) {
    if (!imageUrl) return ''
    // 如果是http或https开头的完整URL，直接返回
    if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
      return imageUrl
    }
    // 否则添加当前域名前缀
    return `${window.location.origin}/api/${imageUrl}`
  }

  static getFullVideoUrl(videoUrl) {
    if (!videoUrl) return ''
    // 如果是http或https开头的完整URL，直接返回
    if (videoUrl.startsWith('http://') || videoUrl.startsWith('https://')) {
      return videoUrl
    }
    // 如果以/开头，说明是绝对路径，直接拼接域名
    if (videoUrl.startsWith('/')) {
      return `${window.location.origin}/api${videoUrl}`
    }
    // 否则添加当前域名前缀和api路径
    return `${window.location.origin}/api/${videoUrl}`
  }

  // 验证图片文件
  static validateImage(file, maxSizeMB = 10) {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
    
    if (!file.type.startsWith('image/')) {
      throw new Error('只能上传图片文件!')
    }
    
    if (!this.validateFileType(file, allowedTypes)) {
      throw new Error('只支持 JPG、PNG、GIF、WebP 格式的图片!')
    }
    
    if (!this.validateFileSize(file, maxSizeMB)) {
      throw new Error(`图片大小不能超过 ${maxSizeMB}MB!`)
    }
    
    return true
  }

  // 验证文档文件
  static validateDocument(file, maxSizeMB = 10) {
    const allowedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ]
    
    if (!this.validateFileType(file, allowedTypes)) {
      throw new Error('只支持 PDF、Word、Excel 格式的文档!')
    }
    
    if (!this.validateFileSize(file, maxSizeMB)) {
      throw new Error(`文档大小不能超过 ${maxSizeMB}MB!`)
    }
    
    return true
  }

  // 验证视频文件
  static validateVideo(file, maxSizeMB = 50) {
    const allowedTypes = [
      'video/mp4',
      'video/avi',
      'video/mov',
      'video/wmv',
      'video/flv',
      'video/mkv',
      'video/webm'
    ]
    
    if (!file.type.startsWith('video/')) {
      throw new Error('只能上传视频文件!')
    }
    
    if (!this.validateFileType(file, allowedTypes)) {
      throw new Error('只支持 MP4、AVI、MOV、WMV、FLV、MKV、WebM 格式的视频!')
    }
    
    if (!this.validateFileSize(file, maxSizeMB)) {
      throw new Error(`视频大小不能超过 ${maxSizeMB}MB!`)
    }
    
    return true
  }
}

export default FileUploader 