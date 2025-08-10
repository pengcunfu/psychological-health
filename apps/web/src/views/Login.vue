<template>
  <div class="login-container">
    <!-- 装饰元素 -->
    <div class="decoration-elements">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
      <div class="floating-shape shape-4"></div>
      <div class="floating-shape shape-5"></div>
    </div>
    
    <div class="login-form-wrapper">
      <div class="login-header">
        <h1>美光心理管理后台</h1>
        <p>管理系统登录</p>
      </div>

      <a-form
          :model="formState"
          name="login"
          class="login-form"
          @finish="handleSubmit"
          :rules="rules"
      >
        <a-form-item name="username">
          <a-input
              v-model:value="formState.username"
              size="large"
              placeholder="用户名"
          >
            <template #prefix>
              <user-outlined/>
            </template>
          </a-input>
        </a-form-item>

        <a-form-item name="password">
          <a-input-password
              v-model:value="formState.password"
              size="large"
              placeholder="密码"
          >
            <template #prefix>
              <lock-outlined/>
            </template>
          </a-input-password>
        </a-form-item>

        <a-form-item name="verifyCode">
          <div class="verify-code-container">
            <a-input
                v-model:value="formState.verifyCode"
                size="large"
                placeholder="验证码"
                style="width: 70%"
            />
            <div class="verify-code-img" @click="refreshVerifyCode">
              <img v-if="verifyCodeUrl" :src="verifyCodeUrl" alt="验证码"/>
              <div v-else class="verify-code-placeholder">点击获取</div>
            </div>
          </div>
        </a-form-item>

        <a-form-item>
          <a-checkbox v-model:checked="formState.remember">
            记住我
          </a-checkbox>
          <a class="login-form-forgot" href="">
            忘记密码
          </a>
        </a-form-item>

        <a-form-item>
          <a-button
              type="primary"
              html-type="submit"
              size="large"
              class="login-form-button"
              :loading="loading"
          >
            登录
          </a-button>
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import { authAPI } from '@/api'

const router = useRouter()
const loading = ref(false)
const verifyCodeUrl = ref('')

const formState = reactive({
  username: '',
  password: '',
  verifyCode: '',
  remember: true,
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    // {min: 3, max: 20, message: '用户名长度必须在3-20个字符之间', trigger: 'blur'},
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    // { min: 6, max: 20, message: '密码长度必须在6-20个字符之间', trigger: 'blur' },
  ],
  verifyCode: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
  ],
}

const refreshVerifyCode = () => {
  // 调用后端验证码API
  verifyCodeUrl.value = authAPI.getVerifyCode()
}

const handleSubmit = async () => {
  loading.value = true

  try {
    // 构建登录请求数据
    const loginData = {
      username: formState.username,
      password: formState.password
    }

    // 添加验证码参数
    if (formState.verifyCode) {
      loginData.verify_code = formState.verifyCode
    }

    // 调用登录API
    const result = await authAPI.login(loginData)

    // 检查响应
    if (result.code === 200) {
      const { token, user } = result.data

      // 存储token和用户信息
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(user))

      // 如果记住密码，则存储用户名
      if (formState.remember) {
        localStorage.setItem('remembered_username', formState.username)
      } else {
        localStorage.removeItem('remembered_username')
      }

      message.success('登录成功')
      router.push('/')
    } else {
      // 刷新验证码
      refreshVerifyCode()
      // 清空验证码输入
      formState.verifyCode = ''
    }
  } catch (error) {
    console.error('Login error:', error)

    // 刷新验证码
    refreshVerifyCode()
    // 清空验证码输入
    formState.verifyCode = ''
  } finally {
    loading.value = false
  }
}

// 初始化时，如果有记住的用户名，则填充
const initForm = () => {
  const rememberedUsername = localStorage.getItem('remembered_username')
  if (rememberedUsername) {
    formState.username = rememberedUsername
    formState.remember = true
  }
}

// 页面挂载时初始化
onMounted(() => {
  initForm()
  refreshVerifyCode() // 页面加载时就获取验证码
})
</script>

<style lang="scss" scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  position: relative;
  overflow: hidden;
  
  // 主要渐变背景
  background: linear-gradient(
    135deg,
    #f8fafc 0%,
    #e2e8f0 25%,
    #cbd5e1 50%,
    #94a3b8 75%,
    #64748b 100%
  );
  
  // 动态背景装饰
  &::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: 
      radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.12) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.12) 0%, transparent 50%),
      radial-gradient(circle at 40% 40%, rgba(236, 72, 153, 0.12) 0%, transparent 50%);
    animation: float 20s ease-in-out infinite;
    z-index: 1;
  }
  
  // 装饰圆圈
  &::after {
    content: '';
    position: absolute;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: linear-gradient(45deg, rgba(34, 197, 94, 0.08), rgba(16, 185, 129, 0.05));
    top: -150px;
    right: -150px;
    z-index: 1;
    animation: rotate 30s linear infinite;
  }
}

// 添加浮动动画
@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  33% {
    transform: translate(30px, -30px) rotate(120deg);
  }
  66% {
    transform: translate(-20px, 20px) rotate(240deg);
  }
}

// 旋转动画
@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

