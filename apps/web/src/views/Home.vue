<template>
  <div class="admin-layout">
    <!-- 左侧菜单 -->
    <div class="sidebar" :class="{ collapsed: collapsed }">
      <div class="logo">
        <h2 v-if="!collapsed">心理健康平台</h2>
        <h2 v-else>心理</h2>
      </div>

      <div class="menu">
        <!-- 首页 -->
        <div class="menu-item" :class="{ active: activePath === '/' }" @click="navigateTo('/')">
          <span class="menu-icon"><home-outlined /></span>
          <span class="menu-text" v-if="!collapsed">首页</span>
        </div>

        <!-- 用户管理分类 -->
        <div class="menu-category">
          <div class="category-header" @click="toggleCategory('user')" :class="{ active: activeCategoryKey === 'user' }">
            <span class="menu-icon"><team-outlined /></span>
            <span class="menu-text" v-if="!collapsed">用户管理</span>
            <span class="arrow" v-if="!collapsed">
              <down-outlined v-if="activeCategoryKey === 'user'" />
              <right-outlined v-else />
            </span>
          </div>
          <div class="category-items" v-show="activeCategoryKey === 'user' && !collapsed">
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/users' }" @click="navigateTo('/admin/users')">
              <span class="menu-text">用户列表</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/counselors' }" @click="navigateTo('/admin/counselors')">
              <span class="menu-text">咨询师管理</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/roles' }" @click="navigateTo('/admin/roles')">
              <span class="menu-text">角色管理</span>
            </div>
          </div>
        </div>

        <!-- 内容管理分类 -->
        <div class="menu-category">
          <div class="category-header" @click="toggleCategory('content')" :class="{ active: activeCategoryKey === 'content' }">
            <span class="menu-icon"><read-outlined /></span>
            <span class="menu-text" v-if="!collapsed">内容管理</span>
            <span class="arrow" v-if="!collapsed">
              <down-outlined v-if="activeCategoryKey === 'content'" />
              <right-outlined v-else />
            </span>
          </div>
          <div class="category-items" v-show="activeCategoryKey === 'content' && !collapsed">
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/courses' }" @click="navigateTo('/admin/courses')">
              <span class="menu-text">课程管理</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/course-outlines' }" @click="navigateTo('/admin/course-outlines')">
              <span class="menu-text">课程大纲</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/announcements' }" @click="navigateTo('/admin/announcements')">
              <span class="menu-text">公告管理</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/banners' }" @click="navigateTo('/admin/banners')">
              <span class="menu-text">横幅管理</span>
            </div>
          </div>
        </div>

        <!-- 业务管理分类 -->
        <div class="menu-category">
          <div class="category-header" @click="toggleCategory('business')" :class="{ active: activeCategoryKey === 'business' }">
            <span class="menu-icon"><shopping-outlined /></span>
            <span class="menu-text" v-if="!collapsed">业务管理</span>
            <span class="arrow" v-if="!collapsed">
              <down-outlined v-if="activeCategoryKey === 'business'" />
              <right-outlined v-else />
            </span>
          </div>
          <div class="category-items" v-show="activeCategoryKey === 'business' && !collapsed">
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/orders' }" @click="navigateTo('/admin/orders')">
              <span class="menu-text">订单管理</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/appointments' }" @click="navigateTo('/admin/appointments')">
              <span class="menu-text">预约管理</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/assessments' }" @click="navigateTo('/admin/assessments')">
              <span class="menu-text">心理测评</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/reviews' }" @click="navigateTo('/admin/reviews')">
              <span class="menu-text">评价管理</span>
            </div>
          </div>
        </div>

        <!-- 系统设置分类 -->
        <div class="menu-category">
          <div class="category-header" @click="toggleCategory('system')" :class="{ active: activeCategoryKey === 'system' }">
            <span class="menu-icon"><setting-outlined /></span>
            <span class="menu-text" v-if="!collapsed">系统设置</span>
            <span class="arrow" v-if="!collapsed">
              <down-outlined v-if="activeCategoryKey === 'system'" />
              <right-outlined v-else />
            </span>
          </div>
          <div class="category-items" v-show="activeCategoryKey === 'system' && !collapsed">
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/categories' }" @click="navigateTo('/admin/categories')">
              <span class="menu-text">分类管理</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/disease-tags' }" @click="navigateTo('/admin/disease-tags')">
              <span class="menu-text">疾病标签</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/menus' }" @click="navigateTo('/admin/menus')">
              <span class="menu-text">菜单管理</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/groups' }" @click="navigateTo('/admin/groups')">
              <span class="menu-text">群组管理</span>
            </div>
            <div class="menu-item sub-item" :class="{ active: activePath === '/admin/workspaces' }" @click="navigateTo('/admin/workspaces')">
              <span class="menu-text">工作空间</span>
            </div>
          </div>
        </div>
      </div>

      <div class="collapse-button" @click="toggleCollapse">
        <menu-fold-outlined v-if="!collapsed" />
        <menu-unfold-outlined v-else />
      </div>
    </div>

    <!-- 右侧内容区 -->
    <div class="main-content">
      <!-- 顶部导航栏 -->
      <div class="header">
        <div class="breadcrumb">
          <span>{{ getPageTitle() }}</span>
        </div>
        <div class="user-info">
          <span>欢迎, {{ user?.username || '用户' }}</span>
          <a-dropdown>
            <a class="user-dropdown" @click.prevent>
              <a-avatar :size="32" :src="user?.avatar">{{ user?.username?.charAt(0).toUpperCase() || 'U' }}</a-avatar>
              <span class="username">{{ user?.username || '用户' }}</span>
              <down-outlined/>
            </a>
            <template #overlay>
              <a-menu>
                <a-menu-item key="profile">
                  <user-outlined/>
                  个人资料
                </a-menu-item>
                <a-menu-item key="settings">
                  <setting-outlined/>
                  系统设置
                </a-menu-item>
                <a-menu-divider/>
                <a-menu-item key="logout" @click="handleLogout">
                  <logout-outlined/>
                  退出登录
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </div>

      <!-- 内容区域 -->
      <div class="content">
        <router-view v-if="$route.path !== '/'"/>
        <div v-else class="dashboard">
          <div class="welcome-card">
            <h2>欢迎使用心理健康平台管理系统</h2>
            <p>您可以使用左侧菜单导航到不同的管理功能。</p>
          </div>

          <div class="stats-cards">
            <a-row :gutter="16">
              <a-col :span="6">
                <a-card>
                  <template #title>用户总数</template>
                  <h3>1,286</h3>
                  <p>较上周 <span style="color: #52c41a">+12%</span></p>
                </a-card>
              </a-col>
              <a-col :span="6">
                <a-card>
                  <template #title>咨询师总数</template>
                  <h3>86</h3>
                  <p>较上周 <span style="color: #52c41a">+5%</span></p>
                </a-card>
              </a-col>
              <a-col :span="6">
                <a-card>
                  <template #title>本周预约</template>
                  <h3>128</h3>
                  <p>较上周 <span style="color: #52c41a">+18%</span></p>
                </a-card>
              </a-col>
              <a-col :span="6">
                <a-card>
                  <template #title>本周收入</template>
                  <h3>¥25,680</h3>
                  <p>较上周 <span style="color: #52c41a">+8%</span></p>
                </a-card>
              </a-col>
            </a-row>
          </div>

          <div class="quick-actions">
            <h3>快捷操作</h3>
            <div class="actions-grid">
              <router-link to="/admin/users" class="action-link">
                <a-card hoverable class="action-card">
                  <div class="action-content">
                    <div class="action-icon"><team-outlined /></div>
                    <div class="action-text">用户管理</div>
                  </div>
                </a-card>
              </router-link>

              <router-link to="/admin/counselors" class="action-link">
                <a-card hoverable class="action-card">
                  <div class="action-content">
                    <div class="action-icon"><team-outlined /></div>
                    <div class="action-text">咨询师管理</div>
                  </div>
                </a-card>
              </router-link>

              <router-link to="/admin/courses" class="action-link">
                <a-card hoverable class="action-card">
                  <div class="action-content">
                    <div class="action-icon"><read-outlined /></div>
                    <div class="action-text">课程管理</div>
                  </div>
                </a-card>
              </router-link>

              <router-link to="/admin/orders" class="action-link">
                <a-card hoverable class="action-card">
                  <div class="action-content">
                    <div class="action-icon"><shopping-outlined /></div>
                    <div class="action-text">订单管理</div>
                  </div>
                </a-card>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {ref, onMounted, computed} from 'vue'
