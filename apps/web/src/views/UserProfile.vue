<template>
  <div class="profile-page">
    <!-- 顶部横幅 -->
    <div class="profile-banner">
      <div class="banner-content">
        <div class="user-overview">
          <div class="avatar-section">
            <a-upload
              name="avatar"
              :show-upload-list="false"
              :before-upload="beforeUpload"
              :custom-request="handleAvatarUpload"
              accept="image/*"
            >
              <div class="avatar-wrapper">
                <a-avatar :size="80" :src="profileForm.avatar" class="user-avatar">
                  {{ profileForm.username?.charAt(0).toUpperCase() || 'U' }}
                </a-avatar>
                <div class="avatar-edit">
                  <camera-outlined />
                </div>
              </div>
            </a-upload>
          </div>
          <div class="user-details">
            <h1 class="user-name">{{ profileForm.username || '用户名' }}</h1>
            <p class="user-subtitle">{{ profileForm.realName || '未设置真实姓名' }}</p>
            <div class="user-badges">
              <a-tag v-if="profileForm.phone" color="green" class="info-tag">
                <phone-outlined />
                已绑定手机
              </a-tag>
              <a-tag v-if="profileForm.email" color="blue" class="info-tag">
                <mail-outlined />
                已绑定邮箱
              </a-tag>
              <a-tag v-if="!profileForm.phone || !profileForm.email" color="orange" class="info-tag">
                <exclamation-circle-outlined />
                信息待完善
              </a-tag>
            </div>
          </div>
        </div>
        <div class="quick-stats">
          <div class="stat-card">
            <div class="stat-number">{{ profileForm.phone ? '已绑定' : '未绑定' }}</div>
            <div class="stat-label">手机号</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ profileForm.email ? '已绑定' : '未绑定' }}</div>
            <div class="stat-label">邮箱</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">正常</div>
            <div class="stat-label">账户状态</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="profile-content">
      <div class="content-container">
        <!-- 左侧导航 -->
        <div class="sidebar-nav">
          <div class="nav-menu">
            <div 
              class="nav-item" 
              :class="{ active: activeTab === 'basic' }"
              @click="activeTab = 'basic'"
            >
              <div class="nav-icon">
                <user-outlined />
              </div>
              <span>基本信息</span>
            </div>
            <div 
              class="nav-item" 
              :class="{ active: activeTab === 'password' }"
              @click="activeTab = 'password'"
            >
              <div class="nav-icon">
                <lock-outlined />
              </div>
              <span>修改密码</span>
            </div>
            <div 
              class="nav-item" 
              :class="{ active: activeTab === 'security' }"
              @click="activeTab = 'security'"
            >
              <div class="nav-icon">
                <security-scan-outlined />
              </div>
              <span>账户安全</span>
            </div>
          </div>
        </div>

        <!-- 右侧内容 -->
        <div class="main-content">
          <!-- 基本信息 -->
          <div v-if="activeTab === 'basic'" class="content-section">
            <div class="section-header">
              <h2>基本信息</h2>
              <p>管理您的个人基本信息</p>
            </div>
            
            <div class="form-container">
              <a-form
                ref="profileFormRef"
                :model="profileForm"
                :rules="profileRules"
                layout="vertical"
                @finish="handleProfileSubmit"
                class="profile-form"
              >
                <div class="form-grid">
                  <div class="form-group">
                    <a-form-item label="用户名" name="username">
                      <a-input 
                        v-model:value="profileForm.username" 
                        placeholder="请输入用户名"
                        :disabled="true"
                        size="large"
                        class="form-input"
                      />
                      <div class="input-tip">用户名创建后不可修改</div>
                    </a-form-item>
                  </div>
                  
                  <div class="form-group">
                    <a-form-item label="真实姓名" name="realName">
                      <a-input 
                        v-model:value="profileForm.realName" 
                        placeholder="请输入真实姓名"
                        size="large"
                        class="form-input"
                      />
                    </a-form-item>
                  </div>
                  
                  <div class="form-group">
                    <a-form-item label="手机号" name="phone">
                      <a-input 
                        v-model:value="profileForm.phone" 
                        placeholder="请输入手机号"
                        :maxlength="11"
                        size="large"
                        class="form-input"
                      />
                    </a-form-item>
                  </div>
                  
                  <div class="form-group">
                    <a-form-item label="邮箱地址" name="email">
                      <a-input 
                        v-model:value="profileForm.email" 
                        placeholder="请输入邮箱地址"
                        type="email"
                        size="large"
                        class="form-input"
                      />
                    </a-form-item>
                  </div>
                  
                  <div class="form-group">
                    <a-form-item label="性别" name="gender">
                      <a-radio-group v-model:value="profileForm.gender" size="large">
                        <a-radio :value="1" class="gender-radio">男</a-radio>
                        <a-radio :value="2" class="gender-radio">女</a-radio>
                        <a-radio :value="0" class="gender-radio">保密</a-radio>
                      </a-radio-group>
                    </a-form-item>
                  </div>
                  
                  <div class="form-group">
                    <a-form-item label="出生日期" name="birthday">
                      <a-date-picker 
                        v-model:value="profileForm.birthday" 
                        placeholder="请选择出生日期"
                        style="width: 100%"
                        size="large"
                        :disabledDate="disabledDate"
                        class="form-input"
                      />
                    </a-form-item>
                  </div>
                </div>
                
                <div class="form-group full-width">
                  <a-form-item label="个人简介" name="bio">
                    <a-textarea 
                      v-model:value="profileForm.bio" 
                      placeholder="请输入个人简介，让别人更好地了解您"
                      :rows="4"
                      :maxlength="500"
                      show-count
                      size="large"
                      class="form-textarea"
                    />
                  </a-form-item>
                </div>

                <div class="form-actions">
                  <a-button type="primary" html-type="submit" :loading="profileLoading" size="large" class="action-btn primary">
                    <save-outlined />
                    保存修改
                  </a-button>
                  <a-button @click="resetProfileForm" size="large" class="action-btn">
                    <reload-outlined />
                    重置
                  </a-button>
                </div>
              </a-form>
            </div>
          </div>

          <!-- 修改密码 -->
          <div v-if="activeTab === 'password'" class="content-section">
            <div class="section-header">
              <h2>修改密码</h2>
              <p>定期修改密码可以提高账户安全性</p>
            </div>
            
            <div class="form-container">
              <div class="password-form-wrapper">
                <a-form
                  ref="passwordFormRef"
                  :model="passwordForm"
                  :rules="passwordRules"
                  layout="vertical"
                  @finish="handlePasswordSubmit"
                  class="password-form"
                >
                  <div class="form-group">
                    <a-form-item label="当前密码" name="oldPassword">
                      <a-input-password 
                        v-model:value="passwordForm.oldPassword" 
                        placeholder="请输入当前密码"
                        autocomplete="current-password"
                        size="large"
                        class="form-input"
                      />
                    </a-form-item>
                  </div>

                  <div class="form-group">
                    <a-form-item label="新密码" name="newPassword">
                      <a-input-password 
                        v-model:value="passwordForm.newPassword" 
                        placeholder="请输入新密码"
                        autocomplete="new-password"
                        size="large"
                        class="form-input"
                      />
                      <div class="input-tip">密码长度至少6位，建议包含字母、数字和特殊字符</div>
                    </a-form-item>
                  </div>

                  <div class="form-group">
                    <a-form-item label="确认新密码" name="confirmPassword">
                      <a-input-password 
                        v-model:value="passwordForm.confirmPassword" 
                        placeholder="请再次输入新密码"
                        autocomplete="new-password"
                        size="large"
                        class="form-input"
                      />
                    </a-form-item>
                  </div>

                  <div class="form-actions">
                    <a-button type="primary" html-type="submit" :loading="passwordLoading" size="large" class="action-btn primary">
                      <key-outlined />
                      修改密码
                    </a-button>
                    <a-button @click="resetPasswordForm" size="large" class="action-btn">
                      <reload-outlined />
                      重置
                    </a-button>
                  </div>
                </a-form>
              </div>
            </div>
          </div>

          <!-- 账户安全 -->
          <div v-if="activeTab === 'security'" class="content-section">
            <div class="section-header">
              <h2>账户安全</h2>
              <p>管理您的账户安全设置</p>
            </div>
            
            <div class="security-grid">
              <div 
                v-for="item in securityItems" 
                :key="item.title"
                class="security-card"
                :class="{ disabled: item.disabled }"
              >
                <div class="security-icon" :style="{ backgroundColor: item.color }">
                  <component :is="item.icon" />
                </div>
                <div class="security-content">
                  <div class="security-title">
                    <span>{{ item.title }}</span>
                    <a-tag v-if="item.status" :color="item.statusColor" class="status-tag">
                      {{ item.status }}
                    </a-tag>
                  </div>
                  <div class="security-desc">{{ item.description }}</div>
                </div>
                <div class="security-action">
                  <a-button 
                    type="primary"
                    :disabled="item.disabled"
                    @click="item.action"
                    class="security-btn"
                  >
                    {{ item.actionText }}
                  </a-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { message } from 'ant-design-vue'
