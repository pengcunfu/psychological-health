import api from '@/utils/api'

// 统一导出所有API模块
export { userAPI } from './user'
export { counselorAPI } from './counselor'
export { courseAPI, courseOutlineAPI, getCourses, getCourse, createCourse, updateCourse, deleteCourse, getCourseOutlines, getCourseOutline, createCourseOutline, updateCourseOutline, deleteCourseOutline } from './course'
export { authAPI } from './auth'
export { orderAPI } from './order'
export { announcementAPI, categoryAPI, bannerAPI } from './content'
export { reviewAPI, appointmentAPI, assessmentAPI } from './business'
export { roleAPI, menuAPI, groupAPI, statsAPI, settingAPI, workspaceAPI, getRoles, getRole, createRole, updateRole, deleteRole, getDiseaseTags, getDiseaseTag, createDiseaseTag, updateDiseaseTag, deleteDiseaseTag, getWorkspaces, getWorkspace, createWorkspace, updateWorkspace, deleteWorkspace } from './system'
export { uploadAPI, uploadAvatar, uploadBanner, uploadCourseCover, uploadCourseVideo, uploadAssessment, uploadFile, FileUploader } from './upload'

// 从原来的 admin.js 导入咨询人API（如果存在的话）
export { consultantAPI } from './consultant'

// 默认导出包含所有API的对象
export default {
  // 用户管理
  userAPI: () => import('./user').then(m => m.userAPI),
  
  // 咨询师管理
  counselorAPI: () => import('./counselor').then(m => m.counselorAPI),
  
  // 课程管理
  courseAPI: () => import('./course').then(m => m.courseAPI),
  courseOutlineAPI: () => import('./course').then(m => m.courseOutlineAPI),
  
  // 认证
  authAPI: () => import('./auth').then(m => m.authAPI),
  
  // 订单管理
  orderAPI: () => import('./order').then(m => m.orderAPI),
  
  // 内容管理
  announcementAPI: () => import('./content').then(m => m.announcementAPI),
  categoryAPI: () => import('./content').then(m => m.categoryAPI),
  bannerAPI: () => import('./content').then(m => m.bannerAPI),
  
  // 业务管理
  reviewAPI: () => import('./business').then(m => m.reviewAPI),
  appointmentAPI: () => import('./business').then(m => m.appointmentAPI),
  assessmentAPI: () => import('./business').then(m => m.assessmentAPI),
  
  // 系统管理
  roleAPI: () => import('./system').then(m => m.roleAPI),
  menuAPI: () => import('./system').then(m => m.menuAPI),
  groupAPI: () => import('./system').then(m => m.groupAPI),
  statsAPI: () => import('./system').then(m => m.statsAPI),
  settingAPI: () => import('./system').then(m => m.settingAPI),
  workspaceAPI: () => import('./system').then(m => m.workspaceAPI),
  
  // 文件上传
  uploadAPI: () => import('./upload').then(m => m.uploadAPI),
  
  // 咨询人管理（如果存在）
  consultantAPI: () => import('./consultant').then(m => m.consultantAPI).catch(() => null)
} 