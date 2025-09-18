import api from '@/utils/api'
import { FileUploader } from '@/utils/FileUploader'

/**
 * 文件上传API类
 */
export class uploadAPI {
  // 上传头像
  static async uploadAvatar(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      return await api.post('/upload/avatar', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } catch (error) {
      console.error('上传头像失败:', error)
      throw error
    }
  }

  // 上传横幅图
  static async uploadBanner(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      return await api.post('/upload/banner', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } catch (error) {
      console.error('上传横幅图失败:', error)
      throw error
    }
  }

  // 上传课程封面
  static async uploadCourseCover(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      return await api.post('/upload/course-cover', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } catch (error) {
      console.error('上传课程封面失败:', error)
      throw error
    }
  }

  // 上传课程视频
  static async uploadCourseVideo(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      return await api.post('/upload/course-video', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } catch (error) {
      console.error('上传课程视频失败:', error)
      throw error
    }
  }

  // 上传测评封面
  static async uploadAssessment(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      return await api.post('/upload/assessment', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } catch (error) {
      console.error('上传测评封面失败:', error)
      throw error
    }
  }

  // 通用图片上传
  static async uploadImage(formData) {
    try {
      return await api.post('/upload/image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } catch (error) {
      console.error('上传图片失败:', error)
      throw error
    }
  }

  // 通用文件上传
  static async uploadFile(formData) {
    try {
      return await api.post('/upload/file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } catch (error) {
      console.error('上传文件失败:', error)
      throw error
    }
  }

  // 通用文件上传（带参数）
  static async upload(file, fileType = null, useUniqueName = true) {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      if (fileType) {
        formData.append('file_type', fileType)
      }
      
      formData.append('use_unique_name', useUniqueName.toString())

      return await api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } catch (error) {
      console.error('上传文件失败:', error)
      throw error
    }
  }
}

// 向后兼容的单独导出函数
export const uploadAvatar = (file) => uploadAPI.uploadAvatar(file)
export const uploadBanner = (file) => uploadAPI.uploadBanner(file)
export const uploadCourseCover = (file) => uploadAPI.uploadCourseCover(file)
export const uploadCourseVideo = (file) => uploadAPI.uploadCourseVideo(file)
export const uploadAssessment = (file) => uploadAPI.uploadAssessment(file)
export const uploadFile = (file, fileType, useUniqueName) => uploadAPI.upload(file, fileType, useUniqueName)

// 兼容导出FileUploader类（从utils目录导入）
export { FileUploader } from '@/utils/FileUploader'

// 默认导出（保持向后兼容）
export default {
  uploadAvatar,
  uploadBanner,
  uploadCourseCover,
  uploadCourseVideo,
  uploadAssessment,
  uploadFile,
  FileUploader,
  // 新的API类
  uploadAPI
}