import {useRouter, useRoute} from 'vue-router'
import {message} from 'ant-design-vue'
import {authAPI} from '@/api/admin'
import {
  UserOutlined, 
  SettingOutlined, 
  LogoutOutlined, 
  DownOutlined, 
  RightOutlined,
  HomeOutlined,
  TeamOutlined,
  ReadOutlined,
  ShoppingOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined
} from '@ant-design/icons-vue'

export default {
  name: 'Home',
  components: {
    UserOutlined,
    SettingOutlined,
    LogoutOutlined,
    DownOutlined,
    RightOutlined,
    HomeOutlined,
    TeamOutlined,
    ReadOutlined,
    ShoppingOutlined,
    MenuFoldOutlined,
    MenuUnfoldOutlined
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const user = ref(null)
    const collapsed = ref(false)
    const activeCategoryKey = ref('')

    const activePath = computed(() => {
      return route.path
    })

    // 根据当前路径自动展开对应的菜单分类
    const initActiveCategory = () => {
      const path = route.path
      if (path.includes('/admin/users') || path.includes('/admin/counselors') || path.includes('/admin/roles')) {
        activeCategoryKey.value = 'user'
      } else if (path.includes('/admin/courses') || path.includes('/admin/course-outlines') || 
                path.includes('/admin/announcements') || path.includes('/admin/banners')) {
        activeCategoryKey.value = 'content'
      } else if (path.includes('/admin/orders') || path.includes('/admin/appointments') || 
                path.includes('/admin/reviews')) {
        activeCategoryKey.value = 'business'
      } else if (path.includes('/admin/categories') || path.includes('/admin/disease-tags') || 
                path.includes('/admin/menus') || path.includes('/admin/groups') || 
                path.includes('/admin/workspaces')) {
        activeCategoryKey.value = 'system'
      }
    }

    const toggleCategory = (key) => {
      if (collapsed.value) {
        collapsed.value = false
        activeCategoryKey.value = key
      } else {
        activeCategoryKey.value = activeCategoryKey.value === key ? '' : key
      }
    }

    const handleLogout = async () => {
      try {
        await authAPI.logout()
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        message.success('退出登录成功')
        router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
        // 即使API调用失败，也清除本地存储
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push('/login')
      }
    }

    const toggleCollapse = () => {
      collapsed.value = !collapsed.value
      if (collapsed.value) {
        activeCategoryKey.value = ''
      } else {
        initActiveCategory()
      }
    }

    const navigateTo = (path) => {
      router.push(path)
    }

    const getPageTitle = () => {
      if (route.path === '/') {
        return '首页'
      }

      const routeMatch = route.matched.find(r => r.meta.title)
      return routeMatch ? routeMatch.meta.title : '心理健康平台'
    }

    onMounted(() => {
      // 从localStorage获取用户信息
      const userInfo = localStorage.getItem('user')
      if (userInfo) {
        try {
          user.value = JSON.parse(userInfo)
        } catch (error) {
          console.error('Parse user info error:', error)
        }
      }
      
      // 初始化激活的菜单分类
      initActiveCategory()
    })

    return {
      user,
      collapsed,
      activePath,
      activeCategoryKey,
      handleLogout,
      toggleCollapse,
      toggleCategory,
      navigateTo,
      getPageTitle
    }
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* 左侧菜单样式 */
.sidebar {
  width: 220px;
  background: #001529;
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
}

.sidebar.collapsed {
  width: 80px;
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo h2 {
  color: white;
  margin: 0;
  font-size: 18px;
  white-space: nowrap;
}

.menu {
  flex: 1;
  padding: 16px 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.3s;
  margin-bottom: 4px;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.menu-item.active {
  background: #1890ff;
}

.menu-icon {
  font-size: 16px;
  margin-right: 12px;
  width: 20px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-text {
  white-space: nowrap;
  opacity: 1;
  transition: opacity 0.3s;
}

/* 菜单分类样式 */
.menu-category {
  margin-bottom: 4px;
}

.category-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.3s;
  position: relative;
}

.category-header:hover {
  background: rgba(255, 255, 255, 0.1);
}

.category-header.active {
  background: rgba(24, 144, 255, 0.2);
}

.arrow {
  position: absolute;
  right: 16px;
  font-size: 12px;
}

.category-items {
  margin-left: 8px;
}

.sub-item {
  padding: 10px 16px 10px 40px;
  margin-bottom: 2px;
}

.collapse-button {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* 右侧内容区样式 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  height: 64px;
  background: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.breadcrumb {
  font-size: 16px;
  font-weight: 500;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: inherit;
  text-decoration: none;
}

.username {
  margin: 0 4px;
}

.content {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
  background: #f0f2f5;
}

/* 仪表盘样式 */
.dashboard {
  /* max-width: 1200px; */
  margin: 0 auto;
}

.welcome-card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.welcome-card h2 {
  color: #1890ff;
  margin-bottom: 16px;
}

.stats-cards {
  margin-bottom: 24px;
}

.stats-cards h3 {
  font-size: 24px;
  margin: 8px 0;
}

.quick-actions {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.quick-actions h3 {
  margin-bottom: 20px;
  color: #333;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.action-link {
  text-decoration: none;
  color: inherit;
}

.action-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.action-card:hover {
  transform: translateY(-2px);
}

.action-content {
  text-align: center;
  padding: 20px;
}

.action-icon {
  font-size: 24px;
  margin-bottom: 12px;
  color: #1890ff;
}

.action-text {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

/* 响应式样式 */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 100;
    height: 100vh;
    left: 0;
    top: 0;
  }

  .sidebar.collapsed {
    left: -80px;
  }

  .main-content {
    margin-left: 0;
  }

  .content {
    padding: 16px;
  }

  .header {
    padding: 0 16px;
  }

  .username {
    display: none;
  }

  .stats-cards .ant-col {
    width: 100%;
    margin-bottom: 16px;
  }
}
</style> 