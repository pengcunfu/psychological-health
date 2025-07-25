import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    token: null,
    userId: null,
    userInfo: null,
    statistics: null,
    isLoggedIn: false
  }),
  
  getters: {
    getUserInfo: (state) => state.userInfo,
    getToken: (state) => state.token,
    getIsLoggedIn: (state) => state.isLoggedIn,
    getStatistics: (state) => state.statistics
  },
  
  actions: {
    async loginByPhone(phone, code) {
      try {
        const response = await fetch('/api/user/login/phone', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ phone, code })
        });
        const data = await response.json();
        
        this.setLoginState(data);
        return data;
      } catch (error) {
        console.error('登录失败', error);
        throw error;
      }
    },
    
    async loginByWechat(code) {
      try {
        const response = await fetch('/api/user/login/wechat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ code })
        });
        const data = await response.json();
        
        this.setLoginState(data);
        return data;
      } catch (error) {
        console.error('微信登录失败', error);
        throw error;
      }
    },
    
    async fetchUserProfile() {
      try {
        const response = await fetch('/api/user/profile', {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        });
        const data = await response.json();
        
        this.userInfo = data;
        return data;
      } catch (error) {
        console.error('获取用户信息失败', error);
        throw error;
      }
    },
    
    async updateUserProfile(profileData) {
      try {
        const response = await fetch('/api/user/profile/update', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`
          },
          body: JSON.stringify(profileData)
        });
        
        await this.fetchUserProfile();
        return await response.json();
      } catch (error) {
        console.error('更新用户信息失败', error);
        throw error;
      }
    },
    
    async fetchUserStatistics() {
      try {
        const response = await fetch('/api/user/statistics', {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        });
        const data = await response.json();
        
        this.statistics = data;
        return data;
      } catch (error) {
        console.error('获取用户统计数据失败', error);
        throw error;
      }
    },
    
    setLoginState(data) {
      this.token = data.token;
      this.userId = data.userId;
      this.isLoggedIn = true;
      localStorage.setItem('token', data.token);
      localStorage.setItem('userId', data.userId);
    },
    
    logout() {
      this.token = null;
      this.userId = null;
      this.userInfo = null;
      this.statistics = null;
      this.isLoggedIn = false;
      localStorage.removeItem('token');
      localStorage.removeItem('userId');
    },
    
    checkLoginStatus() {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');
      
      if (token && userId) {
        this.token = token;
        this.userId = userId;
        this.isLoggedIn = true;
        this.fetchUserProfile();
        return true;
      }
      
      return false;
    }
  }
});
