# 登录页面设置说明

## 功能概述

已为心理健康平台的 Web 应用完成了登录页面的开发，包含以下功能：

### 主要功能
1. **用户登录** - 用户名/密码登录
2. **验证码支持** - 可选的图形验证码
3. **表单验证** - 前端表单校验
4. **记住密码** - 本地存储选项
5. **路由守卫** - 自动跳转和权限控制
6. **响应式设计** - 适配移动设备

### 技术栈
- Vue 3 + Composition API
- Vue Router 4
- Ant Design Vue 4.x
- Axios (HTTP请求)

## 文件结构

```
src/
├── views/
│   ├── Login.vue           # 登录页面组件
│   └── Home.vue           # 首页组件
├── router/
│   └── index.js           # 路由配置
├── utils/
│   └── api.js             # API请求工具
├── App.vue                # 主应用组件
└── main.js                # 应用入口
```

## 使用说明

### 1. 启动开发服务器

```bash
cd apps/web
pnpm install  # 如果还未安装依赖
pnpm run serve
```

### 2. 访问登录页面

默认访问 `http://localhost:8080` 会自动跳转到登录页面 `/login`

### 3. 登录功能

- **用户名**: 输入注册的用户名（3-20个字符）
- **密码**: 输入密码（至少6个字符）
- **验证码**: 点击"显示验证码"链接可启用验证码功能
- **记住密码**: 可选择记住登录状态

### 4. 后端API对接

登录页面会调用以下后端API端点：

- `POST /auth/login` - 用户登录
- `GET /auth/verify-code` - 获取验证码
- `POST /auth/logout` - 用户登出
- `GET /auth/profile` - 获取用户信息

确保后端服务运行在 `http://localhost:5000`

## 配置说明

### API基础URL配置

在 `src/utils/api.js` 中可以修改API基础URL：

```javascript
const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000',
  // ...
})
```

### 路由配置

在 `src/router/index.js` 中配置路由规则：

```javascript
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  // ...
]
```

## 安全特性

1. **Token认证** - 使用JWT token进行身份验证
2. **路由守卫** - 未登录用户自动跳转到登录页
3. **自动登出** - Token过期或401错误时自动清除登录状态
4. **XSS防护** - 表单输入验证和转义

## 样式说明

- 使用渐变背景色营造现代感
- 卡片式布局增强视觉层次
- 响应式设计适配各种屏幕尺寸
- 悬停动效提升用户体验

## 后续扩展

可以基于此登录页面继续开发：

1. **注册页面** - 用户注册功能
2. **忘记密码** - 密码重置流程
3. **社交登录** - 第三方登录集成
4. **双因子认证** - 短信/邮箱验证
5. **用户中心** - 个人信息管理

## 注意事项

1. 确保后端API正常运行
2. 检查网络请求的CORS配置
3. 生产环境需要配置正确的API地址
4. 建议启用HTTPS保护用户数据安全 