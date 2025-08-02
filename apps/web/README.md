# 心理健康平台 Web 前端

## 项目简介

这是心理健康平台的Web前端项目，基于Vue 3和Vite构建。

## 技术栈

- Vue 3
- Vue Router 4
- Ant Design Vue 4
- Axios
- Vite

## 开发指南

### 环境要求

- Node.js 16+
- npm 7+ 或 pnpm 7+

### 安装依赖

```bash
# 使用npm
npm install

# 或使用pnpm
pnpm install
```

### 开发服务器

```bash
# 使用npm
npm run dev

# 或使用pnpm
pnpm dev
```

### 构建生产版本

```bash
# 使用npm
npm run build

# 或使用pnpm
pnpm build
```

### 预览生产构建

```bash
# 使用npm
npm run preview

# 或使用pnpm
pnpm preview
```

## 项目结构

- `public/` - 静态资源目录
  - `index.html` - 静态HTML模板（已废弃，使用根目录的index.html）
- `src/` - 源代码目录
  - `api/` - API请求模块
  - `assets/` - 静态资源
  - `components/` - 公共组件
  - `router/` - 路由配置
  - `views/` - 页面组件
    - `admin/` - 管理后台页面
- `index.html` - 应用入口HTML文件

## Vite配置说明

本项目使用Vite作为构建工具，主要配置包括：

1. 入口文件位置：使用项目根目录的`index.html`作为入口文件
2. 开发服务器端口：8081
3. API代理：将`/api`请求代理到后端服务器，并移除`/api`前缀
4. 路径别名：`@`指向`src`目录

## 环境变量

- `VITE_APP_TITLE` - 应用标题
- `VITE_APP_API_URL` - API服务器地址