// 添加更多装饰元素
.login-container {
  // 左下角装饰
  &:before {
    content: '';
    position: absolute;
    bottom: -100px;
    left: -100px;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(251, 146, 60, 0.1), rgba(249, 115, 22, 0.08));
    z-index: 1;
    animation: pulse 4s ease-in-out infinite alternate;
  }
}

// 脉冲动画
@keyframes pulse {
  from {
    transform: scale(1);
    opacity: 0.7;
  }
  to {
    transform: scale(1.1);
    opacity: 0.4;
  }
}

// 装饰元素容器
.decoration-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

// 浮动装饰形状
.floating-shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  border: none;
  
  &.shape-1 {
    width: 80px;
    height: 80px;
    top: 10%;
    left: 10%;
    background: linear-gradient(45deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.15));
    animation: float-up-down 6s ease-in-out infinite;
  }
  
  &.shape-2 {
    width: 60px;
    height: 60px;
    top: 20%;
    right: 15%;
    background: linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(219, 39, 119, 0.15));
    animation: float-left-right 8s ease-in-out infinite;
    animation-delay: -2s;
  }
  
  &.shape-3 {
    width: 100px;
    height: 100px;
    bottom: 15%;
    left: 8%;
    background: linear-gradient(225deg, rgba(34, 197, 94, 0.2), rgba(22, 163, 74, 0.15));
    animation: float-diagonal 10s ease-in-out infinite;
    animation-delay: -4s;
  }
  
  &.shape-4 {
    width: 40px;
    height: 40px;
    top: 60%;
    right: 25%;
    background: linear-gradient(315deg, rgba(251, 146, 60, 0.2), rgba(249, 115, 22, 0.15));
    animation: float-up-down 7s ease-in-out infinite;
    animation-delay: -1s;
  }
  
  &.shape-5 {
    width: 70px;
    height: 70px;
    bottom: 25%;
    right: 10%;
    background: linear-gradient(45deg, rgba(139, 92, 246, 0.2), rgba(124, 58, 237, 0.15));
    animation: float-left-right 9s ease-in-out infinite;
    animation-delay: -3s;
  }
}

// 浮动动画变体
@keyframes float-up-down {
  0%, 100% {
    transform: translateY(0px) scale(1);
  }
  50% {
    transform: translateY(-20px) scale(1.05);
  }
}

@keyframes float-left-right {
  0%, 100% {
    transform: translateX(0px) rotate(0deg);
  }
  50% {
    transform: translateX(15px) rotate(180deg);
  }
}

@keyframes float-diagonal {
  0%, 100% {
    transform: translate(0px, 0px) rotate(0deg);
  }
  25% {
    transform: translate(10px, -10px) rotate(90deg);
  }
  50% {
    transform: translate(20px, 0px) rotate(180deg);
  }
  75% {
    transform: translate(10px, 10px) rotate(270deg);
  }
}

.login-form-wrapper {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 2;
  border: 1px solid rgba(255, 255, 255, 0.3);
  
  // 添加微妙的内部光效
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.1) 0%,
      transparent 50%,
      rgba(255, 255, 255, 0.05) 100%
    );
    border-radius: 16px;
    pointer-events: none;
  }
}

.login-header {
  text-align: center;
  margin-bottom: 40px;

  h1 {
    margin-bottom: 8px;
    color: #1e293b;
    font-weight: 600;
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
  }

  p {
    color: #475569;
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.3);
  }
}

.login-form-button {
  width: 100%;
  height: 48px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border: none;
  box-shadow: 0 3px 12px rgba(59, 130, 246, 0.25);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  }
  
  &:active {
    transform: translateY(0);
    box-shadow: 0 3px 12px rgba(59, 130, 246, 0.25);
  }
  
  &:focus {
    outline: none;
    box-shadow: 0 3px 12px rgba(59, 130, 246, 0.25), 0 0 0 2px rgba(59, 130, 246, 0.2);
  }
}

.login-form-forgot {
  float: right;
  color: #64748b;
  text-decoration: none;
  transition: color 0.2s;

  &:hover {
    color: #334155;
    text-decoration: underline;
  }
}

.verify-code-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.verify-code-img {
  width: 28%;
  height: 40px;
  cursor: pointer;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.9);

  img {
    width: 100%;
    height: 100%;
    object-fit: contain; /* 保持原始比例，完整显示图片 */
    object-position: center;
  }
}

.verify-code-placeholder {
  color: #64748b;
  font-size: 12px;
}

// 深度选择器样式
:deep(.ant-form-item-label > label) {
  color: #334155 !important;
  font-weight: 500;
}

:deep(.ant-checkbox-wrapper) {
  color: #475569 !important;

  .ant-checkbox-inner {
    background-color: rgba(255, 255, 255, 0.9);
    border-color: #cbd5e1;
  }

  &:hover .ant-checkbox-inner {
    border-color: #3b82f6;
  }
}

:deep(.ant-input) {
  background-color: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 255, 255, 0.2);
  color: #333;
  border-radius: 8px;
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);

  &:focus {
    background-color: rgba(255, 255, 255, 0.95);
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
  }
  
  &:hover {
    border-color: rgba(255, 255, 255, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
}

:deep(.ant-input-affix-wrapper) {
  background-color: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);

  &:focus-within {
    background-color: rgba(255, 255, 255, 0.95);
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
  }
  
  &:hover {
    border-color: rgba(255, 255, 255, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
}

:deep(.ant-input-prefix) {
  color: #64748b;
}
</style> 