import { authAPI, uploadAPI } from '@/api'
import dayjs from 'dayjs'
import {
  UserOutlined,
  CameraOutlined,
  LockOutlined,
  SecurityScanOutlined,
  PhoneOutlined,
  MailOutlined,
  EyeOutlined,
  SaveOutlined,
  ReloadOutlined,
  KeyOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons-vue'

const activeTab = ref('basic')
const profileLoading = ref(false)
const passwordLoading = ref(false)
const profileFormRef = ref()
const passwordFormRef = ref()

// 个人信息表单
const profileForm = reactive({
  username: '',
  phone: '',
  email: '',
  realName: '',
  gender: 0,
  birthday: null,
  bio: '',
  avatar: ''
})

// 密码修改表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 个人信息验证规则
const profileRules = {
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  realName: [
    { max: 20, message: '真实姓名不能超过20个字符', trigger: 'blur' }
  ]
}

// 密码修改验证规则
const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' },
    { max: 20, message: '密码长度不能超过20位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value) => {
        if (value && value !== passwordForm.newPassword) {
          return Promise.reject('两次输入的密码不一致')
        }
        return Promise.resolve()
      },
      trigger: 'blur'
    }
  ]
}

// 账户安全项目
const securityItems = computed(() => [
  {
    icon: LockOutlined,
    color: '#52c41a',
    title: '登录密码',
    status: '正常',
    statusColor: 'green',
    description: '定期更换密码可以提高账户安全性',
    actionText: '修改',
    action: () => {
      activeTab.value = 'password'
    }
  },
  {
    icon: PhoneOutlined,
    color: profileForm.phone ? '#52c41a' : '#faad14',
    title: '手机绑定',
    status: profileForm.phone ? '已绑定' : '未绑定',
    statusColor: profileForm.phone ? 'green' : 'orange',
    description: profileForm.phone ? `已绑定手机：${profileForm.phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')}` : '绑定手机号可以提高账户安全性',
    actionText: profileForm.phone ? '更换' : '绑定',
    action: () => {
      activeTab.value = 'basic'
      message.info('请在基本信息页面修改手机号')
    }
  },
  {
    icon: MailOutlined,
    color: profileForm.email ? '#52c41a' : '#faad14',
    title: '邮箱绑定',
    status: profileForm.email ? '已绑定' : '未绑定',
    statusColor: profileForm.email ? 'green' : 'orange',
    description: profileForm.email ? `已绑定邮箱：${profileForm.email}` : '绑定邮箱可以用于密码找回',
    actionText: profileForm.email ? '更换' : '绑定',
    action: () => {
      activeTab.value = 'basic'
      message.info('请在基本信息页面修改邮箱')
    }
  },
  {
    icon: EyeOutlined,
    color: '#1890ff',
    title: '登录日志',
    status: '功能开发中',
    statusColor: 'blue',
    description: '查看最近的登录记录和安全日志',
    actionText: '查看',
    disabled: true,
    action: () => {
      message.info('功能开发中...')
    }
  }
])

