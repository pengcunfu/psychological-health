import api from '@/utils/api'

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

  // 获取菜单树结构
  getMenuTree: () => api.get('/menu/tree'),

  // 获取用户权限菜单
  getUserPermissions: (userId) => api.get(`/menu/user/${userId}/permissions`)
}

// 群组管理API
export const groupAPI = {
  // 获取群组列表
  getGroups: (params) => api.get('/group', { params }),

  // 获取群组详情
  getGroup: (id) => api.get(`/group/${id}`),

  // 创建群组
  createGroup: (data) => api.post('/group', data),

  // 更新群组
  updateGroup: (id, data) => api.put(`/group/${id}`, data),

  // 删除群组
  deleteGroup: (id) => api.delete(`/group/${id}`)
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

// 工作空间管理API
export const workspaceAPI = {
  // 获取工作空间列表
  getWorkspaces: (params) => api.get('/workspace', { params }),

  // 获取工作空间详情
  getWorkspace: (id) => api.get(`/workspace/${id}`),

  // 创建工作空间
  createWorkspace: (data) => api.post('/workspace', data),

  // 更新工作空间
  updateWorkspace: (id, data) => api.put(`/workspace/${id}`, data),

  // 删除工作空间
  deleteWorkspace: (id) => api.delete(`/workspace/${id}`)
}

// 向后兼容的单独导出函数
export const getRoles = (params) => api.get('/role', { params })
export const getRole = (id) => api.get(`/role/${id}`)
export const createRole = (data) => api.post('/role', data)
export const updateRole = (id, data) => api.put(`/role/${id}`, data)
export const deleteRole = (id) => api.delete(`/role/${id}`)

// 疾病标签管理接口
export const getDiseaseTags = (params) => api.get('/disease-tag', { params })
export const getDiseaseTag = (id) => api.get(`/disease-tag/${id}`)
export const createDiseaseTag = (data) => api.post('/disease-tag', data)
export const updateDiseaseTag = (id, data) => api.put(`/disease-tag/${id}`, data)
export const deleteDiseaseTag = (id) => api.delete(`/disease-tag/${id}`)

// 工作空间管理接口（向后兼容）
export const getWorkspaces = (params) => workspaceAPI.getWorkspaces(params)
export const getWorkspace = (id) => workspaceAPI.getWorkspace(id)
export const createWorkspace = (data) => workspaceAPI.createWorkspace(data)
export const updateWorkspace = (id, data) => workspaceAPI.updateWorkspace(id, data)
export const deleteWorkspace = (id) => workspaceAPI.deleteWorkspace(id)

export default { roleAPI, menuAPI, groupAPI, statsAPI, settingAPI, workspaceAPI } 