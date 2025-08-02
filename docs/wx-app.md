# 心理咨询预约小程序（用户端）

## 项目介绍

这是一个基于 uni-app 开发的心理咨询预约小程序的用户端应用。该应用旨在为用户提供便捷的心理咨询服务预约平台，支持多端运行（微信小程序、H5等）。

## 主要功能

- 用户认证
  - 手机号验证码登录
  - 微信一键登录
  - 用户信息管理
  
- 咨询服务
  - 咨询师列表浏览
  - 咨询师详情查看
  - 在线预约咨询
  - 咨询记录管理
  
- 课程管理
  - 心理课程浏览
  - 课程收藏
  - 课程购买
  
- 订单系统
  - 咨询预约
  - 课程购买
  - 订单管理
  - 支付功能
  
- 用户互动
  - 收藏功能
  - 评价系统
  - 消息通知

## 技术栈

- 框架：uni-app (Vue 3)
- UI 组件：uview-plus ^3.4.24
- 工具库：
  - dayjs ^1.11.13（日期处理）
  - clipboard ^2.0.11（剪贴板操作）
- 样式处理：
  - sass ^1.63.2
  - sass-loader ^10.4.1

## 项目结构

```
├── api/                # API 接口
├── components/         # 公共组件
├── hooks/             # 自定义钩子
├── pages/             # 页面文件
├── static/            # 静态资源
├── store/             # 状态管理
├── utils/             # 工具函数
├── App.vue            # 应用入口组件
├── main.js            # 主入口文件
├── manifest.json      # 应用配置
├── pages.json         # 页面配置
└── uni.scss           # 全局样式
```

## 环境要求

- Node.js 16.x LTS（推荐 16.14.0 或以上）
- yarn 包管理器
- HBuilderX 3.0+（推荐）
- 微信开发者工具（用于小程序开发）

## 开发环境搭建

1. 安装 Node.js
```bash
# 推荐使用 nvm 管理 Node.js 版本
nvm install 16.14.0
nvm use 16.14.0

# 验证 Node.js 版本
node -v
```

2. 安装 yarn
```bash
npm install -g yarn

# 验证 yarn 版本
yarn -v
```

3. 安装开发工具
- 下载并安装 [HBuilderX](https://www.dcloud.io/hbuilderx.html)
- 下载并安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)

## 安装和运行

1. 克隆项目
```bash
git clone [项目地址]
```

2. 安装依赖
```bash
# 进入项目目录
cd ui-user

# 安装依赖
yarn install
```

3. 开发运行
- 使用 HBuilderX 导入项目
- 选择运行到要部署的平台（如：微信小程序、H5等）
- 或使用命令行：
```bash
# 运行到 H5
yarn dev:h5

# 运行到微信小程序
yarn dev:mp-weixin
```

## 部署说明

1. 微信小程序
- 在 manifest.json 中配置小程序的 AppID
- 使用 HBuilderX 发布到微信小程序
```bash
# 构建微信小程序
yarn build:mp-weixin
```

2. H5 部署
```bash
# 构建 H5 版本
yarn build:h5

# 将 dist/build/h5 目录下的文件部署到服务器
```

## 注意事项

- 首次运行需要在 manifest.json 中配置相应平台的信息
- 微信小程序需要在微信开发者工具中设置不校验合法域名
- API 接口地址需要在 /api 目录下配置
- 确保使用正确的 Node.js 版本（16.x）以避免兼容性问题
- 建议使用 yarn 而不是 npm 来管理依赖，以确保依赖版本的一致性

## 文档

- [API 文档](./api.md)
- [咨询师角色管理](./咨询师角色管理.md)

## 版本信息

当前版本：1.0.0

## License

[MIT License](LICENSE) 