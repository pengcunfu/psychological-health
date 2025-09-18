import axios from 'axios'
import { message } from 'ant-design-vue'
import router from '@/router'

// 创建axios实例
const api = axios.create({
    baseURL: import.meta.env.VITE_APP_API_URL || '/api',
    timeout: 5000,
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
        const data = response.data

        // 检查success字段，如果为false，提示错误消息
        if (!data.success) {

            // 检查业务状态码，如果code为401，直接跳转到登录页面
            if (data.code === 401) {
                localStorage.removeItem('token')
                localStorage.removeItem('user')
                router.push('/login')
                return Promise.reject(new Error(data.message || '未授权访问'))
            }

            const errorMessage = data.message || '操作失败'
            // 这里可以使用全局的消息提示组件
            console.error('API Error:', errorMessage)
            message.error(data.message || '操作失败')
            return Promise.reject(new Error(errorMessage))

        }

        return data
    },
    error => {
        // HTTP状态码错误处理
        if (error.response) {
            const { status, data } = error.response

            // 其他HTTP错误
            const errorMessage = data?.message || `请求失败 (${status})`
            message.error(errorMessage)
            return Promise.reject(new Error(errorMessage))
        }

        // 网络错误或超时
        if (error.code === 'ECONNABORTED') {
            message.error('请求超时')
            return Promise.reject(new Error('请求超时'))
        }

        message.error('网络错误，请检查网络连接')
        return Promise.reject(new Error('网络错误，请检查网络连接'))
    }
)

export default api 