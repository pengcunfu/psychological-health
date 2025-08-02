import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response && error.response.status === 401) {
      // 未授权，清除token并跳转到登录页
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 用户管理API
export const userAPI = {
  // 获取用户列表
  getUsers: (params) => api.get('/user', { params }),
  
  // 获取用户详情
  getUser: (id) => api.get(`/user/${id}`),
  
  // 创建用户
  createUser: (data) => api.post('/user', data),
  
  // 更新用户
  updateUser: (id, data) => api.put(`/user/${id}`, data),
  
  // 删除用户
  deleteUser: (id) => api.delete(`/user/${id}`),
  
  // 更新用户状态
  updateUserStatus: (id, status) => api.put(`/user/${id}/status`, { status }),
  
  // 重置密码
  resetPassword: (id) => api.post(`/user/${id}/reset-password`),
  
  // 上传头像
  uploadAvatar: (id, formData) => api.post(`/user/${id}/avatar`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 咨询师管理API
export const counselorAPI = {
  // 获取咨询师列表
  getCounselors: (params) => api.get('/counselor', { params }),
  
  // 获取咨询师详情
  getCounselor: (id) => api.get(`/counselor/${id}`),
  
  // 创建咨询师
  createCounselor: (data) => api.post('/counselor', data),
  
  // 更新咨询师
  updateCounselor: (id, data) => api.put(`/counselor/${id}`, data),
  
  // 删除咨询师
  deleteCounselor: (id) => api.delete(`/counselor/${id}`),
  
  // 更新咨询师状态
  updateCounselorStatus: (id, status) => api.put(`/counselor/${id}/status`, { status }),
  
  // 获取咨询师评价
  getCounselorReviews: (id, params) => api.get(`/counselor/${id}/reviews`, { params }),
  
  // 上传头像
  uploadAvatar: (id, formData) => api.post(`/counselor/${id}/avatar`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }),
  
  // 获取咨询师可用时间
  getAvailableTimes: (id, params) => api.get(`/counselor/${id}/available-times`, { params })
}

// 课程管理API
export const courseAPI = {
  // 获取课程列表
  getCourses: (params) => api.get('/course', { params }),
  
  // 获取课程详情
  getCourse: (id) => api.get(`/course/${id}`),
  
  // 创建课程
  createCourse: (data) => api.post('/course', data),
  
  // 更新课程
  updateCourse: (id, data) => api.put(`/course/${id}`, data),
  
  // 删除课程
  deleteCourse: (id) => api.delete(`/course/${id}`),
  
  // 上传课程封面
  uploadCover: (id, formData) => api.post(`/course/${id}/cover`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }),
  
  // 获取课程评价
  getCourseReviews: (id, params) => api.get(`/course/${id}/reviews`, { params }),
  
  // 获取课程章节
  getCourseChapters: (id) => api.get(`/course/${id}/chapters`)
}

// 订单管理API
export const orderAPI = {
  // 获取订单列表
  getOrders: (params) => api.get('/order', { params }),
  
  // 获取订单详情
  getOrder: (id) => api.get(`/order/${id}`),
  
  // 更新订单状态
  updateOrderStatus: (id, status) => api.put(`/order/${id}/status`, { status }),
  
  // 取消订单
  cancelOrder: (id, reason) => api.post(`/order/${id}/cancel`, { reason }),
  
  // 退款
  refundOrder: (id, data) => api.post(`/order/${id}/refund`, data),
  
  // 获取订单统计
  getOrderStats: (params) => api.get('/order/stats', { params })
}

// 公告管理API
export const announcementAPI = {
  // 获取公告列表
  getAnnouncements: (params) => api.get('/announcement', { params }),
  
  // 获取公告详情
  getAnnouncement: (id) => api.get(`/announcement/${id}`),
  
  // 创建公告
  createAnnouncement: (data) => api.post('/announcement', data),
  
  // 更新公告
  updateAnnouncement: (id, data) => api.put(`/announcement/${id}`, data),
  
  // 删除公告
  deleteAnnouncement: (id) => api.delete(`/announcement/${id}`),
  
  // 置顶公告
  pinAnnouncement: (id, isPinned) => api.put(`/announcement/${id}/pin`, { is_pinned: isPinned })
}

// 分类管理API
export const categoryAPI = {
  // 获取分类列表
  getCategories: (params) => api.get('/category', { params }),
  
  // 获取分类详情
  getCategory: (id) => api.get(`/category/${id}`),
  
  // 创建分类
  createCategory: (data) => api.post('/category', data),
  
  // 更新分类
  updateCategory: (id, data) => api.put(`/category/${id}`, data),
  
  // 删除分类
  deleteCategory: (id) => api.delete(`/category/${id}`),
  
  // 获取分类下的项目
  getCategoryItems: (id, params) => api.get(`/category/${id}/items`, { params })
}

// 评价管理API
export const reviewAPI = {
  // 获取评价列表
  getReviews: (params) => api.get('/review', { params }),
  
  // 获取评价详情
  getReview: (id) => api.get(`/review/${id}`),
  
  // 审核评价
  auditReview: (id, status) => api.put(`/review/${id}/audit`, { status }),
  
  // 删除评价
  deleteReview: (id) => api.delete(`/review/${id}`),
  
  // 回复评价
  replyReview: (id, content) => api.post(`/review/${id}/reply`, { content })
}

// 预约管理API
export const appointmentAPI = {
  // 获取预约列表
  getAppointments: (params) => api.get('/appointment', { params }),
  
  // 获取预约详情
  getAppointment: (id) => api.get(`/appointment/${id}`),
  
  // 创建预约
  createAppointment: (data) => api.post('/appointment', data),
  
  // 更新预约
  updateAppointment: (id, data) => api.put(`/appointment/${id}`, data),
  
  // 更新预约状态
  updateAppointmentStatus: (id, status) => api.put(`/appointment/${id}/status`, { status }),
  
  // 取消预约
  cancelAppointment: (id, reason) => api.post(`/appointment/${id}/cancel`, { reason }),
  
  // 获取可用时间段
  getAvailableTimeSlots: (params) => api.get('/appointment/available-slots', { params })
}

// 角色管理API
export const roleAPI = {
  // 获取角色列表
  getRoles: (params) => api.get('/role', { params }),
  
  // 获取角色详情
  getRole: (id) => api.get(`/role/${id}`),
  
  // 创建角色
  createRole: (data) => api.post('/role', data),
  
  // 更新角色
  updateRole: (id, data) => api.put(`/role/${id}`, data),
  
  // 删除角色
  deleteRole: (id) => api.delete(`/role/${id}`),
  
  // 获取角色权限
  getRolePermissions: (id) => api.get(`/role/${id}/permissions`),
  
  // 更新角色权限
  updateRolePermissions: (id, permissions) => api.put(`/role/${id}/permissions`, { permissions })
}

// 菜单管理API
export const menuAPI = {
  // 获取菜单列表
  getMenus: (params) => api.get('/menu', { params }),
  
  // 获取菜单详情
  getMenu: (id) => api.get(`/menu/${id}`),
  
  // 创建菜单
  createMenu: (data) => api.post('/menu', data),
  
  // 更新菜单
  updateMenu: (id, data) => api.put(`/menu/${id}`, data),
  
  // 删除菜单
  deleteMenu: (id) => api.delete(`/menu/${id}`),
  
  // 获取菜单树
  getMenuTree: () => api.get('/menu/tree')
}

// 统计分析API
export const statsAPI = {
  // 获取总体统计
  getOverview: () => api.get('/stats/overview'),
  
  // 获取用户统计
  getUserStats: (params) => api.get('/stats/user', { params }),
  
  // 获取订单统计
  getOrderStats: (params) => api.get('/stats/order', { params }),
  
  // 获取课程统计
  getCourseStats: (params) => api.get('/stats/course', { params }),
  
  // 获取咨询师统计
  getCounselorStats: (params) => api.get('/stats/counselor', { params })
}

// 系统设置API
export const settingAPI = {
  // 获取系统设置
  getSettings: () => api.get('/setting'),
  
  // 更新系统设置
  updateSettings: (data) => api.put('/setting', data),
  
  // 获取支付设置
  getPaymentSettings: () => api.get('/setting/payment'),
  
  // 更新支付设置
  updatePaymentSettings: (data) => api.put('/setting/payment', data),
  
  // 获取短信设置
  getSmsSettings: () => api.get('/setting/sms'),
  
  // 更新短信设置
  updateSmsSettings: (data) => api.put('/setting/sms', data)
}

// 文件上传API
export const uploadAPI = {
  // 上传图片
  uploadImage: (formData) => api.post('/upload/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }),
  
  // 上传文件
  uploadFile: (formData) => api.post('/upload/file', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 认证API
export const authAPI = {
  // 登录
  login: (data) => api.post('/auth/login', data),
  
  // 登出
  logout: () => api.post('/auth/logout'),
  
  // 获取当前用户信息
  getCurrentUser: () => api.get('/auth/current-user'),
  
  // 获取验证码
  getVerifyCode: () => {
    const url = `${api.defaults.baseURL}/auth/verify-code?t=${new Date().getTime()}`;
    return url;
  },
  
  // 修改密码
  changePassword: (data) => api.post('/auth/change-password', data),
  
  // 重置密码
  resetPassword: (data) => api.post('/auth/reset-password', data)
}

export default {
  userAPI,
  counselorAPI,
  courseAPI,
  orderAPI,
  announcementAPI,
  categoryAPI,
  reviewAPI,
  appointmentAPI,
  roleAPI,
  menuAPI,
  statsAPI,
  settingAPI,
  uploadAPI,
  authAPI
} 