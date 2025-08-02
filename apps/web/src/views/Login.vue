<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <div class="login-header">
        <h1>心理健康平台</h1>
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
              <user-outlined />
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
              <lock-outlined />
            </template>
          </a-input-password>
        </a-form-item>
        
        <a-form-item name="verifyCode" v-if="showVerifyCode">
          <div class="verify-code-container">
            <a-input
              v-model:value="formState.verifyCode"
              size="large"
              placeholder="验证码"
              style="width: 70%"
            />
            <div class="verify-code-img" @click="refreshVerifyCode">
              <img v-if="verifyCodeUrl" :src="verifyCodeUrl" alt="验证码" />
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

<script>
import { defineComponent, reactive, ref } from 'vue';
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { useRouter } from 'vue-router';
import { authAPI } from '@/api/admin';

export default defineComponent({
  name: 'Login',
  components: {
    UserOutlined,
    LockOutlined,
  },
  setup() {
    const router = useRouter();
    const loading = ref(false);
    const showVerifyCode = ref(false);
    const verifyCodeUrl = ref('');
    
    const formState = reactive({
      username: '',
      password: '',
      verifyCode: '',
      remember: true,
    });
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度必须在3-20个字符之间', trigger: 'blur' },
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        // { min: 6, max: 20, message: '密码长度必须在6-20个字符之间', trigger: 'blur' },
      ],
      verifyCode: [
        { required: showVerifyCode.value, message: '请输入验证码', trigger: 'blur' },
      ],
    };
    
    const refreshVerifyCode = () => {
      // 调用后端验证码API
      verifyCodeUrl.value = authAPI.getVerifyCode();
    };
    
    const handleSubmit = async () => {
      loading.value = true;
      
      try {
        // 构建登录请求数据
        const loginData = {
          username: formState.username,
          password: formState.password
        };
        
        // 如果显示了验证码，则添加验证码参数
        if (showVerifyCode.value && formState.verifyCode) {
          loginData.verify_code = formState.verifyCode;
        }
        
        // 调用登录API
        const result = await authAPI.login(loginData);
        
        // 检查响应
        if (result.code === 200) {
          const { token, user } = result.data;
          
          // 存储token和用户信息
          localStorage.setItem('token', token);
          localStorage.setItem('user', JSON.stringify(user));
          
          // 如果记住密码，则存储用户名
          if (formState.remember) {
            localStorage.setItem('remembered_username', formState.username);
          } else {
            localStorage.removeItem('remembered_username');
          }
          
          message.success('登录成功');
          router.push('/');
        } else {
          // 处理错误响应
          message.error(result.message || '登录失败');
          // 显示验证码
          showVerifyCode.value = true;
          refreshVerifyCode();
        }
      } catch (error) {
        console.error('Login error:', error);
        const errorMsg = error.response?.data?.message || '登录失败，请稍后再试';
        message.error(errorMsg);
        
        // 显示验证码
        showVerifyCode.value = true;
        refreshVerifyCode();
      } finally {
        loading.value = false;
      }
    };
    
    // 初始化时，如果有记住的用户名，则填充
    const initForm = () => {
      const rememberedUsername = localStorage.getItem('remembered_username');
      if (rememberedUsername) {
        formState.username = rememberedUsername;
        formState.remember = true;
      }
    };
    
    // 初始化
    initForm();
    
    return {
      formState,
      rules,
      loading,
      showVerifyCode,
      verifyCodeUrl,
      handleSubmit,
      refreshVerifyCode,
    };
  },
});
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #1890ff 0%, #722ed1 100%);
}

.login-form-wrapper {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h1 {
  margin-bottom: 8px;
  color: #1890ff;
}

.login-header p {
  color: #666;
}

.login-form-button {
  width: 100%;
}

.login-form-forgot {
  float: right;
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
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.verify-code-placeholder {
  color: #999;
  font-size: 12px;
}
</style> 