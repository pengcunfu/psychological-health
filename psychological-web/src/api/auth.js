import api from '@/utils/api'

// 认证API
export const authAPI = {
    // 登录
    login: (data) => api.post('/auth/login', data),

    // 登出
    logout: () => api.post('/auth/logout'),

    // 获取当前用户信息
    getCurrentUser: () => api.get('/auth/profile'),

    // 更新用户信息
    updateProfile: (data) => api.put('/auth/profile', data),

    // 获取验证码
    getVerifyCode: () => {
        const url = `${api.defaults.baseURL}/auth/verify-code?t=${new Date().getTime()}`
        return url
    },

    // 修改密码
    changePassword: (data) => api.put('/auth/change-password', data),

    // 重置密码
    resetPassword: (data) => api.post('/auth/reset-password', data)
}

export default authAPI 