// 获取用户信息
const getCurrentUser = async () => {
  try {
    const response = await authAPI.getCurrentUser()
    if (response.code === 200) {
      const user = response.data
      Object.assign(profileForm, {
        username: user.username,
        phone: user.phone || '',
        email: user.email || '',
        realName: user.real_name || '',
        gender: user.gender || 0,
        birthday: user.birth_date ? dayjs(user.birth_date) : null,
        bio: user.brief_introduction || '',
        avatar: user.avatar || ''
      })
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 头像上传前的验证
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    message.error('只能上传图片文件!')
    return false
  }
  
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    message.error('图片大小不能超过2MB!')
    return false
  }
  
  return true
}

// 处理头像上传
const handleAvatarUpload = async ({ file, onSuccess, onError }) => {
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await uploadAPI.uploadImage(formData)
    if (response.code === 200) {
      profileForm.avatar = response.data.url
      message.success('头像上传成功')
      onSuccess()
    } else {
      throw new Error(response.message || '上传失败')
    }
  } catch (error) {
    console.error('头像上传失败:', error)
    message.error('头像上传失败')
    onError(error)
  }
}

// 禁用未来日期
const disabledDate = (current) => {
  return current && current > dayjs().endOf('day')
}

// 提交个人信息
const handleProfileSubmit = async () => {
  try {
    profileLoading.value = true
    
    const data = {
      phone: profileForm.phone,
      email: profileForm.email,
      real_name: profileForm.realName,
      gender: profileForm.gender,
      birth_date: profileForm.birthday ? profileForm.birthday.format('YYYY-MM-DD') : null,
      brief_introduction: profileForm.bio,
      avatar: profileForm.avatar
    }

    const response = await authAPI.updateProfile(data)
    if (response.code === 200) {
      message.success('个人信息更新成功')
      // 更新本地存储的用户信息
      const userInfo = JSON.parse(localStorage.getItem('user') || '{}')
      Object.assign(userInfo, data)
      localStorage.setItem('user', JSON.stringify(userInfo))
    } else {
      throw new Error(response.message || '更新失败')
    }
  } catch (error) {
    console.error('更新个人信息失败:', error)
    message.error(error.message || '更新个人信息失败')
  } finally {
    profileLoading.value = false
  }
}

