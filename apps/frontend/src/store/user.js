import { defineStore } from 'pinia'
import { ref } from 'vue'
import { request } from '@/utils/request'
import { setToken, getToken, removeToken } from '@/utils/auth'
import { logout as logoutApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(getToken() || '')
  const userInfo = ref(null)
  const isLoggedIn = ref(!!getToken())

  // 设置登录信息
  const setLoginInfo = async (loginData) => {
    token.value = loginData.token
    userInfo.value = loginData.user
    isLoggedIn.value = true
    
    // 保存token到本地存储
    setToken(loginData.token)
    
    return {
      success: true,
      message: '登录成功'
    }
  }

  // 登录（保持兼容性）
  const login = async (data) => {
    try {
      const res = await request({
        url: '/auth/login',
        method: 'POST',
        data
      })

      if (res.code === 200 && res.success) {
        return await setLoginInfo(res.data)
      }
      
      return {
        success: false,
        message: res.message || '登录失败'
      }
    } catch (error) {
      console.error('登录失败:', error)
      return {
        success: false,
        message: '登录失败，请检查网络连接'
      }
    }
  }

  // 退出登录
  const logout = async () => {
    try {
      await logoutApi()
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      // 无论请求成功与否，都清除本地登录状态
      token.value = ''
      userInfo.value = null
      isLoggedIn.value = false
      removeToken()
    }
  }

  // 获取用户信息
  const getUserInfo = async () => {
    if (!token.value) {
      return {
        success: false,
        message: '未登录'
      }
    }

    try {
      const res = await request({
        url: '/auth/profile',
        method: 'GET'
      })

      if (res.code === 200 && res.success) {
        userInfo.value = res.data
        return {
          success: true,
          data: res.data
        }
      }
      
      return {
        success: false,
        message: res.message || '获取用户信息失败'
      }
    } catch (error) {
      console.error('获取用户信息失败:', error)
      return {
        success: false,
        message: '获取用户信息失败，请检查网络连接'
      }
    }
  }

  // 初始化用户信息（如果已登录）
  const initUserInfo = async () => {
    if (token.value) {
      return await getUserInfo()
    }
    return {
      success: false,
      message: '未登录'
    }
  }

  // 更新用户信息
  const updateUserInfo = async (data) => {
    try {
      const res = await request({
        url: '/auth/profile',
        method: 'PUT',
        data
      })

      if (res.code === 200 && res.success) {
        // 更新本地用户信息
        userInfo.value = {
          ...userInfo.value,
          ...res.data
        }
        
        return {
          success: true,
          message: '更新成功'
        }
      }
      
      return {
        success: false,
        message: res.message || '更新失败'
      }
    } catch (error) {
      console.error('更新用户信息失败:', error)
      return {
        success: false,
        message: '更新用户信息失败，请检查网络连接'
      }
    }
  }

  // 修改密码
  const changePassword = async (data) => {
    try {
      const res = await request({
        url: '/auth/change-password',
        method: 'PUT',
        data
      })

      return {
        success: res.code === 200 && res.success,
        message: res.message
      }
    } catch (error) {
      console.error('修改密码失败:', error)
      return {
        success: false,
        message: '修改密码失败，请检查网络连接'
      }
    }
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    setLoginInfo,
    login,
    logout,
    getUserInfo,
    initUserInfo,
    updateUserInfo,
    changePassword
  }
}) 