import axios from 'axios'

// 创建axios实例
const api = axios.create({
    baseURL: import.meta.env.VITE_APP_API_URL || '/api',
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
            localStorage.removeItem('user')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

// 认证相关API
export const authAPI = {
    // 登录
    login: (credentials) => api.post('/auth/login', credentials),

    // 登出
    logout: () => api.post('/auth/logout'),

    // 注册
    register: (userData) => api.post('/auth/register', userData),

    // 获取验证码
    getVerifyCode: () => api.get('/auth/verify-code', {responseType: 'blob'}),

    // 获取用户信息
    getProfile: () => api.get('/auth/profile'),

    // 刷新token
    refreshToken: () => api.post('/auth/refresh-token')
}

export default api 