// 提交密码修改
const handlePasswordSubmit = async () => {
  try {
    passwordLoading.value = true
    
    const data = {
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword
    }

    const response = await authAPI.changePassword(data)
    if (response.code === 200) {
      message.success('密码修改成功')
      resetPasswordForm()
    } else {
      throw new Error(response.message || '密码修改失败')
    }
  } catch (error) {
    console.error('密码修改失败:', error)
  } finally {
    passwordLoading.value = false
  }
}

// 重置个人信息表单
const resetProfileForm = () => {
  getCurrentUser()
}

// 重置密码表单
const resetPasswordForm = () => {
  Object.assign(passwordForm, {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  passwordFormRef.value?.clearValidate()
}

onMounted(() => {
  getCurrentUser()
})
</script>

<style lang="scss" scoped>
.profile-page {
  min-height: 100vh;
  background: #f0f2f5;
}

.profile-banner {
  background: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  padding: 16px;
  margin-bottom: 12px;
}

.banner-content {
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-overview {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar-wrapper {
  position: relative;
  cursor: pointer;
}

.user-avatar {
  border: 2px solid #f0f0f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.avatar-edit {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 28px;
  height: 28px;
  background: #1890ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  border: 2px solid white;
  transition: all 0.2s;

  &:hover {
    background: #40a9ff;
    transform: scale(1.05);
  }
}

.user-details {
  color: #333;
}

.user-name {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: #1890ff;
}

.user-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0 0 12px 0;
}

.user-badges {
  display: flex;
  gap: 8px;
}

.info-tag {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  border: 1px solid #d9d9d9;
}

.quick-stats {
  display: flex;
  gap: 16px;
}

.stat-card {
  background: #fafafa;
  border: 1px solid #f0f0f0;
  padding: 16px;
  border-radius: 4px;
  text-align: center;
  min-width: 100px;
}

.stat-number {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.profile-content {
  margin: 0 auto;
}

.content-container {
  display: flex;
  gap: 16px;
  background: white;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.sidebar-nav {
  width: 220px;
  background: #fafafa;
  border-right: 1px solid #f0f0f0;
  padding: 24px 0;
}

.nav-menu {
  padding: 0 16px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  margin-bottom: 4px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  color: #333;

  &:hover {
    background: rgba(24, 144, 255, 0.1);
    color: #1890ff;
  }

  &.active {
    background: #1890ff;
    color: white;
  }
}

.nav-icon {
  font-size: 16px;
}

.main-content {
  flex: 1;
  padding: 24px;
}

.content-section {
  animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-header {
  margin-bottom: 20px;

  h2 {
    font-size: 20px;
    font-weight: 600;
    color: #333;
    margin: 0 0 4px 0;
  }

  p {
    font-size: 14px;
    color: #666;
    margin: 0;
  }
}

.form-container {
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  padding: 24px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  position: relative;

  &.full-width {
    grid-column: 1 / -1;
  }
}

.form-input, .form-textarea {
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  transition: all 0.2s;

  &:focus {
    border-color: #1890ff;
    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
  }
}

.input-tip {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

.gender-radio {
  margin-right: 16px;
  font-weight: normal;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-start;
  margin-top: 20px;
}

.action-btn {
  min-width: 100px;
  border-radius: 4px;
  font-weight: 500;
  transition: all 0.2s;

  &.primary {
    background: #1890ff;
    border-color: #1890ff;

    &:hover {
      background: #40a9ff;
      border-color: #40a9ff;
      transform: translateY(-1px);
    }
  }
}

.password-form-wrapper {
  max-width: 400px;
  margin: 0 auto;
}

.password-form .form-group {
  margin-bottom: 16px;
}

.security-grid {
  display: grid;
  gap: 16px;
}

.security-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  transition: all 0.2s;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-1px);
  }

  &.disabled {
    opacity: 0.6;
  }
}

.security-icon {
  width: 48px;
  height: 48px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.security-content {
  flex: 1;
}

.security-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.security-desc {
  font-size: 14px;
  color: #666;
}

.status-tag {
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 2px;
}

.security-btn {
  border-radius: 4px;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .content-container {
    flex-direction: column;
  }
  
  .sidebar-nav {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .nav-menu {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 0 16px;
  }
  
  .nav-item {
    flex-shrink: 0;
    margin-bottom: 0;
  }
}

@media (max-width: 768px) {
  .banner-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .user-overview {
    flex-direction: column;
    gap: 12px;
  }
  
  .quick-stats {
    justify-content: center;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .main-content {
    padding: 16px;
  }
  
  .form-container {
    padding: 16px;
  }
  
  .profile-content {
    padding: 0 12px 16px;
  }
  
  .banner-content {
    padding: 0 12px;
  }
}
</style> 