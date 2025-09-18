import api from '@/utils/api'

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

  // 分配用户角色
  assignUserRoles: (id, roleIds) => api.put(`/user/${id}/roles`, { role_ids: roleIds }),

  // 上传头像
  uploadAvatar: (id, formData) => api.post(`/user/${id}/avatar`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export default userAPI
